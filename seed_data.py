"""
Seed Data - Creates sample data for testing.

This runs automatically when the app starts if the database is empty.
It creates a demo user with sample accounts, categories, and transactions
so you can see how the app looks with data.
"""
from models import db, User, Account, Category, Transaction
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random


def create_sample_data():
    """Create sample data if database is empty."""
    
    # Check if we already have data
    if User.query.first() is not None:
        return  # Data already exists, don't duplicate
    
    print("Creating sample data...")
    
    # Create a demo user
    demo_user = User(
        email='demo@example.com',
        password_hash=generate_password_hash('demo123', method='pbkdf2:sha256'),
        name='Jack'  # Using your name!
    )
    db.session.add(demo_user)
    db.session.flush()  # This assigns the ID without committing
    
    # Create sample accounts
    accounts = [
        Account(user_id=demo_user.id, name='Checking Account', account_type='bank', balance=2500.00),
        Account(user_id=demo_user.id, name='Savings', account_type='savings', balance=5000.00),
        Account(user_id=demo_user.id, name='Cash Wallet', account_type='cash', balance=150.00),
    ]
    db.session.add_all(accounts)
    db.session.flush()
    
    # Create expense categories
    expense_categories = [
        Category(user_id=demo_user.id, name='Groceries', category_type='expense', icon='🛒', color='#22c55e'),
        Category(user_id=demo_user.id, name='Restaurants', category_type='expense', icon='🍕', color='#f97316'),
        Category(user_id=demo_user.id, name='Transport', category_type='expense', icon='🚗', color='#3b82f6'),
        Category(user_id=demo_user.id, name='Entertainment', category_type='expense', icon='🎬', color='#a855f7'),
        Category(user_id=demo_user.id, name='Shopping', category_type='expense', icon='🛍️', color='#ec4899'),
        Category(user_id=demo_user.id, name='Bills', category_type='expense', icon='📄', color='#64748b'),
    ]
    
    # Create income categories
    income_categories = [
        Category(user_id=demo_user.id, name='Salary', category_type='income', icon='💰', color='#22c55e'),
        Category(user_id=demo_user.id, name='Freelance', category_type='income', icon='💻', color='#06b6d4'),
        Category(user_id=demo_user.id, name='Gifts', category_type='income', icon='🎁', color='#f43f5e'),
    ]
    
    all_categories = expense_categories + income_categories
    db.session.add_all(all_categories)
    db.session.flush()
    
    # Create sample transactions for the last 30 days
    transactions = []
    checking = accounts[0]
    
    # Sample transaction data
    sample_expenses = [
        (expense_categories[0], 'Weekly groceries', -75.50),
        (expense_categories[0], 'Supermarket', -42.30),
        (expense_categories[1], 'Pizza night', -28.00),
        (expense_categories[1], 'Coffee shop', -6.50),
        (expense_categories[2], 'Gas', -45.00),
        (expense_categories[2], 'Uber ride', -15.00),
        (expense_categories[3], 'Netflix', -15.99),
        (expense_categories[3], 'Movie tickets', -24.00),
        (expense_categories[4], 'New shoes', -89.00),
        (expense_categories[5], 'Electric bill', -120.00),
    ]
    
    # Create transactions over the past 30 days
    today = datetime.now().date()
    
    for i in range(30):
        date = today - timedelta(days=i)
        
        # Add 0-2 random expenses per day
        num_expenses = random.randint(0, 2)
        for _ in range(num_expenses):
            cat, desc, amount = random.choice(sample_expenses)
            # Add some variation to amounts
            amount = round(amount * random.uniform(0.8, 1.2), 2)
            
            transactions.append(Transaction(
                account_id=checking.id,
                category_id=cat.id,
                amount=amount,
                description=desc,
                date=date
            ))
    
    # Add monthly salary at the start of month
    first_of_month = today.replace(day=1)
    transactions.append(Transaction(
        account_id=checking.id,
        category_id=income_categories[0].id,
        amount=3500.00,
        description='Monthly salary',
        date=first_of_month
    ))
    
    db.session.add_all(transactions)
    db.session.commit()
    
    print(f"Created {len(transactions)} sample transactions!")
