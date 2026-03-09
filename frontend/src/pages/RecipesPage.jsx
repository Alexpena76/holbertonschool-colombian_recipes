import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { recipesAPI, categoriesAPI } from '../services/api';
import { Search, Clock, Users, ChefHat, Filter } from 'lucide-react';

const difficultyColors = {
  easy: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  hard: 'bg-red-100 text-red-800',
};

const difficultyEmoji = {
  easy: '🟢',
  medium: '🟡',
  hard: '🔴',
};

export default function RecipesPage() {
  const [recipes, setRecipes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');

  useEffect(() => {
    fetchData();
  }, [selectedCategory, selectedDifficulty]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (selectedDifficulty) params.difficulty = selectedDifficulty;

      const [recipesRes, categoriesRes] = await Promise.all([
        recipesAPI.getAll(params),
        categoriesAPI.getAll(),
      ]);

      setRecipes(recipesRes.data.data.recipes || []);
      setCategories(categoriesRes.data.data.categories || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      fetchData();
      return;
    }

    try {
      setLoading(true);
      const response = await recipesAPI.search(searchQuery);
      setRecipes(response.data.data.recipes || []);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('');
    setSelectedDifficulty('');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Colombian Recipes</h1>
        <p className="text-gray-600">Discover authentic dishes from Colombia 🇨🇴</p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-8">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <form onSubmit={handleSearch} className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search recipes or ingredients..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-colombian-blue focus:border-colombian-blue"
              />
            </div>
          </form>

          {/* Category Filter */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="pl-10 pr-8 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-colombian-blue focus:border-colombian-blue appearance-none bg-white"
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.name}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty Filter */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-colombian-blue focus:border-colombian-blue appearance-none bg-white"
          >
            <option value="">All Difficulties</option>
            <option value="easy">🟢 Easy</option>
            <option value="medium">🟡 Medium</option>
            <option value="hard">🔴 Hard</option>
          </select>

          {/* Clear Filters */}
          {(searchQuery || selectedCategory || selectedDifficulty) && (
            <button
              onClick={clearFilters}
              className="px-4 py-3 text-gray-600 hover:text-gray-900 font-medium"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Recipe Grid */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-colombian-blue"></div>
        </div>
      ) : recipes.length === 0 ? (
        <div className="text-center py-12">
          <ChefHat className="mx-auto h-16 w-16 text-gray-300 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No recipes found</h3>
          <p className="text-gray-500">Try adjusting your search or filters</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <Link
              key={recipe.id}
              to={`/recipes/${recipe.id}`}
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow group"
            >
              {/* Recipe Image Placeholder */}
              <div className="h-48 bg-gradient-to-br from-colombian-yellow to-orange-400 flex items-center justify-center relative overflow-hidden">
                <span className="text-6xl group-hover:scale-110 transition-transform">
                  {recipe.category === 'breakfast' ? '🍳' :
                   recipe.category === 'lunch' ? '🍲' :
                   recipe.category === 'dinner' ? '🍖' :
                   recipe.category === 'dessert' ? '🍮' :
                   recipe.category === 'snack' ? '🫓' : '🍽️'}
                </span>
                <div className="absolute top-3 right-3">
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${difficultyColors[recipe.difficulty]}`}>
                    {difficultyEmoji[recipe.difficulty]} {recipe.difficulty}
                  </span>
                </div>
              </div>

              {/* Recipe Info */}
              <div className="p-5">
                <h3 className="font-bold text-lg mb-2 text-gray-900 group-hover:text-colombian-blue transition-colors">
                  {recipe.name}
                </h3>
                {recipe.name_es && (
                  <p className="text-sm text-gray-500 italic mb-3">{recipe.name_es}</p>
                )}
                
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  {recipe.prep_time && (
                    <div className="flex items-center space-x-1">
                      <Clock className="h-4 w-4" />
                      <span>{recipe.prep_time + (recipe.cook_time || 0)} min</span>
                    </div>
                  )}
                  {recipe.servings && (
                    <div className="flex items-center space-x-1">
                      <Users className="h-4 w-4" />
                      <span>{recipe.servings} servings</span>
                    </div>
                  )}
                </div>

                {recipe.region && (
                  <p className="mt-3 text-xs text-gray-500">
                    📍 {recipe.region}
                  </p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
