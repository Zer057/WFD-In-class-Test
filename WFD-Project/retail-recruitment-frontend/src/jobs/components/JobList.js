import { useEffect, useState } from 'react';
import api from '../services/api';

export default function JobList() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    api.get('jobs/').then(res => setJobs(res.data));
  }, []);

  return (
    <ul>
      {jobs.map(job => (
        <li key={job.id}>{job.title}</li>
      ))}
    </ul>
  );
}
