import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { Truck, Smartphone, Check, Loader } from 'lucide-react';

const Checkout = () => {
    const navigate = useNavigate();
    const [cartItems, setCartItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [address, setAddress] = useState({ fullName: '', street: '', city: '', zipCode: '', country: '' });
    const [paymentMethod, setPaymentMethod] = useState('COD');
    const [upiId, setUpiId] = useState('');
    const [isProcessing, setIsProcessing] = useState(false);

    useEffect(() => { fetchCart(); }, []);

    const fetchCart = async () => {
        try {
            const response = await api.get('cart/');
            if (response.data && Array.isArray(response.data.items)) setCartItems(response.data.items);
            else setCartItems([]);
        } catch (err) { console.error("Failed to fetch cart", err); }
        finally { setLoading(false); }
    };

    const calculateTotal = () => {
        const sub = cartItems.reduce((acc, item) => acc + (parseFloat(item.product.price) * item.quantity), 0);
        return sub + (sub > 100 ? 0 : 10);
    };

    const handlePlaceOrder = async (e) => {
        e.preventDefault();
        setIsProcessing(true);

        // Simulate payment processing delay
        if (paymentMethod !== 'COD') {
            await new Promise(resolve => setTimeout(resolve, 2000));
        }

        try {
            const subtotal = calculateTotal(); // Naive calculation, mainly for display. Backend recalculates.
            // Create pending orders for each item (or single order logic if backend supports it)
            // NOTE: Current backend logic creates one order per item if we loop, OR one bulk order if we send no product_id (cart checkout mode).
            // Based on views.py: OrderViewSet.create without product_id cheks cart and creates ONE order for all items.
            // This is MUCH better. Let's use that.

            const payload = {
                shipping_address: `${address.fullName}, ${address.street}, ${address.city}, ${address.zipCode}, ${address.country}`,
                full_name: address.fullName,
                payment_method: paymentMethod,
                transaction_id: paymentMethod === 'COD' ? null : `TXN_${Date.now()}_${Math.floor(Math.random() * 1000)}`
            };

            await api.post('orders/', payload);

            navigate('/order-success');
        } catch (error) {
            console.error("Order failed", error);
            alert("Failed to place order. " + (error.response?.data?.error || ""));
            setIsProcessing(false);
        }
    };

    if (loading) return <div className="pt-32 text-center">Loading...</div>;
    if (cartItems.length === 0) return <div className="pt-32 text-center">Cart is empty.</div>;

    return (
        <div className="pt-24 pb-16 px-4 max-w-7xl mx-auto min-h-screen">
            <h1 className="text-4xl font-serif text-accent mb-12 text-center">Secure Checkout</h1>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                {/* Left Column: Details */}
                <div className="lg:col-span-7 space-y-8">

                    {/* Address Section */}
                    <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100">
                        <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                            <span className="w-8 h-8 bg-accent text-white rounded-full flex items-center justify-center text-sm">1</span>
                            Shipping Address
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <input placeholder="Full Name" className="p-3 bg-gray-50 rounded border-none focus:ring-1 focus:ring-accent" value={address.fullName} onChange={e => setAddress({ ...address, fullName: e.target.value })} />
                            <input placeholder="Street Address" className="p-3 bg-gray-50 rounded border-none focus:ring-1 focus:ring-accent" value={address.street} onChange={e => setAddress({ ...address, street: e.target.value })} />
                            <input placeholder="City" className="p-3 bg-gray-50 rounded border-none focus:ring-1 focus:ring-accent" value={address.city} onChange={e => setAddress({ ...address, city: e.target.value })} />
                            <input placeholder="Zip Code" className="p-3 bg-gray-50 rounded border-none focus:ring-1 focus:ring-accent" value={address.zipCode} onChange={e => setAddress({ ...address, zipCode: e.target.value })} />
                            <input placeholder="Country" className="p-3 bg-gray-50 rounded border-none focus:ring-1 focus:ring-accent md:col-span-2" value={address.country} onChange={e => setAddress({ ...address, country: e.target.value })} />
                        </div>
                    </div>

                    {/* Payment Section */}
                    <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100">
                        <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                            <span className="w-8 h-8 bg-accent text-white rounded-full flex items-center justify-center text-sm">2</span>
                            Payment Method
                        </h2>

                        <div className="space-y-4">
                            {/* COD Option */}
                            <label className={`flex items-center p-4 border rounded-lg cursor-pointer transition-all ${paymentMethod === 'COD' ? 'border-accent bg-accent/5' : 'border-gray-200 hover:border-accent/50'}`}>
                                <input type="radio" name="payment" value="COD" checked={paymentMethod === 'COD'} onChange={() => setPaymentMethod('COD')} className="w-5 h-5 text-accent" />
                                <div className="ml-4 flex items-center gap-3">
                                    <Truck className="text-gray-500" />
                                    <span className="font-medium">Cash on Delivery</span>
                                </div>
                            </label>

                            {/* UPI Option */}
                            <label className={`flex items-center p-4 border rounded-lg cursor-pointer transition-all ${paymentMethod === 'UPI' ? 'border-accent bg-accent/5' : 'border-gray-200 hover:border-accent/50'}`}>
                                <input type="radio" name="payment" value="UPI" checked={paymentMethod === 'UPI'} onChange={() => setPaymentMethod('UPI')} className="w-5 h-5 text-accent" />
                                <div className="ml-4 flex items-center gap-3">
                                    <Smartphone className="text-gray-500" />
                                    <span className="font-medium">UPI (PhonePe / GPay)</span>
                                </div>
                            </label>

                            {/* UPI Details */}
                            {paymentMethod === 'UPI' && (
                                <div className="ml-9 p-4 bg-gray-50 rounded-lg animate-fade-in">
                                    <p className="text-sm text-gray-500 mb-3">Scan QR code or enter UPI ID to pay</p>
                                    <input placeholder="Enter UPI ID (e.g. name@upi)" className="w-full p-3 border border-gray-200 rounded mb-3" value={upiId} onChange={e => setUpiId(e.target.value)} />
                                    <div className="h-32 bg-white flex items-center justify-center border border-dashed border-gray-300 rounded text-gray-400 text-sm">
                                        [ Demo QR Code ]
                                    </div>
                                </div>
                            )}


                        </div>
                    </div>
                </div>

                {/* Right Column: Summary */}
                <div className="lg:col-span-5">
                    <div className="bg-gray-50 p-8 rounded-xl sticky top-28">
                        <h3 className="text-xl font-serif mb-6 text-secondary">Order Summary</h3>
                        <div className="space-y-4 mb-6 max-h-60 overflow-y-auto pr-2">
                            {cartItems.map(item => (
                                <div key={item.id} className="flex justify-between text-sm py-2 border-b border-gray-200 last:border-0">
                                    <div className="flex gap-3">
                                        <div className="w-12 h-12 bg-gray-200 rounded overflow-hidden">
                                            {item.product.image && <img src={item.product.image.startsWith('http') ? item.product.image : `http://127.0.0.1:8000${item.product.image}`} className="w-full h-full object-cover" />}
                                        </div>
                                        <div>
                                            <p className="font-medium">{item.product.name}</p>
                                            <p className="text-gray-500">x{item.quantity}</p>
                                        </div>
                                    </div>
                                    <span className="font-medium">${(parseFloat(item.product.price) * item.quantity).toFixed(2)}</span>
                                </div>
                            ))}
                        </div>

                        <div className="pt-4 border-t border-gray-200 space-y-2">
                            <div className="flex justify-between text-lg font-bold text-secondary">
                                <span>Total To Pay</span>
                                <span>${calculateTotal().toFixed(2)}</span>
                            </div>
                        </div>

                        <button
                            onClick={handlePlaceOrder}
                            disabled={isProcessing}
                            className="w-full mt-8 py-4 bg-accent text-white font-bold rounded-lg hover:bg-secondary transition-all transform hover:scale-[1.02] shadow-lg disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2"
                        >
                            {isProcessing ? (
                                <>Processing <Loader className="animate-spin" size={20} /></>
                            ) : (
                                "Confirm Order"
                            )}
                        </button>

                        <p className="text-xs text-center text-gray-400 mt-4 flex items-center justify-center gap-1">
                            <Check size={12} /> SSL Secure Payment
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Checkout;
