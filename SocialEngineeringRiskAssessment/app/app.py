import sys
import os

# Add parent directory to path so we can run from the root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from app.config import Config
from app.database.database import db

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    db.init_app(flask_app)

    with flask_app.app_context():
        # Create database tables
        import app.database.models
        db.create_all()

    # Import and register blueprints
    from app.routes.main import bp as main_bp
    flask_app.register_blueprint(main_bp)
    
    from app.routes.users import bp as users_bp
    flask_app.register_blueprint(users_bp, url_prefix='/users')
    
    from app.routes.simulation import bp as sim_bp
    flask_app.register_blueprint(sim_bp, url_prefix='/simulations')
    
    from app.routes.risk import bp as risk_bp
    flask_app.register_blueprint(risk_bp, url_prefix='/risk')

    @flask_app.route('/health')
    def health():
        return {"status": "ok"}

    return flask_app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True, port=5000)
