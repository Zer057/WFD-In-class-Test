import React, { useState } from 'react';
import axios from 'axios';

const CreateJobForm = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    location: '',
  });

  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage('');
    setErrorMessage('');

    try {
      const token = localStorage.getItem('access');
      await axios.post('http://localhost:8000/api/jobs/', formData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setSuccessMessage('Job posted successfully!');
      setFormData({ title: '', description: '', location: '' });
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to post job. Please check your input or login status.');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Post a New Job</h2>
      {successMessage && <div className="text-green-600 mb-2">{successMessage}</div>}
      {errorMessage && <div className="text-red-600 mb-2">{errorMessage}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="title"
          placeholder="Job Title"
          value={formData.title}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <textarea
          name="description"
          placeholder="Job Description"
          value={formData.description}
          onChange={handleChange}
          required
          rows={5}
          className="w-full border px-3 py-2 rounded"
        />
        <input
          type="text"
          name="location"
          placeholder="Job Location"
          value={formData.location}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700"
        >
          Submit Job
        </button>
      </form>
    </div>
  );
};

export default CreateJobForm;
