import test from "node:test";
import assert from "node:assert/strict";

import {
  DIFFICULTIES,
  GuessGame,
  ReverseGuesser,
  fnv1a32,
  portableDailyTarget,
  smartHint,
} from "../../src/guessnova/web/game-engine.mjs";

test("portable daily vector matches Python", () => {
  const text = "guessnova-daily-v2:2026-08-19:normal";
  assert.equal(fnv1a32(text), 230553734);
  assert.equal(portableDailyTarget("2026-08-19", "normal"), 35);
});

test("difficulty definitions match the Python domain", () => {
  assert.deepEqual(DIFFICULTIES.easy, { minimum: 1, maximum: 50, maxAttempts: 10, timedSeconds: 60 });
  assert.deepEqual(DIFFICULTIES.normal, { minimum: 1, maximum: 100, maxAttempts: 9, timedSeconds: 45 });
  assert.deepEqual(DIFFICULTIES.hard, { minimum: 1, maximum: 500, maxAttempts: 10, timedSeconds: 40 });
  assert.deepEqual(DIFFICULTIES.expert, { minimum: 1, maximum: 1000, maxAttempts: 10, timedSeconds: 35 });
});

test("browser GuessGame follows classic outcome semantics", () => {
  let now = 0;
  const game = new GuessGame({ difficultyName: "normal", mode: "classic", target: 35, now: () => now });
  const low = game.guess(20);
  assert.equal(low.outcome, "too_low");
  assert.equal(low.attemptsUsed, 1);
  assert.match(low.hint, /higher/);

  now = 1500;
  const won = game.guess(35);
  assert.equal(won.outcome, "correct");
  assert.equal(game.summary().won, true);
  assert.equal(game.summary().attempts, 2);
  assert.equal(game.summary().elapsedSeconds, 1.5);

  now = 999_000;
  assert.equal(game.summary().elapsedSeconds, 1.5);
});

test("timed browser rounds freeze timeout duration", () => {
  let now = 0;
  const game = new GuessGame({ difficultyName: "normal", mode: "timed", target: 35, now: () => now });
  now = 45_000;
  assert.equal(game.guess(20).outcome, "timeout");

  now = 90_000;
  assert.equal(game.summary().elapsedSeconds, 45);
});

test("browser GuessGame rejects non-integer explicit targets", () => {
  assert.throws(
    () => new GuessGame({ difficultyName: "normal", target: 35.5 }),
    /outside the difficulty range/,
  );
});

test("smart hints preserve Python thresholds and parity", () => {
  const hint = smartHint(50, 45, DIFFICULTIES.normal);
  assert.match(hint, /hot/);
  assert.match(hint, /higher/);
  assert.match(hint, /even/);
});

test("reverse guesser converges with binary responses", () => {
  const reverse = new ReverseGuesser(1, 100);
  assert.equal(reverse.nextGuess(), 50);
  reverse.respond("higher");
  assert.equal(reverse.nextGuess(), 75);
  reverse.respond("lower");
  assert.equal(reverse.nextGuess(), 62);
  reverse.respond("correct");
  assert.equal(reverse.finished, true);
  assert.equal(reverse.attempts, 3);
});

test("reverse contradictions do not corrupt search bounds", () => {
  const reverse = new ReverseGuesser(1, 2);
  assert.equal(reverse.nextGuess(), 1);

  assert.throws(() => reverse.respond("lower"), /inconsistent/);
  assert.deepEqual(
    { low: reverse.low, high: reverse.high, current: reverse.current, attempts: reverse.attempts },
    { low: 1, high: 2, current: 1, attempts: 1 },
  );

  reverse.respond("higher");
  assert.equal(reverse.nextGuess(), 2);
});

test("reverse feedback is rejected after completion", () => {
  const reverse = new ReverseGuesser(1, 2);
  assert.equal(reverse.nextGuess(), 1);
  reverse.respond("correct");
  const snapshot = { low: reverse.low, high: reverse.high, current: reverse.current, attempts: reverse.attempts };

  assert.throws(() => reverse.respond("higher"), /already finished/);
  assert.deepEqual(
    { low: reverse.low, high: reverse.high, current: reverse.current, attempts: reverse.attempts },
    snapshot,
  );
});
