# Deployment Guide

This guide provides detailed instructions for deploying the Carevia application to various platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
  - [Railway](#railway)
  - [Render](#render)
  - [Heroku](#heroku)
  - [AWS/GCP/Azure](#awsgcpazure)
- [Database Setup](#database-setup)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Monitoring](#monitoring)

## Prerequisites

- MongoDB Atlas account (or MongoDB instance)
- Domain name (optional, for production)
- Cloud platform account (Railway, Render, Heroku, etc.)
- Docker installed (for Docker deployment)

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Required
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=<appname>

# Application
ENVIRONMENT=production
API_VERSION=v1

# CORS - Add your production domain
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Optional API Keys
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

# Logging
LOG_LEVEL=INFO
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/frontend/` directory:

```env
VITE_API_URL=https://your-api-domain.com/api/v1
```

## Docker Deployment

### Local Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

### Production Docker Deployment

1. **Build images:**
   ```bash
   docker build -t carevia-backend:latest ./backend
   docker build -t carevia-frontend:latest ./frontend/frontend
   ```

2. **Run containers:**
   ```bash
   # Backend
   docker run -d \\
     --name carevia-backend \\
     -p 8000:8000 \\
     -e MONGO_URI="your_mongo_uri" \\
     -e ENVIRONMENT="production" \\
     -e ALLOWED_ORIGINS="https://your-domain.com" \\
     carevia-backend:latest

   # Frontend
   docker run -d \\
     --name carevia-frontend \\
     -p 80:80 \\
     carevia-frontend:latest
   ```

## Cloud Platform Deployment

### Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Deploy Backend:**
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **Set environment variables in Railway dashboard:**
   - Go to your project → Variables
   - Add all required environment variables

5. **Deploy Frontend:**
   ```bash
   cd frontend/frontend
   railway init
   railway up
   ```

### Render

1. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select `backend` as root directory
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Add environment variables:**
   - Go to Environment tab
   - Add all required variables

3. **Create Static Site for Frontend:**
   - Connect repository
   - Select `frontend/frontend` as root directory
   - Build command: `npm install && npm run build`
   - Publish directory: `dist`

### Heroku

1. **Install Heroku CLI:**
   ```bash
   npm install -g heroku
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create apps:**
   ```bash
   heroku create carevia-backend
   heroku create carevia-frontend
   ```

4. **Deploy Backend:**
   ```bash
   cd backend
   git init
   heroku git:remote -a carevia-backend
   git add .
   git commit -m "Deploy backend"
   git push heroku main
   ```

5. **Set environment variables:**
   ```bash
   heroku config:set MONGO_URI="your_mongo_uri" -a carevia-backend
   heroku config:set ENVIRONMENT="production" -a carevia-backend
   ```

### AWS/GCP/Azure

#### AWS Elastic Beanstalk

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   cd backend
   eb init -p python-3.11 carevia-backend
   ```

3. **Create environment:**
   ```bash
   eb create carevia-backend-env
   ```

4. **Set environment variables:**
   ```bash
   eb setenv MONGO_URI="your_mongo_uri" ENVIRONMENT="production"
   ```

5. **Deploy:**
   ```bash
   eb deploy
   ```

#### Google Cloud Run

1. **Build and push Docker image:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/carevia-backend
   ```

2. **Deploy:**
   ```bash
   gcloud run deploy carevia-backend \\
     --image gcr.io/PROJECT_ID/carevia-backend \\
     --platform managed \\
     --region us-central1 \\
     --allow-unauthenticated \\
     --set-env-vars MONGO_URI="your_mongo_uri"
   ```

#### Azure App Service

1. **Create resource group:**
   ```bash
   az group create --name carevia-rg --location eastus
   ```

2. **Create App Service plan:**
   ```bash
   az appservice plan create --name carevia-plan --resource-group carevia-rg --sku B1 --is-linux
   ```

3. **Create web app:**
   ```bash
   az webapp create --resource-group carevia-rg --plan carevia-plan --name carevia-backend --runtime "PYTHON:3.11"
   ```

4. **Deploy:**
   ```bash
   az webapp up --name carevia-backend --resource-group carevia-rg
   ```

## Database Setup

### MongoDB Atlas

1. **Create a cluster:**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a new cluster (free tier available)

2. **Create database user:**
   - Database Access → Add New Database User
   - Choose password authentication
   - Save credentials securely

3. **Whitelist IP addresses:**
   - Network Access → Add IP Address
   - For development: Add your current IP
   - For production: Add `0.0.0.0/0` (allow from anywhere) or specific IPs

4. **Get connection string:**
   - Clusters → Connect → Connect your application
   - Copy the connection string
   - Replace `<password>` with your database user password

## SSL/TLS Configuration

### Using Let's Encrypt (for self-hosted)

1. **Install Certbot:**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Obtain certificate:**
   ```bash
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

3. **Auto-renewal:**
   ```bash
   sudo certbot renew --dry-run
   ```

### Cloud Platform SSL

Most cloud platforms (Railway, Render, Heroku) provide automatic SSL certificates. Just add your custom domain in the platform settings.

## Monitoring

### Health Checks

The application provides health check endpoints:

- **Backend Health:** `GET /health`
- **Backend Readiness:** `GET /ready`
- **Frontend Health:** `GET /health` (nginx)

### Logging

Logs are written to stdout/stderr and can be viewed:

```bash
# Docker
docker logs carevia-backend

# Railway
railway logs

# Heroku
heroku logs --tail -a carevia-backend
```

### Monitoring Tools

Consider integrating:

- **Sentry** - Error tracking
- **Datadog** - Application monitoring
- **New Relic** - Performance monitoring
- **Prometheus + Grafana** - Metrics and dashboards

## Post-Deployment Checklist

- [ ] Verify environment variables are set correctly
- [ ] Test health check endpoints
- [ ] Verify database connection
- [ ] Test job fetching from external APIs
- [ ] Verify CORS configuration
- [ ] Test frontend can communicate with backend
- [ ] Check application logs for errors
- [ ] Set up monitoring and alerts
- [ ] Configure automatic backups for database
- [ ] Document deployment process for team

## Troubleshooting

### Common Issues

1. **Database Connection Failed:**
   - Verify MONGO_URI is correct
   - Check IP whitelist in MongoDB Atlas
   - Ensure network connectivity

2. **CORS Errors:**
   - Add frontend domain to ALLOWED_ORIGINS
   - Verify environment variable is loaded

3. **Jobs Not Fetching:**
   - Check API keys for Adzuna
   - Verify external API endpoints are accessible
   - Check application logs for errors

4. **Container Won't Start:**
   - Check Docker logs: `docker logs <container-name>`
   - Verify all required environment variables are set
   - Check port conflicts

## Support

For deployment issues, please:
1. Check application logs
2. Verify environment configuration
3. Review this deployment guide
4. Open an issue on GitHub with logs and error messages
