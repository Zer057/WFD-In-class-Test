import { Link } from 'react-router-dom';

export default function ManagerDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-green-600">Manager Dashboard</h1>
        <div className="space-x-4">
          <Link to="/candidate-dashboard" className="text-green-500 hover:underline">Candidate</Link>
          <Link to="/recruiter-dashboard" className="text-green-500 hover:underline">Recruiter</Link>
          <Link to="/dashboard" className="text-green-500 hover:underline">Main Dashboard</Link>
          <Link to="/" className="text-red-500 hover:underline">Logout</Link>
        </div>
      </nav>
      <main className="p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white shadow rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-2">Team Overview</h2>
            <p>Monitor the performance and progress of your team members.</p>
            <button className="mt-4 bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600">View Team</button>
          </div>
          <div className="bg-white shadow rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-2">Reports</h2>
            <p>Generate reports on project status and employee performance.</p>
            <button className="mt-4 bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600">Generate Report</button>
          </div>
        </div>
      </main>
    </div>
  );
}
