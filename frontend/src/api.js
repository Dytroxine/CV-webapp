import axios from 'axios';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authLogin = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  const response = await api.post('/auth/login', formData);
  return response.data;
};

export const authRegister = async (email, password) => {
  const response = await api.post('/auth/register', { email, password });
  return response.data;
};

export const getResumes = async () => {
  const response = await api.get('/resumes/');
  return response.data;
};

export const createResume = async (resume) => {
  const response = await api.post('/resumes/', resume);
  return response.data;
};

export const improveResume = async (resumeId) => {
  const response = await api.post(`/resumes/${resumeId}/improve`);
  return response.data;
};