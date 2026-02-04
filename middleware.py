"""
Security middleware for Flask app.
Adds security headers to all responses.
"""


def add_security_headers(app):
    """
    Add security headers to protect against common vulnerabilities.
    
    Headers added:
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-Frame-Options: Prevents clickjacking attacks
    - X-XSS-Protection: Enables XSS filter in browsers
    - Strict-Transport-Security: Enforces HTTPS
    - Content-Security-Policy: Prevents XSS and injection attacks
    """
    
    @app.after_request
    def security_headers(response):
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking - don't allow site to be framed
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Enable XSS protection in browsers
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Force HTTPS for 1 year (only in production)
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy
        # Allow trusted CDNs for Chart.js, Tailwind CSS, and Google Fonts
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com; "
            "font-src 'self' data: https://fonts.gstatic.com; "
            "connect-src 'self' https://cdn.jsdelivr.net;"
        )
        
        return response
    
    return app
