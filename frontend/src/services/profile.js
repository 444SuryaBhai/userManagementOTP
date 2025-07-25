import { getToken, logout as clearToken } from './auth';

const API_BASE = 'http://localhost:8000'; // Adjust if needed

export async function getProfile() {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${API_BASE}/profile`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Not authenticated');
  return res.json();
}

export function logout() {
  clearToken();
} 