# 🇨🇴 Colombian Recipe API

A REST API for authentic Colombian recipes with an AI-powered cooking assistant.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- 🔐 **User Authentication** - JWT-based registration and login
- 🍲 **Recipe Browsing** - Browse by category, region, or difficulty
- 🔍 **Search** - Find recipes by name or ingredient
- 🤖 **AI Cooking Assistant** - Get real-time help from Claude AI
- 💬 **Conversation History** - Save and continue AI conversations
- 🌐 **Bilingual** - English and Spanish support

## MVP Recipes

| Recipe | Category | Difficulty | Region |
|--------|----------|------------|--------|
| Bandeja Paisa | Lunch | Hard | Antioquia |
| Ajiaco Bogotano | Lunch | Medium | Cundinamarca |
| Colombian Arepas | Breakfast | Easy | Nacional |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/colombian-recipe-api.git
   cd colombian-recipe-api
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values (especially ANTHROPIC_API_KEY)
   ```

3. **Start the containers**
   ```bash
   docker-compose up -d
   ```

4. **Verify it's running**
   ```bash
   curl http://localhost:5000/api/v1/health
   ```

The API is now running at `http://localhost:5000`

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Create account |
| `/api/v1/auth/login` | POST | Login (get JWT) |
| `/api/v1/auth/logout` | POST | Logout |
| `/api/v1/auth/me` | GET | Current user |

### Recipes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/categories` | GET | List categories |
| `/api/v1/recipes` | GET | List recipes |
| `/api/v1/recipes/{id}` | GET | Recipe details |
| `/api/v1/recipes/search?q=` | GET | Search recipes |

### AI Assistant

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/assistant/ask` | POST | Ask cooking question |
| `/api/v1/assistant/substitute` | POST | Get substitutions |

### Conversations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/conversations` | GET | List conversations |
| `/api/v1/conversations/{id}` | GET | Get conversation |
| `/api/v1/conversations/{id}` | DELETE | Delete conversation |

## Usage Examples

### Register a User

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "chef@example.com",
    "password": "secret123",
    "name": "Chef Alex"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "chef@example.com",
    "password": "secret123"
  }'
```

### Get Recipes (with JWT)

```bash
curl http://localhost:5000/api/v1/recipes \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Ask AI Assistant

```bash
curl -X POST http://localhost:5000/api/v1/assistant/ask \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipe_id": "bandeja-paisa",
    "question": "My beans are still hard after 2 hours, what should I do?"
  }'
```

## Project Structure

```
colombian-recipe-api/
├── api/
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   └── services/       # Business logic
│   ├── tests/              # Test files
│   ├── Dockerfile
│   ├── requirements.txt
│   └── init.sql            # Seed data
├── frontend/               # React app (Sprint 3)
├── docker-compose.yml
├── .env.example
└── README.md
```

## Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Database**: MySQL 8.0
- **Auth**: Flask-JWT-Extended, bcrypt
- **AI**: Claude API (Anthropic)
- **Infrastructure**: Docker, AWS (production)

## Development

### Run Tests

```bash
docker-compose exec api pytest
```

### View Logs

```bash
docker-compose logs -f api
```

### Access Database

```bash
docker-compose exec db mysql -u root -p colombian_recipes
```

## Deployment

See [docs/deployment.md](docs/deployment.md) for AWS deployment instructions.

## Author

**Alejandro Pena**

- Holberton School
- February 2025