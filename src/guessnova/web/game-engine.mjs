export const DIFFICULTIES = Object.freeze({
  easy: Object.freeze({ minimum: 1, maximum: 50, maxAttempts: 10, timedSeconds: 60 }),
  normal: Object.freeze({ minimum: 1, maximum: 100, maxAttempts: 9, timedSeconds: 45 }),
  hard: Object.freeze({ minimum: 1, maximum: 500, maxAttempts: 10, timedSeconds: 40 }),
  expert: Object.freeze({ minimum: 1, maximum: 1000, maxAttempts: 10, timedSeconds: 35 }),
});

export const MODES = Object.freeze(["classic", "timed", "streak", "daily", "reverse"]);
export const HINT_PENALTY_XP = 10;

export function fnv1a32(text) {
  const bytes = new TextEncoder().encode(text);
  let hash = 0x811c9dc5;
  for (const value of bytes) {
    hash ^= value;
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash >>> 0;
}

export function portableDailyTarget(day, difficultyName = "normal") {
  const difficulty = DIFFICULTIES[difficultyName];
  if (!difficulty) throw new Error(`unknown difficulty: ${difficultyName}`);
  const span = difficulty.maximum - difficulty.minimum + 1;
  const hash = fnv1a32(`guessnova-daily-v2:${day}:${difficultyName}`);
  return difficulty.minimum + (hash % span);
}

export function randomTarget(difficultyName = "normal") {
  const difficulty = DIFFICULTIES[difficultyName];
  if (!difficulty) throw new Error(`unknown difficulty: ${difficultyName}`);
  const span = difficulty.maximum - difficulty.minimum + 1;
  const values = new Uint32Array(1);
  globalThis.crypto.getRandomValues(values);
  return difficulty.minimum + (values[0] % span);
}

export function smartHint(target, guess, difficulty) {
  const distance = Math.abs(target - guess);
  const ratio = distance / Math.max(1, difficulty.maximum - difficulty.minimum);
  let temperature = "cold";
  if (ratio <= 0.02) temperature = "scorching hot";
  else if (ratio <= 0.08) temperature = "hot";
  else if (ratio <= 0.2) temperature = "warm";
  else if (ratio <= 0.4) temperature = "cool";
  const parity = target % 2 === 0 ? "even" : "odd";
  const direction = target > guess ? "higher" : "lower";
  return `${temperature}; try ${direction}. The target is ${parity}.`;
}

export class GuessGame {
  constructor({ difficultyName = "normal", mode = "classic", target = null, now = () => performance.now() } = {}) {
    if (!DIFFICULTIES[difficultyName]) throw new Error(`unknown difficulty: ${difficultyName}`);
    if (!MODES.includes(mode) || mode === "reverse") throw new Error(`unsupported GuessGame mode: ${mode}`);
    this.difficultyName = difficultyName;
    this.mode = mode;
    this.difficulty = DIFFICULTIES[difficultyName];
    this.now = now;
    this.target = target ?? randomTarget(difficultyName);
    if (
      !Number.isInteger(this.target)
      || this.target < this.difficulty.minimum
      || this.target > this.difficulty.maximum
    ) {
      throw new Error("target is outside the difficulty range");
    }
    this.startedAt = this.now();
    this.finishedAt = null;
    this.guesses = [];
    this.finished = false;
    this.won = false;
    this.hintsUsed = 0;
    this.hintPenalty = 0;
  }

  get attemptsUsed() { return this.guesses.length; }
  get attemptsLeft() { return Math.max(0, this.difficulty.maxAttempts - this.attemptsUsed); }
  get elapsedSeconds() {
    const endpoint = this.finishedAt ?? this.now();
    return Math.max(0, (endpoint - this.startedAt) / 1000);
  }
  get timedOut() { return this.mode === "timed" && this.elapsedSeconds >= this.difficulty.timedSeconds; }

  isTimedOutAt(timestamp) {
    return this.mode === "timed"
      && Math.max(0, (timestamp - this.startedAt) / 1000) >= this.difficulty.timedSeconds;
  }

  finish(timestamp, won = false) {
    this.finished = true;
    this.won = won;
    this.finishedAt = timestamp;
  }

  requestHint({ penalize = true } = {}) {
    if (this.finished) throw new Error("game is already finished");
    const now = this.now();
    if (this.isTimedOutAt(now)) {
      this.finish(now);
      throw new Error("time expired");
    }
    const span = this.difficulty.maximum - this.difficulty.minimum + 1;
    const radius = Math.max(2, Math.floor(span / 10));
    let lower = Math.max(this.difficulty.minimum, this.target - radius);
    let upper = Math.min(this.difficulty.maximum, this.target + radius);
    if (lower === upper) {
      lower = Math.max(this.difficulty.minimum, lower - 1);
      upper = Math.min(this.difficulty.maximum, upper + 1);
    }
    this.hintsUsed += 1;
    if (penalize) this.hintPenalty += HINT_PENALTY_XP;
    const suffix = penalize ? ` Using it costs ${HINT_PENALTY_XP} XP from a winning reward.` : "";
    return `Range hint: the target is between ${lower} and ${upper}.${suffix}`;
  }

  guess(value) {
    if (this.finished) throw new Error("game is already finished");
    const now = this.now();
    if (this.isTimedOutAt(now)) {
      this.finish(now);
      return { guess: value, outcome: "timeout", attemptsUsed: this.attemptsUsed, attemptsLeft: this.attemptsLeft };
    }
    if (!Number.isInteger(value) || value < this.difficulty.minimum || value > this.difficulty.maximum) {
      return { guess: value, outcome: "out_of_range", attemptsUsed: this.attemptsUsed, attemptsLeft: this.attemptsLeft };
    }
    this.guesses.push(value);
    if (value === this.target) {
      this.finish(now, true);
      return { guess: value, outcome: "correct", attemptsUsed: this.attemptsUsed, attemptsLeft: this.attemptsLeft };
    }
    if (this.attemptsLeft === 0) {
      this.finish(now);
      return { guess: value, outcome: "exhausted", attemptsUsed: this.attemptsUsed, attemptsLeft: 0 };
    }
    const outcome = value < this.target ? "too_low" : "too_high";
    return {
      guess: value,
      outcome,
      attemptsUsed: this.attemptsUsed,
      attemptsLeft: this.attemptsLeft,
      hint: smartHint(this.target, value, this.difficulty),
    };
  }

  summary() {
    return {
      mode: this.mode,
      difficulty: this.difficultyName,
      target: this.target,
      won: this.won,
      attempts: this.attemptsUsed,
      elapsedSeconds: this.elapsedSeconds,
      guesses: [...this.guesses],
      hintsUsed: this.hintsUsed,
      hintPenalty: this.hintPenalty,
    };
  }
}

export class ReverseGuesser {
  constructor(minimum = 1, maximum = 100) {
    if (minimum >= maximum) throw new Error("minimum must be less than maximum");
    this.minimum = minimum;
    this.maximum = maximum;
    this.low = minimum;
    this.high = maximum;
    this.current = null;
    this.attempts = 0;
    this.finished = false;
  }

  nextGuess() {
    if (this.finished) throw new Error("reverse game is already finished");
    if (this.low > this.high) throw new Error("responses are inconsistent");
    this.current = Math.floor((this.low + this.high) / 2);
    this.attempts += 1;
    return this.current;
  }

  respond(response) {
    if (this.finished) throw new Error("reverse game is already finished");
    if (this.current === null) throw new Error("call nextGuess before respond");
    const normalized = response.trim().toLowerCase();
    if (normalized === "correct") {
      this.finished = true;
      return;
    }
    if (normalized === "higher") {
      const nextLow = this.current + 1;
      if (nextLow > this.high) throw new Error("responses are inconsistent");
      this.low = nextLow;
    } else if (normalized === "lower") {
      const nextHigh = this.current - 1;
      if (this.low > nextHigh) throw new Error("responses are inconsistent");
      this.high = nextHigh;
    } else {
      throw new Error("response must be higher, lower, or correct");
    }
  }
}
