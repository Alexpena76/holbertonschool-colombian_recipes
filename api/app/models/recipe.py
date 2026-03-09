"""
Recipe Model
"""
from datetime import datetime
from app import db


class Recipe(db.Model):
    """Recipe model for Colombian dishes."""
    __tablename__ = 'recipes'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_es = db.Column(db.String(200))
    category = db.Column(db.String(50), db.ForeignKey('categories.id'), index=True)
    region = db.Column(db.String(100))
    difficulty = db.Column(db.Enum('easy', 'medium', 'hard'), default='medium', index=True)
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    servings = db.Column(db.Integer, default=4)
    description = db.Column(db.Text)
    description_es = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ingredients = db.relationship('Ingredient', backref='recipe', lazy='dynamic', cascade='all, delete-orphan', order_by='Ingredient.order_index')
    steps = db.relationship('Step', backref='recipe', lazy='dynamic', cascade='all, delete-orphan', order_by='Step.step_number')
    
    def to_dict(self, include_details=False):
        """Convert recipe to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'name_es': self.name_es,
            'category': self.category,
            'region': self.region,
            'difficulty': self.difficulty,
            'prep_time_minutes': self.prep_time_minutes,
            'cook_time_minutes': self.cook_time_minutes,
            'servings': self.servings,
            'image_url': self.image_url
        }
        
        if include_details:
            data['description'] = self.description
            data['description_es'] = self.description_es
            data['ingredients'] = [ing.to_dict() for ing in self.ingredients]
            data['steps'] = [step.to_dict() for step in self.steps]
            data['created_at'] = self.created_at.isoformat() if self.created_at else None
        
        return data
    
    def to_context_string(self):
        """Convert recipe to context string for AI assistant"""
        context = f"Recipe: {self.name}\n"
        
        if self.description:
            context += f"Description: {self.description}\n"
        
        if hasattr(self, 'prep_time') and self.prep_time:
            context += f"Prep time: {self.prep_time} minutes\n"
        
        if hasattr(self, 'cook_time') and self.cook_time:
            context += f"Cook time: {self.cook_time} minutes\n"
        
        if hasattr(self, 'servings') and self.servings:
            context += f"Servings: {self.servings}\n"
        
        # Add ingredients
        if self.ingredients:
            context += "\nIngredients:\n"
            for ing in self.ingredients:
                context += f"- {ing.amount} {ing.unit} {ing.name}\n"
        
        # Add steps
        if self.steps:
            context += "\nSteps:\n"
            for step in self.steps:
                context += f"{step.step_number}. {step.instruction}\n"
        
        return context
    
    def __repr__(self):
        return f'<Recipe {self.id}>'
