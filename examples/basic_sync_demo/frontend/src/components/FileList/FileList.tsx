import { Table, Thead, Tbody, Tr, Th, Box, Text } from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import FileItem from './FileItem';
import { listFiles } from '../../services/files';

interface File {
  id: string;
  name: string;
  type: 'file' | 'folder';
  modified: string;
  size?: string;
}

const FileList = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFiles = async () => {
    try {
      const response = await listFiles();
      setFiles(response.files);
    } catch (error) {
      console.error('Failed to fetch files:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <Box>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Modified</Th>
            <Th>Size</Th>
            <Th width="100px">Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {files.map(file => (
            <FileItem 
              key={file.id} 
              file={file} 
              onRefresh={fetchFiles}
            />
          ))}
        </Tbody>
      </Table>
      {files.length === 0 && (
        <Text textAlign="center" py={8} color="gray.500">
          No files found
        </Text>
      )}
    </Box>
  );
};

export default FileList; 