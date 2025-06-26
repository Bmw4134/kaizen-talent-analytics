from flask import render_template, request, jsonify, session, redirect, url_for, flash
from app import app, db
from models import User, DashboardSession, SystemLog
from dashboards import traxovo, dwc, jdd, crypto_nexus_trade
from intelligence.quantum_nexus import QuantumNexusIntelligence
from utils.helpers import validate_dashboard_access, log_system_event
import json
from datetime import datetime
import logging
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize Quantum Nexus Intelligence
qni = QuantumNexusIntelligence()

# Import and initialize NEXUS Master Control
try:
    from nexus_master_control import nexus_master
    from automation_kernel.diagnostic_healer import diagnostic_healer
    from communication.alert_router import alert_router
    from nexus_total_recall import nexus_total_recall
    # Import windowed interface module to register routes
    import nexus_windowed_interface
    NEXUS_MASTER_ACTIVE = True
    
    # Auto-initialize NEXUS Intelligence Core
    nexus_master.initialize_master_control()
    diagnostic_healer.start_monitoring()
    
    # Deploy Total Recall Protocol
    nexus_total_recall.deploy_all_modules()
    
    log_system_event('info', 'NEXUS Total Recall Protocol & Intelligence Core Override Complete', 'nexus_master')
except Exception as e:
    NEXUS_MASTER_ACTIVE = False
    log_system_event('warning', f'NEXUS Master Control initialization failed: {e}', 'nexus_master')

@app.route('/')
def index():
    """Main landing page with dashboard overview"""
    try:
        dashboards = [
            {
                'name': 'TRAXOVO',
                'id': 'traxovo',
                'description': 'Advanced tracking and optimization system',
                'status': 'active',
                'icon': 'activity'
            },
            {
                'name': 'DWC',
                'id': 'dwc',
                'description': 'Dynamic workflow controller',
                'status': 'active',
                'icon': 'layers'
            },
            {
                'name': 'JDD',
                'id': 'jdd',
                'description': 'Joint data dashboard',
                'status': 'active',
                'icon': 'database'
            },
            {
                'name': 'CryptoNexusTrade',
                'id': 'crypto_nexus_trade',
                'description': 'Cryptocurrency trading platform',
                'status': 'active',
                'icon': 'trending-up'
            }
        ]
        
        # Apply Quantum Nexus Intelligence processing
        intelligent_data = qni.process_dashboard_overview(dashboards)
        
        log_system_event('info', 'Main dashboard accessed', 'routes')
        
        return render_template('index.html', 
                             dashboards=dashboards, 
                             intelligent_data=intelligent_data)
    except Exception as e:
        log_system_event('error', f'Error accessing main dashboard: {str(e)}', 'routes')
        return render_template('error.html', error="Dashboard initialization failed")

@app.route('/dashboard/<dashboard_name>')
def dashboard(dashboard_name):
    """Route to specific dashboard"""
    try:
        if not validate_dashboard_access(dashboard_name):
            flash('Access denied to requested dashboard', 'error')
            return redirect(url_for('index'))
        
        # Get dashboard data based on name
        dashboard_data = None
        if dashboard_name == 'traxovo':
            dashboard_data = traxovo.get_dashboard_data()
        elif dashboard_name == 'dwc':
            dashboard_data = dwc.get_dashboard_data()
        elif dashboard_name == 'jdd':
            dashboard_data = jdd.get_dashboard_data()
        elif dashboard_name == 'crypto_nexus_trade':
            dashboard_data = crypto_nexus_trade.get_dashboard_data()
        else:
            flash('Dashboard not found', 'error')
            return redirect(url_for('index'))
        
        # Apply intelligence processing
        enhanced_data = qni.enhance_dashboard_data(dashboard_name, dashboard_data)
        
        # Update session tracking
        session_entry = DashboardSession(
            dashboard_name=dashboard_name,
            session_data=json.dumps(enhanced_data),
            last_accessed=datetime.utcnow()
        )
        db.session.add(session_entry)
        db.session.commit()
        
        log_system_event('info', f'Dashboard {dashboard_name} accessed', 'routes')
        
        return render_template(f'dashboards/{dashboard_name}.html', 
                             dashboard_data=enhanced_data,
                             dashboard_name=dashboard_name)
    except Exception as e:
        log_system_event('error', f'Error accessing dashboard {dashboard_name}: {str(e)}', 'routes')
        return render_template('error.html', 
                             error=f"Failed to load {dashboard_name} dashboard")

@app.route('/api/dashboard/<dashboard_name>/data')
def api_dashboard_data(dashboard_name):
    """API endpoint for dashboard data"""
    try:
        if not validate_dashboard_access(dashboard_name):
            return jsonify({'error': 'Access denied'}), 403
        
        # Get fresh data from dashboard modules
        if dashboard_name == 'traxovo':
            data = traxovo.get_api_data()
        elif dashboard_name == 'dwc':
            data = dwc.get_api_data()
        elif dashboard_name == 'jdd':
            data = jdd.get_api_data()
        elif dashboard_name == 'crypto_nexus_trade':
            data = crypto_nexus_trade.get_api_data()
        else:
            return jsonify({'error': 'Dashboard not found'}), 404
        
        # Apply intelligence enhancement
        enhanced_data = qni.enhance_api_response(dashboard_name, data)
        
        return jsonify(enhanced_data)
    except Exception as e:
        log_system_event('error', f'API error for {dashboard_name}: {str(e)}', 'routes')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/intelligence/process', methods=['POST'])
def api_intelligence_process():
    """API endpoint for quantum nexus intelligence processing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        processed_data = qni.process_user_request(data)
        return jsonify(processed_data)
    except Exception as e:
        log_system_event('error', f'Intelligence processing error: {str(e)}', 'routes')
        return jsonify({'error': 'Processing failed'}), 500

@app.route('/nexus-windowed')
def nexus_windowed():
    """NEXUS Windowed Command Center Interface"""
    try:
        log_system_event('info', 'NEXUS Command Center accessed', 'routes')
        return render_template('nexus_command_center.html')
    except Exception as e:
        log_system_event('error', f'Error accessing NEXUS Command Center: {str(e)}', 'routes')
        return render_template('error.html', error="Command center failed to load")

@app.route('/proxy/<path:url>')
def browser_proxy(url):
    """Standard NEXUS proxy with basic bypass"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            overlay = '''
            <div style="position: fixed; top: 10px; right: 10px; background: #007bff; color: white; padding: 8px 15px; border-radius: 20px; font-size: 11px; z-index: 10000;">
                🤖 NEXUS Proxy Active
            </div>
            '''
            if '</body>' in content:
                content = content.replace('</body>', overlay + '</body>')
            else:
                content += overlay
            return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            # Fallback to PTNI neural
            from intelligence.ptni_neural import ptni_neural
            return ptni_neural.neural_breakthrough(url), 200, {'Content-Type': 'text/html; charset=utf-8'}
            
    except Exception as e:
        logger.error(f"Standard proxy failed for {url}: {str(e)}")
        from intelligence.ptni_neural import ptni_neural
        return ptni_neural.neural_breakthrough(url), 200, {'Content-Type': 'text/html; charset=utf-8'}

@app.route('/ptni-bypass/<path:url>')
def ptni_advanced_bypass(url):
    """Advanced PTNI neural bypass system"""
    try:
        from intelligence.ptni_neural import ptni_neural
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.info(f"PTNI Neural: Processing {url}")
        
        content = ptni_neural.neural_breakthrough(url)
        return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"PTNI Neural failed for {url}: {str(e)}")
        return f'''
        <html>
        <head><title>PTNI Neural Error</title></head>
        <body style="background: #0d1117; color: #e6edf3; font-family: system-ui; padding: 50px; text-align: center;">
            <h2>🧠 PTNI Neural System</h2>
            <p>Neural breakthrough encountered an error</p>
            <p><strong>Target:</strong> {url}</p>
            <p><strong>Error:</strong> {str(e)}</p>
            <button onclick="window.location.reload()" style="background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                Retry Neural Breakthrough
            </button>
        </body>
        </html>
        ''', 500

@app.route('/api/system/status')
def api_system_status():
    """System status endpoint"""
    try:
        status = {
            'system': 'operational',
            'dashboards': {
                'traxovo': traxovo.get_status(),
                'dwc': dwc.get_status(),
                'jdd': jdd.get_status(),
                'crypto_nexus_trade': crypto_nexus_trade.get_status()
            },
            'intelligence': qni.get_status(),
            'timestamp': datetime.utcnow().isoformat()
        }
        return jsonify(status)
    except Exception as e:
        log_system_event('error', f'System status error: {str(e)}', 'routes')
        return jsonify({'error': 'Status check failed'}), 500

@app.errorhandler(404)
def not_found_error(error):
    log_system_event('warning', f'404 error: {request.url}', 'routes')
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    log_system_event('error', f'500 error: {str(error)}', 'routes')
    db.session.rollback()
    return render_template('error.html', error="Internal server error"), 500
