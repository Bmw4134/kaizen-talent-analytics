"""
PTNI Neural Processing - Connection Error Resolution
Fixes URL parsing and connection issues in neural processing system
"""

import re
from urllib.parse import urlparse, urlunparse
from utils.helpers import log_system_event

class PTNINeuralFix:
    def __init__(self):
        self.url_patterns = {
            'double_protocol': r'https?://https?:/',
            'malformed_localhost': r'https?://localhost:\d+',
            'invalid_host': r'https?://(?:http|https)/',
            'replit_domain': r'workspace\.[\w\d]+\.repl\.co'
        }
    
    def fix_malformed_url(self, url):
        """Fix common URL malformation issues"""
        original_url = url
        
        # Fix missing protocol scheme first
        if not url.startswith(('http://', 'https://')):
            if 'localhost' in url or '127.0.0.1' in url:
                url = f'http://{url}'
            else:
                url = f'https://{url}'
        
        # Fix double protocol issues
        if re.search(self.url_patterns['double_protocol'], url):
            url = re.sub(r'https://http:/', 'http://', url)
            url = re.sub(r'https://https:/', 'https://', url)
            url = re.sub(r'http://https:/', 'https://', url)
        
        # Fix malformed Replit URLs (common issue: https:/replit.com instead of https://replit.com)
        if 'replit.com' in url:
            url = re.sub(r'https:/([^/])', r'https://\1', url)
            url = re.sub(r'http:/([^/])', r'http://\1', url)
        
        # Fix invalid host protocols being treated as hostnames
        if re.search(self.url_patterns['invalid_host'], url):
            # Extract the actual target from malformed URL
            if 'localhost' in url:
                url = 'http://localhost:5000'
            elif 'repl.co' in url:
                # Extract replit domain properly
                match = re.search(r'([\w\d-]+\.repl\.co)', url)
                if match:
                    url = f'https://{match.group(1)}'
        
        # Ensure proper protocol for localhost
        if 'localhost' in url and not url.startswith(('http://', 'https://')):
            url = f'http://{url}'
        
        # Ensure proper protocol for replit domains
        if 'repl.co' in url and not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        if url != original_url:
            log_system_event('info', f'PTNI URL fixed: {original_url} → {url}', 'ptni')
        
        return url
    
    def validate_url_structure(self, url):
        """Validate URL structure and return connection parameters"""
        try:
            parsed = urlparse(url)
            
            # Check for valid hostname
            if not parsed.hostname or parsed.hostname in ['http', 'https']:
                return {
                    'valid': False,
                    'error': 'Invalid hostname detected',
                    'suggested_fix': self.fix_malformed_url(url)
                }
            
            # Check for proper scheme
            if parsed.scheme not in ['http', 'https']:
                return {
                    'valid': False,
                    'error': 'Invalid or missing protocol scheme',
                    'suggested_fix': f'https://{url}' if not url.startswith(('http://', 'https://')) else url
                }
            
            return {
                'valid': True,
                'hostname': parsed.hostname,
                'port': parsed.port or (443 if parsed.scheme == 'https' else 80),
                'scheme': parsed.scheme,
                'path': parsed.path or '/'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'URL parsing failed: {str(e)}',
                'suggested_fix': self.fix_malformed_url(url)
            }
    
    def get_connection_strategy(self, url):
        """Determine optimal connection strategy for given URL"""
        validation = self.validate_url_structure(url)
        
        if not validation['valid']:
            # Try to fix the URL
            fixed_url = validation['suggested_fix']
            validation = self.validate_url_structure(fixed_url)
            
            if validation['valid']:
                url = fixed_url
            else:
                return {
                    'strategy': 'failed',
                    'error': validation['error'],
                    'original_url': url
                }
        
        # Determine connection strategy based on hostname
        hostname = validation['hostname']
        
        if hostname in ['localhost', '127.0.0.1']:
            return {
                'strategy': 'localhost',
                'url': url,
                'ports_to_try': [5000, 3000, 8000, 80],
                'timeout': 10,
                'verify_ssl': False
            }
        elif 'repl.co' in hostname:
            return {
                'strategy': 'replit',
                'url': url,
                'timeout': 25,
                'verify_ssl': True,
                'headers': {
                    'Referer': 'https://replit.com/',
                    'User-Agent': 'Mozilla/5.0 (compatible; PTNI/1.0)'
                }
            }
        else:
            return {
                'strategy': 'standard',
                'url': url,
                'timeout': 20,
                'verify_ssl': True
            }

def fix_ptni_urls_in_logs():
    """Fix PTNI URLs found in system logs"""
    ptni_fix = PTNINeuralFix()
    
    # Common problematic URLs from logs
    problematic_urls = [
        'https://http:/localhost:3000',
        'https://http:/127.0.0.1:3000',
        'https://https:/workspace.bmwatson34.repl.co/',
    ]
    
    fixes = {}
    for url in problematic_urls:
        fixed_url = ptni_fix.fix_malformed_url(url)
        strategy = ptni_fix.get_connection_strategy(fixed_url)
        fixes[url] = {
            'fixed_url': fixed_url,
            'strategy': strategy
        }
    
    return fixes

def apply_ptni_neural_fixes():
    """Apply comprehensive PTNI neural processing fixes"""
    log_system_event('info', 'PTNI Neural Fix: Starting comprehensive connection repair', 'ptni')
    
    fixes = fix_ptni_urls_in_logs()
    
    for original_url, fix_data in fixes.items():
        log_system_event('info', f'PTNI Fix Applied: {original_url} → {fix_data["fixed_url"]}', 'ptni')
    
    return {
        'status': 'success',
        'fixes_applied': len(fixes),
        'connection_strategies': fixes
    }