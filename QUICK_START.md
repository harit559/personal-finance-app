# 🚀 Harit Finance - Quick Start Guide

**Get up and running in 10 minutes!**

**📚 Navigation:** [README](README.md) | [Documentation Index](DOCUMENTATION_INDEX.md) | [Deployment](DEPLOYMENT_GUIDE.md) | [Testing](TESTING_GUIDE.md)

---

## 📋 Prerequisites

Before you start, make sure you have:

- ✅ **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
- ✅ **Poetry** ([Install guide](POETRY_GUIDE.md))
- ✅ **Git** (for version control)
- ✅ **A text editor** (VS Code, Cursor, etc.)

Check your Python version:
```bash
python3 --version  # Should be 3.10 or higher
```

---

## 🎯 Local Development Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd /Users/harit/Projects/personal_finance_app

# Install all dependencies with Poetry
poetry install
```

This installs Flask, SQLAlchemy, pytest, and all other dependencies.

---

### Step 2: Create Environment File (1 minute)

```bash
# Copy the example file
cp .env.example .env
```

**Generate secret keys:**
```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate DB_ENCRYPTION_KEY  
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Edit `.env` file:**
```env
SECRET_KEY=your_first_generated_key_here
DB_ENCRYPTION_KEY=your_second_generated_key_here
DATABASE_URL=sqlite:///finance.db
FLASK_ENV=development
```

> ⚠️ **Important:** Never commit `.env` to git! It's already in `.gitignore`.

---

### Step 3: Run the Application (1 minute)

```bash
poetry run python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5001
 * Debug mode: on
```

**Open your browser:** http://localhost:5001

---

### Step 4: Create Your Account

1. Click **"Sign Up"**
2. Enter your name, email, and password
3. Click **"Create Account"**
4. You're in! 🎉

---

## 🎮 Using the App

### Create Your First Account

1. Go to **"Accounts"** → **"+ Add Account"**
2. Enter account details:
   - Name: "My Checking"
   - Type: Bank Account
   - Currency: USD
   - Initial Balance: 1000
3. Click **"Create Account"**

### Record a Transaction

1. Go to **"Transactions"** → **"+ Add Transaction"**
2. Choose **Expense** or **Income**
3. Enter amount and details
4. Click **"Add Transaction"**

### Transfer Money ✨ NEW

1. Go to **"Transactions"** → **"💸 Transfer"**
2. Select **From Account** and **To Account**
3. Enter amount
4. Click **"Transfer Money"**

Both account balances update automatically!

### Create Categories

1. Go to **"Categories"** → **"+ Add Category"**
2. Choose type (Expense or Income)
3. Add name and emoji icon (🍔 💰 🏠)
4. Pick a color
5. Click **"Create Category"**

---

## 🧪 Running Tests

Verify everything works:

```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific tests
poetry run pytest tests/test_transactions.py -v

# Run only transfer feature tests
poetry run pytest tests/test_transactions.py::TestTransferFeature -v
```

**Expected:** 53-60 tests passing

> 📖 **Learn more:** See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing information.

---

## 🚢 Deploy to Production

Ready to go live? Follow these steps:

### Quick Deployment Checklist

- [ ] Code is pushed to GitHub
- [ ] Environment variables are set
- [ ] Database is configured
- [ ] SECRET_KEY is secure
- [ ] Tests are passing

> 📖 **Full deployment guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### Deploy to Render.com (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render auto-detects `render.yaml`
   - Click "Create Web Service"

4. **Wait for Deployment**
   - First deployment takes 2-3 minutes
   - Check build logs for progress

5. **Your App is Live!** 🎉
   - Access at: `your-app-name.onrender.com`

---

## 🛠️ Common Tasks

### Update Dependencies

```bash
# Update all packages
poetry update

# Add a new package
poetry add package-name

# Remove a package
poetry remove package-name
```

### Database Tasks

```bash
# Delete database (fresh start)
rm finance.db

# Database will be recreated on next run
poetry run python app.py
```

### Switch Python Version

```bash
# Check current version
poetry env info

# Use different Python version
poetry env use python3.11

# Reinstall dependencies
poetry install
```

---

## 🔧 Development Workflow

### Daily Development

```bash
# 1. Start the app
poetry run python app.py

# 2. Make changes to code
# Edit files in routes/, templates/, models.py

# 3. Test your changes
poetry run pytest tests/ -v

# 4. Commit your work
git add .
git commit -m "Description of changes"
```

### Before Deploying

```bash
# Run tests
poetry run pytest tests/ -v

# Check for linter errors
poetry run flake8 .  # if you have flake8 installed

# Commit everything
git add .
git commit -m "Ready for deployment"
git push
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| **app.py** | Main application entry point |
| **config.py** | Configuration settings |
| **models.py** | Database models |
| **routes/** | URL handlers and business logic |
| **templates/** | HTML pages |
| **tests/** | Unit tests |
| **.env** | Environment variables (local only) |
| **pyproject.toml** | Poetry dependencies |
| **render.yaml** | Deployment configuration |

> 📖 **Complete reference:** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## 🆘 Troubleshooting

### "pytest not found"

**Problem:** Running `pytest` doesn't work  
**Solution:** Use `poetry run pytest tests/ -v`  
**Why:** pytest is in Poetry's virtual environment

### "Database is locked"

**Problem:** Can't write to database  
**Solution:** 
```bash
rm finance.db
poetry run python app.py
```

### "Import Error"

**Problem:** Module not found errors  
**Solution:**
```bash
poetry install  # Reinstall all dependencies
```

### "Port 5001 already in use"

**Problem:** Another app is using port 5001  
**Solution:** Kill the process or change port in `app.py`:
```python
app.run(debug=True, port=5002)  # Use different port
```

### Can't login after deployment

**Problem:** Different SECRET_KEY  
**Solution:** 
- Render auto-generates SECRET_KEY
- Just create a new account
- Old accounts won't work (different encryption key)

---

## 💡 Tips & Best Practices

### Security

✅ **DO:**
- Use strong, random SECRET_KEY in production
- Keep .env file private (never commit)
- Use different SECRET_KEY for dev and production
- Run tests before deploying

❌ **DON'T:**
- Use default secret keys
- Commit .env to git
- Share your SECRET_KEY
- Deploy without testing

### Development

✅ **DO:**
- Run tests frequently
- Commit code regularly
- Write descriptive commit messages
- Test locally before deploying

❌ **DON'T:**
- Skip testing
- Make large uncommitted changes
- Deploy untested code
- Ignore error messages

---

## 🎯 What's Next?

Now that you have the app running:

1. ✅ **Explore Features**
   - Create accounts
   - Record transactions
   - Try the transfer feature
   - Set up categories

2. ✅ **Understand the Code**
   - Read [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
   - Browse `routes/` files
   - Look at `templates/` files
   - Study `tests/` to understand features

3. ✅ **Learn Testing**
   - Read [TESTING_GUIDE.md](TESTING_GUIDE.md)
   - Run individual tests
   - Understand test patterns

4. ✅ **Deploy to Production**
   - Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
   - Set up on Render.com
   - Share with friends!

---

## 📚 Additional Resources

### Documentation
- **[README.md](README.md)** - Project overview
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation map
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing guide
- **[POETRY_GUIDE.md](POETRY_GUIDE.md)** - Dependency management

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Render Documentation](https://render.com/docs)

---

## ✅ Quick Command Reference

```bash
# Development
poetry run python app.py              # Run app
poetry run pytest tests/ -v           # Run all tests
poetry env info                       # Check environment

# Dependencies
poetry install                        # Install dependencies
poetry add <package>                  # Add package
poetry update                         # Update packages

# Database
rm finance.db                         # Delete database
poetry run python app.py              # Recreate database

# Git
git status                            # Check status
git add .                             # Stage changes
git commit -m "message"               # Commit
git push                              # Push to GitHub
```

---

**🎉 Congratulations!** You now have Harit Finance running locally. Happy tracking!

**Questions?** Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for more guides.
