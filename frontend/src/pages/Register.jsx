import React, { useState } from 'react';
import { registerUser, verifyRegisterOTP } from '../services/register';
import { useNavigate } from 'react-router-dom';
import Loader from '../components/Loader';
import Alert from '../components/Alert';

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', phone: '' });
  const [userId, setUserId] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState('register');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const res = await registerUser(form);
      setUserId(res.user_id);
      setStep('otp');
      setSuccess(res.message || 'Registration successful. OTP sent.');
    } catch (err) {
      setError(err.message || 'Registration failed');
    }
    setLoading(false);
  };

  const handleVerifyOTP = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await verifyRegisterOTP(userId, otp);
      setSuccess('OTP verified! You can now login.');
      setTimeout(() => navigate('/'), 1500);
    } catch (err) {
      setError(err.message || 'OTP verification failed');
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 400, margin: '40px auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Register</h2>
      {step === 'register' && (
        <form onSubmit={handleRegister}>
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required style={{ width: '100%', marginBottom: 12, padding: 8 }} />
          <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required style={{ width: '100%', marginBottom: 12, padding: 8 }} />
          <input name="phone" type="tel" placeholder="Phone" value={form.phone} onChange={handleChange} required style={{ width: '100%', marginBottom: 12, padding: 8 }} />
          <button type="submit" style={{ width: '100%', marginTop: 12 }} disabled={loading}>Register</button>
        </form>
      )}
      {step === 'otp' && (
        <form onSubmit={handleVerifyOTP}>
          <input value={otp} onChange={e => setOtp(e.target.value)} placeholder="Enter OTP" required style={{ width: '100%', marginBottom: 12, padding: 8 }} />
          <button type="submit" style={{ width: '100%', marginTop: 12 }} disabled={loading}>Verify OTP</button>
        </form>
      )}
      {loading && <Loader />}
      <Alert type="error" message={error} />
      <Alert type="success" message={success} />
      <div style={{ marginTop: 16 }}>
        <button onClick={() => navigate('/')} style={{ width: '100%' }}>Back to Login</button>
      </div>
    </div>
  );
} 