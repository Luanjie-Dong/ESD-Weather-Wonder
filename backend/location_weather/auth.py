import os
import time
from functools import wraps
from flask import request, jsonify
from jwt_utils import generate_service_token, verify_service_token

SERVICE_NAME = "location_weather"

# Token cache
_token = None
_token_expiry = 0

def get_service_token():
    """Generate a JWT token for this service using shared secret"""
    global _token, _token_expiry
    
    # Return cached token if it's still valid
    if _token and time.time() < _token_expiry - 60:  # 1 minute buffer
        return _token
    
    # Generate new token locally
    _token = generate_service_token(SERVICE_NAME)
    _token_expiry = time.time() + 3600  # 1 hour
    
    return _token

def add_auth_headers(headers=None):
    """Add authorization headers to a request"""
    if headers is None:
        headers = {}
    
    token = get_service_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    return headers

def requires_auth(f):
    """Decorator to verify JWT tokens from other services"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Authorization header is missing or invalid"}), 401
        
        token = auth_header.split(' ')[1]
        
        # Verify token locally using shared secret
        payload = verify_service_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Add the verified service to request context
        request.service = payload.get('service')
        
        return f(*args, **kwargs)
    
    return decorated