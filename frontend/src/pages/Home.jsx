import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

import cosmetices from '../assets/cosmetices.jpg';
import lip1 from '../assets/lip1.webp';
import found5 from '../assets/found5.webp';
import PERFUME from '../assets/PERFUME.webp';
import BLUSH from '../assets/BLUSH.webp';
import NAILPOLISH from '../assets/Nailpolish.webp';
const Hero = () => (
    <div className="relative h-screen flex items-center justify-center bg-gradient-to-r from-primary to-cream overflow-hidden">
        <div className="absolute inset-0 opacity-40">
            {/* Background pattern or image here */}
            <img src={cosmetices} alt="Cosmetics" className="w-full h-full object-cover" />
        </div>
        <div className="relative z-10 text-center px-4">
            <h1 className="text-5xl md:text-7xl font-serif text-accent mb-6 tracking-tight animate-fade-in-up">
                Redefine Your Beauty
            </h1>
            <p className="text-xl md:text-2xl text-accent/80 mb-8 max-w-2xl mx-auto font-light">
                Discover the new era of luxury cosmetics. Pure, Elegant, Cosmic.
            </p>
            <Link to="/shop" className="inline-block px-10 py-4 border-2 border-accent text-accent hover:bg-accent hover:text-white transition-all duration-300 tracking-widest text-sm font-semibold uppercase">
                Shop Collection
            </Link>
        </div>
    </div>
);

const CategoryCard = ({ title, img, link }) => (
    <Link to={link} className="group relative block h-96 overflow-hidden">
        <img src={img} alt={title} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
        <div className="absolute inset-0 flex items-center justify-center">
            <h3 className="text-3xl text-white font-serif tracking-widest uppercase border-b-2 border-transparent group-hover:border-white transition-all pb-1">
                {title}
            </h3>
        </div>
    </Link>
);

const TrendingSection = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => { // Fetch trending products for home page
        const fetchTrending = async () => {
            try {
                // Use the main products endpoint which is confirmed to work on the Shop page
                const response = await api.get(`products/?t=${Date.now()}`);
                setProducts(response.data.slice(0, 50)); // Display latest 50 items
            } catch (error) {
                console.error("Failed to fetch trending", error);
            } finally {
                setLoading(false);
            }
        };
        fetchTrending();
    }, []);

    if (loading) return <div className="py-20 text-center">Loading...</div>;

    return (
        <section className="py-20 px-4 max-w-7xl mx-auto bg-white/50">
            <h2 className="text-4xl font-serif text-center mb-12">New Arrivals</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 mb-12">
                {products.map(product => (
                    <Link key={product.id} to={`/product/${product.id}`} className="group block">
                        <div className="relative h-80 overflow-hidden mb-4 bg-gray-100">
                            <img
                                src={product.image || "https://placehold.co/400x600?text=Cosmico"}
                                alt={product.name}
                                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                            />
                            <div className="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition-all" />
                        </div>
                        <h3 className="text-lg font-serif mb-1 group-hover:text-accent transition-colors">{product.name}</h3>
                        <p className="text-secondary font-medium">${product.price}</p>
                    </Link>
                ))}
            </div>
            <div className="text-center">
                <Link to="/shop" className="inline-block px-8 py-3 border border-primary text-primary hover:bg-primary hover:text-white transition-all duration-300 tracking-widest text-sm font-semibold uppercase">
                    View All Collection
                </Link>
            </div>
        </section >
    );
};

const Home = () => {
    return (
        <div className="w-full">
            <Hero />

            {/* Trending Section - Added for visibility */}
            <TrendingSection />

            {/* Categories */}
            <section className="py-20 px-4 max-w-7xl mx-auto">
                <h2 className="text-4xl font-serif text-center mb-16">The Collection</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                    <CategoryCard
                        title="Lipstick"
                        link="/shop/lipstick"
                        img={lip1}
                    />
                    <CategoryCard
                        title="Foundation"
                        link="/shop/foundation"
                        img={found5}
                    />
                    <CategoryCard
                        title="Perfume"
                        link="/shop/perfume"
                        img={PERFUME}
                    />
                    <CategoryCard
                        title="Blush"
                        link="/shop/blush"
                        img={BLUSH}
                    />
                    <CategoryCard
                        title="Nailpolish"
                        link="/shop/Nailpolish"
                        img={NAILPOLISH}
                    />
                </div>
            </section>
        </div>
    );
};

export default Home;
