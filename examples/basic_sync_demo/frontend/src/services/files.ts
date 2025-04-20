import api from './api';

export const uploadFile = async (file: File, folderId?: string) => {
  const formData = new FormData();
  formData.append('upload_file', file);
  if (folderId) {
    formData.append('folder_id', folderId);
  }
  
  return api.post('/files/upload', formData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    }
  });
};

export const downloadFile = async (fileId: string) => {
  const response = await api.get(`/files/download/${fileId}`, {
    responseType: 'blob'
  });
  return response.data;
};

export const listFiles = async () => {
  const token = localStorage.getItem('token');
  const response = await api.get('/files/list', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.data;
}; 