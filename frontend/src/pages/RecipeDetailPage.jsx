import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Users, ChefHat, Minus, Plus } from 'lucide-react';
import { recipesAPI } from '../services/api';
import { useLanguage } from '../context/LanguageContext';

const RecipeDetailPage = () => {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [servings, setServings] = useState(4);
  const [originalServings, setOriginalServings] = useState(4);
  const { t } = useLanguage();

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const response = await recipesAPI.getById(id);
        const recipeData = response.data.data?.recipe;
        setRecipe(recipeData);
        setServings(recipeData?.servings || 4);
        setOriginalServings(recipeData?.servings || 4);
      } catch (error) {
        console.error('Error fetching recipe:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [id]);

  const adjustQuantity = (quantity) => {
    if (!quantity) return quantity;
    const adjusted = (quantity * servings) / originalServings;
    return adjusted % 1 === 0 ? adjusted : adjusted.toFixed(1);
  };

  const getDifficultyLabel = (difficulty) => {
    const labels = {
      easy: t('recipes.easy'),
      medium: t('recipes.medium'),
      hard: t('recipes.hard'),
    };
    return labels[difficulty] || difficulty;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-800"></div>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <ChefHat className="h-16 w-16 text-gray-400 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">{t('recipeDetail.notFound')}</h2>
        <p className="text-gray-600 mb-4">{t('recipeDetail.notFoundMessage')}</p>
        <Link to="/recipes" className="text-blue-800 hover:text-blue-900 font-semibold">
          {t('recipeDetail.backToRecipes')}
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Button */}
        <Link
          to="/recipes"
          className="inline-flex items-center text-blue-800 hover:text-blue-900 mb-6"
        >
          <ArrowLeft className="h-5 w-5 mr-1" />
          {t('recipeDetail.backToRecipes')}
        </Link>

        {/* Recipe Header */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-8">
          <div className="h-64 bg-gradient-to-br from-yellow-400 to-red-500 flex items-center justify-center overflow-hidden">
            {recipe.image_url ? (
              <img 
                src={recipe.image_url} 
                alt={recipe.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <ChefHat className="h-32 w-32 text-white opacity-80" />
            )}
          </div>
          <div className="p-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{recipe.name}</h1>
            <p className="text-gray-600 mb-4">{recipe.description}</p>
            
            {/* Recipe Meta */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-4 border-t border-b border-gray-200">
              <div className="text-center">
                <Clock className="h-6 w-6 mx-auto text-blue-800 mb-1" />
                <p className="text-sm text-gray-500">{t('recipeDetail.prepTime')}</p>
                <p className="font-semibold">{recipe.prep_time_minutes} {t('recipeDetail.minutes')}</p>
              </div>
              <div className="text-center">
                <Clock className="h-6 w-6 mx-auto text-blue-800 mb-1" />
                <p className="text-sm text-gray-500">{t('recipeDetail.cookTime')}</p>
                <p className="font-semibold">{recipe.cook_time_minutes} {t('recipeDetail.minutes')}</p>
              </div>
              <div className="text-center">
                <Users className="h-6 w-6 mx-auto text-blue-800 mb-1" />
                <p className="text-sm text-gray-500">{t('recipeDetail.servings')}</p>
                <p className="font-semibold">{recipe.servings}</p>
              </div>
              <div className="text-center">
                <ChefHat className="h-6 w-6 mx-auto text-blue-800 mb-1" />
                <p className="text-sm text-gray-500">{t('recipeDetail.difficulty')}</p>
                <p className="font-semibold capitalize">{getDifficultyLabel(recipe.difficulty)}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Ingredients */}
          <div className="md:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">{t('recipeDetail.ingredients')}</h2>
              
              {/* Servings Adjuster */}
              <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3 mb-4">
                <span className="text-sm font-medium text-gray-700">{t('recipeDetail.servings')}</span>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setServings(Math.max(1, servings - 1))}
                    className="p-1 rounded-full bg-blue-100 text-blue-800 hover:bg-blue-200"
                  >
                    <Minus className="h-4 w-4" />
                  </button>
                  <span className="font-bold text-lg w-8 text-center">{servings}</span>
                  <button
                    onClick={() => setServings(servings + 1)}
                    className="p-1 rounded-full bg-blue-100 text-blue-800 hover:bg-blue-200"
                  >
                    <Plus className="h-4 w-4" />
                  </button>
                </div>
              </div>

              <ul className="space-y-2">
                {recipe.ingredients?.map((ingredient, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-2 h-2 bg-yellow-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    <span>
                      <strong>{adjustQuantity(ingredient.amount)} {ingredient.unit}</strong>{' '}
                      {ingredient.name}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Instructions */}
          <div className="md:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">{t('recipeDetail.instructions')}</h2>
              <ol className="space-y-4">
                {recipe.steps?.map((step, index) => (
                  <li key={index} className="flex">
                    <span className="flex-shrink-0 w-8 h-8 bg-blue-800 text-white rounded-full flex items-center justify-center font-bold mr-4">
                      {step.step_number}
                    </span>
                    <p className="text-gray-700 pt-1">{step.instruction}</p>
                  </li>
                ))}
              </ol>
            </div>

            {/* AI Assistant Link */}
            <Link
              to="/chat"
              className="mt-6 block w-full text-center bg-yellow-500 hover:bg-yellow-600 text-blue-900 font-bold py-3 rounded-lg transition"
            >
              {t('recipeDetail.askAI')}
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetailPage;