"""
Category Routes
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.services.recipe_service import RecipeService
from app.services.response_service import success_response

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories with recipe counts."""
    categories = RecipeService.get_all_categories()
    
    return success_response(
        data={
            'categories': [cat.to_dict(include_count=True) for cat in categories]
        }
    )
