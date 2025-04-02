import { Flex, Box } from '@chakra-ui/react';
import Sidebar from '../Sidebar/Sidebar';
import TopBar from '../TopBar/TopBar';
import MainContent from '../MainContent/MainContent';

const MainLayout = () => {
  return (
    <Flex h="100vh">
      <Box w="240px" borderRight="1px" borderColor="gray.200">
        <Sidebar />
      </Box>
      <Flex direction="column" flex="1">
        <TopBar />
        <MainContent />
      </Flex>
    </Flex>
  );
};

export default MainLayout; 