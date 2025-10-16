import axios from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8002';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth headers if needed
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken');
      // window.location.href = '/login';
    }
    
    // Return a more user-friendly error
    const errorMessage = error.response?.data?.message || error.message || 'An error occurred';
    return Promise.reject({
      ...error,
      message: errorMessage,
      status: error.response?.status,
    });
  }
);

// Service Desk API endpoints
export const serviceDeskAPI = {
  // Get all tickets
  getTickets: async (params = {}) => {
    const response = await api.get('/api/v1/tickets', { params });
    return response.data;
  },

  // Get ticket by ID
  getTicket: async (ticketId) => {
    const response = await api.get(`/api/v1/tickets/${ticketId}`);
    return response.data;
  },

  // Create new ticket
  createTicket: async (ticketData) => {
    const response = await api.post('/api/v1/tickets', ticketData);
    return response.data;
  },

  // Update ticket
  updateTicket: async (ticketId, updateData) => {
    const response = await api.put(`/service-desk/tickets/${ticketId}`, updateData);
    return response.data;
  },

  // Assign ticket
  assignTicket: async (ticketId, agentId) => {
    const response = await api.patch(`/service-desk/tickets/${ticketId}/assign`, {
      assigned_to: agentId,
    });
    return response.data;
  },

  // Update ticket status
  updateTicketStatus: async (ticketId, status) => {
    const response = await api.patch(`/service-desk/tickets/${ticketId}/status`, {
      status,
    });
    return response.data;
  },

  // Categorize ticket using AI
  categorizeTicket: async (ticketId) => {
    const response = await api.post(`/service-desk/tickets/${ticketId}/categorize`);
    return response.data;
  },

  // Route ticket using AI
  routeTicket: async (ticketId) => {
    const response = await api.post(`/service-desk/tickets/${ticketId}/route`);
    return response.data;
  },

  // Get ticket analytics
  getTicketAnalytics: async (params = {}) => {
    const response = await api.get('/service-desk/analytics', { params });
    return response.data;
  },
};

// Knowledge Base API endpoints
export const knowledgeBaseAPI = {
  // Search articles
  searchArticles: async (query, filters = {}) => {
    const response = await api.get('/knowledge-base/search', {
      params: { query, ...filters },
    });
    return response.data;
  },

  // Get all articles
  getArticles: async (params = {}) => {
    const response = await api.get('/knowledge-base/articles', { params });
    return response.data;
  },

  // Get article by ID
  getArticle: async (articleId) => {
    const response = await api.get(`/knowledge-base/articles/${articleId}`);
    return response.data;
  },

  // Create new article
  createArticle: async (articleData) => {
    const response = await api.post('/knowledge-base/articles', articleData);
    return response.data;
  },

  // Update article
  updateArticle: async (articleId, updateData) => {
    const response = await api.put(`/knowledge-base/articles/${articleId}`, updateData);
    return response.data;
  },

  // Delete article
  deleteArticle: async (articleId) => {
    const response = await api.delete(`/knowledge-base/articles/${articleId}`);
    return response.data;
  },

  // Analyze knowledge gaps
  analyzeGaps: async () => {
    const response = await api.post('/knowledge-base/analyze-gaps');
    return response.data;
  },

  // Generate article suggestions
  generateSuggestions: async (ticketData) => {
    const response = await api.post('/knowledge-base/generate-suggestions', ticketData);
    return response.data;
  },
};

// Chatbot API endpoints
export const chatbotAPI = {
  // Send message to chatbot
  sendMessage: async (message, sessionId = null) => {
    const response = await api.post('/chatbot/message', {
      message,
      session_id: sessionId,
    });
    return response.data;
  },

  // Get chat session
  getSession: async (sessionId) => {
    const response = await api.get(`/chatbot/sessions/${sessionId}`);
    return response.data;
  },

  // Create new chat session
  createSession: async () => {
    const response = await api.post('/chatbot/sessions');
    return response.data;
  },

  // Get chat history
  getChatHistory: async (sessionId) => {
    const response = await api.get(`/chatbot/sessions/${sessionId}/history`);
    return response.data;
  },

  // Clear chat session
  clearSession: async (sessionId) => {
    const response = await api.delete(`/chatbot/sessions/${sessionId}`);
    return response.data;
  },
};

// Dashboard API endpoints
export const dashboardAPI = {
  // Get dashboard overview
  getOverview: async () => {
    const response = await api.get('/dashboard/overview');
    return response.data;
  },

  // Get ticket metrics
  getTicketMetrics: async (timeRange = '7d') => {
    const response = await api.get('/dashboard/ticket-metrics', {
      params: { time_range: timeRange },
    });
    return response.data;
  },

  // Get agent performance
  getAgentPerformance: async () => {
    const response = await api.get('/dashboard/agent-performance');
    return response.data;
  },

  // Get system health
  getSystemHealth: async () => {
    const response = await api.get('/dashboard/system-health');
    return response.data;
  },
};

// Mock data generators for development (when backend is not available)
export const mockData = {
  tickets: [
    {
      id: 1,
      title: 'Cannot access email',
      description: 'User unable to login to Outlook',
      status: 'open',
      priority: 'medium',
      category: 'Email',
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T10:30:00Z',
      assigned_to: null,
      requester: 'john.doe@company.com',
    },
    {
      id: 2,
      title: 'VPN connection issues',
      description: 'Cannot connect to company VPN from home',
      status: 'in_progress',
      priority: 'high',
      category: 'Network',
      created_at: '2024-01-15T09:15:00Z',
      updated_at: '2024-01-15T11:45:00Z',
      assigned_to: 'agent-1',
      requester: 'jane.smith@company.com',
    },
    {
      id: 3,
      title: 'Software installation request',
      description: 'Need Adobe Creative Suite installed on workstation',
      status: 'resolved',
      priority: 'low',
      category: 'Software',
      created_at: '2024-01-14T14:20:00Z',
      updated_at: '2024-01-15T08:30:00Z',
      assigned_to: 'agent-2',
      requester: 'bob.johnson@company.com',
    },
  ],

  articles: [
    {
      id: 1,
      title: 'How to Reset Your Password',
      content: 'Step-by-step guide to reset your company password...',
      category: 'Account Management',
      tags: ['password', 'security', 'login'],
      created_at: '2024-01-10T12:00:00Z',
      updated_at: '2024-01-12T15:30:00Z',
      author: 'IT Admin',
    },
    {
      id: 2,
      title: 'VPN Setup Guide',
      content: 'Instructions for setting up VPN connection...',
      category: 'Network',
      tags: ['vpn', 'remote', 'connection'],
      created_at: '2024-01-08T10:15:00Z',
      updated_at: '2024-01-08T10:15:00Z',
      author: 'Network Admin',
    },
  ],

  dashboardStats: {
    totalTickets: 156,
    openTickets: 23,
    resolvedToday: 12,
    avgResolutionTime: '2.5 hours',
    agentWorkload: 85,
    systemUptime: 99.9,
  },
};

// Development mode helpers
const isDevelopment = process.env.NODE_ENV === 'development';

// Wrapper functions that use mock data in development when API fails
export const apiWithFallback = {
  getTickets: async (params) => {
    try {
      return await serviceDeskAPI.getTickets(params);
    } catch (error) {
      if (isDevelopment) {
        console.warn('API call failed, using mock data:', error.message);
        return { tickets: mockData.tickets, total: mockData.tickets.length };
      }
      throw error;
    }
  },

  getTicket: async (ticketId) => {
    try {
      return await serviceDeskAPI.getTicket(ticketId);
    } catch (error) {
      if (isDevelopment) {
        console.warn('API call failed, using mock data:', error.message);
        const mockTicket = mockData.tickets.find(t => t.id.toString() === ticketId.toString());
        return { data: mockTicket || mockData.tickets[0] };
      }
      throw error;
    }
  },

  getArticles: async (params) => {
    try {
      return await knowledgeBaseAPI.getArticles(params);
    } catch (error) {
      if (isDevelopment) {
        console.warn('API call failed, using mock data:', error.message);
        return { articles: mockData.articles, total: mockData.articles.length };
      }
      throw error;
    }
  },

  getDashboardStats: async () => {
    try {
      return await dashboardAPI.getOverview();
    } catch (error) {
      if (isDevelopment) {
        console.warn('API call failed, using mock data:', error.message);
        return mockData.dashboardStats;
      }
      throw error;
    }
  },
};

export default api;
