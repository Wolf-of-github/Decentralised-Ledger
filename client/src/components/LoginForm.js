import React, { useState } from 'react';

const LoginForm = ({ selectedNode, setToken, setRole, setPatientId }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${selectedNode}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        setToken(data.token);

        const payload = JSON.parse(atob(data.token.split('.')[1]));
        setRole(payload.role);
        if (payload.role === 'patient') {
          setPatientId(payload.patient_id);
        }

        alert('Login successful!');
      } else {
        alert(data.error || 'Login failed.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login error.');
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="card shadow" style={{ width: '500px', padding: '30px' }}>
        <div className="card-body">
          <h2 className="card-title mb-4 text-center fw-bold" style={{ fontSize: '2rem' }}>
            Login
          </h2>
          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <input
                type="text"
                className="form-control form-control-lg"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="mb-4">
              <input
                type="password"
                className="form-control form-control-lg"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="d-grid">
              <button type="submit" className="btn btn-primary btn-lg">
                Log In
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;