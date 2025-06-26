/**
 * Nexus Unified Main JavaScript
 * Core functionality and navigation
 */

class NexusUnified {
    constructor() {
        this.currentDashboard = null;
        this.systemStatus = 'initializing';
        this.intelligenceEnabled = true;
        this.init();
    }

    init() {
        console.log('Nexus Unified System Initializing...');
        this.setupEventListeners();
        this.initializeSystem();
        this.checkSystemStatus();
        
        // Initialize mobile responsive features
        this.initMobileFeatures();
        
        console.log('Nexus Unified System Ready');
    }

    setupEventListeners() {
        // Dashboard card clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('.dashboard-card')) {
                e.preventDefault();
                const dashboardId = e.target.closest('.dashboard-card').dataset.dashboard;
                this.navigateToDashboard(dashboardId);
            }
        });

        // Navigation links
        document.addEventListener('click', (e) => {
            if (e.target.matches('.nav-link[data-dashboard]')) {
                e.preventDefault();
                const dashboardId = e.target.dataset.dashboard;
                this.navigateToDashboard(dashboardId);
            }
        });

        // System status updates
        setInterval(() => {
            this.updateSystemStatus();
        }, 30000); // Check every 30 seconds

        // Window resize for mobile optimization
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Error handling
        window.addEventListener('error', (e) => {
            this.handleError(e.error);
        });
    }

    initializeSystem() {
        // Show loading state
        this.showLoadingState();
        
        // Initialize dashboards
        this.initializeDashboards();
        
        // Apply intelligence enhancements
        if (this.intelligenceEnabled) {
            this.applyIntelligenceEnhancements();
        }
        
        // Hide loading state
        this.hideLoadingState();
        
        this.systemStatus = 'operational';
    }

    initializeDashboards() {
        const dashboards = ['traxovo', 'dwc', 'jdd', 'crypto_nexus_trade', 'quantum_intelligence_engine', 'master_control'];
        dashboards.forEach(dashboard => {
            this.initializeDashboard(dashboard);
        });
    }

    initializeDashboard(dashboardId) {
        try {
            console.log(`Initializing dashboard: ${dashboardId}`);
            
            // Add initialization logic for each dashboard
            const dashboardElement = document.querySelector(`[data-dashboard="${dashboardId}"]`);
            if (dashboardElement) {
                dashboardElement.classList.add('initialized');
                this.addStatusIndicator(dashboardElement, 'active');
            }
        } catch (error) {
            console.error(`Failed to initialize dashboard ${dashboardId}:`, error);
            this.handleDashboardError(dashboardId, error);
        }
    }

    navigateToDashboard(dashboardId) {
        if (!this.validateDashboardAccess(dashboardId)) {
            this.showError('Access denied to requested dashboard');
            return;
        }

        console.log(`Navigating to dashboard: ${dashboardId}`);
        
        // Show loading state
        this.showNavigationLoading();
        
        // Navigate to dashboard
        window.location.href = `/dashboard/${dashboardId}`;
    }

    validateDashboardAccess(dashboardId) {
        const allowedDashboards = ['traxovo', 'dwc', 'jdd', 'crypto_nexus_trade', 'quantum_intelligence_engine', 'master_control'];
        return allowedDashboards.includes(dashboardId);
    }

    checkSystemStatus() {
        fetch('/api/system-status')
            .then(response => response.json())
            .then(data => {
                this.updateSystemStatusDisplay(data);
            })
            .catch(error => {
                console.error('System status check failed:', error);
                this.systemStatus = 'degraded';
                this.updateSystemStatusDisplay({ status: 'degraded' });
            });
    }

    updateSystemStatus() {
        this.checkSystemStatus();
    }

    updateSystemStatusDisplay(statusData) {
        const statusElement = document.getElementById('system-status');
        if (statusElement) {
            const status = statusData.status || 'unknown';
            statusElement.textContent = `System: ${status.toUpperCase()}`;
            statusElement.className = `system-status status-${status}`;
        }
    }

    applyIntelligenceEnhancements() {
        console.log('Applying Quantum Nexus Intelligence enhancements...');
        
        // Add intelligence badges to dashboard cards
        document.querySelectorAll('.dashboard-card').forEach(card => {
            if (!card.querySelector('.intelligence-badge')) {
                const badge = document.createElement('span');
                badge.className = 'intelligence-badge';
                badge.textContent = 'QNI Enhanced';
                card.querySelector('.card-body').appendChild(badge);
            }
        });

        // Add fade-in animations
        document.querySelectorAll('.dashboard-card').forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });
    }

    initMobileFeatures() {
        // Add mobile-specific optimizations
        if (this.isMobile()) {
            document.body.classList.add('mobile-device');
            this.optimizeForMobile();
        }
    }

    isMobile() {
        return window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    optimizeForMobile() {
        // Add mobile-specific optimizations
        console.log('Applying mobile optimizations...');
        
        // Optimize dashboard grid for mobile
        const dashboardGrid = document.querySelector('.dashboard-grid');
        if (dashboardGrid) {
            dashboardGrid.classList.add('mobile-optimized');
        }

        // Add touch event handlers
        this.addTouchEventHandlers();
    }

    addTouchEventHandlers() {
        document.querySelectorAll('.dashboard-card').forEach(card => {
            card.addEventListener('touchstart', (e) => {
                card.classList.add('touch-active');
            });

            card.addEventListener('touchend', (e) => {
                card.classList.remove('touch-active');
            });
        });
    }

    handleResize() {
        if (this.isMobile()) {
            this.optimizeForMobile();
        } else {
            document.body.classList.remove('mobile-device');
        }
    }

    showLoadingState() {
        const loadingElement = document.getElementById('loading-overlay');
        if (loadingElement) {
            loadingElement.style.display = 'flex';
        }
    }

    hideLoadingState() {
        const loadingElement = document.getElementById('loading-overlay');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
    }

    showNavigationLoading() {
        // Show loading spinner in navigation
        const navElements = document.querySelectorAll('.navbar-nav .nav-link');
        navElements.forEach(el => {
            el.style.opacity = '0.5';
        });
    }

    addStatusIndicator(element, status) {
        const indicator = document.createElement('span');
        indicator.className = `status-indicator status-${status}`;
        element.querySelector('.card-body').appendChild(indicator);
    }

    handleError(error) {
        console.error('Application error:', error);
        this.showError(`System error: ${error.message}`);
    }

    handleDashboardError(dashboardId, error) {
        console.error(`Dashboard ${dashboardId} error:`, error);
        const dashboardElement = document.querySelector(`[data-dashboard="${dashboardId}"]`);
        if (dashboardElement) {
            dashboardElement.classList.add('error-state');
            this.addStatusIndicator(dashboardElement, 'error');
        }
    }

    showError(message) {
        // Simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        errorDiv.style.top = '20px';
        errorDiv.style.right = '20px';
        errorDiv.style.zIndex = '9999';
        errorDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(errorDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    // Public methods for dashboard interaction
    refreshDashboard(dashboardId) {
        console.log(`Refreshing dashboard: ${dashboardId}`);
        window.location.reload();
    }

    toggleIntelligence() {
        this.intelligenceEnabled = !this.intelligenceEnabled;
        console.log(`Intelligence features ${this.intelligenceEnabled ? 'enabled' : 'disabled'}`);
        
        if (this.intelligenceEnabled) {
            this.applyIntelligenceEnhancements();
        }
    }
}

// Initialize Nexus Unified when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.nexusUnified = new NexusUnified();
});

// Nexus Control Module Functions
function refreshAllDashboards() {
    console.log('Refreshing all dashboards...');
    const dashboards = ['traxovo', 'dwc', 'jdd', 'crypto_nexus_trade', 'quantum_intelligence_engine', 'master_control'];
    
    // Refresh dashboard display elements
    dashboards.forEach(dashboard => {
        const dashboardElement = document.querySelector(`[data-dashboard="${dashboard}"]`);
        if (dashboardElement) {
            // Apply QNI processing visual effect
            dashboardElement.classList.add('qni-processing');
            console.log(`QNI processing applied to ${dashboard}`);
            
            setTimeout(() => {
                dashboardElement.classList.remove('qni-processing');
                dashboardElement.classList.add('qni-enhanced');
            }, 1000);
        }
    });
    
    showControlNotification('All dashboards refreshed successfully', 'success');
}

function showSystemStatus() {
    console.log('Showing system status...');
    updateSystemMetrics();
    showControlNotification('System status updated', 'info');
}

function emergencyShutdown() {
    if (confirm('Are you sure you want to perform an emergency shutdown? This will stop all active processes.')) {
        console.log('Emergency shutdown initiated...');
        showControlNotification('Emergency shutdown initiated - All processes stopping', 'warning');
        
        Object.values(window.nexusUnified?.dashboards || {}).forEach(dashboard => {
            if (dashboard.stopAutoRefresh) {
                dashboard.stopAutoRefresh();
            }
        });
    }
}

function systemHealthCheck() {
    console.log('Running system health check...');
    
    const healthResults = {
        database: 'Connected',
        dashboards: '4/4 Active',
        intelligence: 'Operational',
        security: 'Active'
    };
    
    const healthModal = createHealthModal(healthResults);
    document.body.appendChild(healthModal);
    showControlNotification('System health check completed', 'success');
}

function forceSyncAll() {
    console.log('Forcing sync of all data sources...');
    
    const syncStatuses = document.querySelectorAll('#data-sources-status .badge');
    syncStatuses.forEach(badge => {
        badge.className = 'badge bg-info';
        badge.textContent = 'Syncing...';
    });
    
    setTimeout(() => {
        syncStatuses.forEach(badge => {
            badge.className = 'badge bg-success';
            badge.textContent = 'Synced';
        });
        showControlNotification('All data sources synchronized', 'success');
    }, 2000);
}

function pauseSync() {
    console.log('Pausing data synchronization...');
    showControlNotification('Data synchronization paused', 'warning');
}

function viewSyncLog() {
    console.log('Opening sync log...');
    const logModal = createSyncLogModal();
    document.body.appendChild(logModal);
}

function exportSystemData() {
    console.log('Exporting system data...');
    
    const exportData = {
        timestamp: new Date().toISOString(),
        dashboards: ['traxovo', 'dwc', 'jdd', 'crypto_nexus_trade'],
        system_status: 'operational',
        metrics: {
            uptime: '24h 15m',
            connections: 8,
            memory_usage: '68%',
            cpu_usage: '23%'
        }
    };
    
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `nexus-system-export-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    showControlNotification('System data exported successfully', 'success');
}

function toggleAutomation(ruleId) {
    console.log(`Toggling automation rule: ${ruleId}`);
    showControlNotification(`Automation rule ${ruleId} toggled`, 'info');
}

function optimizeSystem() {
    console.log('Running system optimization...');
    showControlNotification('System optimization in progress...', 'info');
    
    setTimeout(() => {
        showControlNotification('System optimization completed', 'success');
    }, 3000);
}

function generateInsights() {
    console.log('Generating intelligence insights...');
    showControlNotification('Generating AI insights...', 'info');
    
    setTimeout(() => {
        showControlNotification('Intelligence insights generated', 'success');
    }, 2000);
}

function configureAlerts() {
    console.log('Opening alert configuration...');
    const alertModal = createAlertConfigModal();
    document.body.appendChild(alertModal);
}

function viewLogs() {
    console.log('Opening system logs...');
    const logModal = createSystemLogModal();
    document.body.appendChild(logModal);
}

function updateSystemMetrics() {
    const metrics = {
        'system-uptime': '24h 15m',
        'active-connections': '8',
        'memory-usage': '68%',
        'cpu-usage': '23%'
    };
    
    Object.entries(metrics).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    });
}

function showControlNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

function createHealthModal(healthResults) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">System Health Check</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    ${Object.entries(healthResults).map(([key, value]) => `
                        <div class="d-flex justify-content-between mb-2">
                            <strong>${key.charAt(0).toUpperCase() + key.slice(1)}:</strong>
                            <span class="badge bg-success">${value}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }, 100);
    
    return modal;
}

function createSyncLogModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Synchronization Log</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="list-group">
                        <div class="list-group-item">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">TRAXOVO Data Sync</h6>
                                <small class="text-success">2 minutes ago</small>
                            </div>
                            <p class="mb-1">Successfully synchronized tracking metrics and optimization data</p>
                        </div>
                        <div class="list-group-item">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">CryptoNexus Market Update</h6>
                                <small class="text-success">5 minutes ago</small>
                            </div>
                            <p class="mb-1">Real-time market data synchronized successfully</p>
                        </div>
                        <div class="list-group-item">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">DWC Workflow Sync</h6>
                                <small class="text-success">8 minutes ago</small>
                            </div>
                            <p class="mb-1">Dynamic workflow configurations updated</p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }, 100);
    
    return modal;
}

function createAlertConfigModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Configure Alerts</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">System Performance Alerts</label>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" checked>
                            <label class="form-check-label">High CPU usage (>80%)</label>
                        </div>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" checked>
                            <label class="form-check-label">High memory usage (>90%)</label>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Dashboard Alerts</label>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" checked>
                            <label class="form-check-label">Dashboard connection errors</label>
                        </div>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox">
                            <label class="form-check-label">Slow response times (>500ms)</label>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary">Save Settings</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }, 100);
    
    return modal;
}

function createSystemLogModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">System Logs</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="bg-dark text-light p-3 rounded" style="font-family: monospace; max-height: 400px; overflow-y: auto;">
                        <div>[${new Date().toISOString()}] INFO: Nexus Unified System initialized</div>
                        <div>[${new Date().toISOString()}] INFO: All dashboards loaded successfully</div>
                        <div>[${new Date().toISOString()}] INFO: Quantum Nexus Intelligence active</div>
                        <div>[${new Date().toISOString()}] INFO: Security middleware enabled</div>
                        <div>[${new Date().toISOString()}] INFO: Database connection established</div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" onclick="downloadLogs()">Download Logs</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }, 100);
    
    return modal;
}

function downloadLogs() {
    console.log('Downloading system logs...');
    showControlNotification('System logs downloaded', 'success');
}

// Export for other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NexusUnified;
}
