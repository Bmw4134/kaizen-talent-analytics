/**
 * Dashboard-specific JavaScript functionality
 * Handles individual dashboard operations and data management
 */

class DashboardManager {
    constructor(dashboardName) {
        this.dashboardName = dashboardName;
        this.refreshInterval = null;
        this.lastUpdate = null;
        this.isActive = false;
        this.init();
    }

    init() {
        console.log(`Initializing dashboard: ${this.dashboardName}`);
        this.setupEventListeners();
        this.startAutoRefresh();
        this.loadDashboardData();
        this.isActive = true;
    }

    setupEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshDashboard();
            });
        }

        // Settings button
        const settingsBtn = document.getElementById('dashboard-settings');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => {
                this.showSettings();
            });
        }

        // Export button
        const exportBtn = document.getElementById('export-data');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportData();
            });
        }

        // Auto-refresh toggle
        const autoRefreshToggle = document.getElementById('auto-refresh-toggle');
        if (autoRefreshToggle) {
            autoRefreshToggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.startAutoRefresh();
                } else {
                    this.stopAutoRefresh();
                }
            });
        }
    }

    loadDashboardData() {
        this.showLoadingState();
        
        fetch(`/api/dashboard-data/${this.dashboardName}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                this.processData(data);
                this.renderDashboard(data);
                this.lastUpdate = new Date();
                this.updateLastRefreshTime();
            })
            .catch(error => {
                console.error(`Failed to load ${this.dashboardName} data:`, error);
                this.showError(`Failed to load dashboard data: ${error.message}`);
            })
            .finally(() => {
                this.hideLoadingState();
            });
    }

    processData(data) {
        // Apply intelligence enhancements if available
        if (data.intelligence) {
            console.log(`Intelligence data available for ${this.dashboardName}:`, data.intelligence);
            this.applyIntelligenceInsights(data.intelligence);
        }

        // Process QNI metadata
        if (data.qni_metadata) {
            console.log(`QNI processing applied to ${this.dashboardName}`);
            this.displayQNIMetadata(data.qni_metadata);
        }
    }

    renderDashboard(data) {
        try {
            // Render based on dashboard type
            switch (this.dashboardName) {
                case 'traxovo':
                    this.renderTraxovo(data);
                    break;
                case 'dwc':
                    this.renderDWC(data);
                    break;
                case 'jdd':
                    this.renderJDD(data);
                    break;
                case 'crypto_nexus_trade':
                    this.renderCryptoNexusTrade(data);
                    break;
                default:
                    this.renderGenericDashboard(data);
            }
        } catch (error) {
            console.error(`Error rendering ${this.dashboardName}:`, error);
            this.showError('Failed to render dashboard');
        }
    }

    renderTraxovo(data) {
        // Update TRAXOVO specific elements
        this.updateMetric('active-tracks', data.metrics?.active_tracks || 0);
        this.updateMetric('optimization-score', (data.metrics?.optimization_score || 0).toFixed(2));
        this.updateMetric('system-efficiency', (data.metrics?.system_efficiency || 0).toFixed(2) + '%');
        
        // Update status
        this.updateStatus(data.status || 'unknown');
        
        // Render optimization recommendations
        this.renderOptimizationRecommendations(data.optimization?.recommendations || []);
    }

    renderDWC(data) {
        // Update DWC specific elements
        this.updateMetric('active-workflows', data.workflow?.active_workflows || 0);
        this.updateMetric('pending-tasks', data.workflow?.pending_tasks || 0);
        this.updateMetric('completed-today', data.workflow?.completed_today || 0);
        this.updateMetric('system-load', (data.workflow?.system_load || 0).toFixed(1) + '%');
        
        // Update workflow list
        this.renderWorkflowList(data.workflow?.workflows || []);
        
        // Update control panel
        this.renderControlPanel(data.control_panel || {});
    }

    renderJDD(data) {
        // Update JDD specific elements
        this.updateMetric('connected-sources', data.data_sources?.connected_sources || 0);
        this.updateMetric('total-records', data.analytics?.total_records || 0);
        this.updateMetric('processing-queue', data.analytics?.processing_queue || 0);
        this.updateMetric('data-quality-score', (data.data_sources?.data_quality_score || 0).toFixed(2));
        
        // Render data sources
        this.renderDataSources(data.data_sources?.sources || []);
        
        // Render analytics
        this.renderAnalytics(data.analytics || {});
    }

    renderCryptoNexusTrade(data) {
        // Update crypto trading specific elements
        this.updateMetric('portfolio-value', this.formatCurrency(data.market?.portfolio_value || 0));
        this.updateMetric('daily-change', this.formatPercentage(data.market?.daily_change || 0));
        this.updateMetric('active-trades', data.market?.active_trades || 0);
        this.updateMetric('market-status', data.market?.market_status || 'closed');
        
        // Render trading data
        this.renderTradingData(data.trading || {});
        
        // Render market data
        this.renderMarketData(data.market || {});
    }

    renderGenericDashboard(data) {
        // Generic dashboard rendering
        const container = document.getElementById('dashboard-content');
        if (container && data) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <h5>Dashboard: ${this.dashboardName}</h5>
                    <p>Status: ${data.status || 'active'}</p>
                    <p>Version: ${data.version || 'unknown'}</p>
                    <p>Last Updated: ${data.timestamp || 'unknown'}</p>
                </div>
            `;
        }
    }

    updateMetric(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
            element.classList.add('updated');
            setTimeout(() => element.classList.remove('updated'), 1000);
        }
    }

    updateStatus(status) {
        const statusElement = document.getElementById('dashboard-status');
        if (statusElement) {
            statusElement.textContent = status.toUpperCase();
            statusElement.className = `badge status-${status}`;
        }
    }

    renderOptimizationRecommendations(recommendations) {
        const container = document.getElementById('optimization-recommendations');
        if (container) {
            if (recommendations.length === 0) {
                container.innerHTML = '<p class="text-muted">No optimization recommendations available.</p>';
                return;
            }
            
            const html = recommendations.map(rec => `
                <div class="alert alert-info">
                    <strong>${rec.title || 'Recommendation'}</strong>
                    <p>${rec.description || 'No description available'}</p>
                </div>
            `).join('');
            
            container.innerHTML = html;
        }
    }

    renderWorkflowList(workflows) {
        const container = document.getElementById('workflow-list');
        if (container) {
            if (workflows.length === 0) {
                container.innerHTML = '<p class="text-muted">No active workflows.</p>';
                return;
            }
            
            const html = workflows.map(workflow => `
                <div class="card mb-2">
                    <div class="card-body">
                        <h6>${workflow.name || 'Unnamed Workflow'}</h6>
                        <p class="text-muted">${workflow.description || 'No description'}</p>
                        <span class="badge bg-${workflow.status === 'running' ? 'success' : 'secondary'}">
                            ${workflow.status || 'unknown'}
                        </span>
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = html;
        }
    }

    renderControlPanel(controlData) {
        const container = document.getElementById('control-panel');
        if (container) {
            container.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h6>System Health</h6>
                        <p class="text-success">${controlData.system_health || 'Unknown'}</p>
                    </div>
                    <div class="col-md-6">
                        <h6>Configuration Status</h6>
                        <p class="text-info">${controlData.configuration_status || 'Unknown'}</p>
                    </div>
                </div>
            `;
        }
    }

    renderDataSources(sources) {
        const container = document.getElementById('data-sources');
        if (container) {
            if (sources.length === 0) {
                container.innerHTML = '<p class="text-muted">No data sources connected.</p>';
                return;
            }
            
            const html = sources.map(source => `
                <div class="card mb-2">
                    <div class="card-body">
                        <h6>${source.name || 'Unnamed Source'}</h6>
                        <p class="text-muted">${source.type || 'Unknown type'}</p>
                        <span class="badge bg-${source.status === 'connected' ? 'success' : 'warning'}">
                            ${source.status || 'unknown'}
                        </span>
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = html;
        }
    }

    renderAnalytics(analytics) {
        const container = document.getElementById('analytics-data');
        if (container) {
            container.innerHTML = `
                <div class="row">
                    <div class="col-md-4">
                        <div class="metric-card">
                            <div class="metric-value">${analytics.insights_generated || 0}</div>
                            <div class="metric-label">Insights Generated</div>
                        </div>
                    </div>
                    <div class="col-md-8">
                        <h6>Analytics Status</h6>
                        <p class="text-info">${analytics.analytics_status || 'Unknown'}</p>
                    </div>
                </div>
            `;
        }
    }

    renderTradingData(trading) {
        const container = document.getElementById('trading-data');
        if (container) {
            const performance = trading.performance_metrics || {};
            container.innerHTML = `
                <div class="row">
                    <div class="col-md-3">
                        <div class="metric-card">
                            <div class="metric-value">${this.formatCurrency(performance.total_profit_loss || 0)}</div>
                            <div class="metric-label">P&L</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric-card">
                            <div class="metric-value">${this.formatPercentage(performance.win_rate || 0)}</div>
                            <div class="metric-label">Win Rate</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric-card">
                            <div class="metric-value">${performance.total_trades || 0}</div>
                            <div class="metric-label">Total Trades</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="metric-card">
                            <div class="metric-value">${performance.avg_trade_duration || '0h'}</div>
                            <div class="metric-label">Avg Duration</div>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    renderMarketData(market) {
        const container = document.getElementById('market-data');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-info">
                    <h6>Market Status: ${(market.market_status || 'closed').toUpperCase()}</h6>
                    <p>Last Update: ${market.last_update || 'Unknown'}</p>
                    ${market.alerts && market.alerts.length > 0 ? 
                        `<div class="mt-2">
                            <strong>Alerts:</strong>
                            <ul>${market.alerts.map(alert => `<li>${alert}</li>`).join('')}</ul>
                        </div>` : 
                        ''
                    }
                </div>
            `;
        }
    }

    applyIntelligenceInsights(intelligence) {
        // Display intelligence insights
        const container = document.getElementById('intelligence-insights');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-primary">
                    <h6><i class="fas fa-brain"></i> Quantum Nexus Intelligence</h6>
                    <p>${intelligence.insights || 'Intelligence processing completed'}</p>
                    <small>Optimization Score: ${(intelligence.optimization_score || 0).toFixed(2)}</small>
                </div>
            `;
        }
    }

    displayQNIMetadata(metadata) {
        const container = document.getElementById('qni-metadata');
        if (container) {
            container.innerHTML = `
                <div class="card border-primary">
                    <div class="card-body">
                        <h6 class="card-title">QNI Processing</h6>
                        <p class="card-text">
                            Processing Time: ${metadata.processing_time_ms || 0}ms<br>
                            Confidence: ${(metadata.confidence_score || 0).toFixed(2)}<br>
                            Processed: ${metadata.timestamp || 'Unknown'}
                        </p>
                    </div>
                </div>
            `;
        }
    }

    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        
        this.refreshInterval = setInterval(() => {
            if (this.isActive) {
                this.loadDashboardData();
            }
        }, 30000); // Refresh every 30 seconds
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    refreshDashboard() {
        console.log(`Manually refreshing ${this.dashboardName} dashboard`);
        this.loadDashboardData();
    }

    showSettings() {
        // Placeholder for dashboard settings modal
        alert('Dashboard settings coming soon!');
    }

    exportData() {
        // Simple data export functionality
        const dataStr = JSON.stringify({
            dashboard: this.dashboardName,
            lastUpdate: this.lastUpdate,
            timestamp: new Date().toISOString()
        }, null, 2);
        
        const blob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.dashboardName}_export_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    updateLastRefreshTime() {
        const element = document.getElementById('last-refresh');
        if (element && this.lastUpdate) {
            element.textContent = `Last updated: ${this.lastUpdate.toLocaleTimeString()}`;
        }
    }

    showLoadingState() {
        const loadingElements = document.querySelectorAll('.loading-spinner');
        loadingElements.forEach(el => el.style.display = 'inline-block');
        
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<span class="loading-spinner"></span> Loading...';
        }
    }

    hideLoadingState() {
        const loadingElements = document.querySelectorAll('.loading-spinner');
        loadingElements.forEach(el => el.style.display = 'none');
        
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
        }
    }

    showError(message) {
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    formatPercentage(value) {
        return `${value.toFixed(2)}%`;
    }

    destroy() {
        this.isActive = false;
        this.stopAutoRefresh();
    }
}

// Auto-initialize dashboard manager if dashboard name is available
document.addEventListener('DOMContentLoaded', () => {
    const dashboardElement = document.querySelector('[data-dashboard-name]');
    if (dashboardElement) {
        const dashboardName = dashboardElement.dataset.dashboardName;
        window.dashboardManager = new DashboardManager(dashboardName);
    }
});
