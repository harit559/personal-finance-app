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


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """
    Forgot password page.
    User enters email, receives reset link.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = user.generate_reset_token()
            db.session.commit()
            
            # Send email
            from flask_mail import Message
            from flask import current_app
            from app import mail
            
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            msg = Message(
                subject='Reset Your Password - Harit Finance',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email]
            )
            msg.body = f'''Hello {user.name},

You requested to reset your password. Click the link below to reset it:

{reset_url}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
Harit Finance Team
'''
            msg.html = f'''
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #4f46e5;">Reset Your Password</h2>
    <p>Hello {user.name},</p>
    <p>You requested to reset your password. Click the button below to reset it:</p>
    <p style="margin: 30px 0;">
        <a href="{reset_url}" style="background-color: #4f46e5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
            Reset Password
        </a>
    </p>
    <p style="color: #64748b; font-size: 14px;">This link will expire in 1 hour.</p>
    <p style="color: #64748b; font-size: 14px;">If you didn't request this, please ignore this email.</p>
    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
    <p style="color: #94a3b8; font-size: 12px;">Harit Finance - Your Personal Finance Manager</p>
</div>
'''
            
            try:
                mail.send(msg)
                flash('Password reset link sent! Check your email.', 'success')
            except Exception as e:
                flash(f'Error sending email. Please contact support. Error: {str(e)}', 'error')
                # Clear the token if email fails
                user.clear_reset_token()
                db.session.commit()
        else:
            # Don't reveal if email exists (security best practice)
            flash('If that email exists, a reset link has been sent.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Reset password page.
    User clicks link from email, enters new password.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Find user by token
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Update password
        user.set_password(password)
        user.clear_reset_token()
        db.session.commit()
        
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)
