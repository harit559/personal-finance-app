"""
Test Authentication (Login, Registration, Logout)

These tests verify that user authentication works correctly.
"""
import pytest
from app import create_app
from models import db, User


@pytest.fixture
def app():
    """Create a test app with a temporary database."""
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


class TestUserRegistration:
    """Tests for user registration."""
    
    def test_register_new_user_success(self, client, app):
        """Test successful user registration."""
        response = client.post('/auth/register', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Check user was created in database
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user is not None
            assert user.name == 'Test User'
            assert user.check_password('password123')
    
    def test_register_duplicate_email(self, client, app):
        """Test that registering with duplicate email fails."""
        # Create first user
        with app.app_context():
            user = User(name='First User', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Try to register with same email
        response = client.post('/auth/register', data={
            'name': 'Second User',
            'email': 'test@example.com',
            'password': 'password456'
        }, follow_redirects=True)
        
        html = response.data.decode()
        assert 'already exists' in html.lower() or 'already registered' in html.lower()
    
    def test_register_missing_fields(self, client):
        """Test that registration fails with missing fields."""
        response = client.post('/auth/register', data={
            'name': 'Test User',
            # Missing email and password
        }, follow_redirects=True)
        
        assert response.status_code in [200, 400]  # Should show form again


class TestUserLogin:
    """Tests for user login."""
    
    def test_login_success(self, client, app):
        """Test successful login."""
        # Create a user
        with app.app_context():
            user = User(name='Test User', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Login
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        html = response.data.decode()
        # Should redirect to dashboard
        assert 'Welcome' in html or 'Dashboard' in html
    
    def test_login_wrong_password(self, client, app):
        """Test login with wrong password."""
        # Create a user
        with app.app_context():
            user = User(name='Test User', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Try to login with wrong password
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        html = response.data.decode()
        assert 'invalid' in html.lower() or 'incorrect' in html.lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        response = client.post('/auth/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        html = response.data.decode()
        assert 'invalid' in html.lower() or 'not found' in html.lower()


class TestUserLogout:
    """Tests for user logout."""
    
    def test_logout_success(self, client, app):
        """Test successful logout."""
        # Create and login user
        with app.app_context():
            user = User(name='Test User', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Logout
        response = client.get('/auth/logout', follow_redirects=True)
        html = response.data.decode()
        
        # Should redirect to login page
        assert 'Login' in html or 'Log in' in html


class TestPasswordHashing:
    """Tests for password security."""
    
    def test_password_is_hashed(self, app):
        """Test that passwords are hashed, not stored in plain text."""
        with app.app_context():
            user = User(name='Test User', email='test@example.com')
            user.set_password('password123')
            
            # Password hash should NOT equal the plain password
            assert user.password_hash != 'password123'
            # But check_password should work
            assert user.check_password('password123')
            assert not user.check_password('wrongpassword')
