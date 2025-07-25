import React, { useRef } from 'react';

export default function OTPInput({ value, onChange }) {
  const inputs = useRef([]);

  const handleChange = (e, idx) => {
    const val = e.target.value.replace(/\D/g, '');
    let otpArr = value.split('');
    otpArr[idx] = val;
    const otp = otpArr.join('').slice(0, 6);
    onChange(otp);
    if (val && idx < 5) {
      inputs.current[idx + 1].focus();
    }
  };

  const handleKeyDown = (e, idx) => {
    if (e.key === 'Backspace' && !value[idx] && idx > 0) {
      inputs.current[idx - 1].focus();
    }
  };

  const handlePaste = (e) => {
    const paste = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    onChange(paste);
    if (paste.length === 6) {
      inputs.current[5].focus();
    }
  };

  return (
    <div style={{ display: 'flex', gap: 8, justifyContent: 'center', marginBottom: 12 }}>
      {[...Array(6)].map((_, idx) => (
        <input
          key={idx}
          ref={el => inputs.current[idx] = el}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={value[idx] || ''}
          onChange={e => handleChange(e, idx)}
          onKeyDown={e => handleKeyDown(e, idx)}
          onPaste={handlePaste}
          style={{ width: 36, height: 36, textAlign: 'center', fontSize: 18 }}
        />
      ))}
    </div>
  );
} 