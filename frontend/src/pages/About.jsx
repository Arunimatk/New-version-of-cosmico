import React from 'react';
import { Sparkles, Star, Heart } from 'lucide-react';


const About = () => {
    return (
        <div className="w-full pt-20">
            {/* Hero Section */}
            <div className="relative py-32 bg-secondary text-white overflow-hidden">
                <div className="absolute inset-0 opacity-10">
                    {/* Abstract background pattern could go here */}
                    <div className="absolute top-0 left-0 w-64 h-64 bg-accent rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2"></div>
                    <div className="absolute bottom-0 right-0 w-96 h-96 bg-primary rounded-full blur-3xl transform translate-x-1/3 translate-y-1/3"></div>
                </div>
                <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
                    <span className="text-accent uppercase tracking-[0.2em] mb-4 block text-sm font-semibold animate-fade-in">Our Consmic Journey</span>
                    <h1 className="text-5xl md:text-7xl font-serif mb-8 leading-tight">
                        Beauty Beyond the <br /> <span className="italic text-accent">Ordinary</span>
                    </h1>
                    <p className="text-lg md:text-xl text-white/80 max-w-2xl mx-auto leading-relaxed font-light">
                        Born from stardust and dreams, COSMICO is more than a beauty brand. It is an exploration of self-expression, designed to elevate your everyday rituals into celestial experiences.
                    </p>
                </div>
            </div>

            {/* Our Story Section */}
            <div className="py-24 px-4 max-w-4xl mx-auto text-center">
                <div>
                    <h2 className="text-4xl font-serif text-secondary mb-8">The Genesis</h2>
                    <div className="space-y-6 text-gray-600 leading-loose text-lg">
                        <p>
                            It started with a simple question: <span className="italic font-serif text-accent">Why should makeup be mundane?</span>
                        </p>
                        <p>
                            Founded in 2025, COSMICO was envisioned as a bridge between high-performance skincare and avant-garde artistry. We believe that beauty products should not only look good on your skin but should also spark joy and creativity.
                        </p>
                        <p>
                            Every formula is crafted with precision, blending potent natural ingredients with cutting-edge science. We don't just follow trends; we look to the cosmos for inspiration, creating shades and textures that are timeless yet futuristic.
                        </p>
                    </div>
                    <div className="mt-10 flex justify-center space-x-8">
                        <div className="flex flex-col items-center text-center">
                            <div className="w-12 h-12 bg-cream rounded-full flex items-center justify-center text-accent mb-3">
                                <Sparkles size={24} />
                            </div>
                            <span className="text-sm uppercase tracking-wider font-semibold text-secondary">Cruelty Free</span>
                        </div>
                        <div className="flex flex-col items-center text-center">
                            <div className="w-12 h-12 bg-cream rounded-full flex items-center justify-center text-accent mb-3">
                                <Star size={24} />
                            </div>
                            <span className="text-sm uppercase tracking-wider font-semibold text-secondary">Premium Quality</span>
                        </div>
                        <div className="flex flex-col items-center text-center">
                            <div className="w-12 h-12 bg-cream rounded-full flex items-center justify-center text-accent mb-3">
                                <Heart size={24} />
                            </div>
                            <span className="text-sm uppercase tracking-wider font-semibold text-secondary">Clean Beauty</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default About;
