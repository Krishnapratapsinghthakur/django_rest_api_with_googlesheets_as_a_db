// API Service for Google Sheets Backend
const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const api = {
    // Get all items
    async getItems() {
        const response = await fetch(`${API_BASE_URL}/sheet-items/`);
        if (!response.ok) {
            throw new Error('Failed to fetch items');
        }
        return response.json();
    },

    // Get single item by ID
    async getItem(id) {
        const response = await fetch(`${API_BASE_URL}/sheet-items/${id}/`);
        if (!response.ok) {
            throw new Error('Item not found');
        }
        return response.json();
    },

    // Create new item
    async createItem(data) {
        const response = await fetch(`${API_BASE_URL}/sheet-items/`, {
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
        const response = await fetch(`${API_BASE_URL}/sheet-items/${id}/`, {
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
        const response = await fetch(`${API_BASE_URL}/sheet-items/${id}/`, {
            method: 'DELETE',
        });
        if (!response.ok && response.status !== 204) {
            throw new Error('Failed to delete item');
        }
        return true;
    },
};
