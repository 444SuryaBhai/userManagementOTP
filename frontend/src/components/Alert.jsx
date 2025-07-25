import React from 'react';

export default function Alert({ type = 'error', message }) {
  if (!message) return null;
  return (
    <div style={{
      background: type === 'error' ? '#ffe5e5' : '#e5ffe5',
      color: type === 'error' ? '#b00' : '#080',
      padding: 12,
      borderRadius: 6,
      margin: '12px 0',
      textAlign: 'center',
      border: `1px solid ${type === 'error' ? '#fbb' : '#bfb'}`
    }}>
      {message}
    </div>
  );
} 