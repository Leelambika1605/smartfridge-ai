import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('smartfridge_token'));
  const [loading, setLoading] = useState(true);

  // Load user profile on initial render if token exists
  useEffect(() => {
    const fetchUser = async () => {
      const storedToken = localStorage.getItem('smartfridge_token');
      if (storedToken) {
        try {
          const profile = await authService.getProfile();
          setUser(profile);
        } catch (error) {
          console.error("Failed to restore session:", error);
          logout();
        }
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    localStorage.setItem('smartfridge_token', data.token);
    setToken(data.token);
    setUser(data.user);
    return data;
  };

  const register = async (email, fullName, password) => {
    const data = await authService.register(email, fullName, password);
    localStorage.setItem('smartfridge_token', data.token);
    setToken(data.token);
    setUser(data.user);
    return data;
  };

  const logout = () => {
    localStorage.removeItem('smartfridge_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        loading,
        login,
        register,
        logout,
        activeFridge: user?.refrigerators?.[0] || null,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
