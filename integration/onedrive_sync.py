"""
NEXUS OneDrive Sync Connector
Automated file synchronization and backup
"""
import os
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OneDriveConnector:
    def __init__(self):
        self.client_id = os.environ.get('ONEDRIVE_CLIENT_ID')
        self.client_secret = os.environ.get('ONEDRIVE_CLIENT_SECRET')
        self.access_token = os.environ.get('ONEDRIVE_ACCESS_TOKEN')
        self.base_url = 'https://graph.microsoft.com/v1.0'
        
    def is_authenticated(self):
        """Check if OneDrive credentials are available"""
        return bool(self.access_token)
    
    def upload_file(self, file_path, remote_path):
        """Upload file to OneDrive"""
        if not self.is_authenticated():
            return {'error': 'OneDrive authentication required'}
        
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            url = f"{self.base_url}/me/drive/root:/{remote_path}:/content"
            
            with open(file_path, 'rb') as file:
                response = requests.put(url, headers=headers, data=file)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"OneDrive upload failed: {e}")
            return {'error': str(e)}
    
    def sync_nexus_reports(self, reports_dir='reports'):
        """Sync NEXUS reports to OneDrive"""
        if not os.path.exists(reports_dir):
            return {'error': 'Reports directory not found'}
        
        sync_results = []
        for filename in os.listdir(reports_dir):
            if filename.endswith('.json'):
                local_path = os.path.join(reports_dir, filename)
                remote_path = f"NEXUS_Reports/{filename}"
                result = self.upload_file(local_path, remote_path)
                sync_results.append({'file': filename, 'result': result})
        
        return {'synced_files': len(sync_results), 'results': sync_results}

onedrive_connector = OneDriveConnector()