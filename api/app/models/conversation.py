"""
Conversation Model
"""
from datetime import datetime
from app import db


class Conversation(db.Model):
    """AI conversation model - stores chat sessions"""
    
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), 
                        nullable=False, index=True)
    recipe_id = db.Column(db.String(50), db.ForeignKey('recipes.id', ondelete='SET NULL'),
                          index=True, nullable=True)
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='conversation', lazy='dynamic',
                               cascade='all, delete-orphan', order_by='Message.created_at')
    recipe = db.relationship('Recipe', backref='conversations')
    user = db.relationship('User', backref='conversations')
    
    def __init__(self, user_id, recipe_id=None, title=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.title = title
    
    def to_dict(self, include_messages=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id,
            'recipe_name': self.recipe.name if self.recipe else None,
            'title': self.title,
            'message_count': self.messages.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_messages:
            data['messages'] = [msg.to_dict() for msg in self.messages.all()]
        
        return data
    
    def __repr__(self):
        return f'<Conversation {self.id}>'
