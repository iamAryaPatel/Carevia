# 🚀 Deploy Carevia Frontend to Vercel - Step-by-Step Guide

Vercel is perfect for React/Vite applications and offers the best performance for frontends!

---

## ✨ Why Vercel?

- ✅ **100% Free** for personal projects
- ✅ **Blazing fast** global CDN
- ✅ **No sleep/cold starts** (unlike Render free tier)
- ✅ **Automatic HTTPS**
- ✅ **Auto-deploy** from GitHub
- ✅ **Built specifically for React/Next.js/Vite**

---

## 📋 Prerequisites

- ✅ GitHub account with your code pushed
- ✅ Vercel account (we'll create this in Step 1)
- ✅ Backend deployed (you already have this on Render)

---

## 🎯 Step-by-Step Deployment

### **STEP 1: Create Vercel Account**

1. Go to: **https://vercel.com**
2. Click **"Sign Up"** (top right)
3. Choose **"Continue with GitHub"** (recommended)
4. Authorize Vercel to access your GitHub account
5. You'll be redirected to your Vercel dashboard

---

### **STEP 2: Import Your Project**

#### 2.1 Start New Project

1. On Vercel Dashboard: **https://vercel.com/dashboard**
2. Click **"Add New..."** button (top right)
3. Select **"Project"**

#### 2.2 Import from GitHub

4. You'll see **"Import Git Repository"** section
5. Find your **"carevia"** or **"Carevia"** repository
6. Click **"Import"** next to it

> [!NOTE]
> If you don't see your repository, click **"Adjust GitHub App Permissions"** and grant access to the repo.

---

### **STEP 3: Configure Project Settings**

Vercel will auto-detect your project settings, but let's verify:

#### 3.1 Project Configuration

| Setting | Value |
|---------|-------|
| **Project Name** | `carevia-frontend` (or any name you like) |
| **Framework Preset** | `Vite` (should auto-detect) |
| **Root Directory** | `frontend/frontend` |
| **Build Command** | `npm run build` (auto-detected) |
| **Output Directory** | `dist` (auto-detected) |
| **Install Command** | `npm install` (auto-detected) |

#### 3.2 Set Root Directory

This is **IMPORTANT**:

1. Click **"Edit"** next to **Root Directory**
2. Enter: `frontend/frontend`
3. Click **"Continue"**

---

### **STEP 4: Add Environment Variables**

This is **CRITICAL** for your app to work!

1. Expand **"Environment Variables"** section
2. Click **"Add"** or enter the following:

**Variable 1:**
- **Name:** `VITE_API_URL`
- **Value:** `https://YOUR-BACKEND-URL/api/v1`

**Example:**
```
VITE_API_URL=https://carevia-backend.onrender.com/api/v1
```

> [!IMPORTANT]
> Replace `YOUR-BACKEND-URL` with your actual Render backend URL!

3. Make sure **"Production"**, **"Preview"**, and **"Development"** are all checked
4. Click **"Add"**

---

### **STEP 5: Deploy!**

1. Click **"Deploy"** button at the bottom
2. Vercel will start building your project
3. You'll see a build log with progress
4. Wait **2-5 minutes** for deployment to complete

#### What Happens During Deployment:

- ✅ Clones your GitHub repository
- ✅ Installs dependencies (`npm install`)
- ✅ Builds your project (`npm run build`)
- ✅ Deploys to global CDN
- ✅ Generates a URL for your app

---

### **STEP 6: Get Your Live URL** 🎉

Once deployment completes:

1. You'll see **"Congratulations!"** with confetti 🎊
2. Your app URL will be displayed:
   ```
   https://carevia-frontend.vercel.app
   ```
   or
   ```
   https://carevia-frontend-YOUR-USERNAME.vercel.app
   ```
3. Click **"Visit"** to see your live app!

---

### **STEP 7: Update Backend CORS**

Now that your frontend has a new URL, update your backend:

1. Go to **Render Dashboard**: https://dashboard.render.com/
2. Click on **carevia-backend** service
3. Click **"Environment"** in left sidebar
4. Find **`ALLOWED_ORIGINS`** variable
5. Click **Edit** (pencil icon)
6. Update to your Vercel URL:
   ```
   https://carevia-frontend.vercel.app
   ```
7. Click **"Save Changes"**
8. Backend will auto-redeploy (~2 minutes)

---

### **STEP 8: Test Your Deployment** ✅

1. Visit your Vercel URL
2. You should see your Carevia app load
3. Try searching for jobs
4. Open browser console (F12) to check for errors
5. Verify API calls are working

---

## 🎊 You're Live on Vercel!

Your frontend is now deployed on Vercel's global CDN!

**Your URLs:**
- **Frontend (Vercel):** `https://carevia-frontend.vercel.app`
- **Backend (Render):** `https://carevia-backend.onrender.com`

---

## 🔄 Auto-Deployment

Every time you push to GitHub, Vercel automatically redeploys!

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push

# Vercel automatically detects and redeploys! 🚀
```

You'll get email notifications for each deployment.

---

## ⚙️ Vercel Dashboard Features

### View Deployments

1. Go to: https://vercel.com/dashboard
2. Click on **carevia-frontend** project
3. See all deployments with:
   - ✅ Build logs
   - ✅ Preview URLs
   - ✅ Performance metrics
   - ✅ Analytics

### Preview Deployments

Every Git branch gets its own preview URL automatically!

- **main branch** → Production URL
- **feature branches** → Preview URLs (e.g., `https://carevia-frontend-git-feature-branch.vercel.app`)

---

## 🌐 Custom Domain (Optional)

Want to use your own domain like `carevia.com`?

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Vercel Dashboard → Project → Settings → Domains
3. Click **"Add"**
4. Enter your domain name
5. Follow DNS configuration instructions
6. Vercel provides **free SSL automatically**!

---

## 📊 Performance & Analytics

Vercel provides built-in analytics:

1. Go to your project dashboard
2. Click **"Analytics"** tab
3. See:
   - Page views
   - Top pages
   - Top referrers
   - Real User Metrics (Core Web Vitals)

---

## 🔧 Advanced Configuration

### Update Environment Variables

1. Vercel Dashboard → Project → Settings → Environment Variables
2. Edit or add new variables
3. Redeploy for changes to take effect

### Change Build Settings

1. Vercel Dashboard → Project → Settings → General
2. Update:
   - Build Command
   - Output Directory
   - Install Command
   - Root Directory

### Redeploy Manually

1. Go to Deployments tab
2. Click **"..."** (three dots) on any deployment
3. Select **"Redeploy"**

---

## 🆚 Vercel vs Render (Frontend)

| Feature | Vercel | Render Free |
|---------|--------|-------------|
| **Speed** | ⚡ Instant (CDN) | 🐌 Slow (cold starts) |
| **Sleep** | ❌ Never sleeps | ✅ Sleeps after 15 min |
| **Build Time** | 🚀 2-3 minutes | 🐌 5-10 minutes |
| **Global CDN** | ✅ Yes | ❌ No |
| **Analytics** | ✅ Built-in | ❌ No |
| **Preview URLs** | ✅ Automatic | ❌ Manual |
| **Best For** | Frontend/Static | Full-stack/Docker |

**Recommendation:** Use **Vercel for frontend** + **Render for backend** = Best of both worlds! 🎯

---

## 🆘 Troubleshooting

### Build Fails

**Check build logs:**
1. Vercel Dashboard → Deployments → Click failed deployment
2. View logs to see the error

**Common issues:**
- ❌ Missing dependencies → Check `package.json`
- ❌ TypeScript errors → We already fixed this by removing `tsc -b`
- ❌ Environment variables → Verify `VITE_API_URL` is set

### Frontend Loads but API Calls Fail

**Check browser console (F12):**
- ❌ CORS errors → Update backend `ALLOWED_ORIGINS`
- ❌ Wrong API URL → Check `VITE_API_URL` environment variable
- ❌ Backend sleeping → Wait 30 seconds for Render to wake up

### 404 on Page Refresh

This should be fixed by the `vercel.json` config, but if it happens:
1. Verify `vercel.json` exists in `frontend/frontend/`
2. Redeploy the project

---

## 🎯 Quick Reference

### Deploy Command (if using Vercel CLI)

```bash
# Install Vercel CLI (optional)
npm i -g vercel

# Deploy from terminal
cd d:\carevia\frontend\frontend
vercel

# Deploy to production
vercel --prod
```

### Important URLs

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Documentation:** https://vercel.com/docs
- **Support:** https://vercel.com/support

---

## ✅ Deployment Checklist

- [ ] Vercel account created
- [ ] Project imported from GitHub
- [ ] Root directory set to `frontend/frontend`
- [ ] `VITE_API_URL` environment variable added
- [ ] Deployment completed successfully
- [ ] Frontend URL copied
- [ ] Backend CORS updated with Vercel URL
- [ ] App tested and working
- [ ] Auto-deployment verified (push to GitHub)

---

## 🚀 Next Steps

1. **Monitor Performance:** Check Vercel Analytics
2. **Set Up Alerts:** Configure deployment notifications
3. **Add Custom Domain:** (Optional) Use your own domain
4. **Enable Preview Deployments:** Test features before production

---

## 💡 Pro Tips

1. **Use Preview Deployments:** Every PR gets its own URL for testing
2. **Environment Variables:** Use different values for Preview vs Production
3. **Vercel CLI:** Install for local testing and quick deployments
4. **Edge Functions:** Upgrade to add serverless functions if needed
5. **Image Optimization:** Vercel automatically optimizes images

---

> [!TIP]
> **Vercel is FREE forever for personal projects!** No credit card required. Perfect for portfolios and side projects.

**Happy Deploying! 🎉**
