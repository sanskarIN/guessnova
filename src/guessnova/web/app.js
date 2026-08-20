import { DIFFICULTIES, GuessGame, ReverseGuesser, portableDailyTarget } from "./game-engine.mjs";

const STORAGE_KEY = "guessnova.web.v1";
const HISTORY_LIMIT = 12;

const byId = (id) => document.getElementById(id);
const modeSelect = byId("mode");
const difficultySelect = byId("difficulty");
const newGameButton = byId("newGame");
const hintButton = byId("hintButton");
const resetDataButton = byId("resetData");
const installButton = byId("installButton");
const guessForm = byId("guessForm");
const guessInput = byId("guessInput");
const standardPlay = byId("standardPlay");
const reversePlay = byId("reversePlay");
const rangeText = byId("rangeText");
const attemptsText = byId("attempts");
const hintsText = byId("hints");
const streakText = byId("streak");
const modeBadge = byId("modeBadge");
const playTitle = byId("playTitle");
const message = byId("message");
const timer = byId("timer");
const reverseGuess = byId("reverseGuess");
const lowerButton = byId("lowerButton");
const correctButton = byId("correctButton");
const higherButton = byId("higherButton");

let game = null;
let reverse = null;
let timerId = null;
let installPrompt = null;
let recordedCurrentRound = false;

function defaultState() {
  return {
    gamesPlayed: 0,
    gamesWon: 0,
    currentStreak: 0,
    bestStreak: 0,
    history: [],
    settings: { mode: "classic", difficulty: "normal" },
  };
}

function loadState() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "null");
    if (!parsed || typeof parsed !== "object") return defaultState();
    const base = defaultState();
    return {
      ...base,
      ...parsed,
      history: Array.isArray(parsed.history) ? parsed.history.slice(0, HISTORY_LIMIT) : [],
      settings: { ...base.settings, ...(parsed.settings ?? {}) },
    };
  } catch {
    return defaultState();
  }
}

let state = loadState();

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // Privacy settings can block persistence; gameplay continues in memory.
  }
}

function clearSavedState() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // A blocked storage backend is already effectively cleared for this app session.
  }
}

function localDay() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function titleCase(value) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function setMessage(text) {
  message.textContent = text;
}

function stopTimer() {
  if (timerId !== null) {
    clearInterval(timerId);
    timerId = null;
  }
}

function renderStats() {
  byId("gamesPlayed").textContent = String(state.gamesPlayed);
  byId("gamesWon").textContent = String(state.gamesWon);
  byId("winRate").textContent = state.gamesPlayed === 0 ? "0%" : `${Math.round((state.gamesWon / state.gamesPlayed) * 100)}%`;
  byId("bestStreak").textContent = String(state.bestStreak);
  streakText.textContent = String(state.currentStreak);

  const history = byId("history");
  history.replaceChildren();
  if (state.history.length === 0) {
    const item = document.createElement("li");
    item.textContent = "No rounds yet.";
    history.append(item);
    return;
  }
  for (const round of state.history) {
    const item = document.createElement("li");
    const result = round.won ? "Won" : "Lost";
    item.textContent = `${result} · ${titleCase(round.mode)} · ${titleCase(round.difficulty)} · ${round.attempts} attempt${round.attempts === 1 ? "" : "s"}`;
    history.append(item);
  }
}

function recordRound(summary) {
  if (recordedCurrentRound) return;
  recordedCurrentRound = true;
  state.gamesPlayed += 1;
  if (summary.won) {
    state.gamesWon += 1;
    state.currentStreak += 1;
    state.bestStreak = Math.max(state.bestStreak, state.currentStreak);
  } else {
    state.currentStreak = 0;
  }
  state.history.unshift({
    mode: summary.mode,
    difficulty: summary.difficulty,
    won: summary.won,
    attempts: summary.attempts,
    target: summary.target ?? null,
    completedAt: new Date().toISOString(),
  });
  state.history = state.history.slice(0, HISTORY_LIMIT);
  saveState();
  renderStats();
}

function finishStandard(outcome) {
  stopTimer();
  guessInput.disabled = true;
  hintButton.disabled = true;
  const summary = game.summary();
  recordRound(summary);
  if (outcome === "correct") {
    setMessage(`Correct! The target was ${summary.target}. You solved it in ${summary.attempts} attempt${summary.attempts === 1 ? "" : "s"}.`);
  } else if (outcome === "timeout") {
    setMessage(`Time expired. The target was ${summary.target}. Start a new round to try again.`);
  } else {
    setMessage(`No attempts left. The target was ${summary.target}. Start a new round to try again.`);
  }
}

function updateRoundMetrics() {
  if (!game) return;
  attemptsText.textContent = `${game.attemptsUsed} / ${game.difficulty.maxAttempts}`;
  hintsText.textContent = String(game.hintsUsed);
}

function startTimer() {
  stopTimer();
  if (!game || game.mode !== "timed") {
    timer.hidden = true;
    return;
  }
  timer.hidden = false;
  const tick = () => {
    if (!game || game.finished) return;
    const remaining = Math.max(0, Math.ceil(game.difficulty.timedSeconds - game.elapsedSeconds));
    timer.textContent = `${remaining}s`;
    if (remaining <= 0) {
      const feedback = game.guess(game.difficulty.minimum - 1);
      finishStandard(feedback.outcome);
    }
  };
  tick();
  timerId = setInterval(tick, 250);
}

function startReverse(difficultyName) {
  const difficulty = DIFFICULTIES[difficultyName];
  reverse = new ReverseGuesser(difficulty.minimum, difficulty.maximum);
  game = null;
  standardPlay.hidden = true;
  reversePlay.hidden = false;
  hintButton.disabled = true;
  lowerButton.disabled = false;
  correctButton.disabled = false;
  higherButton.disabled = false;
  timer.hidden = true;
  playTitle.textContent = "I’ll guess your number";
  rangeText.textContent = "";
  reverseGuess.textContent = String(reverse.nextGuess());
  setMessage(`Think of a number from ${difficulty.minimum} to ${difficulty.maximum}. Tell me whether my guess should be lower or higher.`);
}

function startStandard(mode, difficultyName) {
  const difficulty = DIFFICULTIES[difficultyName];
  let target = null;
  if (mode === "daily") target = portableDailyTarget(localDay(), difficultyName);
  game = new GuessGame({ mode, difficultyName, target });
  reverse = null;
  standardPlay.hidden = false;
  reversePlay.hidden = true;
  guessInput.disabled = false;
  hintButton.disabled = false;
  playTitle.textContent = mode === "daily" ? "Today’s shared challenge" : "Find the hidden number";
  rangeText.textContent = `Choose a number from ${difficulty.minimum} to ${difficulty.maximum}.`;
  guessInput.min = String(difficulty.minimum);
  guessInput.max = String(difficulty.maximum);
  guessInput.value = "";
  attemptsText.textContent = `0 / ${difficulty.maxAttempts}`;
  hintsText.textContent = "0";
  setMessage(mode === "daily" ? `Daily challenge for ${localDay()}.` : "Start guessing.");
  startTimer();
  guessInput.focus();
}

function startRound() {
  stopTimer();
  recordedCurrentRound = false;
  const mode = modeSelect.value;
  const difficultyName = difficultySelect.value;
  state.settings = { mode, difficulty: difficultyName };
  saveState();
  modeBadge.textContent = `${titleCase(mode)} · ${titleCase(difficultyName)}`;
  if (mode === "reverse") startReverse(difficultyName);
  else startStandard(mode, difficultyName);
  renderStats();
}

function reverseResponse(response) {
  if (!reverse || reverse.finished) return;
  try {
    reverse.respond(response);
    if (response === "correct") {
      const attempts = reverse.attempts;
      recordRound({ mode: "reverse", difficulty: difficultySelect.value, won: true, attempts, target: reverse.current });
      setMessage(`Got it in ${attempts} attempt${attempts === 1 ? "" : "s"}! Start a new round to play again.`);
      lowerButton.disabled = true;
      correctButton.disabled = true;
      higherButton.disabled = true;
      return;
    }
    reverseGuess.textContent = String(reverse.nextGuess());
    setMessage("Thanks — narrowing the range.");
  } catch (error) {
    setMessage(error instanceof Error ? error.message : "Those answers are inconsistent. Start a new round.");
  }
}

guessForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!game || game.finished) return;
  const value = Number(guessInput.value);
  const feedback = game.guess(value);
  updateRoundMetrics();
  if (feedback.outcome === "out_of_range") {
    setMessage(`Enter a whole number from ${game.difficulty.minimum} to ${game.difficulty.maximum}.`);
    return;
  }
  if (["correct", "exhausted", "timeout"].includes(feedback.outcome)) {
    finishStandard(feedback.outcome);
    return;
  }
  const direction = feedback.outcome === "too_low" ? "Too low." : "Too high.";
  setMessage(`${direction} ${feedback.hint ?? ""}`.trim());
  guessInput.select();
});

hintButton.addEventListener("click", () => {
  if (!game || game.finished) return;
  try {
    setMessage(game.requestHint({ penalize: true }));
    updateRoundMetrics();
  } catch (error) {
    if (game.finished) finishStandard("timeout");
    else setMessage(error instanceof Error ? error.message : "Unable to create a hint.");
  }
});

newGameButton.addEventListener("click", startRound);
modeSelect.addEventListener("change", () => {
  hintButton.disabled = modeSelect.value === "reverse";
});
lowerButton.addEventListener("click", () => reverseResponse("lower"));
correctButton.addEventListener("click", () => reverseResponse("correct"));
higherButton.addEventListener("click", () => reverseResponse("higher"));

resetDataButton.addEventListener("click", () => {
  const confirmed = globalThis.confirm("Reset all GuessNova progress stored in this browser?");
  if (!confirmed) return;
  clearSavedState();
  state = defaultState();
  modeSelect.value = state.settings.mode;
  difficultySelect.value = state.settings.difficulty;
  renderStats();
  startRound();
});

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  installPrompt = event;
  installButton.hidden = false;
});

installButton.addEventListener("click", async () => {
  if (!installPrompt) return;
  await installPrompt.prompt();
  await installPrompt.userChoice;
  installPrompt = null;
  installButton.hidden = true;
});

window.addEventListener("appinstalled", () => {
  installPrompt = null;
  installButton.hidden = true;
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch(() => {
      setMessage("The game works online, but offline installation could not be enabled in this browser.");
    });
  });
}

if (state.settings.mode in { classic: 1, timed: 1, streak: 1, daily: 1, reverse: 1 }) {
  modeSelect.value = state.settings.mode;
}
if (state.settings.difficulty in DIFFICULTIES) {
  difficultySelect.value = state.settings.difficulty;
}
renderStats();
startRound();