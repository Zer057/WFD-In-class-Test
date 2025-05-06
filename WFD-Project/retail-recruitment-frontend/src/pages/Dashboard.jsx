import { Link } from 'react-router-dom';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-indigo-600">Main Dashboard</h1>
        <div className="space-x-4">
          <Link to="/candidate-dashboard" className="text-indigo-500 hover:underline">Candidate</Link>
          <Link to="/manager-dashboard" className="text-indigo-500 hover:underline">Manager</Link>
          <Link to="/recruiter-dashboard" className="text-indigo-500 hover:underline">Recruiter</Link>
          <Link to="/" className="text-red-500 hover:underline">Logout</Link>
        </div>
      </nav>

      <main className="p-8">
        <h2 className="text-2xl font-bold text-center mb-6">Welcome to the Dashboard</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/candidate-dashboard" className="bg-white shadow rounded-xl p-6 hover:shadow-lg text-center">
            <h3 className="text-lg font-semibold mb-2">Candidate Portal</h3>
            <p>View jobs, apply, and manage your profile.</p>
          </Link>
          <Link to="/manager-dashboard" className="bg-white shadow rounded-xl p-6 hover:shadow-lg text-center">
            <h3 className="text-lg font-semibold mb-2">Manager Portal</h3>
            <p>Monitor team progress and reports.</p>
          </Link>
          <Link to="/recruiter-dashboard" className="bg-white shadow rounded-xl p-6 hover:shadow-lg text-center">
            <h3 className="text-lg font-semibold mb-2">Recruiter Portal</h3>
            <p>Post jobs, review candidates, manage interviews.</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
