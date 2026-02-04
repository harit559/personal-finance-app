"""
Utility functions for the app.
"""

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
