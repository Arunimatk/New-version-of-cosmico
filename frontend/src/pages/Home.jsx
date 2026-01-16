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

const Home = () => {
    return (
        <div className="w-full">
            <Hero />
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
        </div >
    );
};

export default Home;
