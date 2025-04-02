import api from './api';

export const login = async (username: string, password: string) => {
  const response = await api.post('/auth/login', { username, password });
  localStorage.setItem('token', response.data.access_token);
  return response.data;
};

export const signup = async (username: string, password: string) => {
  const response = await api.post('/auth/signup', { username, password });
  return response.data;
};

export const logout = async () => {
  await api.post('/auth/logout');
  localStorage.removeItem('token');
}; 