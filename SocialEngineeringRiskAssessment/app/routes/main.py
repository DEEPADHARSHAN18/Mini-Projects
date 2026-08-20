from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

from app.database.models import User, RiskAssessment
from sqlalchemy import func

@bp.route('/dashboard')
def dashboard():
    users = User.query.all()
    total_users = len(users)
    
    assessments = RiskAssessment.query.all()
    
    high_risk = len([a for a in assessments if a.risk_level == 'HIGH'])
    medium_risk = len([a for a in assessments if a.risk_level == 'MEDIUM'])
    low_risk = len([a for a in assessments if a.risk_level == 'LOW'])
    
    avg_score = 0
    if assessments:
        avg_score = round(sum(a.final_risk_score for a in assessments) / len(assessments), 1)
        
    stats = {
        'total_users': total_users,
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk,
        'avg_score': avg_score
    }
    return render_template('dashboard.html', stats=stats)
