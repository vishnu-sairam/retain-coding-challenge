"""Standardized API response utilities"""

from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    """Create a standardized success response"""
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400, error_code=None):
    """Create a standardized error response"""
    response = {
        "status": "error",
        "message": message
    }
    if error_code:
        response["error_code"] = error_code
    
    return jsonify(response), status_code


def validation_error_response(errors):
    """Create a response for validation errors"""
    return error_response(
        message="Validation failed",
        status_code=422,
        error_code="VALIDATION_ERROR"
    )[0].get_json() | {"errors": errors}, 422


def not_found_response(resource="Resource"):
    """Create a standardized not found response"""
    return error_response(
        message=f"{resource} not found",
        status_code=404,
        error_code="NOT_FOUND"
    )


def unauthorized_response(message="Unauthorized"):
    """Create a standardized unauthorized response"""
    return error_response(
        message=message,
        status_code=401,
        error_code="UNAUTHORIZED"
    )


def server_error_response(message="Internal server error"):
    """Create a standardized server error response"""
    return error_response(
        message=message,
        status_code=500,
        error_code="INTERNAL_ERROR"
    )
