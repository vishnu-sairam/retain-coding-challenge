"""Secure Flask User Management API - Refactored Version"""

from flask import Flask
from routes.user_routes import user_bp
from config import Config
from models.database import db_manager
import atexit

def create_app():
    """Application factory pattern for better structure"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(user_bp)
    
    # Register cleanup function
    atexit.register(cleanup_db_connections)
    
    return app

def cleanup_db_connections():
    """Clean up database connections on app shutdown"""
    try:
        db_manager.close_connection()
    except:
        pass

if __name__ == '__main__':
    app = create_app()
    
    # Run with secure settings
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG  # This will be False in production
    )
