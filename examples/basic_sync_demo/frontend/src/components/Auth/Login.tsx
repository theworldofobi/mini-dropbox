import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Input, VStack, HStack, Text, useToast } from '@chakra-ui/react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { login: setAuth } = useAuth();
  const toast = useToast();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const response = await api.post('/auth/login', {
        username,
        password
      });
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      setAuth(token);
      navigate('/');
    } catch (error: any) {
      toast({
        title: 'Login failed',
        description: error.response?.data?.detail || 'Invalid username or password',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const handleGuestAccess = async () => {
    try {
      const response = await api.post('/auth/guest-login');
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      setAuth(token);
      navigate('/');
    } catch (error: any) {
      toast({
        title: 'Guest access failed',
        description: error.response?.data?.detail || 'Unable to access as guest',
        status: 'error',
        duration: 3000,
      });
    }
  };

  return (
    <Box p={8} maxW="400px" mx="auto" mt={16}>
      <form onSubmit={handleLogin}>
        <VStack spacing={4}>
          <Text fontSize="2xl" fontWeight="bold">Welcome to Dropbox-lite</Text>
          <Input
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" colorScheme="blue" width="100%">
            Login
          </Button>
          <HStack width="100%" spacing={4}>
            <Button variant="outline" width="50%" onClick={() => navigate('/signup')}>
              Sign Up
            </Button>
            <Button variant="ghost" width="50%" onClick={handleGuestAccess}>
              Continue as Guest
            </Button>
          </HStack>
        </VStack>
      </form>
    </Box>
  );
};

export default Login; 