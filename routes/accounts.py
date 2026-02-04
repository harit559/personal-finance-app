"""
Account Routes - Managing financial accounts.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Account

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/')
@login_required
def list_accounts():
    """List all accounts."""
    # Only get this user's accounts
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    total_balance = sum(a.balance for a in accounts)
    
    return render_template('accounts/list.html',
                           accounts=accounts,
                           total_balance=total_balance)


@accounts_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_account():
    """Add a new account."""
    if request.method == 'POST':
        from datetime import datetime
        
        initial_balance = float(request.form.get('balance', 0))
        starting_date_str = request.form['starting_date']
        starting_date = datetime.strptime(starting_date_str, '%Y-%m-%d').date()
        
        account = Account(
            user_id=current_user.id,  # Associate with logged-in user
            name=request.form['name'],
            account_type=request.form['account_type'],
            balance=initial_balance,
            starting_balance=initial_balance,
            starting_date=starting_date,
            currency=request.form.get('currency', 'USD')
        )
        
        db.session.add(account)
        db.session.commit()
        
        flash('Account created!', 'success')
        return redirect(url_for('accounts.list_accounts'))
    
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('accounts/add.html', today=today)


@accounts_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    """Edit an account."""
    account = db.session.get(Account, id)
    if not account:
        return "Not found", 404
    
    # Make sure this account belongs to the current user
    if account.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('accounts.list_accounts'))
    
    if request.method == 'POST':
        account.name = request.form['name']
        account.account_type = request.form['account_type']
        account.currency = request.form.get('currency', 'USD')
        
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('accounts.list_accounts'))
    
    return render_template('accounts/edit.html', account=account)


@accounts_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    """Delete an account and all its transactions."""
    account = db.session.get(Account, id)
    if not account:
        return "Not found", 404
    
    # Make sure this account belongs to the current user
    if account.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('accounts.list_accounts'))
    
    db.session.delete(account)
    db.session.commit()
    
    flash('Account deleted.', 'info')
    return redirect(url_for('accounts.list_accounts'))
