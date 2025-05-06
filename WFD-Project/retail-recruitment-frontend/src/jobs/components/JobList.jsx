import React, { useEffect, useState } from 'react';
import { fetchJobs } from '../api/jobApi';

const JobList = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetchJobs()
      .then(response => setJobs(response.data))
      .catch(error => console.error('Error fetching jobs:', error));
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold">Job Listings</h2>
      <ul>
        {jobs.map(job => (
          <li key={job.id}>{job.title} - {job.company}</li>
        ))}
          <Link
                to={`/jobs/${job.id}`}
                className="text-blue-600 hover:underline text-xl font-medium"
                >
                {job.title}
          </Link>
      </ul>
    </div>
  );
};

export default JobList;
