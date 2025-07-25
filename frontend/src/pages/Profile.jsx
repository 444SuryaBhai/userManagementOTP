import React, { useEffect, useState } from 'react';
import { getProfile, logout } from '../services/profile';
import { useNavigate } from 'react-router-dom';
import Loader from '../components/Loader';
import Alert from '../components/Alert';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    getProfile()
      .then(setUser)
      .catch(err => {
        setError('Not authenticated');
        setTimeout(() => navigate('/'), 1000);
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  if (loading) return <Loader />;
  if (error) return <Alert type="error" message={error} />;
  if (!user) return null;

  return (
    <div style={{ maxWidth: 400, margin: '40px auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Profile</h2>
      <img src={user.profile_picture} alt="Profile" style={{ width: 80, height: 80, borderRadius: '50%', marginBottom: 16 }} />
      <div><b>Name:</b> {user.name}</div>
      <div><b>Email:</b> {user.email}</div>
      <div><b>Phone:</b> {user.phone}</div>
      <button onClick={handleLogout} style={{ marginTop: 24, width: '100%' }}>Logout</button>
    </div>
  );
} 