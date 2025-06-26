/**
 * Mobile-specific JavaScript functionality
 * Handles mobile responsive features and touch interactions
 */

class MobileManager {
    constructor() {
        this.isMobile = this.detectMobile();
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.swipeThreshold = 50;
        this.init();
    }

    init() {
        if (!this.isMobile) return;
        
        console.log('Initializing mobile features...');
        this.setupMobileNavigation();
        this.setupTouchHandlers();
        this.optimizeForMobile();
        this.setupOrientationHandling();
    }

    detectMobile() {
        return window.innerWidth <= 768 || 
               /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    setupMobileNavigation() {
        // Create mobile navigation menu
        this.createMobileMenu();
        
        // Handle mobile navigation toggle
        const mobileToggle = document.getElementById('mobile-nav-toggle');
        if (mobileToggle) {
            mobileToggle.addEventListener('click', () => {
                this.toggleMobileNav();
            });
        }

        // Close mobile nav when clicking outside
        document.addEventListener('click', (e) => {
            const mobileNav = document.getElementById('mobile-nav');
            const toggle = document.getElementById('mobile-nav-toggle');
            
            if (mobileNav && !mobileNav.contains(e.target) && !toggle.contains(e.target)) {
                this.closeMobileNav();
            }
        });
    }

    createMobileMenu() {
        const existingNav = document.querySelector('.navbar-nav');
        if (!existingNav) return;

        // Clone navigation for mobile
        const mobileNav = document.createElement('div');
        mobileNav.id = 'mobile-nav';
        mobileNav.className = 'mobile-nav d-lg-none';
        mobileNav.innerHTML = `
            <div class="mobile-nav-header">
                <h5>Nexus Dashboards</h5>
                <button type="button" class="btn-close" id="mobile-nav-close"></button>
            </div>
            <div class="mobile-nav-body">
                <div class="mobile-nav-item">
                    <a href="/" class="mobile-nav-link">
                        <i class="fas fa-home"></i> Home
                    </a>
                </div>
                <div class="mobile-nav-item">
                    <a href="/dashboard/traxovo" class="mobile-nav-link">
                        <i class="fas fa-activity"></i> TRAXOVO
                    </a>
                </div>
                <div class="mobile-nav-item">
                    <a href="/dashboard/dwc" class="mobile-nav-link">
                        <i class="fas fa-layers"></i> DWC
                    </a>
                </div>
                <div class="mobile-nav-item">
                    <a href="/dashboard/jdd" class="mobile-nav-link">
                        <i class="fas fa-database"></i> JDD
                    </a>
                </div>
                <div class="mobile-nav-item">
                    <a href="/dashboard/crypto_nexus_trade" class="mobile-nav-link">
                        <i class="fas fa-chart-line"></i> CryptoNexusTrade
                    </a>
                </div>
            </div>
            <div class="mobile-nav-footer">
                <div class="system-status-mobile">
                    <small id="mobile-system-status">System: Operational</small>
                </div>
            </div>
        `;

        document.body.appendChild(mobileNav);

        // Add close button handler
        const closeBtn = document.getElementById('mobile-nav-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.closeMobileNav();
            });
        }

        // Add CSS for mobile nav
        this.addMobileNavStyles();
    }

    addMobileNavStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .mobile-nav {
                position: fixed;
                top: 0;
                left: -100%;
                width: 280px;
                height: 100vh;
                background: var(--bs-body-bg);
                border-right: 1px solid var(--bs-border-color);
                z-index: 9999;
                transition: left 0.3s ease-in-out;
                overflow-y: auto;
            }
            
            .mobile-nav.active {
                left: 0;
            }
            
            .mobile-nav-header {
                padding: 1rem;
                border-bottom: 1px solid var(--bs-border-color);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .mobile-nav-body {
                padding: 1rem 0;
            }
            
            .mobile-nav-item {
                margin-bottom: 0.5rem;
            }
            
            .mobile-nav-link {
                display: flex;
                align-items: center;
                padding: 0.75rem 1rem;
                color: var(--bs-body-color);
                text-decoration: none;
                transition: background-color 0.2s ease;
            }
            
            .mobile-nav-link:hover {
                background-color: var(--bs-secondary-bg);
                color: var(--bs-primary);
            }
            
            .mobile-nav-link i {
                margin-right: 0.75rem;
                width: 20px;
            }
            
            .mobile-nav-footer {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 1rem;
                border-top: 1px solid var(--bs-border-color);
                background: var(--bs-body-bg);
            }
            
            .mobile-nav-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 9998;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .mobile-nav-overlay.active {
                opacity: 1;
                visibility: visible;
            }
            
            .touch-active {
                transform: scale(0.98);
                transition: transform 0.1s ease;
            }
        `;
        document.head.appendChild(style);
    }

    toggleMobileNav() {
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav) {
            if (mobileNav.classList.contains('active')) {
                this.closeMobileNav();
            } else {
                this.openMobileNav();
            }
        }
    }

    openMobileNav() {
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav) {
            mobileNav.classList.add('active');
            
            // Create overlay
            const overlay = document.createElement('div');
            overlay.className = 'mobile-nav-overlay active';
            overlay.addEventListener('click', () => {
                this.closeMobileNav();
            });
            document.body.appendChild(overlay);
            
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }
    }

    closeMobileNav() {
        const mobileNav = document.getElementById('mobile-nav');
        const overlay = document.querySelector('.mobile-nav-overlay');
        
        if (mobileNav) {
            mobileNav.classList.remove('active');
        }
        
        if (overlay) {
            overlay.remove();
        }
        
        // Restore body scroll
        document.body.style.overflow = '';
    }

    setupTouchHandlers() {
        // Swipe gestures for dashboard navigation
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            if (!this.touchStartX || !this.touchStartY) return;

            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const deltaX = touchEndX - this.touchStartX;
            const deltaY = touchEndY - this.touchStartY;
            
            // Check if it's a horizontal swipe
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > this.swipeThreshold) {
                if (deltaX > 0) {
                    this.handleSwipeRight();
                } else {
                    this.handleSwipeLeft();
                }
            }
            
            this.touchStartX = 0;
            this.touchStartY = 0;
        }, { passive: true });

        // Touch feedback for interactive elements
        document.addEventListener('touchstart', (e) => {
            const target = e.target.closest('.dashboard-card, .btn, .nav-link');
            if (target) {
                target.classList.add('touch-active');
            }
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            const target = e.target.closest('.dashboard-card, .btn, .nav-link');
            if (target) {
                setTimeout(() => {
                    target.classList.remove('touch-active');
                }, 150);
            }
        }, { passive: true });
    }

    handleSwipeRight() {
        // Open mobile nav on right swipe from left edge
        if (this.touchStartX < 50) {
            this.openMobileNav();
        }
    }

    handleSwipeLeft() {
        // Close mobile nav on left swipe
        const mobileNav = document.getElementById('mobile-nav');
        if (mobileNav && mobileNav.classList.contains('active')) {
            this.closeMobileNav();
        }
    }

    optimizeForMobile() {
        // Add mobile-specific classes
        document.body.classList.add('mobile-optimized');
        
        // Optimize dashboard grid
        const dashboardGrid = document.querySelector('.dashboard-grid');
        if (dashboardGrid) {
            dashboardGrid.style.gridTemplateColumns = '1fr';
            dashboardGrid.style.gap = '1rem';
        }

        // Optimize metric cards
        const metricCards = document.querySelectorAll('.metric-card');
        metricCards.forEach(card => {
            card.style.padding = '1rem';
            card.style.marginBottom = '0.5rem';
        });

        // Optimize navbar
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            navbar.classList.add('mobile-navbar');
        }

        // Add mobile toggle button if not exists
        this.addMobileToggleButton();
    }

    addMobileToggleButton() {
        const navbar = document.querySelector('.navbar');
        if (!navbar || document.getElementById('mobile-nav-toggle')) return;

        const toggleButton = document.createElement('button');
        toggleButton.id = 'mobile-nav-toggle';
        toggleButton.className = 'btn btn-outline-primary d-lg-none';
        toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
        toggleButton.style.marginLeft = 'auto';

        const navbarBrand = navbar.querySelector('.navbar-brand');
        if (navbarBrand) {
            navbarBrand.parentNode.insertBefore(toggleButton, navbarBrand.nextSibling);
        }
    }

    setupOrientationHandling() {
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleOrientationChange();
            }, 100);
        });
    }

    handleOrientationChange() {
        // Recalculate layout after orientation change
        this.optimizeForMobile();
        
        // Close mobile nav if open
        this.closeMobileNav();
        
        // Trigger resize event
        window.dispatchEvent(new Event('resize'));
    }

    // Mobile-specific dashboard features
    enablePullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pullDistance = 0;
        const threshold = 100;
        
        document.addEventListener('touchstart', (e) => {
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
            }
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            if (startY > 0) {
                currentY = e.touches[0].clientY;
                pullDistance = currentY - startY;
                
                if (pullDistance > 0 && pullDistance < threshold) {
                    // Visual feedback for pull to refresh
                    this.showPullToRefreshIndicator(pullDistance / threshold);
                }
            }
        }, { passive: true });
        
        document.addEventListener('touchend', () => {
            if (pullDistance >= threshold) {
                this.triggerRefresh();
            }
            
            startY = 0;
            currentY = 0;
            pullDistance = 0;
            this.hidePullToRefreshIndicator();
        }, { passive: true });
    }

    showPullToRefreshIndicator(progress) {
        let indicator = document.getElementById('pull-to-refresh-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'pull-to-refresh-indicator';
            indicator.innerHTML = '<i class="fas fa-sync-alt"></i>';
            indicator.style.cssText = `
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: var(--bs-primary);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 2rem;
                z-index: 1000;
                transition: opacity 0.2s ease;
            `;
            document.body.appendChild(indicator);
        }
        
        indicator.style.opacity = progress;
        indicator.style.transform = `translateX(-50%) rotate(${progress * 360}deg)`;
    }

    hidePullToRefreshIndicator() {
        const indicator = document.getElementById('pull-to-refresh-indicator');
        if (indicator) {
            indicator.style.opacity = '0';
            setTimeout(() => {
                if (indicator.parentNode) {
                    indicator.parentNode.removeChild(indicator);
                }
            }, 200);
        }
    }

    triggerRefresh() {
        // Trigger page refresh or dashboard reload
        if (window.dashboardManager) {
            window.dashboardManager.refreshDashboard();
        } else {
            window.location.reload();
        }
    }

    // Haptic feedback (if supported)
    vibrate(pattern = [100]) {
        if ('vibrate' in navigator) {
            navigator.vibrate(pattern);
        }
    }

    // Mobile-specific error handling
    showMobileError(message) {
        const errorToast = document.createElement('div');
        errorToast.className = 'mobile-error-toast';
        errorToast.textContent = message;
        errorToast.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: var(--bs-danger);
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            z-index: 9999;
            animation: slideUp 0.3s ease;
        `;
        
        document.body.appendChild(errorToast);
        
        setTimeout(() => {
            errorToast.style.animation = 'slideDown 0.3s ease forwards';
            setTimeout(() => {
                if (errorToast.parentNode) {
                    errorToast.parentNode.removeChild(errorToast);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize mobile manager
document.addEventListener('DOMContentLoaded', () => {
    window.mobileManager = new MobileManager();
    
    // Enable pull to refresh if on mobile
    if (window.mobileManager.isMobile) {
        window.mobileManager.enablePullToRefresh();
    }
});

// Add CSS animations
const mobileAnimations = document.createElement('style');
mobileAnimations.textContent = `
    @keyframes slideUp {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideDown {
        from { transform: translateY(0); opacity: 1; }
        to { transform: translateY(100%); opacity: 0; }
    }
`;
document.head.appendChild(mobileAnimations);
