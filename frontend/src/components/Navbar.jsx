import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  const token = localStorage.getItem('token');
  return (
    <nav style={{ display: 'flex', gap: 16, padding: 16, borderBottom: '1px solid #eee', marginBottom: 24 }}>
      <Link to="/">Login</Link>
      <Link to="/register">Register</Link>
      {token && <Link to="/profile">Profile</Link>}
    </nav>
  );
} 