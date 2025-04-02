import api from './api';

export const uploadFile = async (file: File, folderId?: string) => {
  console.log("uploading file")
  const formData = new FormData();
  formData.append('file', file);
  if (folderId) {
    formData.append('folder_id', folderId);
  }
  console.log("appended to formdata")
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
  const response = await api.get('/files/list');
  return response.data;
}; 