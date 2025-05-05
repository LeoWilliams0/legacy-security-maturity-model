import os 

class Config:
    
    # If not found simple insecure default string suitable ONLY for development.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-insecure-default-key-replace-me'

    
    # If not found uses an SQLite database file named 'legacy_assessment.db'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'legacy_assessment.db')
        )
