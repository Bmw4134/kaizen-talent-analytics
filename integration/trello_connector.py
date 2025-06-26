"""
NEXUS Trello Integration Connector
Automated workflow synchronization with Trello boards
"""
import os
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TrelloConnector:
    def __init__(self):
        self.api_key = os.environ.get('TRELLO_API_KEY')
        self.token = os.environ.get('TRELLO_TOKEN')
        self.base_url = 'https://api.trello.com/1'
        self.board_id = os.environ.get('TRELLO_BOARD_ID')
        
    def is_authenticated(self):
        """Check if Trello credentials are available"""
        return bool(self.api_key and self.token)
    
    def get_boards(self):
        """Get user's Trello boards"""
        if not self.is_authenticated():
            return {'error': 'Trello credentials required'}
        
        try:
            url = f"{self.base_url}/members/me/boards"
            params = {'key': self.api_key, 'token': self.token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch boards: {e}")
            return {'error': str(e)}
    
    def create_automation_card(self, list_id, title, description=""):
        """Create automated task card"""
        if not self.is_authenticated():
            return {'error': 'Authentication required'}
        
        try:
            url = f"{self.base_url}/cards"
            data = {
                'key': self.api_key,
                'token': self.token,
                'idList': list_id,
                'name': title,
                'desc': description
            }
            response = requests.post(url, data=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to create card: {e}")
            return {'error': str(e)}
    
    def sync_nexus_activities(self, activities):
        """Sync NEXUS activities to Trello"""
        if not self.board_id:
            return {'error': 'Board ID not configured'}
        
        results = []
        for activity in activities:
            result = self.create_automation_card(
                activity.get('list_id'),
                f"NEXUS: {activity.get('title')}",
                activity.get('description', '')
            )
            results.append(result)
        
        return {'synced': len(results), 'results': results}

trello_connector = TrelloConnector()