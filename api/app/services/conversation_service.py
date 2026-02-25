"""
Conversation Service - Chat history management
"""
from app import db
from app.models.conversation import Conversation
from app.models.message import Message


class ConversationService:
    """Service class for conversation operations."""
    
    @staticmethod
    def create_conversation(user_id, recipe_id, title=None):
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            recipe_id=recipe_id,
            title=title
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return conversation
    
    @staticmethod
    def get_or_create(user_id, recipe_id, conversation_id=None):
        """
        Get existing conversation or create new one.
        
        Args:
            user_id: User's ID
            recipe_id: Recipe ID for context
            conversation_id: Optional existing conversation ID
        
        Returns:
            Conversation object
        """
        if conversation_id:
            conversation = Conversation.query.filter_by(
                id=conversation_id,
                user_id=user_id
            ).first()
            
            if conversation:
                return conversation
        
        # Create new conversation
        return ConversationService.create_conversation(user_id, recipe_id)
    
    @staticmethod
    def add_message(conversation_id, role, content):
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: Conversation ID
            role: Message role ('user' or 'assistant')
            content: Message content
        
        Returns:
            Message object
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        
        db.session.add(message)
        
        # Update conversation timestamp
        conversation = Conversation.query.get(conversation_id)
        if conversation:
            db.session.commit()
        
        return message
    
    @staticmethod
    def get_user_conversations(user_id):
        """Get all conversations for a user."""
        return Conversation.query.filter_by(user_id=user_id).order_by(
            Conversation.updated_at.desc()
        )
    
    @staticmethod
    def get_by_id(conversation_id, user_id):
        """Get conversation by ID (with user verification)."""
        return Conversation.query.filter_by(
            id=conversation_id,
            user_id=user_id
        ).first()
    
    @staticmethod
    def delete(conversation_id, user_id):
        """Delete a conversation."""
        conversation = ConversationService.get_by_id(conversation_id, user_id)
        
        if conversation:
            db.session.delete(conversation)
            db.session.commit()
            return True
        
        return False
