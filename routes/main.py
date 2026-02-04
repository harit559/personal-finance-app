"""
Main Routes - Home page and dashboard.

A Blueprint is like a mini-application that groups related routes together.
This makes it easy to organize your code as the app grows.
"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Transaction, Account, Category
from sqlalchemy import func
from datetime import datetime, timedelta
from calendar import monthrange

# Create a blueprint named 'main'
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def index():
    """
    Home page / Dashboard.
    Shows summary of finances: total balance, recent transactions, spending by category.
    """
    # Get month/year from query params (default to current month)
    today = datetime.now()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)
    
    # Calculate first and last day of selected month
    first_of_month = datetime(year, month, 1).date()
    last_day = monthrange(year, month)[1]
    last_of_month = datetime(year, month, last_day).date()
    
    # Calculate previous and next month for navigation
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year
    
    # Check if next month is in the future
    is_current_month = (year == today.year and month == today.month)
    
    # Get only THIS USER's accounts
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    
    # Get this user's account IDs for filtering transactions
    user_account_ids = [a.id for a in accounts]
    
    # Calculate account balances as of the selected month
    total_balance = 0
    for account in accounts:
        # Check if account existed at the end of this month
        if account.starting_date and account.starting_date > last_of_month:
            # Account didn't exist yet - don't include it
            account.balance_at_month = None
        else:
            # Calculate balance at end of selected month
            # Method: Current balance - sum of all transactions after the selected month
            transactions_after = db.session.query(func.sum(Transaction.amount)) \
                .filter(Transaction.account_id == account.id) \
                .filter(Transaction.date > last_of_month) \
                .scalar() or 0
            account.balance_at_month = account.balance - transactions_after
            total_balance += account.balance_at_month
    
    # Get recent transactions (last 10) - only from user's accounts
    recent_transactions = Transaction.query \
        .filter(Transaction.account_id.in_(user_account_ids)) \
        .order_by(Transaction.date.desc()) \
        .limit(10) \
        .all()
    
    # Calculate spending for selected month - only from user's accounts
    monthly_spending = db.session.query(func.sum(Transaction.amount)) \
        .filter(Transaction.account_id.in_(user_account_ids)) \
        .filter(Transaction.amount < 0) \
        .filter(Transaction.date >= first_of_month) \
        .filter(Transaction.date <= last_of_month) \
        .scalar() or 0
    
    monthly_income = db.session.query(func.sum(Transaction.amount)) \
        .filter(Transaction.account_id.in_(user_account_ids)) \
        .filter(Transaction.amount > 0) \
        .filter(Transaction.date >= first_of_month) \
        .filter(Transaction.date <= last_of_month) \
        .scalar() or 0
    
    # Get spending by category for selected month (for pie chart)
    spending_by_category = db.session.query(
        Category.name,
        Category.icon,
        Category.color,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction, Transaction.category_id == Category.id) \
     .filter(Transaction.account_id.in_(user_account_ids)) \
     .filter(Transaction.amount < 0) \
     .filter(Transaction.date >= first_of_month) \
     .filter(Transaction.date <= last_of_month) \
     .group_by(Category.id) \
     .all()
    
    # Prepare chart data
    chart_labels = [f"{row.icon} {row.name}" for row in spending_by_category]
    chart_data = [abs(row.total) for row in spending_by_category]
    chart_colors = [row.color for row in spending_by_category]
    
    # Month name for display
    month_name = first_of_month.strftime('%B %Y')
    
    # Get primary currency from first account or default to USD
    primary_currency = accounts[0].currency if accounts else 'USD'
    
    return render_template('index.html',
                           total_balance=total_balance,
                           accounts=accounts,
                           recent_transactions=recent_transactions,
                           monthly_spending=abs(monthly_spending),
                           monthly_income=monthly_income,
                           chart_labels=chart_labels,
                           chart_data=chart_data,
                           chart_colors=chart_colors,
                           month_name=month_name,
                           prev_month=prev_month,
                           prev_year=prev_year,
                           next_month=next_month,
                           next_year=next_year,
                           is_current_month=is_current_month,
                           primary_currency=primary_currency)


@main_bp.route('/about')
def about():
    """Simple about page."""
    return render_template('about.html')
