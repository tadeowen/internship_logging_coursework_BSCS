import { useState, useEffect } from 'react';
import api from '../services/api';

export default function Evaluations() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ student: '', punctuality: 20, technical_skills: 30, communication: 20, initiative: 15, teamwork: 15, comments: '' });

  const load = async () => {
    try {
      const res = await api.get('/evaluation/evaluations/');
      setItems(res.data.results || res.data);
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/evaluation/evaluations/', form);
    setShowForm(false);
    setForm({ student: '', punctuality: 20, technical_skills: 30, communication: 20, initiative: 15, teamwork: 15, comments: '' });
    load();
  };

  const grade = (total) => {
    if (total >= 80) return 'Excellent';
    if (total >= 65) return 'Very Good';
    if (total >= 50) return 'Good';
    return 'Needs Support';
  };

  if (loading) return <div className="text-center py-5 text-muted">Loading evaluations...</div>;

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="page-title mb-0">Evaluations</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <i className={`fas ${showForm ? 'fa-times' : 'fa-plus'} me-1`}></i>
          {showForm ? 'Cancel' : 'New Evaluation'}
        </button>
      </div>
      {showForm && (
        <form onSubmit={handleSubmit} className="card border-0 shadow-sm mb-3">
          <div className="card-body">
            <h5 className="fw-semibold mb-3">New Evaluation</h5>
            <div className="row g-2">
              <div className="col-12">
                <label className="form-label small">Student Username</label>
                <input className="form-control" value={form.student} onChange={(e) => setForm({ ...form, student: e.target.value })} required />
              </div>
              {[
                ['punctuality', 'Punctuality /20'],
                ['technical_skills', 'Technical Skills /30'],
                ['communication', 'Communication /20'],
                ['initiative', 'Initiative /15'],
                ['teamwork', 'Teamwork /15'],
              ].map(([field, label]) => (
                <div className="col-md-4" key={field}>
                  <label className="form-label small">{label}</label>
                  <input type="number" className="form-control" value={form[field]} onChange={(e) => setForm({ ...form, [field]: e.target.value })} required />
                </div>
              ))}
            </div>
            <div className="mt-2">
              <label className="form-label small">Comments</label>
              <textarea className="form-control" rows="3" value={form.comments} onChange={(e) => setForm({ ...form, comments: e.target.value })}></textarea>
            </div>
            <button type="submit" className="btn btn-primary mt-3">Submit Evaluation</button>
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
                  <th>Evaluator</th>
                  <th>Scores</th>
                  <th>Total</th>
                  <th>Grade</th>
                </tr>
              </thead>
              <tbody>
                {items.map((ev) => {
                  const total = ev.total_score || (ev.punctuality + ev.technical_skills + ev.communication + ev.initiative + ev.teamwork);
                  return (
                    <tr key={ev.id}>
                      <td>{ev.student_details?.username || ev.student}</td>
                      <td>{ev.evaluator_details?.username || ev.evaluator}</td>
                      <td className="small">
                        P:{ev.punctuality} T:{ev.technical_skills} C:{ev.communication} I:{ev.initiative} W:{ev.teamwork}
                      </td>
                      <td className="fw-bold">{total}</td>
                      <td><span className={`badge bg-${total >= 65 ? 'success' : total >= 50 ? 'warning' : 'danger'}`}>{grade(total)}</span></td>
                    </tr>
                  );
                })}
                {items.length === 0 && <tr><td colSpan="5" className="text-center py-4 text-muted">No evaluations</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
