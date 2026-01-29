import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/Header';
import ItemList from './components/ItemList';
import ItemForm from './components/ItemForm';
import DeleteConfirm from './components/DeleteConfirm';
import LoginPage from './components/LoginPage';
import { api } from './services/api';
import './App.css';

function AppContent() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formOpen, setFormOpen] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [deleteItem, setDeleteItem] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch items when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      fetchItems();
    }
  }, [isAuthenticated]);

  const fetchItems = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await api.getItems();
      setItems(data);
    } catch (err) {
      setError('Failed to load items. Make sure the Django server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddClick = () => {
    setEditItem(null);
    setFormOpen(true);
  };

  const handleEditClick = (item) => {
    setEditItem(item);
    setFormOpen(true);
  };

  const handleFormSubmit = async (data, id) => {
    if (id) {
      // Update existing item
      const updated = await api.updateItem(id, data);
      setItems(items.map(item => item.id === id ? updated : item));
    } else {
      // Create new item
      const newItem = await api.createItem(data);
      setItems([...items, newItem]);
    }
  };

  const handleDeleteClick = (item) => {
    setDeleteItem(item);
  };

  const handleDeleteConfirm = async (id) => {
    setDeleteLoading(true);
    try {
      await api.deleteItem(id);
      setItems(items.filter(item => item.id !== id));
      setDeleteItem(null);
    } catch (err) {
      console.error(err);
    } finally {
      setDeleteLoading(false);
    }
  };

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="app loading-screen">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  // Show login if not authenticated
  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <div className="app">
      <Header onAddClick={handleAddClick} />

      <main className="main-content">
        {error && (
          <div className="error-banner">
            <p>{error}</p>
            <button onClick={fetchItems}>Retry</button>
          </div>
        )}

        <ItemList
          items={items}
          loading={loading}
          onEdit={handleEditClick}
          onDelete={handleDeleteClick}
        />
      </main>

      <ItemForm
        isOpen={formOpen}
        onClose={() => setFormOpen(false)}
        onSubmit={handleFormSubmit}
        editItem={editItem}
      />

      <DeleteConfirm
        isOpen={!!deleteItem}
        item={deleteItem}
        onClose={() => setDeleteItem(null)}
        onConfirm={handleDeleteConfirm}
        loading={deleteLoading}
      />

      <footer className="footer">
        <p>Powered by Django + React + Google Sheets</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
