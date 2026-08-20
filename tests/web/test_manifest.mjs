import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const webRoot = new URL("../../src/guessnova/web/", import.meta.url);
const manifest = JSON.parse(await readFile(new URL("manifest.webmanifest", webRoot), "utf8"));
const html = await readFile(new URL("index.html", webRoot), "utf8");
const serviceWorker = await readFile(new URL("sw.js", webRoot), "utf8");

function pngDimensions(buffer) {
  const signature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  assert.deepEqual(buffer.subarray(0, 8), signature);
  return {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20),
  };
}

test("manifest uses a scoped standalone app identity", () => {
  assert.equal(manifest.name, "GuessNova");
  assert.equal(manifest.short_name, "GuessNova");
  assert.equal(manifest.id, "./");
  assert.equal(manifest.start_url, "./");
  assert.equal(manifest.scope, "./");
  assert.equal(manifest.display, "standalone");
  assert.equal(manifest.lang, "en");
});

test("manifest declares real 192px and 512px PNG icons", async () => {
  const expected = new Map([
    ["./icon-192.png", 192],
    ["./icon-512.png", 512],
  ]);

  assert.equal(manifest.icons.length, expected.size);
  for (const icon of manifest.icons) {
    const dimension = expected.get(icon.src);
    assert.ok(dimension, `unexpected icon: ${icon.src}`);
    assert.equal(icon.sizes, `${dimension}x${dimension}`);
    assert.equal(icon.type, "image/png");

    const bytes = await readFile(new URL(icon.src.replace("./", ""), webRoot));
    assert.deepEqual(pngDimensions(bytes), { width: dimension, height: dimension });
  }
});

test("HTML and offline shell reference installability assets", () => {
  assert.match(html, /rel="manifest" href="\.\/manifest\.webmanifest"/);
  assert.match(html, /rel="apple-touch-icon" href="\.\/icon-192\.png"/);
  assert.match(serviceWorker, /\.\/manifest\.webmanifest/);
  assert.match(serviceWorker, /\.\/icon-192\.png/);
  assert.match(serviceWorker, /\.\/icon-512\.png/);
});
