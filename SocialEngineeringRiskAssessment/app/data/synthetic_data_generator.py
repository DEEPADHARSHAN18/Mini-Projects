import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # Features
    security_training = np.random.choice([0, 1], size=num_samples, p=[0.4, 0.6]) # 1=Yes, 0=No
    mfa_enabled = np.random.choice([0, 1], size=num_samples, p=[0.3, 0.7])
    
    password_hygiene = np.random.choice(['Poor', 'Fair', 'Good'], size=num_samples, p=[0.2, 0.5, 0.3])
    social_media_exposure = np.random.choice(['Low', 'Medium', 'High'], size=num_samples, p=[0.4, 0.4, 0.2])
    sensitive_data_access = np.random.choice(['None', 'Limited', 'High'], size=num_samples, p=[0.3, 0.5, 0.2])
    policy_awareness = np.random.choice(['Low', 'Medium', 'High'], size=num_samples, p=[0.2, 0.5, 0.3])
    
    # Simulation behaviour
    clicked_link = np.random.choice([0, 1], size=num_samples, p=[0.7, 0.3])
    reported_phishing = np.where(clicked_link == 1, 
                                 np.random.choice([0, 1], size=num_samples, p=[0.9, 0.1]), 
                                 np.random.choice([0, 1], size=num_samples, p=[0.4, 0.6]))
    
    indicators_identified = np.where(clicked_link == 1,
                                     np.random.randint(0, 2, size=num_samples),
                                     np.random.randint(1, 6, size=num_samples))
    
    # Target: Risk Level (0=Low, 1=Medium, 2=High)
    # We will derive a logical target based on the features to make the model learn something sensible
    risk_score = np.zeros(num_samples)
    
    risk_score += np.where(security_training == 0, 15, 0)
    risk_score += np.where(mfa_enabled == 0, 20, 0)
    risk_score += np.where(password_hygiene == 'Poor', 15, np.where(password_hygiene == 'Fair', 5, 0))
    risk_score += np.where(social_media_exposure == 'High', 10, np.where(social_media_exposure == 'Medium', 5, 0))
    risk_score += np.where(sensitive_data_access == 'High', 10, 0)
    risk_score += np.where(policy_awareness == 'Low', 10, 0)
    
    risk_score += np.where(clicked_link == 1, 30, 0)
    risk_score -= np.where(reported_phishing == 1, 10, 0)
    risk_score -= (indicators_identified * 2)
    
    # Add some noise
    risk_score += np.random.normal(0, 5, size=num_samples)
    
    # Classify based on score thresholds (approximate)
    target = np.where(risk_score > 65, 2, np.where(risk_score > 35, 1, 0))
    
    df = pd.DataFrame({
        'security_training': security_training,
        'mfa_enabled': mfa_enabled,
        'password_hygiene': password_hygiene,
        'social_media_exposure': social_media_exposure,
        'sensitive_data_access': sensitive_data_access,
        'policy_awareness': policy_awareness,
        'clicked_link': clicked_link,
        'reported_phishing': reported_phishing,
        'indicators_identified': indicators_identified,
        'risk_level': target
    })
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'synthetic_dataset.csv')
    df.to_csv(file_path, index=False)
    print(f"Synthetic data generated at {file_path}")
    
if __name__ == "__main__":
    generate_synthetic_data()
