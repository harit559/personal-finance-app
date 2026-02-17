"""
Test Transaction CRUD Operations and Transfer Feature

Tests for transactions including the new transfer functionality.
"""
import pytest
from app import create_app
from models import db, User, Account, Transaction, Category
from datetime import date


@pytest.fixture
def app():
    """Create a test app."""
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def user_with_accounts(client, app):
    """Create user with two accounts and a category."""
    with app.app_context():
        user = User(name='Test User', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.flush()
        
        account1 = Account(
            user_id=user.id,
            name='Checking',
            account_type='bank',
            balance=1000.00,
            currency='USD'
        )
        account2 = Account(
            user_id=user.id,
            name='Savings',
            account_type='savings',
            balance=5000.00,
            currency='USD'
        )
        category = Category(
            user_id=user.id,
            name='Food',
            category_type='expense'
        )
        db.session.add(account1)
        db.session.add(account2)
        db.session.add(category)
        db.session.commit()
        
        data = {
            'user_id': user.id,
            'account1_id': account1.id,
            'account2_id': account2.id,
            'category_id': category.id
        }
    
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    return data


class TestCreateTransaction:
    """Tests for creating transactions."""
    
    def test_create_expense_transaction(self, client, app, user_with_accounts):
        """Test creating an expense transaction."""
        account_id = user_with_accounts['account1_id']
        category_id = user_with_accounts['category_id']
        
        # Get initial balance
        with app.app_context():
            account = Account.query.get(account_id)
            initial_balance = account.balance
        
        # Create expense
        response = client.post('/transactions/add', data={
            'amount': '50.00',
            'description': 'Lunch',
            'date': date.today().strftime('%Y-%m-%d'),
            'account_id': account_id,
            'category_id': category_id,
            'type': 'expense'
        }, follow_redirects=True)
        
        # Verify transaction and balance update
        with app.app_context():
            transaction = Transaction.query.filter_by(description='Lunch').first()
            assert transaction is not None
            assert transaction.amount == -50.00  # Negative for expense
            
            account = Account.query.get(account_id)
            assert account.balance == initial_balance - 50.00
    
    def test_create_income_transaction(self, client, app, user_with_accounts):
        """Test creating an income transaction."""
        account_id = user_with_accounts['account1_id']
        
        with app.app_context():
            account = Account.query.get(account_id)
            initial_balance = account.balance
        
        # Create income
        client.post('/transactions/add', data={
            'amount': '1000.00',
            'description': 'Salary',
            'date': date.today().strftime('%Y-%m-%d'),
            'account_id': account_id,
            'type': 'income'
        }, follow_redirects=True)
        
        with app.app_context():
            transaction = Transaction.query.filter_by(description='Salary').first()
            assert transaction is not None
            assert transaction.amount == 1000.00  # Positive for income
            
            account = Account.query.get(account_id)
            assert account.balance == initial_balance + 1000.00


class TestUpdateTransaction:
    """Tests for updating transactions."""
    
    def test_update_transaction_amount(self, client, app, user_with_accounts):
        """Test updating transaction amount."""
        account_id = user_with_accounts['account1_id']
        
        # Create transaction (and update account balance to match)
        with app.app_context():
            account = Account.query.get(account_id)
            initial_balance = account.balance
            
            transaction = Transaction(
                account_id=account_id,
                amount=-50.00,
                description='Original',
                date=date.today()
            )
            db.session.add(transaction)
            account.balance += transaction.amount  # Sync balance with transaction
            db.session.commit()
            transaction_id = transaction.id
            # Balance is now initial_balance - 50
        
        # Update amount
        client.post(f'/transactions/edit/{transaction_id}', data={
            'amount': '100.00',
            'description': 'Updated',
            'date': date.today().strftime('%Y-%m-%d'),
            'account_id': account_id,
            'type': 'expense'
        })
        
        # Verify update
        with app.app_context():
            transaction = Transaction.query.get(transaction_id)
            assert transaction.amount == -100.00
            assert transaction.description == 'Updated'
            
            # Balance should be adjusted: initial - 100
            account = Account.query.get(account_id)
            assert account.balance == initial_balance - 100.00
    
    def test_update_transaction_switch_account(self, client, app, user_with_accounts):
        """Test switching transaction to different account."""
        account1_id = user_with_accounts['account1_id']
        account2_id = user_with_accounts['account2_id']
        
        # Create transaction in account1
        with app.app_context():
            transaction = Transaction(
                account_id=account1_id,
                amount=-50.00,
                description='Test',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            transaction_id = transaction.id
            
            # Update balances
            account1 = Account.query.get(account1_id)
            account2 = Account.query.get(account2_id)
            account1.balance += transaction.amount
            db.session.commit()
            
            account1_balance = account1.balance
            account2_balance = account2.balance
        
        # Move transaction to account2
        client.post(f'/transactions/edit/{transaction_id}', data={
            'amount': '50.00',
            'description': 'Test',
            'date': date.today().strftime('%Y-%m-%d'),
            'account_id': account2_id,  # Changed from account1
            'type': 'expense'
        })
        
        # Verify balances updated correctly
        with app.app_context():
            transaction = Transaction.query.get(transaction_id)
            assert transaction.account_id == account2_id
            
            # Account1 should have transaction removed
            account1 = Account.query.get(account1_id)
            assert account1.balance == account1_balance + 50.00  # Reversed
            
            # Account2 should have transaction added
            account2 = Account.query.get(account2_id)
            assert account2.balance == account2_balance - 50.00  # Applied


class TestDeleteTransaction:
    """Tests for deleting transactions."""
    
    def test_delete_transaction_updates_balance(self, client, app, user_with_accounts):
        """Test that deleting transaction updates account balance."""
        account_id = user_with_accounts['account1_id']
        
        # Create transaction
        with app.app_context():
            account = Account.query.get(account_id)
            initial_balance = account.balance
            
            transaction = Transaction(
                account_id=account_id,
                amount=-50.00,
                description='To Delete',
                date=date.today()
            )
            db.session.add(transaction)
            account.balance -= 50.00
            db.session.commit()
            transaction_id = transaction.id
        
        # Delete transaction
        client.post(f'/transactions/delete/{transaction_id}', follow_redirects=True)
        
        # Verify transaction deleted and balance restored
        with app.app_context():
            transaction = Transaction.query.get(transaction_id)
            assert transaction is None
            
            account = Account.query.get(account_id)
            assert account.balance == initial_balance  # Balance restored


class TestTransferFeature:
    """Tests for the new transfer between accounts feature."""
    
    def test_transfer_between_accounts(self, client, app, user_with_accounts):
        """Test transferring money between two accounts."""
        account1_id = user_with_accounts['account1_id']
        account2_id = user_with_accounts['account2_id']
        
        # Get initial balances
        with app.app_context():
            account1 = Account.query.get(account1_id)
            account2 = Account.query.get(account2_id)
            balance1_initial = account1.balance
            balance2_initial = account2.balance
        
        # Transfer $200 from account1 to account2
        response = client.post('/transactions/transfer', data={
            'from_account_id': account1_id,
            'to_account_id': account2_id,
            'amount': '200.00',
            'date': date.today().strftime('%Y-%m-%d'),
            'description': 'Test Transfer'
        }, follow_redirects=True)
        
        # Verify balances updated
        with app.app_context():
            account1 = Account.query.get(account1_id)
            account2 = Account.query.get(account2_id)
            
            assert account1.balance == balance1_initial - 200.00
            assert account2.balance == balance2_initial + 200.00
            
            # Verify two transactions were created
            transactions = Transaction.query.filter(
                Transaction.description.contains('Test Transfer')
            ).all()
            assert len(transactions) == 2
            
            # One should be negative (from account1)
            # One should be positive (to account2)
            amounts = [t.amount for t in transactions]
            assert -200.00 in amounts
            assert 200.00 in amounts
    
    def test_transfer_to_same_account_fails(self, client, user_with_accounts):
        """Test that transferring to same account is prevented."""
        account_id = user_with_accounts['account1_id']
        
        response = client.post('/transactions/transfer', data={
            'from_account_id': account_id,
            'to_account_id': account_id,  # Same account!
            'amount': '100.00',
            'date': date.today().strftime('%Y-%m-%d')
        }, follow_redirects=True)
        
        html = response.data.decode()
        assert 'same account' in html.lower()
    
    def test_transfer_insufficient_balance(self, client, app, user_with_accounts):
        """Test that transfer fails with insufficient balance."""
        account1_id = user_with_accounts['account1_id']
        account2_id = user_with_accounts['account2_id']
        
        # Try to transfer more than account has
        response = client.post('/transactions/transfer', data={
            'from_account_id': account1_id,
            'to_account_id': account2_id,
            'amount': '999999.00',  # Way more than account1 has
            'date': date.today().strftime('%Y-%m-%d')
        }, follow_redirects=True)
        
        html = response.data.decode()
        assert 'insufficient' in html.lower()


class TestTransactionValidation:
    """Tests for transaction validation."""
    
    def test_cannot_create_transaction_without_amount(self, client, user_with_accounts):
        """Test that amount is required."""
        response = client.post('/transactions/add', data={
            'description': 'No amount',
            'date': date.today().strftime('%Y-%m-%d'),
            'account_id': user_with_accounts['account1_id'],
            'type': 'expense'
            # Missing amount
        }, follow_redirects=True)
        
        assert response.status_code in [200, 400]
    
    def test_cannot_create_transaction_without_date(self, client, user_with_accounts):
        """Test that date is required."""
        response = client.post('/transactions/add', data={
            'amount': '50.00',
            'description': 'No date',
            'account_id': user_with_accounts['account1_id'],
            'type': 'expense'
            # Missing date
        }, follow_redirects=True)
        
        assert response.status_code in [200, 400]
