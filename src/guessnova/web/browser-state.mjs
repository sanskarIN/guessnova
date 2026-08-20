import { DIFFICULTIES, MODES } from "./game-engine.mjs";

export const STORAGE_KEY = "guessnova.web.v1";
export const HISTORY_LIMIT = 12;
export const BROWSER_STATE_SCHEMA = 1;
export const MAX_SERIALIZED_STATE_CHARS = 262_144;

const MAX_COUNTER = 1_000_000_000;

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function normalizeCounter(value) {
  if (!Number.isSafeInteger(value) || value < 0) return 0;
  return Math.min(value, MAX_COUNTER);
}

function normalizeMode(value) {
  return typeof value === "string" && MODES.includes(value) ? value : "classic";
}

function normalizeDifficulty(value) {
  return typeof value === "string" && Object.hasOwn(DIFFICULTIES, value) ? value : "normal";
}

function normalizeCompletedAt(value) {
  if (typeof value !== "string" || value.length === 0 || value.length > 64) return null;
  return Number.isNaN(Date.parse(value)) ? null : value;
}

function normalizeHistoryEntry(value) {
  if (!isRecord(value)) return null;
  const mode = normalizeMode(value.mode);
  const difficulty = normalizeDifficulty(value.difficulty);
  const definition = DIFFICULTIES[difficulty];
  const target = Number.isSafeInteger(value.target)
    && value.target >= definition.minimum
    && value.target <= definition.maximum
    ? value.target
    : null;

  return {
    mode,
    difficulty,
    won: value.won === true,
    attempts: normalizeCounter(value.attempts),
    target,
    completedAt: normalizeCompletedAt(value.completedAt),
  };
}

export function defaultBrowserState() {
  return {
    schema: BROWSER_STATE_SCHEMA,
    gamesPlayed: 0,
    gamesWon: 0,
    currentStreak: 0,
    bestStreak: 0,
    history: [],
    settings: { mode: "classic", difficulty: "normal" },
  };
}

export function normalizeBrowserState(value) {
  if (!isRecord(value)) return defaultBrowserState();
  if (Object.hasOwn(value, "schema") && value.schema !== BROWSER_STATE_SCHEMA) {
    return defaultBrowserState();
  }

  const gamesPlayed = normalizeCounter(value.gamesPlayed);
  const gamesWon = Math.min(normalizeCounter(value.gamesWon), gamesPlayed);
  const currentStreak = Math.min(normalizeCounter(value.currentStreak), gamesWon);
  const bestStreak = Math.min(
    Math.max(normalizeCounter(value.bestStreak), currentStreak),
    gamesWon,
  );
  const history = Array.isArray(value.history)
    ? value.history
      .map(normalizeHistoryEntry)
      .filter((entry) => entry !== null)
      .slice(0, HISTORY_LIMIT)
    : [];
  const settings = isRecord(value.settings) ? value.settings : {};

  return {
    schema: BROWSER_STATE_SCHEMA,
    gamesPlayed,
    gamesWon,
    currentStreak,
    bestStreak,
    history,
    settings: {
      mode: normalizeMode(settings.mode),
      difficulty: normalizeDifficulty(settings.difficulty),
    },
  };
}

export function parseBrowserState(serialized) {
  if (
    typeof serialized !== "string"
    || serialized.length === 0
    || serialized.length > MAX_SERIALIZED_STATE_CHARS
  ) {
    return defaultBrowserState();
  }
  try {
    return normalizeBrowserState(JSON.parse(serialized));
  } catch {
    return defaultBrowserState();
  }
}

export function serializeBrowserState(value) {
  return JSON.stringify(normalizeBrowserState(value));
}
