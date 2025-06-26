"""
PTNI Bypass Enhancer V2 - Advanced Website Loading for Picture-in-Picture
Enhanced connection strategies with comprehensive URL fixing and proxy capabilities
"""

import requests
import re
from urllib.parse import urlparse, urljoin
from utils.helpers import log_system_event

class PTNIBypassEnhancerV2:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def normalize_url(self, url):
        """Normalize and fix common URL issues"""
        original_url = url
        
        # Remove extra whitespace
        url = url.strip()
        
        # Fix missing protocol
        if not url.startswith(('http://', 'https://')):
            if 'localhost' in url or '127.0.0.1' in url or url.startswith('192.168.'):
                url = f'http://{url}'
            else:
                url = f'https://{url}'
        
        # Fix malformed protocols (common copy-paste issues)
        url = re.sub(r'https?:/([^/])', r'https://\1', url)
        
        # Fix double slashes in path
        url = re.sub(r'([^:])//+', r'\1/', url)
        
        # Ensure proper Replit domain format
        if 'replit.com' in url:
            # Convert @username/repl-name format to proper URL
            replit_match = re.search(r'replit\.com/@([^/]+)/([^/?]+)', url)
            if replit_match:
                username, repl_name = replit_match.groups()
                url = f'https://{repl_name}--{username}.repl.co'
        
        if url != original_url:
            log_system_event('info', f'PTNI V2: URL normalized {original_url} → {url}', 'ptni')
        
        return url
    
    def get_enhanced_headers(self, url):
        """Get enhanced headers based on target domain"""
        headers = self.session.headers.copy()
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if 'repl.co' in domain:
            headers.update({
                'Referer': 'https://replit.com/',
                'Origin': 'https://replit.com',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Dest': 'document'
            })
        elif 'github.io' in domain:
            headers.update({
                'Referer': 'https://github.com/',
                'Origin': 'https://github.com'
            })
        elif 'localhost' in domain or '127.0.0.1' in domain:
            headers.update({
                'Host': parsed.netloc,
                'Connection': 'keep-alive'
            })
        
        return headers
    
    def enhanced_fetch(self, url, timeout=30):
        """Enhanced website fetching with multiple fallback strategies"""
        url = self.normalize_url(url)
        headers = self.get_enhanced_headers(url)
        
        strategies = [
            ('direct', {'verify': True, 'timeout': timeout}),
            ('no_verify', {'verify': False, 'timeout': timeout}),
            ('mobile_agent', {'verify': False, 'timeout': timeout, 'mobile': True}),
            ('simple_agent', {'verify': False, 'timeout': timeout, 'simple': True})
        ]
        
        for strategy_name, options in strategies:
            try:
                # Modify headers based on strategy
                request_headers = headers.copy()
                
                if options.get('mobile'):
                    request_headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
                elif options.get('simple'):
                    request_headers['User-Agent'] = 'Mozilla/5.0 (compatible; PTNI/2.0)'
                
                log_system_event('info', f'PTNI V2: Trying {strategy_name} strategy for {url}', 'ptni')
                
                response = self.session.get(
                    url,
                    headers=request_headers,
                    timeout=options['timeout'],
                    verify=options['verify'],
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    log_system_event('info', f'PTNI V2: Success with {strategy_name} strategy for {url}', 'ptni')
                    return {
                        'success': True,
                        'content': response.text,
                        'strategy': strategy_name,
                        'status_code': response.status_code,
                        'final_url': response.url
                    }
                else:
                    log_system_event('warning', f'PTNI V2: {strategy_name} returned {response.status_code} for {url}', 'ptni')
                    
            except Exception as e:
                log_system_event('warning', f'PTNI V2: {strategy_name} failed for {url}: {str(e)}', 'ptni')
                continue
        
        return {
            'success': False,
            'error': 'All connection strategies failed',
            'url': url
        }
    
    def create_iframe_safe_content(self, content, base_url):
        """Create iframe-safe content with enhanced compatibility"""
        try:
            # Remove X-Frame-Options blockers
            content = re.sub(r'<meta[^>]*http-equiv=["\']?X-Frame-Options["\']?[^>]*>', '', content, flags=re.IGNORECASE)
            
            # Fix relative URLs
            parsed_base = urlparse(base_url)
            base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
            
            # Fix relative links
            content = re.sub(r'href=["\'](?!http)([^"\']+)["\']', f'href="{base_domain}\\1"', content)
            content = re.sub(r'src=["\'](?!http)([^"\']+)["\']', f'src="{base_domain}\\1"', content)
            
            # Add iframe compatibility meta tags
            iframe_meta = '''
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { margin: 0; padding: 10px; overflow-x: auto; }
                * { max-width: 100%; }
            </style>
            '''
            
            # Insert meta tags after <head>
            content = re.sub(r'(<head[^>]*>)', f'\\1{iframe_meta}', content, flags=re.IGNORECASE)
            
            return content
            
        except Exception as e:
            log_system_event('error', f'PTNI V2: Content processing failed: {str(e)}', 'ptni')
            return content
    
    def test_connection_methods(self, url):
        """Test different connection methods and return diagnostics"""
        url = self.normalize_url(url)
        test_results = {}
        
        # Test basic connectivity
        try:
            response = requests.head(url, timeout=10, verify=False)
            test_results['head_request'] = {
                'status': response.status_code,
                'headers': dict(response.headers)
            }
        except Exception as e:
            test_results['head_request'] = {'error': str(e)}
        
        # Test full fetch
        fetch_result = self.enhanced_fetch(url)
        test_results['enhanced_fetch'] = fetch_result
        
        return test_results

def create_pip_interface_with_enhanced_bypass():
    """Create Picture-in-Picture interface with enhanced PTNI bypass"""
    return '''
    <div class="pip-enhanced-interface">
        <div class="pip-controls">
            <input type="text" id="pip-url-input" placeholder="Enter website URL..." class="form-control">
            <button onclick="loadEnhancedPiP()" class="btn btn-primary">Load with Enhanced Bypass</button>
            <button onclick="testConnection()" class="btn btn-secondary">Test Connection</button>
        </div>
        <div id="pip-status" class="alert alert-info" style="display: none;"></div>
        <div class="pip-container">
            <iframe id="pip-frame" src="about:blank" frameborder="0" 
                    style="width: 100%; height: 600px; border: 1px solid #ccc; border-radius: 8px;">
            </iframe>
        </div>
    </div>
    
    <script>
    function showStatus(message, type = 'info') {
        const status = document.getElementById('pip-status');
        status.className = `alert alert-${type}`;
        status.textContent = message;
        status.style.display = 'block';
    }
    
    function loadEnhancedPiP() {
        const url = document.getElementById('pip-url-input').value.trim();
        if (!url) {
            showStatus('Please enter a URL', 'warning');
            return;
        }
        
        showStatus('Loading with enhanced PTNI bypass...', 'info');
        
        fetch('/api/ptni-enhanced-fetch', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const iframe = document.getElementById('pip-frame');
                const blob = new Blob([data.content], {type: 'text/html'});
                const objectURL = URL.createObjectURL(blob);
                iframe.src = objectURL;
                showStatus(`Loaded successfully using ${data.strategy} strategy`, 'success');
            } else {
                showStatus(`Failed to load: ${data.error}`, 'danger');
            }
        })
        .catch(error => {
            showStatus(`Error: ${error.message}`, 'danger');
        });
    }
    
    function testConnection() {
        const url = document.getElementById('pip-url-input').value.trim();
        if (!url) {
            showStatus('Please enter a URL to test', 'warning');
            return;
        }
        
        showStatus('Testing connection methods...', 'info');
        
        fetch('/api/ptni-test-connection', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url})
        })
        .then(response => response.json())
        .then(data => {
            console.log('Connection test results:', data);
            showStatus(`Connection test completed. Check console for details.`, 'info');
        })
        .catch(error => {
            showStatus(`Test failed: ${error.message}`, 'danger');
        });
    }
    </script>
    '''

def get_enhanced_pip_template():
    """Get enhanced Picture-in-Picture template"""
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NEXUS Enhanced PiP Interface</title>
        <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
        <style>
            .pip-enhanced-interface {{
                padding: 20px;
                background: var(--bs-dark);
                border-radius: 12px;
                margin: 20px 0;
            }}
            .pip-controls {{
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                flex-wrap: wrap;
            }}
            .pip-controls input {{
                flex: 1;
                min-width: 300px;
            }}
            .pip-container {{
                position: relative;
                background: #000;
                border-radius: 8px;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <h2 class="text-primary mb-3">
                <i class="fas fa-external-link-alt"></i>
                NEXUS Enhanced Picture-in-Picture Interface
            </h2>
            {create_pip_interface_with_enhanced_bypass()}
        </div>
    </body>
    </html>
    '''