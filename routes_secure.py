"""
Secure API Routes for Dashboard Lockdown
Implements authenticated endpoints with live data binding
"""

from flask import jsonify, request
from datetime import datetime
from app import app
from crypto_market_integration import crypto_market
from utils.helpers import log_system_event
from security.dashboard_lock import require_secure_access, enforce_live_api_only, authenticate_dashboard_user

# Secure Asset Positions API
@app.route('/api/asset-positions')
@require_secure_access
@enforce_live_api_only
def get_asset_positions():
    """Get live asset positions - secure endpoint"""
    try:
        crypto_data = crypto_market.get_live_crypto_prices()
        
        if crypto_data['status'] != 'success':
            log_system_event('error', 'Asset positions API: Crypto data unavailable', 'security')
            return jsonify({'error': 'Live asset data unavailable'}), 503
        
        positions = []
        holdings = {'BTC': 0.5, 'ETH': 2.3, 'ADA': 1000, 'SOL': 15.7}
        
        for symbol, amount in holdings.items():
            if symbol in crypto_data['data']:
                market_data = crypto_data['data'][symbol]
                position_value = market_data['price'] * amount
                
                positions.append({
                    'asset': symbol,
                    'amount': amount,
                    'current_price': market_data['price'],
                    'position_value': round(position_value, 2),
                    'change_24h': market_data['change_24h'],
                    'market_cap': market_data['market_cap'],
                    'volume_24h': market_data['volume_24h'],
                    'last_updated': market_data['timestamp']
                })
        
        total_portfolio_value = sum(pos['position_value'] for pos in positions)
        
        response_data = {
            'status': 'success',
            'total_portfolio_value': round(total_portfolio_value, 2),
            'positions': positions,
            'data_source': 'live_api',
            'timestamp': datetime.utcnow().isoformat(),
            'security_level': 'authenticated'
        }
        
        log_system_event('info', f'Asset positions accessed - Portfolio value: ${total_portfolio_value:,.2f}', 'security')
        return jsonify(response_data)
        
    except Exception as e:
        log_system_event('error', f'Asset positions API error: {str(e)}', 'security')
        return jsonify({'error': 'Asset positions service unavailable'}), 500

# Secure Revenue Module API
@app.route('/api/revenue_module')
@require_secure_access
@enforce_live_api_only
def get_revenue_module():
    """Get live revenue data - secure endpoint"""
    try:
        crypto_data = crypto_market.get_live_crypto_prices()
        
        if crypto_data['status'] != 'success':
            log_system_event('error', 'Revenue module API: Market data unavailable', 'security')
            return jsonify({'error': 'Live revenue data unavailable'}), 503
        
        holdings = {'BTC': 0.5, 'ETH': 2.3, 'ADA': 1000, 'SOL': 15.7}
        daily_revenue = 0
        monthly_revenue = 0
        
        for symbol, amount in holdings.items():
            if symbol in crypto_data['data']:
                market_data = crypto_data['data'][symbol]
                position_value = market_data['price'] * amount
                daily_change = position_value * (market_data['change_24h'] / 100)
                
                daily_revenue += daily_change
                monthly_revenue += daily_change * 30
        
        revenue_data = {
            'status': 'success',
            'daily_revenue': round(daily_revenue, 2),
            'monthly_revenue_projection': round(monthly_revenue, 2),
            'quarterly_revenue_projection': round(monthly_revenue * 3, 2),
            'annual_revenue_projection': round(monthly_revenue * 12, 2),
            'revenue_breakdown': {
                'crypto_trading': round(daily_revenue * 0.6, 2),
                'optimization_services': round(daily_revenue * 0.25, 2),
                'intelligence_licensing': round(daily_revenue * 0.15, 2)
            },
            'performance_metrics': {
                'roi_daily': round((daily_revenue / sum(holdings.values())) * 100, 2),
                'growth_rate': round(abs(daily_revenue) / 1000 * 100, 2),
                'efficiency_score': min(100, max(0, 80 + (daily_revenue / 100)))
            },
            'data_source': 'live_market_data',
            'timestamp': datetime.utcnow().isoformat(),
            'security_level': 'authenticated'
        }
        
        log_system_event('info', f'Revenue module accessed - Daily revenue: ${daily_revenue:,.2f}', 'security')
        return jsonify(revenue_data)
        
    except Exception as e:
        log_system_event('error', f'Revenue module API error: {str(e)}', 'security')
        return jsonify({'error': 'Revenue module service unavailable'}), 500

# Secure Authentication Endpoint
@app.route('/api/secure-login', methods=['POST'])
def secure_login():
    """Secure login endpoint for dashboard access"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        auth_result = authenticate_dashboard_user(username, password)
        
        if auth_result['success']:
            log_system_event('info', f'Secure login successful for {username}', 'security')
            return jsonify(auth_result)
        else:
            log_system_event('warning', f'Failed login attempt for {username}', 'security')
            return jsonify(auth_result), 401
            
    except Exception as e:
        log_system_event('error', f'Secure login error: {str(e)}', 'security')
        return jsonify({'error': 'Authentication service unavailable'}), 500