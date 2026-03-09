# AWS Deployment Guide for Colombian Recipe API

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Route 53  │───▶│ CloudFront  │───▶│     S3      │     │
│  │    (DNS)    │    │    (CDN)    │    │ (Frontend)  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │     ALB     │───▶│    ECS      │───▶│    RDS      │     │
│  │ (API Load   │    │  (Flask)    │    │  (MySQL)    │     │
│  │  Balancer)  │    └─────────────┘    └─────────────┘     │
│  └─────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```

## Option 1: Simple Deployment (EC2 + RDS)

Best for: Learning, small projects, tight budgets

### Step 1: Create RDS MySQL Database

1. Go to AWS Console → RDS → Create Database
2. Choose:
   - Engine: MySQL 8.0
   - Template: Free tier
   - DB Instance: db.t3.micro
   - Storage: 20GB
   - DB name: `colombian_recipes`
   - Master username: `admin`
   - Auto-generate password: Yes
3. VPC: Default
4. Public access: Yes (for setup, disable later)
5. Create database

**Save the endpoint** (e.g., `colombian-db.xxxxx.us-east-1.rds.amazonaws.com`)

### Step 2: Launch EC2 Instance

1. Go to EC2 → Launch Instance
2. Choose:
   - AMI: Ubuntu 24.04 LTS
   - Instance type: t2.micro (free tier)
   - Key pair: Create or select existing
   - Security group: Allow SSH (22), HTTP (80), HTTPS (443), Custom TCP (5000)
3. Launch instance

### Step 3: Connect and Deploy

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose git
sudo usermod -aG docker ubuntu
newgrp docker

# Clone your repo
git clone https://github.com/Alexpena76/holbertonschool-colombian_recipes.git
cd holbertonschool-colombian_recipes

# Create production .env
cat > .env << 'EOF'
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-super-secure-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# RDS Database
DATABASE_URL=mysql+pymysql://admin:YOUR_RDS_PASSWORD@your-rds-endpoint:3306/colombian_recipes

# AI Providers
ANTHROPIC_API_KEY=your-key
OPENAI_API_KEY=your-key
GOOGLE_API_KEY=your-key
GROQ_API_KEY=your-key
EOF

# Build and run (API only, using RDS)
docker-compose -f docker-compose.prod.yml up -d
```

### Step 4: Setup Nginx Reverse Proxy

```bash
sudo apt install -y nginx

sudo tee /etc/nginx/sites-available/colombian-api << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/colombian-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Setup SSL with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Option 2: Production Deployment (ECS + S3 + CloudFront)

Best for: Production, scalability, professional projects

### Prerequisites
- AWS CLI installed and configured
- Domain name (optional but recommended)

### Step 1: Create ECR Repository

```bash
aws ecr create-repository --repository-name colombian-api --region us-east-1
```

### Step 2: Push Docker Image to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t colombian-api ./api
docker tag colombian-api:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/colombian-api:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/colombian-api:latest
```

### Step 3: Create RDS Instance

Same as Option 1, Step 1.

### Step 4: Create ECS Cluster

1. Go to ECS → Create Cluster
2. Choose: Fargate
3. Name: `colombian-cluster`

### Step 5: Create Task Definition

1. ECS → Task Definitions → Create new
2. Choose Fargate
3. Configure:
   - Name: `colombian-api-task`
   - CPU: 0.25 vCPU
   - Memory: 0.5 GB
4. Add container:
   - Name: `colombian-api`
   - Image: `YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/colombian-api:latest`
   - Port: 5000
   - Environment variables: Add all from .env

### Step 6: Create Service

1. ECS → Cluster → Create Service
2. Choose:
   - Launch type: Fargate
   - Task definition: colombian-api-task
   - Service name: colombian-api-service
   - Number of tasks: 2
3. Configure load balancer (ALB)

### Step 7: Deploy Frontend to S3 + CloudFront

```bash
# Build frontend
cd frontend
npm run build

# Create S3 bucket
aws s3 mb s3://colombian-recipes-frontend --region us-east-1

# Enable static hosting
aws s3 website s3://colombian-recipes-frontend --index-document index.html --error-document index.html

# Upload files
aws s3 sync dist/ s3://colombian-recipes-frontend --acl public-read

# Create CloudFront distribution (via console for easier setup)
```

---

## Environment Variables for Production

```env
# Flask
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=generate-a-64-char-random-string
JWT_SECRET_KEY=generate-another-64-char-random-string

# Database (RDS)
DATABASE_URL=mysql+pymysql://admin:password@rds-endpoint:3306/colombian_recipes

# AI Providers
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GOOGLE_API_KEY=xxxxx
GROQ_API_KEY=gsk_xxxxx

# CORS (your frontend domain)
CORS_ORIGINS=https://colombianrecipes.com,https://www.colombianrecipes.com
```

---

## Cost Estimates (Monthly)

### Option 1: EC2 + RDS
- EC2 t2.micro: Free tier (first year) / ~$8.50
- RDS db.t3.micro: Free tier (first year) / ~$15
- **Total: Free → ~$25/month**

### Option 2: ECS + S3 + CloudFront
- ECS Fargate (0.25 vCPU, 0.5GB): ~$10-15
- RDS db.t3.micro: ~$15
- S3 + CloudFront: ~$1-5
- ALB: ~$16
- **Total: ~$45-55/month**

---

## Quick Start Commands

```bash
# Local development
docker-compose up -d

# Production build
docker-compose -f docker-compose.prod.yml build

# View logs
docker-compose logs -f api

# Database backup
docker exec colombian-db mysqldump -u root -p colombian_recipes > backup.sql
```
