import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { CheckCircle, ShoppingBag, ArrowRight } from 'lucide-react';
import confetti from 'canvas-confetti';

const OrderSuccess = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Fire confetti
        const duration = 3000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        const random = (min, max) => Math.random() * (max - min) + min;

        const interval = setInterval(function () {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            const particleCount = 50 * (timeLeft / duration);
            confetti({ ...defaults, particleCount, origin: { x: random(0.1, 0.3), y: Math.random() - 0.2 } });
            confetti({ ...defaults, particleCount, origin: { x: random(0.7, 0.9), y: Math.random() - 0.2 } });
        }, 250);
    }, []);

    return (
        <div className="min-h-screen pt-24 bg-gradient-to-b from-white to-gray-50 flex flex-col items-center text-center px-4">
            <div className="mb-6 animate-bounce-subtle">
                <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto text-green-500">
                    <CheckCircle size={64} strokeWidth={1.5} />
                </div>
            </div>

            <h1 className="text-4xl md:text-5xl font-serif text-secondary mb-4 animate-fade-in-up">Order Placed Successfully!</h1>
            <p className="text-lg text-gray-500 max-w-lg mb-10 animate-fade-in-up delay-100">
                Thank you for your purchase. Your cosmetic journey has just begun.
                We have sent a confirmation email to your inbox.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 animate-fade-in-up delay-200">
                <Link to="/shop" className="group flex items-center px-8 py-4 bg-accent text-white font-medium uppercase tracking-widest rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                    <ShoppingBag size={20} className="mr-2 group-hover:animate-pulse" />
                    Continue Shopping
                </Link>
                <div onClick={() => navigate('/')} className="cursor-pointer group flex items-center px-8 py-4 border-2 border-accent text-accent font-medium uppercase tracking-widest rounded-lg hover:bg-accent hover:text-white transition-all">
                    Return Home
                    <ArrowRight size={20} className="ml-2 group-hover:translate-x-1 transition-transform" />
                </div>
            </div>
        </div>
    );
};

export default OrderSuccess;
