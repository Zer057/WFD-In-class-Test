import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password1: '',
        password2: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Send formData to your Django backend API endpoint
        try {
            const response = await fetch('http://localhost:8000/api/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            if (response.ok) {
                alert('User registered successfully!');
            } else {
                alert('Registration failed: ' + JSON.stringify(data));
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred');
        }
    };

    return (
        <div className="container mt-5">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label>Username</label>
                    <input type="text" name="username" className="form-control" value={formData.username} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label>Email</label>
                    <input type="email" name="email" className="form-control" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label>Password</label>
                    <input type="password" name="password1" className="form-control" value={formData.password1} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label>Confirm Password</label>
                    <input type="password" name="password2" className="form-control" value={formData.password2} onChange={handleChange} required />
                </div>
                <button type="submit" className="btn btn-primary">Register</button>
            </form>
        </div>
    );
};

export default RegisterForm;
