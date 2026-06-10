import { useState, useEffect } from 'react';
import api from '../services/api';

export default function Placements() {
  const [placements, setPlacements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ student: '', company_name: '', company_address: '', start_date: '', end_date: '', status: 'active' });

  const load = async () => {
    try {
      const res = await api.get('/accounts/placements/');
      setPlacements(res.data.results || res.data);
    } catch {
      setPlacements([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/accounts/placements/', form);
    setShowForm(false);
    setForm({ student: '', company_name: '', company_address: '', start_date: '', end_date: '', status: 'active' });
    load();
  };

  if (loading) return <div className="text-center py-5 text-muted">Loading placements...</div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="page-title mb-0">Internship Placements</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <i className={`fas ${showForm ? 'fa-times' : 'fa-plus'} me-1`}></i>
          {showForm ? 'Cancel' : 'New Placement'}
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleSubmit} className="card border-0 shadow-sm mb-3">
          <div className="card-body">
            <h5 className="fw-semibold mb-3">New Placement</h5>
            <div className="row g-2">
              <div className="col-md-6">
                <label className="form-label small">Student Username</label>
                <input className="form-control" value={form.student} onChange={(e) => setForm({ ...form, student: e.target.value })} required />
              </div>
              <div className="col-md-6">
                <label className="form-label small">Company Name</label>
                <input className="form-control" value={form.company_name} onChange={(e) => setForm({ ...form, company_name: e.target.value })} required />
              </div>
              <div className="col-12">
                <label className="form-label small">Company Address</label>
                <input className="form-control" value={form.company_address} onChange={(e) => setForm({ ...form, company_address: e.target.value })} />
              </div>
              <div className="col-md-4">
                <label className="form-label small">Start Date</label>
                <input type="date" className="form-control" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} required />
              </div>
              <div className="col-md-4">
                <label className="form-label small">End Date</label>
                <input type="date" className="form-control" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} required />
              </div>
              <div className="col-md-4">
                <label className="form-label small">Status</label>
                <select className="form-select" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                  <option value="active">Active</option>
                  <option value="planned">Planned</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
            </div>
            <div className="mt-3">
              <button type="submit" className="btn btn-primary">Create Placement</button>
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
                  <th>Student</th>
                  <th>Company</th>
                  <th>Address</th>
                  <th>Period</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {placements.map((p) => (
                  <tr key={p.id}>
                    <td className="fw-semibold">{p.student_details?.username || p.student}</td>
                    <td>{p.company_details?.name || p.company_name || p.company}</td>
                    <td>{p.company_details?.address || p.company_address || '-'}</td>
                    <td>{p.start_date} → {p.end_date}</td>
                    <td>
                      <span className={`badge bg-${p.status === 'active' ? 'success' : p.status === 'planned' ? 'info' : 'secondary'}`}>
                        {p.status}
                      </span>
                    </td>
                  </tr>
                ))}
                {placements.length === 0 && <tr><td colSpan="5" className="text-center py-4 text-muted">No placements</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
