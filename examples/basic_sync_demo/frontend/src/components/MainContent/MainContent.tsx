import { Box } from '@chakra-ui/react';
import FileList from '../FileList/FileList';

const MainContent = () => {
  return (
    <Box flex="1" p={4} bg="gray.50" overflowY="auto">
      <FileList />
    </Box>
  );
};

export default MainContent; 