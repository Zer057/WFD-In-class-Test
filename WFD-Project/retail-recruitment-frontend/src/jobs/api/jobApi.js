import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/jobs/';

export const fetchJobs = () => axios.get(BASE_URL);
export const fetchJob = (id) => axios.get(`${BASE_URL}${id}/`);
export const createJob = (data) => axios.post(BASE_URL, data);
export const updateJob = (id, data) => axios.put(`${BASE_URL}${id}/`, data);
export const deleteJob = (id) => axios.delete(`${BASE_URL}${id}/`);
