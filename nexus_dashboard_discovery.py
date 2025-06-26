"""
NEXUS Dashboard Discovery System
Comprehensive scanning and identification of all dashboard modules
"""

import os
import glob
import importlib
import json
from datetime import datetime

class NEXUSDashboardDiscovery:
    def __init__(self):
        self.discovered_dashboards = {}
        self.scan_locations = [
            'dashboards/',
            'templates/dashboards/',
            'static/dashboards/',
            'attached_assets/',
            'instance/'
        ]
        
    def discover_all_dashboards(self):
        """Discover all dashboard modules across the system"""
        dashboards = {}
        
        # Scan Python dashboard modules
        python_dashboards = self._scan_python_dashboards()
        dashboards.update(python_dashboards)
        
        # Scan HTML templates
        template_dashboards = self._scan_template_dashboards()
        dashboards.update(template_dashboards)
        
        # Scan attached assets for additional dashboards
        asset_dashboards = self._scan_asset_dashboards()
        dashboards.update(asset_dashboards)
        
        # Scan database for recorded dashboard sessions
        db_dashboards = self._scan_database_dashboards()
        dashboards.update(db_dashboards)
        
        self.discovered_dashboards = dashboards
        return dashboards
    
    def _scan_python_dashboards(self):
        """Scan for Python dashboard modules"""
        dashboards = {}
        
        if os.path.exists('dashboards/'):
            for file in os.listdir('dashboards/'):
                if file.endswith('.py') and file != '__init__.py':
                    dashboard_name = file[:-3]  # Remove .py extension
                    try:
                        module = importlib.import_module(f'dashboards.{dashboard_name}')
                        
                        # Check if module has required dashboard functions
                        if hasattr(module, 'get_dashboard_data'):
                            dashboards[dashboard_name] = {
                                'type': 'python_module',
                                'source': f'dashboards/{file}',
                                'status': 'active',
                                'has_api': hasattr(module, 'get_api_data'),
                                'discovered_at': datetime.utcnow().isoformat()
                            }
                    except Exception as e:
                        dashboards[dashboard_name] = {
                            'type': 'python_module',
                            'source': f'dashboards/{file}',
                            'status': 'error',
                            'error': str(e),
                            'discovered_at': datetime.utcnow().isoformat()
                        }
        
        return dashboards
    
    def _scan_template_dashboards(self):
        """Scan for HTML dashboard templates"""
        dashboards = {}
        
        if os.path.exists('templates/dashboards/'):
            for file in os.listdir('templates/dashboards/'):
                if file.endswith('.html'):
                    dashboard_name = file[:-5]  # Remove .html extension
                    if dashboard_name not in self.discovered_dashboards:
                        dashboards[dashboard_name] = {
                            'type': 'html_template',
                            'source': f'templates/dashboards/{file}',
                            'status': 'template_only',
                            'discovered_at': datetime.utcnow().isoformat()
                        }
        
        return dashboards
    
    def _scan_asset_dashboards(self):
        """Scan attached assets for dashboard configurations"""
        dashboards = {}
        
        # Check for dashboard configurations in attached assets
        asset_patterns = [
            'attached_assets/**/*.json',
            'attached_assets/**/*dashboard*.py',
            'attached_assets/**/*dashboard*.html',
            'attached_assets/**/*nexus*.py'
        ]
        
        for pattern in asset_patterns:
            for file_path in glob.glob(pattern, recursive=True):
                try:
                    # Extract potential dashboard name from file
                    file_name = os.path.basename(file_path)
                    if 'dashboard' in file_name.lower() or 'nexus' in file_name.lower():
                        # Extract dashboard name from filename
                        potential_name = file_name.split('.')[0].lower()
                        potential_name = potential_name.replace('_dashboard', '').replace('dashboard_', '')
                        potential_name = potential_name.replace('nexus_', '').replace('_nexus', '')
                        
                        if potential_name and potential_name not in self.discovered_dashboards:
                            dashboards[potential_name] = {
                                'type': 'asset_file',
                                'source': file_path,
                                'status': 'archived',
                                'discovered_at': datetime.utcnow().isoformat()
                            }
                except Exception:
                    continue
        
        return dashboards
    
    def _scan_database_dashboards(self):
        """Scan database for dashboard session records"""
        dashboards = {}
        
        try:
            from app import db
            from models import DashboardSession
            
            # Get unique dashboard names from database
            with db.app_context():
                unique_dashboards = db.session.query(DashboardSession.dashboard_name).distinct().all()
                
                for (dashboard_name,) in unique_dashboards:
                    if dashboard_name and dashboard_name not in self.discovered_dashboards:
                        dashboards[dashboard_name] = {
                            'type': 'database_record',
                            'source': 'dashboard_session table',
                            'status': 'recorded',
                            'discovered_at': datetime.utcnow().isoformat()
                        }
        except Exception:
            pass
        
        return dashboards
    
    def get_dashboard_count(self):
        """Get total count of discovered dashboards"""
        return len(self.discovered_dashboards)
    
    def get_active_dashboards(self):
        """Get only active/operational dashboards"""
        return {name: info for name, info in self.discovered_dashboards.items() 
                if info.get('status') in ['active', 'operational']}
    
    def get_discovery_report(self):
        """Generate comprehensive discovery report"""
        active_count = len(self.get_active_dashboards())
        total_count = self.get_dashboard_count()
        
        report = {
            'discovery_timestamp': datetime.utcnow().isoformat(),
            'total_dashboards_discovered': total_count,
            'active_dashboards': active_count,
            'discovery_breakdown': {
                'python_modules': len([d for d in self.discovered_dashboards.values() if d['type'] == 'python_module']),
                'html_templates': len([d for d in self.discovered_dashboards.values() if d['type'] == 'html_template']),
                'asset_files': len([d for d in self.discovered_dashboards.values() if d['type'] == 'asset_file']),
                'database_records': len([d for d in self.discovered_dashboards.values() if d['type'] == 'database_record'])
            },
            'dashboard_details': self.discovered_dashboards,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self):
        """Generate recommendations based on discovery results"""
        recommendations = []
        
        active_count = len(self.get_active_dashboards())
        total_count = self.get_dashboard_count()
        
        if total_count > active_count:
            recommendations.append(f"Found {total_count - active_count} additional dashboard(s) that could be activated")
        
        if total_count > 4:
            recommendations.append(f"System has {total_count} total dashboards - consider implementing dashboard grouping")
        
        asset_dashboards = [d for d in self.discovered_dashboards.values() if d['type'] == 'asset_file']
        if asset_dashboards:
            recommendations.append(f"Found {len(asset_dashboards)} dashboard(s) in assets - consider integrating them")
        
        return recommendations

def discover_system_dashboards():
    """Main discovery function"""
    discovery = NEXUSDashboardDiscovery()
    return discovery.discover_all_dashboards()

def get_dashboard_discovery_report():
    """Get comprehensive dashboard discovery report"""
    discovery = NEXUSDashboardDiscovery()
    discovery.discover_all_dashboards()
    return discovery.get_discovery_report()

if __name__ == "__main__":
    report = get_dashboard_discovery_report()
    print(json.dumps(report, indent=2))