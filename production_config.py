"""
Production Configuration for NEXUS UF Platform
Optimized settings for production deployment with recursive evolution
"""

import os
from datetime import timedelta

class ProductionConfig:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET') or os.urandom(32)
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30
    }
    
    # Security Settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Performance Optimization
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=365)
    TEMPLATES_AUTO_RELOAD = False
    EXPLAIN_TEMPLATE_LOADING = False
    
    # API Configuration
    API_RATE_LIMIT = '1000 per hour'
    API_TIMEOUT = 30
    
    # Recursive Evolution Settings
    EVOLUTION_MODE = 'production'
    KPI_MONITORING = True
    SELF_HEALING = True
    API_FALLBACK = True
    MOBILE_OPTIMIZATION = True
    
    # Logging Configuration
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
    
    # CORS Settings
    CORS_ORIGINS = ['https://*.replit.app', 'https://*.replit.dev']
    
    # Performance Monitoring
    PERFORMANCE_TRACKING = True
    ANALYTICS_ENABLED = True
    ERROR_REPORTING = True

# Production Environment Variables
PRODUCTION_ENV = {
    'FLASK_ENV': 'production',
    'FLASK_DEBUG': 'False',
    'WERKZEUG_RUN_MAIN': 'true',
    'PYTHONPATH': '/home/runner/workspace',
    'NEXUS_MODE': 'production',
    'RECURSIVE_EVOLUTION': 'active'
}

def configure_production_app(app):
    """Configure Flask app for production deployment"""
    
    # Apply production configuration
    app.config.from_object(ProductionConfig)
    
    # Enable production optimizations
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    
    # Configure logging for production
    import logging
    from logging.handlers import RotatingFileHandler
    
    if not app.debug:
        # File logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/nexus_uf.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('NEXUS UF Production Startup')
    
    # Initialize production extensions
    from flask_compress import Compress
    from flask_talisman import Talisman
    
    # Enable compression
    compress = Compress()
    compress.init_app(app)
    
    # Security headers
    talisman = Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
            'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com",
            'font-src': "'self' https://cdn.jsdelivr.net",
            'img-src': "'self' data: https:",
            'connect-src': "'self' https://api.perplexity.ai https://api.coingecko.com"
        }
    )
    
    return app

def get_production_status():
    """Get production environment status"""
    return {
        'mode': 'production',
        'ssl_enabled': True,
        'compression': True,
        'security_headers': True,
        'database_pooling': True,
        'logging': 'file_rotation',
        'recursive_evolution': 'active',
        'api_optimization': True,
        'mobile_ready': True,
        'performance_monitoring': True
    }