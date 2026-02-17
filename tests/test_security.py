"""
Security Tests - CSRF, ownership, open redirect, password validation, logout.
"""
from datetime import date
import pytest
from app import create_app
from models import db, User, Account


@pytest.fixture
def app():
    """Create test app."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_and_account(app):
    """Create a user with an account."""
    with app.app_context():
        user = User(name='Alice', email='alice@test.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.flush()
        account = Account(user_id=user.id, name='Cash', account_type='cash',
                         balance=100, starting_balance=100,
                         starting_date=date(2024, 1, 1), currency='USD')
        db.session.add(account)
        db.session.commit()
        return user, account


class TestPasswordValidation:
    """Test password requirements on registration and reset."""

    def test_register_rejects_short_password(self, client):
        """Password under 8 chars should fail."""
        response = client.post('/auth/register', data={
            'name': 'Test', 'email': 'test@test.com', 'password': 'short1'
        }, follow_redirects=True)
        html = response.data.decode()
        assert 'at least 8' in html.lower() or '8 characters' in html.lower()

    def test_register_rejects_password_without_number(self, client):
        """Password without number should fail."""
        response = client.post('/auth/register', data={
            'name': 'Test', 'email': 'test@test.com', 'password': 'passwordonly'
        }, follow_redirects=True)
        html = response.data.decode()
        assert 'number' in html.lower()

    def test_register_rejects_password_without_letter(self, client):
        """Password without letter should fail."""
        response = client.post('/auth/register', data={
            'name': 'Test', 'email': 'test@test.com', 'password': '12345678'
        }, follow_redirects=True)
        html = response.data.decode()
        assert 'letter' in html.lower()

    def test_register_accepts_valid_password(self, client, app):
        """Valid password (8+ chars, letter, number) should succeed."""
        response = client.post('/auth/register', data={
            'name': 'Test', 'email': 'valid@test.com', 'password': 'validpass1'
        }, follow_redirects=True)
        with app.app_context():
            assert User.query.filter_by(email='valid@test.com').first() is not None


class TestOpenRedirect:
    """Test open redirect protection on login."""

    def test_login_ignores_external_next(self, client, user_and_account):
        """?next=https://evil.com should redirect to home, not evil.com."""
        user, _ = user_and_account
        response = client.post('/auth/login', data={
            'email': 'alice@test.com', 'password': 'password123'
        }, query_string={'next': 'https://evil.com'}, follow_redirects=False)
        assert response.location
        assert 'evil.com' not in response.location
        assert '/auth/login' not in response.location or 'localhost' in response.location

    def test_login_allows_safe_next(self, client, user_and_account):
        """?next=/transactions/ should redirect to /transactions/."""
        response = client.post('/auth/login', data={
            'email': 'alice@test.com', 'password': 'password123'
        }, query_string={'next': '/transactions/'}, follow_redirects=False)
        assert '/transactions/' in (response.location or '')


class TestLogoutPostOnly:
    """Test logout requires POST."""

    def test_logout_get_returns_405(self, client, user_and_account):
        """GET /auth/logout should return 405 Method Not Allowed."""
        client.post('/auth/login', data={
            'email': 'alice@test.com', 'password': 'password123'
        }, follow_redirects=True)
        response = client.get('/auth/logout')
        assert response.status_code == 405


class TestOwnershipCheck:
    """Test transaction ownership validation."""

    def test_add_transaction_rejects_invalid_account_id(self, client, user_and_account):
        """Adding transaction with fake account_id should fail."""
        client.post('/auth/login', data={
            'email': 'alice@test.com', 'password': 'password123'
        }, follow_redirects=True)
        # CSRF disabled in testing - submit with invalid account_id
        response = client.post('/transactions/add', data={
            'account_id': '99999',
            'amount': '50',
            'date': '2024-01-15',
            'type': 'expense',
        }, follow_redirects=True)
        html = response.data.decode()
        assert 'invalid account' in html.lower()
