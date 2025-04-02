import { Flex, Input, Button, IconButton, ButtonGroup, Menu, MenuButton, MenuList, MenuItem, Tooltip, useToast } from '@chakra-ui/react';
import { BellIcon, QuestionIcon, ChevronDownIcon } from '@chakra-ui/icons';
import { FaUpload, FaFolderPlus, FaSync, FaSignOutAlt } from 'react-icons/fa';
import { useRef, useState } from 'react';
import { uploadFile } from '../../services/files';
import { logout } from '../../services/auth';
import { initSync } from '../../services/sync';

const TopBar = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const toast = useToast();

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
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } };
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
      const lastSync = localStorage.getItem('lastSyncTs') || '0';
      const result = await initSync(parseInt(lastSync));
      localStorage.setItem('lastSyncTs', Date.now().toString());
      
      toast({
        title: "Sync complete",
        description: result.changes ? "Changes detected and synced" : "Everything up to date",
        status: "success",
        duration: 3000,
      });

      if (result.changes) {
        window.location.reload();
      }
    } catch (error) {
      toast({
        title: "Sync failed",
        description: "Failed to sync files",
        status: "error",
        duration: 3000,
      });
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <Flex p={4} borderBottom="1px" borderColor="gray.200" align="center" justify="space-between" bg="white">
      {/* Left section - Main actions */}
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
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleUpload}
          multiple
        />
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
      </ButtonGroup>

      {/* Middle section - Search */}
      <Flex flex={1}>
        <Input
          placeholder="Search in Dropbox"
          size="md"
          maxW="600px"
          bg="gray.50"
          _placeholder={{ color: 'gray.500' }}
        />
      </Flex>

      {/* Right section - User actions */}
      <ButtonGroup>
        <Tooltip label="Logout">
          <IconButton
            aria-label="Logout"
            icon={<FaSignOutAlt />}
            variant="ghost"
            onClick={logout}
          />
        </Tooltip>
      </ButtonGroup>
    </Flex>
  );
};

export default TopBar; 