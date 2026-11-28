import axios from 'axios';

let rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
rawUrl = rawUrl.replace(/\/+$/, '');
const API_BASE_URL = rawUrl.endsWith('/api/v1') ? rawUrl : `${rawUrl}/api/v1`;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Automatically injects JWT Bearer token
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

// Response interceptor: Clears token on 401 Unauthorized
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

export const authService = {
  login: async (email, password) => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },
  register: async (email, fullName, password) => {
    const response = await apiClient.post('/auth/register', {
      email,
      full_name: fullName,
      password,
    });
    return response.data;
  },
  getProfile: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },
  updateProfile: async (data) => {
    const response = await apiClient.put('/auth/me', data);
    return response.data;
  },
  getRefrigerators: async () => {
    const response = await apiClient.get('/auth/refrigerators');
    return response.data;
  },
};

export default apiClient;
