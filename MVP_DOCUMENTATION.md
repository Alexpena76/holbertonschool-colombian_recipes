# 🇨🇴 Colombian Recipe API — MVP Documentation

> **Project:** Colombian Recipe API with AI Cooking Assistant  
> **Author:** Alejandro Pena  
> **Date:** February 2025  
> **Stack:** Python, Flask, React, TypeScript, AWS, Claude AI

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [User Stories](#2-user-stories)
3. [System Architecture](#3-system-architecture)
4. [Database Design](#4-database-design)
5. [Sequence Diagrams](#5-sequence-diagrams)
6. [API Specification](#6-api-specification)
7. [SCM Strategy](#7-scm-strategy)
8. [QA Strategy](#8-qa-strategy)
9. [Technical Justifications](#9-technical-justifications)

---

## 1. Project Overview

### Purpose

A REST API that provides access to authentic Colombian recipes with an AI-powered cooking assistant that helps users through the cooking process in real-time.

### Key Features

- 🍲 Browse Colombian recipes by category, region, and difficulty
- 🔍 Search recipes by name or ingredient
- 🤖 AI cooking assistant for real-time guidance
- 🔄 Ingredient substitution suggestions
- 🌐 Bilingual support (English/Spanish)
- 📱 Responsive web interface

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | Python 3.11, Flask, Gunicorn |
| Database | MySQL 8.0, SQLAlchemy ORM |
| AI | Claude API (Anthropic) |
| Infrastructure | AWS (S3, RDS, CloudFront, EC2), Docker, Nginx |
| CI/CD | GitHub Actions |

---

## 2. User Stories

### Prioritization Method: MoSCoW

### 🔴 MUST HAVE (MVP Core)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-01 | As a **user**, I want to **browse Colombian recipes by category**, so that **I can find dishes appropriate for my meal time**. | Categories displayed, recipes filterable |
| US-02 | As a **user**, I want to **view detailed recipe information**, so that **I can prepare the dish correctly**. | Ingredients, steps, times shown |
| US-03 | As a **user**, I want to **search recipes by name or ingredient**, so that **I can find specific dishes**. | Search returns relevant results |
| US-04 | As a **user**, I want to **ask the AI assistant questions about a recipe**, so that **I can get real-time help while cooking**. | AI responds with contextual advice |
| US-05 | As a **user**, I want to **receive step-by-step AI guidance**, so that **I don't make mistakes preparing unfamiliar dishes**. | AI provides clear instructions |
| US-06 | As a **developer**, I want to **access recipes via REST API**, so that **I can integrate into applications**. | RESTful endpoints, JSON responses |

### 🟡 SHOULD HAVE

| ID | User Story |
|----|------------|
| US-07 | As a user, I want to adjust serving sizes and have ingredients automatically recalculate |
| US-08 | As a user, I want to ask the AI for ingredient substitutions |
| US-09 | As a user, I want to filter recipes by difficulty level |
| US-10 | As a user, I want to see recipe images |
| US-11 | As a user, I want to view recipes in Spanish or English |

### 🟢 COULD HAVE

| ID | User Story |
|----|------------|
| US-12 | As a user, I want to save favorite recipes |
| US-13 | As a user, I want to see nutritional information |
| US-14 | As a user, I want to rate and review recipes |

### ⚪ WON'T HAVE (Future)

- User-uploaded recipes
- Video tutorials
- Meal planning
- Grocery delivery integration

---

## 3. System Architecture

### High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                    👨‍🍳 USER                                       │
└──────────────────────────────────────┬───────────────────────────────────────────┘
                                       │ HTTPS
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              ☁️  AWS CLOUD                                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                        FRONTEND HOSTING                                     │ │
│  │   ┌─────────────────────┐         ┌─────────────────────────────┐          │ │
│  │   │   🌐 CloudFront     │────────▶│      🪣 S3 Bucket           │          │ │
│  │   │   (CDN)             │         │   (React App)               │          │ │
│  │   └─────────────────────┘         └─────────────────────────────┘          │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                       │ REST API                                 │
│                                       ▼                                          │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                          BACKEND API (EC2)                                  │ │
│  │   ┌─────────────────────────────────────────────────────────────────────┐  │ │
│  │   │                    🖥️  EC2 Instance (t3.micro)                       │  │ │
│  │   │   ┌─────────────────────────────────────────────────────────────┐   │  │ │
│  │   │   │                   🐳 Docker Compose                          │   │  │ │
│  │   │   │   ┌────────────────┐       ┌────────────────────────────┐   │   │  │ │
│  │   │   │   │  🔒 Nginx      │──────▶│      🚀 Flask API          │   │   │  │ │
│  │   │   │   │  (Proxy/SSL)   │       │   (Python + Gunicorn)      │   │   │  │ │
│  │   │   │   └────────────────┘       │   ┌──────────────────────┐ │   │   │  │ │
│  │   │   │                            │   │  🍲 Recipe Service   │ │   │   │  │ │
│  │   │   │                            │   │  🤖 AI Service       │ │   │   │  │ │
│  │   │   │                            │   └──────────────────────┘ │   │   │  │ │
│  │   │   │                            └────────────────────────────┘   │   │  │ │
│  │   │   └─────────────────────────────────────────────────────────────┘   │  │ │
│  │   └─────────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                          │                              │                        │
│                          ▼                              ▼                        │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                            DATA LAYER                                       │ │
│  │   ┌────────────────────────────┐    ┌────────────────────────────────┐     │ │
│  │   │      🗄️ RDS MySQL          │    │      🖼️ S3 Bucket              │     │ │
│  │   │      (db.t3.micro)         │    │   (Recipe Images)              │     │ │
│  │   │   • recipes                │    │   • /images/recipes/           │     │ │
│  │   │   • ingredients            │    │   • /images/categories/        │     │ │
│  │   │   • steps                  │    │                                │     │ │
│  │   │   • categories             │    │                                │     │ │
│  │   └────────────────────────────┘    └────────────────────────────────┘     │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │ Claude API
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           🧠 CLAUDE API (External)                                │
│                              Anthropic AI Service                                 │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### AWS Services Used

| Service | Purpose | Tier |
|---------|---------|------|
| S3 | Host React app + recipe images | Free tier |
| CloudFront | CDN for global delivery | ~$1/month |
| EC2 | Run Flask API (Docker) | Free tier (t3.micro) |
| RDS | Managed MySQL database | Free tier (db.t3.micro) |

### Estimated Monthly Cost

| Phase | Cost |
|-------|------|
| During Free Tier (12 months) | ~$1-2/month |
| After Free Tier | ~$25-30/month |

---

## 4. Database Design

### Entity-Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   categories    │       │     recipes     │       │   ingredients   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ PK id           │       │ PK id           │       │ PK id           │
│    name         │◄──────│ FK category     │───────│ FK recipe_id    │
│    name_es      │       │    name         │       │    name         │
│    image_url    │       │    name_es      │       │    name_es      │
└─────────────────┘       │    region       │       │    amount       │
                          │    difficulty   │       │    unit         │
                          │    prep_time    │       │    order_index  │
                          │    cook_time    │       └─────────────────┘
                          │    servings     │
                          │    description  │       ┌─────────────────┐
                          │    image_url    │       │      steps      │
                          │    created_at   │       ├─────────────────┤
                          └────────┬────────┘       │ PK id           │
                                   │                │ FK recipe_id    │
                                   └───────────────▶│    step_number  │
                                                    │    instruction  │
                                                    │    instruction_es│
                                                    └─────────────────┘
```

### Database Schema (SQL)

```sql
-- Categories table
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_es VARCHAR(100),
    image_url VARCHAR(500)
);

-- Recipes table
CREATE TABLE recipes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    name_es VARCHAR(200),
    category VARCHAR(50),
    region VARCHAR(100),
    difficulty ENUM('easy', 'medium', 'hard'),
    prep_time_minutes INT,
    cook_time_minutes INT,
    servings INT,
    description TEXT,
    description_es TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category) REFERENCES categories(id)
);

-- Ingredients table
CREATE TABLE ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id VARCHAR(50),
    name VARCHAR(200) NOT NULL,
    name_es VARCHAR(200),
    amount DECIMAL(10,2),
    unit VARCHAR(50),
    order_index INT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Steps table
CREATE TABLE steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id VARCHAR(50),
    step_number INT,
    instruction TEXT NOT NULL,
    instruction_es TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
```

---

## 5. Sequence Diagrams

### Use Case 1: Browse Recipes by Category

```
┌────────┐     ┌────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │ CloudFront │     │  React   │     │  Flask   │     │   RDS    │     │    S3    │
└───┬────┘     └─────┬──────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │                │                 │                │                │                │
    │ 1. Visit URL   │                 │                │                │                │
    │───────────────>│                 │                │                │                │
    │                │ 2. Serve React  │                │                │                │
    │                │────────────────>│                │                │                │
    │                │                 │ 3. GET /recipes│                │                │
    │                │                 │───────────────>│                │                │
    │                │                 │                │ 4. SELECT *    │                │
    │                │                 │                │───────────────>│                │
    │                │                 │                │ 5. Rows        │                │
    │                │                 │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │                │                 │ 6. JSON        │                │                │
    │                │                 │<─ ─ ─ ─ ─ ─ ─ ─│                │                │
    │                │                 │ 7. GET images  │                │                │
    │                │                 │───────────────────────────────────────────────>│
    │ 8. Display     │                 │                │                │                │
    │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                │                │                │
```

### Use Case 2: AI Cooking Assistant Q&A

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │  React   │     │  Flask   │     │   RDS    │     │  Claude  │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                │                │
    │ 1. Ask        │                │                │                │
    │   question    │                │                │                │
    │──────────────>│                │                │                │
    │               │ 2. POST        │                │                │
    │               │  /assistant/ask│                │                │
    │               │───────────────>│                │                │
    │               │                │ 3. Get recipe  │                │
    │               │                │   context      │                │
    │               │                │───────────────>│                │
    │               │                │ 4. Recipe data │                │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │ 5. POST prompt │                │
    │               │                │───────────────────────────────>│
    │               │                │ 6. AI response │                │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │               │ 7. JSON        │                │                │
    │               │<─ ─ ─ ─ ─ ─ ─ ─│                │                │
    │ 8. Display    │                │                │                │
    │<─ ─ ─ ─ ─ ─ ─ │                │                │                │
```

### Use Case 3: Search Recipes

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │  React   │     │  Flask   │     │   RDS    │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                │
    │ 1. Type       │                │                │
    │  "platano"    │                │                │
    │──────────────>│                │                │
    │               │ 2. Debounce    │                │
    │               │───┐            │                │
    │               │<──┘            │                │
    │               │ 3. GET /search │                │
    │               │───────────────>│                │
    │               │                │ 4. SELECT LIKE │
    │               │                │───────────────>│
    │               │                │ 5. Matches     │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─│
    │               │ 6. JSON        │                │
    │               │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │ 7. Display    │                │                │
    │<─ ─ ─ ─ ─ ─ ─ │                │                │
```

---

## 6. API Specification

### External API: Claude (Anthropic)

| Attribute | Value |
|-----------|-------|
| Provider | Anthropic |
| Endpoint | `https://api.anthropic.com/v1/messages` |
| Purpose | AI cooking assistant |
| Auth | API Key header |

### Internal API Endpoints

**Base URL:** `https://api.colombianrecipes.com/api/v1`

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/recipes` | GET | Yes | List recipes (paginated) |
| `/recipes/{id}` | GET | Yes | Get recipe details |
| `/recipes/search` | GET | Yes | Search recipes |
| `/categories` | GET | Yes | List categories |
| `/assistant/ask` | POST | Yes | AI cooking question |
| `/assistant/substitute` | POST | Yes | Ingredient substitution |

### Example: GET /recipes

**Request:**
```http
GET /api/v1/recipes?category=lunch&page=1
X-API-Key: your_api_key
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recipes": [
      {
        "id": "bandeja-paisa",
        "name": "Bandeja Paisa",
        "category": "lunch",
        "difficulty": "hard",
        "image_url": "https://cdn.example.com/bandeja.jpg"
      }
    ]
  },
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 24
  }
}
```

### Example: POST /assistant/ask

**Request:**
```http
POST /api/v1/assistant/ask
Content-Type: application/json
X-API-Key: your_api_key

{
  "recipe_id": "bandeja-paisa",
  "question": "My beans are still hard after 2 hours",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "Don't worry! Try adding a pinch of baking soda...",
    "tips": ["Don't add salt early", "Use fresh beans"]
  }
}
```

---

## 7. SCM Strategy

### Version Control

| Tool | Value |
|------|-------|
| VCS | Git |
| Platform | GitHub |
| Branching | GitHub Flow |

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Main | `main` | `main` |
| Feature | `feature/{desc}` | `feature/recipe-search` |
| Bug Fix | `fix/{desc}` | `fix/auth-bug` |
| Hotfix | `hotfix/{desc}` | `hotfix/api-crash` |

### Commit Convention

```
<type>(<scope>): <description>

feat(api): add recipe search endpoint
fix(auth): resolve API key validation
docs(readme): update installation guide
```

### Pull Request Workflow

1. Create feature branch from `main`
2. Make commits with conventional messages
3. Push and create Pull Request
4. Automated tests run (lint, unit, integration)
5. Self-review code
6. Squash and merge to `main`
7. Auto-deploy to production

### Branch Protection (main)

- ✅ Require pull request
- ✅ Require status checks to pass
- ✅ Require linear history
- ❌ No force push
- ❌ No deletion

---

## 8. QA Strategy

### Testing Pyramid

```
              ┌─────────────┐
              │   E2E       │  ← Fewer, slower
              │  (Cypress)  │
             ─┴─────────────┴─
            ┌─────────────────┐
            │  Integration    │  ← API + DB
            │ (pytest, Jest)  │
           ─┴─────────────────┴─
          ┌───────────────────────┐
          │      Unit Tests       │  ← Many, fast
          │   (pytest, Jest)      │
         ─┴───────────────────────┴─
```

### Testing by Layer

| Layer | Test Type | Tool | Coverage |
|-------|-----------|------|----------|
| Backend | Unit | pytest | 80% |
| Backend | Integration | pytest | 70% |
| Frontend | Unit | Jest + RTL | 70% |
| Frontend | Component | Jest + RTL | 60% |
| API | E2E | Postman/Newman | Critical paths |

### CI/CD Pipeline

```
Push → Lint → Unit Tests → Build → Integration Tests → Deploy
```

| Stage | Trigger | Tools |
|-------|---------|-------|
| Lint | Every push | flake8, eslint, black |
| Unit Tests | Every push | pytest, jest |
| Build | PR to main | Docker |
| Integration | PR to main | pytest + test DB |
| Deploy | Merge to main | AWS (S3, EC2) |

---

## 9. Technical Justifications

### Why These Technologies?

| Technology | Justification |
|------------|---------------|
| **Flask** | Lightweight, Python expertise, quick MVP development |
| **React + TypeScript** | Component-based UI, type safety, existing skills |
| **MySQL** | Relational data (recipes → ingredients), existing skills |
| **AWS** | Industry standard, free tier, learning opportunity |
| **Claude API** | Superior contextual understanding for cooking advice |
| **Docker** | Consistent environments, existing skills |

### Why Hybrid AWS Architecture?

| Factor | Decision |
|--------|----------|
| **Learning** | Gain real AWS experience for resume |
| **Familiarity** | Keep Flask/Docker skills, add cloud layer |
| **Cost** | Free tier eligible, ~$1-2/month initially |
| **Scalability** | Can upgrade EC2, add read replicas later |

### Why GitHub Flow (not GitFlow)?

| Factor | GitHub Flow |
|--------|-------------|
| Team size | Solo developer - simpler is better |
| Release cadence | Continuous deployment |
| Complexity | Low overhead, fewer branches |

### Why Claude for AI?

| Factor | Claude |
|--------|--------|
| Contextual understanding | Excellent for recipe-specific advice |
| Bilingual | Native English/Spanish support |
| Tone | Warm, conversational (good for cooking) |
| Experience | Already familiar with the API |

---

## Appendix: File Structure

```
colombian-recipe-api/
├── README.md                 # This documentation
├── docker-compose.yml        # Container orchestration
├── .github/
│   └── workflows/
│       └── ci.yml            # CI/CD pipeline
├── api/                      # Flask backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── pages/
│   │   └── services/
│   ├── Dockerfile
│   └── package.json
└── docs/                     # Additional documentation
    ├── architecture.jsx      # Interactive diagram
    ├── sequence-diagrams.jsx
    └── api-spec.md
```

---

## Quick Links

- **GitHub Repository:** `github.com/Alexpena76/colombian-recipe-api`
- **Live Demo:** (Coming soon)
- **API Documentation:** (Coming soon)

---

*This documentation was created as part of the Holberton School MVP project.*
