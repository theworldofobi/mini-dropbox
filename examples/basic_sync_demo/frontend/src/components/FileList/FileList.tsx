import { Table, Thead, Tbody, Tr, Th, Box, Spinner, Center } from '@chakra-ui/react';
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
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await listFiles();
        setFiles(response.files);
      } catch (error) {
        console.error('Failed to fetch files:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFiles();
  }, []);

  if (isLoading) {
    return (
      <Center h="200px">
        <Spinner />
      </Center>
    );
  }

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
          {files.map((file: any) => (
            <FileItem key={file.id} file={file} />
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default FileList; 