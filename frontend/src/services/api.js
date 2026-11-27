import axios from 'axios';

let rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
// Ensure no trailing slash
rawUrl = rawUrl.replace(/\/+$/, '');
// Ensure /api/v1 suffix is present
const API_BASE_URL = rawUrl.endsWith('/api/v1') ? rawUrl : `${rawUrl}/api/v1`;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smartfridge_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for unified error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('smartfridge_token');
    }
    return Promise.reject(error);
  }
);

export const systemService = {
  getHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
