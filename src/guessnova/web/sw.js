const CACHE_NAME = "guessnova-web-v4";
const APP_SHELL = [
  "./",
  "./index.html",
  "./app.css",
  "./app.js",
  "./browser-state.mjs",
  "./game-engine.mjs",
  "./manifest.webmanifest",
  "./icon.svg",
  "./icon-192.png",
  "./icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

async function safeCacheMatch(request) {
  try {
    return await caches.match(request);
  } catch {
    return undefined;
  }
}

async function cacheSuccessfulResponse(request, response) {
  if (!response || response.status !== 200 || response.type === "opaque") return;
  try {
    const cache = await caches.open(CACHE_NAME);
    await cache.put(request, response.clone());
  } catch {
    // Cache Storage can be blocked or full; a successful network response still wins.
  }
}

async function respondToRequest(request) {
  const cached = await safeCacheMatch(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    await cacheSuccessfulResponse(request, response);
    return response;
  } catch (error) {
    if (request.mode === "navigate") {
      const fallback = await safeCacheMatch("./index.html");
      if (fallback) return fallback;
    }
    throw error;
  }
}

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(respondToRequest(event.request));
});
