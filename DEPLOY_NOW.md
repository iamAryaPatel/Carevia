# Quick Deployment Guide - Railway

## ✅ Git Repository Updated
Your code is now on GitHub: https://github.com/iamAryaPatel/Carevia.git

## 🚀 Deploy to Railway (Recommended - Free Tier Available)

### Step 1: Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub (it will connect to your repositories)

### Step 2: Deploy Backend

1. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `iamAryaPatel/Carevia`

2. **Configure Backend Service**
   - Railway will auto-detect the Dockerfile
   - Set root directory: `backend`
   - Railway will automatically build and deploy

3. **Add Environment Variables**
   - Go to your backend service → Variables
   - Add these variables:
     ```
     MONGO_URI=mongodb+srv://<username>:<password>@carevia-cluster.7os6oaj.mongodb.net/?appName=carevia-cluster
     ENVIRONMENT=production
     API_VERSION=v1
     ALLOWED_ORIGINS=https://your-frontend-url.railway.app
     LOG_LEVEL=INFO
     ```
   - **IMPORTANT:** Update `ALLOWED_ORIGINS` after you deploy frontend

4. **Get Backend URL**
   - Railway will provide a URL like: `https://carevia-backend-production.up.railway.app`
   - Copy this URL for frontend configuration

### Step 3: Deploy Frontend

1. **Add Another Service**
   - In the same project, click "New Service"
   - Select "Deploy from GitHub repo"
   - Choose `iamAryaPatel/Carevia` again

2. **Configure Frontend Service**
   - Set root directory: `frontend/frontend`
   - Railway will auto-detect Dockerfile

3. **Add Environment Variable**
   - Go to frontend service → Variables
   - Add:
     ```
     VITE_API_URL=https://your-backend-url.railway.app/api/v1
     ```
   - Replace with your actual backend URL from Step 2

4. **Get Frontend URL**
   - Railway will provide: `https://carevia-frontend-production.up.railway.app`

### Step 4: Update CORS

1. Go back to **backend service** → Variables
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS=https://carevia-frontend-production.up.railway.app
   ```
3. Backend will automatically redeploy

### Step 5: Test Your Deployment

1. Visit your frontend URL
2. Jobs should load from the backend
3. Check health: `https://your-backend-url.railway.app/health`
4. View API docs: `https://your-backend-url.railway.app/api/v1/docs`

---

## 🎯 Alternative: Deploy with Render

### Backend (Web Service)
1. Go to [Render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo: `iamAryaPatel/Carevia`
4. Settings:
   - Name: `carevia-backend`
   - Root Directory: `backend`
   - Environment: `Docker`
   - Add environment variables (same as Railway)

### Frontend (Static Site)
1. New → Static Site
2. Connect same repo
3. Settings:
   - Root Directory: `frontend/frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Add environment variable: `VITE_API_URL`

---

## 📋 Post-Deployment Checklist

- [ ] Backend is running (check `/health` endpoint)
- [ ] Frontend loads successfully
- [ ] Jobs are fetching from backend
- [ ] CORS is configured correctly
- [ ] MongoDB connection is working
- [ ] Check logs for any errors

---

## 🆘 Troubleshooting

**Jobs not loading:**
- Check browser console for CORS errors
- Verify `ALLOWED_ORIGINS` includes your frontend URL
- Check backend logs in Railway/Render

**Database connection failed:**
- Verify `MONGO_URI` is correct
- Check MongoDB Atlas IP whitelist (add `0.0.0.0/0` for cloud deployments)

**Build failed:**
- Check deployment logs
- Verify Dockerfile paths are correct
- Ensure all dependencies are in requirements.txt

---

## 🎉 Your Application is Production-Ready!

All code improvements are complete and pushed to GitHub. Follow the steps above to deploy to Railway or Render in minutes!
