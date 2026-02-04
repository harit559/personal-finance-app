# 🧪 Testing Guide for Harit Finance

## What Are Unit Tests?

**Unit tests** are automated tests that verify individual parts (units) of your code work correctly. Think of them as quality checks:

- ✅ Do all features work as expected?
- ✅ Does the transfer feature actually transfer money?
- ✅ Can users only see their own data?
- ✅ Are passwords stored securely?

**Why test?**
1. **Catch bugs early** - Find problems before users do
2. **Confidence** - Make changes without breaking things
3. **Documentation** - Tests show how code should work
4. **Professionalism** - Industry standard practice

## 📁 What I Created For You

I've created **6 comprehensive test files** covering all your backend features:

### Test Files Overview

| File | Tests | Purpose |
|------|-------|---------|
| `test_auth.py` | 9 tests | Login, registration, logout, password security |
| `test_accounts.py` | 11 tests | Creating, viewing, editing, deleting accounts |
| `test_transactions.py` | 13 tests | Transactions + **your new transfer feature!** |
| `test_categories.py` | 11 tests | Category management and deletion handling |
| `test_models.py` | 10 tests | Database models and relationships |
| `test_user_separation.py` | 10 tests | Security - users can only see their own data |

**Total: 64 comprehensive tests** covering your entire backend!

## 🎯 Key Features Tested

### ✅ Your New Features
1. **Transfer Between Accounts** ✨
   - Transfer money from one account to another
   - Prevents transfers to the same account
   - Checks for sufficient balance
   - Creates proper transaction records

2. **Switch Account in Edit** ✨
   - Move transactions between accounts
   - Balance updates correctly in both accounts

### ✅ Core Features
3. Authentication (register, login, logout)
4. Account CRUD (Create, Read, Update, Delete)
5. Transaction CRUD
6. Category CRUD
7. Data security (user separation)
8. Password hashing
9. Database relationships

## 🚀 How to Run Tests

### Step 1: Make sure pytest is installed
```bash
# Check if pytest is installed
pytest --version

# If not installed, install it
pip install pytest
```

### Step 2: Run ALL tests
```bash
# Go to your project directory
cd /Users/harit/Projects/personal_finance_app

# Run all tests
pytest tests/ -v
```

### Step 3: Understand the output

**Success looks like:**
```
tests/test_transactions.py::TestTransferFeature::test_transfer_between_accounts PASSED [✓]
tests/test_transactions.py::TestTransferFeature::test_transfer_to_same_account_fails PASSED [✓]
tests/test_transactions.py::TestTransferFeature::test_transfer_insufficient_balance PASSED [✓]

=============================== 64 passed in 2.34s ===============================
```

**Failure looks like:**
```
tests/test_auth.py::TestUserLogin::test_login_success FAILED [✗]

FAILED tests/test_auth.py::TestUserLogin::test_login_success - AssertionError: ...
```

## 📖 Understanding the Tests

Let me explain one test in detail so you understand how they work:

### Example: Test Transfer Between Accounts

```python
def test_transfer_between_accounts(self, client, app, user_with_accounts):
    """Test transferring money between two accounts."""
    
    # STEP 1: ARRANGE - Set up initial data
    account1_id = user_with_accounts['account1_id']
    account2_id = user_with_accounts['account2_id']
    
    # Get initial balances
    with app.app_context():
        account1 = Account.query.get(account1_id)
        account2 = Account.query.get(account2_id)
        balance1_initial = account1.balance  # e.g., $1000
        balance2_initial = account2.balance  # e.g., $5000
    
    # STEP 2: ACT - Perform the action being tested
    # Transfer $200 from account1 to account2
    response = client.post('/transactions/transfer', data={
        'from_account_id': account1_id,
        'to_account_id': account2_id,
        'amount': '200.00',
        'date': date.today().strftime('%Y-%m-%d'),
        'description': 'Test Transfer'
    }, follow_redirects=True)
    
    # STEP 3: ASSERT - Verify it worked correctly
    with app.app_context():
        account1 = Account.query.get(account1_id)
        account2 = Account.query.get(account2_id)
        
        # Account1 should have $200 less
        assert account1.balance == balance1_initial - 200.00  # $800
        
        # Account2 should have $200 more
        assert account2.balance == balance2_initial + 200.00  # $5200
        
        # Two transactions should be created
        transactions = Transaction.query.filter(
            Transaction.description.contains('Test Transfer')
        ).all()
        assert len(transactions) == 2
```

### What This Test Does:

1. **ARRANGE**: Sets up two accounts with known balances
2. **ACT**: Makes a transfer request (like clicking the Transfer button)
3. **ASSERT**: Checks that:
   - Source account lost money
   - Destination account gained money
   - Two transaction records were created

This is called the **AAA Pattern** (Arrange, Act, Assert) - industry standard!

## 🔍 Different Ways to Run Tests

### Run all tests (recommended first time)
```bash
pytest tests/ -v
```

### Run just one file
```bash
pytest tests/test_transactions.py -v
```

### Run just transfer tests
```bash
pytest tests/test_transactions.py::TestTransferFeature -v
```

### Run one specific test
```bash
pytest tests/test_transactions.py::TestTransferFeature::test_transfer_between_accounts -v
```

### Run tests matching a keyword
```bash
pytest tests/ -k transfer -v
```

### Run tests and stop at first failure
```bash
pytest tests/ -x
```

### Run with less output (quiet mode)
```bash
pytest tests/ -q
```

### Run and see print statements
```bash
pytest tests/ -v -s
```

## 🎓 Test Concepts Explained

### 1. Fixtures
```python
@pytest.fixture
def logged_in_user(client, app):
    # This creates a test user automatically
    # Used by many tests so you don't repeat code
```

**What it does:** Sets up data before each test
**Like:** Setting up a test environment

### 2. Test Classes
```python
class TestTransferFeature:
    """Group related tests together"""
    def test_transfer_works(self):
        # Test code
    
    def test_transfer_fails_same_account(self):
        # Test code
```

**What it does:** Organizes tests by feature
**Like:** Folders for organizing files

### 3. Assertions
```python
assert account.balance == 1000.00  # Check if true
assert user is not None             # Check exists
assert 'error' in response         # Check contains
```

**What it does:** Verifies expected result
**Like:** Double-checking your math

### 4. Test Database
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

**What it does:** Uses temporary database in RAM
**Why:** Fast, doesn't affect your real database, cleaned up automatically

## 📊 What Each Test File Does

### `test_auth.py` - Authentication Tests
```python
✅ test_register_new_user_success         # Can create account
✅ test_register_duplicate_email          # Can't use same email twice
✅ test_login_success                     # Can login with correct password
✅ test_login_wrong_password              # Can't login with wrong password
✅ test_logout_success                    # Can logout
✅ test_password_is_hashed                # Passwords are encrypted
```

### `test_accounts.py` - Account Tests
```python
✅ test_create_account_success            # Can create account
✅ test_create_account_different_currencies  # Supports USD, THB, EUR, etc.
✅ test_view_accounts_list                # Can see all accounts
✅ test_update_account_name               # Can rename account
✅ test_delete_account                    # Can delete account
```

### `test_transactions.py` - Transaction Tests
```python
✅ test_create_expense_transaction        # Can record expenses
✅ test_create_income_transaction         # Can record income
✅ test_update_transaction_amount         # Can edit amount
✅ test_update_transaction_switch_account # NEW: Can move to different account
✅ test_transfer_between_accounts         # NEW: Transfer feature works!
✅ test_transfer_to_same_account_fails    # NEW: Prevents same-account transfer
✅ test_transfer_insufficient_balance     # NEW: Checks balance before transfer
```

### `test_categories.py` - Category Tests
```python
✅ test_create_expense_category           # Can create expense categories
✅ test_create_income_category            # Can create income categories
✅ test_update_category_name              # Can rename category
✅ test_delete_category_with_transactions # Handles deletion properly
```

### `test_models.py` - Database Model Tests
```python
✅ test_user_password_hashing             # Passwords stored securely
✅ test_account_user_relationship         # Accounts belong to users
✅ test_transaction_account_relationship  # Transactions belong to accounts
✅ test_delete_user_cascades              # Deleting user deletes their data
```

### `test_user_separation.py` - Security Tests
```python
✅ test_alice_only_sees_her_accounts      # Data privacy works
✅ test_alice_cannot_edit_bobs_account    # Users can't hack each other
✅ test_unauthenticated_redirects         # Must login to see data
```

## 💡 Why These Tests Matter

### Real-World Example:

**Without tests:**
```
You: "I added the transfer feature!"
Boss: "Does it work?"
You: "I tested it manually once..."
Boss: "But what if someone transfers $0? Or negative amounts? Or to the same account?"
You: "Uh... I didn't check those..."
```

**With tests:**
```
You: "I added the transfer feature with 13 automated tests!"
Boss: "What do they test?"
You: "Normal transfers, edge cases, error handling, balance updates, everything!"
Boss: "Perfect! Deploy it!"
```

### What Tests Catch:

1. **Transfer to same account** - Would have broken without test
2. **Negative amounts** - Could have allowed stealing money
3. **Balance not updating** - Would corrupt data
4. **Security holes** - Users seeing others' data

## 🔧 Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'pytest'"
```bash
# Solution: Install pytest
pip install pytest
```

### Issue: "Database is locked"
```bash
# Solution: Tests use in-memory DB, shouldn't happen
# But if it does, delete old databases
rm finance.db
pytest tests/ -v
```

### Issue: Tests fail because app.py can't import
```bash
# Solution: Make sure you're in the right directory
cd /Users/harit/Projects/personal_finance_app
pytest tests/ -v
```

## 🎯 Best Practices for Testing

### 1. Test Before Deploy
```bash
# Before pushing to production
pytest tests/ -v

# If all pass, you're good to go!
```

### 2. Test After Changes
```bash
# Made changes to transfer feature?
pytest tests/test_transactions.py::TestTransferFeature -v
```

### 3. Add Tests for New Features
When you add a new feature, add tests:
```python
def test_my_new_feature(self, client, app):
    # Arrange
    # ... set up data
    
    # Act
    # ... use the feature
    
    # Assert
    # ... verify it worked
```

## 📚 Learning Resources

### Want to Learn More?

1. **Official Pytest Docs**: https://docs.pytest.org/
2. **Flask Testing**: https://flask.palletsprojects.com/en/latest/testing/
3. **Test-Driven Development**: Write tests first, then code

### Next Steps:

1. ✅ Run all tests: `pytest tests/ -v`
2. ✅ Look at one test file and understand it
3. ✅ Try modifying a test to see what happens
4. ✅ Write your own test for a new feature
5. ✅ Run tests before every deployment

## 🎉 Summary

You now have:
- ✅ **64 comprehensive tests** for your entire backend
- ✅ Tests for **all your new features** (transfer, account switching)
- ✅ **Security tests** ensuring data privacy
- ✅ **Documentation** (this guide!) to understand everything
- ✅ **Industry-standard practices** (AAA pattern, fixtures, assertions)

Your app is now **professionally tested** and ready for production! 🚀

## Quick Reference Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific file
pytest tests/test_transactions.py -v

# Run specific test
pytest tests/test_transactions.py::TestTransferFeature::test_transfer_between_accounts -v

# Run and stop at first failure
pytest tests/ -x

# Run matching keyword
pytest tests/ -k transfer -v

# Quiet mode
pytest tests/ -q
```

---

**Questions?** Read the tests - they're documentation! Each test shows exactly how a feature should work.
