import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Logs from './pages/Logs';
import Attendance from './pages/Attendance';
import Evaluations from './pages/Evaluations';
import Users from './pages/Users';
import Placements from './pages/Placements';
import Register from './pages/Register';

const ProtectedRoute = ({ children, roles }) => {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-6">Loading...</div>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" replace />;
  return children;
};

function AppRoutes() {
  const { user, logout } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" replace /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/" replace /> : <Register />} />
      <Route path="/" element={
        <ProtectedRoute><Layout /></ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="logs" element={<Logs />} />
        <Route path="attendance" element={<Attendance />} />
        <Route path="evaluations" element={
          <ProtectedRoute roles={['admin', 'supervisor', 'lecturer']}><Evaluations /></ProtectedRoute>
        } />
        <Route path="users" element={
          <ProtectedRoute roles={['admin']}><Users /></ProtectedRoute>
        } />
        <Route path="placements" element={
          <ProtectedRoute roles={['admin']}><Placements /></ProtectedRoute>
        } />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}
