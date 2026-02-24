"""
Colombian Recipe API - Application Factory
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def register_error_handlers(app):
    """Register error handlers for the application."""
    from app.services.response_service import error_response
    
    @app.errorhandler(400)
    def bad_request(error):
        return error_response('BAD_REQUEST', 'Bad request', 400)
    
    @app.errorhandler(401)
    def unauthorized(error):
        return error_response('UNAUTHORIZED', 'Authentication required', 401)
    
    @app.errorhandler(404)
    def not_found(error):
        return error_response('NOT_FOUND', 'Resource not found', 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        return error_response('INTERNAL_ERROR', 'Internal server error', 500)