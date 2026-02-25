"""
Recipe Service - Recipe data operations
"""
from sqlalchemy import or_
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.ingredient import Ingredient


class RecipeService:
    """Service class for recipe operations."""
    
    @staticmethod
    def get_all(category=None, difficulty=None, region=None):
        """
        Get all recipes with optional filtering.
        
        Args:
            category: Filter by category ID
            difficulty: Filter by difficulty level
            region: Filter by region
        
        Returns:
            SQLAlchemy query object
        """
        query = Recipe.query
        
        if category:
            query = query.filter(Recipe.category == category)
        
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)
        
        if region:
            query = query.filter(Recipe.region.ilike(f'%{region}%'))
        
        return query.order_by(Recipe.name)
    
    @staticmethod
    def get_by_id(recipe_id):
        """Get recipe by ID with full details."""
        return Recipe.query.get(recipe_id)
    
    @staticmethod
    def search(query_string):
        """
        Search recipes by name or ingredient.
        
        Args:
            query_string: Search query
        
        Returns:
            SQLAlchemy query object
        """
        search_term = f'%{query_string}%'
        
        # Search in recipe names and descriptions
        recipe_ids = Recipe.query.filter(
            or_(
                Recipe.name.ilike(search_term),
                Recipe.name_es.ilike(search_term),
                Recipe.description.ilike(search_term)
            )
        ).with_entities(Recipe.id).all()
        
        # Search in ingredients
        ingredient_recipe_ids = Ingredient.query.filter(
            or_(
                Ingredient.name.ilike(search_term),
                Ingredient.name_es.ilike(search_term)
            )
        ).with_entities(Ingredient.recipe_id).distinct().all()
        
        # Combine results
        all_ids = set([r[0] for r in recipe_ids] + [r[0] for r in ingredient_recipe_ids])
        
        if not all_ids:
            return Recipe.query.filter(Recipe.id == None)  # Return empty query
        
        return Recipe.query.filter(Recipe.id.in_(all_ids)).order_by(Recipe.name)
    
    @staticmethod
    def get_all_categories():
        """Get all categories with recipe counts."""
        return Category.query.order_by(Category.name).all()
    
    @staticmethod
    def get_category_by_id(category_id):
        """Get category by ID."""
        return Category.query.get(category_id)
