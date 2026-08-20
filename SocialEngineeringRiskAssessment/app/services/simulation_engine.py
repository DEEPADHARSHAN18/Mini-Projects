def calculate_awareness_score(response):
    score = 100
    
    if response.clicked:
        score -= 50
        
    if response.reported:
        score += 20
        
    # Award points for identifying indicators
    if response.indicators_identified > 0:
        score += (response.indicators_identified * 10)
        
    # Cap at 100
    if score > 100:
        score = 100
    elif score < 0:
        score = 0
        
    return score
