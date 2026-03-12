import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Menu, X, ChefHat, Globe } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const { language, toggleLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsOpen(false);
  };

  return (
    <nav className="bg-blue-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <ChefHat className="h-8 w-8 text-yellow-400" />
            <span className="font-bold text-xl">
              {language === 'en' ? 'Colombian' : 'Recetas'}
              <span className="text-yellow-400"> {language === 'en' ? 'Recipes' : 'Colombianas'}</span>
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/" className="hover:text-yellow-400 transition px-3 py-2">
              {t('nav.home')}
            </Link>
            <Link to="/recipes" className="hover:text-yellow-400 transition px-3 py-2">
              {t('nav.recipes')}
            </Link>
            {user && (
              <Link to="/chat" className="hover:text-yellow-400 transition px-3 py-2">
                {t('nav.chat')}
              </Link>
            )}
            
            {/* Language Toggle */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-1 bg-blue-700 hover:bg-blue-600 px-3 py-2 rounded-lg transition"
              title={language === 'en' ? 'Cambiar a Español' : 'Switch to English'}
            >
              <Globe className="h-4 w-4" />
              <span className="font-medium">{language === 'en' ? 'ES' : 'EN'}</span>
            </button>

            {user ? (
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition"
              >
                {t('nav.logout')}
              </button>
            ) : (
              <>
                <Link
                  to="/login"
                  className="hover:text-yellow-400 transition px-3 py-2"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  className="bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-semibold px-4 py-2 rounded-lg transition"
                >
                  {t('nav.signUp')}
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center space-x-2">
            {/* Language Toggle Mobile */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-1 bg-blue-700 hover:bg-blue-600 px-2 py-1 rounded transition"
            >
              <Globe className="h-4 w-4" />
              <span className="text-sm font-medium">{language === 'en' ? 'ES' : 'EN'}</span>
            </button>
            
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-white hover:text-yellow-400"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4">
            <div className="flex flex-col space-y-2">
              <Link
                to="/"
                onClick={() => setIsOpen(false)}
                className="hover:bg-blue-700 px-3 py-2 rounded"
              >
                {t('nav.home')}
              </Link>
              <Link
                to="/recipes"
                onClick={() => setIsOpen(false)}
                className="hover:bg-blue-700 px-3 py-2 rounded"
              >
                {t('nav.recipes')}
              </Link>
              {user && (
                <Link
                  to="/chat"
                  onClick={() => setIsOpen(false)}
                  className="hover:bg-blue-700 px-3 py-2 rounded"
                >
                  {t('nav.chat')}
                </Link>
              )}
              {user ? (
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 px-3 py-2 rounded text-left"
                >
                  {t('nav.logout')}
                </button>
              ) : (
                <>
                  <Link
                    to="/login"
                    onClick={() => setIsOpen(false)}
                    className="hover:bg-blue-700 px-3 py-2 rounded"
                  >
                    {t('nav.login')}
                  </Link>
                  <Link
                    to="/register"
                    onClick={() => setIsOpen(false)}
                    className="bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-semibold px-3 py-2 rounded"
                  >
                    {t('nav.signUp')}
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
