import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-cyber-key-123'
    
    # SQLite database inside the app folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data', 'risk_assessment.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
