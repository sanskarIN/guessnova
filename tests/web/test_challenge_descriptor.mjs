import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

import {
  PORTABLE_CHALLENGE_DESCRIPTOR_VERSION,
  normalizePortableChallengeDescriptor,
  portableChallengeTarget,
} from "../../src/guessnova/web/challenge-descriptor.mjs";

const vectors = JSON.parse(
  readFileSync(new URL("../fixtures/portable_challenges_v1.json", import.meta.url), "utf8"),
);

test("shared portable challenge vectors match the browser engine", () => {
  for (const vector of vectors) {
    assert.deepEqual(normalizePortableChallengeDescriptor(vector.descriptor), vector.descriptor);
    assert.equal(portableChallengeTarget(vector.descriptor), vector.target);
  }
});

test("portable challenge descriptor rejects unsupported versions", () => {
  assert.equal(PORTABLE_CHALLENGE_DESCRIPTOR_VERSION, 1);
  assert.throws(
    () => normalizePortableChallengeDescriptor({
      version: 2,
      mode: "classic",
      difficulty: "normal",
      seed: 42,
    }),
    /unsupported portable challenge descriptor version: 2/,
  );
});

test("portable challenge descriptor rejects non-portable modes", () => {
  assert.throws(
    () => normalizePortableChallengeDescriptor({
      version: 1,
      mode: "reverse",
      difficulty: "normal",
      seed: 42,
    }),
    /game mode is not portable: reverse/,
  );
});

test("portable challenge descriptor enforces safe seeds and canonical dates", () => {
  assert.throws(
    () => normalizePortableChallengeDescriptor({
      version: 1,
      mode: "classic",
      difficulty: "normal",
      seed: Number.MAX_SAFE_INTEGER + 1,
    }),
    /safe integer/,
  );
  assert.throws(
    () => normalizePortableChallengeDescriptor({
      version: 1,
      mode: "daily",
      difficulty: "normal",
      day: "2026-02-30",
    }),
    /YYYY-MM-DD/,
  );
});
