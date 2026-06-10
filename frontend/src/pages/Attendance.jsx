import { useState, useEffect } from 'react';
import api from '../services/api';

export default function Attendance() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/logbook/attendance/')
      .then((res) => setRecords(res.data.results || res.data))
      .catch(() => setRecords([]))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-5 text-muted">Loading attendance...</div>;

  return (
    <div>
      <h2 className="page-title">Attendance Records</h2>
      <div className="card border-0 shadow-sm">
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-hover mb-0">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Check In</th>
                  <th>Check Out</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.id}>
                    <td>{r.student_details?.username || r.student}</td>
                    <td>{r.date}</td>
                    <td>
                      <span className={`badge bg-${r.status === 'present' ? 'success' : r.status === 'late' ? 'warning' : r.status === 'absent' ? 'danger' : 'secondary'}`}>
                        {r.status}
                      </span>
                    </td>
                    <td>{r.check_in || '-'}</td>
                    <td>{r.check_out || '-'}</td>
                  </tr>
                ))}
                {records.length === 0 && <tr><td colSpan="5" className="text-center py-4 text-muted">No attendance records</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
