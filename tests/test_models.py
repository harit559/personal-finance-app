"""
Test Database Models

Tests for the database models and their relationships.
"""
import pytest
from app import create_app
from models import db, User, Account, Transaction, Category, Budget
from datetime import date, datetime, timezone


@pytest.fixture
def app():
    """Create a test app."""
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


class TestUserModel:
    """Tests for User model."""
    
    def test_create_user(self, app):
        """Test creating a user."""
        with app.app_context():
            user = User(name='Test User', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.name == 'Test User'
            assert user.email == 'test@example.com'
            assert user.created_at is not None
    
    def test_user_password_hashing(self, app):
        """Test password hashing and verification."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('mysecret')
            
            # Password should be hashed
            assert user.password_hash != 'mysecret'
            
            # check_password should work
            assert user.check_password('mysecret') is True
            assert user.check_password('wrongpassword') is False
    
    def test_user_email_unique(self, app):
        """Test that email must be unique."""
        with app.app_context():
            user1 = User(name='User 1', email='same@example.com')
            user1.set_password('pass1')
            db.session.add(user1)
            db.session.commit()
            
            # Try to create another user with same email
            user2 = User(name='User 2', email='same@example.com')
            user2.set_password('pass2')
            db.session.add(user2)
            
            with pytest.raises(Exception):  # Should raise integrity error
                db.session.commit()


class TestAccountModel:
    """Tests for Account model."""
    
    def test_create_account(self, app):
        """Test creating an account."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            account = Account(
                user_id=user.id,
                name='My Account',
                account_type='bank',
                balance=1000.00,
                currency='USD'
            )
            db.session.add(account)
            db.session.commit()
            
            assert account.id is not None
            assert account.name == 'My Account'
            assert account.balance == 1000.00
            assert account.currency == 'USD'
    
    def test_account_user_relationship(self, app):
        """Test relationship between Account and User."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            account = Account(
                user_id=user.id,
                name='Test Account',
                account_type='bank',
                balance=0,
                currency='USD'
            )
            db.session.add(account)
            db.session.commit()
            
            # Can access user from account
            assert account.user.email == 'test@example.com'
            
            # Can access accounts from user
            assert len(user.accounts) == 1
            assert user.accounts[0].name == 'Test Account'
    
    def test_delete_user_cascades_to_accounts(self, app):
        """Test that deleting user also deletes their accounts."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            account = Account(
                user_id=user.id,
                name='Test',
                account_type='bank',
                balance=0,
                currency='USD'
            )
            db.session.add(account)
            db.session.commit()
            
            user_id = user.id
            account_id = account.id
            
            # Delete user
            db.session.delete(user)
            db.session.commit()
            
            # Account should also be deleted
            account = Account.query.get(account_id)
            assert account is None


class TestTransactionModel:
    """Tests for Transaction model."""
    
    def test_create_transaction(self, app):
        """Test creating a transaction."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            account = Account(
                user_id=user.id,
                name='Test',
                account_type='bank',
                balance=1000,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            transaction = Transaction(
                account_id=account.id,
                amount=-50.00,
                description='Test expense',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            
            assert transaction.id is not None
            assert transaction.amount == -50.00
            assert transaction.description == 'Test expense'
    
    def test_transaction_account_relationship(self, app):
        """Test relationship between Transaction and Account."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            account = Account(
                user_id=user.id,
                name='Test Account',
                account_type='bank',
                balance=0,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            transaction = Transaction(
                account_id=account.id,
                amount=-25.00,
                description='Test',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            
            # Can access account from transaction
            assert transaction.account.name == 'Test Account'
            
            # Can access transactions from account
            assert len(account.transactions) == 1
            assert account.transactions[0].description == 'Test'
    
    def test_delete_account_cascades_to_transactions(self, app):
        """Test that deleting account deletes its transactions."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            account = Account(
                user_id=user.id,
                name='Test',
                account_type='bank',
                balance=0,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            transaction = Transaction(
                account_id=account.id,
                amount=-10,
                description='Test',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            
            transaction_id = transaction.id
            
            # Delete account
            db.session.delete(account)
            db.session.commit()
            
            # Transaction should be deleted
            transaction = Transaction.query.get(transaction_id)
            assert transaction is None


class TestCategoryModel:
    """Tests for Category model."""
    
    def test_create_category(self, app):
        """Test creating a category."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            category = Category(
                user_id=user.id,
                name='Food',
                category_type='expense',
                icon='🍔',
                color='#ff0000'
            )
            db.session.add(category)
            db.session.commit()
            
            assert category.id is not None
            assert category.name == 'Food'
            assert category.category_type == 'expense'
    
    def test_category_user_relationship(self, app):
        """Test relationship between Category and User."""
        with app.app_context():
            user = User(name='Test', email='test@example.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.flush()
            
            category = Category(
                user_id=user.id,
                name='Shopping',
                category_type='expense'
            )
            db.session.add(category)
            db.session.commit()
            
            # Can access user from category
            assert category.user.email == 'test@example.com'
            
            # Can access categories from user
            assert len(user.categories) == 1
            assert user.categories[0].name == 'Shopping'


class TestRelationships:
    """Tests for model relationships."""
    
    def test_complete_data_flow(self, app):
        """Test creating a complete data flow: User -> Account -> Category -> Transaction."""
        with app.app_context():
            # Create user
            user = User(name='John', email='john@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.flush()
            
            # Create account
            account = Account(
                user_id=user.id,
                name='Checking',
                account_type='bank',
                balance=1000,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            # Create category
            category = Category(
                user_id=user.id,
                name='Food',
                category_type='expense'
            )
            db.session.add(category)
            db.session.flush()
            
            # Create transaction
            transaction = Transaction(
                account_id=account.id,
                category_id=category.id,
                amount=-30.00,
                description='Lunch',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            
            # Verify all relationships work
            assert transaction.account.name == 'Checking'
            assert transaction.category.name == 'Food'
            assert transaction.account.user.name == 'John'
            assert account.transactions[0].description == 'Lunch'
            assert category.transactions[0].description == 'Lunch'
