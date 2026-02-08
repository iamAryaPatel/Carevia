# 🚀 Deploy Carevia to Render.com - Complete Free Guide

This guide will walk you through deploying your Carevia application to Render.com's free tier.

---

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Render.com account (sign up at https://render.com - it's free!)
- ✅ Your MongoDB connection string (you already have this)
- ✅ Your code pushed to GitHub

---

## 🎯 Deployment Overview

We'll deploy **two services**:
1. **Backend** (FastAPI + Python) - Docker-based
2. **Frontend** (React + Vite) - Docker-based with Nginx

**Total Cost: $0/month** ✨

---

## Step 1: Push Your Code to GitHub

### Option A: If you haven't pushed to GitHub yet

```bash
cd d:\carevia

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Production ready"

# Create a new repository on GitHub at: https://github.com/new
# Name it: carevia (or any name you prefer)
# Then run:

git remote add origin https://github.com/YOUR-USERNAME/carevia.git
git branch -M main
git push -u origin main
```

### Option B: If you already have a GitHub repo

Just make sure your latest code is pushed:

```bash
git add .
git commit -m "Ready for Render deployment"
git push
```

---

## Step 2: Deploy Backend to Render

### 2.1 Create Backend Web Service

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Click **"Build and deploy from a Git repository"** → **Next**
4. **Connect your GitHub repository** (authorize Render if needed)
5. Select your **carevia** repository

### 2.2 Configure Backend Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `carevia-backend` |
| **Region** | Choose closest to you (e.g., Singapore, Oregon) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Environment** | `Docker` |
| **Instance Type** | `Free` |

### 2.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

```
MONGO_URI=mongodb+srv://careviauser:Arya462005@carevia-cluster.7os6oaj.mongodb.net/carevia?retryWrites=true&w=majority&appName=carevia-cluster

ENVIRONMENT=production

API_VERSION=v1

ALLOWED_ORIGINS=*

LOG_LEVEL=INFO
```

> [!IMPORTANT]
> We'll update `ALLOWED_ORIGINS` later with your frontend URL for security.

### 2.4 Deploy Backend

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. **Copy your backend URL** - it will look like:
   ```
   https://carevia-backend.onrender.com
   ```

> [!NOTE]
> Free tier services sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

---

## Step 3: Deploy Frontend to Render

### 3.1 Create Frontend Web Service

1. Go back to **Render Dashboard**
2. Click **"New +"** → **"Web Service"**
3. Select the **same carevia repository**

### 3.2 Configure Frontend Service

| Setting | Value |
|---------|-------|
| **Name** | `carevia-frontend` |
| **Region** | Same as backend |
| **Branch** | `main` |
| **Root Directory** | `frontend/frontend` |
| **Environment** | `Docker` |
| **Instance Type** | `Free` |

### 3.3 Add Frontend Environment Variable

Click **"Advanced"** → **"Add Environment Variable"**

```
VITE_API_URL=https://YOUR-BACKEND-URL/api/v1
```

**Replace `YOUR-BACKEND-URL`** with your actual backend URL from Step 2.4!

Example:
```
VITE_API_URL=https://carevia-backend.onrender.com/api/v1
```

### 3.4 Deploy Frontend

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. **Copy your frontend URL**:
   ```
   https://carevia-frontend.onrender.com
   ```

---

## Step 4: Update CORS Settings

Now that you have your frontend URL, update the backend's CORS settings:

1. Go to **Render Dashboard** → **carevia-backend**
2. Click **"Environment"** in the left sidebar
3. Find **`ALLOWED_ORIGINS`** variable
4. Click **Edit** and change from `*` to your frontend URL:
   ```
   https://carevia-frontend.onrender.com
   ```
5. Click **"Save Changes"**
6. Backend will automatically redeploy

---

## Step 5: Test Your Deployment

### Test Backend

Visit: `https://YOUR-BACKEND-URL/docs`

You should see the FastAPI Swagger documentation.

### Test Frontend

Visit: `https://YOUR-FRONTEND-URL`

You should see your Carevia application!

---

## 🎉 You're Live!

Your application is now deployed and accessible worldwide!

**Backend URL**: `https://carevia-backend.onrender.com`  
**Frontend URL**: `https://carevia-frontend.onrender.com`

---

## 📊 Understanding Render Free Tier

### What You Get (Free Forever)

- ✅ 750 hours/month per service (enough for 1 service running 24/7)
- ✅ Automatic HTTPS/SSL
- ✅ Auto-deploy from GitHub
- ✅ Custom domains (optional)
- ✅ Unlimited bandwidth

### Limitations

- ⚠️ Services **sleep after 15 minutes** of inactivity
- ⚠️ First request after sleep takes **~30 seconds** to wake up
- ⚠️ Limited to **512 MB RAM** per service
- ⚠️ Shared CPU (slower than paid tiers)

### Tips for Free Tier

1. **Keep services awake** (optional):
   - Use a free service like [UptimeRobot](https://uptimerobot.com/) to ping your app every 14 minutes
   - This prevents sleep but uses your 750 hours faster

2. **Monitor usage**:
   - Check dashboard for hours used
   - Free tier = 750 hours/month per service

---

## 🔧 Troubleshooting

### Backend won't start

**Check logs**: Render Dashboard → carevia-backend → Logs

Common issues:
- ❌ Missing environment variables → Add them in Environment tab
- ❌ MongoDB connection failed → Check `MONGO_URI` is correct
- ❌ Port issues → Dockerfile already exposes port 8000 ✅

### Frontend shows blank page

**Check browser console** (F12):
- ❌ API calls failing → Check `VITE_API_URL` is correct
- ❌ CORS errors → Update backend's `ALLOWED_ORIGINS`

### Service is slow

- ⏰ First request after sleep takes ~30 seconds (normal for free tier)
- ⏰ Subsequent requests should be fast

---

## 🔄 Updating Your App

### Automatic Deployment

Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature X"
git push

# Render automatically detects and redeploys!
```

### Manual Deployment

1. Go to Render Dashboard
2. Select your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🌐 Custom Domain (Optional)

Want to use your own domain instead of `.onrender.com`?

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Render Dashboard → Service → Settings
3. Add custom domain
4. Update DNS records as instructed
5. Render provides free SSL automatically!

---

## 💡 Alternative: Use Render Blueprint (Advanced)

You already have a `render.yaml` file! You can deploy both services at once:

1. Go to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Connect your repository
4. Render reads `render.yaml` and creates both services automatically!

> [!TIP]
> You'll still need to manually add the `MONGO_URI` and `VITE_API_URL` values after blueprint deployment.

---

## 📈 Monitoring Your App

### View Logs

**Real-time logs**:
1. Render Dashboard → Select service
2. Click **"Logs"** tab
3. See live application logs

### Metrics

- **Events**: Deployment history
- **Metrics**: CPU, Memory usage (paid tier only)

---

## 🆘 Need Help?

### Render Resources

- 📚 [Render Docs](https://render.com/docs)
- 💬 [Render Community](https://community.render.com/)
- 📧 [Support](https://render.com/support)

### Common Questions

**Q: Can I use PostgreSQL instead of MongoDB?**  
A: Yes! Render offers free PostgreSQL databases (90 days, then you can create a new one).

**Q: How do I add more services?**  
A: Just click "New +" and repeat the process.

**Q: Can I upgrade later?**  
A: Yes! Upgrade to paid tier anytime for better performance and no sleep.

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Frontend deployed on Render
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Backend API tested (`/docs` endpoint)
- [ ] Frontend tested (can access the app)
- [ ] Both services communicate correctly

---

## 🎊 Congratulations!

Your Carevia application is now live and accessible to anyone in the world!

**Share your app**: `https://carevia-frontend.onrender.com`

---

> [!NOTE]
> **Next Steps:**
> - Set up monitoring with UptimeRobot (optional)
> - Add custom domain (optional)
> - Monitor usage in Render dashboard
> - Consider upgrading if you need better performance

**Happy Deploying! 🚀**
