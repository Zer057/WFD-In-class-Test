import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setCredentials({...credentials, [e.target.name]: e.target.value});
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Logging in with:', credentials);
    // Add authentication logic here
    navigate('/dashboard'); // Redirect after login
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-8 shadow-lg rounded-xl w-full max-w-md mx-auto mt-20">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-600">Login</h2>

      <div className="mb-4">
        <label className="block mb-1 font-semibold">Email</label>
        <input
          type="email"
          name="email"
          value={credentials.email}
          onChange={handleChange}
          className="w-full border rounded-lg px-3 py-2"
          required
        />
      </div>

      <div className="mb-6">
        <label className="block mb-1 font-semibold">Password</label>
        <input
          type="password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          className="w-full border rounded-lg px-3 py-2"
          required
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
      >
        Login
      </button>

      <p className="text-center mt-4">
        Don't have an account? <a href="/register" className="text-blue-500 hover:underline">Register</a>
      </p>
    </form>
  );
}
