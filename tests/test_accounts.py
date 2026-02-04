"""
Test Account CRUD Operations

Tests for creating, reading, updating, and deleting accounts.
"""
import pytest
from app import create_app
from models import db, User, Account, Transaction
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
def logged_in_user(client, app):
    """Create and login a user."""
    with app.app_context():
        user = User(name='Test User', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    return user_id


class TestCreateAccount:
    """Tests for creating accounts."""
    
    def test_create_account_success(self, client, app, logged_in_user):
        """Test creating a new account."""
        response = client.post('/accounts/add', data={
            'name': 'My Checking',
            'account_type': 'bank',
            'balance': '1000.00',
            'currency': 'USD',
            'starting_date': date.today().strftime('%Y-%m-%d')
        }, follow_redirects=True)
        
        # Verify account was created
        with app.app_context():
            account = Account.query.filter_by(name='My Checking').first()
            assert account is not None
            assert account.account_type == 'bank'
            assert account.balance == 1000.00
            assert account.currency == 'USD'
            assert account.user_id == logged_in_user
    
    def test_create_account_different_currencies(self, client, app, logged_in_user):
        """Test creating accounts with different currencies."""
        currencies = ['USD', 'THB', 'EUR', 'GBP']
        
        for currency in currencies:
            client.post('/accounts/add', data={
                'name': f'{currency} Account',
                'account_type': 'bank',
                'balance': '500.00',
                'currency': currency,
                'starting_date': date.today().strftime('%Y-%m-%d')
            })
        
        with app.app_context():
            for currency in currencies:
                account = Account.query.filter_by(currency=currency).first()
                assert account is not None
    
    def test_create_account_zero_balance(self, client, app, logged_in_user):
        """Test creating account with zero initial balance."""
        response = client.post('/accounts/add', data={
            'name': 'Empty Account',
            'account_type': 'savings',
            'balance': '0',
            'currency': 'USD',
            'starting_date': date.today().strftime('%Y-%m-%d')
        }, follow_redirects=True)
        
        with app.app_context():
            account = Account.query.filter_by(name='Empty Account').first()
            assert account is not None
            assert account.balance == 0.0


class TestReadAccounts:
    """Tests for viewing accounts."""
    
    def test_view_accounts_list(self, client, app, logged_in_user):
        """Test viewing list of accounts."""
        # Create some accounts
        with app.app_context():
            account1 = Account(
                user_id=logged_in_user,
                name='Checking',
                account_type='bank',
                balance=1000.00,
                currency='USD'
            )
            account2 = Account(
                user_id=logged_in_user,
                name='Savings',
                account_type='savings',
                balance=5000.00,
                currency='USD'
            )
            db.session.add(account1)
            db.session.add(account2)
            db.session.commit()
        
        response = client.get('/accounts/')
        html = response.data.decode()
        
        assert 'Checking' in html
        assert 'Savings' in html
        assert '1000.00' in html or '$1,000.00' in html
    
    def test_view_empty_accounts_list(self, client, logged_in_user):
        """Test viewing accounts when user has none."""
        response = client.get('/accounts/')
        html = response.data.decode()
        
        assert 'No accounts' in html or 'Add your first account' in html


class TestUpdateAccount:
    """Tests for updating accounts."""
    
    def test_update_account_name(self, client, app, logged_in_user):
        """Test updating account name."""
        # Create account
        with app.app_context():
            account = Account(
                user_id=logged_in_user,
                name='Old Name',
                account_type='bank',
                balance=1000.00,
                currency='USD'
            )
            db.session.add(account)
            db.session.commit()
            account_id = account.id
        
        # Update account
        client.post(f'/accounts/edit/{account_id}', data={
            'name': 'New Name',
            'account_type': 'bank',
            'currency': 'USD'
        })
        
        # Verify update
        with app.app_context():
            account = Account.query.get(account_id)
            assert account.name == 'New Name'
    
    def test_update_account_type(self, client, app, logged_in_user):
        """Test updating account type."""
        # Create account
        with app.app_context():
            account = Account(
                user_id=logged_in_user,
                name='Test Account',
                account_type='bank',
                balance=1000.00,
                currency='USD'
            )
            db.session.add(account)
            db.session.commit()
            account_id = account.id
        
        # Update type
        client.post(f'/accounts/edit/{account_id}', data={
            'name': 'Test Account',
            'account_type': 'savings',
            'currency': 'USD'
        })
        
        with app.app_context():
            account = Account.query.get(account_id)
            assert account.account_type == 'savings'


class TestDeleteAccount:
    """Tests for deleting accounts."""
    
    def test_delete_account_without_transactions(self, client, app, logged_in_user):
        """Test deleting an account with no transactions."""
        # Create account
        with app.app_context():
            account = Account(
                user_id=logged_in_user,
                name='To Delete',
                account_type='bank',
                balance=0,
                currency='USD'
            )
            db.session.add(account)
            db.session.commit()
            account_id = account.id
        
        # Delete account
        client.post(f'/accounts/delete/{account_id}', follow_redirects=True)
        
        # Verify deletion
        with app.app_context():
            account = Account.query.get(account_id)
            assert account is None
    
    def test_delete_account_with_transactions(self, client, app, logged_in_user):
        """Test that deleting account also deletes its transactions."""
        # Create account with transaction
        with app.app_context():
            account = Account(
                user_id=logged_in_user,
                name='To Delete',
                account_type='bank',
                balance=100,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            transaction = Transaction(
                account_id=account.id,
                amount=-50,
                description='Test',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            account_id = account.id
            transaction_id = transaction.id
        
        # Delete account
        client.post(f'/accounts/delete/{account_id}', follow_redirects=True)
        
        # Verify both account and transaction are deleted
        with app.app_context():
            account = Account.query.get(account_id)
            transaction = Transaction.query.get(transaction_id)
            assert account is None
            assert transaction is None  # Cascade delete
