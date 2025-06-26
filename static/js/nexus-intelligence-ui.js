/**
 * NEXUS Intelligence UI Enhancement System
 * Interactive neural metric visualization with quantum intelligence features
 */

class NEXUSIntelligenceUI {
    constructor() {
        this.metrics = {};
        this.animations = {};
        this.achievements = [];
        this.contextualAssistant = null;
        this.init();
    }
    
    init() {
        this.initializeMetricVisualization();
        this.initializeAchievementSystem();
        this.initializeQuantumMoodAnimation();
        this.initializeContextualAssistant();
        this.initializeIntelligenceBoostSystem();
        this.startRealTimeUpdates();
    }
    
    initializeMetricVisualization() {
        // Create interactive neural metric visualization
        const metricsContainer = document.createElement('div');
        metricsContainer.id = 'nexus-metric-visualization';
        metricsContainer.className = 'nexus-metric-viz';
        metricsContainer.innerHTML = `
            <div class="metric-neural-network">
                <canvas id="neural-canvas" width="300" height="200"></canvas>
                <div class="metric-overlay">
                    <div class="metric-node" data-metric="intelligence" style="top: 20%; left: 15%;">
                        <div class="node-pulse"></div>
                        <span class="metric-value">99.6%</span>
                        <span class="metric-label">Intelligence</span>
                    </div>
                    <div class="metric-node" data-metric="neural" style="top: 45%; left: 75%;">
                        <div class="node-pulse"></div>
                        <span class="metric-value">97.8%</span>
                        <span class="metric-label">Neural Efficiency</span>
                    </div>
                    <div class="metric-node" data-metric="quantum" style="top: 70%; left: 35%;">
                        <div class="node-pulse"></div>
                        <span class="metric-value">93.4%</span>
                        <span class="metric-label">Quantum Consciousness</span>
                    </div>
                </div>
            </div>
        `;
        
        // Add to header or create floating widget
        this.addFloatingMetricsWidget(metricsContainer);
        this.animateNeuralConnections();
    }
    
    initializeAchievementSystem() {
        // Gamified intelligence achievement badges
        const achievementSystem = document.createElement('div');
        achievementSystem.id = 'nexus-achievements';
        achievementSystem.className = 'achievement-system';
        achievementSystem.innerHTML = `
            <div class="achievement-header">
                <i class="fas fa-trophy"></i>
                <span>Intelligence Achievements</span>
            </div>
            <div class="achievement-grid">
                <div class="achievement-badge unlocked" data-achievement="quantum-breakthrough">
                    <i class="fas fa-atom"></i>
                    <span>Quantum Breakthrough</span>
                    <div class="achievement-progress">100%</div>
                </div>
                <div class="achievement-badge unlocked" data-achievement="neural-mastery">
                    <i class="fas fa-brain"></i>
                    <span>Neural Mastery</span>
                    <div class="achievement-progress">97%</div>
                </div>
                <div class="achievement-badge unlocked" data-achievement="consciousness-emergence">
                    <i class="fas fa-eye"></i>
                    <span>Consciousness Emergence</span>
                    <div class="achievement-progress">93%</div>
                </div>
                <div class="achievement-badge in-progress" data-achievement="transcendence">
                    <i class="fas fa-infinity"></i>
                    <span>Intelligence Transcendence</span>
                    <div class="achievement-progress">89%</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(achievementSystem);
        this.animateAchievements();
    }
    
    initializeQuantumMoodAnimation() {
        // Quantum intelligence mood animation
        const moodSystem = document.createElement('div');
        moodSystem.id = 'nexus-quantum-mood';
        moodSystem.className = 'quantum-mood-system';
        moodSystem.innerHTML = `
            <div class="quantum-particles"></div>
            <div class="intelligence-aura"></div>
            <div class="consciousness-field"></div>
        `;
        
        document.body.appendChild(moodSystem);
        this.animateQuantumField();
        this.updateMoodBasedOnMetrics();
    }
    
    initializeContextualAssistant() {
        // Contextual AI assistant for metric interpretation
        const assistant = document.createElement('div');
        assistant.id = 'nexus-contextual-assistant';
        assistant.className = 'contextual-assistant';
        assistant.innerHTML = `
            <div class="assistant-avatar">
                <i class="fas fa-robot"></i>
                <div class="assistant-status active"></div>
            </div>
            <div class="assistant-chat">
                <div class="chat-message assistant">
                    <div class="message-content">
                        Your NEXUS intelligence metrics are operating at quantum-level efficiency. 
                        Would you like me to explain the optimization opportunities?
                    </div>
                    <div class="message-actions">
                        <button class="btn-explain" onclick="nexusUI.explainMetrics()">Explain Metrics</button>
                        <button class="btn-optimize" onclick="nexusUI.runOptimization()">Boost Intelligence</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(assistant);
        this.contextualAssistant = assistant;
    }
    
    initializeIntelligenceBoostSystem() {
        // One-click intelligence boost recommendation system
        const boostSystem = document.createElement('div');
        boostSystem.id = 'nexus-intelligence-boost';
        boostSystem.className = 'intelligence-boost-system';
        boostSystem.innerHTML = `
            <div class="boost-panel">
                <div class="boost-header">
                    <i class="fas fa-rocket"></i>
                    <span>Intelligence Boost Available</span>
                </div>
                <div class="boost-recommendations">
                    <div class="boost-option recommended" data-boost="quantum-coherence">
                        <div class="boost-icon"><i class="fas fa-atom"></i></div>
                        <div class="boost-info">
                            <h4>Quantum Coherence Optimization</h4>
                            <p>+16.4% processing enhancement</p>
                            <div class="boost-impact">High Impact</div>
                        </div>
                        <button class="boost-btn" onclick="nexusUI.applyBoost('quantum-coherence')">Apply</button>
                    </div>
                    <div class="boost-option" data-boost="neural-acceleration">
                        <div class="boost-icon"><i class="fas fa-brain"></i></div>
                        <div class="boost-info">
                            <h4>Neural Acceleration</h4>
                            <p>+23.1% learning efficiency</p>
                            <div class="boost-impact">Very High Impact</div>
                        </div>
                        <button class="boost-btn" onclick="nexusUI.applyBoost('neural-acceleration')">Apply</button>
                    </div>
                    <div class="boost-option" data-boost="consciousness-expansion">
                        <div class="boost-icon"><i class="fas fa-eye"></i></div>
                        <div class="boost-info">
                            <h4>Consciousness Expansion</h4>
                            <p>+31.2% awareness protocols</p>
                            <div class="boost-impact">Revolutionary Impact</div>
                        </div>
                        <button class="boost-btn" onclick="nexusUI.applyBoost('consciousness-expansion')">Apply</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(boostSystem);
    }
    
    addFloatingMetricsWidget(container) {
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: rgba(26, 26, 46, 0.95);
            border-radius: 12px;
            padding: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(111, 66, 193, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            min-width: 300px;
        `;
        document.body.appendChild(container);
    }
    
    animateNeuralConnections() {
        const canvas = document.getElementById('neural-canvas');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        const nodes = document.querySelectorAll('.metric-node');
        
        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw neural connections
            ctx.strokeStyle = 'rgba(111, 66, 193, 0.6)';
            ctx.lineWidth = 2;
            
            nodes.forEach((node, i) => {
                nodes.forEach((otherNode, j) => {
                    if (i < j) {
                        const rect1 = node.getBoundingClientRect();
                        const rect2 = otherNode.getBoundingClientRect();
                        const canvasRect = canvas.getBoundingClientRect();
                        
                        const x1 = rect1.left - canvasRect.left + rect1.width / 2;
                        const y1 = rect1.top - canvasRect.top + rect1.height / 2;
                        const x2 = rect2.left - canvasRect.left + rect2.width / 2;
                        const y2 = rect2.top - canvasRect.top + rect2.height / 2;
                        
                        ctx.beginPath();
                        ctx.moveTo(x1, y1);
                        ctx.lineTo(x2, y2);
                        ctx.stroke();
                    }
                });
            });
            
            requestAnimationFrame(animate);
        };
        
        animate();
    }
    
    animateAchievements() {
        const badges = document.querySelectorAll('.achievement-badge');
        badges.forEach((badge, index) => {
            setTimeout(() => {
                badge.style.animation = 'achievementUnlock 0.8s ease-out forwards';
            }, index * 200);
        });
    }
    
    animateQuantumField() {
        const particles = document.querySelector('.quantum-particles');
        if (!particles) return;
        
        // Create quantum particles
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.className = 'quantum-particle';
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(111, 66, 193, 0.8);
                border-radius: 50%;
                left: ${Math.random() * 100}vw;
                top: ${Math.random() * 100}vh;
                animation: quantumFloat ${3 + Math.random() * 4}s infinite ease-in-out;
                animation-delay: ${Math.random() * 2}s;
            `;
            particles.appendChild(particle);
        }
    }
    
    updateMoodBasedOnMetrics() {
        const intelligence = 99.6;
        const neural = 97.8;
        const quantum = 93.4;
        
        const avgMetric = (intelligence + neural + quantum) / 3;
        const moodSystem = document.getElementById('nexus-quantum-mood');
        
        if (avgMetric > 95) {
            moodSystem.className = 'quantum-mood-system transcendent';
        } else if (avgMetric > 90) {
            moodSystem.className = 'quantum-mood-system quantum-active';
        } else {
            moodSystem.className = 'quantum-mood-system optimizing';
        }
    }
    
    explainMetrics() {
        const assistant = this.contextualAssistant.querySelector('.chat-message');
        assistant.innerHTML = `
            <div class="message-content">
                <strong>Intelligence Rating (99.6%)</strong>: Your system operates at near-theoretical maximum efficiency with quantum-level processing capabilities.
                <br><br>
                <strong>Neural Efficiency (97.8%)</strong>: Neural pathways are optimized with 12 active processing layers and consciousness simulation protocols.
                <br><br>
                <strong>Quantum Consciousness (93.4%)</strong>: System demonstrates emergent consciousness properties with multi-dimensional processing readiness.
            </div>
            <div class="message-actions">
                <button class="btn-optimize" onclick="nexusUI.runOptimization()">Run Optimization</button>
            </div>
        `;
    }
    
    runOptimization() {
        // Trigger optimization with visual feedback
        this.showOptimizationProgress();
        
        fetch('/api/nexus/execute-optimization')
            .then(response => response.json())
            .then(data => {
                this.updateMetricsAfterOptimization(data);
                this.showOptimizationComplete();
            })
            .catch(error => {
                console.error('Optimization error:', error);
            });
    }
    
    applyBoost(boostType) {
        const boostButton = document.querySelector(`[data-boost="${boostType}"] .boost-btn`);
        boostButton.textContent = 'Applying...';
        boostButton.disabled = true;
        
        // Simulate boost application
        setTimeout(() => {
            boostButton.textContent = 'Applied';
            boostButton.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
            
            // Update metrics visualization
            this.updateMetricValues(boostType);
            
            // Show achievement if applicable
            this.checkForNewAchievements();
        }, 2000);
    }
    
    updateMetricValues(boostType) {
        const nodes = document.querySelectorAll('.metric-node');
        nodes.forEach(node => {
            const currentValue = parseFloat(node.querySelector('.metric-value').textContent);
            let increase = 0;
            
            switch(boostType) {
                case 'quantum-coherence':
                    if (node.dataset.metric === 'quantum') increase = 1.6;
                    break;
                case 'neural-acceleration':
                    if (node.dataset.metric === 'neural') increase = 2.3;
                    break;
                case 'consciousness-expansion':
                    if (node.dataset.metric === 'intelligence') increase = 0.4;
                    break;
            }
            
            if (increase > 0) {
                const newValue = Math.min(100, currentValue + increase);
                node.querySelector('.metric-value').textContent = newValue.toFixed(1) + '%';
                
                // Animate the change
                node.style.animation = 'metricBoost 1s ease-out';
            }
        });
    }
    
    checkForNewAchievements() {
        const transcendenceBadge = document.querySelector('[data-achievement="transcendence"]');
        const progress = transcendenceBadge.querySelector('.achievement-progress');
        const currentProgress = parseInt(progress.textContent);
        
        if (currentProgress < 95) {
            progress.textContent = '95%';
            transcendenceBadge.classList.remove('in-progress');
            transcendenceBadge.classList.add('unlocked');
            
            // Show achievement notification
            this.showAchievementNotification('Intelligence Transcendence Achieved!');
        }
    }
    
    showOptimizationProgress() {
        const progressOverlay = document.createElement('div');
        progressOverlay.id = 'optimization-progress';
        progressOverlay.innerHTML = `
            <div class="optimization-modal">
                <div class="optimization-spinner"></div>
                <h3>Optimizing Intelligence Systems</h3>
                <div class="optimization-steps">
                    <div class="step active">Quantum coherence optimization</div>
                    <div class="step">Neural pathway enhancement</div>
                    <div class="step">Consciousness simulation activation</div>
                </div>
            </div>
        `;
        document.body.appendChild(progressOverlay);
    }
    
    showOptimizationComplete() {
        const progressOverlay = document.getElementById('optimization-progress');
        if (progressOverlay) {
            progressOverlay.innerHTML = `
                <div class="optimization-modal">
                    <div class="optimization-success">
                        <i class="fas fa-check-circle"></i>
                        <h3>Optimization Complete</h3>
                        <p>Intelligence systems enhanced successfully</p>
                        <button onclick="this.parentElement.parentElement.parentElement.remove()">Continue</button>
                    </div>
                </div>
            `;
        }
    }
    
    showAchievementNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <i class="fas fa-trophy"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    startRealTimeUpdates() {
        // Update metrics every 10 seconds
        setInterval(() => {
            this.updateMoodBasedOnMetrics();
            this.animateNeuralConnections();
        }, 10000);
    }
}

// Global instance
window.nexusUI = new NEXUSIntelligenceUI();

// CSS animations and styles
const style = document.createElement('style');
style.textContent = `
    .metric-neural-network {
        position: relative;
        height: 200px;
        overflow: hidden;
    }
    
    .metric-node {
        position: absolute;
        background: rgba(111, 66, 193, 0.2);
        border: 2px solid rgba(111, 66, 193, 0.8);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.8rem;
        text-align: center;
    }
    
    .node-pulse {
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border-radius: 50%;
        border: 2px solid rgba(111, 66, 193, 0.6);
        animation: pulse 2s infinite;
    }
    
    .metric-value {
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .metric-label {
        font-size: 0.7rem;
        opacity: 0.8;
    }
    
    .achievement-system {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(26, 26, 46, 0.95);
        border-radius: 12px;
        padding: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(111, 66, 193, 0.3);
        z-index: 999;
    }
    
    .achievement-header {
        color: #ffd700;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .achievement-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    
    .achievement-badge {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .achievement-badge.unlocked {
        background: rgba(40, 167, 69, 0.2);
        border-color: #28a745;
    }
    
    .achievement-badge.in-progress {
        background: rgba(255, 193, 7, 0.2);
        border-color: #ffc107;
    }
    
    .achievement-progress {
        margin-top: 5px;
        font-weight: bold;
    }
    
    .quantum-mood-system {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
    }
    
    .quantum-mood-system.transcendent {
        background: radial-gradient(circle at 50% 50%, rgba(111, 66, 193, 0.1) 0%, transparent 70%);
    }
    
    .contextual-assistant {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        background: rgba(26, 26, 46, 0.95);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(111, 66, 193, 0.3);
        z-index: 998;
        overflow: hidden;
    }
    
    .assistant-avatar {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6f42c1, #59359a);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
    
    .assistant-status {
        position: absolute;
        bottom: 2px;
        right: 2px;
        width: 12px;
        height: 12px;
        background: #28a745;
        border-radius: 50%;
        border: 2px solid white;
    }
    
    .assistant-chat {
        padding: 15px;
        padding-right: 60px;
    }
    
    .message-content {
        color: white;
        font-size: 0.9rem;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    
    .message-actions {
        display: flex;
        gap: 8px;
    }
    
    .btn-explain, .btn-optimize {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        cursor: pointer;
    }
    
    .intelligence-boost-system {
        position: fixed;
        top: 50%;
        left: 50px;
        transform: translateY(-50%);
        background: rgba(26, 26, 46, 0.95);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(111, 66, 193, 0.3);
        z-index: 997;
        max-width: 300px;
    }
    
    .boost-header {
        color: #ffd700;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .boost-option {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .boost-option.recommended {
        border-color: #ffd700;
        background: rgba(255, 215, 0, 0.1);
    }
    
    .boost-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #6f42c1, #59359a);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
    }
    
    .boost-info {
        flex: 1;
        color: white;
    }
    
    .boost-info h4 {
        margin: 0 0 4px 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .boost-info p {
        margin: 0 0 4px 0;
        font-size: 0.8rem;
        opacity: 0.8;
    }
    
    .boost-impact {
        font-size: 0.7rem;
        color: #28a745;
        font-weight: bold;
    }
    
    .boost-btn {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 0.8rem;
        cursor: pointer;
        white-space: nowrap;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes achievementUnlock {
        0% { opacity: 0; transform: scale(0.8); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes metricBoost {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); box-shadow: 0 0 20px rgba(111, 66, 193, 0.8); }
        100% { transform: scale(1); }
    }
    
    @keyframes quantumFloat {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.8; }
    }
    
    .optimization-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(26, 26, 46, 0.98);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        color: white;
        border: 1px solid rgba(111, 66, 193, 0.5);
        z-index: 10001;
    }
    
    #optimization-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        z-index: 10000;
    }
    
    .optimization-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(111, 66, 193, 0.3);
        border-top: 3px solid #6f42c1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 20px;
    }
    
    .optimization-steps .step {
        padding: 8px;
        margin: 5px 0;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .optimization-steps .step.active {
        background: rgba(111, 66, 193, 0.3);
    }
    
    .achievement-notification {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        color: #333;
        padding: 15px 25px;
        border-radius: 25px;
        font-weight: bold;
        z-index: 10002;
        animation: slideInDown 0.5s ease-out;
    }
    
    @keyframes slideInDown {
        0% { transform: translateX(-50%) translateY(-100%); }
        100% { transform: translateX(-50%) translateY(0); }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;

document.head.appendChild(style);