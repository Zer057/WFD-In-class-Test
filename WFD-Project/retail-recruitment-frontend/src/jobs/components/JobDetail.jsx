import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const JobDetails = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/jobs/${id}/`);
        setJob(response.data);
      } catch (err) {
        setError('Job not found or failed to fetch.');
        console.error(err);
      }
    };

    fetchJob();
  }, [id]);

  if (error) {
    return <div className="text-red-600">{error}</div>;
  }

  if (!job) {
    return <div>Loading...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto bg-white shadow-md rounded p-6">
      <h2 className="text-3xl font-bold mb-4 text-blue-700">{job.title}</h2>
      <p className="text-gray-700 mb-2"><strong>Description:</strong> {job.description}</p>
      <p className="text-gray-700 mb-2"><strong>Location:</strong> {job.location}</p>
      <p className="text-gray-500 text-sm">Posted by: {job.recruiter?.user?.username || 'Unknown'}</p>

      <Link
        to="/"
        className="mt-6 inline-block text-blue-600 hover:underline"
      >
        ← Back to Listings
      </Link>
    </div>
  );
};

export default JobDetails;
