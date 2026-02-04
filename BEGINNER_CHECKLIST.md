# Beginner's Deployment Checklist

## Before You Start

This is your simplified, step-by-step checklist. Follow this order!

---

## Phase 1: Make Your App Production-Ready (Do These First)

### Step 1: Create a Strong Secret Key ⚡

```bash
# Run this command in your terminal:
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output. Create a `.env` file (if you don't have one):

```bash
cp .env.example .env
```

Edit `.env` and paste your secret key:
```
SECRET_KEY=your_generated_key_here_should_be_long_and_random
DB_ENCRYPTION_KEY=also_generate_another_key_here
```

**⚠️ IMPORTANT:** Never commit `.env` to GitHub! (It's already in `.gitignore`)

---

### Step 2: Add Production Web Server

Your app currently uses Flask's development server. For production, you need Gunicorn:

```bash
poetry add gunicorn
```

---

### Step 3: Create requirements.txt

Hosting platforms often need `requirements.txt`:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

---

### Step 4: Update config.py for Production

We need to handle production vs development environments better.

---

### Step 5: Test Locally with Gunicorn

Make sure it works before deploying:

```bash
# Create the app instance at module level (needed for Gunicorn)
# Then test:
gunicorn "app:create_app()"
```

Visit `http://localhost:8000` to test.

---

## Phase 2: Choose Your Hosting (Pick ONE)

### Option A: Render.com (Recommended for Beginners)

**Why Render?**
- Free tier (no credit card needed)
- Easiest setup
- Automatic HTTPS
- Free PostgreSQL database

**Steps:**
1. Create account at [render.com](https://render.com)
2. Push your code to GitHub
3. Click "New +" → "Web Service"
4. Connect GitHub repo
5. Render auto-detects everything
6. Add environment variables in dashboard
7. Click "Deploy"

**Time: 15-20 minutes**

---

### Option B: PythonAnywhere

**Why PythonAnywhere?**
- Very beginner-friendly
- Good free tier
- No Git knowledge required

**Steps:**
1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload files via web interface (or use Git)
3. Follow their Flask setup guide
4. Configure in their web dashboard

**Time: 30 minutes**

---

### Option C: Railway.app

**Why Railway?**
- Modern interface
- Very easy
- $5 free credit

**Steps:**
1. Create account at [railway.app](https://railway.app)
2. Connect GitHub
3. Add PostgreSQL
4. Deploy!

**Time: 10 minutes**

---

## Phase 3: After Deployment

### Things to Check:

- [ ] Can you visit your site URL?
- [ ] Can you create a new account?
- [ ] Can you log in?
- [ ] Can you add a transaction?
- [ ] Can you add an account?
- [ ] Does everything look correct (CSS loading)?

### If Something Breaks:

1. **Check the logs** (every platform has a "Logs" section)
2. **Most common issues:**
   - Forgot to set `SECRET_KEY` environment variable
   - Database URL not configured
   - Gunicorn not installed

---

## Phase 4: Security & Maintenance

### Required Security Steps:

1. **Change default secret key** ✅ (you did this in Step 1)
2. **Use HTTPS** ✅ (automatic on most platforms)
3. **Keep dependencies updated:**
   ```bash
   poetry update
   poetry export -f requirements.txt --output requirements.txt --without-hashes
   ```

### Recommended (Do Within First Week):

- [ ] Set up database backups
- [ ] Add your privacy policy page
- [ ] Test on mobile devices
- [ ] Set up error monitoring (Sentry)

---

## Phase 5: Improvements (Optional, Do Later)

### Easy Wins:
- [ ] Add email password reset
- [ ] Add budget alerts
- [ ] Add data export (CSV)
- [ ] Add recurring transactions

### Medium Difficulty:
- [ ] Add charts/graphs
- [ ] Add two-factor authentication
- [ ] Add API for mobile app

---

## Quick Reference: Important Commands

```bash
# Start development server
poetry run python app.py

# Test with production server locally
poetry run gunicorn "app:create_app()"

# Update dependencies
poetry update

# Export requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Run tests
poetry run pytest
```

---

## Getting Help

### Platform-Specific Help:
- **Render:** [render.com/docs](https://render.com/docs)
- **PythonAnywhere:** [help.pythonanywhere.com](https://help.pythonanywhere.com)
- **Railway:** [docs.railway.app](https://docs.railway.app)

### General Help:
- Stack Overflow (tag: flask, python)
- Flask documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- This app is well-commented - read the code!

---

## Your First Deployment Timeline

If you follow this checklist:

- **Preparation:** 15-30 minutes (Steps 1-5)
- **Deployment:** 15-30 minutes (Choose platform, deploy)
- **Testing:** 10-15 minutes (Make sure everything works)
- **Total:** ~1-2 hours for your first deployment

---

## Red Flags (Don't Do These!)

❌ Don't commit `.env` file to GitHub
❌ Don't use SQLite in production (use PostgreSQL)
❌ Don't hardcode passwords or API keys
❌ Don't leave `DEBUG=True` in production
❌ Don't skip HTTPS
❌ Don't forget to backup your database

---

## Success Checklist

You'll know you're successful when:

✅ Your app has a public URL (like `https://yourapp.onrender.com`)
✅ You can access it from any device
✅ Multiple people can use it simultaneously
✅ Data persists (doesn't disappear on restart)
✅ HTTPS lock icon appears in browser
✅ You can log in and use all features

---

**You've got this! Start with Render.com if you're unsure.** 🚀
