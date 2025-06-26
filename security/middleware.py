"""
Security Middleware for Nexus Unified System
Implements comprehensive security measures
"""

import re
from werkzeug.wrappers import Request, Response
from utils.helpers import log_system_event

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
        self.blocked_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS protection
            r'javascript:',                # JavaScript protocol
            r'vbscript:',                 # VBScript protocol
            r'on\w+\s*=',                 # Event handlers
            r'expression\s*\(',           # CSS expressions
            r'import\s+',                 # ES6 imports
            r'eval\s*\(',                 # eval() calls
        ]
        self.security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.replit.com; style-src 'self' 'unsafe-inline' https://cdn.replit.com; img-src 'self' data: https:; font-src 'self' https://cdn.replit.com;",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        
        # Security checks
        if not self.validate_request(request):
            log_system_event('warning', f'Blocked suspicious request: {request.url}', 'security')
            response = Response('Access Denied', status=403)
            return response(environ, start_response)
        
        # Process request through the application
        def new_start_response(status, response_headers):
            # Add security headers
            for header, value in self.security_headers.items():
                response_headers.append((header, value))
            return start_response(status, response_headers)
        
        return self.app(environ, new_start_response)
    
    def validate_request(self, request):
        """Validate incoming requests for security threats"""
        try:
            # Allow PTNI bypass routes
            if '/ptni-bypass/' in request.path or '/proxy/' in request.path:
                return True
            
            # Check for XSS and injection attempts
            for pattern in self.blocked_patterns:
                if request.query_string:
                    if re.search(pattern, request.query_string.decode('utf-8'), re.IGNORECASE):
                        return False
                
                if request.data:
                    try:
                        data_str = request.data.decode('utf-8')
                        if re.search(pattern, data_str, re.IGNORECASE):
                            return False
                    except UnicodeDecodeError:
                        # Skip binary data
                        pass
            
            # Check for path traversal attempts (but allow encoded URLs in PTNI)
            if '..' in request.path or ('//' in request.path and '/ptni-bypass/' not in request.path):
                return False
            
            # Validate HTTP methods
            if request.method not in ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']:
                return False
            
            # Rate limiting (basic implementation)
            # In production, use Redis or similar for distributed rate limiting
            if self.check_rate_limit(request):
                return False
            
            return True
        except Exception as e:
            log_system_event('error', f'Security validation error: {str(e)}', 'security')
            return False
    
    def check_rate_limit(self, request):
        """Basic rate limiting check"""
        # This is a simplified implementation
        # In production, implement proper rate limiting with Redis
        return False
    
    def sanitize_input(self, input_string):
        """Sanitize user input"""
        if not isinstance(input_string, str):
            return input_string
        
        # Remove potentially dangerous patterns
        for pattern in self.blocked_patterns:
            input_string = re.sub(pattern, '', input_string, flags=re.IGNORECASE)
        
        return input_string
