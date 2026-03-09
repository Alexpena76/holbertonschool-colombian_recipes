import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ChefHat, LogOut, MessageCircle, UtensilsCrossed } from 'lucide-react';

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-colombian-blue text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <ChefHat className="h-8 w-8 text-colombian-yellow" />
              <span className="font-bold text-xl">Colombian Recipes</span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/recipes"
                  className="flex items-center space-x-1 hover:text-colombian-yellow transition-colors"
                >
                  <UtensilsCrossed className="h-5 w-5" />
                  <span>Recipes</span>
                </Link>
                <Link
                  to="/chat"
                  className="flex items-center space-x-1 hover:text-colombian-yellow transition-colors"
                >
                  <MessageCircle className="h-5 w-5" />
                  <span>AI Chef</span>
                </Link>
                <div className="flex items-center space-x-3 ml-4 pl-4 border-l border-blue-400">
                  <span className="text-sm">Hola, {user?.name || 'Chef'}!</span>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 hover:text-colombian-yellow transition-colors"
                  >
                    <LogOut className="h-5 w-5" />
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="hover:text-colombian-yellow transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-colombian-yellow text-colombian-blue px-4 py-2 rounded-lg font-semibold hover:bg-yellow-400 transition-colors"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
