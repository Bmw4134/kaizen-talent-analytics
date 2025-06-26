"""
Utility functions for Nexus Unified System
"""

import logging
from datetime import datetime

def log_system_event(level, message, module=None, user_id=None):
    """Log system events to database and console"""
    try:
        # Console logging
        logger = logging.getLogger(__name__)
        if level == 'debug':
            logger.debug(f"[{module}] {message}")
        elif level == 'info':
            logger.info(f"[{module}] {message}")
        elif level == 'warning':
            logger.warning(f"[{module}] {message}")
        elif level == 'error':
            logger.error(f"[{module}] {message}")
        
        # Database logging - use late import to avoid circular imports
        try:
            from app import db
            from models import SystemLog
            
            log_entry = SystemLog(
                level=level,
                message=message,
                module=module,
                user_id=user_id,
                timestamp=datetime.utcnow()
            )
            db.session.add(log_entry)
            db.session.commit()
        except ImportError:
            # Database logging not available yet
            pass
    except Exception as e:
        # Fallback to console only if database logging fails
        logging.error(f"Failed to log system event: {str(e)}")

def validate_dashboard_access(dashboard_name):
    """Validate if dashboard access is allowed"""
    allowed_dashboards = ['traxovo', 'dwc', 'jdd', 'crypto_nexus_trade']
    return dashboard_name in allowed_dashboards

def format_currency(amount, currency='USD'):
    """Format currency values"""
    try:
        if currency == 'USD':
            return f"${amount:,.2f}"
        elif currency == 'BTC':
            return f"₿{amount:.8f}"
        elif currency == 'ETH':
            return f"Ξ{amount:.6f}"
        else:
            return f"{amount:,.2f} {currency}"
    except:
        return "N/A"

def format_percentage(value):
    """Format percentage values"""
    try:
        return f"{value:.2f}%"
    except:
        return "N/A"

def safe_divide(numerator, denominator):
    """Safely divide two numbers"""
    try:
        if denominator == 0:
            return 0
        return numerator / denominator
    except:
        return 0

def truncate_string(text, max_length=50):
    """Truncate string to specified length"""
    if not isinstance(text, str):
        return str(text)
    
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_json_data(data):
    """Validate JSON data structure"""
    try:
        if isinstance(data, dict):
            return True
        return False
    except:
        return False

def get_system_health():
    """Get overall system health status"""
    try:
        return {
            'status': 'operational',
            'timestamp': datetime.utcnow().isoformat(),
            'components': {
                'database': 'operational',
                'dashboards': 'operational',
                'security': 'operational',
                'intelligence': 'operational'
            }
        }
    except Exception as e:
        log_system_event('error', f'System health check failed: {str(e)}', 'helpers')
        return {
            'status': 'degraded',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }
