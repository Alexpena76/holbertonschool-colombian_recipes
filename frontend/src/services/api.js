import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (email, password, name) => api.post('/auth/register', { email, password, name }),
  me: () => api.get('/auth/me'),
};

// Recipes
export const recipesAPI = {
  getAll: (params = {}) => api.get('/recipes', { params }),
  getById: (id) => api.get(`/recipes/${id}`),
  search: (query) => api.get('/recipes/search', { params: { q: query } }),
};

// Categories
export const categoriesAPI = {
  getAll: () => api.get('/categories'),
  getById: (id) => api.get(`/categories/${id}`),
};

// AI Assistant
export const assistantAPI = {
  ask: (question, recipeId = null, conversationId = null, language = 'en') =>
    api.post('/assistant/ask', {
      question,
      recipe_id: recipeId,
      conversation_id: conversationId,
      language,
    }),
  substitute: (ingredient, recipeId = null, reason = 'unavailable', language = 'en') =>
    api.post('/assistant/substitute', {
      ingredient,
      recipe_id: recipeId,
      reason,
      language,
    }),
  status: () => api.get('/assistant/status'),
};

// Conversations
export const conversationsAPI = {
  getAll: (params = {}) => api.get('/conversations', { params }),
  getById: (id) => api.get(`/conversations/${id}`),
  delete: (id) => api.delete(`/conversations/${id}`),
};

export default api;
