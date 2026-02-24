"""
Step Model
"""
from app import db


class Step(db.Model):
    """Step model for cooking instructions."""
    __tablename__ = 'steps'
    
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.String(50), db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    instruction_es = db.Column(db.Text)
    
    def to_dict(self):
        """Convert step to dictionary."""
        return {
            'id': self.id,
            'step_number': self.step_number,
            'instruction': self.instruction,
            'instruction_es': self.instruction_es
        }
    
    def __repr__(self):
        return f'<Step {self.recipe_id} #{self.step_number}>'
