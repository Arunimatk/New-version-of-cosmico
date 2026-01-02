import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, Heart, User, Search, Menu, X } from 'lucide-react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('token');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <nav className="fixed w-full z-50 glass-card border-b border-white border-opacity-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="text-3xl font-serif font-bold tracking-wider text-secondary">
              COSMICO
            </Link>
          </div>

          <div className="hidden md:flex space-x-8 items-center">
            <Link to="/" className="text-accent hover:text-secondary transition-colors font-medium">HOME</Link>
            <Link to="/shop" className="text-accent hover:text-secondary transition-colors font-medium">SHOP</Link>
            <Link to="/about" className="text-accent hover:text-secondary transition-colors font-medium">STORY</Link>
          </div>

          <div className="hidden md:flex items-center space-x-6">
            <button className="text-accent hover:text-secondary">
              <Search size={22} />
            </button>
            <Link to="/wishlist" className="text-accent hover:text-secondary">
              <Heart size={22} />
            </Link>
            <Link to="/cart" className="text-accent hover:text-secondary relative">
              <ShoppingBag size={22} />
              {/* Badge functionality later */}
            </Link>
            {isLoggedIn ? (
              <div className="flex items-center space-x-4">
                <span className="text-accent font-medium">
                  Hy {localStorage.getItem('username') || 'User'}
                </span>
                <Link to="/orders" className="text-accent hover:text-secondary font-medium text-sm">
                  MY ORDERS
                </Link>
                <button onClick={handleLogout} className="text-accent hover:text-secondary font-medium">
                  LOGOUT
                </button>
              </div>
            ) : (
              <Link to="/login" className="text-accent hover:text-secondary">
                <User size={22} />
              </Link>
            )}
          </div>

          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="text-accent">
              {isOpen ? <X size={28} /> : <Menu size={28} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden glass-card absolute w-full">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 text-center">
            <Link to="/" className="block px-3 py-2 text-accent hover:text-secondary font-medium" onClick={() => setIsOpen(false)}>HOME</Link>
            <Link to="/shop" className="block px-3 py-2 text-accent hover:text-secondary font-medium" onClick={() => setIsOpen(false)}>SHOP</Link>
            <Link to="/wishlist" className="block px-3 py-2 text-accent hover:text-secondary font-medium" onClick={() => setIsOpen(false)}>WISHLIST</Link>
            <Link to="/cart" className="block px-3 py-2 text-accent hover:text-secondary font-medium" onClick={() => setIsOpen(false)}>CART</Link>
            {isLoggedIn ? (
              <>
                <Link to="/orders" className="block px-3 py-2 text-accent hover:text-secondary font-medium" onClick={() => setIsOpen(false)}>MY ORDERS</Link>
                <button onClick={() => { handleLogout(); setIsOpen(false); }} className="block w-full px-3 py-2 text-accent hover:text-secondary font-medium">LOGOUT</button>
              </>
            ) : (
              <Link to="/login" className="block px-3 py-2 text-accent hover:text-secondary font-medium" onClick={() => setIsOpen(false)}>LOGIN</Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
