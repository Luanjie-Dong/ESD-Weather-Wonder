import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify

# Load JWT secret from environment variable
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRATION = 3600  # 1 hour

def generate_service_token(service_name):
    """Generate a JWT token for service-to-service communication"""
    payload = {
        "service": service_name,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_EXPIRATION),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_service_token(token):
    """Verify a service JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to protect routes with JWT verification"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        # Verify token
        payload = verify_service_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Add service info to request
        request.service = payload.get('service')
        
        return f(*args, **kwargs)
    
    return decorated