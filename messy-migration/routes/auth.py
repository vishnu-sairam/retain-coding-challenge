"""Secure authentication routes with proper validation and password verification"""

from flask import Blueprint, request
from models.user import User
from utils.responses import success_response, error_response, unauthorized_response
from utils.validators import validate_required_fields
import json

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Secure login endpoint with proper password verification"""
    try:
        # Parse JSON data safely
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        if not data:
            return error_response("Invalid JSON data", 400)
        
        # Validate required fields
        required_fields = ['email', 'password']
        valid_fields, field_errors = validate_required_fields(data, required_fields)
        if not valid_fields:
            return error_response("Missing required fields", 422), {"errors": field_errors}
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Get user by email using secure query
        user = User.get_by_email(email)
        if not user:
            return unauthorized_response("Invalid email or password")
        
        # Verify password using secure hash comparison
        if not user.verify_password(password):
            return unauthorized_response("Invalid email or password")
        
        # Return success response with user data (excluding sensitive info)
        return success_response(
            data={
                "user_id": user.id,
                "name": user.name,
                "email": user.email
            },
            message="Login successful"
        )
    
    except json.JSONDecodeError:
        return error_response("Invalid JSON format", 400)
    except Exception as e:
        return error_response(f"Login failed: {str(e)}", 500)
