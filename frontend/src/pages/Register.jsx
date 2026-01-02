import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

const Register = () => {
    const [formData, setFormData] = useState({ username: '', email: '', password: '', confirmPassword: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        try {
            const response = await api.post('auth/register/', {
                username: formData.username,
                email: formData.email,
                password: formData.password
            });
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('username', formData.username);

            // Check for pending action
            const pendingAction = localStorage.getItem('pendingAction');
            if (pendingAction) {
                const action = JSON.parse(pendingAction);
                localStorage.removeItem('pendingAction');

                if (action.type === 'addToCart') {
                    await api.post('cart/add/', action.payload);
                    navigate('/cart');
                } else if (action.type === 'buyNow') {
                    await api.post('cart/add/', action.payload);
                    navigate('/checkout');
                } else {
                    navigate('/');
                }
            } else {
                navigate('/');
            }

        } catch (err) {
            setError(err.response?.data?.error || 'Registration failed');
        }
    };

    return (
        <div className="min-h-screen pt-20 flex items-center justify-center bg-primary">
            <div className="glass-card p-10 max-w-md w-full rounded-none">
                <h2 className="text-3xl font-serif text-center mb-8">Create Account</h2>
                {error && <p className="text-red-500 text-center mb-4">{error}</p>}
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-1">Username</label>
                        <input
                            type="text" name="username" value={formData.username} onChange={handleChange}
                            className="w-full bg-white bg-opacity-50 border border-gray-200 p-3 focus:outline-none focus:border-secondary transition-colors"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Email</label>
                        <input
                            type="email" name="email" value={formData.email} onChange={handleChange}
                            className="w-full bg-white bg-opacity-50 border border-gray-200 p-3 focus:outline-none focus:border-secondary transition-colors"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Password</label>
                        <input
                            type="password" name="password" value={formData.password} onChange={handleChange}
                            className="w-full bg-white bg-opacity-50 border border-gray-200 p-3 focus:outline-none focus:border-secondary transition-colors"
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Confirm Password</label>
                        <input
                            type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange}
                            className="w-full bg-white bg-opacity-50 border border-gray-200 p-3 focus:outline-none focus:border-secondary transition-colors"
                            required
                        />
                    </div>
                    <button type="submit" className="w-full bg-accent text-white py-3 hover:bg-secondary transition-colors uppercase tracking-wider text-sm">
                        Register
                    </button>
                </form>
                <div className="mt-6 text-center text-sm">
                    <p>Already have an account? <Link to="/login" className="text-secondary hover:underline">Login</Link></p>
                </div>
            </div>
        </div>
    );
};

export default Register;
