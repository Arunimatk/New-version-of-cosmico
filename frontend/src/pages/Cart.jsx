import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, ShoppingBag } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await api.get('cart/');
      // Backend returns { id: ..., items: [...], total_price: ... }
      if (response.data && Array.isArray(response.data.items)) {
        setCartItems(response.data.items);
      } else {
        setCartItems([]);
        console.error("Unexpected cart API format", response.data);
      }
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch cart", err);
      if (err.response && err.response.status === 401) {
        navigate('/login');
      } else {
        setError('Failed to load cart items.');
      }
      setLoading(false);
    }
  };

  const handleRemove = async (productId) => {
    try {
      await api.post('cart/remove/', { product_id: productId });
      // Re-fetch cart or filter out locally. Detailed fetch preferred to update totals from backend if needed,
      // but simplistic local update is faster for UI.
      // Since we calculate total locally in this component now, filtering is fine.
      setCartItems(cartItems.filter(item => item.product.id !== productId));
    } catch (err) {
      console.error("Failed to remove item", err);
      setError("Failed to remove item. Please try again.");
    }
  };




  if (loading) return <div className="pt-24 text-center">Loading cart...</div>;

  if (cartItems.length === 0) {
    return (
      <div className="pt-24 px-4 max-w-7xl mx-auto min-h-screen text-center flex flex-col items-center justify-center">
        <ShoppingBag size={64} className="text-gray-300 mb-6" />
        <h2 className="text-4xl font-serif mb-4">Your Cart is Empty</h2>
        <p className="text-gray-500 mb-8">Looks like you haven't added anything yet.</p>
        <Link to="/shop" className="px-8 py-3 bg-accent text-white uppercase tracking-widest hover:bg-secondary transition-colors">
          Start Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="pt-24 px-4 max-w-7xl mx-auto min-h-screen">
      <h2 className="text-4xl font-serif mb-12 text-center">Your Cart</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <div className="lg:col-span-2 space-y-6">
          {cartItems.map((item) => (
            <div key={item.id} className="flex gap-6 p-4 bg-white rounded-xl shadow-sm items-center">
              <div className="w-24 h-24 flex-shrink-0 bg-gray-100 rounded-lg overflow-hidden">
                {item.product.image ? (
                  <img
                    src={item.product.image.startsWith('http') ? item.product.image : `http://127.0.0.1:8000${item.product.image}`}
                    alt={item.product.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">No Img</div>
                )}
              </div>
              <div className="flex-grow">
                <h3 className="text-lg font-medium text-accent">{item.product.name}</h3>
                {item.shade && <p className="text-sm text-gray-500 mt-1">Shade: {item.shade}</p>}
                <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
              </div>
              <div className="text-right">
                <div className="text-lg font-medium text-secondary">${item.product.price}</div>
                <button
                  onClick={() => handleRemove(item.product.id)}
                  className="mt-2 text-red-400 hover:text-red-600 p-2 transition-colors"
                  title="Remove item"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white p-6 rounded-xl shadow-sm sticky top-28">
            <h3 className="text-xl font-serif mb-6 text-secondary">Order Summary</h3>

            <div className="space-y-4 mb-6">
              <div className="flex justify-between text-gray-600">
                <span>Subtotal</span>
                <span>${cartItems.reduce((acc, item) => acc + (parseFloat(item.product.price) * item.quantity), 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-gray-600">
                <span>Shipping</span>
                <span className="text-green-600">Free</span>
              </div>
              <div className="h-px bg-gray-100 my-4"></div>
              <div className="flex justify-between text-lg font-medium text-secondary">
                <span>Total</span>
                <span>${cartItems.reduce((acc, item) => acc + (parseFloat(item.product.price) * item.quantity), 0).toFixed(2)}</span>
              </div>
            </div>

            <button
              onClick={() => navigate('/checkout')}
              className="w-full py-4 bg-accent text-white font-medium tracking-widest uppercase hover:bg-secondary transition-colors rounded-lg mb-4"
            >
              Proceed to Checkout
            </button>

            <Link to="/shop" className="block text-center text-sm text-gray-500 hover:text-accent transition-colors">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
