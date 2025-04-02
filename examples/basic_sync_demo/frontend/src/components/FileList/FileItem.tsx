import { Tr, Td, Button, ButtonGroup, IconButton, Menu, MenuButton, MenuList, MenuItem, HStack, Text, useToast } from '@chakra-ui/react';
import { FaFile, FaFolder, FaDownload, FaShare, FaTrash } from 'react-icons/fa';
import { downloadFile } from '../../services/files';
import { createShareLink } from '../../services/share';
import { useState } from 'react';

interface FileItemProps {
  file: {
    id: string;
    name: string;
    type: 'file' | 'folder';
    modified: string;
    size?: string;
  };
  onRefresh: () => void;
}

const FileItem = ({ file, onRefresh }: FileItemProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const handleDownload = async () => {
    setIsLoading(true);
    try {
      const blob = await downloadFile(file.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.name;
      a.click();
      window.URL.revokeObjectURL(url);
      
      toast({
        title: "Download started",
        description: `Downloading ${file.name}`,
        status: "success",
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: "Download failed",
        description: "Failed to download file",
        status: "error",
        duration: 3000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleShare = async () => {
    try {
      const shareData = await createShareLink(file.id);
      const shareUrl = `${window.location.origin}/share/${shareData.token}`;
      
      // Copy to clipboard
      await navigator.clipboard.writeText(shareUrl);
      
      toast({
        title: "Share link created",
        description: "Link copied to clipboard",
        status: "success",
        duration: 5000,
      });
    } catch (error) {
      toast({
        title: "Share failed",
        description: "Failed to create share link",
        status: "error",
        duration: 3000,
      });
    }
  };

  const handleDelete = async () => {
    // Implement delete functionality
  };

  return (
    <Tr _hover={{ bg: 'gray.50' }}>
      <Td>
        <HStack>
          {file.type === 'folder' ? <FaFolder color="#7B8B9A" /> : <FaFile color="#7B8B9A" />}
          <Text>{file.name}</Text>
        </HStack>
      </Td>
      <Td>{file.modified}</Td>
      <Td>{file.size || '--'}</Td>
      <Td>
        <ButtonGroup size="sm" spacing={2}>
          <IconButton
            aria-label="Download"
            icon={<FaDownload />}
            onClick={handleDownload}
            isLoading={isLoading}
            variant="ghost"
          />
          <IconButton
            aria-label="Share"
            icon={<FaShare />}
            onClick={handleShare}
            variant="ghost"
          />
          <IconButton
            aria-label="Delete"
            icon={<FaTrash />}
            colorScheme="red"
            variant="ghost"
          />
        </ButtonGroup>
      </Td>
    </Tr>
  );
};

export default FileItem; 