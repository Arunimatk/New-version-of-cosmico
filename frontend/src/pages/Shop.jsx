import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Heart, ShoppingBag, Eye } from 'lucide-react';
import api from '../api';

const Shop = () => {
    const { category } = useParams();
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);




    const handleAddToCart = async (productId, action = 'cart') => {
        try {
            await api.post('cart/add/', { product_id: productId, quantity: 1 });
            if (action === 'checkout') {
                navigate('/checkout');
            } else {
                navigate('/cart');
            }
        } catch (error) {
            console.error("Add to cart failed", error);
            if (error.response) {
                if (error.response.status === 401) {
                    // Save pending action
                    const pendingAction = {
                        type: action === 'checkout' ? 'buyNow' : 'addToCart',
                        payload: { product_id: productId, quantity: 1 }
                    };
                    localStorage.setItem('pendingAction', JSON.stringify(pendingAction));
                    navigate('/login');
                } else {
                    alert(`Add to cart failed: ${error.response.data.error || 'Unknown error'}`);
                }
            } else {
                alert("Network error or server unreachable.");
            }
        }
    };

    const handleAddToWishlist = async (productId) => {
        try {
            await api.post('wishlist/toggle/', { product_id: productId });
            alert("Updated wishlist!");
        } catch (error) {
            if (error.response && error.response.status === 401) {
                navigate('/login');
            }
        }
    };

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('products/');
                let data = response.data;
                if (category) {
                    data = data.filter(p => p.category_name.toLowerCase() === category.toLowerCase());
                }
                console.log("Shop Data:", data); // Debugging
                setProducts(data);
            } catch (error) {
                console.error("Failed to fetch products", error);
            }
        };
        fetchProducts();
    }, [category]);

    return (
        <div className="pt-24 px-4 max-w-7xl mx-auto min-h-screen">
            <h2 className="text-4xl font-serif text-center mb-10 capitalize">{category || "All Products"}</h2>

            {products.length === 0 ? (
                <div className="text-center text-gray-500 text-xl mt-10">
                    <p>No products found in this category.</p>
                    <p className="text-sm mt-2">Try adding products via the Admin Panel.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                    {products.map(product => (
                        <div key={product.id} className="group flex flex-col h-full bg-white bg-opacity-50 glass-card transition-all duration-300 hover:shadow-xl">
                            <div className="relative overflow-hidden h-80 bg-gray-100">
                                {/* Fix: Prepend backend URL if path is relative */}
                                <img
                                    src={product.image ? (product.image.startsWith('http') ? product.image : `http://127.0.0.1:8000${product.image}`) : "https://placehold.co/400x600?text=Cosmico"}
                                    alt={product.name}
                                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                />
                                {/* Make image clickable to go to detail */}
                                <Link to={`/product/${product.id}`} className="absolute inset-0 z-10" />

                                <div className="absolute top-3 right-3 flex flex-col gap-2 z-20">
                                    <button onClick={(e) => { e.preventDefault(); handleAddToWishlist(product.id); }} className="p-2.5 bg-white bg-opacity-90 rounded-full text-accent hover:text-white hover:bg-accent hover:shadow-lg transition-all shadow-md transform hover:scale-110" title="Add to Wishlist">
                                        <Heart size={22} />
                                    </button>
                                    <button onClick={(e) => { e.preventDefault(); handleAddToCart(product.id, 'cart'); }} className="p-2.5 bg-white bg-opacity-90 rounded-full text-accent hover:text-white hover:bg-accent hover:shadow-lg transition-all shadow-md transform hover:scale-110" title="Add to Cart">
                                        <ShoppingBag size={22} />
                                    </button>
                                </div>


                            </div>
                            <div className="p-4 flex-grow flex flex-col justify-between text-center">
                                <div>
                                    <Link to={`/product/${product.id}`}>
                                        <h3 className="text-xl font-serif mb-1 hover:text-accent transition-colors">{product.name}</h3>
                                    </Link>
                                    <p className="text-sm text-gray-500 line-clamp-2 mb-2">{product.description}</p>
                                </div>

                                <div className="mt-2">
                                    <div className="flex justify-center gap-1 mb-2">
                                        {product.shades && Array.isArray(product.shades) && product.shades.map((shade, idx) => (
                                            // Fix: Check if shade is a hex color or a text name
                                            shade.startsWith('#') ? (
                                                <div key={idx} className="w-4 h-4 rounded-full border border-gray-200" style={{ backgroundColor: shade }} title={shade} />
                                            ) : (
                                                <span key={idx} className="text-[10px] px-1.5 py-0.5 bg-gray-100 border border-gray-200 rounded text-gray-600 truncate max-w-[60px]" title={shade}>
                                                    {shade}
                                                </span>
                                            )
                                        ))}
                                    </div>
                                    <p className="text-secondary font-medium text-lg">${product.price}</p>
                                    <div className="flex flex-col gap-2 mt-3">
                                        <div className="flex gap-2">
                                            <button
                                                onClick={(e) => { e.preventDefault(); handleAddToCart(product.id, 'cart'); }}
                                                className="flex-1 py-2.5 border border-accent text-accent font-medium uppercase text-xs tracking-wider hover:bg-accent hover:text-white transition-colors"
                                            >
                                                Add to Cart
                                            </button>
                                            <button
                                                onClick={(e) => { e.preventDefault(); handleAddToCart(product.id, 'checkout'); }}
                                                className="flex-1 py-2.5 bg-accent text-white font-medium uppercase text-xs tracking-wider hover:bg-secondary transition-colors"
                                            >
                                                Buy Now
                                            </button>
                                        </div>
                                        <Link to={`/product/${product.id}`} className="block w-full py-2 bg-gray-100 text-gray-700 text-center uppercase text-xs tracking-wider hover:bg-gray-200 transition-colors">
                                            View Details
                                        </Link>
                                    </div>


                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Shop;
