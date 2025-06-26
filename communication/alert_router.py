"""
NEXUS Alert Router - Multi-channel Communication System
SMS, Email, and Real-time notification distribution
"""
import os
import logging
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertRouter:
    def __init__(self):
        self.channels = {
            'sms': self._init_sms_channel(),
            'email': self._init_email_channel(),
            'dashboard': True  # Always available
        }
        self.alert_queue = []
        
    def _init_sms_channel(self):
        """Initialize SMS channel via Twilio"""
        return bool(os.environ.get('TWILIO_ACCOUNT_SID') and os.environ.get('TWILIO_AUTH_TOKEN'))
    
    def _init_email_channel(self):
        """Initialize email channel via SendGrid"""
        return bool(os.environ.get('SENDGRID_API_KEY'))
    
    def route_alert(self, message, priority=AlertPriority.MEDIUM, channels=None):
        """Route alert to appropriate channels based on priority"""
        alert = {
            'id': len(self.alert_queue) + 1,
            'message': message,
            'priority': priority.value,
            'timestamp': datetime.now().isoformat(),
            'channels_sent': [],
            'status': 'pending'
        }
        
        # Determine channels based on priority if not specified
        if channels is None:
            channels = self._get_channels_for_priority(priority)
        
        # Send to each channel
        for channel in channels:
            if self._send_to_channel(channel, alert):
                alert['channels_sent'].append(channel)
        
        alert['status'] = 'sent' if alert['channels_sent'] else 'failed'
        self.alert_queue.append(alert)
        
        logger.info(f"Alert routed: {message} via {alert['channels_sent']}")
        return alert
    
    def _get_channels_for_priority(self, priority):
        """Get appropriate channels based on alert priority"""
        channel_map = {
            AlertPriority.LOW: ['dashboard'],
            AlertPriority.MEDIUM: ['dashboard', 'email'],
            AlertPriority.HIGH: ['dashboard', 'email', 'sms'],
            AlertPriority.CRITICAL: ['dashboard', 'email', 'sms']
        }
        return channel_map.get(priority, ['dashboard'])
    
    def _send_to_channel(self, channel, alert):
        """Send alert to specific channel"""
        try:
            if channel == 'dashboard':
                return self._send_dashboard_alert(alert)
            elif channel == 'sms' and self.channels['sms']:
                return self._send_sms_alert(alert)
            elif channel == 'email' and self.channels['email']:
                return self._send_email_alert(alert)
            return False
        except Exception as e:
            logger.error(f"Failed to send alert via {channel}: {e}")
            return False
    
    def _send_dashboard_alert(self, alert):
        """Send alert to dashboard interface"""
        # Dashboard alerts are always successful as they're queued
        return True
    
    def _send_sms_alert(self, alert):
        """Send SMS alert via Twilio"""
        try:
            from twilio.rest import Client
            client = Client(
                os.environ.get('TWILIO_ACCOUNT_SID'),
                os.environ.get('TWILIO_AUTH_TOKEN')
            )
            
            phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
            admin_phone = os.environ.get('ADMIN_PHONE_NUMBER', '+1234567890')
            
            message = client.messages.create(
                body=f"NEXUS Alert [{alert['priority'].upper()}]: {alert['message']}",
                from_=phone_number,
                to=admin_phone
            )
            
            return bool(message.sid)
        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            return False
    
    def _send_email_alert(self, alert):
        """Send email alert via SendGrid"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
            
            message = Mail(
                from_email='alerts@nexus-system.com',
                to_emails=os.environ.get('ADMIN_EMAIL', 'admin@example.com'),
                subject=f"NEXUS Alert - {alert['priority'].upper()}",
                html_content=f"""
                <h3>NEXUS System Alert</h3>
                <p><strong>Priority:</strong> {alert['priority'].upper()}</p>
                <p><strong>Message:</strong> {alert['message']}</p>
                <p><strong>Timestamp:</strong> {alert['timestamp']}</p>
                """
            )
            
            response = sg.send(message)
            return response.status_code == 202
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False
    
    def get_recent_alerts(self, limit=10):
        """Get recent alerts from queue"""
        return self.alert_queue[-limit:] if self.alert_queue else []
    
    def get_channel_status(self):
        """Get status of all communication channels"""
        return {
            'sms': 'active' if self.channels['sms'] else 'requires_config',
            'email': 'active' if self.channels['email'] else 'requires_config',
            'dashboard': 'active'
        }

alert_router = AlertRouter()