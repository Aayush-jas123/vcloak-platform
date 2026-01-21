# vcloak Deployment Guide

## Deploying to Render with NeonDB

### Prerequisites
- GitHub account
- Render account (https://render.com)
- NeonDB account (https://neon.tech)

### Step 1: Set up NeonDB

1. Go to https://neon.tech and create a new project
2. Create a new database called `vcloak`
3. Copy the connection string (it will look like: `postgresql://user:password@host/vcloak`)
4. Save this connection string for later

### Step 2: Push to GitHub

The code is already in your local repository. Push it to GitHub:

```bash
cd d:\project\vcloak
git init
git add .
git commit -m "Initial commit - vcloak luggage storage platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/vcloak.git
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to https://render.com and sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: vcloak
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Instance Type**: Free (or your preferred tier)

5. Add Environment Variables:
   - `SECRET_KEY`: Generate a random string (e.g., use `openssl rand -hex 32`)
   - `JWT_SECRET_KEY`: Generate another random string
   - `DATABASE_URL`: Your NeonDB connection string from Step 1
   - `FLASK_ENV`: `production`
   - `CORS_ORIGINS`: Your frontend URL (e.g., `https://vcloak.onrender.com`)

6. Click "Create Web Service"

### Step 4: Deploy Frontend (Static Site)

Option 1: Deploy frontend separately on Render
1. Click "New +" and select "Static Site"
2. Connect the same GitHub repository
3. Configure:
   - **Name**: vcloak-frontend
   - **Build Command**: Leave empty
   - **Publish Directory**: `frontend`

Option 2: Serve frontend from Flask (simpler)
- The frontend files are already in the `frontend` directory
- Access them via the Render URL + `/frontend/index.html`

### Step 5: Update Frontend API URL

After deployment, update the API URL in `frontend/js/api.js`:

```javascript
const API_BASE_URL = 'https://your-render-app.onrender.com/api';
```

### Environment Variables Reference

Required environment variables for production:

```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://user:password@host/database
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend-url.com
```

### Default Admin Credentials

After first deployment, you can login with:
- Email: `admin@vcloak.com`
- Password: `admin123`

**IMPORTANT**: Change these credentials immediately after first login!

### Troubleshooting

1. **Database connection errors**: Verify your DATABASE_URL is correct
2. **CORS errors**: Make sure CORS_ORIGINS includes your frontend URL
3. **Build failures**: Check the build logs in Render dashboard
4. **Import errors**: Ensure all dependencies are in requirements.txt

### Monitoring

- View logs in Render dashboard
- Monitor database usage in NeonDB dashboard
- Set up health check endpoint: `https://your-app.onrender.com/health`
