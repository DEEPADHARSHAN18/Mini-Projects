import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input, RandomRotation, RandomZoom, RandomTranslation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
import cv2

# Ensure reproducibility
SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

from src.config.settings import RAW_DATA_DIR, METRICS_DIR, MODELS_DIR

# Paths
IMAGE_MODELS_DIR = MODELS_DIR / "image"
CONFUSION_MATRICES_DIR = Path("outputs/confusion_matrices")
PLOTS_DIR = Path("outputs/plots")
PREDICTIONS_DIR = Path("outputs/predictions")

for d in [IMAGE_MODELS_DIR, CONFUSION_MATRICES_DIR, PLOTS_DIR, PREDICTIONS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Hyperparameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 29
EPOCHS_STAGE1 = 5
EPOCHS_STAGE2 = 3

def build_model():
    # Data Augmentation (No horizontal flip to preserve sign handedness)
    data_augmentation = tf.keras.Sequential([
        RandomRotation(0.1, seed=SEED),
        RandomZoom(0.1, seed=SEED),
        RandomTranslation(height_factor=0.1, width_factor=0.1, seed=SEED)
    ], name="data_augmentation")

    inputs = Input(shape=IMG_SIZE + (3,))
    
    # Preprocessing expected by MobileNetV2
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    
    # Augmentation
    x = data_augmentation(x)
    
    # Base model
    base_model = MobileNetV2(input_shape=IMG_SIZE + (3,), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze base model for stage 1
    
    x = base_model(x, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2, seed=SEED)(x)
    outputs = Dense(NUM_CLASSES, activation='softmax')(x)
    
    model = Model(inputs, outputs)
    return model, base_model

def train_and_evaluate():
    print("1. Loading and Splitting Dataset...")
    
    # Using tf.keras.utils.image_dataset_from_directory
    train_ds = tf.keras.utils.image_dataset_from_directory(
        RAW_DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        RAW_DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode='categorical'
    )
    
    class_names = train_ds.class_names
    print(f"Classes found ({len(class_names)}):", class_names)
    
    # Pre-fetch for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
    
    # Build model
    model, base_model = build_model()
    
    print("\n2. Stage 1: Training Classification Head...")
    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    best_model_path = IMAGE_MODELS_DIR / "asl_mobilenetv2_baseline.keras"
    
    callbacks_stage1 = [
        EarlyStopping(patience=1, restore_best_weights=True, monitor='val_accuracy'),
        ModelCheckpoint(filepath=best_model_path, save_best_only=True, monitor='val_accuracy')
    ]
    
    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_STAGE1,
        callbacks=callbacks_stage1
    )
    
    print("\n3. Stage 2: Fine-Tuning Top Layers...")
    # Load best weights from Stage 1 to ensure Stage 2 starts from the best baseline
    if best_model_path.exists():
        model.load_weights(best_model_path)
        
    # Unfreeze the top layers of the base model
    base_model.trainable = True
    # Fine-tune from this layer onwards
    fine_tune_at = 100
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False
        
    model.compile(
        optimizer=Adam(learning_rate=1e-5),  # Lower learning rate
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Ensure Stage 2 only overwrites the checkpoint if it actually beats Stage 1
    best_stage1_acc = max(history1.history['val_accuracy'])
    
    callbacks_stage2 = [
        EarlyStopping(patience=1, restore_best_weights=True, monitor='val_accuracy'),
        ReduceLROnPlateau(factor=0.2, patience=1, min_lr=1e-7, monitor='val_accuracy'),
        ModelCheckpoint(
            filepath=best_model_path, 
            save_best_only=True, 
            monitor='val_accuracy',
            initial_value_threshold=best_stage1_acc
        )
    ]
    
    history2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_STAGE2,
        callbacks=callbacks_stage2
    )
    
    print("\n4. Evaluation...")
    # Get true labels and predictions
    y_true = []
    y_pred = []
    
    print("Running predictions on validation set...")
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    weighted_f1 = f1_score(y_true, y_pred, average='weighted')
    
    print(f"Validation Accuracy: {acc:.4f}")
    print(f"Validation Macro F1: {macro_f1:.4f}")
    print(f"Validation Weighted F1: {weighted_f1:.4f}")
    
    report_dict = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    report_df.to_csv(METRICS_DIR / "image_model_classification_report.csv")
    
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(22, 20))
    sns.heatmap(cm, annot=False, cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix: MobileNetV2 Image Model')
    plt.ylabel('True Class')
    plt.xlabel('Predicted Class')
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRICES_DIR / "image_model_confusion_matrix.png")
    plt.close()
    
    # 5. INFERENCE TEST & VISUALIZATION
    print("\n5. Inference Test & Visualization...")
    # Classes of interest
    target_classes = ['A', 'M', 'N', 'space', 'nothing', 'del']
    target_indices = [class_names.index(c) for c in target_classes if c in class_names]
    
    found_examples = {c: False for c in target_classes}
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    plot_idx = 0
    
    # Find one example for each target class
    for images, labels in val_ds:
        if all(found_examples.values()):
            break
            
        true_batch = np.argmax(labels.numpy(), axis=1)
        preds_batch = model.predict(images, verbose=0)
        pred_labels = np.argmax(preds_batch, axis=1)
        
        for i in range(len(true_batch)):
            true_idx = true_batch[i]
            true_class = class_names[true_idx]
            
            if true_class in target_classes and not found_examples[true_class]:
                pred_class = class_names[pred_labels[i]]
                conf = np.max(preds_batch[i])
                
                print(f"Actual: {true_class:10s} | Predicted: {pred_class:10s} | Confidence: {conf:.4f}")
                
                img = images[i].numpy().astype("uint8")
                
                ax = axes[plot_idx]
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                ax.set_title(f"True: {true_class} | Pred: {pred_class}\nConf: {conf:.4f}")
                ax.axis('off')
                
                found_examples[true_class] = True
                plot_idx += 1
                
                if plot_idx >= 6:
                    break
                    
    plt.tight_layout()
    plt.savefig(PREDICTIONS_DIR / "image_model_predictions.png")
    plt.close()
    
    # Find most confused pairs
    np.fill_diagonal(cm, 0) # Ignore correct predictions
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    stacked = cm_df.stack().reset_index()
    stacked.columns = ['True', 'Predicted', 'Count']
    stacked = stacked[stacked['Count'] > 0]
    top_confusions = stacked.sort_values(by='Count', ascending=False).head(10)
    
    print("\nMost Confused Pairs:")
    print(top_confusions.to_string(index=False))
    top_confusions.to_csv(METRICS_DIR / "image_model_top_confused_pairs.csv", index=False)

if __name__ == "__main__":
    train_and_evaluate()
