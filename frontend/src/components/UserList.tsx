/**
 * UserList component - displays a list of users from the API
 */
import { useState, useEffect } from 'react';
import { userApi } from '@/services/api';
import type { User } from '@/models/user';

export default function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await userApi.getAll();
      setUsers(data);
    } catch (err) {
      setError('Failed to load users. Make sure the backend is running.');
      console.error('Error loading users:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading users...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={loadUsers}>Retry</button>
      </div>
    );
  }

  return (
    <div className="user-list">
      <h2>Users</h2>
      <div className="list-container">
        {users.length === 0 ? (
          <p>No users found.</p>
        ) : (
          <div className="grid">
            {users.map((user) => (
              <div key={user.id} className="card">
                <div className="card-header">
                  <h3>{user.name}</h3>
                  <span className={`badge ${user.role}`}>{user.role}</span>
                </div>
                <div className="card-body">
                  <p className="email">{user.email}</p>
                  <p className="meta">
                    <span className={`status ${user.is_active ? 'active' : 'inactive'}`}>
                      {user.is_active ? '● Active' : '○ Inactive'}
                    </span>
                    <span className="date">
                      Joined: {new Date(user.created_at).toLocaleDateString()}
                    </span>
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

