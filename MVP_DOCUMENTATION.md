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
9. [Sprint Planning](#9-sprint-planning)
10. [Technical Justifications](#10-technical-justifications)

---

## 1. Project Overview

### Purpose

A REST API that provides access to authentic Colombian recipes with an AI-powered cooking assistant that helps users through the cooking process in real-time. Users can create accounts, chat with the AI assistant, and access their conversation history across sessions.

### Key Features

- 🔐 User registration and authentication (JWT)
- 🍲 Browse Colombian recipes by category, region, and difficulty
- 🔍 Search recipes by name or ingredient
- 🤖 AI cooking assistant for real-time guidance
- 💬 Saved conversation history per user
- 🔄 Continue previous AI conversations
- 🌐 Bilingual support (English/Spanish)
- 📱 Responsive web interface

### MVP Recipes (3 Total)

| Recipe | Category | Difficulty | Region |
|--------|----------|------------|--------|
| **Bandeja Paisa** | Lunch | Hard | Antioquia |
| **Ajiaco** | Lunch | Medium | Cundinamarca |
| **Arepas** | Breakfast | Easy | Nacional |

These 3 recipes represent different difficulty levels and regions of Colombia.

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Tailwind CSS, Vite |
| Backend | Python 3.11, Flask, Gunicorn, SQLAlchemy |
| Database | MySQL 8.0 |
| Authentication | Flask-JWT-Extended, bcrypt |
| AI | Claude API (Anthropic) |
| Infrastructure | AWS (S3, RDS, CloudFront, EC2), Docker, Nginx |
| CI/CD | GitHub Actions |

---

## 2. User Stories

### Prioritization Method: MoSCoW

### 🔴 MUST HAVE (MVP Core)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-01 | As a **user**, I want to **browse Colombian recipes by category**, so that **I can find dishes appropriate for my meal time**. | Categories displayed with recipe counts; clicking category shows filtered recipes |
| US-02 | As a **user**, I want to **view detailed recipe information**, so that **I can prepare the dish correctly**. | Shows ingredients with amounts, step-by-step instructions, prep/cook times |
| US-03 | As a **user**, I want to **search recipes by name or ingredient**, so that **I can find specific dishes or use ingredients I have**. | Search returns relevant results; matches recipe names and ingredients |
| US-04 | As a **user**, I want to **ask the AI assistant questions about a recipe**, so that **I can get real-time help while cooking**. | AI responds with contextual advice based on the specific recipe |
| US-05 | As a **user**, I want to **create an account and log in**, so that **my conversations and preferences are saved**. | Can register with email/password; login returns JWT; protected routes work |
| US-06 | As a **user**, I want to **see my previous AI conversations**, so that **I can reference past cooking help and continue where I left off**. | Conversation list shows all chats; can view full history; can continue conversation |
| US-07 | As a **developer**, I want to **access recipes via REST API**, so that **I can integrate into applications**. | RESTful endpoints; consistent JSON responses; proper error handling |

### 🟡 SHOULD HAVE (Post-MVP)

| ID | User Story |
|----|------------|
| US-08 | As a user, I want to adjust serving sizes and have ingredients automatically recalculate |
| US-09 | As a user, I want to ask the AI for ingredient substitutions |
| US-10 | As a user, I want to filter recipes by difficulty level |
| US-11 | As a user, I want to see recipe images |
| US-12 | As a user, I want to view recipes in Spanish or English |

### 🟢 COULD HAVE (Future)

| ID | User Story |
|----|------------|
| US-13 | As a user, I want to save favorite recipes |
| US-14 | As a user, I want to rate and review recipes |
| US-15 | As a user, I want to see nutritional information |

### ⚪ WON'T HAVE (Out of Scope)

- User-uploaded recipes
- Video tutorials
- Meal planning
- Grocery delivery integration
- Social sharing features

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
│  │   │   (CDN + HTTPS)     │         │   colombian-recipes-app     │          │ │
│  │   │                     │         │   • index.html              │          │ │
│  │   │                     │         │   • bundle.js               │          │ │
│  │   │                     │         │   • styles.css              │          │ │
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
│  │   │   │                                                              │   │  │ │
│  │   │   │   ┌────────────────┐       ┌────────────────────────────┐   │   │  │ │
│  │   │   │   │  🔒 Nginx      │──────▶│      🚀 Flask API          │   │   │  │ │
│  │   │   │   │  (SSL/Proxy)   │       │   (Python + Gunicorn)      │   │   │  │ │
│  │   │   │   │  Port 80/443   │       │   Port 5000                │   │   │  │ │
│  │   │   │   └────────────────┘       │                            │   │   │  │ │
│  │   │   │                            │   ┌──────────────────────┐ │   │   │  │ │
│  │   │   │                            │   │ 🔐 Auth Service      │ │   │   │  │ │
│  │   │   │                            │   │ 🍲 Recipe Service    │ │   │   │  │ │
│  │   │   │                            │   │ 🤖 AI Service        │ │   │   │  │ │
│  │   │   │                            │   │ 💬 Conversation Svc  │ │   │   │  │ │
│  │   │   │                            │   └──────────────────────┘ │   │   │  │ │
│  │   │   │                            └────────────────────────────┘   │   │  │ │
│  │   │   └─────────────────────────────────────────────────────────────┘   │  │ │
│  │   └─────────────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                          │
│                                       ▼                                          │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                            DATA LAYER                                       │ │
│  │                                                                             │ │
│  │   ┌────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                      🗄️ RDS MySQL (db.t3.micro)                     │   │ │
│  │   │                                                                     │   │ │
│  │   │   ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────────┐  │   │ │
│  │   │   │  users    │ │ recipes   │ │ingredients│ │   conversations   │  │   │ │
│  │   │   └───────────┘ └───────────┘ └───────────┘ └───────────────────┘  │   │ │
│  │   │   ┌───────────┐ ┌───────────┐ ┌───────────────────────────────────┐│   │ │
│  │   │   │categories │ │   steps   │ │           messages               ││   │ │
│  │   │   └───────────┘ └───────────┘ └───────────────────────────────────┘│   │ │
│  │   │                                                                     │   │ │
│  │   └────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                             │ │
│  │   ┌────────────────────────────────────────────────────────────────────┐   │ │
│  │   │                 🖼️ S3 Bucket (colombian-recipes-images)             │   │ │
│  │   │                 • /images/recipes/                                  │   │ │
│  │   │                 • /images/categories/                               │   │ │
│  │   └────────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Claude API (HTTPS)
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           🧠 CLAUDE API (External)                                │
│                              Anthropic AI Service                                 │
│                         https://api.anthropic.com/v1                             │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Component Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| CloudFront | AWS CDN | Global content delivery, HTTPS |
| S3 (App) | AWS Storage | Host React static files |
| S3 (Images) | AWS Storage | Store recipe/category images |
| EC2 | AWS Compute | Run Flask API in Docker |
| RDS | AWS Database | Managed MySQL instance |
| Nginx | Reverse Proxy | SSL termination, load balancing |
| Flask | Python Framework | REST API, business logic |
| Claude API | Anthropic | AI cooking assistant |

### AWS Cost Estimates

| Phase | Monthly Cost |
|-------|--------------|
| Free Tier (12 months) | ~$1-2/month |
| After Free Tier | ~$25-30/month |

---

## 4. Database Design

### Entity-Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ PK id           │──────────────────────────────────┐
│    email        │                                  │
│    password_hash│                                  │
│    name         │                                  │
│    created_at   │                                  │
└─────────────────┘                                  │
                                                     │
┌─────────────────┐       ┌─────────────────┐        │       ┌─────────────────┐
│   categories    │       │     recipes     │        │       │  conversations  │
├─────────────────┤       ├─────────────────┤        │       ├─────────────────┤
│ PK id           │◄──────│ FK category     │◄───────┼───────│ FK recipe_id    │
│    name         │       │ PK id           │        │       │ PK id           │
│    name_es      │       │    name         │        └──────▶│ FK user_id      │
│    image_url    │       │    name_es      │                │    title        │
└─────────────────┘       │    region       │                │    created_at   │
                          │    difficulty   │                │    updated_at   │
                          │    prep_time    │                └────────┬────────┘
                          │    cook_time    │                         │
                          │    servings     │                         │
                          │    description  │                         │
                          │    description_es                         │
                          │    image_url    │                         │
                          │    created_at   │                         │
                          └────────┬────────┘                         │
                                   │                                  │
                ┌──────────────────┼──────────────────┐               │
                ▼                  ▼                  │               │
     ┌─────────────────┐ ┌─────────────────┐         │               │
     │   ingredients   │ │      steps      │         │               │
     ├─────────────────┤ ├─────────────────┤         │               │
     │ PK id           │ │ PK id           │         │               │
     │ FK recipe_id    │ │ FK recipe_id    │         │               │
     │    name         │ │    step_number  │         │               │
     │    name_es      │ │    instruction  │         │               │
     │    amount       │ │    instruction_es         │               │
     │    unit         │ └─────────────────┘         │               │
     │    order_index  │                             │               │
     └─────────────────┘                             │               │
                                                     │               │
                                                     │               ▼
                                                     │       ┌─────────────────┐
                                                     │       │    messages     │
                                                     │       ├─────────────────┤
                                                     │       │ PK id           │
                                                     └──────▶│ FK conversation │
                                                             │    role (enum)  │
                                                             │    content      │
                                                             │    created_at   │
                                                             └─────────────────┘

RELATIONSHIPS:
─────────────────────────────────────────────────────────────────────────────────
• users (1) ──────< conversations (many)     : A user can have many conversations
• recipes (1) ────< conversations (many)     : A recipe can have many conversations
• conversations (1) ──< messages (many)      : A conversation has many messages
• categories (1) ─< recipes (many)           : A category contains many recipes
• recipes (1) ────< ingredients (many)       : A recipe has many ingredients
• recipes (1) ────< steps (many)             : A recipe has many steps
```

### Database Schema (SQL)

```sql
-- =====================================================
-- USERS TABLE
-- =====================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_email (email)
);

-- =====================================================
-- CATEGORIES TABLE
-- =====================================================
CREATE TABLE categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_es VARCHAR(100),
    image_url VARCHAR(500)
);

-- =====================================================
-- RECIPES TABLE
-- =====================================================
CREATE TABLE recipes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    name_es VARCHAR(200),
    category VARCHAR(50),
    region VARCHAR(100),
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    prep_time_minutes INT,
    cook_time_minutes INT,
    servings INT DEFAULT 4,
    description TEXT,
    description_es TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category) REFERENCES categories(id),
    INDEX idx_category (category),
    INDEX idx_difficulty (difficulty),
    FULLTEXT idx_search (name, name_es, description)
);

-- =====================================================
-- INGREDIENTS TABLE
-- =====================================================
CREATE TABLE ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    name_es VARCHAR(200),
    amount DECIMAL(10,2),
    unit VARCHAR(50),
    order_index INT DEFAULT 0,
    
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    INDEX idx_recipe (recipe_id)
);

-- =====================================================
-- STEPS TABLE
-- =====================================================
CREATE TABLE steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id VARCHAR(50) NOT NULL,
    step_number INT NOT NULL,
    instruction TEXT NOT NULL,
    instruction_es TEXT,
    
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    INDEX idx_recipe_step (recipe_id, step_number)
);

-- =====================================================
-- CONVERSATIONS TABLE
-- =====================================================
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id VARCHAR(50),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_updated (updated_at DESC)
);

-- =====================================================
-- MESSAGES TABLE
-- =====================================================
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    role ENUM('user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    INDEX idx_conversation (conversation_id),
    INDEX idx_created (created_at)
);
```

### Table Summary

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | Store user accounts | email, password_hash, name |
| `categories` | Recipe categories | name, name_es, image_url |
| `recipes` | Recipe metadata | name, difficulty, prep_time, cook_time |
| `ingredients` | Recipe ingredients | name, amount, unit |
| `steps` | Cooking instructions | step_number, instruction |
| `conversations` | AI chat sessions | user_id, recipe_id, title |
| `messages` | Chat messages | role, content, conversation_id |

---

## 5. Sequence Diagrams

### Use Case 1: User Registration & Login

```
┌────────┐          ┌──────────┐          ┌──────────┐          ┌──────────┐
│  User  │          │  React   │          │  Flask   │          │   RDS    │
└───┬────┘          └────┬─────┘          └────┬─────┘          └────┬─────┘
    │                    │                     │                     │
    │ 1. Fill register   │                     │                     │
    │    form            │                     │                     │
    │───────────────────>│                     │                     │
    │                    │                     │                     │
    │                    │ 2. POST /auth/register                    │
    │                    │    {email, password, name}                │
    │                    │────────────────────>│                     │
    │                    │                     │                     │
    │                    │                     │ 3. Check if email   │
    │                    │                     │    exists           │
    │                    │                     │────────────────────>│
    │                    │                     │                     │
    │                    │                     │ 4. Email available  │
    │                    │                     │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │                    │                     │                     │
    │                    │                     │ 5. Hash password    │
    │                    │                     │    (bcrypt)         │
    │                    │                     │──┐                  │
    │                    │                     │  │                  │
    │                    │                     │<─┘                  │
    │                    │                     │                     │
    │                    │                     │ 6. INSERT user      │
    │                    │                     │────────────────────>│
    │                    │                     │                     │
    │                    │                     │ 7. User created     │
    │                    │                     │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │                    │                     │                     │
    │                    │ 8. 201 Created      │                     │
    │                    │    {user}           │                     │
    │                    │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                     │
    │                    │                     │                     │
    │ 9. Redirect to     │                     │                     │
    │    login           │                     │                     │
    │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                     │                     │
    │                    │                     │                     │
    │ 10. Enter login    │                     │                     │
    │     credentials    │                     │                     │
    │───────────────────>│                     │                     │
    │                    │                     │                     │
    │                    │ 11. POST /auth/login                      │
    │                    │     {email, password}                     │
    │                    │────────────────────>│                     │
    │                    │                     │                     │
    │                    │                     │ 12. Get user by     │
    │                    │                     │     email           │
    │                    │                     │────────────────────>│
    │                    │                     │                     │
    │                    │                     │ 13. User record     │
    │                    │                     │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │                    │                     │                     │
    │                    │                     │ 14. Verify password │
    │                    │                     │     (bcrypt)        │
    │                    │                     │──┐                  │
    │                    │                     │  │                  │
    │                    │                     │<─┘                  │
    │                    │                     │                     │
    │                    │                     │ 15. Generate JWT    │
    │                    │                     │──┐                  │
    │                    │                     │  │                  │
    │                    │                     │<─┘                  │
    │                    │                     │                     │
    │                    │ 16. 200 OK          │                     │
    │                    │     {access_token,  │                     │
    │                    │      user}          │                     │
    │                    │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                     │
    │                    │                     │                     │
    │                    │ 17. Store JWT in    │                     │
    │                    │     localStorage    │                     │
    │                    │──┐                  │                     │
    │                    │<─┘                  │                     │
    │                    │                     │                     │
    │ 18. Redirect to    │                     │                     │
    │     home (authed)  │                     │                     │
    │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                     │                     │
```

### Use Case 2: Browse Recipes by Category

```
┌────────┐     ┌────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │ CloudFront │     │  React   │     │  Flask   │     │   RDS    │     │    S3    │
└───┬────┘     └─────┬──────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │                │                 │                │                │                │
    │ 1. Visit URL   │                 │                │                │                │
    │───────────────>│                 │                │                │                │
    │                │                 │                │                │                │
    │                │ 2. Serve React  │                │                │                │
    │                │    from S3      │                │                │                │
    │                │────────────────>│                │                │                │
    │                │                 │                │                │                │
    │                │                 │ 3. GET /categories               │                │
    │                │                 │    (with JWT)  │                │                │
    │                │                 │───────────────>│                │                │
    │                │                 │                │                │                │
    │                │                 │                │ 4. SELECT *    │                │
    │                │                 │                │    FROM categories              │
    │                │                 │                │───────────────>│                │
    │                │                 │                │                │                │
    │                │                 │                │ 5. Categories  │                │
    │                │                 │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │                │                 │                │                │                │
    │                │                 │ 6. JSON        │                │                │
    │                │                 │<─ ─ ─ ─ ─ ─ ─ ─│                │                │
    │                │                 │                │                │                │
    │ 7. Click       │                 │                │                │                │
    │   "Lunch"      │                 │                │                │                │
    │────────────────────────────────>│                │                │                │
    │                │                 │                │                │                │
    │                │                 │ 8. GET /recipes│                │                │
    │                │                 │    ?category=lunch              │                │
    │                │                 │───────────────>│                │                │
    │                │                 │                │                │                │
    │                │                 │                │ 9. SELECT *    │                │
    │                │                 │                │    WHERE cat=  │                │
    │                │                 │                │───────────────>│                │
    │                │                 │                │                │                │
    │                │                 │                │ 10. Recipes    │                │
    │                │                 │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │                │                 │                │                │                │
    │                │                 │ 11. JSON       │                │                │
    │                │                 │<─ ─ ─ ─ ─ ─ ─ ─│                │                │
    │                │                 │                │                │                │
    │                │                 │ 12. Load images from S3         │                │
    │                │                 │───────────────────────────────────────────────>│
    │                │                 │                │                │                │
    │ 13. Display    │                 │                │                │                │
    │     recipes    │                 │                │                │                │
    │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                │                │                │
```

### Use Case 3: AI Cooking Assistant with Saved History

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │  React   │     │  Flask   │     │   RDS    │     │  Claude  │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                │                │
    │ 1. View recipe│                │                │                │
    │    detail     │                │                │                │
    │──────────────>│                │                │                │
    │               │                │                │                │
    │ 2. Click      │                │                │                │
    │   "Ask AI"    │                │                │                │
    │──────────────>│                │                │                │
    │               │                │                │                │
    │ 3. Type       │                │                │                │
    │   question    │                │                │                │
    │──────────────>│                │                │                │
    │               │                │                │                │
    │               │ 4. POST /assistant/ask          │                │
    │               │    {recipe_id, question}        │                │
    │               │    Authorization: Bearer JWT    │                │
    │               │───────────────>│                │                │
    │               │                │                │                │
    │               │                │ 5. Verify JWT  │                │
    │               │                │    Get user_id │                │
    │               │                │──┐             │                │
    │               │                │<─┘             │                │
    │               │                │                │                │
    │               │                │ 6. Get recipe  │                │
    │               │                │    context     │                │
    │               │                │───────────────>│                │
    │               │                │                │                │
    │               │                │ 7. Recipe +    │                │
    │               │                │    ingredients │                │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │                │                │
    │               │                │ 8. Create/get  │                │
    │               │                │    conversation│                │
    │               │                │───────────────>│                │
    │               │                │                │                │
    │               │                │ 9. conversation_id               │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │                │                │
    │               │                │ 10. Save user  │                │
    │               │                │     message    │                │
    │               │                │───────────────>│                │
    │               │                │                │                │
    │               │                │ 11. Build prompt with context   │
    │               │                │     POST /messages               │
    │               │                │───────────────────────────────>│
    │               │                │                │                │
    │               │                │ 12. AI response│                │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
    │               │                │                │                │
    │               │                │ 13. Save AI    │                │
    │               │                │     message    │                │
    │               │                │───────────────>│                │
    │               │                │                │                │
    │               │ 14. JSON       │                │                │
    │               │     {response, │                │                │
    │               │      conversation_id}           │                │
    │               │<─ ─ ─ ─ ─ ─ ─ ─│                │                │
    │               │                │                │                │
    │ 15. Display   │                │                │                │
    │     answer    │                │                │                │
    │<─ ─ ─ ─ ─ ─ ─ │                │                │                │
```

### Use Case 4: View Conversation History

```
┌────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User  │     │  React   │     │  Flask   │     │   RDS    │
└───┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
    │               │                │                │
    │ 1. Click      │                │                │
    │   "History"   │                │                │
    │──────────────>│                │                │
    │               │                │                │
    │               │ 2. GET /conversations           │
    │               │    Authorization: Bearer JWT    │
    │               │───────────────>│                │
    │               │                │                │
    │               │                │ 3. SELECT *    │
    │               │                │    WHERE user_id = ?            │
    │               │                │    ORDER BY updated_at DESC     │
    │               │                │───────────────>│                │
    │               │                │                │                │
    │               │                │ 4. Conversation list            │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │                │                │
    │               │ 5. JSON        │                │                │
    │               │    {conversations: [...]}       │
    │               │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │                │
    │ 6. Display    │                │                │
    │    list       │                │                │
    │<─ ─ ─ ─ ─ ─ ─ │                │                │
    │               │                │                │
    │ 7. Click      │                │                │
    │    conversation                │                │
    │──────────────>│                │                │
    │               │                │                │
    │               │ 8. GET /conversations/{id}      │
    │               │───────────────>│                │
    │               │                │                │
    │               │                │ 9. SELECT messages              │
    │               │                │    WHERE conversation_id = ?    │
    │               │                │───────────────>│                │
    │               │                │                │                │
    │               │                │ 10. Messages   │                │
    │               │                │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │                │                │
    │               │ 11. JSON       │                │
    │               │     {conversation, messages}    │
    │               │<─ ─ ─ ─ ─ ─ ─ ─│                │
    │               │                │                │
    │ 12. Display   │                │                │
    │     full chat │                │                │
    │<─ ─ ─ ─ ─ ─ ─ │                │                │
    │               │                │                │
    │ 13. Type new  │                │                │
    │     question  │                │                │
    │──────────────>│                │                │
    │               │                │                │
    │               │ 14. POST /assistant/ask         │
    │               │     {conversation_id, question} │
    │               │───────────────>│                │
    │               │                │                │
    │               │      ... (continues conversation)
```

---

## 6. API Specification

### Base URL

```
Production:  https://api.colombianrecipes.com/api/v1
Development: http://localhost:5000/api/v1
```

### Authentication

| Method | Description |
|--------|-------------|
| Type | JWT (JSON Web Token) |
| Header | `Authorization: Bearer <token>` |
| Expiry | 24 hours |

### Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Server Error |

---

### External API: Claude (Anthropic)

| Attribute | Value |
|-----------|-------|
| Provider | Anthropic |
| Base URL | `https://api.anthropic.com/v1` |
| Endpoint | `POST /messages` |
| Model | `claude-sonnet-4-20250514` |
| Auth | API Key (x-api-key header) |

---

### Internal API Endpoints

#### Authentication Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/auth/register` | POST | No | Create new user account |
| `/auth/login` | POST | No | Login and get JWT token |
| `/auth/logout` | POST | Yes | Invalidate current token |
| `/auth/me` | GET | Yes | Get current user info |

##### POST /auth/register

**Request:**
```json
{
  "email": "alex@example.com",
  "password": "securePassword123",
  "name": "Alex"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "email": "alex@example.com",
      "name": "Alex",
      "created_at": "2025-02-17T10:30:00Z"
    }
  },
  "message": "Registration successful"
}
```

##### POST /auth/login

**Request:**
```json
{
  "email": "alex@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 86400,
    "user": {
      "id": 1,
      "email": "alex@example.com",
      "name": "Alex"
    }
  }
}
```

---

#### Recipe Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/categories` | GET | Yes | List all categories |
| `/recipes` | GET | Yes | List recipes (paginated) |
| `/recipes/{id}` | GET | Yes | Get recipe details |
| `/recipes/search` | GET | Yes | Search recipes |

##### GET /recipes

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| per_page | int | 20 | Items per page (max 50) |
| category | string | — | Filter by category |
| difficulty | string | — | Filter by difficulty |
| lang | string | en | Response language |

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
        "region": "Antioquia",
        "difficulty": "hard",
        "prep_time_minutes": 30,
        "cook_time_minutes": 120,
        "servings": 4,
        "image_url": "https://cdn.example.com/bandeja.jpg"
      }
    ]
  },
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 24,
    "pages": 2
  }
}
```

##### GET /recipes/{id}

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "bandeja-paisa",
    "name": "Bandeja Paisa",
    "category": "lunch",
    "region": "Antioquia",
    "difficulty": "hard",
    "prep_time_minutes": 30,
    "cook_time_minutes": 120,
    "servings": 4,
    "description": "Colombia's most iconic dish...",
    "image_url": "https://cdn.example.com/bandeja.jpg",
    "ingredients": [
      {
        "id": 1,
        "name": "Red beans",
        "amount": 500,
        "unit": "g"
      }
    ],
    "steps": [
      {
        "step_number": 1,
        "instruction": "Soak the beans overnight..."
      }
    ]
  }
}
```

---

#### AI Assistant Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/assistant/ask` | POST | Yes | Ask cooking question |
| `/assistant/substitute` | POST | Yes | Get ingredient substitution |

##### POST /assistant/ask

**Request:**
```json
{
  "recipe_id": "bandeja-paisa",
  "question": "My beans are still hard after 2 hours",
  "conversation_id": null,
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "conversation_id": 42,
    "recipe_id": "bandeja-paisa",
    "response": "Don't worry! Hard beans can happen for a few reasons...",
    "tips": [
      "Add a pinch of baking soda",
      "Don't add salt until the end"
    ]
  }
}
```

---

#### Conversation Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/conversations` | GET | Yes | List user's conversations |
| `/conversations/{id}` | GET | Yes | Get conversation with messages |
| `/conversations/{id}` | DELETE | Yes | Delete conversation |

##### GET /conversations

**Response:**
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "id": 42,
        "recipe_id": "bandeja-paisa",
        "recipe_name": "Bandeja Paisa",
        "title": "Bean cooking questions",
        "message_count": 4,
        "created_at": "2025-02-17T10:30:00Z",
        "updated_at": "2025-02-17T11:45:00Z"
      }
    ]
  },
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 5
  }
}
```

##### GET /conversations/{id}

**Response:**
```json
{
  "success": true,
  "data": {
    "conversation": {
      "id": 42,
      "recipe_id": "bandeja-paisa",
      "recipe_name": "Bandeja Paisa",
      "title": "Bean cooking questions",
      "created_at": "2025-02-17T10:30:00Z"
    },
    "messages": [
      {
        "id": 1,
        "role": "user",
        "content": "My beans are still hard after 2 hours",
        "created_at": "2025-02-17T10:30:00Z"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "Don't worry! Hard beans can happen...",
        "created_at": "2025-02-17T10:30:05Z"
      }
    ]
  }
}
```

---

### API Endpoints Summary

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/auth/register` | POST | ❌ | Create account |
| `/auth/login` | POST | ❌ | Get JWT token |
| `/auth/logout` | POST | ✅ | Invalidate token |
| `/auth/me` | GET | ✅ | Current user |
| `/categories` | GET | ✅ | List categories |
| `/recipes` | GET | ✅ | List recipes |
| `/recipes/{id}` | GET | ✅ | Recipe details |
| `/recipes/search` | GET | ✅ | Search recipes |
| `/assistant/ask` | POST | ✅ | AI question |
| `/assistant/substitute` | POST | ✅ | Substitutions |
| `/conversations` | GET | ✅ | List conversations |
| `/conversations/{id}` | GET | ✅ | Conversation detail |
| `/conversations/{id}` | DELETE | ✅ | Delete conversation |
| `/health` | GET | ❌ | Health check |

---

## 7. SCM Strategy

### Version Control

| Tool | Platform |
|------|----------|
| Git | GitHub |
| Branching | GitHub Flow |

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Main | `main` | `main` |
| Feature | `feature/{desc}` | `feature/user-auth` |
| Bug Fix | `fix/{desc}` | `fix/login-validation` |
| Hotfix | `hotfix/{desc}` | `hotfix/api-crash` |

### Commit Convention

```
<type>(<scope>): <description>

feat(auth): add user registration endpoint
fix(chat): resolve message ordering bug
docs(api): update endpoint documentation
```

### Pull Request Workflow

1. Create feature branch from `main`
2. Make commits with conventional messages
3. Push and create Pull Request
4. Automated tests run
5. Self-review code
6. Squash and merge to `main`
7. Auto-deploy to production

### Branch Protection (main)

- ✅ Require pull request
- ✅ Require status checks to pass
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

| Layer | Test Type | Tool | Target |
|-------|-----------|------|--------|
| Backend | Unit | pytest | 80% |
| Backend | Integration | pytest | 70% |
| Frontend | Unit | Jest | 70% |
| Frontend | Component | RTL | 60% |
| API | E2E | Postman | Critical paths |

### CI/CD Pipeline

```
Push → Lint → Unit Tests → Build → Integration Tests → Deploy
```

| Stage | Trigger | Tools |
|-------|---------|-------|
| Lint | Every push | flake8, eslint |
| Unit Tests | Every push | pytest, jest |
| Build | PR to main | Docker |
| Deploy | Merge to main | AWS |

---

## 9. Sprint Planning

### Overview

| Attribute | Value |
|-----------|-------|
| **Project Start** | Thursday, February 19, 2026 |
| **Project Deadline** | Monday, March 9, 2026 |
| **Total Duration** | 18 days (~2.5 weeks) |
| **Sprint Duration** | 6 days per sprint |
| **Total Sprints** | 3 |
| **Total Hours** | ~148 hours |
| **Avg Hours/Day** | ~8 hours |

### Sprint Timeline

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

### Sprint Details

| Sprint | Dates | Focus | Key Deliverables | Hours |
|--------|-------|-------|------------------|-------|
| 1 | Feb 19-24 | Foundation | Docker, DB tables, Auth API, Recipe API | 50 |
| 2 | Feb 25 - Mar 2 | AI & Conversations | Claude integration, conversation saving, React setup | 50 |
| 3 | Mar 3-9 | Frontend & Deploy | All UI components, AWS deployment | 48 |

### Task Summary by Category

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

---

## 10. Technical Justifications

### Why These Technologies?

| Technology | Justification |
|------------|---------------|
| **Flask** | Lightweight Python framework; existing expertise; fast MVP development |
| **React + TypeScript** | Component-based UI; type safety; large ecosystem; existing skills |
| **MySQL** | Relational data model fits recipes/ingredients; ACID compliance; existing skills |
| **JWT** | Stateless authentication; works well with REST; easy to implement |
| **AWS** | Industry standard; free tier available; learning opportunity for resume |
| **Claude API** | Superior contextual understanding; bilingual support; conversational tone |
| **Docker** | Consistent environments; easy deployment; existing experience |

### Why Save Conversations?

| Benefit | Explanation |
|---------|-------------|
| **User Experience** | Users can reference past cooking help |
| **Context** | AI can understand ongoing cooking session |
| **Learning** | Users build a personal cooking knowledge base |
| **Engagement** | Increases return visits and app stickiness |

### Why JWT Authentication?

| Factor | JWT Advantage |
|--------|---------------|
| Stateless | No server-side session storage needed |
| Scalable | Works across multiple servers |
| Standard | Well-documented, widely supported |
| Portable | Can be used for API and future mobile app |

### Why GitHub Flow?

| Factor | Benefit |
|--------|---------|
| Simplicity | Single main branch, feature branches |
| Solo Developer | Low overhead, easy to manage |
| Continuous Deployment | Merge to main = deploy |

---

## Appendix: Project Structure

```
colombian-recipe-api/
├── README.md                     # This documentation
├── docker-compose.yml            # Local development
├── .env.example                  # Environment template
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
│
├── api/                          # Flask Backend
│   ├── app/
│   │   ├── __init__.py           # App factory
│   │   ├── config.py             # Configuration
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── recipe.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── recipes.py
│   │   │   ├── assistant.py
│   │   │   └── conversations.py
│   │   └── services/
│   │       ├── user_service.py
│   │       ├── recipe_service.py
│   │       ├── ai_service.py
│   │       └── conversation_service.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── RecipeCard/
│   │   │   ├── ChatInterface/
│   │   │   └── ConversationList/
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── HomePage.tsx
│   │   │   ├── RecipeDetailPage.tsx
│   │   │   └── ConversationHistoryPage.tsx
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── hooks/
│   │   └── services/
│   │       └── api.ts
│   ├── Dockerfile
│   └── package.json
│
└── docs/                         # Additional docs
    └── api-spec.md
```

---

## Quick Reference

| Resource | Link |
|----------|------|
| GitHub Repository | `github.com/Alexpena76/colombian-recipe-api` |
| Live Demo | (Coming after Sprint 5) |
| API Base URL | `https://api.colombianrecipes.com/api/v1` |

---

## Final Deliverables Checklist

### Backend
- [ ] User registration/login (JWT)
- [ ] Protected routes
- [ ] Categories endpoint
- [ ] Recipes list/detail/search
- [ ] AI assistant endpoint
- [ ] Conversations CRUD

### Frontend
- [ ] Login/Register pages
- [ ] Protected routes
- [ ] Recipe browsing
- [ ] Recipe detail page
- [ ] AI chat interface
- [ ] Conversation history

### Infrastructure
- [ ] Docker Compose (local)
- [ ] AWS RDS (MySQL)
- [ ] AWS EC2 (API)
- [ ] AWS S3 + CloudFront (React)

### Documentation
- [ ] README
- [ ] API documentation
- [ ] Database schema

---

*This documentation was created as part of the Holberton School MVP project.*

**Ready to build! 🇨🇴🚀**
