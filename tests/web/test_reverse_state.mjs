import test from "node:test";
import assert from "node:assert/strict";

import { ReverseGuesser } from "../../src/guessnova/web/game-engine.mjs";

test("reverse guess requires feedback before another guess", () => {
  const reverse = new ReverseGuesser(1, 100);
  assert.equal(reverse.nextGuess(), 50);

  assert.throws(() => reverse.nextGuess(), /respond before/);
  assert.equal(reverse.attempts, 1);
  assert.equal(reverse.current, 50);
});

test("valid reverse feedback consumes the pending guess", () => {
  const reverse = new ReverseGuesser(1, 100);
  assert.equal(reverse.nextGuess(), 50);
  reverse.respond("higher");

  assert.equal(reverse.current, null);
  assert.equal(reverse.low, 51);
  assert.equal(reverse.nextGuess(), 75);
});

test("invalid reverse feedback remains recoverable", () => {
  const reverse = new ReverseGuesser(1, 2);
  assert.equal(reverse.nextGuess(), 1);

  assert.throws(() => reverse.respond("lower"), /inconsistent/);
  assert.equal(reverse.current, 1);
  assert.equal(reverse.low, 1);
  assert.equal(reverse.high, 2);

  reverse.respond("higher");
  assert.equal(reverse.current, null);
  assert.equal(reverse.nextGuess(), 2);
});

test("reverse feedback requires text without consuming pending guess", () => {
  const reverse = new ReverseGuesser(1, 10);
  assert.equal(reverse.nextGuess(), 5);

  assert.throws(() => reverse.respond(null), /higher, lower, or correct/);
  assert.equal(reverse.current, 5);
  assert.equal(reverse.attempts, 1);
  assert.equal(reverse.low, 1);
  assert.equal(reverse.high, 10);
});
