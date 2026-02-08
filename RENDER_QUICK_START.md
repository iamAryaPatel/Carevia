# 🚀 Render.com Quick Start - Carevia

## ⚡ 5-Minute Deployment

### 1️⃣ Push to GitHub
```bash
git push origin main
```

### 2️⃣ Deploy Backend
1. Go to https://dashboard.render.com/
2. **New +** → **Web Service**
3. Connect your **carevia** repo
4. Settings:
   - Name: `carevia-backend`
   - Root Directory: `backend`
   - Environment: `Docker`
   - Instance Type: `Free`
5. **Add Environment Variables**:
   ```
   MONGO_URI=mongodb+srv://careviauser:Arya462005@carevia-cluster.7os6oaj.mongodb.net/carevia?retryWrites=true&w=majority&appName=carevia-cluster
   ENVIRONMENT=production
   API_VERSION=v1
   ALLOWED_ORIGINS=*
   LOG_LEVEL=INFO
   ```
6. **Create Web Service**
7. **Copy backend URL**: `https://carevia-backend.onrender.com`

### 3️⃣ Deploy Frontend
1. **New +** → **Web Service** (same repo)
2. Settings:
   - Name: `carevia-frontend`
   - Root Directory: `frontend/frontend`
   - Environment: `Docker`
   - Instance Type: `Free`
3. **Add Environment Variable**:
   ```
   VITE_API_URL=https://YOUR-BACKEND-URL/api/v1
   ```
   (Replace with your actual backend URL!)
4. **Create Web Service**
5. **Copy frontend URL**: `https://carevia-frontend.onrender.com`

### 4️⃣ Update CORS
1. Go to **carevia-backend** → **Environment**
2. Edit `ALLOWED_ORIGINS` to your frontend URL:
   ```
   https://carevia-frontend.onrender.com
   ```
3. Save (auto-redeploys)

### ✅ Done!
Visit your app: `https://carevia-frontend.onrender.com`

---

## 📌 Important Notes

- ⏰ **Free tier sleeps after 15 min** - first request takes ~30s to wake
- 🔄 **Auto-deploys** when you push to GitHub
- 📊 **750 hours/month** per service (enough for 24/7)
- 🔒 **Free HTTPS** included

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check logs in Render dashboard |
| Frontend blank page | Check `VITE_API_URL` is correct |
| CORS errors | Update `ALLOWED_ORIGINS` in backend |
| Slow first load | Normal for free tier after sleep |

---

## 📚 Full Guide
See [RENDER_DEPLOYMENT_GUIDE.md](./RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions.
