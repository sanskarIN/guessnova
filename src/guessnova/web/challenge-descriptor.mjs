import { DIFFICULTIES, fnv1a32, portableDailyTarget } from "./game-engine.mjs";

export const PORTABLE_CHALLENGE_DESCRIPTOR_VERSION = 1;
export const PORTABLE_CHALLENGE_NAMESPACE = "guessnova-challenge-v1";
export const PORTABLE_CHALLENGE_MODES = Object.freeze(["classic", "timed", "streak", "daily"]);

function validateCanonicalDate(value) {
  if (typeof value !== "string") {
    throw new Error("portable challenge date must use YYYY-MM-DD");
  }
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) throw new Error("portable challenge date must use YYYY-MM-DD");

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (year < 1 || month < 1 || month > 12) {
    throw new Error("portable challenge date must use YYYY-MM-DD");
  }
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const monthLengths = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (day < 1 || day > monthLengths[month - 1]) {
    throw new Error("portable challenge date must use YYYY-MM-DD");
  }
  return value;
}

function validateFields(value, mode) {
  const expected = mode === "daily"
    ? ["day", "difficulty", "mode", "version"]
    : ["difficulty", "mode", "seed", "version"];
  const actual = Object.keys(value).sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    const missing = expected.filter((key) => !actual.includes(key));
    const unknown = actual.filter((key) => !expected.includes(key));
    const details = [];
    if (missing.length) details.push(`missing fields: ${missing.join(", ")}`);
    if (unknown.length) details.push(`unknown fields: ${unknown.join(", ")}`);
    throw new Error(`invalid portable challenge descriptor fields (${details.join("; ")})`);
  }
}

export function normalizePortableChallengeDescriptor(value) {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("portable challenge descriptor must be an object");
  }
  if (value.version !== PORTABLE_CHALLENGE_DESCRIPTOR_VERSION) {
    throw new Error(`unsupported portable challenge descriptor version: ${value.version}`);
  }
  if (typeof value.mode !== "string" || !PORTABLE_CHALLENGE_MODES.includes(value.mode)) {
    if (value.mode === "reverse") throw new Error("game mode is not portable: reverse");
    throw new Error(`unknown game mode: ${value.mode}`);
  }
  if (typeof value.difficulty !== "string" || !DIFFICULTIES[value.difficulty]) {
    throw new Error(`unknown difficulty: ${value.difficulty}`);
  }

  validateFields(value, value.mode);
  if (value.mode === "daily") {
    return Object.freeze({
      version: PORTABLE_CHALLENGE_DESCRIPTOR_VERSION,
      mode: value.mode,
      difficulty: value.difficulty,
      day: validateCanonicalDate(value.day),
    });
  }

  if (!Number.isSafeInteger(value.seed)) {
    throw new Error("portable challenge seed must be a safe integer");
  }
  return Object.freeze({
    version: PORTABLE_CHALLENGE_DESCRIPTOR_VERSION,
    mode: value.mode,
    difficulty: value.difficulty,
    seed: value.seed,
  });
}

export function portableChallengeTarget(value) {
  const descriptor = normalizePortableChallengeDescriptor(value);
  if (descriptor.mode === "daily") {
    return portableDailyTarget(descriptor.day, descriptor.difficulty);
  }

  const difficulty = DIFFICULTIES[descriptor.difficulty];
  const fingerprint = `${PORTABLE_CHALLENGE_NAMESPACE}:${descriptor.mode}:${descriptor.difficulty}:${descriptor.seed}`;
  const span = difficulty.maximum - difficulty.minimum + 1;
  return difficulty.minimum + (fnv1a32(fingerprint) % span);
}
