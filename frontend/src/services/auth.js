const API_BASE = 'http://localhost:8000'; // Adjust if needed

export async function sendOTP(method, value) {
  let url, body;
  if (method === 'email') {
    url = `${API_BASE}/login/email-otp/request`;
    body = JSON.stringify({ email: value });
  } else {
    url = `${API_BASE}/login/phone-otp/request`;
    body = JSON.stringify({ phone: value });
  }
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body
  });
  if (!res.ok) throw new Error('Failed to send OTP');
  return res.json();
}

export async function verifyOTP(method, user_id, otp) {
  let url, body;
  if (method === 'email') {
    url = `${API_BASE}/login/email-otp/verify`;
    body = JSON.stringify({ user_id, otp, type: 'email' });
  } else {
    url = `${API_BASE}/login/phone-otp/verify`;
    body = JSON.stringify({ user_id, otp, type: 'phone' });
  }
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body
  });
  if (!res.ok) throw new Error('Invalid OTP');
  const data = await res.json();
  if (data.access_token) localStorage.setItem('token', data.access_token);
  return data;
}

export async function oauthLogin(provider) {
  window.location.href = `${API_BASE}/login/oauth/${provider}`;
}

export function getToken() {
  return localStorage.getItem('token');
}

export function logout() {
  localStorage.removeItem('token');
} 