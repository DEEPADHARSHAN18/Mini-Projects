from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database.database import db
from app.database.models import User, Simulation, SimulationResponse

bp = Blueprint('simulation', __name__)

@bp.route('/', methods=['GET'])
def select():
    users = User.query.all()
    return render_template('simulation/select.html', users=users)

@bp.route('/start', methods=['POST'])
def start_simulation():
    user_id = request.form.get('user_id')
    scenario_type = request.form.get('scenario_type')

    if not user_id or not scenario_type:
        flash("Please select a user and a scenario.")
        return redirect(url_for('simulation.select'))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for('simulation.select'))

    # Create simulation record
    simulation = Simulation(
        user_id=user.id,
        scenario_type=scenario_type,
        scenario_name=f"{scenario_type} Simulation for {user.name}"
    )
    db.session.add(simulation)
    db.session.commit()

    # Redirect based on scenario_type
    if scenario_type == 'Phishing':
        return redirect(url_for('simulation.phishing', user_id=user.id))
    elif scenario_type == 'Fake IT Support':
        return redirect(url_for('simulation.fake_it_support', user_id=user.id))
    elif scenario_type == 'Password Reset':
        return redirect(url_for('simulation.password_reset', user_id=user.id))
    elif scenario_type == 'Suspicious Attachment':
        return redirect(url_for('simulation.suspicious_attachment', user_id=user.id))
    else:
        flash(f"{scenario_type} is under development.")
        return redirect(url_for('simulation.select'))

# Phishing scenario
@bp.route('/phishing/<int:user_id>', methods=['GET'])
def phishing(user_id):
    simulation = Simulation.query.filter_by(user_id=user_id).order_by(Simulation.started_at.desc()).first_or_404()
    sim_id = simulation.id
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()
    if not response:
        response = SimulationResponse(simulation_id=sim_id, opened=True)
        db.session.add(response)
        db.session.commit()
    return render_template('simulation/phishing.html', simulation=simulation)

# Fake IT Support scenario
@bp.route('/fake_it_support/<int:user_id>', methods=['GET'])
def fake_it_support(user_id):
    simulation = Simulation.query.filter_by(user_id=user_id).order_by(Simulation.started_at.desc()).first_or_404()
    sim_id = simulation.id
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()
    if not response:
        response = SimulationResponse(simulation_id=sim_id, opened=True)
        db.session.add(response)
        db.session.commit()
    return render_template('simulation/fake_it_support.html', simulation=simulation)

# Password Reset scenario
@bp.route('/password_reset/<int:user_id>', methods=['GET'])
def password_reset(user_id):
    simulation = Simulation.query.filter_by(user_id=user_id).order_by(Simulation.started_at.desc()).first_or_404()
    sim_id = simulation.id
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()
    if not response:
        response = SimulationResponse(simulation_id=sim_id, opened=True)
        db.session.add(response)
        db.session.commit()
    return render_template('simulation/password_reset.html', simulation=simulation)

# Suspicious Attachment scenario
@bp.route('/suspicious_attachment/<int:user_id>', methods=['GET'])
def suspicious_attachment(user_id):
    simulation = Simulation.query.filter_by(user_id=user_id).order_by(Simulation.started_at.desc()).first_or_404()
    sim_id = simulation.id
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()
    if not response:
        response = SimulationResponse(simulation_id=sim_id, opened=True)
        db.session.add(response)
        db.session.commit()
    return render_template('simulation/suspicious_attachment.html', simulation=simulation)

@bp.route('/action/<int:sim_id>', methods=['POST'])
def handle_action(sim_id):
    action = request.form.get('action')
    simulation = Simulation.query.get_or_404(sim_id)
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()

    if action == 'click':
        response.clicked = True
        response.final_decision = 'Clicked Action'
    elif action == 'report':
        response.reported = True
        response.final_decision = 'Reported'
    elif action == 'analyze':
        response.analyzed = True
        db.session.commit()
        return "analysis_mode"
    elif action == 'submit_analysis':
        indicators = request.form.getlist('indicators')
        response.indicators_identified = len(indicators)
        response.final_decision = 'Analyzed and Reported'
    db.session.commit()
    return redirect(url_for('simulation.result', sim_id=sim_id))

@bp.route('/result/<int:sim_id>', methods=['GET'])
def result(sim_id):
    simulation = Simulation.query.get_or_404(sim_id)
    response = SimulationResponse.query.filter_by(simulation_id=sim_id).first()
    from app.services.simulation_engine import calculate_awareness_score
    awareness_score = calculate_awareness_score(response)
    return render_template('simulation/result.html', simulation=simulation, response=response, score=awareness_score)
