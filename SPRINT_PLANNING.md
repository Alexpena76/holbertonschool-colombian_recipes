# Colombian Recipe API — Sprint Planning

## Sprint Overview

| Attribute | Value |
|-----------|-------|
| **Project Start** | Thursday, February 19, 2026 |
| **Project Deadline** | Monday, March 9, 2026 |
| **Total Duration** | 18 days (~2.5 weeks) |
| **Sprint Duration** | 6 days per sprint |
| **Total Sprints** | 3 sprints |
| **Team Size** | 1 (Solo Developer: Alex) |
| **Working Hours** | ~8-10 hrs/day |
| **Total Estimated Hours** | ~148 hours |

---

## Calendar View

```
     FEBRUARY 2026                      MARCH 2026
Su Mo Tu We Th Fr Sa               Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7                1  2  3  4  5  6  7
 8  9 10 11 12 13 14                8 [9] ← DEADLINE
15 16 17 18[19]20 21               
22 23 24 25 26 27 28               

[19] = Project Start (Today)
[9]  = Project Deadline (March 9)
```

---

## Sprint Timeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           18-DAY SPRINT TIMELINE TO MARCH 9                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  Feb 19-24 (6 days)        Feb 25 - Mar 2 (6 days)      Mar 3-9 (6 days)                       │
│  ═══════════════════       ═══════════════════════      ══════════════════                      │
│                                                                                                 │
│  ┌─────────────────┐       ┌─────────────────────┐      ┌─────────────────┐                    │
│  │    SPRINT 1     │       │      SPRINT 2       │      │    SPRINT 3     │                    │
│  │                 │       │                     │      │                 │                    │
│  │  🏗️ Setup        │       │  🤖 AI Assistant     │      │  ⚛️ Frontend     │                    │
│  │  🗄️ Database     │──────▶│  💬 Conversations   │─────▶│  💬 Chat UI     │                    │
│  │  🔐 Auth API     │       │  🔍 Search          │      │  📜 History     │                    │
│  │  📡 Recipe API   │       │  📝 Recipe Details  │      │  ☁️ AWS Deploy  │                    │
│  │                 │       │                     │      │                 │                    │
│  │    ~50 hrs      │       │      ~50 hrs        │      │    ~48 hrs      │                    │
│  └─────────────────┘       └─────────────────────┘      └─────────────────┘                    │
│                                                                                                 │
│  MILESTONE:                MILESTONE:                   MILESTONE:                             │
│  Backend API               AI + Conversations           MVP COMPLETE! 🚀                       │
│  working locally           fully working                Deployed to AWS                        │
│                                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────     │
│  Feb 19    Feb 24         Feb 25         Mar 2          Mar 3            Mar 9                 │
│  START ────────────────────────────────────────────────────────────────────── DEADLINE         │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Project Scope (MVP)

### Core Features

1. 🔐 User registration and authentication (JWT)
2. 🍲 Browse Colombian recipes by category
3. 🔍 Search recipes by name or ingredient
4. 📝 View detailed recipe information
5. 🤖 AI cooking assistant with contextual help
6. 💬 Saved conversation history per user
7. ☁️ Deployed to AWS

### MVP Recipes (3 Total)

| Recipe | Category | Difficulty | Region |
|--------|----------|------------|--------|
| **Bandeja Paisa** | Lunch | Hard | Antioquia |
| **Ajiaco** | Lunch | Medium | Cundinamarca |
| **Arepas** | Breakfast | Easy | Nacional |

These 3 recipes represent different difficulty levels and regions of Colombia.

---

## User Stories Summary

### 🔴 MUST HAVE (MVP Core)

| ID | User Story | Sprint |
|----|------------|--------|
| US-01 | As a user, I want to browse recipes by category | 1, 3 |
| US-02 | As a user, I want to view detailed recipe information | 2, 3 |
| US-03 | As a user, I want to search recipes by name or ingredient | 2, 3 |
| US-04 | As a user, I want to ask the AI assistant cooking questions | 2, 3 |
| US-05 | As a user, I want to create an account and log in | 1, 3 |
| US-06 | As a user, I want to see my previous AI conversations | 2, 3 |
| US-07 | As a developer, I want to access recipes via REST API | 1 |

---

## Sprint 1: Foundation, Auth & Recipe API

### Dates: Feb 19 - Feb 24 (6 days)

### Goal
Set up complete backend infrastructure with authentication and recipe endpoints working locally.

### Daily Breakdown

| Day | Date | Focus | Hours |
|-----|------|-------|-------|
| Day 1 | Thu Feb 19 | Project setup, Docker, Flask structure | 8 |
| Day 2 | Fri Feb 20 | All database tables, SQLAlchemy models | 8 |
| Day 3 | Sat Feb 21 | Seed data (categories, recipes, ingredients, steps) | 8 |
| Day 4 | Sun Feb 22 | User auth (register, login, JWT) | 10 |
| Day 5 | Mon Feb 23 | Recipe endpoints (list, detail, categories) | 8 |
| Day 6 | Tue Feb 24 | Error handling, pagination, testing | 8 |

### Sprint 1 Tasks

| Priority | Task ID | Task | Hours | Day |
|----------|---------|------|-------|-----|
| 🔴 MUST | T-01 | Create GitHub repository | 0.5 | 1 |
| 🔴 MUST | T-02 | Create Flask project structure | 1.5 | 1 |
| 🔴 MUST | T-03 | Create React project (Vite + TS + Tailwind) | 2 | 1 |
| 🔴 MUST | T-04 | Set up Docker Compose (Flask + MySQL) | 3 | 1 |
| 🔴 MUST | T-05 | Configure SQLAlchemy ORM | 1 | 1 |
| 🔴 MUST | T-06 | Create `users` table + model | 1.5 | 2 |
| 🔴 MUST | T-07 | Create `categories` table + model | 1 | 2 |
| 🔴 MUST | T-08 | Create `recipes` table + model | 1.5 | 2 |
| 🔴 MUST | T-09 | Create `ingredients` table + model | 1 | 2 |
| 🔴 MUST | T-10 | Create `steps` table + model | 1 | 2 |
| 🔴 MUST | T-11 | Create `conversations` table + model | 1.5 | 2 |
| 🔴 MUST | T-12 | Create `messages` table + model | 1.5 | 2 |
| 🔴 MUST | T-13 | Seed categories (6 categories) | 1 | 3 |
| 🔴 MUST | T-14 | Seed recipes (3 recipes) | 1 | 3 |
| 🔴 MUST | T-15 | Seed ingredients for all recipes | 1 | 3 |
| 🔴 MUST | T-16 | Seed steps for all recipes | 1 | 3 |
| 🔴 MUST | T-17 | Install Flask-JWT-Extended | 0.5 | 4 |
| 🔴 MUST | T-18 | Create UserService class | 2 | 4 |
| 🔴 MUST | T-19 | Build POST /auth/register endpoint | 2.5 | 4 |
| 🔴 MUST | T-20 | Build POST /auth/login endpoint | 2.5 | 4 |
| 🔴 MUST | T-21 | Build POST /auth/logout endpoint | 1 | 4 |
| 🔴 MUST | T-22 | Build GET /auth/me endpoint | 1 | 4 |
| 🔴 MUST | T-23 | Add @jwt_required decorator | 0.5 | 4 |
| 🔴 MUST | T-24 | Build GET /categories endpoint | 1.5 | 5 |
| 🔴 MUST | T-25 | Build GET /recipes endpoint | 2.5 | 5 |
| 🔴 MUST | T-26 | Build GET /recipes/{id} endpoint | 2 | 5 |
| 🔴 MUST | T-27 | Build GET /recipes/search endpoint | 2 | 5 |
| 🔴 MUST | T-28 | Create JSON response helper | 1.5 | 6 |
| 🔴 MUST | T-29 | Create error handling middleware | 2 | 6 |
| 🔴 MUST | T-30 | Add pagination to list endpoints | 2 | 6 |
| 🔴 MUST | T-31 | Test all endpoints with Postman | 2.5 | 6 |

**Sprint 1 Total: ~47 hours**

### Sprint 1 Deliverables

- ✅ Docker Compose running Flask + MySQL locally
- ✅ All 7 database tables created with models
- ✅ Sample data seeded (6 categories, 3 recipes with ingredients/steps)
- ✅ User registration and login working
- ✅ JWT authentication on protected routes
- ✅ Recipe endpoints (list, detail, search, categories)
- ✅ Consistent error handling and pagination

### Sprint 1 Success Criteria

```bash
# All these should work:
docker-compose up -d                    # Containers running
curl -X POST localhost:5000/api/v1/auth/register  # Creates user
curl -X POST localhost:5000/api/v1/auth/login     # Returns JWT
curl localhost:5000/api/v1/recipes -H "Authorization: Bearer $TOKEN"  # Returns recipes
curl localhost:5000/api/v1/recipes/bandeja-paisa -H "Authorization: Bearer $TOKEN"  # Returns details
```

---

## Sprint 2: AI Assistant & Conversations

### Dates: Feb 25 - Mar 2 (6 days)

### Goal
Implement AI cooking assistant with conversation history saving.

### Daily Breakdown

| Day | Date | Focus | Hours |
|-----|------|-------|-------|
| Day 1 | Wed Feb 25 | Claude API setup, AIService class | 8 |
| Day 2 | Thu Feb 26 | POST /assistant/ask endpoint | 10 |
| Day 3 | Fri Feb 27 | ConversationService, save messages | 8 |
| Day 4 | Sat Feb 28 | Conversation endpoints (list, detail, delete) | 8 |
| Day 5 | Sun Mar 1 | React project setup, AuthContext | 8 |
| Day 6 | Mon Mar 2 | Login/Register pages, routing | 8 |

### Sprint 2 Tasks

| Priority | Task ID | Task | Hours | Day |
|----------|---------|------|-------|-----|
| 🔴 MUST | T-32 | Set up Claude API credentials | 1 | 1 |
| 🔴 MUST | T-33 | Create AIService class | 3 | 1 |
| 🔴 MUST | T-34 | Build prompt template with recipe context | 2 | 1 |
| 🔴 MUST | T-35 | Test Claude API calls | 2 | 1 |
| 🔴 MUST | T-36 | Build POST /assistant/ask endpoint | 4 | 2 |
| 🔴 MUST | T-37 | Add recipe context fetching | 2 | 2 |
| 🔴 MUST | T-38 | Handle API errors gracefully | 2 | 2 |
| 🔴 MUST | T-39 | Test AI responses | 2 | 2 |
| 🔴 MUST | T-40 | Create ConversationService class | 2 | 3 |
| 🔴 MUST | T-41 | Create/get conversation logic | 2 | 3 |
| 🔴 MUST | T-42 | Save user message to database | 2 | 3 |
| 🔴 MUST | T-43 | Save AI response to database | 2 | 3 |
| 🔴 MUST | T-44 | Build GET /conversations endpoint | 2 | 4 |
| 🔴 MUST | T-45 | Build GET /conversations/{id} endpoint | 2 | 4 |
| 🔴 MUST | T-46 | Build DELETE /conversations/{id} endpoint | 1.5 | 4 |
| 🔴 MUST | T-47 | Add conversation_id to /assistant/ask | 1.5 | 4 |
| 🔴 MUST | T-48 | Test conversation flow end-to-end | 1 | 4 |
| 🔴 MUST | T-49 | Set up React with TypeScript and Tailwind | 2 | 5 |
| 🔴 MUST | T-50 | Create API service (axios setup) | 1.5 | 5 |
| 🔴 MUST | T-51 | Create AuthContext | 2.5 | 5 |
| 🔴 MUST | T-52 | Create ProtectedRoute component | 2 | 5 |
| 🔴 MUST | T-53 | Create LoginPage component | 3 | 6 |
| 🔴 MUST | T-54 | Create RegisterPage component | 2.5 | 6 |
| 🔴 MUST | T-55 | Set up React Router | 1.5 | 6 |
| 🔴 MUST | T-56 | Test auth flow in frontend | 1 | 6 |

**Sprint 2 Total: ~50 hours**

### Sprint 2 Deliverables

- ✅ AI assistant answering cooking questions
- ✅ Recipe context included in AI prompts
- ✅ All messages saved to database
- ✅ Conversation list endpoint
- ✅ Conversation detail endpoint
- ✅ Continue existing conversation
- ✅ React app with authentication working
- ✅ Login and Register pages

### Sprint 2 Success Criteria

```bash
# Backend AI test:
curl -X POST localhost:5000/api/v1/assistant/ask \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"recipe_id":"bandeja-paisa","question":"My beans are hard"}'
# Returns AI response + conversation_id

# Conversation history:
curl localhost:5000/api/v1/conversations -H "Authorization: Bearer $TOKEN"
# Returns list of user's conversations

# Frontend:
npm run dev  # React app runs
# Can login/register and see protected routes
```

---

## Sprint 3: Frontend UI & AWS Deployment

### Dates: Mar 3 - Mar 9 (6 days + buffer)

### Goal
Complete all frontend UI and deploy to AWS.

### Daily Breakdown

| Day | Date | Focus | Hours |
|-----|------|-------|-------|
| Day 1 | Tue Mar 3 | Recipe browsing UI (categories, grid, cards) | 8 |
| Day 2 | Wed Mar 4 | Recipe detail page, search UI | 8 |
| Day 3 | Thu Mar 5 | Chat interface component | 8 |
| Day 4 | Fri Mar 6 | Conversation history page | 8 |
| Day 5 | Sat Mar 7 | AWS setup (RDS, EC2, S3) | 10 |
| Day 6 | Sun Mar 8 | Deploy + testing | 6 |
| Buffer | Mon Mar 9 | Bug fixes, documentation | — |

### Sprint 3 Tasks

| Priority | Task ID | Task | Hours | Day |
|----------|---------|------|-------|-----|
| 🔴 MUST | T-57 | Create CategoryList component | 2 | 1 |
| 🔴 MUST | T-58 | Create RecipeCard component | 2 | 1 |
| 🔴 MUST | T-59 | Create RecipeGrid component | 2 | 1 |
| 🔴 MUST | T-60 | Create HomePage (categories view) | 2 | 1 |
| 🔴 MUST | T-61 | Create RecipeDetailPage | 3 | 2 |
| 🔴 MUST | T-62 | Create IngredientList component | 1.5 | 2 |
| 🔴 MUST | T-63 | Create StepList component | 1.5 | 2 |
| 🔴 MUST | T-64 | Create SearchBar component | 2 | 2 |
| 🔴 MUST | T-65 | Create ChatInterface component | 3 | 3 |
| 🔴 MUST | T-66 | Create ChatMessage component | 2 | 3 |
| 🔴 MUST | T-67 | Connect chat to API | 2 | 3 |
| 🔴 MUST | T-68 | Add loading states | 1 | 3 |
| 🔴 MUST | T-69 | Create ConversationListPage | 3 | 4 |
| 🔴 MUST | T-70 | Create ConversationDetailPage | 3 | 4 |
| 🔴 MUST | T-71 | Add "Continue conversation" feature | 2 | 4 |
| 🔴 MUST | T-72 | Set up AWS RDS MySQL | 2 | 5 |
| 🔴 MUST | T-73 | Set up AWS EC2 instance | 2 | 5 |
| 🔴 MUST | T-74 | Deploy Flask to EC2 with Docker | 3 | 5 |
| 🔴 MUST | T-75 | Set up S3 bucket for React | 1.5 | 5 |
| 🔴 MUST | T-76 | Configure CloudFront CDN | 1.5 | 5 |
| 🔴 MUST | T-77 | Deploy React build to S3 | 1.5 | 6 |
| 🔴 MUST | T-78 | Configure environment variables | 1 | 6 |
| 🔴 MUST | T-79 | Test full flow on production | 2 | 6 |
| 🔴 MUST | T-80 | Write final documentation | 1.5 | 6 |

**Sprint 3 Total: ~48 hours**

### Sprint 3 Deliverables

- ✅ Complete recipe browsing UI
- ✅ Recipe detail page with ingredients/steps
- ✅ Search functionality
- ✅ AI chat interface
- ✅ Conversation history page
- ✅ Flask API deployed to EC2
- ✅ React app deployed to S3/CloudFront
- ✅ MySQL database on RDS
- ✅ **MVP COMPLETE AND LIVE!** 🚀

### Sprint 3 Success Criteria

```bash
# Production URLs work:
https://colombianrecipes.com           # React app loads
https://api.colombianrecipes.com/api/v1/health  # API responds

# Full user flow works:
# 1. Register new account
# 2. Login
# 3. Browse categories
# 4. View recipe detail
# 5. Ask AI a question
# 6. View conversation history
# 7. Continue a conversation
```

---

## Complete Task Summary

### By Category

| Category | Tasks | Hours |
|----------|-------|-------|
| Infrastructure & Setup | 12 | 18 |
| Database & Models | 7 | 10 |
| Seed Data | 4 | 8 |
| Authentication API | 8 | 13 |
| Recipe API | 6 | 13 |
| AI Assistant API | 8 | 18 |
| Conversations API | 8 | 13 |
| React Auth & Setup | 8 | 14 |
| React Recipe UI | 8 | 16 |
| React Chat UI | 6 | 13 |
| AWS Deployment | 8 | 14 |
| **Total** | **83** | **~148** |

### By Sprint

| Sprint | Dates | Focus | Hours |
|--------|-------|-------|-------|
| Sprint 1 | Feb 19-24 | Backend Foundation | 50 |
| Sprint 2 | Feb 25 - Mar 2 | AI + Conversations | 50 |
| Sprint 3 | Mar 3-9 | Frontend + Deploy | 48 |
| **Total** | **18 days** | | **~148 hrs** |

---

## Risk Management

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AWS setup takes longer | Medium | High | Start AWS on Day 5 of Sprint 3; have local demo ready |
| Claude API issues | Low | High | Test early in Sprint 2; implement retry logic |
| Frontend takes longer | Medium | Medium | Keep UI simple; use Tailwind components |
| Running behind schedule | Medium | High | Cut SHOULD HAVE features; focus on MUST HAVE only |

### Contingency Plan

If running behind by end of Sprint 2:
1. Simplify frontend (basic styling only)
2. Skip conversation history UI (API still works)
3. Deploy to EC2 only (skip CloudFront)
4. Document remaining work for future

---

## Daily Standup Template

```markdown
## Date: [YYYY-MM-DD] | Sprint [X] Day [Y]

**Hours worked:** X hrs

**✅ Completed:**
- T-XX: [Task description]
- T-XX: [Task description]

**🔄 In Progress:**
- T-XX: [Task description] - X% done

**🚧 Blockers:**
- [Any issues]

**📋 Tomorrow:**
- T-XX: [Task description]
```

---

## Definition of Done

A task is **DONE** when:

- [ ] Code written and working
- [ ] Committed with proper message
- [ ] No console errors
- [ ] Works in Docker (backend) or browser (frontend)
- [ ] Tested manually

---

## Final Checklist (March 9)

### Backend API
- [ ] User registration/login (JWT)
- [ ] GET /categories
- [ ] GET /recipes (with pagination)
- [ ] GET /recipes/{id}
- [ ] GET /recipes/search
- [ ] POST /assistant/ask
- [ ] GET /conversations
- [ ] GET /conversations/{id}
- [ ] DELETE /conversations/{id}

### Frontend Pages
- [ ] Login page
- [ ] Register page
- [ ] Home page (categories)
- [ ] Recipe list/grid
- [ ] Recipe detail page
- [ ] AI chat interface
- [ ] Conversation history

### Deployment
- [ ] RDS MySQL running
- [ ] EC2 with Flask API
- [ ] S3 + CloudFront with React
- [ ] Environment variables set
- [ ] HTTPS working

### Documentation
- [ ] README complete
- [ ] API documented
- [ ] GitHub repo public

---

## Summary

| Metric | Value |
|--------|-------|
| **Start Date** | Thursday, February 19, 2026 |
| **Deadline** | Monday, March 9, 2026 |
| **Total Days** | 18 days |
| **Total Sprints** | 3 |
| **Sprint Length** | 6 days each |
| **Total Hours** | ~148 hours |
| **Avg Hours/Day** | ~8 hours |
| **Database Tables** | 7 |
| **API Endpoints** | 14 |
| **React Pages** | 7 |

---
