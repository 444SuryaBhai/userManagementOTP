import React, { useState } from 'react';
import OTPInput from '../components/OTPInput';
import { sendOTP, verifyOTP, oauthLogin } from '../services/auth';
import { useNavigate, Link } from 'react-router-dom';
import Loader from '../components/Loader';
import Alert from '../components/Alert';

const OAUTH_PROVIDERS = [
  { name: 'Google', id: 'google' },
  { name: 'GitHub', id: 'github' },
];

export default function Login() {
  const [method, setMethod] = useState('email');
  const [value, setValue] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState('');
  const [userId, setUserId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSendOTP = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const res = await sendOTP(method, value);
      setOtpSent(true);
      setUserId(res.user_id); // Store user_id from backend
      setSuccess('OTP sent!');
    } catch (err) {
      setError(err.message || 'Failed to send OTP');
    }
    setLoading(false);
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await verifyOTP(method, userId, otp); // Use userId for verification
      setSuccess('Login successful!');
      setTimeout(() => navigate('/profile'), 1000);
    } catch (err) {
      setError(err.message || 'Invalid OTP');
    }
    setLoading(false);
  };

  const handleOAuth = async (provider) => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      await oauthLogin(provider);
      setSuccess('OAuth login successful!');
      setTimeout(() => navigate('/profile'), 1000);
    } catch (err) {
      setError(err.message || 'OAuth login failed');
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 400, margin: '40px auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
      <h2>Login</h2>
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setMethod('email')} disabled={method === 'email'}>Email</button>
        <button onClick={() => setMethod('phone')} disabled={method === 'phone'} style={{ marginLeft: 8 }}>Phone</button>
      </div>
      <form onSubmit={otpSent ? handleVerifyOTP : handleSendOTP}>
        <input
          type={method === 'email' ? 'email' : 'tel'}
          placeholder={method === 'email' ? 'Enter your email' : 'Enter your phone'}
          value={value}
          onChange={e => setValue(e.target.value)}
          required
          style={{ width: '100%', marginBottom: 12, padding: 8 }}
          disabled={otpSent}
        />
        {otpSent && (
          <OTPInput value={otp} onChange={setOtp} />
        )}
        <button type="submit" style={{ width: '100%', marginTop: 12 }} disabled={loading}>
          {otpSent ? 'Verify OTP' : 'Send OTP'}
        </button>
      </form>
      <div style={{ margin: '16px 0', textAlign: 'center' }}>or</div>
      {OAUTH_PROVIDERS.map(p => (
        <button
          key={p.id}
          onClick={() => handleOAuth(p.id)}
          style={{ width: '100%', marginBottom: 8 }}
          disabled={loading}
        >
          Login with {p.name}
        </button>
      ))}
      {loading && <Loader />}
      <Alert type="error" message={error} />
      <Alert type="success" message={success} />
      <div style={{ marginTop: 16, textAlign: 'center' }}>
        <Link to="/register">Don't have an account? Register</Link>
      </div>
    </div>
  );
} 