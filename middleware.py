"""
Security middleware for Flask app.
Adds security headers to all responses.
"""
from flask import request


def add_security_headers(app):
    """
    Add security headers to protect against common vulnerabilities.
    """
    
    @app.after_request
    def security_headers(response):
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Enable XSS protection in browsers
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Don't cache sensitive pages (financial data)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        
        # Limit referrer leakage
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Restrict browser features
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        
        # Force HTTPS (production only)
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "object-src 'none'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' data: https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self' https://cdn.jsdelivr.net;"
        )
        
        return response
    
    return app
