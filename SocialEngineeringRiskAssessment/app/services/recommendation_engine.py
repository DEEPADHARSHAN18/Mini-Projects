from app.database.models import RiskFactor, Recommendation

def identify_risk_factors(user, simulation_response=None):
    """
    Identifies specific risk factors based on user profile and behaviour.
    Returns a list of dictionaries.
    """
    factors = []
    
    if not user.mfa_enabled:
        factors.append({
            'factor': 'MFA Disabled',
            'severity': 'High',
            'explanation': 'Multi-factor authentication is not enabled, leaving the account vulnerable to credential theft.'
        })
        
    if not user.security_training:
        factors.append({
            'factor': 'No Security Training',
            'severity': 'Medium',
            'explanation': 'User has not completed mandatory security awareness training.'
        })
        
    if user.password_hygiene == 'Poor':
        factors.append({
            'factor': 'Poor Password Hygiene',
            'severity': 'High',
            'explanation': 'User reports reusing passwords across multiple accounts.'
        })
        
    if user.social_media_exposure == 'High':
        factors.append({
            'factor': 'High Social Media Exposure',
            'severity': 'Medium',
            'explanation': 'Publicly available information could be used for targeted spear-phishing.'
        })
        
    if simulation_response:
        if simulation_response.clicked:
            factors.append({
                'factor': 'Phishing Susceptibility',
                'severity': 'High',
                'explanation': 'User clicked a malicious link during a controlled simulation.'
            })
            
        if simulation_response.indicators_identified < 3:
            factors.append({
                'factor': 'Low Threat Recognition',
                'severity': 'Medium',
                'explanation': 'User failed to identify key suspicious indicators in a simulated attack.'
            })
            
    return factors

def generate_recommendations(risk_factors):
    """
    Generates actionable recommendations based on identified risk factors.
    Returns a list of dictionaries.
    """
    recommendations = []
    
    for factor in risk_factors:
        f_name = factor['factor']
        
        if f_name == 'MFA Disabled':
            recommendations.append({
                'recommendation': 'Enable Multi-Factor Authentication (MFA) immediately using an authenticator app or hardware token.',
                'priority': 'High'
            })
            
        elif f_name == 'No Security Training':
            recommendations.append({
                'recommendation': 'Assign and ensure completion of standard security awareness training module.',
                'priority': 'Medium'
            })
            
        elif f_name == 'Poor Password Hygiene':
            recommendations.append({
                'recommendation': 'Adopt a company-approved Password Manager and generate strong, unique passwords for all accounts.',
                'priority': 'High'
            })
            
        elif f_name == 'High Social Media Exposure':
            recommendations.append({
                'recommendation': 'Review social media privacy settings and reduce unnecessary public exposure of organizational affiliation.',
                'priority': 'Low'
            })
            
        elif f_name == 'Phishing Susceptibility':
            recommendations.append({
                'recommendation': 'Complete targeted anti-phishing training and participate in follow-up simulations within 30 days.',
                'priority': 'High'
            })
            
        elif f_name == 'Low Threat Recognition':
            recommendations.append({
                'recommendation': 'Review educational materials on identifying social engineering indicators (urgency, sender domains).',
                'priority': 'Medium'
            })
            
    return recommendations
