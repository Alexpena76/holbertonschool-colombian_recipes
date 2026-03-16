# Colombian Recipes App - 5 Minute Presentation Script

## SLIDE 1: Introduction (30 seconds)
---

**"Good [morning/afternoon], I'm Alex Peña, and today I'm presenting Colombian Recipes - a full-stack web application that brings authentic Colombian cuisine to your kitchen with the help of AI."**

**Key Points to Say:**
- This is a recipe platform featuring traditional Colombian dishes like Bandeja Paisa, Ajiaco Bogotano, and Arepas
- What makes it unique: an AI-powered cooking assistant that helps users while they cook
- Fully bilingual: English and Spanish support throughout the entire application

---

## SLIDE 2: The Problem & Solution (45 seconds)
---

**"The problem I wanted to solve:"**

- Colombian cuisine is rich and diverse, but recipes are often scattered across the internet in inconsistent formats
- Traditional recipes can be intimidating for new cooks - they need guidance while cooking
- Most recipe sites don't offer real-time help when you're stuck in the kitchen

**"My solution:"**

- A centralized platform for authentic Colombian recipes with detailed instructions
- An AI cooking assistant (powered by multiple AI providers) that can answer questions like:
  - "My beans are still hard after 2 hours, what should I do?"
  - "What can I substitute for chicharrón if I'm vegetarian?"
- Full bilingual support - toggle between English and Spanish instantly

---

## SLIDE 3: Architecture Overview (60 seconds)
---

**"Let me walk you through the technical architecture:"**

### Three-Tier Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                React + Vite + Tailwind CSS                   │
│                   (Nginx Container)                          │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST API
┌─────────────────────────▼───────────────────────────────────┐
│                        BACKEND                               │
│              Python Flask + Flask-RESTX                      │
│           JWT Authentication + CORS                          │
│                   (Python Container)                         │
└─────────────────────────┬───────────────────────────────────┘
                          │ SQLAlchemy ORM
┌─────────────────────────▼───────────────────────────────────┐
│                       DATABASE                               │
│                    MySQL 8.4 (AWS RDS)                       │
│               Managed Database Service                       │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    EXTERNAL SERVICES                         │
│         Claude API → OpenAI → Gemini → Groq                  │
│              (Multi-provider AI fallback)                    │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- **Frontend**: React 18 with Vite for fast builds, Tailwind CSS for styling, deployed in an Nginx container
- **Backend**: Python Flask REST API with 14 endpoints, JWT authentication for secure user sessions
- **Database**: MySQL on AWS RDS - fully managed, automated backups
- **AI Service**: Multi-provider architecture with fallback chain (Claude → OpenAI → Gemini → Groq)
- **Deployment**: Docker Compose orchestrating both containers on AWS EC2

---

## SLIDE 4: Key Features Demo (90 seconds)
---

**"Let me show you the key features:"**

### 1. Recipe Browsing & Filtering
- Browse all recipes with search functionality
- Filter by category (breakfast, lunch, dinner) and difficulty (easy, medium, hard)
- Each recipe shows cooking time, servings, and difficulty at a glance

### 2. Detailed Recipe View
- Full ingredients list with dynamic serving adjustment (change from 4 to 8 servings, ingredients auto-calculate)
- Step-by-step cooking instructions
- Beautiful food photography

### 3. Bilingual Support (EN/ES)
- One-click language toggle in the navbar
- Everything translates: UI, recipe descriptions, cooking instructions
- User preference saved to localStorage

### 4. AI Cooking Assistant
- Ask any question about Colombian cooking
- Context-aware: knows which recipe you're viewing
- Responds in your selected language
- Examples:
  - "What makes Ajiaco different from other soups?"
  - "How do I know when my plantains are ripe enough?"

### 5. User Authentication
- Secure registration and login
- JWT tokens for session management
- AI assistant requires login to prevent abuse

---

## SLIDE 5: Technical Deep Dive (45 seconds)
---

**"Some technical highlights I'm proud of:"**

### Backend (Flask API)
- **7 Database Models**: User, Recipe, Ingredient, Step, Category, Conversation, Message
- **14 REST Endpoints**: Full CRUD for recipes, auth, AI assistant
- **Facade Pattern**: Clean separation between routes and business logic
- **Multi-provider AI**: Automatic fallback if primary AI is unavailable

### Frontend (React)
- **Context API**: AuthContext for user state, LanguageContext for i18n
- **Axios Interceptors**: Automatic token injection and 401 handling
- **Responsive Design**: Mobile-first with Tailwind CSS

### DevOps
- **Docker Compose**: Two-container orchestration (api + frontend)
- **AWS Infrastructure**: EC2 (t3.micro) + RDS MySQL (db.t3.micro)
- **CI/CD Workflow**: Local → GitHub → SSH Pull → Docker Rebuild

---

## SLIDE 6: Data Model (30 seconds)
---

**"The database structure:"**

```
Users (1) ─────────┬───────── (N) Conversations
                   │                    │
                   │               (N) Messages
                   │
Recipes (N) ───────┼───────── (1) Categories
    │              │
    ├── (N) Ingredients
    │
    └── (N) Steps
```

- **Users**: Authentication, links to conversation history
- **Recipes**: Core data with bilingual fields (name/name_es, description/description_es)
- **Ingredients & Steps**: Ordered by index, also bilingual
- **Conversations & Messages**: Stores AI chat history per user

---

## SLIDE 7: Challenges & Lessons Learned (30 seconds)
---

**"Key challenges I overcame:"**

1. **CORS Issues**: Configured Flask-CORS properly for cross-origin requests between frontend and API containers

2. **Docker Networking**: Understanding how containers communicate and exposing the right ports

3. **AWS Security Groups**: Had to open port 5000 for API access - learned about AWS networking

4. **Case Sensitivity**: Linux file system is case-sensitive (LanguageContext.jsx vs languagecontext.jsx) - caused deployment failures

5. **API Response Parsing**: Ensuring frontend correctly handles nested JSON structures from the API

---

## SLIDE 8: Future Enhancements (15 seconds)
---

**"What's next:"**

- Add more recipes to the database
- User favorites and recipe ratings
- Shopping list generation from selected recipes
- Voice-guided cooking mode
- Recipe submission by users (with moderation)

---

## SLIDE 9: Conclusion & Demo (15 seconds)
---

**"To summarize:"**

Colombian Recipes is a production-ready, full-stack application featuring:
- ✅ React frontend with bilingual support
- ✅ Flask REST API with JWT auth
- ✅ MySQL database on AWS RDS
- ✅ AI-powered cooking assistant
- ✅ Docker containerized deployment on AWS EC2

**"The app is live at http://18.118.142.25 - let me show you a quick demo..."**

---

## TALKING POINTS FOR Q&A

**If asked about AI implementation:**
"I implemented a multi-provider architecture with fallback. The system tries Claude first, then falls back to OpenAI, Gemini, and finally Groq. This ensures high availability even if one provider has issues."

**If asked about security:**
"User passwords are hashed with bcrypt before storage. Authentication uses JWT tokens with expiration. The AI assistant requires authentication to prevent abuse and track conversations."

**If asked about scalability:**
"The architecture is designed for scalability - the database is already on managed RDS which can scale vertically. The Docker containers can be deployed to ECS or Kubernetes for horizontal scaling."

**If asked about the tech stack choices:**
"I chose Flask because of my Python experience and its flexibility. React for the frontend because of its component-based architecture and large ecosystem. MySQL because it's reliable and I have experience with it. Docker for consistent deployments across environments."

---

## LIVE DEMO SCRIPT (if time permits)

1. **Show homepage** - "Here's the landing page with featured recipes"
2. **Click language toggle** - "Watch how everything switches to Spanish"
3. **Navigate to Recipes** - "We can search and filter recipes"
4. **Click on Bandeja Paisa** - "Here's the full recipe with ingredients and steps in Spanish"
5. **Adjust servings** - "Watch the ingredients recalculate"
6. **Go to AI Assistant** - "Let me ask a question about cooking..."
7. **Type a question** - "¿Cómo sé si mis frijoles están listos?" (How do I know if my beans are ready?)
8. **Show response** - "The AI responds in Spanish with helpful cooking advice"

---

**Total Time: ~5 minutes**
