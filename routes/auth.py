"""
Authentication Routes - Login, Logout, Register.

Handles user authentication using Flask-Login.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Category, Account

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page.
    GET: Show login form
    POST: Process login
    """
    # If already logged in, go to home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to the page they were trying to access, or home
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page.
    GET: Show registration form
    POST: Create new user
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  # Get the user ID before committing
        
        # Create default categories for the new user
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
        
        # Create a default account for the new user
        from datetime import date
        default_account = Account(
            user_id=user.id,
            name='Cash',
            account_type='cash',
            balance=0.0,
            starting_balance=0.0,
            starting_date=date.today()
        )
        db.session.add(default_account)
        
        db.session.commit()
        
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
