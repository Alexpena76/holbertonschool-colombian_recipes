import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { recipesAPI } from '../services/api';
import { Clock, Users, ChefHat, MessageCircle, ArrowLeft, Minus, Plus } from 'lucide-react';

const difficultyColors = {
  easy: 'bg-green-100 text-green-800 border-green-200',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  hard: 'bg-red-100 text-red-800 border-red-200',
};

export default function RecipeDetailPage() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [servings, setServings] = useState(4);
  const [originalServings, setOriginalServings] = useState(4);

  useEffect(() => {
    fetchRecipe();
  }, [id]);

  const fetchRecipe = async () => {
    try {
      setLoading(true);
      const response = await recipesAPI.getById(id);
      const recipeData = response.data.data;
      setRecipe(recipeData);
      setServings(recipeData.servings || 4);
      setOriginalServings(recipeData.servings || 4);
    } catch (error) {
      console.error('Error fetching recipe:', error);
    } finally {
      setLoading(false);
    }
  };

  const adjustServings = (delta) => {
    const newServings = Math.max(1, servings + delta);
    setServings(newServings);
  };

  const scaleAmount = (amount) => {
    if (!amount) return amount;
    const scaled = (amount * servings) / originalServings;
    return Number.isInteger(scaled) ? scaled : scaled.toFixed(1);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-colombian-blue"></div>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <ChefHat className="mx-auto h-16 w-16 text-gray-300 mb-4" />
          <h2 className="text-xl font-semibold text-gray-900">Recipe not found</h2>
          <Link to="/recipes" className="text-colombian-blue hover:underline mt-2 inline-block">
            Back to recipes
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/recipes"
        className="inline-flex items-center text-gray-600 hover:text-colombian-blue mb-6"
      >
        <ArrowLeft className="h-5 w-5 mr-1" />
        Back to recipes
      </Link>

      {/* Recipe Header */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden mb-8">
        {/* Hero Image Placeholder */}
        <div className="h-64 bg-gradient-to-br from-colombian-yellow via-orange-400 to-colombian-red flex items-center justify-center">
          <span className="text-8xl">
            {recipe.category === 'breakfast' ? '🍳' :
             recipe.category === 'lunch' ? '🍲' :
             recipe.category === 'dinner' ? '🍖' :
             recipe.category === 'dessert' ? '🍮' :
             recipe.category === 'snack' ? '🫓' : '🍽️'}
          </span>
        </div>

        <div className="p-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-1">{recipe.name}</h1>
              {recipe.name_es && (
                <p className="text-lg text-gray-500 italic">{recipe.name_es}</p>
              )}
            </div>
            <span className={`px-4 py-2 rounded-full font-medium border ${difficultyColors[recipe.difficulty]}`}>
              {recipe.difficulty === 'easy' ? '🟢' : recipe.difficulty === 'medium' ? '🟡' : '🔴'} {recipe.difficulty}
            </span>
          </div>

          {recipe.description && (
            <p className="mt-4 text-gray-600">{recipe.description}</p>
          )}

          {/* Meta Info */}
          <div className="flex flex-wrap gap-6 mt-6 pt-6 border-t border-gray-200">
            {recipe.prep_time && (
              <div className="flex items-center space-x-2 text-gray-600">
                <Clock className="h-5 w-5 text-colombian-blue" />
                <div>
                  <p className="text-sm text-gray-500">Prep Time</p>
                  <p className="font-semibold">{recipe.prep_time} min</p>
                </div>
              </div>
            )}
            {recipe.cook_time && (
              <div className="flex items-center space-x-2 text-gray-600">
                <Clock className="h-5 w-5 text-colombian-red" />
                <div>
                  <p className="text-sm text-gray-500">Cook Time</p>
                  <p className="font-semibold">{recipe.cook_time} min</p>
                </div>
              </div>
            )}
            {recipe.region && (
              <div className="flex items-center space-x-2 text-gray-600">
                <span className="text-xl">📍</span>
                <div>
                  <p className="text-sm text-gray-500">Region</p>
                  <p className="font-semibold">{recipe.region}</p>
                </div>
              </div>
            )}
          </div>

          {/* AI Assistant Button */}
          <div className="mt-6">
            <Link
              to={`/chat/${recipe.id}`}
              className="inline-flex items-center space-x-2 bg-colombian-blue text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-800 transition-colors"
            >
              <MessageCircle className="h-5 w-5" />
              <span>Ask AI Chef for Help</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Ingredients */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Ingredients</h2>
          
          {/* Servings Adjuster */}
          <div className="flex items-center space-x-3">
            <Users className="h-5 w-5 text-gray-500" />
            <button
              onClick={() => adjustServings(-1)}
              className="p-1 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            >
              <Minus className="h-4 w-4" />
            </button>
            <span className="font-semibold text-lg w-8 text-center">{servings}</span>
            <button
              onClick={() => adjustServings(1)}
              className="p-1 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            >
              <Plus className="h-4 w-4" />
            </button>
            <span className="text-gray-500">servings</span>
          </div>
        </div>

        {recipe.ingredients && recipe.ingredients.length > 0 ? (
          <ul className="grid md:grid-cols-2 gap-3">
            {recipe.ingredients.map((ing, index) => (
              <li key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <span className="text-colombian-yellow">•</span>
                <span>
                  <strong className="text-colombian-blue">{scaleAmount(ing.amount)}</strong>
                  {ing.unit && ` ${ing.unit}`} {ing.name}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No ingredients listed</p>
        )}
      </div>

      {/* Steps */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Instructions</h2>

        {recipe.steps && recipe.steps.length > 0 ? (
          <ol className="space-y-6">
            {recipe.steps.map((step, index) => (
              <li key={index} className="flex space-x-4">
                <div className="flex-shrink-0 w-10 h-10 bg-colombian-blue text-white rounded-full flex items-center justify-center font-bold">
                  {step.step_number || index + 1}
                </div>
                <div className="flex-1 pt-2">
                  <p className="text-gray-700 leading-relaxed">{step.instruction}</p>
                  {step.instruction_es && (
                    <p className="text-gray-500 italic mt-2 text-sm">{step.instruction_es}</p>
                  )}
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <p className="text-gray-500">No instructions listed</p>
        )}
      </div>

      {/* Bottom CTA */}
      <div className="mt-8 text-center">
        <p className="text-gray-600 mb-4">Need help while cooking?</p>
        <Link
          to={`/chat/${recipe.id}`}
          className="inline-flex items-center space-x-2 bg-colombian-yellow text-colombian-blue px-8 py-4 rounded-lg font-bold text-lg hover:bg-yellow-400 transition-colors"
        >
          <MessageCircle className="h-6 w-6" />
          <span>Chat with AI Chef</span>
        </Link>
      </div>
    </div>
  );
}
