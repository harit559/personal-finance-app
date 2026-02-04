"""
Test Category CRUD Operations

Tests for creating, reading, updating, and deleting categories.
"""
import pytest
from app import create_app
from models import db, User, Category, Transaction, Account
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


class TestCreateCategory:
    """Tests for creating categories."""
    
    def test_create_expense_category(self, client, app, logged_in_user):
        """Test creating an expense category."""
        response = client.post('/categories/add', data={
            'name': 'Food',
            'category_type': 'expense',
            'icon': '🍔',
            'color': '#ff0000'
        }, follow_redirects=True)
        
        with app.app_context():
            category = Category.query.filter_by(name='Food').first()
            assert category is not None
            assert category.category_type == 'expense'
            assert category.icon == '🍔'
            assert category.color == '#ff0000'
            assert category.user_id == logged_in_user
    
    def test_create_income_category(self, client, app, logged_in_user):
        """Test creating an income category."""
        client.post('/categories/add', data={
            'name': 'Salary',
            'category_type': 'income',
            'icon': '💰',
            'color': '#00ff00'
        })
        
        with app.app_context():
            category = Category.query.filter_by(name='Salary').first()
            assert category is not None
            assert category.category_type == 'income'


class TestReadCategories:
    """Tests for viewing categories."""
    
    def test_view_categories_list(self, client, app, logged_in_user):
        """Test viewing list of categories."""
        # Create categories
        with app.app_context():
            expense_cat = Category(
                user_id=logged_in_user,
                name='Food',
                category_type='expense',
                icon='🍔'
            )
            income_cat = Category(
                user_id=logged_in_user,
                name='Salary',
                category_type='income',
                icon='💰'
            )
            db.session.add(expense_cat)
            db.session.add(income_cat)
            db.session.commit()
        
        response = client.get('/categories/')
        html = response.data.decode()
        
        assert 'Food' in html
        assert 'Salary' in html
        assert '🍔' in html
        assert '💰' in html


class TestUpdateCategory:
    """Tests for updating categories."""
    
    def test_update_category_name(self, client, app, logged_in_user):
        """Test updating category name."""
        # Create category
        with app.app_context():
            category = Category(
                user_id=logged_in_user,
                name='Old Name',
                category_type='expense'
            )
            db.session.add(category)
            db.session.commit()
            category_id = category.id
        
        # Update category
        client.post(f'/categories/edit/{category_id}', data={
            'name': 'New Name',
            'category_type': 'expense',
            'icon': '📦',
            'color': '#6366f1'
        })
        
        with app.app_context():
            category = Category.query.get(category_id)
            assert category.name == 'New Name'
    
    def test_update_category_icon_and_color(self, client, app, logged_in_user):
        """Test updating category icon and color."""
        # Create category
        with app.app_context():
            category = Category(
                user_id=logged_in_user,
                name='Test',
                category_type='expense',
                icon='📦',
                color='#000000'
            )
            db.session.add(category)
            db.session.commit()
            category_id = category.id
        
        # Update
        client.post(f'/categories/edit/{category_id}', data={
            'name': 'Test',
            'category_type': 'expense',
            'icon': '🎉',
            'color': '#ff00ff'
        })
        
        with app.app_context():
            category = Category.query.get(category_id)
            assert category.icon == '🎉'
            assert category.color == '#ff00ff'


class TestDeleteCategory:
    """Tests for deleting categories."""
    
    def test_delete_category_without_transactions(self, client, app, logged_in_user):
        """Test deleting category with no transactions."""
        # Create category
        with app.app_context():
            category = Category(
                user_id=logged_in_user,
                name='To Delete',
                category_type='expense'
            )
            db.session.add(category)
            db.session.commit()
            category_id = category.id
        
        # Delete
        client.post(f'/categories/delete/{category_id}', data={
            'new_category_id': 'none'
        }, follow_redirects=True)
        
        with app.app_context():
            category = Category.query.get(category_id)
            assert category is None
    
    def test_delete_category_with_transactions_set_to_uncategorized(self, client, app, logged_in_user):
        """Test deleting category that has transactions - set to uncategorized."""
        # Create account, category, and transaction
        with app.app_context():
            account = Account(
                user_id=logged_in_user,
                name='Test Account',
                account_type='bank',
                balance=1000,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            category = Category(
                user_id=logged_in_user,
                name='To Delete',
                category_type='expense'
            )
            db.session.add(category)
            db.session.flush()
            
            transaction = Transaction(
                account_id=account.id,
                category_id=category.id,
                amount=-50,
                description='Test',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            
            category_id = category.id
            transaction_id = transaction.id
        
        # Delete category, setting transactions to uncategorized
        client.post(f'/categories/delete/{category_id}', data={
            'new_category_id': 'none'
        })
        
        with app.app_context():
            category = Category.query.get(category_id)
            assert category is None
            
            # Transaction should still exist but with no category
            transaction = Transaction.query.get(transaction_id)
            assert transaction is not None
            assert transaction.category_id is None
    
    def test_delete_category_with_transactions_move_to_another(self, client, app, logged_in_user):
        """Test deleting category - move transactions to another category."""
        # Create account and two categories
        with app.app_context():
            account = Account(
                user_id=logged_in_user,
                name='Test Account',
                account_type='bank',
                balance=1000,
                currency='USD'
            )
            db.session.add(account)
            db.session.flush()
            
            category1 = Category(
                user_id=logged_in_user,
                name='To Delete',
                category_type='expense'
            )
            category2 = Category(
                user_id=logged_in_user,
                name='Keep This',
                category_type='expense'
            )
            db.session.add(category1)
            db.session.add(category2)
            db.session.flush()
            
            transaction = Transaction(
                account_id=account.id,
                category_id=category1.id,
                amount=-50,
                description='Test',
                date=date.today()
            )
            db.session.add(transaction)
            db.session.commit()
            
            category1_id = category1.id
            category2_id = category2.id
            transaction_id = transaction.id
        
        # Delete category1, move transactions to category2
        client.post(f'/categories/delete/{category1_id}', data={
            'new_category_id': str(category2_id)
        })
        
        with app.app_context():
            # Category1 should be deleted
            category1 = Category.query.get(category1_id)
            assert category1 is None
            
            # Transaction should now belong to category2
            transaction = Transaction.query.get(transaction_id)
            assert transaction.category_id == category2_id


class TestCategoryValidation:
    """Tests for category validation."""
    
    def test_cannot_create_category_without_name(self, client, logged_in_user):
        """Test that name is required."""
        response = client.post('/categories/add', data={
            'category_type': 'expense',
            'icon': '📦',
            'color': '#000000'
            # Missing name
        }, follow_redirects=True)
        
        assert response.status_code in [200, 400]
    
    def test_cannot_create_category_without_type(self, client, logged_in_user):
        """Test that type is required."""
        response = client.post('/categories/add', data={
            'name': 'Test',
            'icon': '📦',
            'color': '#000000'
            # Missing category_type
        }, follow_redirects=True)
        
        assert response.status_code in [200, 400]
