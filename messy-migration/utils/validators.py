"""Input validation utilities"""

import re
from email_validator import validate_email as email_validate, EmailNotValidError


def validate_email(email):
    """Validate email format and deliverability"""
    if not email or not isinstance(email, str):
        return False, "Email is required"
    
    try:
        # Use email-validator library for comprehensive validation
        validated_email = email_validate(email)
        return True, "Email is valid"
    except EmailNotValidError as e:
        return False, f"Invalid email: {str(e)}"


def validate_name(name):
    """Validate user name"""
    if not name or not isinstance(name, str):
        return False, "Name is required"
    
    name = name.strip()
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name must be less than 100 characters"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, "Name is valid"


def validate_required_fields(data, required_fields):
    """Validate that all required fields are present and not empty"""
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"{field} is required")
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            errors.append(f"{field} cannot be empty")
    
    return len(errors) == 0, errors


def validate_user_id(user_id):
    """Validate user ID format"""
    if not user_id:
        return False, "User ID is required"
    
    try:
        user_id_int = int(user_id)
        if user_id_int <= 0:
            return False, "User ID must be a positive integer"
        return True, "User ID is valid"
    except (ValueError, TypeError):
        return False, "User ID must be a valid integer"
