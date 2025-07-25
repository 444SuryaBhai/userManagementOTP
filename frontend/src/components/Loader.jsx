import React from 'react';

export default function Loader() {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 80 }}>
      <div className="loader" style={{ width: 32, height: 32, border: '4px solid #eee', borderTop: '4px solid #333', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
} 