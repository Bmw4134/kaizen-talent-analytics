/**
 * NEXUS Enterprise Service Worker
 * Offline Field Operations & Performance Optimization
 */

const CACHE_NAME = 'nexus-enterprise-v2.0.0';
const CACHE_CRITICAL = 'nexus-critical-v2.0.0';

// Critical resources for offline operation
const CRITICAL_RESOURCES = [
    '/',
    '/static/css/enterprise-unified.css',
    '/static/js/enterprise-deployment.js',
    '/api/system/status',
    '/login'
];

// Cache strategy for different resource types
const CACHE_STRATEGIES = {
    html: 'network-first',
    css: 'cache-first',
    js: 'cache-first',
    api: 'network-first',
    images: 'cache-first'
};

// Install event - cache critical resources
self.addEventListener('install', event => {
    event.waitUntil(
        Promise.all([
            caches.open(CACHE_CRITICAL).then(cache => {
                return cache.addAll(CRITICAL_RESOURCES);
            }),
            caches.open(CACHE_NAME).then(cache => {
                return cache.addAll([
                    '/static/css/enterprise-unified.css',
                    '/static/js/enterprise-deployment.js'
                ]);
            })
        ]).then(() => {
            self.skipWaiting();
        })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME && cacheName !== CACHE_CRITICAL) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            self.clients.claim();
        })
    );
});

// Fetch event - implement cache strategies
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Determine resource type and strategy
    const resourceType = getResourceType(url.pathname);
    const strategy = CACHE_STRATEGIES[resourceType] || 'network-first';
    
    event.respondWith(
        executeStrategy(strategy, request)
    );
});

// Determine resource type from URL
function getResourceType(pathname) {
    if (pathname.startsWith('/api/')) return 'api';
    if (pathname.endsWith('.html') || pathname === '/') return 'html';
    if (pathname.endsWith('.css')) return 'css';
    if (pathname.endsWith('.js')) return 'js';
    if (pathname.match(/\.(png|jpg|jpeg|gif|svg|webp)$/)) return 'images';
    return 'html';
}

// Execute caching strategy
async function executeStrategy(strategy, request) {
    switch (strategy) {
        case 'cache-first':
            return cacheFirst(request);
        case 'network-first':
            return networkFirst(request);
        case 'cache-only':
            return cacheOnly(request);
        case 'network-only':
            return networkOnly(request);
        default:
            return networkFirst(request);
    }
}

// Cache-first strategy
async function cacheFirst(request) {
    const cached = await caches.match(request);
    if (cached) {
        return cached;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        return new Response('Offline - Resource not available', {
            status: 503,
            statusText: 'Service Unavailable'
        });
    }
}

// Network-first strategy
async function networkFirst(request) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cached = await caches.match(request);
        if (cached) {
            return cached;
        }
        
        // Return offline fallback for API requests
        if (request.url.includes('/api/')) {
            return new Response(JSON.stringify({
                status: 'offline',
                message: 'Operating in offline mode',
                timestamp: new Date().toISOString()
            }), {
                headers: { 'Content-Type': 'application/json' },
                status: 200
            });
        }
        
        // Return offline page for HTML requests
        return new Response(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>NEXUS - Offline Mode</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: 'Inter', sans-serif;
                        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                        color: white;
                        margin: 0;
                        padding: 2rem;
                        text-align: center;
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        flex-direction: column;
                    }
                    .offline-icon {
                        font-size: 4rem;
                        margin-bottom: 1rem;
                    }
                    .offline-title {
                        font-size: 2rem;
                        font-weight: 700;
                        margin-bottom: 1rem;
                    }
                    .offline-message {
                        font-size: 1.125rem;
                        opacity: 0.9;
                        max-width: 600px;
                    }
                    .retry-btn {
                        background: white;
                        color: #007bff;
                        border: none;
                        padding: 1rem 2rem;
                        border-radius: 8px;
                        font-weight: 600;
                        margin-top: 2rem;
                        cursor: pointer;
                        font-size: 1rem;
                    }
                </style>
            </head>
            <body>
                <div class="offline-icon">📡</div>
                <div class="offline-title">NEXUS Enterprise - Offline Mode</div>
                <div class="offline-message">
                    You're currently offline. The NEXUS platform is designed for field operations
                    and will automatically sync when connection is restored.
                </div>
                <button class="retry-btn" onclick="window.location.reload()">
                    Retry Connection
                </button>
            </body>
            </html>
        `, {
            headers: { 'Content-Type': 'text/html' },
            status: 200
        });
    }
}

// Cache-only strategy
async function cacheOnly(request) {
    return caches.match(request);
}

// Network-only strategy
async function networkOnly(request) {
    return fetch(request);
}

// Background sync for offline data
self.addEventListener('sync', event => {
    if (event.tag === 'nexus-sync') {
        event.waitUntil(syncOfflineData());
    }
});

// Sync offline data when connection restored
async function syncOfflineData() {
    try {
        // Get pending offline data
        const db = await openIndexedDB();
        const pendingData = await getPendingData(db);
        
        // Sync each pending item
        for (const item of pendingData) {
            await syncDataItem(item);
        }
        
        // Clear synced data
        await clearPendingData(db);
        
        // Notify client of successful sync
        self.clients.matchAll().then(clients => {
            clients.forEach(client => {
                client.postMessage({
                    type: 'sync-complete',
                    message: 'All offline data synchronized'
                });
            });
        });
    } catch (error) {
        console.error('Sync failed:', error);
    }
}

// IndexedDB operations for offline data
function openIndexedDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('nexus-offline-db', 1);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        
        request.onupgradeneeded = event => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('pending-data')) {
                db.createObjectStore('pending-data', { autoIncrement: true });
            }
        };
    });
}

function getPendingData(db) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pending-data'], 'readonly');
        const store = transaction.objectStore('pending-data');
        const request = store.getAll();
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
    });
}

function clearPendingData(db) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pending-data'], 'readwrite');
        const store = transaction.objectStore('pending-data');
        const request = store.clear();
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve();
    });
}

async function syncDataItem(item) {
    try {
        const response = await fetch(item.url, {
            method: item.method,
            headers: item.headers,
            body: item.body
        });
        
        if (!response.ok) {
            throw new Error(`Sync failed: ${response.status}`);
        }
        
        return response;
    } catch (error) {
        console.error('Failed to sync item:', error);
        throw error;
    }
}

// Push notifications for system alerts
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/static/icons/nexus-icon-192.png',
            badge: '/static/icons/nexus-badge-72.png',
            tag: 'nexus-notification',
            requireInteraction: data.urgent || false,
            actions: [
                {
                    action: 'view',
                    title: 'View Dashboard'
                },
                {
                    action: 'dismiss',
                    title: 'Dismiss'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'view') {
        event.waitUntil(
            self.clients.openWindow('/')
        );
    }
});

// Message handling from main thread
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Performance monitoring
self.addEventListener('fetch', event => {
    const startTime = Date.now();
    
    event.respondWith(
        executeStrategy(getResourceType(new URL(event.request.url).pathname), event.request)
            .then(response => {
                const endTime = Date.now();
                const duration = endTime - startTime;
                
                // Log performance metrics
                console.log(`SW: ${event.request.url} - ${duration}ms`);
                
                return response;
            })
    );
});