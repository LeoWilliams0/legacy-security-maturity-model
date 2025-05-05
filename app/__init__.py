import os  # Operating system utilities for filesystem path operations

from flask import Flask, render_template  # Core Flask framework and template rendering engine
from flask_sqlalchemy import SQLAlchemy    # Object-Relational Mapper (ORM) for database interactions
from flask_migrate import Migrate          # Database migration handling using Alembic

# Extension Initialisation 
db = SQLAlchemy()
migrate = Migrate()

#  Application Factory

def create_app() -> Flask:
    # Create the Flask application instance.
    app = Flask(__name__, instance_relative_config=True)
    app.jinja_env.add_extension('jinja2.ext.do')

    app.config.from_object('app.config.Config')

    # Ensure the instance folder (used for config, database files, etc.) exists.
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        app.logger.error(f"Failed to create instance path at {app.instance_path}: {e}")
        
    # Initialise Flask extensions by binding them to the created app instance.
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register the blueprint containing the main application routes.
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Custom Error Handlers 

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404 Not Found: {error}") # Log the error
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Internal Server Error: {error}", exc_info=True) # Log with traceback
        try:
            db.session.rollback()
            app.logger.info("Database session rolled back successfully after 500 error.")
        except Exception as db_error:
            app.logger.error(f"Error rolling back database session: {db_error}")
        return render_template('500.html'), 500

    # Return the fully configured application instance
    return app