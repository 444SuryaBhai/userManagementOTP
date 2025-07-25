const API_BASE = 'http://localhost:8000';

export async function registerUser({ name, email, phone }) {
  const res = await fetch(`${API_BASE}/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, phone })
  });
  if (!res.ok) throw new Error('Registration failed');
  return res.json();
}

export async function verifyRegisterOTP(user_id, otp) {
  const res = await fetch(`${API_BASE}/register/otp/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, otp, type: 'email' }) // or 'phone' if needed
  });
  if (!res.ok) throw new Error('OTP verification failed');
  return res.json();
} 