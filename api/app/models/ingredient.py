"""
Ingredient Model
"""
from app import db


class Ingredient(db.Model):
    """Ingredient model for recipe components."""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.String(50), db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    name_es = db.Column(db.String(200))
    amount = db.Column(db.Numeric(10, 2))
    unit = db.Column(db.String(50))
    order_index = db.Column(db.Integer, default=0)
    
    def to_dict(self, scale=1.0):
        """Convert ingredient to dictionary with optional scaling."""
        return {
            'id': self.id,
            'name': self.name,
            'name_es': self.name_es,
            'amount': float(self.amount * scale) if self.amount else None,
            'unit': self.unit,
            'order_index': self.order_index
        }
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
