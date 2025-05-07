import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import RegisterForm from './pages/RegisterForm';
import AdminDashboard from './pages/Admin_Dashboard';
import Job from './pages/Job';
import JobApplication from './pages/JobApplication.html';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="AdminDashboard" element={<AdminDashboard />} />
          <Route path="Job" element={<Job />} />
         <Route path="JobApplication" element={<JobApplication />} />

      </Routes>
    </Router>
  );
}

export default App;
