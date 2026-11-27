# Cloud Deployment Guide: SmartFridge AI

This guide explains how to deploy **SmartFridge AI** using 100% free cloud tiers.

---

## 🏗️ Architecture for Cloud Deployment

```
[Vercel or Netlify (Free)]           [Render or Railway (Free)]
  React Frontend UI        <=======>   FastAPI Backend API
 (https://*.vercel.app)                 (https://*.onrender.com)
                                                 │
                                                 ▼
                                     [Render Free PostgreSQL]
                                       Managed Cloud DB
```

---

## ⚡ Option 1: 1-Click Render Blueprint (Easiest & Fastest)

The repository includes a `render.yaml` blueprint that provisions:
1. **Free PostgreSQL Database** (`smartfridge-db`)
2. **FastAPI Web Service** (`smartfridge-backend`)
3. **React Static Site** (`smartfridge-frontend`)

### Step 1: Push Project to GitHub
1. Create a new GitHub repository at [github.com/new](https://github.com/new) (name it `smartfridge-ai`).
2. Run in your project root terminal:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/smartfridge-ai.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy with Render Blueprint
1. Go to [dashboard.render.com](https://dashboard.render.com) and sign in.
2. Click **New +** -> **Blueprint**.
3. Connect your `smartfridge-ai` GitHub repository.
4. Render will read `render.yaml` and display the database, backend service, and frontend site.
5. Click **Apply**.
6. Render will automatically provision the PostgreSQL database, install Python dependencies, launch FastAPI, build the React frontend, and wire their URLs together!

---

## 🚀 Option 2: Hybrid Setup (Backend on Render + Frontend on Vercel)

This is the standard production setup providing the fastest global CDN performance for your React frontend.

### Part A: Deploy Backend & Database on Render

1. Go to [dashboard.render.com](https://dashboard.render.com).
2. **Create Database**:
   - Click **New +** -> **PostgreSQL**.
   - Name: `smartfridge-db`.
   - Plan: **Free**.
   - Click **Create Database**.
   - Copy the **Internal Database URL** (or External Database URL).

3. **Create Backend Web Service**:
   - Click **New +** -> **Web Service**.
   - Select your GitHub repository (`smartfridge-ai`).
   - Root Directory: `backend`
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

4. **Add Backend Environment Variables** in the Render settings:
   - `ENVIRONMENT` = `production`
   - `DEBUG` = `false`
   - `SECRET_KEY` = `generate-a-random-secure-string-here`
   - `DATABASE_URL` = paste the database URL from step 2
   - `CORS_ORIGINS` = `*` (or your Vercel URL once generated)
   - `SIMULATION_MODE` = `true`

5. Click **Deploy Web Service**.
   - Once deployed, copy your backend URL: e.g., `https://smartfridge-backend.onrender.com`.

---

### Part B: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) and log in with GitHub.
2. Click **Add New...** -> **Project**.
3. Import your `smartfridge-ai` repository.
4. Configure Project:
   - Framework Preset: **Vite**
   - Root Directory: click **Edit** and choose `frontend`.
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Under **Environment Variables**, add:
   - `VITE_API_URL` = `https://smartfridge-backend.onrender.com/api/v1` *(use your actual Render backend URL)*
6. Click **Deploy**.

Within 60 seconds, your frontend will be live on a `https://smartfridge-ai-*.vercel.app` URL, communicating with your live FastAPI backend and PostgreSQL database!

---

## 🔍 Verifying the Cloud Deployment

1. Visit your Vercel/Render frontend URL in your browser.
2. The Live Backend Health widget on the dashboard will turn green:
   - Status: **Operational (healthy)**
   - Backend API: connected to live cloud FastAPI
   - Database: connected to PostgreSQL
3. You can also view the interactive Swagger API documentation at:
   `https://your-backend.onrender.com/api/v1/docs`
