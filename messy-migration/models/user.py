"""User model with secure database operations"""

from models.database import db_manager
from utils.security import hash_password, verify_password, validate_email, validate_name, validate_password_strength
from utils.responses import error_response, validation_error_response
import sqlite3


class User:
    """User model with secure database operations using parameterized queries"""
    
    def __init__(self, id=None, name=None, email=None, password_hash=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
    
    @classmethod
    def create(cls, name, email, password):
        """Create a new user with validation and secure password hashing"""
        # Validate input
        errors = []
        
        # Validate name
        name_valid, name_msg = validate_name(name)
        if not name_valid:
            errors.append(name_msg)
        
        # Validate email
        email_valid, email_msg = validate_email(email)
        if not email_valid:
            errors.append(email_msg)
        
        # Validate password strength
        password_valid, password_msg = validate_password_strength(password)
        if not password_valid:
            errors.append(password_msg)
        
        if errors:
            return None, validation_error_response(errors)
        
        # Check if email already exists
        if cls.get_by_email(email):
            return None, error_response("Email already exists", 409)
        
        # Hash password securely
        password_hash = hash_password(password)
        
        try:
            with db_manager.get_cursor() as cursor:
                # Use parameterized query to prevent SQL injection
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, password_hash)
                )
                user_id = cursor.lastrowid
                
                return cls(id=user_id, name=name, email=email, password_hash=password_hash), None
        
        except sqlite3.Error as e:
            return None, error_response(f"Database error: {str(e)}", 500)
    
    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID using parameterized query"""
        try:
            with db_manager.get_cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return cls(id=row['id'], name=row['name'], email=row['email'], password_hash=row['password'])
                return None
        
        except sqlite3.Error:
            return None
    
    @classmethod
    def get_by_email(cls, email):
        """Get user by email using parameterized query"""
        try:
            with db_manager.get_cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                row = cursor.fetchone()
                
                if row:
                    return cls(id=row['id'], name=row['name'], email=row['email'], password_hash=row['password'])
                return None
        
        except sqlite3.Error:
            return None
    
    @classmethod
    def get_all(cls):
        """Get all users using secure query"""
        try:
            with db_manager.get_cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users")  # Don't return password hashes
                rows = cursor.fetchall()
                
                return [cls(id=row['id'], name=row['name'], email=row['email']) for row in rows]
        
        except sqlite3.Error:
            return []
    
    @classmethod
    def search_by_name(cls, name_query):
        """Search users by name using parameterized query"""
        try:
            with db_manager.get_cursor() as cursor:
                # Use parameterized query to prevent SQL injection
                cursor.execute(
                    "SELECT id, name, email FROM users WHERE name LIKE ?", 
                    (f"%{name_query}%",)
                )
                rows = cursor.fetchall()
                
                return [cls(id=row['id'], name=row['name'], email=row['email']) for row in rows]
        
        except sqlite3.Error:
            return []
    
    def update(self, name=None, email=None):
        """Update user information with validation"""
        if not self.id:
            return False, error_response("User ID required for update", 400)
        
        errors = []
        
        # Validate name if provided
        if name is not None:
            name_valid, name_msg = validate_name(name)
            if not name_valid:
                errors.append(name_msg)
        
        # Validate email if provided
        if email is not None:
            email_valid, email_msg = validate_email(email)
            if not email_valid:
                errors.append(email_msg)
            
            # Check if email already exists (excluding current user)
            existing_user = self.get_by_email(email)
            if existing_user and existing_user.id != self.id:
                errors.append("Email already exists")
        
        if errors:
            return False, validation_error_response(errors)
        
        try:
            with db_manager.get_cursor() as cursor:
                # Build dynamic query based on provided fields
                updates = []
                params = []
                
                if name is not None:
                    updates.append("name = ?")
                    params.append(name)
                    self.name = name
                
                if email is not None:
                    updates.append("email = ?")
                    params.append(email)
                    self.email = email
                
                if updates:
                    params.append(self.id)
                    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
                    cursor.execute(query, params)
                    
                    return cursor.rowcount > 0, None
                
                return True, None  # No updates needed
        
        except sqlite3.Error as e:
            return False, error_response(f"Database error: {str(e)}", 500)
    
    def delete(self):
        """Delete user using parameterized query"""
        if not self.id:
            return False, error_response("User ID required for deletion", 400)
        
        try:
            with db_manager.get_cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
                return cursor.rowcount > 0, None
        
        except sqlite3.Error as e:
            return False, error_response(f"Database error: {str(e)}", 500)
    
    def verify_password(self, password):
        """Verify password against stored hash"""
        if not self.password_hash:
            return False
        return verify_password(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary (excluding password hash by default)"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
        
        if include_sensitive and self.password_hash:
            data['password_hash'] = self.password_hash
        
        return data
