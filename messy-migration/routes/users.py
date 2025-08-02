"""Secure user CRUD routes with proper validation and error handling"""

from flask import Blueprint, request
from models.user import User
from utils.responses import success_response, error_response, not_found_response
from utils.validators import validate_user_id, validate_required_fields
import json

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users - secure endpoint with proper response format"""
    try:
        users = User.get_all()
        user_data = [user.to_dict() for user in users]
        return success_response(data=user_data, message="Users retrieved successfully")
    
    except Exception as e:
        return error_response(f"Failed to retrieve users: {str(e)}", 500)


@users_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get single user by ID - secure with parameterized queries"""
    # Validate user ID format
    valid_id, id_message = validate_user_id(user_id)
    if not valid_id:
        return error_response(id_message, 400)
    
    try:
        user = User.get_by_id(int(user_id))
        if not user:
            return not_found_response("User")
        
        return success_response(data=user.to_dict(), message="User retrieved successfully")
    
    except Exception as e:
        return error_response(f"Failed to retrieve user: {str(e)}", 500)


@users_bp.route('/users', methods=['POST'])
def create_user():
    """Create new user - secure with validation and password hashing"""
    try:
        # Parse JSON data safely
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        if not data:
            return error_response("Invalid JSON data", 400)
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        valid_fields, field_errors = validate_required_fields(data, required_fields)
        if not valid_fields:
            return error_response("Missing required fields", 422), {"errors": field_errors}
        
        # Create user with validation and secure password hashing
        user, error_response_data = User.create(
            name=data['name'].strip(),
            email=data['email'].strip().lower(),
            password=data['password']
        )
        
        if error_response_data:
            return error_response_data
        
        return success_response(
            data=user.to_dict(), 
            message="User created successfully", 
            status_code=201
        )
    
    except json.JSONDecodeError:
        return error_response("Invalid JSON format", 400)
    except Exception as e:
        return error_response(f"Failed to create user: {str(e)}", 500)


@users_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user - secure with validation"""
    # Validate user ID format
    valid_id, id_message = validate_user_id(user_id)
    if not valid_id:
        return error_response(id_message, 400)
    
    try:
        # Parse JSON data safely
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        if not data:
            return error_response("Invalid JSON data", 400)
        
        # Get existing user
        user = User.get_by_id(int(user_id))
        if not user:
            return not_found_response("User")
        
        # Extract and clean update data
        name = data.get('name')
        email = data.get('email')
        
        if name:
            name = name.strip()
        if email:
            email = email.strip().lower()
        
        # Update user with validation
        success, error_response_data = user.update(name=name, email=email)
        
        if error_response_data:
            return error_response_data
        
        if not success:
            return error_response("No changes were made", 400)
        
        return success_response(data=user.to_dict(), message="User updated successfully")
    
    except json.JSONDecodeError:
        return error_response("Invalid JSON format", 400)
    except Exception as e:
        return error_response(f"Failed to update user: {str(e)}", 500)


@users_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user - secure with proper validation"""
    # Validate user ID format
    valid_id, id_message = validate_user_id(user_id)
    if not valid_id:
        return error_response(id_message, 400)
    
    try:
        # Get existing user
        user = User.get_by_id(int(user_id))
        if not user:
            return not_found_response("User")
        
        # Delete user
        success, error_response_data = user.delete()
        
        if error_response_data:
            return error_response_data
        
        if not success:
            return error_response("Failed to delete user", 500)
        
        return success_response(message=f"User {user_id} deleted successfully")
    
    except Exception as e:
        return error_response(f"Failed to delete user: {str(e)}", 500)


@users_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by name - secure with parameterized queries"""
    name_query = request.args.get('name')
    
    if not name_query or not name_query.strip():
        return error_response("Please provide a name to search", 400)
    
    try:
        users = User.search_by_name(name_query.strip())
        user_data = [user.to_dict() for user in users]
        
        return success_response(
            data=user_data, 
            message=f"Found {len(user_data)} users matching '{name_query}'"
        )
    
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)
