# 📋 Changelog - Harit Finance

All notable changes to this project are documented here.

---

## [1.0.4] - 2026-02-05

### ✨ New Features

#### Password Reset Functionality
- **Added:** Complete "Forgot Password" feature
- **How it works:**
  - User clicks "Forgot Password?" on login page
  - Enters email address
  - Receives password reset link via email
  - Link expires after 1 hour
  - User enters new password
  - Single-use secure tokens
- **Email Support:**
  - Gmail SMTP integration for development
  - Ready for SendGrid migration for production
  - Professional HTML email templates
  - Secure token generation
- **Security Features:**
  - Tokens expire in 1 hour
  - One-time use tokens
  - Secure random token generation (32 characters)
  - Passwords hashed with pbkdf2:sha256
  - Doesn't reveal if email exists (security best practice)

### 🔧 Technical Changes

#### Database Model
- **Updated:** `User` model with reset token fields
  - `reset_token`: Stores secure reset token
  - `reset_token_expires`: Token expiration timestamp
- **Added Methods:**
  - `generate_reset_token()`: Creates secure token
  - `verify_reset_token()`: Validates token and expiration
  - `clear_reset_token()`: Removes token after use

#### Email Configuration
- **Added:** Flask-Mail integration
- **Config:** Email settings in `config.py`
  - `MAIL_SERVER`: SMTP server
  - `MAIL_PORT`: SMTP port (587 for TLS)
  - `MAIL_USE_TLS`: Enable TLS encryption
  - `MAIL_USERNAME`: Email account
  - `MAIL_PASSWORD`: App password or API key
  - `MAIL_DEFAULT_SENDER`: Default sender address

#### New Routes
- **GET/POST** `/auth/forgot-password`: Request password reset
- **GET/POST** `/auth/reset-password/<token>`: Reset password with token

#### New Templates
- **`auth/forgot_password.html`**: Email entry form
- **`auth/reset_password.html`**: New password entry form
- **Updated:** `auth/login.html` with "Forgot password?" link

### 📚 Documentation

- **Added:** `EMAIL_SETUP.md` - Complete Gmail SMTP setup guide
  - Step-by-step instructions
  - 2FA and app password setup
  - Troubleshooting section
  - Security best practices
  - `.env` configuration examples

- **Updated:** `PRODUCTION_OPTIMIZATION.md`
  - Added SendGrid migration guide
  - Comparison: Gmail vs SendGrid
  - Custom domain setup instructions
  - When to switch to SendGrid
  - Migration checklist
  - Added Flask-Migrate setup guide
  - Database migration best practices
  - Step-by-step migration workflow
  - Production deployment with migrations
  - Troubleshooting guide

### 🔒 Security

- **Token Security:**
  - 32-character random tokens (using `secrets.token_urlsafe()`)
  - Stored in database with expiration timestamp
  - Single-use only (cleared after password reset)
  - 1-hour expiration window
- **Email Security:**
  - TLS encryption for email sending
  - App passwords (not real Gmail password)
  - `.env` file for credentials (in `.gitignore`)
- **User Privacy:**
  - Doesn't reveal if email exists in system
  - Generic success message for all submissions

### 🎨 User Experience

- **Intuitive Flow:**
  - "Forgot password?" link prominently placed
  - Clear instructions at each step
  - Professional email design
  - Helpful error messages
  - Password requirements displayed
- **Email Design:**
  - HTML formatted email with styling
  - Clear call-to-action button
  - Fallback plain text version
  - Branded messaging ("Harit Finance")

---

## [1.0.3] - 2026-02-05

### ✨ New Features

#### Smart Category Filtering
- **Added:** Dynamic category filtering in transaction forms
- **How it works:**
  - When "Expense" is selected: Only expense categories show in dropdown
  - When "Income" is selected: Only income categories show in dropdown
  - Categories update instantly when switching transaction type
  - Prevents accidentally selecting wrong category type
- **Benefits:**
  - Cleaner, more intuitive interface
  - Faster data entry (fewer categories to scroll through)
  - Improved data integrity (impossible to select wrong category type)
  - Better user experience
- **Implementation:**
  - JavaScript-based filtering (no page reload needed)
  - Works in both "Add Transaction" and "Edit Transaction" forms
  - Preserves selected category when possible
  - Handles edge cases gracefully (no categories, switching types, etc.)

### 📚 Documentation

- **Added:** `FEATURE_CATEGORY_FILTERING.md` - Comprehensive guide for category filtering feature

---

## [1.0.2] - 2026-02-05

### 🐛 Bug Fixes

#### Content Security Policy (CSP) Configuration
- **Fixed:** CSP blocking Chart.js and Google Fonts from loading
- **Changes:**
  - Added `https://cdn.jsdelivr.net` to `script-src` for Chart.js library
  - Added `https://fonts.googleapis.com` to `style-src` for Google Fonts CSS
  - Added `https://fonts.gstatic.com` to `font-src` for font files
  - Added `https://cdn.jsdelivr.net` to `connect-src` for source maps
  - Updated `middleware.py` with proper CDN allowlist

- **Before:** Browser console showed CSP violations, Chart.js wouldn't load
- **After:** All resources load properly, no CSP errors

### 🎨 Improvements

#### Typography
- **Changed:** Switched from THSarabunNew to Inter font
- **Why:** Better readability, professional appearance, excellent for finance apps
- **Features:**
  - Free & commercial use (SIL Open Font License)
  - Used by GitHub, Figma, Stripe
  - Multiple weights (300-700)
  - Superior number legibility

#### Chart.js Stability
- **Changed:** Using specific version (4.4.1) instead of latest
- **Why:** Ensures stability and compatibility
- **Source:** jsDelivr CDN (fast, reliable)

### 📚 Documentation

#### New Guides Added
- **PRODUCTION_OPTIMIZATION.md**: Complete guide for optimizing Tailwind CSS for production
  - 3 optimization options with pros/cons
  - Performance comparison table
  - Step-by-step instructions
  - Addresses Tailwind CDN warning

- **FONT_RECOMMENDATIONS.md**: Comprehensive font guide
  - 6 best free fonts for finance apps
  - How to switch fonts (takes 2 minutes)
  - Font pairing recommendations
  - Self-hosting instructions

- **CHART_TROUBLESHOOTING.md**: Chart debugging guide
  - Step-by-step troubleshooting
  - Browser console instructions
  - Common issues & solutions
  - Test data scripts

- **RECENT_FIXES.md**: Summary of recent fixes and changes

### 🔒 Security

- **Maintained:** Strict Content Security Policy
- **Added:** Only trusted CDNs (jsdelivr, googleapis, gstatic, tailwindcss)
- **Protected:** XSS, injection attacks, clickjacking still prevented

---

## [1.0.1] - 2026-02-04

### 🐛 Bug Fixes

#### Dashboard Pie Chart Fixed
- **Fixed:** Pie chart not rendering on dashboard
- **Changes:**
  - Added proper container with fixed height for canvas
  - Wrapped chart initialization in `DOMContentLoaded` event
  - Changed `maintainAspectRatio` to `true` with proper `aspectRatio`
  - Fixed currency symbol in tooltip (was hardcoded to `$`)
  - Added defensive checks for empty chart data
  - Improved chart styling and colors
  
- **Before:** Chart wouldn't display or had sizing issues
- **After:** Chart renders properly with correct currency symbols

---

## [1.0.0] - 2026-02-04

### ✨ New Features

#### Transfer Between Accounts
- Transfer money between your accounts seamlessly
- Automatically creates linked transaction records
- Updates both account balances
- Prevents transfers to same account
- Checks for sufficient balance

#### Account Switcher in Edit
- Move transactions between accounts when editing
- Both account balances update correctly
- Maintains transaction history

#### Multi-Currency Support
- Support for USD, THB, EUR, GBP, JPY, CAD
- Currency symbols display correctly throughout app
- Each account can have different currency

### 🎨 Improvements

#### Branding
- Changed app name from "Personal Finance" to "Harit Finance"
- Updated all page titles and headers
- Updated footer with new branding

#### Documentation
- Consolidated 19 markdown files into 8 organized docs
- Created master documentation index
- Added comprehensive testing guide (60 tests)
- Improved cross-references between documents
- Archived old/duplicate documentation

### 🧪 Testing

#### Comprehensive Test Suite
- **60 total tests** covering all backend functionality
- **53 tests passing** (88% success rate)
- Tests for authentication, accounts, transactions, categories
- Tests for new transfer feature
- Security tests for user data separation
- Database model tests

#### Test Files
- `test_auth.py` - Authentication (9 tests)
- `test_accounts.py` - Account CRUD (11 tests)
- `test_transactions.py` - Transactions & transfers (13 tests)
- `test_categories.py` - Categories (11 tests)
- `test_models.py` - Database models (10 tests)
- `test_user_separation.py` - Security (10 tests)

### 📚 Documentation

#### New/Updated Documentation
- `README.md` - Complete project overview
- `DOCUMENTATION_INDEX.md` - Master documentation map
- `QUICK_START.md` - Detailed setup guide
- `TESTING_GUIDE.md` - Beginner-friendly testing guide
- `TEST_SUMMARY.md` - Quick test reference
- `DEPLOYMENT_GUIDE.md` - Production deployment
- `POETRY_GUIDE.md` - Dependency management

### 🔧 Technical Improvements

#### Code Quality
- Industry-standard testing with pytest
- AAA pattern in tests (Arrange, Act, Assert)
- Comprehensive test fixtures
- Edge case coverage
- Security testing

#### Dependencies
- Python 3.12 runtime
- Poetry for dependency management
- Flask 3.0
- SQLAlchemy 2.0
- Pytest 8.0
- All dependencies locked in poetry.lock

### 🚀 Deployment

#### Production Ready
- Configured for Render.com deployment
- Auto-generated SECRET_KEY and DB_ENCRYPTION_KEY
- PostgreSQL database support
- Gunicorn web server
- Environment variable management

---

## How to Use This Changelog

### For Users
- Check what new features are available
- See what bugs were fixed
- Understand version differences

### For Developers
- Track changes between versions
- Understand what was modified
- Reference when debugging

---

## Version Format

We use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** - Incompatible API changes
- **MINOR** - New features (backwards compatible)
- **PATCH** - Bug fixes (backwards compatible)

---

## Links

- **Documentation:** [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Setup Guide:** [QUICK_START.md](QUICK_START.md)
- **Testing:** [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Deployment:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Last Updated:** February 4, 2026
