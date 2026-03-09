import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ChefHat, Sparkles, BookOpen, MessageCircle } from 'lucide-react';

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-colombian-blue text-white py-20 overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-full h-1/2 bg-colombian-yellow"></div>
          <div className="absolute bottom-0 left-0 w-full h-1/4 bg-colombian-red"></div>
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <ChefHat className="h-20 w-20 mx-auto mb-6 text-colombian-yellow" />
          <h1 className="text-5xl font-bold mb-4">
            Authentic Colombian Recipes
          </h1>
          <p className="text-xl mb-8 text-blue-100 max-w-2xl mx-auto">
            Discover the rich flavors of Colombia with our collection of traditional recipes, 
            powered by AI to help you cook like a true Colombian abuela.
          </p>
          {isAuthenticated ? (
            <div className="flex justify-center space-x-4">
              <Link
                to="/recipes"
                className="bg-colombian-yellow text-colombian-blue px-8 py-3 rounded-lg font-bold text-lg hover:bg-yellow-400 transition-colors"
              >
                Browse Recipes
              </Link>
              <Link
                to="/chat"
                className="bg-white text-colombian-blue px-8 py-3 rounded-lg font-bold text-lg hover:bg-gray-100 transition-colors"
              >
                Ask AI Chef
              </Link>
            </div>
          ) : (
            <div className="flex justify-center space-x-4">
              <Link
                to="/register"
                className="bg-colombian-yellow text-colombian-blue px-8 py-3 rounded-lg font-bold text-lg hover:bg-yellow-400 transition-colors"
              >
                Get Started Free
              </Link>
              <Link
                to="/login"
                className="bg-transparent border-2 border-white px-8 py-3 rounded-lg font-bold text-lg hover:bg-white hover:text-colombian-blue transition-colors"
              >
                Login
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Why Colombian Recipes?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="text-center p-6 rounded-xl bg-gray-50 hover:shadow-lg transition-shadow">
              <div className="bg-colombian-yellow rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <BookOpen className="h-8 w-8 text-colombian-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-800">Authentic Recipes</h3>
              <p className="text-gray-600">
                Traditional Colombian recipes passed down through generations, 
                from Bandeja Paisa to Ajiaco Bogotano.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="text-center p-6 rounded-xl bg-gray-50 hover:shadow-lg transition-shadow">
              <div className="bg-colombian-red rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-800">AI-Powered Help</h3>
              <p className="text-gray-600">
                Get instant cooking tips, substitutions, and troubleshooting 
                from our AI assistant trained on Colombian cuisine.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="text-center p-6 rounded-xl bg-gray-50 hover:shadow-lg transition-shadow">
              <div className="bg-colombian-blue rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <MessageCircle className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-800">Interactive Cooking</h3>
              <p className="text-gray-600">
                Chat with our AI chef while you cook. Ask questions, get tips, 
                and save your conversations for later.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Featured Recipes Preview */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Featured Recipes 🇨🇴
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Bandeja Paisa */}
            <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
              <div className="h-48 bg-gradient-to-br from-colombian-yellow to-orange-400 flex items-center justify-center">
                <span className="text-6xl">🍳</span>
              </div>
              <div className="p-6">
                <h3 className="font-bold text-xl mb-2">Bandeja Paisa</h3>
                <p className="text-gray-600 text-sm mb-4">
                  The iconic Colombian platter from Antioquia with beans, rice, meat, and more.
                </p>
                <span className="inline-block bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                  Hard • 2.5 hrs
                </span>
              </div>
            </div>

            {/* Ajiaco */}
            <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
              <div className="h-48 bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
                <span className="text-6xl">🍲</span>
              </div>
              <div className="p-6">
                <h3 className="font-bold text-xl mb-2">Ajiaco Bogotano</h3>
                <p className="text-gray-600 text-sm mb-4">
                  Hearty chicken soup from Bogotá with three types of potatoes and guascas.
                </p>
                <span className="inline-block bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">
                  Medium • 2 hrs
                </span>
              </div>
            </div>

            {/* Arepas */}
            <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
              <div className="h-48 bg-gradient-to-br from-amber-300 to-yellow-400 flex items-center justify-center">
                <span className="text-6xl">🫓</span>
              </div>
              <div className="p-6">
                <h3 className="font-bold text-xl mb-2">Colombian Arepas</h3>
                <p className="text-gray-600 text-sm mb-4">
                  Classic corn cakes that are a staple of Colombian breakfast and snacks.
                </p>
                <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                  Easy • 25 min
                </span>
              </div>
            </div>
          </div>

          {!isAuthenticated && (
            <div className="text-center mt-12">
              <Link
                to="/register"
                className="inline-block bg-colombian-blue text-white px-8 py-3 rounded-lg font-bold text-lg hover:bg-blue-800 transition-colors"
              >
                Sign Up to See All Recipes
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-colombian-blue text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm text-blue-300 mt-2">
            © 2026 Colombian Recipes API • Holberton School Project
          </p>
        </div>
      </footer>
    </div>
  );
}
