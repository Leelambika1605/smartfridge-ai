import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  Sparkles, 
  LogOut, 
  User, 
  Refrigerator as FridgeIcon, 
  LayoutDashboard,
  LogIn,
  UserPlus
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Navbar() {
  const { user, isAuthenticated, logout, activeFridge } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-white flex items-center gap-1">
              SmartFridge <span className="text-cyan-400">AI</span>
            </span>
            <span className="text-[10px] text-slate-400 block -mt-1 font-mono uppercase tracking-wider">
              Autonomous Manager
            </span>
          </div>
        </Link>

        {/* Center Navigation Links */}
        {isAuthenticated && (
          <nav className="hidden md:flex items-center space-x-1">
            <Link
              to="/dashboard"
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-2 ${
                isActive('/dashboard') 
                  ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' 
                  : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
              }`}
            >
              <LayoutDashboard className="h-4 w-4" />
              <span>Dashboard</span>
            </Link>
          </nav>
        )}

        {/* Right Auth / Profile Controls */}
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <div className="flex items-center gap-3">
              {/* Active Fridge Indicator */}
              {activeFridge && (
                <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-800 border border-slate-700/60 text-xs text-slate-300">
                  <FridgeIcon className="h-3.5 w-3.5 text-cyan-400" />
                  <span className="max-w-[130px] truncate font-medium">{activeFridge.name}</span>
                </div>
              )}

              {/* User Profile Pill */}
              <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700 text-xs text-slate-200">
                <User className="h-3.5 w-3.5 text-cyan-400" />
                <span className="font-medium max-w-[120px] truncate">
                  {user.full_name || user.email}
                </span>
              </div>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition"
                title="Log Out"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800/80 hover:bg-slate-800 text-xs font-medium text-slate-200 transition flex items-center gap-1.5"
              >
                <LogIn className="h-3.5 w-3.5 text-slate-400" />
                <span>Log In</span>
              </Link>
              <Link
                to="/register"
                className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-xs font-semibold text-white shadow-md shadow-cyan-500/20 transition flex items-center gap-1.5"
              >
                <UserPlus className="h-3.5 w-3.5" />
                <span>Get Started</span>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
