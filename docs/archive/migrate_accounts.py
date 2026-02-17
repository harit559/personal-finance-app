"""
Migration script to add starting_balance and starting_date to existing accounts.

ARCHIVED: One-time migration. New accounts get these fields by default.
Run only if you have an old database: python migrate_accounts.py
"""
from app import create_app
from models import db, Account, Transaction
from datetime import date
from sqlalchemy import func

app = create_app()

with app.app_context():
    accounts = Account.query.all()
    
    for account in accounts:
        # Check if already has starting_date
        if account.starting_date is not None:
            print(f"✓ {account.name} already migrated")
            continue
        
        print(f"Migrating account: {account.name}")
        
        # Find earliest transaction for this account
        earliest_transaction = Transaction.query \
            .filter_by(account_id=account.id) \
            .order_by(Transaction.date.asc()) \
            .first()
        
        if earliest_transaction:
            # Set starting date to the earliest transaction date
            account.starting_date = earliest_transaction.date
            
            # Calculate starting balance: current balance - sum of all transactions
            total_transactions = db.session.query(func.sum(Transaction.amount)) \
                .filter(Transaction.account_id == account.id) \
                .scalar() or 0
            account.starting_balance = account.balance - total_transactions
        else:
            # No transactions - set starting date to today
            account.starting_date = date.today()
            account.starting_balance = account.balance
        
        print(f"  → Starting date: {account.starting_date}")
        print(f"  → Starting balance: ${account.starting_balance:.2f}")
    
    db.session.commit()
    print("\n✓ Migration complete!")
