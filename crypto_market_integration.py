"""
Real-Time Cryptocurrency Market Data Integration
Connects to Perplexity AI and CoinGecko APIs for live market data
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class CryptoMarketIntegration:
    def __init__(self):
        self.perplexity_api_key = os.environ.get('PERPLEXITY_API_KEY')
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.perplexity_base_url = "https://api.perplexity.ai"
        
        if not self.perplexity_api_key:
            logger.warning("PERPLEXITY_API_KEY not found in environment variables")
    
    def get_live_crypto_prices(self, symbols = None) -> Dict[str, Any]:
        """Fetch live cryptocurrency prices from CoinGecko API"""
        if not symbols:
            symbols = ['bitcoin', 'ethereum', 'cardano', 'solana']
        
        try:
            # CoinGecko API call for real-time prices
            coins_param = ','.join(symbols)
            url = f"{self.coingecko_base_url}/simple/price"
            params = {
                'ids': coins_param,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            market_data = response.json()
            
            # Transform data for NEXUS dashboard
            transformed_data = {}
            symbol_mapping = {
                'bitcoin': 'BTC',
                'ethereum': 'ETH', 
                'cardano': 'ADA',
                'solana': 'SOL'
            }
            
            for coin_id, data in market_data.items():
                symbol = symbol_mapping.get(coin_id, coin_id.upper())
                price_change = data.get('usd_24h_change', 0)
                
                transformed_data[symbol] = {
                    'price': data.get('usd', 0),
                    'change_24h': round(price_change, 2),
                    'volume_24h': data.get('usd_24h_vol', 0),
                    'market_cap': data.get('usd_market_cap', 0),
                    'signal': self._generate_trading_signal(price_change),
                    'timestamp': datetime.utcnow().isoformat()
                }
            
            return {
                'status': 'success',
                'data': transformed_data,
                'source': 'CoinGecko API',
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"CoinGecko API error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Market data unavailable: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def get_market_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get AI-powered market analysis from Perplexity"""
        if not self.perplexity_api_key:
            return {
                'status': 'error',
                'message': 'Perplexity API key not configured'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.perplexity_api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"Provide a brief technical analysis and market sentiment for {symbol} cryptocurrency today. Include price trend, support/resistance levels, and trading recommendation in 2-3 sentences."
            
            payload = {
                'model': 'llama-3.1-sonar-small-128k-online',
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 200,
                'temperature': 0.2
            }
            
            response = requests.post(
                f"{self.perplexity_base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content']
                
                return {
                    'status': 'success',
                    'symbol': symbol,
                    'analysis': analysis,
                    'confidence': self._extract_confidence(analysis),
                    'recommendation': self._extract_recommendation(analysis),
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                logger.error(f"Perplexity API error: {response.status_code}")
                return {
                    'status': 'error',
                    'message': f'Analysis unavailable: API error {response.status_code}'
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Perplexity API connection error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Analysis unavailable: {str(e)}'
            }
    
    def get_portfolio_insights(self, holdings: Dict[str, float]) -> Dict[str, Any]:
        """Generate portfolio analysis using live market data"""
        try:
            # Get live prices for portfolio holdings
            symbols = list(holdings.keys())
            coin_ids = [self._symbol_to_coingecko_id(symbol) for symbol in symbols]
            
            market_data = self.get_live_crypto_prices(coin_ids)
            
            if market_data['status'] != 'success':
                return market_data
            
            total_value = 0
            portfolio_change = 0
            asset_performance = {}
            
            for symbol, amount in holdings.items():
                if symbol in market_data['data']:
                    price = market_data['data'][symbol]['price']
                    change_24h = market_data['data'][symbol]['change_24h']
                    
                    asset_value = price * amount
                    total_value += asset_value
                    portfolio_change += (asset_value * change_24h / 100)
                    
                    asset_performance[symbol] = {
                        'value': asset_value,
                        'change_24h': change_24h,
                        'weight': 0  # Will calculate after total_value
                    }
            
            # Calculate portfolio weights
            for symbol in asset_performance:
                asset_performance[symbol]['weight'] = round(
                    (asset_performance[symbol]['value'] / total_value) * 100, 2
                ) if total_value > 0 else 0
            
            portfolio_change_percent = round(
                (portfolio_change / total_value) * 100, 2
            ) if total_value > 0 else 0
            
            return {
                'status': 'success',
                'total_value': round(total_value, 2),
                'change_24h_percent': portfolio_change_percent,
                'change_24h_value': round(portfolio_change, 2),
                'asset_performance': asset_performance,
                'risk_score': self._calculate_risk_score(asset_performance),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Portfolio analysis error: {str(e)}")
            return {
                'status': 'error',
                'message': f'Portfolio analysis failed: {str(e)}'
            }
    
    def _generate_trading_signal(self, price_change: float) -> str:
        """Generate trading signal based on price movement"""
        if price_change > 5:
            return "Strong Buy"
        elif price_change > 2:
            return "Buy"
        elif price_change > -2:
            return "Hold"
        elif price_change > -5:
            return "Sell"
        else:
            return "Strong Sell"
    
    def _extract_confidence(self, analysis: str) -> str:
        """Extract confidence level from analysis text"""
        analysis_lower = analysis.lower()
        if any(word in analysis_lower for word in ['strong', 'confident', 'clear']):
            return "High"
        elif any(word in analysis_lower for word in ['moderate', 'likely']):
            return "Medium"
        else:
            return "Low"
    
    def _extract_recommendation(self, analysis: str) -> str:
        """Extract trading recommendation from analysis"""
        analysis_lower = analysis.lower()
        if any(word in analysis_lower for word in ['buy', 'bullish', 'upward']):
            return "Buy"
        elif any(word in analysis_lower for word in ['sell', 'bearish', 'downward']):
            return "Sell"
        else:
            return "Hold"
    
    def _symbol_to_coingecko_id(self, symbol: str) -> str:
        """Convert crypto symbol to CoinGecko ID"""
        mapping = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'ADA': 'cardano',
            'SOL': 'solana',
            'LINK': 'chainlink',
            'DOT': 'polkadot',
            'MATIC': 'matic-network'
        }
        return mapping.get(symbol.upper(), symbol.lower())
    
    def _calculate_risk_score(self, asset_performance: Dict) -> str:
        """Calculate portfolio risk score"""
        if not asset_performance:
            return "Unknown"
        
        volatility_sum = sum(
            abs(asset['change_24h']) for asset in asset_performance.values()
        )
        avg_volatility = volatility_sum / len(asset_performance)
        
        if avg_volatility > 10:
            return "High Risk"
        elif avg_volatility > 5:
            return "Medium Risk"
        else:
            return "Low Risk"

# Global instance for use in routes
crypto_market = CryptoMarketIntegration()