import { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Logs() {
  const { user } = useAuth();
  const [logs, setLogs] = useState([]);
  const [form, setForm] = useState({ date: new Date().toISOString().slice(0, 10), activities: '', skills_learned: '', challenges: '', hours_worked: 8 });
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const res = await api.get('/logbook/logs/');
      setLogs(res.data.results || res.data);
    } catch {
      setLogs([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/logbook/logs/', form);
    setShowForm(false);
    setForm({ date: new Date().toISOString().slice(0, 10), activities: '', skills_learned: '', challenges: '', hours_worked: 8 });
    load();
  };

  const handleStatus = async (id, status) => {
    await api.patch(`/logbook/logs/${id}/`, { status });
    load();
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this log?')) return;
    await api.delete(`/logbook/logs/${id}/`);
    load();
  };

  if (loading) return <div className="text-center py-5 text-muted">Loading logs...</div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="page-title mb-0">Daily Logs</h2>
        {user?.role === 'student' && (
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            <i className={`fas ${showForm ? 'fa-times' : 'fa-plus'} me-1`}></i>
            {showForm ? 'Cancel' : 'New Log'}
          </button>
        )}
      </div>
      {showForm && (
        <form onSubmit={handleSubmit} className="card border-0 shadow-sm mb-3">
          <div className="card-body">
            <h5 className="fw-semibold mb-3">Submit Daily Log</h5>
            <div className="row g-2">
              <div className="col-md-3">
                <label className="form-label small">Date</label>
                <input type="date" className="form-control" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required />
              </div>
              <div className="col-md-3">
                <label className="form-label small">Hours Worked</label>
                <input type="number" step="0.1" className="form-control" value={form.hours_worked} onChange={(e) => setForm({ ...form, hours_worked: e.target.value })} required />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Activities</label>
                <input className="form-control" value={form.activities} onChange={(e) => setForm({ ...form, activities: e.target.value })} required />
              </div>
            </div>
            <div className="row g-2 mt-2">
              <div className="col-md-6">
                <label className="form-label small">Skills Learned</label>
                <input className="form-control" value={form.skills_learned} onChange={(e) => setForm({ ...form, skills_learned: e.target.value })} />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Challenges</label>
                <input className="form-control" value={form.challenges} onChange={(e) => setForm({ ...form, challenges: e.target.value })} />
              </div>
            </div>
            <div className="mt-3">
              <button type="submit" className="btn btn-primary">Submit Log</button>
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
                  <th>Date</th>
                  <th>Activities</th>
                  <th>Hours</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td>{log.date}</td>
                    <td>{log.activities?.slice(0, 50)}{log.activities?.length > 50 ? '...' : ''}</td>
                    <td>{log.hours_worked}</td>
                    <td>
                      <span className={`badge bg-${log.status === 'approved' ? 'success' : log.status === 'rejected' ? 'danger' : 'warning'}`}>
                        {log.status}
                      </span>
                    </td>
                    <td>
                      {(user?.role === 'supervisor' || user?.role === 'admin') && log.status === 'pending' && (
                        <div className="btn-group btn-group-sm">
                          <button className="btn btn-success" onClick={() => handleStatus(log.id, 'approved')}>
                            <i className="fas fa-check"></i>
                          </button>
                          <button className="btn btn-danger" onClick={() => handleStatus(log.id, 'rejected')}>
                            <i className="fas fa-times"></i>
                          </button>
                        </div>
                      )}
                      {(user?.role === 'admin' || user?.role === 'student') && (
                        <button className="btn btn-outline-danger btn-sm" onClick={() => handleDelete(log.id)}>
                          <i className="fas fa-trash"></i>
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
                {logs.length === 0 && <tr><td colSpan="5" className="text-center py-4 text-muted">No logs found</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
