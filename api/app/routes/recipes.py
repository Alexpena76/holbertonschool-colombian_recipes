"""
Recipe Routes
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.recipe_service import RecipeService
from app.services.response_service import success_response, error_response, paginate

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('', methods=['GET'])
@jwt_required()
def get_recipes():
    """Get all recipes with optional filtering and pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    region = request.args.get('region')
    
    if difficulty and difficulty not in ['easy', 'medium', 'hard']:
        return error_response('INVALID_DIFFICULTY', 'Difficulty must be easy, medium, or hard', 400)
    
    query = RecipeService.get_all(category=category, difficulty=difficulty, region=region)
    recipes, pagination = paginate(query, page=page, per_page=per_page)
    
    return success_response(
        data={'recipes': [recipe.to_dict() for recipe in recipes]},
        pagination=pagination
    )


@recipes_bp.route('/<string:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe(recipe_id):
    """Get recipe by ID with full details."""
    recipe = RecipeService.get_by_id(recipe_id)
    
    if not recipe:
        return error_response('RECIPE_NOT_FOUND', f'Recipe with id "{recipe_id}" not found', 404)
    
    return success_response(data=recipe.to_dict(include_details=True))


@recipes_bp.route('/search', methods=['GET'])
@jwt_required()
def search_recipes():
    """Search recipes by name or ingredient."""
    query_string = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if not query_string or len(query_string) < 2:
        return error_response('INVALID_QUERY', 'Search query must be at least 2 characters', 400)
    
    query = RecipeService.search(query_string)
    recipes, pagination = paginate(query, page=page, per_page=per_page)
    
    return success_response(
        data={'query': query_string, 'recipes': [recipe.to_dict() for recipe in recipes]},
        pagination=pagination
    )
