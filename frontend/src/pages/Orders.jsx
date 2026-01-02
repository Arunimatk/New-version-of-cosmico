import React, { useEffect, useState } from 'react';
import api from '../api';
import { Package, Clock, CheckCircle, AlertCircle, Calendar } from 'lucide-react';
import { Link } from 'react-router-dom';

const Orders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = async () => {
        try {
            const response = await api.get('orders/');
            // Sort by latest first
            const sortedOrders = response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            setOrders(sortedOrders);
            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch orders", err);
            setError("Failed to load your orders.");
            setLoading(false);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'Completed': return 'text-green-600 bg-green-50 border-green-200';
            case 'Delivered': return 'text-green-600 bg-green-50 border-green-200';
            case 'Shipped': return 'text-blue-600 bg-blue-50 border-blue-200';
            case 'Processing': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
            case 'Cancelled': return 'text-red-600 bg-red-50 border-red-200';
            default: return 'text-gray-600 bg-gray-50 border-gray-200';
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    if (loading) return <div className="pt-32 text-center">Loading orders...</div>;

    if (error) return <div className="pt-32 text-center text-red-500">{error}</div>;

    if (orders.length === 0) {
        return (
            <div className="pt-32 px-4 max-w-7xl mx-auto min-h-screen text-center">
                <Package size={64} className="mx-auto text-gray-300 mb-6" />
                <h2 className="text-3xl font-serif text-secondary mb-4">No Orders Yet</h2>
                <p className="text-gray-500 mb-8">You haven't placed any orders yet.</p>
                <Link to="/shop" className="px-8 py-3 bg-accent text-white uppercase tracking-widest hover:bg-secondary transition-colors rounded">
                    Start Shopping
                </Link>
            </div>
        );
    }

    return (
        <div className="pt-24 pb-16 px-4 max-w-5xl mx-auto min-h-screen">
            <h1 className="text-3xl font-serif text-accent mb-10">My Orders</h1>

            <div className="space-y-6">
                {orders.map((order) => (
                    <div key={order.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
                        {/* Order Header */}
                        <div className="bg-gray-50 p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-gray-100">
                            <div>
                                <p className="text-sm text-gray-500 mb-1 flex items-center gap-2">
                                    <Calendar size={14} />
                                    {formatDate(order.created_at)}
                                </p>
                                <p className="font-mono text-xs text-gray-400">Order ID: #{order.id}</p>
                            </div>
                            <div className="flex flex-col md:items-end">
                                <span className={`px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider border mb-2 ${getStatusColor(order.status || order.payment_status)}`}>
                                    {order.status || order.payment_status || 'Pending'}
                                </span>
                                <span className="font-medium text-secondary">Total: ${parseFloat(order.total_price).toFixed(2)}</span>
                            </div>
                        </div>

                        {/* Order Items */}
                        <div className="p-6">
                            <div className="space-y-4">
                                {order.items && order.items.map((item) => (
                                    <div key={item.id} className="flex justify-between items-center text-sm">
                                        <div className="flex items-center gap-2">
                                            <span className="w-2 h-2 rounded-full bg-accent/20"></span>
                                            <span className="font-medium text-gray-700">{item.product_name || item.product?.name}</span>
                                            <span className="text-gray-400">x{item.quantity}</span>
                                        </div>
                                        <span className="text-gray-600">${parseFloat(item.price).toFixed(2)}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Footer / Actions */}
                        <div className="bg-gray-50 px-6 py-4 border-t border-gray-100 flex justify-between items-center text-xs text-gray-500">
                            <div className="flex gap-4">
                                <span>Method: {order.payment_method}</span>
                                {order.transaction_id && <span>Txn: {order.transaction_id}</span>}
                            </div>
                            {/* Future: Track Order button */}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Orders;
