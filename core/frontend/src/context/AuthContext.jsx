import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for existing tokens on mount
        const accessToken = localStorage.getItem('accessToken');
        const username = localStorage.getItem('username');
        if (accessToken && username) {
            setUser({ username });
        }
        setLoading(false);
    }, []);

    const login = (username, accessToken, refreshToken) => {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
        localStorage.setItem('username', username);
        setUser({ username });
    };

    const logout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('username');
        setUser(null);
    };

    const getAccessToken = () => localStorage.getItem('accessToken');
    const getRefreshToken = () => localStorage.getItem('refreshToken');

    const isAuthenticated = !!user;

    const value = {
        user,
        login,
        logout,
        isAuthenticated,
        loading,
        getAccessToken,
        getRefreshToken,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;
