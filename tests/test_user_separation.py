"""
Tests for User Data Separation

These tests verify that users can only see and modify their own data.
This is critical for security!

Run tests with: pytest tests/ -v
"""
import pytest
from app import create_app
from models import db, User, Account, Transaction, Category
from datetime import date


@pytest.fixture
def app():
    """Create a test app with a temporary database."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def two_users_with_data(app):
    """
    Create two users, each with their own account and transactions.
    This is the main setup for testing data separation.
    """
    with app.app_context():
        # Create User 1 (Alice)
        alice = User(name='Alice', email='alice@test.com')
        alice.set_password('password123')
        db.session.add(alice)
        db.session.flush()
        
        alice_account = Account(
            user_id=alice.id,
            name='Alice Checking',
            account_type='bank',
            balance=1000.00
        )
        db.session.add(alice_account)
        db.session.flush()
        
        alice_category = Category(
            user_id=alice.id,
            name='Alice Food',
            category_type='expense'
        )
        db.session.add(alice_category)
        db.session.flush()
        
        alice_transaction = Transaction(
            account_id=alice_account.id,
            category_id=alice_category.id,
            amount=-50.00,
            description='Alice lunch',
            date=date.today()
        )
        db.session.add(alice_transaction)
        
        # Create User 2 (Bob)
        bob = User(name='Bob', email='bob@test.com')
        bob.set_password('password123')
        db.session.add(bob)
        db.session.flush()
        
        bob_account = Account(
            user_id=bob.id,
            name='Bob Savings',
            account_type='savings',
            balance=5000.00
        )
        db.session.add(bob_account)
        db.session.flush()
        
        bob_category = Category(
            user_id=bob.id,
            name='Bob Entertainment',
            category_type='expense'
        )
        db.session.add(bob_category)
        db.session.flush()
        
        bob_transaction = Transaction(
            account_id=bob_account.id,
            category_id=bob_category.id,
            amount=-100.00,
            description='Bob movie',
            date=date.today()
        )
        db.session.add(bob_transaction)
        
        db.session.commit()
        
        return {
            'alice': {'id': alice.id, 'email': 'alice@test.com', 'account_id': alice_account.id, 'transaction_id': alice_transaction.id},
            'bob': {'id': bob.id, 'email': 'bob@test.com', 'account_id': bob_account.id, 'transaction_id': bob_transaction.id}
        }


def login(client, email, password):
    """Helper function to log in a user."""
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


def logout(client):
    """Helper function to log out."""
    return client.get('/auth/logout', follow_redirects=True)


# ============================================
# TEST: Users can only see their own accounts
# ============================================

class TestAccountSeparation:
    """Tests for account data separation."""
    
    def test_alice_only_sees_her_accounts(self, client, two_users_with_data):
        """Alice should only see her own accounts, not Bob's."""
        login(client, 'alice@test.com', 'password123')
        
        response = client.get('/accounts/')
        html = response.data.decode()
        
        assert 'Alice Checking' in html  # Alice sees her account
        assert 'Bob Savings' not in html  # Alice does NOT see Bob's account
    
    def test_bob_only_sees_his_accounts(self, client, two_users_with_data):
        """Bob should only see his own accounts, not Alice's."""
        login(client, 'bob@test.com', 'password123')
        
        response = client.get('/accounts/')
        html = response.data.decode()
        
        assert 'Bob Savings' in html      # Bob sees his account
        assert 'Alice Checking' not in html  # Bob does NOT see Alice's account
    
    def test_alice_cannot_edit_bobs_account(self, client, two_users_with_data):
        """Alice should not be able to edit Bob's account."""
        login(client, 'alice@test.com', 'password123')
        
        # Try to access Bob's account edit page
        bob_account_id = two_users_with_data['bob']['account_id']
        response = client.get(f'/accounts/edit/{bob_account_id}', follow_redirects=True)
        html = response.data.decode()
        
        assert 'Access denied' in html
    
    def test_alice_cannot_delete_bobs_account(self, client, two_users_with_data):
        """Alice should not be able to delete Bob's account."""
        login(client, 'alice@test.com', 'password123')
        
        bob_account_id = two_users_with_data['bob']['account_id']
        response = client.post(f'/accounts/delete/{bob_account_id}', follow_redirects=True)
        html = response.data.decode()
        
        assert 'Access denied' in html


# ================================================
# TEST: Users can only see their own transactions
# ================================================

class TestTransactionSeparation:
    """Tests for transaction data separation."""
    
    def test_alice_only_sees_her_transactions(self, client, two_users_with_data):
        """Alice should only see her own transactions."""
        login(client, 'alice@test.com', 'password123')
        
        response = client.get('/transactions/')
        html = response.data.decode()
        
        assert 'Alice lunch' in html     # Alice sees her transaction
        assert 'Bob movie' not in html   # Alice does NOT see Bob's transaction
    
    def test_bob_only_sees_his_transactions(self, client, two_users_with_data):
        """Bob should only see his own transactions."""
        login(client, 'bob@test.com', 'password123')
        
        response = client.get('/transactions/')
        html = response.data.decode()
        
        assert 'Bob movie' in html       # Bob sees his transaction
        assert 'Alice lunch' not in html # Bob does NOT see Alice's transaction
    
    def test_alice_cannot_edit_bobs_transaction(self, client, two_users_with_data):
        """Alice should not be able to edit Bob's transaction."""
        login(client, 'alice@test.com', 'password123')
        
        bob_transaction_id = two_users_with_data['bob']['transaction_id']
        response = client.get(f'/transactions/edit/{bob_transaction_id}', follow_redirects=True)
        html = response.data.decode()
        
        assert 'Access denied' in html
    
    def test_alice_cannot_delete_bobs_transaction(self, client, two_users_with_data):
        """Alice should not be able to delete Bob's transaction."""
        login(client, 'alice@test.com', 'password123')
        
        bob_transaction_id = two_users_with_data['bob']['transaction_id']
        response = client.post(f'/transactions/delete/{bob_transaction_id}', follow_redirects=True)
        html = response.data.decode()
        
        assert 'Access denied' in html


# ============================================
# TEST: Dashboard shows only user's own data
# ============================================

class TestDashboardSeparation:
    """Tests for dashboard data separation."""
    
    def test_alice_dashboard_shows_her_balance(self, client, two_users_with_data):
        """Alice's dashboard should show her balance, not Bob's."""
        login(client, 'alice@test.com', 'password123')
        
        response = client.get('/')
        html = response.data.decode()
        
        # Alice has $1000, Bob has $5000
        # Alice should see values related to her $1000 balance
        assert 'Alice Checking' in html
        assert 'Bob Savings' not in html


# ============================================
# TEST: New data is associated with correct user
# ============================================

class TestNewDataAssociation:
    """Tests that new data is correctly associated with the logged-in user."""
    
    def test_new_account_belongs_to_logged_in_user(self, client, app, two_users_with_data):
        """When Alice creates an account, it should belong to Alice."""
        login(client, 'alice@test.com', 'password123')
        
        # Alice creates a new account
        client.post('/accounts/add', data={
            'name': 'Alice New Account',
            'account_type': 'savings',
            'balance': '500',
            'currency': 'USD'
        })
        
        # Verify the account belongs to Alice
        with app.app_context():
            new_account = Account.query.filter_by(name='Alice New Account').first()
            alice = User.query.filter_by(email='alice@test.com').first()
            
            assert new_account is not None
            assert new_account.user_id == alice.id


# ============================================
# Summary test - run all critical checks
# ============================================

class TestSecuritySummary:
    """Summary tests for overall security."""
    
    def test_unauthenticated_user_cannot_access_data(self, client, two_users_with_data):
        """Users who are not logged in should be redirected to login."""
        # Don't log in - try to access protected pages
        
        response = client.get('/accounts/', follow_redirects=True)
        assert b'Please log in' in response.data or b'Login' in response.data
        
        response = client.get('/transactions/', follow_redirects=True)
        assert b'Please log in' in response.data or b'Login' in response.data
        
        response = client.get('/', follow_redirects=True)
        assert b'Please log in' in response.data or b'Login' in response.data
