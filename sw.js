/* ================================================================
   SimuPharma Service Worker — Network-First with Cache Fallback
   ================================================================ */

const CACHE_NAME = 'simupharma-v6';
const ASSETS_TO_CACHE = [
    '/',
    '/index.html',
    '/style.css',
    '/script.js',
    '/assistant.css',
    '/assistant.js',
    '/subpage.css',
    '/subpage.js',
    '/edtech.js',
    '/curriculum.html',
    '/pricing.html',
    '/leaderboard.html',
    '/quiz.html',
    '/simupharma-logo.png'
];

// Install — cache core assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(ASSETS_TO_CACHE))
            .then(() => self.skipWaiting())
    );
});

// Activate — clean old caches immediately
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

// Fetch — NETWORK FIRST, fall back to cache
self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;

    // Skip API calls — never cache those
    if (event.request.url.includes('/api/')) return;

    // Never cache neurolab_agent — always load fresh
    if (event.request.url.includes('neurolab_agent')) return;
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Cache successful responses
                if (response.status === 200) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return response;
            })
            .catch(() => {
                // Network failed — use cache
                return caches.match(event.request).then(cached => {
                    if (cached) return cached;
                    // Offline fallback for HTML pages
                    if (event.request.headers.get('accept')?.includes('text/html')) {
                        return caches.match('/index.html');
                    }
                });
            })
    );
});
