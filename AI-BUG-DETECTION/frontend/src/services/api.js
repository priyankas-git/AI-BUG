// Shared File: API service interface using Axios
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // GET /api/health
  checkHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // POST /api/analyze
  analyzeCode: async (language, code, fileName, projectId = null) => {
    const response = await apiClient.post('/analyze', {
      language,
      code,
      file_name: fileName,
      project_id: projectId
    });
    return response.data;
  },

  // POST /api/fix
  generateFix: async (bugId) => {
    const response = await apiClient.post('/fix', { bug_id: bugId });
    return response.data;
  },

  // POST /api/validate
  validateFix: async (bugId, fixedCode) => {
    const response = await apiClient.post('/validate', {
      bug_id: bugId,
      fixed_code: fixedCode
    });
    return response.data;
  },

  // GET /api/bugs
  getBugs: async () => {
    const response = await apiClient.get('/bugs');
    return response.data;
  },

  // GET /api/bugs/{bug_id}
  getBugDetails: async (bugId) => {
    const response = await apiClient.get(`/bugs/${bugId}`);
    return response.data;
  },

  // GET /api/dashboard
  getDashboardStats: async () => {
    const response = await apiClient.get('/dashboard');
    return response.data;
  },

  // GET /api/projects
  getProjects: async () => {
    const response = await apiClient.get('/projects');
    return response.data;
  }
};

export default api;
