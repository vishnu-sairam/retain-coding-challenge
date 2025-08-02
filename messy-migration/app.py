"""Secure Flask User Management API - Refactored for security and maintainability"""

from flask import Flask
from config import Config
from routes.users import users_bp
from routes.auth import auth_bp
from utils.responses import success_response


def create_app():
    """Application factory pattern for better testing and configuration"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints with API prefix
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    # Home route
    @app.route('/')
    def home():
        return success_response(
            message="User Management System - Secure API",
            data={
                "version": "2.0",
                "endpoints": [
                    "GET /api/users - Get all users",
                    "GET /api/user/<id> - Get user by ID", 
                    "POST /api/users - Create new user",
                    "PUT /api/user/<id> - Update user",
                    "DELETE /api/user/<id> - Delete user",
                    "GET /api/search?name=<name> - Search users by name",
                    "POST /api/login - Authenticate user"
                ]
            }
        )
    
    return app


# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Use secure configuration from Config class
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )