# ⚡ Vercel Quick Start - 5 Minutes

## 🎯 Deploy Frontend to Vercel in 5 Steps

### **1️⃣ Sign Up**
- Go to: https://vercel.com
- Click **"Sign Up"** → **"Continue with GitHub"**
- Authorize Vercel

### **2️⃣ Import Project**
- Vercel Dashboard → **"Add New..."** → **"Project"**
- Find **"carevia"** repository
- Click **"Import"**

### **3️⃣ Configure**
- **Root Directory:** `frontend/frontend` ⚠️ IMPORTANT
- **Framework:** Vite (auto-detected)
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### **4️⃣ Add Environment Variable**
- Expand **"Environment Variables"**
- Add:
  ```
  VITE_API_URL=https://YOUR-BACKEND-URL/api/v1
  ```
  Replace with your actual Render backend URL!

### **5️⃣ Deploy**
- Click **"Deploy"**
- Wait 2-5 minutes
- Get your URL: `https://carevia-frontend.vercel.app`

---

## 🔄 Update Backend CORS

1. Render Dashboard → **carevia-backend** → **Environment**
2. Edit `ALLOWED_ORIGINS` to:
   ```
   https://carevia-frontend.vercel.app
   ```
3. Save (auto-redeploys)

---

## ✅ Done!

Your frontend is live on Vercel! 🎉

**Benefits:**
- ✅ No cold starts (unlike Render free tier)
- ✅ Global CDN (super fast)
- ✅ Auto-deploy from GitHub
- ✅ Free forever

---

**Full Guide:** See [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)
