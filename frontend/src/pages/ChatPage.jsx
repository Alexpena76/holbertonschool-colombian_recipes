import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { assistantAPI, recipesAPI } from '../services/api';
import { Send, ChefHat, User, Loader2, Sparkles } from 'lucide-react';

export default function ChatPage() {
  const { recipeId } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [provider, setProvider] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (recipeId) {
      fetchRecipe();
    } else {
      // Add welcome message for general chat
      setMessages([{
        role: 'assistant',
        content: '¡Hola! 👋 I\'m your AI Colombian cooking assistant. Ask me anything about Colombian recipes, cooking techniques, ingredient substitutions, or traditional dishes!\n\nYou can also ask about a specific recipe by going to the Recipes page and clicking "Ask AI Chef".',
      }]);
    }
  }, [recipeId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchRecipe = async () => {
    try {
      const response = await recipesAPI.getById(recipeId);
      const recipeData = response.data.data;
      setRecipe(recipeData);
      
      // Add welcome message with recipe context
      setMessages([{
        role: 'assistant',
        content: `¡Hola! 👋 I see you're cooking **${recipeData.name}**${recipeData.name_es ? ` (${recipeData.name_es})` : ''}!\n\nI'm here to help you prepare this delicious Colombian dish. Ask me anything - cooking tips, ingredient substitutions, timing questions, or troubleshooting. ¡Buena suerte en la cocina! 🇨🇴`,
      }]);
    } catch (error) {
      console.error('Error fetching recipe:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await assistantAPI.ask(
        userMessage,
        recipeId || null,
        conversationId,
        'en'
      );

      const data = response.data.data;
      
      // Save conversation ID for continuity
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }
      
      // Track which AI provider responded
      setProvider(data.provider);

      // Add AI response to chat
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        provider: data.provider,
      }]);

    } catch (error) {
      console.error('Error getting AI response:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Lo siento, I had trouble processing that. Please try again! 🙏',
        isError: true,
      }]);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = recipeId ? [
    "What can I substitute for this ingredient?",
    "How do I know when it's done?",
    "Can I make this ahead of time?",
    "What should I serve with this?",
  ] : [
    "What's a good Colombian breakfast?",
    "How do I make arepas?",
    "What is bandeja paisa?",
    "Tell me about Colombian coffee",
  ];

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-4rem)] flex flex-col">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4">
        <div className="flex items-center space-x-3">
          <div className="bg-colombian-yellow p-2 rounded-full">
            <ChefHat className="h-6 w-6 text-colombian-blue" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-gray-900">AI Colombian Chef</h1>
            {recipe ? (
              <p className="text-sm text-gray-500">Helping with: {recipe.name}</p>
            ) : (
              <p className="text-sm text-gray-500">Your cooking assistant</p>
            )}
          </div>
          {provider && (
            <span className="ml-auto text-xs bg-gray-100 text-gray-500 px-2 py-1 rounded-full">
              Powered by {provider.replace('Provider', '')}
            </span>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-colombian-blue text-white rounded-br-md'
                  : message.isError
                  ? 'bg-red-50 text-red-700 border border-red-200 rounded-bl-md'
                  : 'bg-white text-gray-800 shadow-md rounded-bl-md'
              }`}
            >
              <div className="flex items-start space-x-2">
                {message.role === 'assistant' && (
                  <ChefHat className={`h-5 w-5 flex-shrink-0 mt-0.5 ${message.isError ? 'text-red-500' : 'text-colombian-yellow'}`} />
                )}
                <div className="flex-1">
                  <p className="whitespace-pre-wrap">{message.content}</p>
                </div>
                {message.role === 'user' && (
                  <User className="h-5 w-5 flex-shrink-0 mt-0.5 text-blue-200" />
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl rounded-bl-md px-4 py-3 shadow-md">
              <div className="flex items-center space-x-2">
                <ChefHat className="h-5 w-5 text-colombian-yellow" />
                <Loader2 className="h-5 w-5 animate-spin text-colombian-blue" />
                <span className="text-gray-500 text-sm">Cooking up a response...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions */}
      {messages.length <= 1 && (
        <div className="bg-white border-t px-6 py-3">
          <p className="text-xs text-gray-500 mb-2 flex items-center">
            <Sparkles className="h-3 w-3 mr-1" />
            Try asking:
          </p>
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => setInput(question)}
                className="text-sm bg-gray-100 hover:bg-colombian-yellow hover:text-colombian-blue px-3 py-1.5 rounded-full transition-colors"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="bg-white border-t px-6 py-4">
        <div className="flex space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything about Colombian cooking..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-colombian-blue focus:border-colombian-blue"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-colombian-blue text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
}
