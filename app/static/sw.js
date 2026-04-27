const CACHE_NAME = 'klinik-takip-v1';
const OFFLINE_URL = '/offline/';

const PRECACHE_URLS = [
  '/',
  '/static/manifest.json',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Sadece GET isteklerini yakala
  if (event.request.method !== 'GET') return;
  // Chrome extension ve non-http isteklerini atla
  if (!event.request.url.startsWith('http')) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Başarılı yanıtı cache'e koy (static dosyalar için)
        if (event.request.url.includes('/static/')) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Offline: cache'den dön
        return caches.match(event.request).then((cached) => {
          return cached || new Response(
            '<html><body style="font-family:sans-serif;text-align:center;padding:2rem"><h2>İnternet bağlantısı yok</h2><p>Bağlantınızı kontrol edip tekrar deneyin.</p></body></html>',
            { headers: { 'Content-Type': 'text/html' } }
          );
        });
      })
  );
});
