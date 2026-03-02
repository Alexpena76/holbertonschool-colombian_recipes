# Sprint 2 Installation Instructions

## Files to Copy

Copy these files to your project:

| Source File | Destination |
|-------------|-------------|
| `ai_service.py` | `api/app/services/ai_service.py` |
| `assistant.py` | `api/app/routes/assistant.py` |
| `conversations.py` | `api/app/routes/conversations.py` |
| `conversation.py` | `api/app/models/conversation.py` |
| `message.py` | `api/app/models/message.py` |
| `env.example` | `.env.example` (replace existing) |

## Step-by-Step Installation

### Step 1: Copy the AI Service
```bash
cp ai_service.py ~/holbertonschool-colombian_recipes/api/app/services/ai_service.py
```

### Step 2: Copy the Routes
```bash
cp assistant.py ~/holbertonschool-colombian_recipes/api/app/routes/assistant.py
cp conversations.py ~/holbertonschool-colombian_recipes/api/app/routes/conversations.py
```

### Step 3: Copy the Models
```bash
cp conversation.py ~/holbertonschool-colombian_recipes/api/app/models/conversation.py
cp message.py ~/holbertonschool-colombian_recipes/api/app/models/message.py
```

### Step 4: Update .env.example
```bash
cp env.example ~/holbertonschool-colombian_recipes/.env.example
```

### Step 5: Add at least ONE API key to your .env file

Edit your `.env` file and add at least one AI provider key:

```bash
nano ~/holbertonschool-colombian_recipes/.env
```

Add one or more of these:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GOOGLE_API_KEY=xxxxx
GROQ_API_KEY=gsk_xxxxx
```

### Step 6: Rebuild and restart
```bash
cd ~/holbertonschool-colombian_recipes
sudo docker-compose down
sudo docker-compose up -d --build
```

## Get Free API Keys

| Provider | Free Tier | Get Key |
|----------|-----------|---------|
| **Groq** (Recommended) | Very generous | https://console.groq.com/keys |
| Claude | $5 credit | https://console.anthropic.com/ |
| OpenAI | $5 credit | https://platform.openai.com/api-keys |
| Gemini | 60 req/min | https://makersuite.google.com/app/apikey |

## Testing in Postman

### 1. Login (get token)
- **POST** `http://localhost:5000/api/v1/auth/login`
- Body: `{"email":"alex@test.com","password":"secret123"}`

### 2. Ask AI Assistant
- **POST** `http://localhost:5000/api/v1/assistant/ask`
- Header: `Authorization: Bearer YOUR_TOKEN`
- Body:
```json
{
  "recipe_id": "bandeja-paisa",
  "question": "My beans are still hard after 2 hours, what should I do?"
}
```

### 3. Get AI Status (see which providers are available)
- **GET** `http://localhost:5000/api/v1/assistant/status`
- Header: `Authorization: Bearer YOUR_TOKEN`

### 4. Get Conversations
- **GET** `http://localhost:5000/api/v1/conversations`
- Header: `Authorization: Bearer YOUR_TOKEN`

### 5. Continue a Conversation
- **POST** `http://localhost:5000/api/v1/assistant/ask`
- Header: `Authorization: Bearer YOUR_TOKEN`
- Body:
```json
{
  "conversation_id": 1,
  "question": "What temperature should the water be?"
}
```

## How the Multi-Provider Fallback Works

```
User Request
     │
     ▼
┌─────────────┐
│  Try Claude │ ──→ Rate Limited? ──→ Next Provider
└─────────────┘
     │ Success
     ▼
┌─────────────┐
│  Try OpenAI │ ──→ Rate Limited? ──→ Next Provider
└─────────────┘
     │ Success
     ▼
┌─────────────┐
│ Try Gemini  │ ──→ Rate Limited? ──→ Next Provider
└─────────────┘
     │ Success
     ▼
┌─────────────┐
│  Try Groq   │ ──→ Rate Limited? ──→ Fallback Response
└─────────────┘
     │ Success
     ▼
   Response!
```

The system automatically:
- Tries providers in order
- Skips rate-limited providers
- Returns which provider answered
- Falls back to a helpful static response if all fail
