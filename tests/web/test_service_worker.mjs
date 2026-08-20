import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(
  new URL("../../src/guessnova/web/sw.js", import.meta.url),
  "utf8",
);

test("service worker precaches all JavaScript modules", () => {
  assert.match(source, /\.\/app\.js/);
  assert.match(source, /\.\/browser-state\.mjs/);
  assert.match(source, /\.\/game-engine\.mjs/);
});

test("offline HTML fallback is limited to navigations", () => {
  assert.match(source, /request\.mode\s*===\s*["']navigate["']/);
  assert.match(source, /safeCacheMatch\(\s*["']\.\/index\.html["']\s*\)/);
  assert.doesNotMatch(
    source,
    /\.catch\(\s*\(\)\s*=>\s*caches\.match\(\s*["']\.\/index\.html["']\s*\)\s*\)/,
  );
});

test("cache storage failures are isolated from network responses", () => {
  assert.match(source, /async function safeCacheMatch\(/);
  assert.match(source, /return await caches\.match\(request\)/);
  assert.match(source, /async function cacheSuccessfulResponse\(/);
  assert.match(source, /await cache\.put\(request, response\.clone\(\)\)/);
  assert.match(
    source,
    /catch\s*\{\s*\/\/ Cache Storage can be blocked or full;/,
  );
});

test("service worker ignores non-GET and cross-origin traffic", () => {
  assert.match(source, /event\.request\.method\s*!==\s*["']GET["']/);
  assert.match(source, /url\.origin\s*!==\s*self\.location\.origin/);
});
