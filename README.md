# 💰 Harit Finance

A modern personal finance tracking application built with Flask. Track your expenses, income, accounts, and transfers across multiple currencies.

[![Tests](https://img.shields.io/badge/tests-53%2F60%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Flask](https://img.shields.io/badge/flask-3.0-orange)]()

## ✨ Features

- 📊 **Multi-Account Management** - Track bank accounts, savings, cash, credit cards
- 💸 **Transactions** - Record income and expenses with categories
- 🔄 **Transfers** - Move money between accounts seamlessly
- 🌍 **Multi-Currency** - Support for USD, THB, EUR, GBP, JPY, CAD
- 📈 **Dashboard** - Visual overview with charts and statistics
- 🏷️ **Categories** - Organize transactions with custom icons and colors
- 🔐 **Secure** - Password hashing, user data separation, authentication
- ✅ **Tested** - 60 comprehensive unit tests

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Poetry (for dependency management)

### Installation

1. **Clone and enter directory**
   ```bash
   cd /Users/harit/Projects/personal_finance_app
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the application**
   ```bash
   poetry run python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5001
   ```

That's it! 🎉

> **📖 Need more details?** See [QUICK_START.md](QUICK_START.md) for detailed setup instructions.

## 📱 Usage

### Creating Your First Account
1. Register/Login to your account
2. Click "Add Account" 
3. Choose account type (Bank, Savings, Cash, Credit Card)
4. Set initial balance
5. Start tracking!

### Recording Transactions
- **Expense**: `Transactions → Add Transaction → Type: Expense`
- **Income**: `Transactions → Add Transaction → Type: Income`
- **Transfer**: `Transactions → Transfer` (move money between accounts)

### Switching Accounts
When editing a transaction, you can now change which account it belongs to. The balances update automatically!

## 🗂️ Project Structure

```
personal_finance_app/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── models.py               # Database models
├── routes/                 # Application routes
│   ├── auth.py            # Authentication (login/register)
│   ├── accounts.py        # Account management
│   ├── transactions.py    # Transactions & transfers
│   ├── categories.py      # Category management
│   └── main.py            # Dashboard
├── templates/             # HTML templates
├── tests/                 # Unit tests (60 tests)
└── docs/                  # Documentation

```

## 🧪 Testing

Run all tests:
```bash
poetry run pytest tests/ -v
```

Run specific tests:
```bash
# Just transfer feature tests
poetry run pytest tests/test_transactions.py::TestTransferFeature -v

# Just authentication tests
poetry run pytest tests/test_auth.py -v
```

**Test Coverage**: 53/60 tests passing (88%)

> **📖 Learn more:** See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing documentation.

## 🚢 Deployment

Deploy to Render.com:

```bash
# Already configured with render.yaml
# Just push to GitHub and connect to Render
```

The app includes:
- ✅ Auto-configured PostgreSQL database
- ✅ Auto-generated SECRET_KEY
- ✅ Python 3.12 runtime
- ✅ Gunicorn web server

> **📖 Deployment guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📚 Documentation

### Essential Reading
- **[QUICK_START.md](QUICK_START.md)** - Detailed setup instructions
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy to production
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Understanding the test suite

### Reference
- **[POETRY_GUIDE.md](POETRY_GUIDE.md)** - Dependency management
- **[tests/README.md](tests/README.md)** - Test documentation

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Framework** | Flask 3.0 |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **ORM** | SQLAlchemy 2.0 |
| **Authentication** | Flask-Login |
| **Frontend** | Tailwind CSS |
| **Charts** | Chart.js |
| **Testing** | Pytest |
| **Server** | Gunicorn |
| **Deployment** | Render.com |

## 🔐 Security Features

- ✅ Password hashing (PBKDF2-SHA256)
- ✅ User data separation (users can only see their own data)
- ✅ Authentication required for all pages
- ✅ Security headers middleware
- ✅ Session management
- ✅ CSRF protection

## 🎯 Key Features Explained

### Multi-Currency Support
Track accounts in different currencies:
```
USD Account: $1,000
THB Account: ฿35,000
EUR Account: €500
```

### Transfer Between Accounts
New feature! Transfer money between your accounts:
1. Click "Transfer" button
2. Select source and destination accounts
3. Enter amount
4. Creates linked transaction records
5. Balances update automatically

### Account Switching
Edit a transaction and move it to a different account:
- Old account balance adjusts
- New account balance updates
- Transaction history maintained

## 📊 Database Schema

```
User
├── Accounts
│   └── Transactions
└── Categories
    └── Transactions
```

**Relationships:**
- User has many Accounts
- User has many Categories
- Account has many Transactions
- Category has many Transactions

## 🤝 Contributing

This is a personal learning project. Feel free to:
- Report issues
- Suggest features
- Learn from the code
- Fork for your own use

## 📝 License

This is a learning project. Use it as you wish!

## 🙏 Acknowledgments

- Built while learning web development
- Uses industry-standard practices
- Includes comprehensive testing
- Production-ready deployment setup

---

## 📖 Quick Reference

### Common Commands

```bash
# Development
poetry run python app.py              # Run app
poetry run pytest tests/ -v           # Run tests
poetry env info                       # Check Python version

# Dependencies
poetry add <package>                  # Add new package
poetry update                         # Update all packages
poetry show                           # List installed packages

# Production
poetry run gunicorn "app:create_app()"  # Run with Gunicorn
```

### Environment Variables

Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///finance.db     # or PostgreSQL URL
FLASK_ENV=development                 # or production
```

### File Locations

| What | Where |
|------|-------|
| Main app | `app.py` |
| Routes | `routes/*.py` |
| Models | `models.py` |
| Templates | `templates/` |
| Tests | `tests/` |
| Config | `config.py` |

---

**Made with ❤️ while learning Flask**

**Questions?** Check the documentation files above or the code comments.
