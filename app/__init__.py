import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login manager
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes.admin import admin_bp
    from app.routes.public import public_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create upload directory if it doesn't exist
    upload_path = os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    
    # Register template filters
    @app.template_filter('image_url')
    def image_url_filter(path):
        """Convert image path to proper static URL."""
        if not path:
            return ''
        # Remove 'static/' prefix if present
        clean_path = path.replace('static/', '') if path.startswith('static/') else path
        return url_for('static', filename=clean_path)
    
    @app.template_filter('ensure_url_protocol')
    def ensure_url_protocol_filter(url):
        """Ensure URL has a protocol (http/https)."""
        if not url:
            return '#'
        if url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            return url
        # Default to https for any other URL
        return f'https://{url}'
    
    # Note: Tables will be created via migrations, not automatically
    
    return app 