# Test Suite Documentation

## Overview

This test suite provides comprehensive coverage for the Harit Finance application backend. All tests are written using `pytest`, which is already included in your `requirements.txt`.

## Test Files

### 1. `test_auth.py` - Authentication Tests
Tests user registration, login, logout, and password security.

**What it tests:**
- ✅ User can register with valid data
- ✅ Cannot register with duplicate email
- ✅ User can login with correct credentials
- ✅ Cannot login with wrong password
- ✅ User can logout successfully
- ✅ Passwords are hashed (not stored in plain text)

### 2. `test_accounts.py` - Account CRUD Tests
Tests creating, reading, updating, and deleting accounts.

**What it tests:**
- ✅ Create account with different types and currencies
- ✅ View list of accounts
- ✅ Update account name and type
- ✅ Delete account (with and without transactions)
- ✅ Account balances are correct

### 3. `test_transactions.py` - Transaction Tests
Tests transaction operations including the **new transfer feature**.

**What it tests:**
- ✅ Create expense and income transactions
- ✅ Update transaction amount and description
- ✅ **Switch transaction to different account**
- ✅ Delete transaction (updates balance correctly)
- ✅ **Transfer between accounts** (new feature!)
- ✅ Cannot transfer to same account
- ✅ Cannot transfer with insufficient balance
- ✅ Transaction validation (amount, date required)

### 4. `test_categories.py` - Category Tests
Tests category management and deletion handling.

**What it tests:**
- ✅ Create expense and income categories
- ✅ View categories list
- ✅ Update category name, icon, color
- ✅ Delete empty category
- ✅ Delete category with transactions (move to another or uncategorize)

### 5. `test_models.py` - Database Model Tests
Tests the database models and their relationships.

**What it tests:**
- ✅ User model creation and password hashing
- ✅ Email uniqueness
- ✅ Account-User relationship
- ✅ Transaction-Account relationship
- ✅ Category-User relationship
- ✅ Cascade deletes (deleting user deletes their data)

### 6. `test_user_separation.py` - Security Tests
Tests that users can only see their own data.

**What it tests:**
- ✅ Alice cannot see Bob's accounts
- ✅ Alice cannot edit or delete Bob's data
- ✅ Dashboard shows only user's own data
- ✅ Unauthenticated users are redirected to login

## Running the Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_auth.py -v
pytest tests/test_transactions.py -v
pytest tests/test_accounts.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_transactions.py::TestTransferFeature -v
```

### Run Specific Test Function
```bash
pytest tests/test_transactions.py::TestTransferFeature::test_transfer_between_accounts -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Tests in Quiet Mode (less output)
```bash
pytest tests/ -q
```

### Run Tests and Stop at First Failure
```bash
pytest tests/ -x
```

## Understanding Test Output

### Success Output
```
tests/test_auth.py::TestUserRegistration::test_register_new_user_success PASSED [100%]
```
✅ Test passed! The feature works correctly.

### Failure Output
```
tests/test_auth.py::TestUserLogin::test_login_wrong_password FAILED
```
❌ Test failed! Check the error message to see what went wrong.

## Test Structure

Each test follows this pattern:

```python
def test_something(self, client, app):
    # 1. ARRANGE: Set up test data
    # Create users, accounts, etc.
    
    # 2. ACT: Perform the action
    # Make a request, call a function
    
    # 3. ASSERT: Verify the result
    # Check that it worked as expected
```

## Common Fixtures

### `app`
- Creates a fresh Flask app for testing
- Uses in-memory SQLite database (fast, isolated)

### `client`
- Test client for making HTTP requests
- Simulates a web browser

### `logged_in_user`
- Creates and logs in a test user
- Saves you from repeating login code

## What Makes a Good Test?

1. **Isolated**: Each test runs independently
2. **Fast**: Uses in-memory database
3. **Clear**: Test name describes what it tests
4. **Reliable**: Same input = same output
5. **Comprehensive**: Tests success AND failure cases

## Coverage Statistics

After running tests with coverage:
- Open `htmlcov/index.html` in browser
- See which lines of code are tested
- Aim for >80% coverage

## Common Issues

### Issue: "No module named 'pytest'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Database locked"
**Solution:** Tests use in-memory DB, shouldn't happen. If it does:
```bash
# Delete any .db files and try again
rm *.db
pytest tests/ -v
```

### Issue: Test fails locally but should pass
**Solution:** Check test isolation
- Make sure each test cleans up after itself
- Don't rely on test execution order
- Use fixtures for setup/teardown

## Best Practices

1. **Write tests first** (Test-Driven Development)
   - Write the test
   - Run it (should fail)
   - Write code to make it pass
   
2. **Test edge cases**
   - What if amount is 0?
   - What if date is in the future?
   - What if user doesn't exist?

3. **Keep tests simple**
   - One test = one thing
   - Clear test names
   - Minimal assertions

4. **Run tests often**
   - Before committing code
   - After making changes
   - As part of deployment

## Next Steps

1. Run all tests and make sure they pass
2. Look at the test code to understand how it works
3. Try modifying a test to see what happens
4. Write your own test for a new feature

## Need Help?

- Read pytest docs: https://docs.pytest.org/
- Look at existing tests for examples
- Tests are documentation - they show how code should work!
