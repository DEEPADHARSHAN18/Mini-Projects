from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database.database import db
from app.database.models import User

bp = Blueprint('users', __name__)

@bp.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@bp.route('/create', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        try:
            # Extract form data
            employee_id = request.form.get('employee_id')
            name = request.form.get('name')
            department = request.form.get('department')
            role = request.form.get('role')
            experience_level = request.form.get('experience_level')
            remote_work_frequency = request.form.get('remote_work_frequency')
            
            security_training_str = request.form.get('security_training')
            security_training = True if security_training_str == 'Yes' else False
            
            mfa_enabled_str = request.form.get('mfa_enabled')
            mfa_enabled = True if mfa_enabled_str == 'Yes' else False
            
            password_hygiene = request.form.get('password_hygiene')
            social_media_exposure = request.form.get('social_media_exposure')
            sensitive_data_access = request.form.get('sensitive_data_access')
            security_policy_awareness = request.form.get('security_policy_awareness')

            # Create User object
            new_user = User(
                employee_id=employee_id,
                name=name,
                department=department,
                role=role,
                experience_level=experience_level,
                remote_work_frequency=remote_work_frequency,
                security_training=security_training,
                mfa_enabled=mfa_enabled,
                password_hygiene=password_hygiene,
                social_media_exposure=social_media_exposure,
                sensitive_data_access=sensitive_data_access,
                security_policy_awareness=security_policy_awareness
            )

            # Save to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('User Profile Created Successfully')
            
            # Redirect to user details or simulation selection
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating profile: {str(e)}")
            return redirect(url_for('users.create_profile'))
            
    return render_template('users/profile.html')

@bp.route('/<int:user_id>', methods=['GET'])
def details(user_id):
    user = User.query.get_or_404(user_id)
    # Get latest assessment if any
    from app.database.models import RiskAssessment
    assessments = RiskAssessment.query.filter_by(user_id=user.id).order_by(RiskAssessment.created_at.desc()).all()
    latest_assessment = assessments[0] if assessments else None
    
    return render_template('users/details.html', user=user, assessment=latest_assessment)

