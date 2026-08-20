from app.ml.predict import predict_risk

def calculate_profile_score(user):
    """Calculates risk score purely based on profile attributes (0-100)"""
    score = 0
    
    if not user.security_training:
        score += 20
        
    if not user.mfa_enabled:
        score += 25
        
    if user.password_hygiene == 'Poor':
        score += 20
    elif user.password_hygiene == 'Fair':
        score += 10
        
    if user.social_media_exposure == 'High':
        score += 15
    elif user.social_media_exposure == 'Medium':
        score += 5
        
    if user.sensitive_data_access == 'High':
        score += 10
        
    if user.security_policy_awareness == 'Low':
        score += 10
        
    return min(100, score)

def evaluate_risk(user, simulation=None, simulation_response=None):
    """
    Complete risk evaluation pipeline combining profile, simulation, and ML.
    """
    
    # 1. Profile Risk
    profile_score = calculate_profile_score(user)
    
    # 2. Behavioural Risk (from simulation if available)
    behavioural_score = 0
    awareness_score = 100
    if simulation_response:
        from app.services.simulation_engine import calculate_awareness_score
        awareness_score = calculate_awareness_score(simulation_response)
        
        # Invert awareness score to get a risk score (0-100)
        behavioural_score = 100 - awareness_score
    else:
        # Default to a moderate risk if no simulation has been done yet
        behavioural_score = 50 
        
    # 3. Machine Learning Prediction
    ml_result = predict_risk(user, simulation_response)
    ml_probability = ml_result['probability'] * 100 # Convert to percentage
    
    # 4. Final Combination
    # Weighting: Profile (30%), Behaviour (30%), ML Prediction (40%)
    final_score = (profile_score * 0.3) + (behavioural_score * 0.3) + (ml_probability * 0.4)
    final_score = round(final_score, 2)
    
    # 5. Risk Classification
    if final_score >= 70:
        risk_level = 'HIGH'
    elif final_score >= 40:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
        
    return {
        'profile_score': profile_score,
        'behavioural_score': behavioural_score,
        'awareness_score': awareness_score,
        'ml_probability': ml_probability,
        'final_risk_score': final_score,
        'risk_level': risk_level
    }
