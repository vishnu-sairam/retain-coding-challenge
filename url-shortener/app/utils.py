"""Utility functions for URL shortener service"""

import re
import string
import random
from urllib.parse import urlparse
from typing import Tuple


def generate_short_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code of specified length.
    
    Args:
        length: Length of the short code (default: 6)
        
    Returns:
        Random alphanumeric string of specified length
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def validate_url(url: str) -> Tuple[bool, str]:
    """Validate if the provided URL is valid and accessible.
    
    Args:
        url: URL string to validate
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not url or not isinstance(url, str):
        return False, "URL is required and must be a string"
    
    # Remove leading/trailing whitespace
    url = url.strip()
    
    if not url:
        return False, "URL cannot be empty"
    
    # Check minimum length
    if len(url) < 4:
        return False, "URL is too short"
    
    # Check maximum length (reasonable limit)
    if len(url) > 2048:
        return False, "URL is too long (max 2048 characters)"
    
    # Add http:// if no scheme is provided
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        parsed = urlparse(url)
        
        # Check if scheme is valid
        if parsed.scheme not in ['http', 'https']:
            return False, "URL must use http or https protocol"
        
        # Check if netloc (domain) exists
        if not parsed.netloc:
            return False, "URL must contain a valid domain"
        
        # Check for valid domain format (basic validation)
        domain_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'
            r'(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        )
        
        # Extract domain from netloc (remove port if present)
        domain = parsed.netloc.split(':')[0]
        
        if not domain_pattern.match(domain):
            return False, "URL contains invalid domain format"
        
        # Check for localhost/private IPs in production (optional security measure)
        if domain.lower() in ['localhost', '127.0.0.1', '0.0.0.0']:
            return False, "Cannot shorten localhost URLs"
        
        return True, url  # Return the normalized URL
        
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"


def is_valid_short_code(code: str) -> bool:
    """Check if a short code has valid format.
    
    Args:
        code: Short code to validate
        
    Returns:
        True if code is valid format, False otherwise
    """
    if not code or not isinstance(code, str):
        return False
    
    # Must be exactly 6 characters
    if len(code) != 6:
        return False
    
    # Must be alphanumeric only
    return code.isalnum()