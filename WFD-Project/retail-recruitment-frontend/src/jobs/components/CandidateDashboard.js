import { Link } from 'react-router-dom';

export default function CandidateDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">Candidate Dashboard</h1>
        <div className="space-x-4">
          <Link to="/manager-dashboard" className="text-blue-500 hover:underline">Manager</Link>
          <Link to="/recruiter-dashboard" className="text-blue-500 hover:underline">Recruiter</Link>
          <Link to="/dashboard" className="text-blue-500 hover:underline">Main Dashboard</Link>
          <Link to="/" className="text-red-500 hover:underline">Logout</Link>
        </div>
      </nav>
      <main className="p-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white shadow rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-2">Job Recommendations</h2>
            <p>View personalized job openings based on your profile.</p>
            <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Explore Jobs</button>
          </div>
          <div className="bg-white shadow rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-2">My Applications</h2>
            <p>Track the status of your job applications in one place.</p>
            <button className="mt-4 bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600">View Applications</button>
          </div>
          <div className="bg-white shadow rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-2">Profile</h2>
            <p>Update your resume, skills, and contact information.</p>
            <button className="mt-4 bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600">Edit Profile</button>
          </div>
        </div>
      </main>
    </div>
  );
}
