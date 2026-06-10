import { useState, useEffect } from 'react';
import api from '../services/api';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [form, setForm] = useState({ username: '', email: '', first_name: '', last_name: '', role: 'student', phone: '', password: '' });

  const roleClass = (role) => {
    if (role === 'admin') return 'role-admin';
    if (role === 'supervisor') return 'role-supervisor';
    if (role === 'lecturer') return 'role-lecturer';
    return 'role-student';
  };

  const load = async () => {
    try {
      const res = await api.get('/accounts/users/');
      setUsers(res.data.results || res.data);
    } catch {
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { ...form };
    if (!data.password) delete data.password;
    if (editUser) {
      await api.put(`/accounts/users/${editUser.id}/`, data);
      setEditUser(null);
    } else {
      await api.post('/accounts/users/', data);
    }
    setShowForm(false);
    setForm({ username: '', email: '', first_name: '', last_name: '', role: 'student', phone: '', password: '' });
    load();
  };

  const startEdit = (u) => {
    setEditUser(u);
    setForm({ username: u.username, email: u.email, first_name: u.first_name || '', last_name: u.last_name || '', role: u.role, phone: u.phone || '', password: '' });
    setShowForm(true);
  };

  const deleteUser = async (id) => {
    if (!confirm('Delete this user?')) return;
    await api.delete(`/accounts/users/${id}/`);
    load();
  };

  const cancelForm = () => {
    setShowForm(false);
    setEditUser(null);
    setForm({ username: '', email: '', first_name: '', last_name: '', role: 'student', phone: '', password: '' });
  };

  if (loading) return <div className="text-center py-5 text-muted">Loading users...</div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="page-title mb-0">Users</h2>
        <button className="btn btn-primary" onClick={() => { cancelForm(); setShowForm(!showForm); }}>
          <i className={`fas ${showForm ? 'fa-times' : 'fa-plus'} me-1`}></i>
          {showForm ? 'Cancel' : 'Add User'}
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleSubmit} className="card border-0 shadow-sm mb-3">
          <div className="card-body">
            <h5 className="fw-semibold mb-3">{editUser ? 'Edit User' : 'New User'}</h5>
            <div className="row g-2">
              <div className="col-md-6">
                <label className="form-label small">Username</label>
                <input className="form-control" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} required />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Email</label>
                <input type="email" className="form-control" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
              </div>
              <div className="col-md-6">
                <label className="form-label small">First Name</label>
                <input className="form-control" value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Last Name</label>
                <input className="form-control" value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Role</label>
                <select className="form-select" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
                  <option value="student">Student</option>
                  <option value="supervisor">Supervisor</option>
                  <option value="lecturer">Lecturer</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div className="col-md-6">
                <label className="form-label small">Phone</label>
                <input className="form-control" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
              </div>
              {!editUser && (
                <div className="col-12">
                  <label className="form-label small">Password {editUser ? '(leave blank to keep)' : '(required)'}</label>
                  <input type="password" className="form-control" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required={!editUser} />
                </div>
              )}
            </div>
            <div className="mt-3">
              <button type="submit" className="btn btn-primary">{editUser ? 'Update' : 'Create'} User</button>
            </div>
          </div>
        </form>
      )}
      <div className="card border-0 shadow-sm">
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-hover mb-0">
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td className="fw-semibold">{u.username}</td>
                    <td>{u.first_name} {u.last_name}</td>
                    <td>{u.email}</td>
                    <td><span className={`role-pill ${roleClass(u.role)}`}>{u.role}</span></td>
                    <td>
                      <button className="btn btn-sm btn-outline-primary me-1" onClick={() => startEdit(u)}>
                        <i className="fas fa-edit"></i>
                      </button>
                      <button className="btn btn-sm btn-outline-danger" onClick={() => deleteUser(u.id)}>
                        <i className="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
                {users.length === 0 && <tr><td colSpan="5" className="text-center py-4 text-muted">No users</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
