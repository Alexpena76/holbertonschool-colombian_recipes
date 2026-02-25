"""
User Service - User authentication and management
"""
from app import db
from app.models.user import User


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(email, password, name=None):
        """Create a new user."""
        if User.query.filter_by(email=email.lower()).first():
            return None
        
        user = User(email=email.lower(), password=password, name=name)
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate a user."""
        user = User.query.filter_by(email=email.lower()).first()
        
        if user and user.check_password(password):
            return user
        
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        """Get user by email."""
        return User.query.filter_by(email=email.lower()).first()
