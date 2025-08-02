"""URL Shortener Service - Main Flask Application"""

from flask import Flask, jsonify, request, redirect
from app.models import url_store
from app.utils import generate_short_code, validate_url, is_valid_short_code
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API",
        "version": "1.0.0",
        "endpoints": {
            "shorten": "POST /api/shorten",
            "redirect": "GET /<short_code>",
            "stats": "GET /api/stats/<short_code>"
        }
    })


@app.route('/api/health')
def api_health():
    """API health check endpoint"""
    stats = url_store.get_stats()
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running",
        "statistics": stats
    })


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Shorten a URL endpoint - POST /api/shorten"""
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Invalid JSON data"
            }), 400
        
        # Extract URL from request
        url = data.get('url')
        if not url:
            return jsonify({
                "error": "Missing 'url' field in request body"
            }), 400
        
        # Validate URL
        is_valid, result = validate_url(url)
        if not is_valid:
            return jsonify({
                "error": f"Invalid URL: {result}"
            }), 400
        
        # Use the normalized URL from validation
        normalized_url = result
        
        # Check if URL was already shortened
        existing_code = url_store.url_already_shortened(normalized_url)
        if existing_code:
            mapping = url_store.get_mapping(existing_code)
            return jsonify({
                "short_code": existing_code,
                "short_url": f"{request.host_url}{existing_code}",
                "original_url": normalized_url,
                "created_at": mapping.created_at.isoformat(),
                "message": "URL was already shortened"
            }), 200
        
        # Generate unique short code
        max_attempts = 10
        for attempt in range(max_attempts):
            short_code = generate_short_code()
            if not url_store.exists(short_code):
                break
        else:
            # This is extremely unlikely with 6-character alphanumeric codes
            logger.error(f"Failed to generate unique short code after {max_attempts} attempts")
            return jsonify({
                "error": "Failed to generate unique short code. Please try again."
            }), 500
        
        # Store the mapping
        try:
            mapping = url_store.store_mapping(short_code, normalized_url)
            logger.info(f"Created short code '{short_code}' for URL '{normalized_url}'")
            
            return jsonify({
                "short_code": short_code,
                "short_url": f"{request.host_url}{short_code}",
                "original_url": normalized_url,
                "created_at": mapping.created_at.isoformat()
            }), 201
            
        except ValueError as e:
            logger.error(f"Error storing mapping: {str(e)}")
            return jsonify({
                "error": "Failed to store URL mapping"
            }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in shorten_url: {str(e)}")
        return jsonify({
            "error": "Internal server error"
        }), 500


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL - GET /<short_code>"""
    try:
        # Validate short code format
        if not is_valid_short_code(short_code):
            return jsonify({
                "error": "Invalid short code format. Must be 6 alphanumeric characters."
            }), 404
        
        # Get mapping from store
        mapping = url_store.get_mapping(short_code)
        if not mapping:
            return jsonify({
                "error": "Short code not found"
            }), 404
        
        # Increment click count
        url_store.increment_click_count(short_code)
        
        logger.info(f"Redirecting '{short_code}' to '{mapping.original_url}' (click #{mapping.click_count + 1})")
        
        # Redirect to original URL
        return redirect(mapping.original_url, code=302)
    
    except Exception as e:
        logger.error(f"Unexpected error in redirect_to_url: {str(e)}")
        return jsonify({
            "error": "Internal server error"
        }), 500


@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Get analytics for a short code - GET /api/stats/<short_code>"""
    try:
        # Validate short code format
        if not is_valid_short_code(short_code):
            return jsonify({
                "error": "Invalid short code format. Must be 6 alphanumeric characters."
            }), 404
        
        # Get mapping from store
        mapping = url_store.get_mapping(short_code)
        if not mapping:
            return jsonify({
                "error": "Short code not found"
            }), 404
        
        # Return analytics
        return jsonify({
            "short_code": short_code,
            "original_url": mapping.original_url,
            "click_count": mapping.click_count,
            "created_at": mapping.created_at.isoformat(),
            "short_url": f"{request.host_url}{short_code}"
        }), 200
    
    except Exception as e:
        logger.error(f"Unexpected error in get_stats: {str(e)}")
        return jsonify({
            "error": "Internal server error"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested resource was not found on this server."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "The method is not allowed for the requested URL."
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred. Please try again later."
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)