"""
Transaction Routes - CRUD operations for transactions.

CRUD = Create, Read, Update, Delete
These are the basic operations for any data in your app.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Transaction, Account, Category
from utils import get_currency_symbol
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
        amount_str = request.form.get('amount')
        date_str = request.form.get('date')
        if not amount_str or not date_str:
            flash('Amount and date are required.', 'error')
            accounts = Account.query.filter_by(user_id=current_user.id).all()
            categories = Category.query.filter_by(user_id=current_user.id).all()
            today = datetime.now().strftime('%Y-%m-%d')
            return render_template('transactions/add.html',
                                   accounts=accounts, categories=categories, today=today)
        
        amount = float(amount_str)
        description = request.form.get('description', '')
        account_id = int(request.form['account_id'])
        category_id = request.form.get('category_id')
        transaction_type = request.form['type']  # 'income' or 'expense'
        
        # Ownership check: account must belong to current user
        account = db.session.get(Account, account_id)
        if not account or account.user_id != current_user.id:
            flash('Invalid account selected.', 'error')
            return redirect(url_for('transactions.add_transaction'))
        
        # Ownership check: category must belong to current user (if provided)
        if category_id:
            category = db.session.get(Category, int(category_id))
            if not category or category.user_id != current_user.id:
                flash('Invalid category selected.', 'error')
                return redirect(url_for('transactions.add_transaction'))
        
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
        
        # Update account balance (account already validated above)
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
        # Store old values
        old_amount = transaction.amount
        old_account_id = transaction.account_id
        
        # Get new values
        new_amount = float(request.form['amount'])
        transaction_type = request.form['type']
        new_account_id = int(request.form['account_id'])
        
        # Make sure new account belongs to current user
        new_account = db.session.get(Account, new_account_id)
        if not new_account or new_account.user_id != current_user.id:
            flash('Invalid account selected.', 'error')
            return redirect(url_for('transactions.edit_transaction', id=id))
        
        if transaction_type == 'expense':
            new_amount = -abs(new_amount)
        else:
            new_amount = abs(new_amount)
        
        # If account changed, adjust both old and new account balances
        if old_account_id != new_account_id:
            # Reverse the transaction in the old account
            old_account = db.session.get(Account, old_account_id)
            if old_account:
                old_account.balance -= old_amount
            
            # Apply the transaction to the new account
            new_account.balance += new_amount
            
            transaction.account_id = new_account_id
        else:
            # Same account, just adjust the difference
            if new_account:
                new_account.balance = new_account.balance - old_amount + new_amount
        
        # Ownership check: category must belong to current user (if provided)
        new_category_id = request.form.get('category_id')
        if new_category_id:
            cat = db.session.get(Category, int(new_category_id))
            if not cat or cat.user_id != current_user.id:
                flash('Invalid category selected.', 'error')
                return redirect(url_for('transactions.edit_transaction', id=id))
        
        # Update transaction fields
        transaction.amount = new_amount
        transaction.description = request.form.get('description', '')
        transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        transaction.category_id = int(new_category_id) if new_category_id else None
        transaction.location = request.form.get('location', '')
        
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


@transactions_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    """
    Transfer money between accounts.
    GET: Show the transfer form
    POST: Process the transfer
    """
    if request.method == 'POST':
        from_account_id = int(request.form['from_account_id'])
        to_account_id = int(request.form['to_account_id'])
        amount = float(request.form['amount'])
        date_str = request.form['date']
        description = request.form.get('description', '')
        
        # Validate accounts are different
        if from_account_id == to_account_id:
            flash('Cannot transfer to the same account!', 'error')
            return redirect(url_for('transactions.transfer'))
        
        # Get accounts and verify ownership
        from_account = db.session.get(Account, from_account_id)
        to_account = db.session.get(Account, to_account_id)
        
        if not from_account or not to_account:
            flash('Invalid account selected.', 'error')
            return redirect(url_for('transactions.transfer'))
        
        if from_account.user_id != current_user.id or to_account.user_id != current_user.id:
            flash('Access denied.', 'error')
            return redirect(url_for('transactions.transfer'))
        
        # Check sufficient balance
        if from_account.balance < amount:
            flash('Insufficient balance in source account!', 'error')
            return redirect(url_for('transactions.transfer'))
        
        # Convert date
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Create description if not provided
        if not description:
            description = f'Transfer to {to_account.name}'
        
        # Create two transactions: expense from source, income to destination
        # Transaction 1: Debit from source account
        trans_out = Transaction(
            amount=-abs(amount),
            description=f'Transfer to {to_account.name}: {description}',
            date=date,
            account_id=from_account_id,
            category_id=None
        )
        
        # Transaction 2: Credit to destination account
        trans_in = Transaction(
            amount=abs(amount),
            description=f'Transfer from {from_account.name}: {description}',
            date=date,
            account_id=to_account_id,
            category_id=None
        )
        
        # Update balances
        from_account.balance -= amount
        to_account.balance += amount
        
        # Save to database
        db.session.add(trans_out)
        db.session.add(trans_in)
        db.session.commit()
        
        currency_symbol = get_currency_symbol(from_account.currency)
        flash(f'Successfully transferred {currency_symbol}{amount:.2f} from {from_account.name} to {to_account.name}!', 'success')
        return redirect(url_for('transactions.list_transactions'))
    
    # GET request - show the form
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('transactions/transfer.html',
                           accounts=accounts,
                           today=today)
