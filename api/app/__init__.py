"""
Colombian Recipe API - Application Factory
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

# Store for revoked tokens
revoked_tokens = set()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'success': False, 'error': {'code': 'TOKEN_EXPIRED', 'message': 'Token has expired'}}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'success': False, 'error': {'code': 'INVALID_TOKEN', 'message': 'Invalid token'}}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'success': False, 'error': {'code': 'MISSING_TOKEN', 'message': 'Authorization token required'}}), 401
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return False
    
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.recipes import recipes_bp
    from app.routes.categories import categories_bp
    from app.routes.assistant import assistant_bp
    from app.routes.conversations import conversations_bp
    
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(recipes_bp, url_prefix='/api/v1/recipes')
    app.register_blueprint(categories_bp, url_prefix='/api/v1/categories')
    app.register_blueprint(assistant_bp, url_prefix='/api/v1/assistant')
    app.register_blueprint(conversations_bp, url_prefix='/api/v1/conversations')
    
    with app.app_context():
        db.create_all()
    
    return app
