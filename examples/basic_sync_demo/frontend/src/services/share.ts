import api from './api';

export const createShareLink = async (fileId: string, permission: string = 'READ', expiresInDays: number = 7) => {
  const response = await api.post(`/share/${fileId}`, {
    permission,
    expires_in_days: expiresInDays
  });
  return response.data;
};

export const getSharedFile = async (token: string) => {
  const response = await api.get(`/share/access/${token}`);
  return response.data;
};

export const revokeShareLink = async (token: string) => {
  const response = await api.delete(`/share/${token}`);
  return response.data;
};

export const listShares = async () => {
  const response = await api.get('/share/list');
  return response.data;
}; 