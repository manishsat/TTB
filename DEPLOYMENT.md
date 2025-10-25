# Deployment Guide

This guide covers deploying the TTB Label Verification application to production.

## Architecture

- **Frontend**: React/Vite app deployed to Vercel
- **Backend**: FastAPI Python app deployed to Railway
- **Database**: None (stateless application)

---

## Backend Deployment (Railway)

### 1. Prerequisites
- GitHub account with the repository
- Railway account (sign up at https://railway.app)

### 2. Deploy Steps

1. **Go to Railway**: https://railway.app
2. **Click "Start a New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose the `TTB` repository**
5. **Configure the service**:
   - Set **Root Directory**: Leave empty (Railway will use repo root)
   - Railway will auto-detect Python and use `nixpacks.toml` config

6. **Add Environment Variables** (if needed):
   ```
   PORT=8000
   PYTHONUNBUFFERED=1
   ```

7. **Deploy**: Railway will automatically:
   - Install Tesseract OCR (via nixpacks.toml)
   - Install Python dependencies
   - Start the FastAPI server
   - Provide a public URL (e.g., `https://your-app.railway.app`)

### 3. Post-Deployment
- Copy the Railway URL (e.g., `https://ttb-production.railway.app`)
- You'll need this for frontend configuration

---

## Frontend Deployment (Vercel)

### 1. Prerequisites
- GitHub account with the repository
- Vercel account (sign up at https://vercel.com)

### 2. Deploy Steps

1. **Go to Vercel**: https://vercel.com
2. **Click "Add New Project"**
3. **Import your GitHub repository** (`TTB`)
4. **Configure the project**:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Add Environment Variable**:
   ```
   VITE_API_URL=https://your-app.railway.app
   ```
   ⚠️ Replace with your actual Railway backend URL

6. **Deploy**: Click "Deploy"
   - Vercel will build and deploy your frontend
   - Provides a URL (e.g., `https://ttb-verification.vercel.app`)

### 3. Post-Deployment
- Test the application at your Vercel URL
- Verify it connects to the Railway backend

---

## Update Backend CORS (Optional but Recommended)

After deployment, update the backend to only allow your Vercel frontend:

Edit `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Your Vercel URL
        "http://localhost:5173"          # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy on Railway (automatic on git push).

---

## Troubleshooting

### Backend Issues

**Tesseract not found**:
- Check Railway build logs
- Ensure `nixpacks.toml` is in repo root
- Verify tesseract is listed in nixPkgs

**Port binding error**:
- Railway sets `$PORT` env variable automatically
- Ensure Procfile uses `--port $PORT`

**500 errors**:
- Check Railway logs: Dashboard → Your Service → Logs
- Look for Python exceptions

### Frontend Issues

**API connection fails**:
- Verify `VITE_API_URL` environment variable in Vercel
- Check Railway URL is correct and accessible
- Check browser console for CORS errors

**Build fails**:
- Check Vercel build logs
- Ensure `frontend/` is set as root directory
- Verify all dependencies in `package.json`

---

## Testing After Deployment

1. **Backend Health Check**: 
   - Visit `https://your-app.railway.app/`
   - Should see: `{"status": "ok", "message": "TTB Label Verification API is running"}`

2. **API Documentation**:
   - Visit `https://your-app.railway.app/docs`
   - Test the `/api/verify` endpoint with a sample image

3. **Full Application**:
   - Visit your Vercel URL
   - Upload a test label from `test_labels/`
   - Verify results display correctly

---

## Maintenance

### Updating the Application

**For code changes**:
1. Push to GitHub main branch
2. Railway auto-deploys backend
3. Vercel auto-deploys frontend

**For environment variables**:
- Railway: Dashboard → Service → Variables
- Vercel: Dashboard → Project → Settings → Environment Variables

### Monitoring

- **Railway**: Dashboard shows CPU, memory, logs
- **Vercel**: Dashboard shows deployment status, build logs
- **Both**: Check error logs regularly

---

## Costs

- **Railway**: Free $5 monthly credit (enough for testing)
- **Vercel**: Free tier (generous limits for personal projects)
- **Total**: $0 for hobbyist/demo use

---

## URLs Reference

After deployment, you'll have:
- **Backend API**: `https://[your-app].railway.app`
- **Frontend App**: `https://[your-app].vercel.app`
- **GitHub Repo**: `https://github.com/manishsat/TTB`

Include all three in your project submission!
