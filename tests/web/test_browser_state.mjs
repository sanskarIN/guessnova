import test from "node:test";
import assert from "node:assert/strict";

import {
  BROWSER_STATE_SCHEMA,
  HISTORY_LIMIT,
  defaultBrowserState,
  normalizeBrowserState,
  parseBrowserState,
  serializeBrowserState,
} from "../../src/guessnova/web/browser-state.mjs";

test("default browser state is isolated and versioned", () => {
  const first = defaultBrowserState();
  const second = defaultBrowserState();
  assert.equal(first.schema, BROWSER_STATE_SCHEMA);
  assert.notEqual(first, second);
  assert.notEqual(first.history, second.history);
  assert.notEqual(first.settings, second.settings);
});

test("malformed persisted values normalize to safe defaults", () => {
  const state = normalizeBrowserState({
    gamesPlayed: "lots",
    gamesWon: -2,
    currentStreak: Number.NaN,
    bestStreak: Infinity,
    history: [null, "bad", 3],
    settings: { mode: "unknown", difficulty: "impossible" },
    injected: "discard me",
  });

  assert.deepEqual(state, defaultBrowserState());
  assert.equal("injected" in state, false);
});

test("inherited object keys cannot become difficulties", () => {
  const state = normalizeBrowserState({
    history: [{
      mode: "classic",
      difficulty: "toString",
      won: true,
      attempts: 1,
      target: 35,
      completedAt: "2026-08-20T00:00:00.000Z",
    }],
    settings: { mode: "classic", difficulty: "toString" },
  });

  assert.equal(state.settings.difficulty, "normal");
  assert.equal(state.history[0].difficulty, "normal");
});

test("statistics are bounded and internally consistent", () => {
  const state = normalizeBrowserState({
    gamesPlayed: 4,
    gamesWon: 99,
    currentStreak: 8,
    bestStreak: 1,
  });

  assert.equal(state.gamesPlayed, 4);
  assert.equal(state.gamesWon, 4);
  assert.equal(state.currentStreak, 4);
  assert.equal(state.bestStreak, 4);
});

test("history discards invalid entries and normalizes fields", () => {
  const history = Array.from({ length: HISTORY_LIMIT + 5 }, (_, index) => ({
    mode: index === 0 ? "bogus" : "classic",
    difficulty: index === 1 ? "bogus" : "normal",
    won: index % 2 === 0,
    attempts: index,
    target: index === 2 ? 99999 : 35,
    completedAt: index === 3 ? "not-a-date" : "2026-08-20T00:00:00.000Z",
  }));
  history.splice(4, 0, null);

  const state = normalizeBrowserState({ history });
  assert.equal(state.history.length, HISTORY_LIMIT);
  assert.equal(state.history[0].mode, "classic");
  assert.equal(state.history[1].difficulty, "normal");
  assert.equal(state.history[2].target, null);
  assert.equal(state.history[3].completedAt, null);
});

test("legacy unversioned browser state remains readable", () => {
  const state = parseBrowserState(JSON.stringify({
    gamesPlayed: 3,
    gamesWon: 2,
    currentStreak: 1,
    bestStreak: 2,
    history: [],
    settings: { mode: "daily", difficulty: "hard" },
  }));

  assert.equal(state.schema, BROWSER_STATE_SCHEMA);
  assert.equal(state.gamesPlayed, 3);
  assert.equal(state.settings.mode, "daily");
  assert.equal(state.settings.difficulty, "hard");
});

test("parse and serialize recover from corrupt storage", () => {
  assert.deepEqual(parseBrowserState("{broken"), defaultBrowserState());
  assert.deepEqual(parseBrowserState(null), defaultBrowserState());

  const serialized = serializeBrowserState({
    gamesPlayed: 2,
    gamesWon: 1,
    currentStreak: 1,
    bestStreak: 1,
    history: [{
      mode: "classic",
      difficulty: "normal",
      won: true,
      attempts: 2,
      target: 35,
      completedAt: "2026-08-20T00:00:00.000Z",
    }],
    settings: { mode: "classic", difficulty: "normal" },
  });

  assert.deepEqual(parseBrowserState(serialized), JSON.parse(serialized));
});
