# Personal Finance App

A simple personal finance tracking app built with Flask - perfect for learning web development!

## Features

- Track income and expenses
- Manage multiple accounts (bank, cash, credit cards)
- Categorize transactions
- View spending summaries
- Modern, dark-themed UI

## Project Structure

```
personal_finance_app/
├── app.py              # Main entry point - starts the Flask server
├── config.py           # Configuration settings (database path, secret key)
├── models.py           # Database models (User, Account, Transaction, etc.)
├── seed_data.py        # Creates sample data for testing
├── requirements.txt    # Python dependencies
│
├── routes/             # URL handlers (organized by feature)
│   ├── __init__.py
│   ├── main.py         # Home page and dashboard
│   ├── transactions.py # Add, edit, delete transactions
│   └── accounts.py     # Manage accounts
│
├── templates/          # HTML templates (Jinja2)
│   ├── base.html       # Base template with navigation
│   ├── index.html      # Dashboard/home page
│   ├── about.html      # About page
│   ├── transactions/   # Transaction-related pages
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   └── accounts/       # Account-related pages
│       ├── list.html
│       ├── add.html
│       └── edit.html
│
└── finance.db          # SQLite database (created automatically)
```

## Quick Start

### 1. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
python app.py
```

### 4. Open in Browser

Go to: **http://localhost:5000**

## How It Works

### The Request Flow

```
Browser Request → Flask (app.py) → Route Handler → Database Query → HTML Template → Response
```

1. User visits a URL (e.g., `/transactions/add`)
2. Flask matches the URL to a route in `routes/transactions.py`
3. The route function queries the database using models
4. Data is passed to an HTML template
5. Template renders with the data
6. HTML is sent back to the browser

### Key Concepts

- **Flask**: A lightweight web framework for Python
- **SQLAlchemy**: Converts Python classes to database tables (ORM)
- **Jinja2**: Template engine that lets you use Python-like code in HTML
- **Blueprints**: Way to organize routes into separate files

## Next Steps for Learning

1. **Add Authentication**: Let users log in with their own accounts
2. **Add Budgets**: Set monthly spending limits per category
3. **Add Charts**: Visualize spending with Chart.js
4. **Add API**: Create REST endpoints for a mobile app
5. **Add Tests**: Write unit tests for your routes

## Common Commands

```bash
# Run the development server
python app.py

# Reset the database (delete and recreate)
rm finance.db && python app.py

# Install a new package
pip install package_name
pip freeze > requirements.txt
```

## Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Frontend**: HTML, Tailwind CSS
- **Templates**: Jinja2
