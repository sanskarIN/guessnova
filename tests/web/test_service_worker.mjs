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
  assert.match(source, /request\.mode === ["']navigate["']/);
  assert.match(source, /caches\.match\(["']\.\/index\.html["']\)/);
  assert.doesNotMatch(source, /\.catch\(\(\) => caches\.match\(["']\.\/index\.html["']\)\)/);
});

test("service worker ignores non-GET and cross-origin traffic", () => {
  assert.match(source, /event\.request\.method !== ["']GET["']/);
  assert.match(source, /url\.origin !== self\.location\.origin/);
});
