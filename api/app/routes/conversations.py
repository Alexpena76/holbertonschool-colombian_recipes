"""
Conversation Routes - Sprint 2
Manage AI conversation history
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.response_service import success_response, error_response, paginate

conversations_bp = Blueprint('conversations', __name__)


@conversations_bp.route('', methods=['GET'])
@jwt_required()
def get_conversations():
    """
    Get user's conversation history
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20, max: 50)
    
    Returns:
        200: List of conversations with pagination
    """
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 50)
    
    # Get conversations ordered by most recent
    query = Conversation.query.filter_by(user_id=int(user_id))\
        .order_by(Conversation.updated_at.desc())
    
    conversations, pagination = paginate(query, page=page, per_page=per_page)
    
    return success_response(
        data={'conversations': [conv.to_dict() for conv in conversations]},
        pagination=pagination
    )


@conversations_bp.route('/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    """
    Get conversation with all messages
    
    Path Parameters:
        conversation_id (int): Conversation ID
    
    Returns:
        200: Conversation with messages
        404: Conversation not found
    """
    user_id = get_jwt_identity()
    
    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=int(user_id)
    ).first()
    
    if not conversation:
        return error_response('CONVERSATION_NOT_FOUND', 'Conversation not found', 404)
    
    return success_response(data={
        'conversation': conversation.to_dict(include_messages=True)
    })


@conversations_bp.route('/<int:conversation_id>', methods=['DELETE'])
@jwt_required()
def delete_conversation(conversation_id):
    """
    Delete a conversation
    
    Path Parameters:
        conversation_id (int): Conversation ID
    
    Returns:
        200: Conversation deleted
        404: Conversation not found
    """
    user_id = get_jwt_identity()
    
    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=int(user_id)
    ).first()
    
    if not conversation:
        return error_response('CONVERSATION_NOT_FOUND', 'Conversation not found', 404)
    
    try:
        db.session.delete(conversation)
        db.session.commit()
        
        return success_response(message='Conversation deleted successfully')
    
    except Exception as e:
        db.session.rollback()
        return error_response('DELETE_FAILED', 'Failed to delete conversation', 500)


@conversations_bp.route('/<int:conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    """
    Get messages for a conversation with pagination
    
    Path Parameters:
        conversation_id (int): Conversation ID
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 50, max: 100)
    
    Returns:
        200: List of messages with pagination
        404: Conversation not found
    """
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 50, type=int), 100)
    
    # Verify conversation belongs to user
    conversation = Conversation.query.filter_by(
        id=conversation_id,
        user_id=int(user_id)
    ).first()
    
    if not conversation:
        return error_response('CONVERSATION_NOT_FOUND', 'Conversation not found', 404)
    
    # Get messages
    query = Message.query.filter_by(conversation_id=conversation_id)\
        .order_by(Message.created_at)
    
    messages, pagination = paginate(query, page=page, per_page=per_page)
    
    return success_response(
        data={'messages': [msg.to_dict() for msg in messages]},
        pagination=pagination
    )
