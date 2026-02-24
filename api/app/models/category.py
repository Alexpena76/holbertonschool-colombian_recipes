"""
Category Model
"""
from app import db


class Category(db.Model):
    """Category model for recipe classification."""
    __tablename__ = 'categories'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_es = db.Column(db.String(100))
    image_url = db.Column(db.String(500))
    
    # Relationships
    recipes = db.relationship('Recipe', backref='category_ref', lazy='dynamic')
    
    def to_dict(self, include_count=False):
        """Convert category to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'name_es': self.name_es,
            'image_url': self.image_url
        }
        if include_count:
            data['recipe_count'] = self.recipes.count()
        return data
    
    def __repr__(self):
        return f'<Category {self.id}>'
