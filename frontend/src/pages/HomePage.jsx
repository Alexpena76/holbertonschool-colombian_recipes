import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { ChefHat, MessageCircle, Clock, Users } from 'lucide-react';
import { recipesAPI } from '../services/api';
import { useLanguage } from '../context/LanguageContext';

const HomePage = () => {
  const [featuredRecipes, setFeaturedRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const { t } = useLanguage();

  useEffect(() => {
    const fetchFeaturedRecipes = async () => {
      try {
        const response = await recipesAPI.getAll({ limit: 3 });
        setFeaturedRecipes(response.data.data?.recipes || []);
      } catch (error) {
        console.error('Error fetching recipes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedRecipes();
  }, []);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-800 via-blue-700 to-yellow-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <ChefHat className="h-20 w-20 mx-auto mb-6 text-yellow-400" />
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              {t('home.title')}
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto text-blue-100">
              {t('home.subtitle')}
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/recipes"
                className="bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-bold py-3 px-8 rounded-lg text-lg transition transform hover:scale-105"
              >
                {t('home.exploreButton')}
              </Link>
              <Link
                to="/chat"
                className="bg-white hover:bg-gray-100 text-blue-800 font-bold py-3 px-8 rounded-lg text-lg transition transform hover:scale-105 flex items-center justify-center gap-2"
              >
                <MessageCircle className="h-5 w-5" />
                {t('home.chatButton')}
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Recipes Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              {t('home.featuredTitle')}
            </h2>
            <p className="text-lg text-gray-600">
              {t('home.featuredSubtitle')}
            </p>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-800 mx-auto"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredRecipes.map((recipe) => (
                <div
                  key={recipe.id}
                  className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition transform hover:-translate-y-1"
                >
                  <div className="h-48 bg-gradient-to-br from-yellow-400 to-red-500 flex items-center justify-center">
                    <ChefHat className="h-20 w-20 text-white opacity-80" />
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                      {recipe.name}
                    </h3>
                    <p className="text-gray-600 mb-4 line-clamp-2">
                      {recipe.description}
                    </p>
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>{recipe.prep_time + recipe.cook_time} {t('recipes.minutes')}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="h-4 w-4" />
                        <span>{recipe.servings} {t('recipes.servings')}</span>
                      </div>
                    </div>
                    <Link
                      to={`/recipes/${recipe.id}`}
                      className="block w-full text-center bg-blue-800 hover:bg-blue-900 text-white font-semibold py-2 rounded-lg transition"
                    >
                      {t('home.viewRecipe')}
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link
              to="/recipes"
              className="inline-block bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-bold py-3 px-8 rounded-lg text-lg transition"
            >
              {t('home.viewAll')}
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;