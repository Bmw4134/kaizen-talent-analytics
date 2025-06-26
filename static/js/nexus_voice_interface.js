
// NEXUS Voice Command Interface
class NEXUSVoiceInterface {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.currentMode = 'D';
        this.gestureConfirmed = false;
        this.initVoiceRecognition();
        this.bindGestureModes();
    }
    
    initVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            this.recognition.onresult = (event) => this.handleVoiceResult(event);
            this.recognition.onerror = (event) => console.error('Voice recognition error:', event.error);
            this.recognition.onstart = () => this.showVoiceIndicator();
            this.recognition.onend = () => this.hideVoiceIndicator();
        }
    }
    
    bindGestureModes() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey) {
                switch(e.key.toLowerCase()) {
                    case 'd': this.switchMode('D'); break;
                    case 'a': this.switchMode('A'); break;
                    case 'i': this.switchMode('I'); break;
                    case 'e': this.switchMode('E'); break;
                }
            }
        });
        
        // Add gesture confirmation for touch devices
        let touchStartTime = 0;
        document.addEventListener('touchstart', (e) => {
            touchStartTime = Date.now();
        });
        
        document.addEventListener('touchend', (e) => {
            const touchDuration = Date.now() - touchStartTime;
            if (touchDuration > 1000) { // Long press
                this.gestureConfirmed = true;
                this.showGestureConfirmation();
            }
        });
    }
    
    switchMode(mode) {
        this.currentMode = mode;
        this.showModeIndicator(mode);
        this.startListening();
    }
    
    startListening() {
        if (this.recognition && !this.isListening) {
            this.recognition.start();
            this.isListening = true;
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
        }
    }
    
    handleVoiceResult(event) {
        const result = event.results[event.results.length - 1];
        if (result.isFinal) {
            const command = result[0].transcript.toLowerCase().trim();
            this.executeVoiceCommand(command);
        }
    }
    
    executeVoiceCommand(command) {
        const modeCommands = {
            'D': {
                'navigate dashboard': () => this.navigateToDashboard(),
                'refresh all': () => this.refreshAllDashboards(),
                'export data': () => this.exportData(),
                'show status': () => this.showSystemStatus()
            },
            'A': {
                'start automation': () => this.startAutomation(),
                'stop automation': () => this.stopAutomation(),
                'schedule task': () => this.scheduleTask(),
                'configure alerts': () => this.configureAlerts()
            },
            'I': {
                'analyze data': () => this.analyzeData(),
                'generate insights': () => this.generateInsights(),
                'optimize system': () => this.optimizeSystem(),
                'enhance intelligence': () => this.enhanceIntelligence()
            },
            'E': {
                'emergency shutdown': () => this.emergencyShutdown(),
                'create backup': () => this.createBackup(),
                'send alert': () => this.sendEmergencyAlert(),
                'recover system': () => this.recoverSystem()
            }
        };
        
        const commands = modeCommands[this.currentMode];
        if (commands && commands[command]) {
            commands[command]();
            this.showCommandConfirmation(command);
        }
    }
    
    showModeIndicator(mode) {
        const indicator = document.getElementById('nexus-mode-indicator') || this.createModeIndicator();
        const modeNames = {
            'D': 'Dashboard', 'A': 'Automation', 'I': 'Intelligence', 'E': 'Emergency'
        };
        indicator.textContent = `${modeNames[mode]} Mode`;
        indicator.className = `nexus-mode-indicator mode-${mode.toLowerCase()}`;
    }
    
    createModeIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'nexus-mode-indicator';
        indicator.style.cssText = `
            position: fixed; top: 20px; left: 20px; z-index: 10000;
            background: linear-gradient(135deg, #28a745, #6f42c1);
            color: white; padding: 8px 16px; border-radius: 20px;
            font-size: 12px; font-weight: bold; opacity: 0.9;
            transition: all 0.3s ease;
        `;
        document.body.appendChild(indicator);
        return indicator;
    }
    
    showVoiceIndicator() {
        const indicator = document.getElementById('nexus-voice-indicator') || this.createVoiceIndicator();
        indicator.style.opacity = '1';
    }
    
    hideVoiceIndicator() {
        const indicator = document.getElementById('nexus-voice-indicator');
        if (indicator) indicator.style.opacity = '0.3';
    }
    
    createVoiceIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'nexus-voice-indicator';
        indicator.innerHTML = '🎤';
        indicator.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            font-size: 24px; opacity: 0.3; transition: opacity 0.3s ease;
        `;
        document.body.appendChild(indicator);
        return indicator;
    }
    
    showCommandConfirmation(command) {
        const confirmation = document.createElement('div');
        confirmation.textContent = `Executed: ${command}`;
        confirmation.style.cssText = `
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: rgba(40, 167, 69, 0.9); color: white; padding: 16px 24px;
            border-radius: 8px; font-weight: bold; z-index: 10001;
        `;
        document.body.appendChild(confirmation);
        
        setTimeout(() => {
            if (confirmation.parentNode) {
                confirmation.parentNode.removeChild(confirmation);
            }
        }, 2000);
    }
    
    showGestureConfirmation() {
        const confirmation = document.createElement('div');
        confirmation.textContent = 'Gesture Confirmed';
        confirmation.style.cssText = `
            position: fixed; bottom: 20px; right: 20px; z-index: 10000;
            background: linear-gradient(135deg, #28a745, #6f42c1);
            color: white; padding: 8px 16px; border-radius: 20px;
            font-size: 12px; font-weight: bold;
        `;
        document.body.appendChild(confirmation);
        
        setTimeout(() => {
            if (confirmation.parentNode) {
                confirmation.parentNode.removeChild(confirmation);
            }
        }, 1500);
    }
    
    // Command implementations
    navigateToDashboard() { window.location.href = '/'; }
    refreshAllDashboards() { if (window.refreshAllDashboards) window.refreshAllDashboards(); }
    exportData() { if (window.exportSystemData) window.exportSystemData(); }
    showSystemStatus() { if (window.showSystemStatus) window.showSystemStatus(); }
    startAutomation() { console.log('Starting automation...'); }
    stopAutomation() { console.log('Stopping automation...'); }
    scheduleTask() { console.log('Scheduling task...'); }
    configureAlerts() { if (window.configureAlerts) window.configureAlerts(); }
    analyzeData() { console.log('Analyzing data...'); }
    generateInsights() { if (window.generateInsights) window.generateInsights(); }
    optimizeSystem() { if (window.optimizeSystem) window.optimizeSystem(); }
    enhanceIntelligence() { console.log('Enhancing intelligence...'); }
    emergencyShutdown() { if (window.emergencyShutdown) window.emergencyShutdown(); }
    createBackup() { console.log('Creating backup...'); }
    sendEmergencyAlert() { console.log('Sending emergency alert...'); }
    recoverSystem() { console.log('Recovering system...'); }
}

// Initialize NEXUS Voice Interface
window.nexusVoiceInterface = new NEXUSVoiceInterface();
