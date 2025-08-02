"""Secure user route handlers"""

from flask import Blueprint, request
from models.user import User
from utils.responses import success_response, error_response, not_found_response, validation_error_response
import json

user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return success_response(message="User Management System - Secure Version")


@user_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users (secure version with JSON response)"""
    try:
        users = User.get_all()
        user_data = [user.to_dict() for user in users]
        return success_response(data=user_data, message="Users retrieved successfully")
    
    except Exception as e:
        return error_response("Failed to retrieve users", 500)


@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get single user by ID (secure version with parameterized query)"""
    try:
        user = User.get_by_id(user_id)
        
        if user:
            return success_response(data=user.to_dict(), message="User retrieved successfully")
        else:
            return not_found_response("User")
    
    except Exception as e:
        return error_response("Failed to retrieve user", 500)


@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create new user (secure version with validation and password hashing)"""
    try:
        # Parse JSON data safely
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return validation_error_response([f"Missing required field: {field}" for field in missing_fields])
        
        # Create user with validation
        user, error_response_obj = User.create(
            name=data['name'].strip(),
            email=data['email'].strip().lower(),
            password=data['password']
        )
        
        if error_response_obj:
            return error_response_obj
        
        return success_response(
            data=user.to_dict(),
            message="User created successfully",
            status_code=201
        )
    
    except json.JSONDecodeError:
        return error_response("Invalid JSON data", 400)
    except Exception as e:
        return error_response("Failed to create user", 500)


@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user (secure version with validation)"""
    try:
        # Check if user exists
        user = User.get_by_id(user_id)
        if not user:
            return not_found_response("User")
        
        # Parse JSON data safely
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        
        # Extract and clean data
        name = data.get('name')
        email = data.get('email')
        
        if name:
            name = name.strip()
        if email:
            email = email.strip().lower()
        
        # Update user with validation
        success, error_response_obj = user.update(name=name, email=email)
        
        if error_response_obj:
            return error_response_obj
        
        if success:
            return success_response(data=user.to_dict(), message="User updated successfully")
        else:
            return error_response("No changes made", 400)
    
    except json.JSONDecodeError:
        return error_response("Invalid JSON data", 400)
    except Exception as e:
        return error_response("Failed to update user", 500)


@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user (secure version with parameterized query)"""
    try:
        # Check if user exists
        user = User.get_by_id(user_id)
        if not user:
            return not_found_response("User")
        
        # Delete user
        success, error_response_obj = user.delete()
        
        if error_response_obj:
            return error_response_obj
        
        if success:
            return success_response(message=f"User {user_id} deleted successfully")
        else:
            return error_response("Failed to delete user", 500)
    
    except Exception as e:
        return error_response("Failed to delete user", 500)


@user_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by name (secure version with parameterized query)"""
    try:
        name_query = request.args.get('name')
        
        if not name_query or not name_query.strip():
            return error_response("Please provide a name to search", 400)
        
        # Search users with secure query
        users = User.search_by_name(name_query.strip())
        user_data = [user.to_dict() for user in users]
        
        return success_response(
            data=user_data,
            message=f"Found {len(users)} users matching '{name_query}'"
        )
    
    except Exception as e:
        return error_response("Failed to search users", 500)


@user_bp.route('/login', methods=['POST'])
def login():
    """User login (secure version with password hashing)"""
    try:
        # Parse JSON data safely
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return validation_error_response(["Email and password are required"])
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Find user by email
        user = User.get_by_email(email)
        
        if user and user.verify_password(password):
            return success_response(
                data={"user_id": user.id, "name": user.name, "email": user.email},
                message="Login successful"
            )
        else:
            return error_response("Invalid email or password", 401)
    
    except json.JSONDecodeError:
        return error_response("Invalid JSON data", 400)
    except Exception as e:
        return error_response("Login failed", 500)
