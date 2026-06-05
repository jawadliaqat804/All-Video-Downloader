// A simple service worker to satisfy PWA requirements
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installed');
});

self.addEventListener('fetch', (event) => {
    // Allows the app to work offline basically by just passing requests through
    event.respondWith(fetch(event.request));
});