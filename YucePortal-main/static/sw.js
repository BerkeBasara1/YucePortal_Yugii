// static/sw.js
// Bump the version to force a fresh cache after deployments.
const CACHE_NAME = "albumler-v1-2025-10-30";

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter((k) => k.startsWith("albumler-") && k !== CACHE_NAME)
          .map((k) => caches.delete(k))
      );
      await self.clients.claim();
    })()
  );
});

// Cache-First only for /static/Albumler/*
self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle GET image requests under your album path
  const isAlbumImage =
    request.method === "GET" &&
    url.pathname.startsWith("/static/Albumler/");

  if (!isAlbumImage) return;

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(request, { ignoreVary: true });
      if (cached) return cached;

      // Fetch from network and store
      try {
        const resp = await fetch(request, { cache: "no-store" });
        if (resp && resp.ok) cache.put(request, resp.clone());
        return resp;
      } catch (err) {
        // Optionally: return a placeholder image here
        return new Response("Image fetch failed", { status: 504 });
      }
    })()
  );
});
