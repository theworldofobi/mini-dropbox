import api from './api';

export const initSync = async (lastSyncTimestamp: number = 0) => {
  const response = await api.post('/sync/init', {
    last_sync_ts: lastSyncTimestamp
  });
  return response.data;
};

export const resolveConflict = async (fileId: string, resolution: 'local' | 'remote') => {
  const response = await api.post('/sync/resolve', {
    file_id: fileId,
    resolution
  });
  return response.data;
}; 