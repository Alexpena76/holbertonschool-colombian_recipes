"""
AI Assistant Routes
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.recipe_service import RecipeService
from app.services.ai_service import AIService
from app.services.conversation_service import ConversationService
from app.services.response_service import success_response, error_response

assistant_bp = Blueprint('assistant', __name__)


@assistant_bp.route('/ask', methods=['POST'])
@jwt_required()
def ask():
    """Ask the AI cooking assistant a question."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return error_response('INVALID_REQUEST', 'Request body is required', 400)
    
    recipe_id = data.get('recipe_id')
    question = data.get('question', '').strip()
    conversation_id = data.get('conversation_id')
    language = data.get('language', 'en')
    
    if not recipe_id:
        return error_response('INVALID_REQUEST', 'recipe_id is required', 400)
    
    if not question:
        return error_response('INVALID_REQUEST', 'question is required', 400)
    
    if language not in ['en', 'es']:
        language = 'en'
    
    # Get recipe
    recipe = RecipeService.get_by_id(recipe_id)
    if not recipe:
        return error_response('RECIPE_NOT_FOUND', f'Recipe "{recipe_id}" not found', 404)
    
    # Get or create conversation
    conversation = ConversationService.get_or_create(user_id, recipe_id, conversation_id)
    
    # Save user message
    ConversationService.add_message(conversation.id, 'user', question)
    
    # Get AI response
    result = AIService.ask(recipe, question, language)
    
    # Save AI response
    ConversationService.add_message(conversation.id, 'assistant', result['response'])
    
    # Update conversation title if new
    if not conversation.title:
        conversation.title = question[:50] + ('...' if len(question) > 50 else '')
        from app import db
        db.session.commit()
    
    return success_response(
        data={
            'conversation_id': conversation.id,
            'recipe_id': recipe_id,
            'response': result['response'],
            'tips': result.get('tips', [])
        }
    )
