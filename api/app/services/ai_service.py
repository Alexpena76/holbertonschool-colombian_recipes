"""
AI Service - Claude API integration for cooking assistant
"""
import requests
from flask import current_app


class AIService:
    """Service class for AI assistant operations."""
    
    CLAUDE_API_URL = 'https://api.anthropic.com/v1/messages'
    
    @staticmethod
    def build_prompt(recipe, question, language='en'):
        """
        Build a contextual prompt for the AI assistant.
        
        Args:
            recipe: Recipe object
            question: User's question
            language: Response language (en/es)
        
        Returns:
            Formatted prompt string
        """
        # Format ingredients
        ingredients_list = '\n'.join([
            f"- {ing.name}: {ing.amount} {ing.unit}" if ing.amount else f"- {ing.name}"
            for ing in recipe.ingredients
        ])
        
        # Format steps
        steps_list = '\n'.join([
            f"{step.step_number}. {step.instruction}"
            for step in recipe.steps
        ])
        
        lang_instruction = "Respond in Spanish." if language == 'es' else "Respond in English."
        
        prompt = f"""You are a friendly Colombian cooking assistant helping someone prepare {recipe.name}.

RECIPE CONTEXT:
Name: {recipe.name}
Region: {recipe.region}
Difficulty: {recipe.difficulty}
Prep Time: {recipe.prep_time_minutes} minutes
Cook Time: {recipe.cook_time_minutes} minutes
Servings: {recipe.servings}

INGREDIENTS:
{ingredients_list}

COOKING STEPS:
{steps_list}

DESCRIPTION:
{recipe.description}

USER'S QUESTION:
{question}

{lang_instruction}
Please provide helpful, practical cooking advice. Be encouraging and share any traditional Colombian cooking tips when relevant. Keep your response concise but thorough."""

        return prompt
    
    @staticmethod
    def ask(recipe, question, language='en'):
        """
        Send a question to the AI assistant.
        
        Args:
            recipe: Recipe object for context
            question: User's question
            language: Response language (en/es)
        
        Returns:
            Dict with response and tips, or None on error
        """
        api_key = current_app.config.get('CLAUDE_API_KEY')
        model = current_app.config.get('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
        
        if not api_key:
            return {
                'response': "I'm sorry, the AI assistant is not configured. Please contact support.",
                'tips': []
            }
        
        prompt = AIService.build_prompt(recipe, question, language)
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                'model': model,
                'max_tokens': 1024,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ]
            }
            
            response = requests.post(
                AIService.CLAUDE_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data['content'][0]['text']
                
                return {
                    'response': ai_response,
                    'tips': AIService._extract_tips(ai_response)
                }
            else:
                return {
                    'response': "I'm having trouble connecting right now. Please try again in a moment.",
                    'tips': []
                }
                
        except requests.exceptions.Timeout:
            return {
                'response': "The request timed out. Please try again.",
                'tips': []
            }
        except Exception as e:
            current_app.logger.error(f"AI Service error: {str(e)}")
            return {
                'response': "An error occurred. Please try again later.",
                'tips': []
            }
    
    @staticmethod
    def _extract_tips(response):
        """Extract cooking tips from AI response."""
        tips = []
        
        # Look for bullet points or numbered tips
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '• ', '* ')) and len(line) > 10:
                tip = line.lstrip('-•* ').strip()
                if len(tip) < 200:  # Only short tips
                    tips.append(tip)
        
        return tips[:5]  # Max 5 tips
