import os
import joblib
import pandas as pd

def predict_risk(user_data, simulation_response=None):
    """
    Predicts the risk level using the trained ML model.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    model_path = os.path.join(base_dir, 'ml', 'model', 'risk_model.pkl')
    
    if not os.path.exists(model_path):
        # Fallback if model isn't trained yet
        return {
            'probability': 0.5,
            'class': 1, # Medium
            'level': 'MEDIUM'
        }
        
    model = joblib.load(model_path)
    
    # Prepare data dictionary matching the training features
    data = {
        'security_training': [1 if user_data.security_training else 0],
        'mfa_enabled': [1 if user_data.mfa_enabled else 0],
        'password_hygiene': [user_data.password_hygiene],
        'social_media_exposure': [user_data.social_media_exposure],
        'sensitive_data_access': [user_data.sensitive_data_access],
        'policy_awareness': [user_data.security_policy_awareness],
        
        # Default simulation values if no simulation has been run yet
        'clicked_link': [0],
        'reported_phishing': [1],
        'indicators_identified': [3]
    }
    
    # Override with actual simulation data if available
    if simulation_response:
        data['clicked_link'] = [1 if simulation_response.clicked else 0]
        data['reported_phishing'] = [1 if simulation_response.reported else 0]
        data['indicators_identified'] = [simulation_response.indicators_identified]
        
    df = pd.DataFrame(data)
    
    # Predict
    pred_class = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]
    
    # Map class to level
    # 0 = Low, 1 = Medium, 2 = High
    risk_mapping = {0: 'LOW', 1: 'MEDIUM', 2: 'HIGH'}
    risk_level = risk_mapping.get(pred_class, 'MEDIUM')
    
    # The probability of the predicted class or the "high risk" class
    # Let's return the probability of being High Risk for consistency in score calculation
    high_risk_prob = probabilities[2] if len(probabilities) > 2 else probabilities[-1]
    
    return {
        'probability': float(high_risk_prob),
        'class': int(pred_class),
        'level': risk_level,
        'probabilities': probabilities.tolist()
    }
