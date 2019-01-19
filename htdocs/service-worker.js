/**
 * SPA Base Service Worker
 */

importScripts('https://cdn.onesignal.com/sdks/OneSignalSDKWorker.js');

var version = 0.1;

// Offline cache name
var cache_name = 'spa_base-' + version;

self.addEventListener('install', function(event) {
    event.waitUntil(
        // Offline Caching
        caches.open(cache_name).then(function(cache) {
            return cache.addAll([
                '/',
                '/css/app.css',
                '/css/auth.css',
                '/icons/logo-32x32.png',
                '/icons/zondicons.svg',
                '/js/show-password.js',
                '/login/',
                '/manifest.webmanifest',
                '/service-worker.js',
                'https://fonts.googleapis.com/css?family=Libre+Franklin:400,400i,700',
                'https://fonts.googleapis.com/css?family=Libre+Baskerville:400,400i,700',
            ])
            .then(function() { self.skipWaiting(); });
        })
    );
});


self.addEventListener('activate', function(event) {
    return event.waitUntil(self.clients.claim());
});


self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.open(cache_name)
            .then(function(cache) { return cache.match(event.request, {ignoreSearch: true}); })
            .then(function(response) {
                return response || fetch(event.request);
            })
    );
});
