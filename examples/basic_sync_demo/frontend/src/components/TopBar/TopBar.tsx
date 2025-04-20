import { Flex, Button, ButtonGroup, Tooltip, useToast } from '@chakra-ui/react';
import { FaUpload, FaSignOutAlt, FaSync } from 'react-icons/fa';
import { useRef, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { uploadFile } from '../../services/files';

const TopBar = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const toast = useToast();
  const { logout } = useAuth();

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      await uploadFile(file);
      toast({
        title: "File uploaded",
        description: `Successfully uploaded ${file.name}`,
        status: "success",
        duration: 3000,
      });
      window.location.reload();
    } catch (error: any) {
      toast({
        title: "Upload failed",
        description: error.response?.data?.detail || "Failed to upload file",
        status: "error",
        duration: 3000,
      });
    } finally {
      setIsUploading(false);
    }
  };

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      // TODO: Add sync functionality
      toast({
        title: "Sync complete",
        status: "success",
        duration: 3000,
      });
      window.location.reload();
    } catch (error) {
      toast({
        title: "Sync failed",
        status: "error",
        duration: 3000,
      });
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <Flex p={4} borderBottom="1px" borderColor="gray.200" align="center" justify="space-between">
      <ButtonGroup spacing={3}>
        <Tooltip label="Upload files">
          <Button
            leftIcon={<FaUpload />}
            colorScheme="blue"
            onClick={() => fileInputRef.current?.click()}
            isLoading={isUploading}
          >
            Upload
          </Button>
        </Tooltip>
        <Tooltip label="Sync files">
          <Button
            leftIcon={<FaSync />}
            onClick={handleSync}
            isLoading={isSyncing}
            variant="outline"
          >
            Sync
          </Button>
        </Tooltip>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleUpload}
        />
      </ButtonGroup>
      
      <Button
        leftIcon={<FaSignOutAlt />}
        variant="ghost"
        onClick={logout}
      >
        Logout
      </Button>
    </Flex>
  );
};

export default TopBar; 