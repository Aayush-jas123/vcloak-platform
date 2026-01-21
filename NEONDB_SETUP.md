# NeonDB Setup Guide for vcloak

## Step 1: Create NeonDB Account

1. Go to https://neon.tech
2. Click "Sign Up" (you can use GitHub to sign in)
3. Verify your email if required

## Step 2: Create a New Project

1. Once logged in, click "Create Project" or "New Project"
2. Project settings:
   - **Project Name**: vcloak
   - **Region**: Choose closest to your location (e.g., US East, EU West)
   - **PostgreSQL Version**: 16 (latest)
   - **Compute Size**: Free tier is fine for now

3. Click "Create Project"

## Step 3: Get Connection String

After creating the project, you'll see a connection string that looks like:

```
postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
```

**Copy this entire connection string!**

## Step 4: Update Local Environment

Update your `backend/.env` file with the NeonDB connection string:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=vcloak-secret-key-2024-change-in-production
JWT_SECRET_KEY=vcloak-jwt-secret-2024-change-in-production
DATABASE_URL=postgresql://your-neondb-connection-string-here
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500
```

## Step 5: Test Connection Locally

1. Install psycopg2 if not already installed:
```powershell
cd backend
.\venv\Scripts\pip.exe install psycopg2-binary
```

2. Restart your Flask server:
```powershell
.\venv\Scripts\python.exe app.py
```

3. The database tables will be created automatically on first run!

## Step 6: Verify Database

You can verify the connection by:

1. Checking the Flask server logs - should see "CREATE TABLE" statements
2. Going to NeonDB dashboard → Tables → You should see:
   - users
   - storage_locations
   - bookings
   - reviews

## Connection String Format

Your NeonDB connection string format:
```
postgresql://[username]:[password]@[host]/[database]?sslmode=require
```

Example:
```
postgresql://myuser:mypassword@ep-cool-cloud-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## Troubleshooting

**Connection Error**: Make sure:
- Connection string is correct
- No extra spaces in the .env file
- psycopg2-binary is installed
- Firewall allows PostgreSQL connections

**SSL Error**: Ensure `?sslmode=require` is at the end of the connection string

**Table Creation Failed**: Check Flask logs for specific error messages

## Next: Deploy to Render

Once NeonDB is working locally, you're ready to deploy to Render!

1. Go to https://render.com
2. Sign up/Login with GitHub
3. Create a new Web Service
4. Connect your vcloak repository
5. Add the NeonDB connection string as an environment variable

---

**Need Help?**
- NeonDB Docs: https://neon.tech/docs
- Check your NeonDB dashboard for connection details
- View Flask server logs for errors
