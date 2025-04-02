import { VStack, Button, Text, Box } from '@chakra-ui/react';
import { FaHome, FaFile, FaStar, FaImage, FaShare, FaTrash } from 'react-icons/fa';

const Sidebar = () => {
  const menuItems = [
    { icon: FaHome, label: 'Home', path: '/' },
    { icon: FaFile, label: 'All files', path: '/files' },
    { icon: FaStar, label: 'Starred', path: '/starred' },
    { icon: FaImage, label: 'Photos', path: '/photos' },
    { icon: FaShare, label: 'Shared', path: '/shared' },
    { icon: FaTrash, label: 'Deleted files', path: '/trash' }
  ];

  return (
    <Box p={4}>
      <VStack spacing={2} align="stretch">
        {menuItems.map((item) => (
          <Button
            key={item.path}
            leftIcon={<item.icon />}
            variant="ghost"
            justifyContent="flex-start"
            w="100%"
            py={6}
          >
            <Text>{item.label}</Text>
          </Button>
        ))}
      </VStack>
    </Box>
  );
};

export default Sidebar; 