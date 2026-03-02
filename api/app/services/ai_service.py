"""
Multi-Provider AI Service with Automatic Fallback
Supports: Claude (Anthropic), OpenAI (ChatGPT), Google (Gemini), Groq
"""
import os
import time
import requests
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.is_available = bool(api_key)
        self.last_error = None
        self.rate_limited_until = 0
    
    @abstractmethod
    def get_response(self, messages: list, system_prompt: str) -> str:
        """Get response from the AI provider"""
        pass
    
    @property
    def name(self) -> str:
        return self.__class__.__name__
    
    def is_rate_limited(self) -> bool:
        """Check if currently rate limited"""
        return time.time() < self.rate_limited_until
    
    def set_rate_limited(self, seconds: int = 60):
        """Set rate limit cooldown"""
        self.rate_limited_until = time.time() + seconds


class ClaudeProvider(AIProvider):
    """Anthropic Claude API Provider"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv('ANTHROPIC_API_KEY', ''))
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-sonnet-4-20250514"
    
    def get_response(self, messages: list, system_prompt: str) -> str:
        if not self.is_available:
            raise Exception("Claude API key not configured")
        
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": messages
        }
        
        response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 429:
            self.set_rate_limited(60)
            raise Exception("Rate limited")
        
        if response.status_code != 200:
            raise Exception(f"Claude API error: {response.status_code}")
        
        result = response.json()
        return result['content'][0]['text']


class OpenAIProvider(AIProvider):
    """OpenAI ChatGPT API Provider"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv('OPENAI_API_KEY', ''))
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
    
    def get_response(self, messages: list, system_prompt: str) -> str:
        if not self.is_available:
            raise Exception("OpenAI API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Format messages for OpenAI
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            formatted_messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        data = {
            "model": self.model,
            "messages": formatted_messages,
            "max_tokens": 1024
        }
        
        response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 429:
            self.set_rate_limited(60)
            raise Exception("Rate limited")
        
        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.status_code}")
        
        result = response.json()
        return result['choices'][0]['message']['content']


class GeminiProvider(AIProvider):
    """Google Gemini API Provider"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv('GOOGLE_API_KEY', ''))
        self.model = "gemini-pro"
    
    @property
    def base_url(self):
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
    
    def get_response(self, messages: list, system_prompt: str) -> str:
        if not self.is_available:
            raise Exception("Google API key not configured")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Format messages for Gemini
        parts = [{"text": system_prompt + "\n\n"}]
        for msg in messages:
            role_prefix = "User: " if msg['role'] == 'user' else "Assistant: "
            parts.append({"text": role_prefix + msg['content'] + "\n"})
        
        data = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "maxOutputTokens": 1024
            }
        }
        
        response = requests.post(
            f"{self.base_url}?key={self.api_key}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 429:
            self.set_rate_limited(60)
            raise Exception("Rate limited")
        
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code}")
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']


class GroqProvider(AIProvider):
    """Groq API Provider (Fast & Free tier)"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key or os.getenv('GROQ_API_KEY', ''))
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"
    
    def get_response(self, messages: list, system_prompt: str) -> str:
        if not self.is_available:
            raise Exception("Groq API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Format messages (OpenAI compatible)
        formatted_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            formatted_messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        data = {
            "model": self.model,
            "messages": formatted_messages,
            "max_tokens": 1024
        }
        
        response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 429:
            self.set_rate_limited(60)
            raise Exception("Rate limited")
        
        if response.status_code != 200:
            raise Exception(f"Groq API error: {response.status_code}")
        
        result = response.json()
        return result['choices'][0]['message']['content']


class AIService:
    """
    Multi-Provider AI Service with Automatic Fallback
    
    Tries providers in order: Claude → OpenAI → Gemini → Groq
    Automatically switches to next provider on rate limit or error
    """
    
    def __init__(self):
        # Initialize all providers
        self.providers = [
            ClaudeProvider(),
            OpenAIProvider(),
            GeminiProvider(),
            GroqProvider()
        ]
        
        # Filter to only available providers
        self.available_providers = [p for p in self.providers if p.is_available]
        
        # Track usage
        self.current_provider_index = 0
        self.total_requests = 0
        self.provider_usage = {p.name: 0 for p in self.providers}
    
    def get_system_prompt(self, language: str = 'en') -> str:
        """Get system prompt for cooking assistant"""
        if language == 'es':
            return """Eres un asistente de cocina colombiana amigable y experto.
Tu trabajo es ayudar a los usuarios a preparar platos colombianos auténticos.

Directrices:
- Sé cálido, alentador y paciente
- Da consejos prácticos específicos para la cocina colombiana
- Si algo sale mal, ofrece soluciones
- Comparte consejos de abuelas colombianas cuando sea relevante
- Mantén las respuestas concisas pero útiles (máximo 3 párrafos)
- Usa emojis ocasionalmente para ser amigable 🇨🇴

Siempre responde en español."""
        
        return """You are a friendly and expert Colombian cooking assistant.
Your job is to help users prepare authentic Colombian dishes.

Guidelines:
- Be warm, encouraging, and patient
- Give practical advice specific to Colombian cooking
- If something goes wrong, offer solutions
- Share Colombian grandmother tips when relevant
- Keep responses concise but helpful (max 3 paragraphs)
- Use occasional emojis to be friendly 🇨🇴

Always respond in English."""
    
    def get_response(self, question: str, recipe_context: str = None, 
                     conversation_history: list = None, language: str = 'en') -> dict:
        """
        Get AI response with automatic provider fallback
        
        Args:
            question: User's question
            recipe_context: Recipe details for context
            conversation_history: Previous messages
            language: Response language (en/es)
        
        Returns:
            dict with response, provider used, and any tips
        """
        system_prompt = self.get_system_prompt(language)
        
        # Build messages
        messages = []
        
        # Add recipe context if provided
        if recipe_context:
            messages.append({
                "role": "user",
                "content": f"Here's the recipe I'm working with:\n{recipe_context}"
            })
            messages.append({
                "role": "assistant", 
                "content": "I see the recipe! I'm ready to help you with any questions about preparing this dish. What would you like to know?"
            })
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current question
        messages.append({
            "role": "user",
            "content": question
        })
        
        # Try each provider until one works
        errors = []
        for provider in self.available_providers:
            if provider.is_rate_limited():
                errors.append(f"{provider.name}: Rate limited")
                continue
            
            try:
                response_text = provider.get_response(messages, system_prompt)
                
                # Track usage
                self.total_requests += 1
                self.provider_usage[provider.name] += 1
                
                # Extract tips if present
                tips = self._extract_tips(response_text)
                
                return {
                    'success': True,
                    'response': response_text,
                    'provider': provider.name,
                    'tips': tips
                }
            
            except Exception as e:
                errors.append(f"{provider.name}: {str(e)}")
                continue
        
        # All providers failed
        return {
            'success': False,
            'response': self._get_fallback_response(question, language),
            'provider': 'fallback',
            'tips': [],
            'errors': errors
        }
    
    def _extract_tips(self, response_text: str) -> list:
        """Extract tips from response if present"""
        tips = []
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                tip = line[2:].strip()
                if 10 < len(tip) < 150:  # Reasonable tip length
                    tips.append(tip)
        return tips[:5]  # Max 5 tips
    
    def _get_fallback_response(self, question: str, language: str) -> str:
        """Return fallback response when all providers fail"""
        if language == 'es':
            return """¡Lo siento! Estoy teniendo dificultades técnicas en este momento. 

Aquí hay algunos consejos generales de cocina colombiana:
- La paciencia es clave - muchos platos colombianos requieren cocción lenta
- Si los frijoles están duros, añade una pizca de bicarbonato
- El hogao (sofrito de tomate y cebolla) es la base de muchos platos

Por favor intenta tu pregunta de nuevo en unos minutos. 🇨🇴"""
        
        return """I'm sorry! I'm having technical difficulties right now.

Here are some general Colombian cooking tips:
- Patience is key - many Colombian dishes require slow cooking
- If beans are hard, add a pinch of baking soda
- Hogao (tomato and onion sauce) is the base of many dishes

Please try your question again in a few minutes. 🇨🇴"""
    
    def get_status(self) -> dict:
        """Get status of all providers"""
        return {
            'total_requests': self.total_requests,
            'provider_usage': self.provider_usage,
            'providers': [
                {
                    'name': p.name,
                    'available': p.is_available,
                    'rate_limited': p.is_rate_limited()
                }
                for p in self.providers
            ]
        }
    
    def get_substitution(self, ingredient: str, recipe_name: str = None,
                         reason: str = 'unavailable', language: str = 'en') -> dict:
        """Get ingredient substitution suggestions"""
        
        if language == 'es':
            question = f"Necesito un sustituto para {ingredient}"
            if recipe_name:
                question += f" en la receta de {recipe_name}"
            question += f". Razón: {reason}. Dame 2-3 opciones con cantidades."
        else:
            question = f"I need a substitute for {ingredient}"
            if recipe_name:
                question += f" in the {recipe_name} recipe"
            question += f". Reason: {reason}. Give me 2-3 options with amounts."
        
        result = self.get_response(question, language=language)
        
        return {
            'original_ingredient': ingredient,
            'reason': reason,
            'suggestions': result['response'],
            'provider': result.get('provider')
        }


# Singleton instance
_ai_service = None

def get_ai_service() -> AIService:
    """Get or create AI service singleton"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
