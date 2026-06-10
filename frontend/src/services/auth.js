import api from './api';

export const login = async (username, password) => {
  const res = await api.post('/accounts/login/', { username, password });
  return res.data;
};

export const register = async (data) => {
  const res = await api.post('/accounts/register/', data);
  return res.data;
};

export const getCurrentUser = async () => {
  const res = await api.get('/accounts/current-user/');
  return res.data;
};
