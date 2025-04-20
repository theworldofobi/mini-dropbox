import { Tr, Td, ButtonGroup, IconButton, HStack, Text, useToast } from '@chakra-ui/react';
import { FaDownload, FaFile, FaFolder } from 'react-icons/fa';
import { useState } from 'react';
import { downloadFile } from '../../services/files';

interface FileItemProps {
  file: {
    file_id: string;
    original_name: string;
    type: 'file' | 'folder';
    created_at: string;
    size: number;
  };
}

const FileItem = ({ file }: FileItemProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const handleDownload = async () => {
    setIsLoading(true);
    try {
      const blob = await downloadFile(file.file_id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.original_name;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      toast({
        title: "Download failed",
        status: "error",
        duration: 3000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Tr _hover={{ bg: 'gray.50' }}>
      <Td>
        <HStack>
          {file.type === 'folder' ? <FaFolder color="#7B8B9A" /> : <FaFile color="#7B8B9A" />}
          <Text>{file.original_name}</Text>
        </HStack>
      </Td>
      <Td>{formatDate(file.created_at)}</Td>
      <Td>{typeof file.size === 'number' ? formatSize(file.size) : '--'}</Td>
      <Td>
        <ButtonGroup size="sm" spacing={2}>
          <IconButton
            aria-label="Download"
            icon={<FaDownload />}
            onClick={handleDownload}
            isLoading={isLoading}
            variant="ghost"
          />
        </ButtonGroup>
      </Td>
    </Tr>
  );
};

export default FileItem; 