import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { to: '/', label: 'Dashboard', icon: 'fa-chart-pie', end: true },
    { to: '/logs', label: 'Daily Logs', icon: 'fa-book-open' },
    { to: '/attendance', label: 'Attendance', icon: 'fa-calendar-check' },
    { to: '/evaluations', label: 'Evaluations', icon: 'fa-star', roles: ['admin', 'supervisor', 'lecturer'] },
    { to: '/users', label: 'Users', icon: 'fa-users', roles: ['admin'] },
    { to: '/placements', label: 'Placements', icon: 'fa-building', roles: ['admin'] },
  ];

  const visibleItems = navItems.filter(item => !item.roles || item.roles.includes(user?.role));

  return (
    <div className="d-flex">
      <aside className="sidebar col-md-2 p-0 d-none d-md-block">
        <div className="brand">
          <i className="fas fa-graduation-cap"></i>
          <span>InternTrack</span>
        </div>
        <nav className="nav flex-column mt-3">
          {visibleItems.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              <i className={`fas ${item.icon}`}></i>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-auto p-3">
          <hr style={{ borderColor: 'rgba(255,255,255,0.1)' }} />
          <div className="small text-muted">Signed in as</div>
          <div className="fw-semibold small">{user?.username}</div>
          <span className={`role-pill role-${user?.role} mt-1 d-inline-block`}>{user?.role}</span>
          <button className="btn btn-outline-light btn-sm w-100 mt-2" onClick={handleLogout}>
            <i className="fas fa-sign-out-alt me-1"></i> Logout
          </button>
        </div>
      </aside>
      <main className="flex-grow-1">
        <nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom px-3 d-md-none">
          <span className="navbar-brand fw-bold">InternTrack</span>
          <div className="d-flex align-items-center gap-2">
            <span className={`role-pill role-${user?.role}`}>{user?.role}</span>
            <button className="btn btn-outline-secondary btn-sm" onClick={handleLogout}>Logout</button>
          </div>
        </nav>
        <div className="main-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
