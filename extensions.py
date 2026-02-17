"""
Shared extensions - avoid circular imports.
Import these in app.py and in routes that need them.
"""
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask import request

csrf = CSRFProtect()


def _get_remote_address():
    """Get client IP, works behind proxy (Render, etc.)."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or '127.0.0.1'


limiter = Limiter(key_func=_get_remote_address)
