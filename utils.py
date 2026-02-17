"""
Utility functions for the app.
"""

# Password requirements
PASSWORD_MIN_LENGTH = 8


def validate_password(password):
    """
    Validate password meets security requirements.
    Returns (is_valid, error_message).
    """
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, f'Password must be at least {PASSWORD_MIN_LENGTH} characters.'
    if not any(c.isdigit() for c in password):
        return False, 'Password must contain at least one number.'
    if not any(c.isalpha() for c in password):
        return False, 'Password must contain at least one letter.'
    return True, None


def get_currency_symbol(currency_code):
    """
    Convert currency code to symbol.
    
    Args:
        currency_code: 3-letter currency code (USD, THB, etc.)
    
    Returns:
        Currency symbol as string
    """
    currency_symbols = {
        'USD': '$',
        'THB': '฿',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CAD': 'C$',
    }
    return currency_symbols.get(currency_code, currency_code)
