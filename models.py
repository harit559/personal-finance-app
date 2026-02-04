"""
Database Models - This is your DATA MODEL.

Each class represents a table in your database.
SQLAlchemy converts these Python classes into SQL tables automatically.

Relationships:
- User has many Accounts
- User has many Categories  
- User has many Budgets
- Account has many Transactions
- Category has many Transactions
- Category has one Budget (optional)
"""
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Create the database instance (will be initialized with the app later)
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User account for the app.
    Each user has their own accounts, categories, and transactions.
    
    UserMixin provides required methods for Flask-Login:
    - is_authenticated: Is the user logged in?
    - is_active: Is the account active?
    - get_id(): Returns the user ID as a string
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships - these let you access related data easily
    # Example: user.accounts returns all accounts for this user
    accounts = db.relationship('Account', backref='user', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Account(db.Model):
    """
    Financial account (bank account, cash wallet, credit card, etc.)
    Users can have multiple accounts to track money in different places.
    """
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Chase Checking", "Cash"
    account_type = db.Column(db.String(50), nullable=False)  # 'bank', 'cash', 'credit', 'savings'
    balance = db.Column(db.Float, default=0.0)  # Current balance
    starting_balance = db.Column(db.Float, default=0.0)  # Initial balance when account was opened
    starting_date = db.Column(db.Date, nullable=True)  # Date when this balance was recorded
    currency = db.Column(db.String(3), default='USD')  # Currency code
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship to transactions
    transactions = db.relationship('Transaction', backref='account', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Account {self.name}>'


class Category(db.Model):
    """
    Transaction category (Food, Transport, Salary, etc.)
    Categories help organize and analyze spending.
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Groceries", "Rent"
    category_type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    icon = db.Column(db.String(50), default='📦')  # Emoji or icon name
    color = db.Column(db.String(7), default='#6366f1')  # Hex color for charts
    
    # Relationships
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    budget = db.relationship('Budget', backref='category', uselist=False)  # One budget per category
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Transaction(db.Model):
    """
    A single financial transaction (income or expense).
    This is the core of the app - every money movement is a transaction.
    """
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    amount = db.Column(db.Float, nullable=False)  # Positive = income, Negative = expense
    description = db.Column(db.String(255))  # Optional note about the transaction
    date = db.Column(db.Date, nullable=False)  # When the transaction happened
    location = db.Column(db.String(100))  #
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Transaction {self.amount} on {self.date}>'


class Budget(db.Model):
    """
    Monthly budget for a category.
    Helps users set spending limits and track if they're staying within budget.
    """
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)  # Budget limit
    period = db.Column(db.String(20), default='monthly')  # 'weekly', 'monthly', 'yearly'
    
    def __repr__(self):
        return f'<Budget {self.amount} for category {self.category_id}>'
