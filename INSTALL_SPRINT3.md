# Sprint 3 Installation Guide

## What's Included

### Frontend (React + Vite + Tailwind)
- `frontend/` - Complete React application
  - `src/App.jsx` - Main app with routing
  - `src/pages/` - All page components
    - `HomePage.jsx` - Landing page
    - `LoginPage.jsx` - Login form
    - `RegisterPage.jsx` - Registration form
    - `RecipesPage.jsx` - Recipe list with search/filter
    - `RecipeDetailPage.jsx` - Single recipe view
    - `ChatPage.jsx` - AI assistant chat interface
  - `src/components/Navbar.jsx` - Navigation bar
  - `src/context/AuthContext.jsx` - Authentication state
  - `src/services/api.js` - API client

### Docker & Deployment
- `docker-compose.yml` - Updated with frontend service
- `docker-compose.prod.yml` - Production config (uses RDS)
- `aws/AWS_DEPLOYMENT.md` - Complete AWS deployment guide

---

## Installation Steps

### Step 1: Copy Frontend Folder

```bash
# From the extracted sprint3 folder
cp -r frontend ~/holbertonschool-colombian_recipes/
```

### Step 2: Update docker-compose.yml

```bash
cp docker-compose.yml ~/holbertonschool-colombian_recipes/
```

### Step 3: Copy Production Files (for AWS deployment)

```bash
cp docker-compose.prod.yml ~/holbertonschool-colombian_recipes/
mkdir -p ~/holbertonschool-colombian_recipes/aws
cp aws/AWS_DEPLOYMENT.md ~/holbertonschool-colombian_recipes/aws/
```

---

## Running Locally

### Option A: Full Stack with Docker

```bash
cd ~/holbertonschool-colombian_recipes
sudo docker-compose down
sudo docker-compose up -d --build
```

Then visit:
- Frontend: http://localhost:3000
- API: http://localhost:5000

### Option B: Frontend Development Mode

```bash
cd ~/holbertonschool-colombian_recipes/frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Then visit: http://localhost:5173

(Make sure the API is running on port 5000)

---

## Project Structure After Sprint 3

```
holbertonschool-colombian_recipes/
├── api/                          # Flask Backend
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── Dockerfile
│   └── init.sql
├── frontend/                     # React Frontend (NEW)
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   └── services/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── aws/                          # AWS Deployment (NEW)
│   └── AWS_DEPLOYMENT.md
├── docker-compose.yml            # Updated with frontend
├── docker-compose.prod.yml       # Production config (NEW)
├── .env
└── README.md
```

---

## Features

### Frontend Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Landing page with features |
| Login | `/login` | User authentication |
| Register | `/register` | New user signup |
| Recipes | `/recipes` | Browse all recipes |
| Recipe Detail | `/recipes/:id` | View single recipe |
| AI Chat | `/chat` | General cooking assistant |
| AI Chat (Recipe) | `/chat/:recipeId` | Recipe-specific help |

### Frontend Features
- 🔐 JWT Authentication
- 🔍 Recipe search & filtering
- 📱 Responsive design
- 🎨 Colombian flag colors theme
- 🤖 AI chat interface
- ⚡ Fast Vite build

---

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api/v1
```

### Backend (.env) - Already configured from Sprint 2
```env
FLASK_ENV=development
JWT_SECRET_KEY=your-secret
DATABASE_URL=mysql+pymysql://...
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
GROQ_API_KEY=...
```

---

## Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### CORS errors
Make sure the API allows your frontend origin in `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Docker build fails
```bash
sudo docker-compose down
sudo docker system prune -f
sudo docker-compose up -d --build
```

---

## Next Steps

1. ✅ Test the frontend locally
2. ✅ Push to GitHub
3. 🚀 Deploy to AWS (see aws/AWS_DEPLOYMENT.md)
4. 📝 Add more recipes
5. 🎨 Customize the design
