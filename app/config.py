import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///fundraiser.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Admin credentials
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Grid defaults
    DEFAULT_GRID_ROWS = int(os.environ.get('DEFAULT_GRID_ROWS', 10))
    DEFAULT_GRID_COLUMNS = int(os.environ.get('DEFAULT_GRID_COLUMNS', 10))
    
    # Image processing
    THUMBNAIL_SIZE = (300, 300)
    IMAGE_SIZE = (800, 800) 