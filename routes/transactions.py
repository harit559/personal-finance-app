"""
Transaction Routes - CRUD operations for transactions.

CRUD = Create, Read, Update, Delete
These are the basic operations for any data in your app.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Transaction, Account, Category
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/')
@login_required
def list_transactions():
    """
    List all transactions.
    GET /transactions/
    """
    # Get only this user's accounts
    user_accounts = Account.query.filter_by(user_id=current_user.id).all()
    user_account_ids = [a.id for a in user_accounts]
    
    # Get transactions only from user's accounts, newest first
    transactions = Transaction.query \
        .filter(Transaction.account_id.in_(user_account_ids)) \
        .order_by(Transaction.date.desc()) \
        .all()
    
    return render_template('transactions/list.html', transactions=transactions)


@transactions_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """
    Add a new transaction.
    GET: Show the form
    POST: Process the form and save to database
    """
    if request.method == 'POST':
        # Get data from the form
        amount = float(request.form['amount'])
        description = request.form.get('description', '')
        date_str = request.form['date']
        account_id = int(request.form['account_id'])
        category_id = request.form.get('category_id')
        transaction_type = request.form['type']  # 'income' or 'expense'
        
        # Convert date string to date object
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Make amount negative for expenses
        if transaction_type == 'expense':
            amount = -abs(amount)
        else:
            amount = abs(amount)
        
        # Get location from form
        location = request.form.get('location', '')
        
        # Create new transaction
        transaction = Transaction(
            amount=amount,
            description=description,
            date=date,
            account_id=account_id,
            category_id=int(category_id) if category_id else None,
            location=location
        )
        
        # Update account balance
        account = db.session.get(Account, account_id)
        if account:
            account.balance += amount
        
        # Save to database
        db.session.add(transaction)
        db.session.commit()
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    # GET request - show the form
    # Only show this user's accounts and categories
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('transactions/add.html',
                           accounts=accounts,
                           categories=categories,
                           today=today)


@transactions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    """
    Edit an existing transaction.
    """
    transaction = db.session.get(Transaction, id)
    if not transaction:
        return "Not found", 404
    
    # Make sure this transaction belongs to the current user
    if transaction.account.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    if request.method == 'POST':
        # Store old amount to adjust account balance
        old_amount = transaction.amount
        
        # Update transaction fields
        new_amount = float(request.form['amount'])
        transaction_type = request.form['type']
        
        if transaction_type == 'expense':
            new_amount = -abs(new_amount)
        else:
            new_amount = abs(new_amount)
        
        transaction.amount = new_amount
        transaction.description = request.form.get('description', '')
        transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        transaction.category_id = request.form.get('category_id') or None
        transaction.location = request.form.get('location', '')
        
        # Adjust account balance
        account = db.session.get(Account, transaction.account_id)
        if account:
            account.balance = account.balance - old_amount + new_amount
        
        db.session.commit()
        flash('Transaction updated!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    # Only show this user's accounts and categories
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    return render_template('transactions/edit.html',
                           transaction=transaction,
                           accounts=accounts,
                           categories=categories)


@transactions_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    """
    Delete a transaction.
    Uses POST method for safety (GET requests shouldn't modify data).
    """
    transaction = db.session.get(Transaction, id)
    if not transaction:
        return "Not found", 404
    
    # Make sure this transaction belongs to the current user
    if transaction.account.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('transactions.list_transactions'))
    
    # Reverse the balance change
    account = db.session.get(Account, transaction.account_id)
    if account:
        account.balance -= transaction.amount
    
    db.session.delete(transaction)
    db.session.commit()
    
    flash('Transaction deleted.', 'info')
    return redirect(url_for('transactions.list_transactions'))
