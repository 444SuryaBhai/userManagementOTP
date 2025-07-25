import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div style={{ textAlign: 'center', marginTop: 80 }}>
      <h1>Welcome to User Management App</h1>
      <p>
        <Link to="/">Login</Link> | <Link to="/register">Register</Link>
      </p>
    </div>
  );
} 