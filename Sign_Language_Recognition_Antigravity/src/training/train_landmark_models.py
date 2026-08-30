import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, classification_report, f1_score, 
    confusion_matrix, ConfusionMatrixDisplay, precision_recall_fscore_support
)

from src.config.settings import DATASET_DIR, METRICS_DIR, MODELS_DIR

# Define new directories for outputs
CONFUSION_MATRICES_DIR = Path("outputs/confusion_matrices")
PLOTS_DIR = Path("outputs/plots")
LANDMARK_MODELS_DIR = MODELS_DIR / "landmark"

# Create directories
for d in [CONFUSION_MATRICES_DIR, PLOTS_DIR, LANDMARK_MODELS_DIR, METRICS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def train_and_evaluate():
    # 1. DATA LOADING
    print("Loading dataset...")
    data_path = DATASET_DIR / "landmarks" / "landmarks.csv"
    df = pd.read_csv(data_path)
    
    # Automatically identify feature columns (those starting with x, y, z followed by a number)
    feature_cols = [col for col in df.columns if col.startswith(('x', 'y', 'z')) and col[1:].isdigit()]
    
    assert len(feature_cols) == 63, f"Expected 63 features, found {len(feature_cols)}"
    
    X = df[feature_cols].values
    y = df['class'].values
    
    # 2. TRAIN/VALIDATION SPLIT
    print("Splitting dataset...")
    # Separate classes with > 1 samples for stratified splitting
    value_counts = pd.Series(y).value_counts()
    valid_classes = value_counts[value_counts > 1].index
    
    mask = np.isin(y, valid_classes)
    X_valid, y_valid = X[mask], y[mask]
    X_invalid, y_invalid = X[~mask], y[~mask]
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_valid, y_valid, test_size=0.2, random_state=42, stratify=y_valid
    )
    
    # Add the invalid classes (e.g. 'nothing') to both or just validation
    # We will add it to validation so it shows up in the evaluation report
    if len(X_invalid) > 0:
        X_val = np.vstack([X_val, X_invalid])
        y_val = np.concatenate([y_val, y_invalid])
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Number of classes: {len(np.unique(y))}")
    print(f"Class distribution (train): {pd.Series(y_train).value_counts().to_dict()}")
    
    # 3. MODELS & 4. PREPROCESSING
    # SVM and MLP need scaled features; RF does not
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'SVM': Pipeline([
            ('scaler', StandardScaler()),
            ('svm', SVC(kernel='rbf', probability=True, random_state=42))
        ]),
        'MLP': Pipeline([
            ('scaler', StandardScaler()),
            ('mlp', MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=300, random_state=42, early_stopping=True))
        ])
    }
    
    results = []
    best_model_name = None
    best_f1 = -1
    best_model = None
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # 5. EVALUATION
        y_pred = model.predict(X_val)
        acc = accuracy_score(y_val, y_pred)
        macro_f1 = f1_score(y_val, y_pred, average='macro')
        weighted_f1 = f1_score(y_val, y_pred, average='weighted')
        
        print(f"{name} Results:")
        print(f"Accuracy: {acc:.4f} | Macro F1: {macro_f1:.4f} | Weighted F1: {weighted_f1:.4f}")
        
        # Generate classification report
        report_dict = classification_report(y_val, y_pred, output_dict=True, zero_division=0)
        report_df = pd.DataFrame(report_dict).transpose()
        report_df.to_csv(METRICS_DIR / f"{name}_classification_report.csv")
        
        # Save confusion matrix plot
        cm = confusion_matrix(y_val, y_pred, labels=np.unique(y))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y))
        fig, ax = plt.subplots(figsize=(20, 20))
        disp.plot(ax=ax, cmap='viridis', xticks_rotation=90)
        plt.title(f"Confusion Matrix: {name}")
        plt.tight_layout()
        plt.savefig(CONFUSION_MATRICES_DIR / f"{name}_confusion_matrix.png")
        plt.close()
        
        results.append({
            'model': name,
            'accuracy': acc,
            'macro_f1': macro_f1,
            'weighted_f1': weighted_f1
        })
        
        # 8. SAVE MODELS
        joblib.dump(model, LANDMARK_MODELS_DIR / f"{name}_baseline.pkl")
        
        if macro_f1 > best_f1:
            best_f1 = macro_f1
            best_model_name = name
            best_model = model
            
    # 7. MODEL COMPARISON
    results_df = pd.DataFrame(results).sort_values(by='macro_f1', ascending=False)
    results_df.to_csv(METRICS_DIR / "landmark_model_comparison.csv", index=False)
    print("\nModel Comparison:")
    print(results_df)
    print(f"\nBest model based on Macro F1: {best_model_name}")
    
    # 10. SANITY CHECK
    print(f"\nPerforming Sanity Check with {best_model_name}...")
    # Take 5 random samples from validation set
    np.random.seed(99)
    sample_indices = np.random.choice(len(X_val), 5, replace=False)
    
    for idx in sample_indices:
        x_sample = X_val[idx].reshape(1, -1)
        true_label = y_val[idx]
        pred_label = best_model.predict(x_sample)[0]
        try:
            proba = best_model.predict_proba(x_sample)[0]
            confidence = np.max(proba)
            conf_str = f"{confidence:.4f}"
        except AttributeError:
            conf_str = "N/A"
            
        print(f"Actual: {true_label:10s} | Predicted: {pred_label:10s} | Confidence: {conf_str}")

if __name__ == "__main__":
    train_and_evaluate()
