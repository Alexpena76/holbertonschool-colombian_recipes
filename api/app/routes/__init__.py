"""
Colombian Recipe API - Routes
"""
from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.recipes import recipes_bp
from app.routes.categories import categories_bp
from app.routes.assistant import assistant_bp
from app.routes.conversations import conversations_bp

__all__ = [
    'health_bp',
    'auth_bp',
    'recipes_bp',
    'categories_bp',
    'assistant_bp',
    'conversations_bp'
]
