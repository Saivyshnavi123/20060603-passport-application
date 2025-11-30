// Authentication service using generic API
import api from './api';

const authService = {
  // Login
  login: async (credentials) => {
    const response = await api.post('/login', credentials);
    
    // API returns: {message, role, user_id}
    if (response.role && response.user_id) {
      // Create user object from response
      const user = {
        username: credentials.username,  // Use the username from login form
        role: response.role,
        user_id: response.user_id
      };
      
      localStorage.setItem('user', JSON.stringify(user));
      localStorage.setItem('username', credentials.username);
      localStorage.setItem('role', response.role);
      localStorage.setItem('user_id', response.user_id.toString());
    }
    
    return response;
  },

  // Register
  register: async (userData) => {
    const response = await api.post('/register', userData);
    // Registration only returns a message, no user data stored
    // User will login after registration
    return response;
  },

  // Logout
  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    localStorage.removeItem('user_id');
  },
};

export default authService;
