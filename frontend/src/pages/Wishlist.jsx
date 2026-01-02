import React, { useEffect, useState } from 'react';
import api from '../api';
import { ShoppingBag, X } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

const Wishlist = () => {
  const [wishlistItems, setWishlistItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchWishlist();
  }, []);

  // ================= FETCH WISHLIST =================
  const fetchWishlist = async () => {
    try {
      const response = await api.get('wishlist/');
      if (response.data && Array.isArray(response.data.items)) {
        setWishlistItems(response.data.items);
      } else {
        setWishlistItems([]);
      }
    } catch (error) {
      console.error("Failed to fetch wishlist", error);
    } finally {
      setLoading(false);
    }
  };

  // ================= REMOVE FROM WISHLIST =================
  const handleRemove = async (productId) => {
    try {
      await api.post('wishlist/toggle/', { product_id: productId });
      setWishlistItems(prev =>
        prev.filter(item => item.product.id !== productId)
      );
    } catch (error) {
      console.error("Failed to remove from wishlist", error);
    }
  };

  // ================= ADD TO CART (AMAZON STYLE) =================
  const handleAddToCart = async (product) => {
    try {
      await api.post('cart/add/', {
        product_id: product.id,
        quantity: 1,
      });

      // Optional: remove from wishlist
      await handleRemove(product.id);

      // 👉 Redirect to Cart page
      navigate('/cart');

    } catch (error) {
      console.error("Failed to add to cart", error);
      alert("Failed to add to cart");
    }
  };

  // ================= LOADING =================
  if (loading) {
    return <div className="pt-24 text-center">Loading wishlist...</div>;
  }

  // ================= EMPTY WISHLIST =================
  if (wishlistItems.length === 0) {
    return (
      <div className="pt-24 px-4 max-w-7xl mx-auto min-h-screen text-center flex flex-col items-center justify-center">
        <ShoppingBag size={64} className="text-gray-300 mb-6" />
        <h2 className="text-4xl font-serif mb-4">Your Wishlist is Empty</h2>
        <p className="text-gray-500 mb-8">Save items you love here.</p>
        <Link
          to="/shop"
          className="px-8 py-3 bg-accent text-white uppercase tracking-widest hover:bg-secondary transition-colors"
        >
          Start Shopping
        </Link>
      </div>
    );
  }

  // ================= UI =================
  return (
    <div className="pt-24 px-4 max-w-7xl mx-auto min-h-screen">
      <h2 className="text-4xl font-serif mb-12 text-center">Your Wishlist</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {wishlistItems.map((item) => (
          <div
            key={item.id}
            className="bg-white rounded-xl shadow-sm overflow-hidden group"
          >
            <div className="relative h-64 overflow-hidden">
              {item.product.image ? (
                <img
                  src={
                    item.product.image.startsWith('http')
                      ? item.product.image
                      : `http://127.0.0.1:8000${item.product.image}`
                  }
                  alt={item.product.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-gray-100 text-gray-400">
                  No Image
                </div>
              )}

              <button
                onClick={() => handleRemove(item.product.id)}
                className="absolute top-4 right-4 bg-white p-2 rounded-full shadow-md text-gray-400 hover:text-red-500"
              >
                <X size={20} />
              </button>
            </div>

            <div className="p-6 text-center">
              <h3 className="text-xl font-medium text-accent mb-2">
                {item.product.name}
              </h3>
              <div className="text-secondary font-medium mb-4">
                ₹{item.product.price}
              </div>

              <button
                onClick={() => handleAddToCart(item.product)}
                className="w-full py-3 border border-secondary text-secondary hover:bg-secondary hover:text-white transition-colors uppercase tracking-wider text-sm"
              >
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Wishlist;

