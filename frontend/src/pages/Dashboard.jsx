import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({ logs: 0, attendance: 0, evaluations: 0, placements: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [
          logsRes,
          attRes,
          evalRes,
          placeRes,
        ] = await Promise.all([
          api.get('/logbook/logs/'),
          api.get('/logbook/attendance/'),
          api.get('/evaluation/evaluations/'),
          api.get('/accounts/placements/'),
        ]);
        setStats({
          logs: logsRes.data?.count || logsRes.data?.length || 0,
          attendance: attRes.data?.count || attRes.data?.length || 0,
          evaluations: evalRes.data?.count || evalRes.data?.length || 0,
          placements: placeRes.data?.count || placeRes.data?.length || 0,
        });
      } catch {
        setStats({ logs: 0, attendance: 0, evaluations: 0, placements: 0 });
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const statCards = [
    { label: 'Log Entries', value: stats.logs, icon: 'fa-book-open', color: 'primary', to: '/logs' },
    { label: 'Attendance', value: stats.attendance, icon: 'fa-calendar-check', color: 'success', to: '/attendance' },
    { label: 'Evaluations', value: stats.evaluations, icon: 'fa-star', color: 'warning', to: '/evaluations' },
    { label: 'Placements', value: stats.placements, icon: 'fa-building', color: 'info', to: '/placements' },
  ];

  return (
    <div>
      <h2 className="page-title">Welcome back, {user?.first_name || user?.username}! 👋</h2>
      {loading ? (
        <div className="text-center py-5 text-muted">Loading dashboard...</div>
      ) : (
        <>
          <div className="row g-3 mb-4">
            {statCards.map((card) => (
              <div className="col-md-6 col-xl-3" key={card.label}>
                <Link to={card.to} className="text-decoration-none">
                  <div className="card card-stat h-100">
                    <div className="card-body d-flex align-items-center justify-content-between">
                      <div>
                        <div className="text-muted small fw-semibold text-uppercase">{card.label}</div>
                        <div className="h3 mb-0 fw-bold">{card.value}</div>
                      </div>
                      <div className={`bg-${card.color} bg-opacity-10 rounded-circle p-3`}>
                        <i className={`fas ${card.icon} text-${card.color} fa-lg`}></i>
                      </div>
                    </div>
                  </div>
                </Link>
              </div>
            ))}
          </div>
          <div className="row g-3">
            <div className="col-md-7">
              <div className="card border-0 shadow-sm">
                <div className="card-header bg-white border-0 fw-semibold">Quick Actions</div>
                <div className="card-body">
                  <div className="d-grid gap-2">
                    <Link to="/logs" className="btn btn-outline-primary text-start">
                      <i className="fas fa-plus-circle me-2"></i> Submit Daily Log
                    </Link>
                    <Link to="/attendance" className="btn btn-outline-success text-start">
                      <i className="fas fa-clock me-2"></i> Update Attendance
                    </Link>
                    {['supervisor', 'lecturer'].includes(user?.role) && (
                      <Link to="/evaluations" className="btn btn-outline-warning text-start">
                        <i className="fas fa-clipboard-check me-2"></i> Evaluate Student
                      </Link>
                    )}
                  </div>
                </div>
              </div>
            </div>
            <div className="col-md-5">
              <div className="card border-0 shadow-sm">
                <div className="card-header bg-white border-0 fw-semibold">Your Role</div>
                <div className="card-body text-center">
                  <span className={`role-pill role-${user?.role} fs-5`}>{user?.role}</span>
                  <div className="mt-3 text-muted small">
                    {user?.role === 'student' && 'Submit logs, attendance and reports.'}
                    {user?.role === 'supervisor' && 'Review student logs and attendance.'}
                    {user?.role === 'lecturer' && 'Review reports and evaluate students.'}
                    {user?.role === 'admin' && 'Manage users and placements.'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
