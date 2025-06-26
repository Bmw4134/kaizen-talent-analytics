"""
Dashboard Security Lock System
Enforces secure login, role-based access, and API binding
"""

import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session, current_app
import logging

logger = logging.getLogger(__name__)

class DashboardSecurityLock:
    def __init__(self):
        self.secure_login = True
        self.access_roles = ["Watson", "Brett", "SystemAdmin"]
        self.enforce_trifecta = True
        self.bind_live_api = True
        self.asset_api = "/api/asset-positions"
        self.revenue_api = "/api/revenue_module"
        self.enforce_zero_suppression = True
        self.snapshot_lock = True
        self.reject_fallbacks = True
        
    def generate_secure_token(self, username, role):
        """Generate secure JWT token for authenticated users"""
        payload = {
            'username': username,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=8),
            'scope': 'dashboard_access',
            'trifecta_enforced': self.enforce_trifecta,
            'api_binding': self.bind_live_api
        }
        
        secret_key = os.environ.get('JWT_SECRET_KEY', 'nexus-secure-key-2024')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    def verify_secure_token(self, token):
        """Verify JWT token and extract user information"""
        try:
            secret_key = os.environ.get('JWT_SECRET_KEY', 'nexus-secure-key-2024')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # Verify role access
            if payload.get('role') not in self.access_roles:
                logger.warning(f"Access denied for role: {payload.get('role')}")
                return None
                
            # Verify trifecta enforcement
            if self.enforce_trifecta and not payload.get('trifecta_enforced'):
                logger.warning("Trifecta enforcement required but not present in token")
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token provided")
            return None
    
    def authenticate_user(self, username, password):
        """Authenticate user against secure credentials"""
        # Secure authentication for authorized roles
        secure_credentials = {
            'Watson': os.environ.get('WATSON_PASSWORD', 'watson'),
            'Brett': os.environ.get('BRETT_PASSWORD', 'brett_secure_2024'),
            'SystemAdmin': os.environ.get('ADMIN_PASSWORD', 'admin_nexus_2024')
        }
        
        if username in secure_credentials:
            if secure_credentials[username] == password:
                logger.info(f"Successful authentication for user: {username}")
                return True
        
        logger.warning(f"Failed authentication attempt for user: {username}")
        return False
    
    def enforce_api_binding(self, endpoint):
        """Enforce live API binding and reject fallbacks"""
        if self.reject_fallbacks:
            # Verify endpoint is using live data sources
            live_endpoints = [
                '/api/crypto/live-prices',
                '/api/asset-positions',
                '/api/revenue_module',
                '/api/traxovo/optimize',
                '/api/dwc/optimize',
                '/api/jdd/optimize',
                '/api/quantum/optimize',
                '/api/master-control/optimize'
            ]
            
            if endpoint not in live_endpoints:
                logger.warning(f"Endpoint {endpoint} not in approved live API list")
                return False
        
        return True
    
    def create_secure_session(self, username, role):
        """Create secure session with snapshot lock"""
        session_data = {
            'username': username,
            'role': role,
            'login_time': datetime.utcnow().isoformat(),
            'session_id': os.urandom(32).hex(),
            'trifecta_enforced': self.enforce_trifecta,
            'api_binding_active': self.bind_live_api,
            'snapshot_locked': self.snapshot_lock
        }
        
        if self.snapshot_lock:
            session_data['snapshot_hash'] = self._generate_snapshot_hash()
        
        return session_data
    
    def _generate_snapshot_hash(self):
        """Generate snapshot hash for session integrity"""
        import hashlib
        timestamp = datetime.utcnow().isoformat()
        random_data = os.urandom(16).hex()
        return hashlib.sha256(f"{timestamp}:{random_data}".encode()).hexdigest()
    
    def validate_session_integrity(self, session_data):
        """Validate session integrity and snapshot lock"""
        if not session_data:
            return False
            
        # Check snapshot lock
        if self.snapshot_lock and 'snapshot_hash' not in session_data:
            logger.warning("Session missing required snapshot hash")
            return False
        
        # Verify trifecta enforcement
        if self.enforce_trifecta and not session_data.get('trifecta_enforced'):
            logger.warning("Session missing trifecta enforcement")
            return False
        
        # Check API binding
        if self.bind_live_api and not session_data.get('api_binding_active'):
            logger.warning("Session missing API binding enforcement")
            return False
        
        return True

# Global security instance
dashboard_security = DashboardSecurityLock()

def require_secure_access(f):
    """Decorator to enforce secure dashboard access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_data = dashboard_security.verify_secure_token(token)
            if user_data:
                request.user = user_data
                return f(*args, **kwargs)
        
        # Check session authentication
        if 'secure_session' in session:
            session_data = session['secure_session']
            if dashboard_security.validate_session_integrity(session_data):
                return f(*args, **kwargs)
        
        # Reject unauthorized access
        logger.warning(f"Unauthorized access attempt to {request.endpoint}")
        return jsonify({
            'error': 'Secure authentication required',
            'message': 'Access restricted to authorized personnel only',
            'required_roles': dashboard_security.access_roles
        }), 401
    
    return decorated_function

def enforce_live_api_only(f):
    """Decorator to enforce live API binding and reject fallbacks"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if dashboard_security.reject_fallbacks:
            endpoint = request.endpoint
            if not dashboard_security.enforce_api_binding(f"/{endpoint}"):
                logger.warning(f"Fallback API access rejected for {endpoint}")
                return jsonify({
                    'error': 'Live API binding required',
                    'message': 'Fallback data sources are disabled in secure mode'
                }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def authenticate_dashboard_user(username, password):
    """Authenticate user and create secure session"""
    if dashboard_security.authenticate_user(username, password):
        # Determine user role
        role = username if username in dashboard_security.access_roles else "Guest"
        
        # Create secure session
        session_data = dashboard_security.create_secure_session(username, role)
        session['secure_session'] = session_data
        
        # Generate access token
        token = dashboard_security.generate_secure_token(username, role)
        
        logger.info(f"Secure dashboard access granted to {username} with role {role}")
        return {
            'success': True,
            'token': token,
            'user': username,
            'role': role,
            'session_data': session_data
        }
    
    return {
        'success': False,
        'error': 'Invalid credentials or insufficient privileges'
    }