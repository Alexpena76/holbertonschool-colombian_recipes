"""
Authentication Routes
"""
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from app.services.user_service import UserService
from app.services.response_service import success_response, error_response

auth_bp = Blueprint('auth', __name__)

# Store for revoked tokens (in production, use Redis)
revoked_tokens = set()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_REQUEST', 'Request body is required', 400)
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    if not email:
        return error_response('INVALID_EMAIL', 'Email is required', 400)
    
    if not password or len(password) < 6:
        return error_response('INVALID_PASSWORD', 'Password must be at least 6 characters', 400)
    
    if '@' not in email or '.' not in email:
        return error_response('INVALID_EMAIL', 'Invalid email format', 400)
    
    user = UserService.create_user(email, password, name)
    
    if not user:
        return error_response('EMAIL_EXISTS', 'Email already registered', 409)
    
    return success_response(
        data={'user': user.to_dict()},
        message='Registration successful',
        status_code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get JWT token."""
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_REQUEST', 'Request body is required', 400)
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return error_response('INVALID_CREDENTIALS', 'Email and password are required', 400)
    
    user = UserService.authenticate(email, password)
    
    if not user:
        return error_response('INVALID_CREDENTIALS', 'Invalid email or password', 401)
    
    access_token = create_access_token(identity=str(user.id))
    
    return success_response(
        data={
            'access_token': access_token,
            'token_type': 'bearer',
            'expires_in': 86400,
            'user': user.to_dict()
        }
    )


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout and invalidate token."""
    jti = get_jwt()['jti']
    revoked_tokens.add(jti)
    
    return success_response(message='Logout successful')


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Get current user information."""
    user_id = get_jwt_identity()
    user = UserService.get_by_id(user_id)
    
    if not user:
        return error_response('USER_NOT_FOUND', 'User not found', 404)
    
    return success_response(data={'user': user.to_dict()})


# Token revocation check
from app import jwt

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in revoked_tokens
