"""
Main Application Entry Point

This is where your Flask app starts. It:
1. Creates the Flask application
2. Connects to the database
3. Registers all the routes (URL endpoints)
4. Runs the development server

To run the app:
    python app.py
    
Then open http://localhost:5000 in your browser.
"""
import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from models import db, User
from utils import get_currency_symbol
from middleware import add_security_headers
from extensions import csrf, limiter

# Create instances
login_manager = LoginManager()
mail = Mail()


def create_app(config_name=None):
    """
    Application Factory Pattern.
    
    This function creates and configures the Flask app.
    Using a function (instead of creating app directly) makes testing easier
    and allows creating multiple app instances if needed.
    
    Args:
        config_name: 'development', 'production', or 'testing'
    """
    # Determine which configuration to use
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Production: fail fast if required env vars are missing
    if config_name == 'production':
        if not app.config.get('SECRET_KEY') or app.config['SECRET_KEY'] == 'dev-secret-key-change-me':
            raise ValueError('SECRET_KEY must be set in production. Add it to Render environment variables.')
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            raise ValueError('DATABASE_URL must be set in production. Render provides this for linked databases.')
    
    # Add security headers
    add_security_headers(app)
    
    # Initialize database with the app
    db.init_app(app)
    
    # Initialize mail
    mail.init_app(app)
    
    # CSRF protection (disabled in testing)
    csrf.init_app(app)
    
    # Rate limiting (disabled in testing)
    limiter.init_app(app)
    
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect here if not logged in
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login uses this to reload user from session."""
        return db.session.get(User, int(user_id))
    
    # Register custom template filters
    @app.template_filter('currency_symbol')
    def currency_symbol_filter(currency_code):
        """Convert currency code to symbol for use in templates."""
        return get_currency_symbol(currency_code)
    
    # Register blueprints (route modules)
    # Blueprints help organize routes into separate files
    from routes.main import main_bp
    from routes.transactions import transactions_bp
    from routes.accounts import accounts_bp
    from routes.categories import categories_bp
    from routes.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Favicon route (prevents 404 for /favicon.ico)
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.svg',
            mimetype='image/svg+xml'
        )
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
        # Create sample data only in development
        if app.config['DEBUG']:
            from seed_data import create_sample_data
            create_sample_data()
    
    return app


# Create app instance at module level (required for Gunicorn)
app = create_app()


# This runs when you execute: python app.py
if __name__ == '__main__':
    # Run the development server
    # debug=True enables:
    #   - Auto-reload when you change code
    #   - Detailed error pages
    app.run(debug=True, port=5001)
