from datetime import datetime
from app.database.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.String(50), nullable=False) # e.g., Junior, Mid, Senior
    security_training = db.Column(db.Boolean, default=False)
    last_training_date = db.Column(db.DateTime, nullable=True)
    mfa_enabled = db.Column(db.Boolean, default=False)
    password_hygiene = db.Column(db.String(50), nullable=False) # e.g., Poor, Fair, Good
    social_media_exposure = db.Column(db.String(50), nullable=False) # e.g., Low, Medium, High
    sensitive_data_access = db.Column(db.String(50), nullable=False) # e.g., None, Limited, Full
    remote_work_frequency = db.Column(db.String(50), nullable=False) # e.g., Never, Occasional, Full-time
    security_policy_awareness = db.Column(db.String(50), nullable=False) # e.g., Low, Medium, High
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    simulations = db.relationship('Simulation', backref='user', lazy=True)
    assessments = db.relationship('RiskAssessment', backref='user', lazy=True)

class Simulation(db.Model):
    __tablename__ = 'simulations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scenario_type = db.Column(db.String(50), nullable=False) # e.g., Phishing
    scenario_name = db.Column(db.String(100), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='In Progress') # e.g., In Progress, Completed
    
    # Relationships
    response = db.relationship('SimulationResponse', backref='simulation', uselist=False, lazy=True)

class SimulationResponse(db.Model):
    __tablename__ = 'simulation_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=False)
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    reported = db.Column(db.Boolean, default=False)
    analyzed = db.Column(db.Boolean, default=False)
    indicators_identified = db.Column(db.Integer, default=0)
    response_time = db.Column(db.Integer, nullable=True) # in seconds
    final_decision = db.Column(db.String(50), nullable=True) # e.g., Clicked Link, Reported, Ignored

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id'), nullable=True)
    profile_score = db.Column(db.Float, nullable=False)
    behavioural_score = db.Column(db.Float, nullable=True)
    awareness_score = db.Column(db.Float, nullable=True)
    ml_probability = db.Column(db.Float, nullable=True)
    final_risk_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False) # LOW, MEDIUM, HIGH
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    risk_factors = db.relationship('RiskFactor', backref='assessment', lazy=True)
    recommendations = db.relationship('Recommendation', backref='assessment', lazy=True)

class RiskFactor(db.Model):
    __tablename__ = 'risk_factors'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('risk_assessments.id'), nullable=False)
    factor = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False) # e.g., Low, Medium, High
    explanation = db.Column(db.Text, nullable=False)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('risk_assessments.id'), nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False) # e.g., Low, Medium, High
