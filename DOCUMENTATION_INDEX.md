# 📚 Harit Finance - Complete Documentation Index

**Quick Links:** [README](README.md) | [Quick Start](QUICK_START.md) | [Deployment](DEPLOYMENT_GUIDE.md) | [Testing](TESTING_GUIDE.md)

---

## 🎯 Start Here

**New to the project?** Follow this path:

1. **[README.md](README.md)** - Project overview and quick start
2. **[QUICK_START.md](QUICK_START.md)** - Detailed setup instructions
3. **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Understanding the tests
4. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy to production

---

## 📖 Documentation by Topic

### 🚀 Getting Started

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[README.md](README.md)** | Project overview, features, quick start | First time here |
| **[QUICK_START.md](QUICK_START.md)** | Detailed installation and setup | Setting up locally |
| **[.env.example](.env.example)** | Environment variable template | Configuration |

### 🧪 Testing

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[TESTING_GUIDE.md](TESTING_GUIDE.md)** | Complete testing guide for beginners | Learning about tests |
| **[TEST_SUMMARY.md](TEST_SUMMARY.md)** | Quick reference of all 60 tests | Quick lookup |
| **[tests/README.md](tests/README.md)** | Technical test documentation | Writing tests |

**Test Files:**
- `tests/test_auth.py` - Authentication tests
- `tests/test_accounts.py` - Account CRUD tests
- `tests/test_transactions.py` - Transaction & transfer tests
- `tests/test_categories.py` - Category tests
- `tests/test_models.py` - Database model tests
- `tests/test_user_separation.py` - Security tests

### 🚢 Deployment

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | Deploy to Render.com | Going to production |
| **[render.yaml](render.yaml)** | Render configuration | Deployment setup |
| **[runtime.txt](runtime.txt)** | Python version for Render | Deployment issues |
| **[Procfile](Procfile)** | Gunicorn configuration | Web server setup |

### 🔧 Development Tools

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[POETRY_GUIDE.md](POETRY_GUIDE.md)** | Using Poetry for dependencies | Managing packages |
| **[pyproject.toml](pyproject.toml)** | Poetry configuration | Adding dependencies |
| **[requirements.txt](requirements.txt)** | Pip dependencies (backup) | Pip installation |

---

## 🗂️ Complete File Reference

### Core Application Files

```
app.py              # Main application entry point
config.py           # Configuration settings (dev/test/prod)
models.py           # Database models (User, Account, Transaction, Category)
utils.py            # Utility functions (currency symbols, etc.)
middleware.py       # Security headers
seed_data.py        # Sample data for development
```

### Routes (URL Handlers)

```
routes/
├── main.py         # Dashboard and home page
├── auth.py         # Login, register, logout
├── accounts.py     # Account CRUD operations
├── transactions.py # Transaction CRUD + transfer feature
└── categories.py   # Category CRUD operations
```

### Templates (HTML)

```
templates/
├── base.html              # Base template with navigation
├── index.html             # Dashboard
├── auth/
│   ├── login.html        # Login page
│   └── register.html     # Registration page
├── accounts/
│   ├── list.html         # View all accounts
│   ├── add.html          # Create account
│   └── edit.html         # Edit account
├── transactions/
│   ├── list.html         # View all transactions
│   ├── add.html          # Record transaction
│   ├── edit.html         # Edit transaction (with account switcher!)
│   └── transfer.html     # Transfer between accounts (NEW!)
└── categories/
    ├── list.html         # View categories
    ├── add.html          # Create category
    ├── edit.html         # Edit category
    └── delete.html       # Delete category (with reassignment)
```

### Tests

```
tests/
├── test_auth.py          # 9 tests - Authentication
├── test_accounts.py      # 11 tests - Account management
├── test_transactions.py  # 13 tests - Transactions & transfers
├── test_categories.py    # 11 tests - Categories
├── test_models.py        # 10 tests - Database models
└── test_user_separation.py  # 10 tests - Security
```

### Configuration Files

```
pyproject.toml      # Poetry dependencies and config
poetry.lock         # Locked dependency versions
requirements.txt    # Pip dependencies (fallback)
runtime.txt         # Python version (3.12)
render.yaml         # Render.com deployment config
Procfile            # Gunicorn web server config
.env.example        # Environment variables template
.env                # Your local environment (not in git)
.gitignore          # Files to exclude from git
.python-version     # Python version for this project
```

---

## 🎯 Common Tasks

### I Want To...

| Task | Documentation | File to Edit |
|------|---------------|--------------|
| **Set up locally** | [QUICK_START.md](QUICK_START.md) | - |
| **Run tests** | [TESTING_GUIDE.md](TESTING_GUIDE.md) | - |
| **Deploy to production** | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | - |
| **Add a new route** | Look at `routes/` examples | Create new file in `routes/` |
| **Add a new page** | Look at `templates/` examples | Create new file in `templates/` |
| **Add a database field** | See `models.py` | Edit `models.py` |
| **Change app name** | - | Edit `templates/base.html` |
| **Add dependency** | [POETRY_GUIDE.md](POETRY_GUIDE.md) | Run `poetry add <package>` |
| **Change currency** | See `utils.py` | Edit `utils.py` |
| **Modify transfer feature** | See `routes/transactions.py` | Edit `routes/transactions.py` |

---

## 🚦 Quick Commands Reference

### Development
```bash
poetry run python app.py              # Run app locally
poetry run pytest tests/ -v           # Run all tests
poetry run pytest tests/ -k transfer  # Run transfer tests only
poetry env info                       # Check Python version
```

### Dependency Management
```bash
poetry install                        # Install all dependencies
poetry add flask-something            # Add new package
poetry update                         # Update all packages
poetry show                           # List installed packages
poetry env list                       # List virtual environments
```

### Testing
```bash
poetry run pytest tests/ -v                          # All tests, verbose
poetry run pytest tests/test_transactions.py -v      # One file
poetry run pytest tests/ -k "transfer" -v            # By keyword
poetry run pytest tests/ -x                          # Stop at first failure
poetry run pytest tests/ --lf                        # Run last failed
```

---

## 📊 Project Statistics

- **Total Lines of Code**: ~3,500
- **Routes**: 25+ endpoints
- **Templates**: 15 HTML files
- **Tests**: 60 comprehensive tests
- **Test Coverage**: 88% (53/60 passing)
- **Documentation**: 6 main guides
- **Supported Currencies**: 6 (USD, THB, EUR, GBP, JPY, CAD)

---

## 🔍 Finding Information

### By Feature

| Feature | Code | Template | Tests |
|---------|------|----------|-------|
| **Authentication** | `routes/auth.py` | `templates/auth/` | `test_auth.py` |
| **Accounts** | `routes/accounts.py` | `templates/accounts/` | `test_accounts.py` |
| **Transactions** | `routes/transactions.py` | `templates/transactions/` | `test_transactions.py` |
| **Transfers** | `routes/transactions.py` | `templates/transactions/transfer.html` | `test_transactions.py` |
| **Categories** | `routes/categories.py` | `templates/categories/` | `test_categories.py` |
| **Dashboard** | `routes/main.py` | `templates/index.html` | - |

### By Technology

| Technology | Where | Documentation |
|------------|-------|---------------|
| **Flask** | `app.py`, `routes/` | [Flask Docs](https://flask.palletsprojects.com/) |
| **SQLAlchemy** | `models.py` | [SQLAlchemy Docs](https://docs.sqlalchemy.org/) |
| **Pytest** | `tests/` | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| **Poetry** | `pyproject.toml` | [POETRY_GUIDE.md](POETRY_GUIDE.md) |
| **Tailwind CSS** | `templates/base.html` | [Tailwind Docs](https://tailwindcss.com/) |

---

## 📝 Documentation Maintenance

### Active Documents (Keep Updated)
- ✅ README.md
- ✅ QUICK_START.md
- ✅ DEPLOYMENT_GUIDE.md
- ✅ TESTING_GUIDE.md
- ✅ TEST_SUMMARY.md
- ✅ POETRY_GUIDE.md
- ✅ This file (DOCUMENTATION_INDEX.md)

### Reference Documents (Update as Needed)
- tests/README.md
- .env.example
- render.yaml
- pyproject.toml

---

## 🆘 Troubleshooting

| Problem | Solution | Documentation |
|---------|----------|---------------|
| **"pytest not found"** | Use `poetry run pytest` | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| **Python version issues** | Check `poetry env info` | [POETRY_GUIDE.md](POETRY_GUIDE.md) |
| **Database errors** | Delete `finance.db`, restart | [QUICK_START.md](QUICK_START.md) |
| **Import errors** | Run `poetry install` | [POETRY_GUIDE.md](POETRY_GUIDE.md) |
| **Deployment fails** | Check logs on Render | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) |
| **Tests failing** | See test output | [TESTING_GUIDE.md](TESTING_GUIDE.md) |

---

## 🎓 Learning Resources

### For Beginners
1. Read [README.md](README.md) - Understand what the app does
2. Follow [QUICK_START.md](QUICK_START.md) - Get it running
3. Read [TESTING_GUIDE.md](TESTING_GUIDE.md) - Understand testing
4. Browse code files with comments

### For Contributors
1. Read all documentation above
2. Run tests: `poetry run pytest tests/ -v`
3. Study test files to understand features
4. Look at `routes/` and `templates/` for patterns

---

**Last Updated**: February 2026  
**App Version**: 1.0.0  
**Python Version**: 3.12  
**Flask Version**: 3.0

---

**Need help?** Check the specific documentation file for your topic, or read the code comments!
