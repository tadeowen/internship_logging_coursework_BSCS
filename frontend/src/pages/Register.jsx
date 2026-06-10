import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '', email: '', password: '', password2: '',
    first_name: '', last_name: '', role: 'student', phone: ''
  });
  const [error, setError] = useState('');

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (form.password !== form.password2) return setError('Passwords do not match');
    try {
      await api.post('/accounts/register/', form);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center" style={{ background: 'linear-gradient(135deg, #1a1f36 0%, #2d3561 100%)' }}>
      <div className="card shadow-lg border-0" style={{ borderRadius: '16px', width: '100%', maxWidth: '450px' }}>
        <div className="card-body p-4">
          <div className="text-center mb-4">
            <i className="fas fa-user-plus fa-2x text-primary mb-2"></i>
            <h4 className="fw-bold">Create Account</h4>
          </div>
          {error && <div className="alert alert-danger py-2">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="row g-2">
              <div className="col-md-6">
                <label className="form-label small">Username</label>
                <input className="form-control" value={form.username} onChange={update('username')} required />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Email</label>
                <input type="email" className="form-control" value={form.email} onChange={update('email')} required />
              </div>
            </div>
            <div className="row g-2 mt-2">
              <div className="col-md-6">
                <label className="form-label small">First Name</label>
                <input className="form-control" value={form.first_name} onChange={update('first_name')} />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Last Name</label>
                <input className="form-control" value={form.last_name} onChange={update('last_name')} />
              </div>
            </div>
            <div className="row g-2 mt-2">
              <div className="col-md-6">
                <label className="form-label small">Password</label>
                <input type="password" className="form-control" value={form.password} onChange={update('password')} required />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Confirm Password</label>
                <input type="password" className="form-control" value={form.password2} onChange={update('password2')} required />
              </div>
            </div>
            <div className="mt-2">
              <label className="form-label small">Role</label>
              <select className="form-select" value={form.role} onChange={update('role')}>
                <option value="student">Student</option>
                <option value="supervisor">Supervisor</option>
                <option value="lecturer">Lecturer</option>
              </select>
            </div>
            <div className="mt-2">
              <label className="form-label small">Phone</label>
              <input className="form-control" value={form.phone} onChange={update('phone')} />
            </div>
            <button type="submit" className="btn btn-primary w-100 mt-3 py-2">Register</button>
          </form>
          <div className="text-center mt-3 small text-muted">
            Already have an account? <a href="/login" className="text-decoration-none">Sign In</a>
          </div>
        </div>
      </div>
    </div>
  );
}
