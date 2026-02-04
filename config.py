"""
Configuration settings for the app.
This file stores settings that might change between development and production.
"""
import os

# Get the directory where this file is located
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration - shared by all environments."""
    
    # Secret key for session security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    
    # Disable modification tracking (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database encryption key
    DB_ENCRYPTION_KEY = os.environ.get('DB_ENCRYPTION_KEY')


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False
    
    # Use SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'finance.db')


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False
    
    # Use PostgreSQL in production
    # Render/Heroku provide DATABASE_URL automatically
    database_url = os.environ.get('DATABASE_URL')
    
    # Fix for Heroku's postgres:// vs postgresql:// issue
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url or 'postgresql://user:password@localhost/financedb'
    
    # Note: Make sure to set SECRET_KEY environment variable in production!


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True
    
    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
