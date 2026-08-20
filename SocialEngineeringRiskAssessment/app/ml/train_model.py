import pandas as pd
import numpy as np
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_model():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(base_dir, 'data', 'synthetic_dataset.csv')
    
    if not os.path.exists(data_path):
        print("Data not found. Run synthetic_data_generator.py first.")
        return
        
    df = pd.read_csv(data_path)
    
    X = df.drop('risk_level', axis=1)
    y = df['risk_level']
    
    # Define categorical and numerical features
    categorical_features = ['password_hygiene', 'social_media_exposure', 'sensitive_data_access', 'policy_awareness']
    numerical_features = ['security_training', 'mfa_enabled', 'clicked_link', 'reported_phishing', 'indicators_identified']
    
    # Create preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    # Create pipeline with preprocessing and model
    # Use class_weight='balanced' in case our synthetic data is imbalanced
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42, max_iter=1000, class_weight='balanced'))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    # Save the model
    model_dir = os.path.join(base_dir, 'ml', 'model')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'risk_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
