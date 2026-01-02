
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Heart, ShoppingBag, ArrowLeft, Star } from 'lucide-react';
import api from '../api';

const ProductDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(null);
    const [selectedShade, setSelectedShade] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await api.get(`products/${id}/`);
                setProduct(response.data);
                if (response.data.shades && response.data.shades.length > 0) {
                    setSelectedShade(response.data.shades[0]);
                }
            } catch (error) {
                console.error("Failed to fetch product", error);
            } finally {
                setLoading(false);
            }
        };
        fetchProduct();
    }, [id]);




    const handleAddToCart = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            localStorage.setItem('pendingAction', JSON.stringify({
                type: 'addToCart',
                payload: { product_id: product.id, quantity: 1, shade: selectedShade }
            }));
            navigate('/register');
            return;
        }

        try {
            await api.post('cart/add/', {
                product_id: product.id,
                quantity: 1,
                shade: selectedShade
            });
            // alert("Added to cart!"); // Removed explicit alert to mimic simple redirect
            navigate('/cart');
        } catch (error) {
            console.error("Add to cart failed", error);
            if (error.response) {
                if (error.response.status === 401) {
                    navigate('/register');
                } else {
                    alert(`Add to cart failed: ${error.response.data.error || 'Unknown error'}`);
                }
            } else {
                alert("Network error or server unreachable.");
            }
        }
    };

    const handleBuyNow = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            localStorage.setItem('pendingAction', JSON.stringify({
                type: 'buyNow',
                payload: { product_id: product.id, quantity: 1, shade: selectedShade }
            }));
            navigate('/register');
            return;
        }

        try {
            await api.post('cart/add/', {
                product_id: product.id,
                quantity: 1,
                shade: selectedShade
            });
            navigate('/checkout');
        } catch (error) {
            console.error("Buy now failed (add to cart)", error);
            if (error.response && error.response.status === 401) {
                navigate('/register');
            }
        }
    };

    const handleAddToWishlist = async () => {
        try {
            await api.post('wishlist/toggle/', { product_id: product.id });
            alert("Updated wishlist!");
        } catch (error) {
            if (error.response && error.response.status === 401) {
                navigate('/login');
            }
        }
    };

    if (loading) return <div className="min-h-screen pt-24 flex justify-center items-center">Loading...</div>;
    if (!product) return <div className="min-h-screen pt-24 flex justify-center items-center">Product not found</div>;

    // Fix Image URL
    const imageUrl = product.image ? (product.image.startsWith('http') ? product.image : `http://127.0.0.1:8000${product.image}`) : "https://placehold.co/600x600?text=Cosmico";

    return (
        <div className="pt-28 pb-16 px-4 max-w-7xl mx-auto min-h-screen">
            <button onClick={() => navigate(-1)} className="flex items-center text-gray-500 hover:text-accent mb-8 transition-colors">
                <ArrowLeft size={20} className="mr-2" /> Back to Shop
            </button>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 lg:gap-20">
                {/* Image Section */}
                <div className="bg-white p-4 rounded-2xl shadow-sm">
                    <img src={imageUrl} alt={product.name} className="w-full h-auto rounded-xl object-cover" />
                </div>

                {/* Details Section */}
                <div className="flex flex-col justify-center">
                    <div className="mb-2 text-sm text-gray-500 uppercase tracking-wider">{product.category_name}</div>
                    <h1 className="text-4xl md:text-5xl font-serif text-accent mb-4">{product.name}</h1>

                    <div className="flex items-center space-x-2 mb-6">
                        <div className="flex text-yellow-500">
                            {[...Array(5)].map((_, i) => (
                                <Star key={i} size={18} fill={i < Math.round(product.rating || 5) ? "currentColor" : "none"} />
                            ))}
                        </div>
                        <span className="text-gray-400 text-sm">({product.rating || 5.0})</span>
                    </div>

                    <p className="text-gray-600 text-lg leading-relaxed mb-8">
                        {product.description}
                    </p>

                    <div className="mb-8">
                        <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wider mb-4">Select Shade</h3>
                        <div className="flex flex-wrap gap-3">
                            {product.shades && product.shades.map((shade, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => setSelectedShade(shade)}
                                    className={`group relative w-10 h-10 rounded-full border-2 transition-all ${selectedShade === shade ? 'border-accent scale-110 shadow-md' : 'border-gray-200 hover:border-accent'}`}
                                    title={shade}
                                >
                                    {shade.startsWith('#') ? (
                                        <span className="absolute inset-1 rounded-full" style={{ backgroundColor: shade }}></span>
                                    ) : (
                                        <span className="absolute inset-0 flex items-center justify-center text-[10px] bg-gray-100 rounded-full text-gray-600 font-medium overflow-hidden px-1">
                                            {shade.slice(0, 3)}
                                        </span>
                                    )}
                                    {/* Tooltip for text shades */}
                                    {!shade.startsWith('#') && (
                                        <span className="absolute -bottom-8 left-1/2 -translate-x-1/2 bg-black text-white text-xs py-1 px-2 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap z-10 pointer-events-none">
                                            {shade}
                                        </span>
                                    )}
                                </button>
                            ))}
                        </div>
                        {selectedShade && (
                            <p className="mt-3 text-sm text-gray-500">Selected: <span className="font-semibold text-accent">{selectedShade}</span></p>
                        )}
                    </div>

                    <div className="flex items-center justify-between border-t border-gray-100 pt-8">
                        <div className="text-3xl font-serif text-secondary">${product.price}</div>
                        <div className="flex space-x-4">
                            <button onClick={handleAddToWishlist} className="p-4 rounded-full border border-gray-200 text-gray-400 hover:bg-gray-50 hover:text-red-500 transition-all">
                                <Heart size={24} />
                            </button>
                            <button onClick={handleAddToCart} className="px-6 py-4 bg-white text-secondary font-medium tracking-widest border border-secondary hover:bg-gray-50 transition-colors uppercase rounded-full flex items-center">
                                <ShoppingBag size={20} className="mr-2" /> Add to Cart
                            </button>
                            <button onClick={handleBuyNow} className="px-8 py-4 bg-accent text-white font-medium tracking-widest hover:bg-secondary transition-colors uppercase rounded-full shadow-lg hover:shadow-xl flex items-center">
                                Buy Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;
