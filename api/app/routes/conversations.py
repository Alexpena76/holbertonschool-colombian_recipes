"""
Conversation Routes
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.conversation_service import ConversationService
from app.services.response_service import success_response, error_response, paginate

conversations_bp = Blueprint('conversations', __name__)


@conversations_bp.route('', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for the current user."""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = ConversationService.get_user_conversations(user_id)
    conversations, pagination = paginate(query, page=page, per_page=per_page)
    
    return success_response(
        data={
            'conversations': [conv.to_dict() for conv in conversations]
        },
        pagination=pagination
    )


@conversations_bp.route('/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    """Get a specific conversation with messages."""
    user_id = get_jwt_identity()
    
    conversation = ConversationService.get_by_id(conversation_id, user_id)
    
    if not conversation:
        return error_response('CONVERSATION_NOT_FOUND', 'Conversation not found', 404)
    
    return success_response(
        data={
            'conversation': conversation.to_dict(),
            'messages': [msg.to_dict() for msg in conversation.messages]
        }
    )


@conversations_bp.route('/<int:conversation_id>', methods=['DELETE'])
@jwt_required()
def delete_conversation(conversation_id):
    """Delete a conversation."""
    user_id = get_jwt_identity()
    
    deleted = ConversationService.delete(conversation_id, user_id)
    
    if not deleted:
        return error_response('CONVERSATION_NOT_FOUND', 'Conversation not found', 404)
    
    return success_response(message='Conversation deleted successfully')
