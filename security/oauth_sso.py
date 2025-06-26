"""
NEXUS OAuth SSO Security Module
Multi-provider authentication and session management
"""
import os
import jwt
import logging
from datetime import datetime, timedelta
from flask import session, request
from werkzeug.security import generate_password_hash, check_password_hash

logger = logging.getLogger(__name__)

class OAuthSSO:
    def __init__(self):
        self.providers = {
            'replit': {'active': True, 'client_id': os.environ.get('REPL_ID')},
            'google': {'active': bool(os.environ.get('GOOGLE_CLIENT_ID')), 'client_id': os.environ.get('GOOGLE_CLIENT_ID')},
            'microsoft': {'active': bool(os.environ.get('MICROSOFT_CLIENT_ID')), 'client_id': os.environ.get('MICROSOFT_CLIENT_ID')}
        }
        self.session_timeout = 3600  # 1 hour
        
    def validate_token(self, token, provider='replit'):
        """Validate authentication token"""
        try:
            if provider == 'replit':
                decoded = jwt.decode(token, options={"verify_signature": False})
                return {'valid': True, 'user_id': decoded.get('sub')}
            return {'valid': False, 'error': 'Unsupported provider'}
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            return {'valid': False, 'error': str(e)}
    
    def create_secure_session(self, user_data, provider='replit'):
        """Create secure user session"""
        session_data = {
            'user_id': user_data.get('sub'),
            'email': user_data.get('email'),
            'provider': provider,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat()
        }
        
        session['nexus_auth'] = session_data
        session.permanent = True
        
        logger.info(f"Secure session created for user: {user_data.get('email', 'unknown')}")
        return session_data
    
    def validate_session(self):
        """Validate current session"""
        nexus_auth = session.get('nexus_auth')
        if not nexus_auth:
            return {'valid': False, 'error': 'No session found'}
        
        expires_at = datetime.fromisoformat(nexus_auth.get('expires_at'))
        if datetime.now() > expires_at:
            self.destroy_session()
            return {'valid': False, 'error': 'Session expired'}
        
        return {'valid': True, 'user_data': nexus_auth}
    
    def destroy_session(self):
        """Destroy user session"""
        if 'nexus_auth' in session:
            del session['nexus_auth']
        session.clear()
        logger.info("Session destroyed")
    
    def get_provider_status(self):
        """Get status of all OAuth providers"""
        return self.providers

oauth_sso = OAuthSSO()