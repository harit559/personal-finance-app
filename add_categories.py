"""
One-time script to add default categories to existing users who don't have any.
Run this once: python add_categories.py
"""
from app import create_app
from models import db, User, Category, Account

app = create_app()

with app.app_context():
    # Find users without categories
    users = User.query.all()
    
    for user in users:
        # Check if user has categories
        existing_categories = Category.query.filter_by(user_id=user.id).count()
        
        if existing_categories == 0:
            print(f"Adding categories for user: {user.email}")
            
            default_categories = [
                # Expense categories
                Category(user_id=user.id, name='Groceries', category_type='expense', icon='🛒', color='#22c55e'),
                Category(user_id=user.id, name='Restaurants', category_type='expense', icon='🍕', color='#f97316'),
                Category(user_id=user.id, name='Transport', category_type='expense', icon='🚗', color='#3b82f6'),
                Category(user_id=user.id, name='Entertainment', category_type='expense', icon='🎬', color='#a855f7'),
                Category(user_id=user.id, name='Shopping', category_type='expense', icon='🛍️', color='#ec4899'),
                Category(user_id=user.id, name='Bills', category_type='expense', icon='📄', color='#64748b'),
                Category(user_id=user.id, name='Health', category_type='expense', icon='🏥', color='#ef4444'),
                # Income categories
                Category(user_id=user.id, name='Salary', category_type='income', icon='💰', color='#22c55e'),
                Category(user_id=user.id, name='Freelance', category_type='income', icon='💻', color='#06b6d4'),
                Category(user_id=user.id, name='Gifts', category_type='income', icon='🎁', color='#f43f5e'),
            ]
            db.session.add_all(default_categories)
        else:
            print(f"User {user.email} already has {existing_categories} categories")
    
    db.session.commit()
    print("Done!")
