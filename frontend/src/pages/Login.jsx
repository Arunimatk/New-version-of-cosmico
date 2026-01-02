import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

const Login = () => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('auth/login/', formData);
            localStorage.setItem('token', response.data.token);
            // Store username for display
            if (response.data.username) {
                localStorage.setItem('username', response.data.username);
            } else {
                // Fallback if backend doesn't return it, though ideally it should. 
                // We can use the input username as a temporary measure if successful.
                localStorage.setItem('username', formData.username);
            }

            await processPendingAction();

        } catch (err) {
            setError('Invalid credentials');
        }
    };

    // Helper to process pending actions
    const processPendingAction = async () => {
        const pendingAction = localStorage.getItem('pendingAction');
        if (pendingAction) {
            const action = JSON.parse(pendingAction);
            localStorage.removeItem('pendingAction');
            try {
                if (action.type === 'addToCart') {
                    await api.post('cart/add/', action.payload);
                    navigate('/cart');
                } else if (action.type === 'buyNow') {
                    await api.post('cart/add/', action.payload); // Buy Now also adds to cart usually, or separate order
                    // Assuming 'buyNow' flow just adds to cart and goes to checkout for now as per previous logic in Shop.jsx
                    navigate('/checkout');
                }
            } catch (error) {
                console.error("Failed to process pending action", error);
                navigate('/');
            }
        } else {
            navigate('/');
        }
    };

    return (
        <div className="min-h-screen pt-20 flex items-center justify-center bg-primary">
            <div className="glass-card p-10 max-w-md w-full rounded-none">
                <h2 className="text-3xl font-serif text-center mb-8">Welcome Back</h2>
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
                        <label className="block text-sm font-medium mb-1">Password</label>
                        <input
                            type="password" name="password" value={formData.password} onChange={handleChange}
                            className="w-full bg-white bg-opacity-50 border border-gray-200 p-3 focus:outline-none focus:border-secondary transition-colors"
                            required
                        />
                    </div>
                    <button type="submit" className="w-full bg-accent text-white py-3 hover:bg-secondary transition-colors uppercase tracking-wider text-sm">
                        Login
                    </button>
                </form>
                <div className="mt-6 text-center text-sm">
                    <p>Don't have an account? <Link to="/register" className="text-secondary hover:underline">Register</Link></p>
                </div>
            </div>
        </div>
    );
};

export default Login;
