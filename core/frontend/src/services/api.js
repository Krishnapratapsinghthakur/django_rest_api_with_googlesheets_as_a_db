// API Service for Google Sheets Backend with Authentication
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Helper to get auth headers
const getAuthHeaders = () => {
    const token = localStorage.getItem('accessToken');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
};

// Helper to refresh token
const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        throw new Error('No refresh token available');
    }

    const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
        // Clear tokens if refresh fails
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('username');
        window.location.reload();
        throw new Error('Session expired. Please login again.');
    }

    const data = await response.json();
    localStorage.setItem('accessToken', data.access);
    return data.access;
};

// Helper to make authenticated requests with auto-refresh
const authFetch = async (url, options = {}) => {
    const headers = {
        ...options.headers,
        ...getAuthHeaders(),
    };

    let response = await fetch(url, { ...options, headers });

    // If unauthorized, try to refresh token
    if (response.status === 401) {
        try {
            await refreshAccessToken();
            // Retry with new token
            const newHeaders = {
                ...options.headers,
                ...getAuthHeaders(),
            };
            response = await fetch(url, { ...options, headers: newHeaders });
        } catch (err) {
            throw new Error('Session expired. Please login again.');
        }
    }

    return response;
};

export const api = {
    // Login - obtain JWT tokens
    async login(username, password) {
        const response = await fetch(`${API_BASE_URL}/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Invalid credentials');
        }

        return response.json();
    },

    // Get all items
    async getItems() {
        const response = await authFetch(`${API_BASE_URL}/sheet-items/`);
        if (!response.ok) {
            throw new Error('Failed to fetch items');
        }
        return response.json();
    },

    // Get single item by ID
    async getItem(id) {
        const response = await authFetch(`${API_BASE_URL}/sheet-items/${id}/`);
        if (!response.ok) {
            throw new Error('Item not found');
        }
        return response.json();
    },

    // Create new item
    async createItem(data) {
        const response = await authFetch(`${API_BASE_URL}/sheet-items/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create item');
        }
        return response.json();
    },

    // Update item
    async updateItem(id, data) {
        const response = await authFetch(`${API_BASE_URL}/sheet-items/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update item');
        }
        return response.json();
    },

    // Delete item
    async deleteItem(id) {
        const response = await authFetch(`${API_BASE_URL}/sheet-items/${id}/`, {
            method: 'DELETE',
        });
        if (!response.ok && response.status !== 204) {
            throw new Error('Failed to delete item');
        }
        return true;
    },
};
