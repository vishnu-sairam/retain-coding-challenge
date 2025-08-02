"""Security utilities for password hashing and validation"""

from werkzeug.security import generate_password_hash, check_password_hash
import re
from config import Config
from utils.validators import validate_email as email_validate, validate_name as name_validate


def hash_password(password):
    """Hash a password using werkzeug's secure method"""
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)


def validate_password_strength(password):
    """Validate password meets minimum security requirements"""
    if len(password) < Config.PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {Config.PASSWORD_MIN_LENGTH} characters long"
    
    # Check for at least one letter and one number
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"


def validate_email(email):
    """Validate email format - wrapper for consistency"""
    return email_validate(email)


def validate_name(name):
    """Validate name format - wrapper for consistency"""
    return name_validate(name)
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name.strip()) > 100:
        return False, "Name must be less than 100 characters"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, "Name is valid"
