import os
from pathlib import Path

class Config:
    """Application configuration class"""
    
    # Database configuration
    DATABASE_PATH = os.path.join(Path(__file__).parent, 'users.db')
    
    # Security configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Application configuration
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5009))
    
    # Password configuration
    PASSWORD_MIN_LENGTH = 8
    
    # Rate limiting (for future implementation)
    RATELIMIT_STORAGE_URL = "memory://"
