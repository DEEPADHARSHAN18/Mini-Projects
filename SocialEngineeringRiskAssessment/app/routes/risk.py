from flask import Blueprint, render_template, request, redirect, url_for
from app.database.database import db
from app.database.models import User, Simulation, SimulationResponse, RiskAssessment, RiskFactor, Recommendation
from app.services.risk_engine import evaluate_risk
from app.services.recommendation_engine import identify_risk_factors, generate_recommendations

bp = Blueprint('risk', __name__)

@bp.route('/evaluate/<int:sim_id>', methods=['GET'])
def evaluate(sim_id):
    simulation = Simulation.query.get_or_404(sim_id)
    user = User.query.get(simulation.user_id)
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()
    
    # 1. Run evaluation
    results = evaluate_risk(user, simulation, response)
    
    # 2. Save assessment
    assessment = RiskAssessment(
        user_id=user.id,
        simulation_id=simulation.id,
        profile_score=results['profile_score'],
        behavioural_score=results['behavioural_score'],
        awareness_score=results['awareness_score'],
        ml_probability=results['ml_probability'],
        final_risk_score=results['final_risk_score'],
        risk_level=results['risk_level']
    )
    db.session.add(assessment)
    db.session.flush() # Get ID
    
    # 3. Identify and save risk factors
    factors = identify_risk_factors(user, response)
    for f in factors:
        db.session.add(RiskFactor(
            assessment_id=assessment.id,
            factor=f['factor'],
            severity=f['severity'],
            explanation=f['explanation']
        ))
        
    # 4. Generate and save recommendations
    recommendations = generate_recommendations(factors)
    for r in recommendations:
        db.session.add(Recommendation(
            assessment_id=assessment.id,
            recommendation=r['recommendation'],
            priority=r['priority']
        ))
        
    db.session.commit()
    
    return redirect(url_for('risk.report', assessment_id=assessment.id))

@bp.route('/report/<int:assessment_id>', methods=['GET'])
def report(assessment_id):
    assessment = RiskAssessment.query.get_or_404(assessment_id)
    user = User.query.get(assessment.user_id)
    factors = RiskFactor.query.filter_by(assessment_id=assessment.id).all()
    recommendations = Recommendation.query.filter_by(assessment_id=assessment.id).all()
    
    return render_template('risk/evaluation.html', 
                           assessment=assessment, 
                           user=user, 
                           factors=factors, 
                           recommendations=recommendations)

@bp.route('/<int:user_id>', methods=['GET'])
def user_risk(user_id):
    from flask import abort, flash
    assessment = RiskAssessment.query.filter_by(user_id=user_id).order_by(RiskAssessment.created_at.desc()).first()
    if not assessment:
        flash("No risk assessment found for this user.")
        return redirect(url_for('users.details', user_id=user_id))
    return redirect(url_for('risk.report', assessment_id=assessment.id))

