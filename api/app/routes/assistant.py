"""
AI Assistant Routes - Sprint 2
With multi-provider fallback support
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.recipe import Recipe
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.ai_service import get_ai_service
from app.services.response_service import success_response, error_response

assistant_bp = Blueprint('assistant', __name__)


@assistant_bp.route('/ask', methods=['POST'])
@jwt_required()
def ask_question():
    """
    Ask the AI cooking assistant a question
    
    Request Body:
        recipe_id (str, optional): Recipe to ask about
        question (str): User's cooking question
        conversation_id (int, optional): Continue existing conversation
        language (str, optional): Response language (en, es)
    
    Returns:
        200: AI response with conversation ID
        400: Validation error
        404: Recipe or conversation not found
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_REQUEST', 'Request body is required', 400)
    
    recipe_id = data.get('recipe_id')
    question = data.get('question', '').strip()
    conversation_id = data.get('conversation_id')
    language = data.get('language', 'en')
    
    # Validate question
    if not question:
        return error_response('VALIDATION_ERROR', 'Question is required', 400)
    
    if len(question) < 3:
        return error_response('VALIDATION_ERROR', 'Question is too short', 400)
    
    if len(question) > 1000:
        return error_response('VALIDATION_ERROR', 'Question is too long (max 1000 characters)', 400)
    
    # Get recipe context if provided
    recipe = None
    recipe_context = None
    if recipe_id:
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return error_response('RECIPE_NOT_FOUND', f'Recipe "{recipe_id}" not found', 404)
        recipe_context = recipe.to_context_string()
    
    # Get or create conversation
    conversation = None
    conversation_history = []
    
    if conversation_id:
        conversation = Conversation.query.filter_by(
            id=conversation_id,
            user_id=int(user_id)
        ).first()
        
        if not conversation:
            return error_response('CONVERSATION_NOT_FOUND', 'Conversation not found', 404)
        
        # Load conversation history
        messages = Message.query.filter_by(conversation_id=conversation.id)\
            .order_by(Message.created_at).all()
        conversation_history = [{'role': m.role, 'content': m.content} for m in messages]
    else:
        # Create new conversation
        title = f"Questions about {recipe.name}" if recipe else "Cooking questions"
        conversation = Conversation(
            user_id=int(user_id),
            recipe_id=recipe_id,
            title=title
        )
        db.session.add(conversation)
        db.session.commit()
    
    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role='user',
        content=question
    )
    db.session.add(user_message)
    
    # Get AI response
    ai_service = get_ai_service()
    result = ai_service.get_response(
        question=question,
        recipe_context=recipe_context,
        conversation_history=conversation_history,
        language=language
    )
    
    # Save AI response
    assistant_message = Message(
        conversation_id=conversation.id,
        role='assistant',
        content=result['response']
    )
    db.session.add(assistant_message)
    db.session.commit()
    
    return success_response(data={
        'conversation_id': conversation.id,
        'recipe_id': recipe_id,
        'recipe_name': recipe.name if recipe else None,
        'question': question,
        'response': result['response'],
        'provider': result.get('provider', 'unknown'),
        'tips': result.get('tips', []),
        'language': language
    })


@assistant_bp.route('/substitute', methods=['POST'])
@jwt_required()
def get_substitution():
    """
    Get ingredient substitution suggestions
    
    Request Body:
        ingredient (str): Ingredient to substitute
        recipe_id (str, optional): Recipe context
        reason (str, optional): Reason for substitution
        language (str, optional): Response language (en, es)
    
    Returns:
        200: Substitution suggestions
        400: Validation error
    """
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_REQUEST', 'Request body is required', 400)
    
    ingredient = data.get('ingredient', '').strip()
    recipe_id = data.get('recipe_id')
    reason = data.get('reason', 'unavailable')
    language = data.get('language', 'en')
    
    if not ingredient:
        return error_response('VALIDATION_ERROR', 'Ingredient is required', 400)
    
    # Get recipe name if provided
    recipe_name = None
    if recipe_id:
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            recipe_name = recipe.name
    
    # Get substitution
    ai_service = get_ai_service()
    result = ai_service.get_substitution(
        ingredient=ingredient,
        recipe_name=recipe_name,
        reason=reason,
        language=language
    )
    
    return success_response(data=result)


@assistant_bp.route('/status', methods=['GET'])
@jwt_required()
def get_ai_status():
    """
    Get AI service status and provider information
    
    Returns:
        200: AI service status including available providers
    """
    ai_service = get_ai_service()
    status = ai_service.get_status()
    
    return success_response(data=status)
