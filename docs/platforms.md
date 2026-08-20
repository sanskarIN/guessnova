# Cross-platform support

GuessNova has two supported presentation families that share the same game concepts:

1. **Python desktop/terminal** — Rich CLI and Textual TUI for Windows, macOS, and Linux.
2. **Offline-first PWA** — responsive browser interface for desktop browsers, Android, iOS/iPadOS, ChromeOS, and other standards-based browser platforms.

The PWA is bundled inside the Python wheel and can also be deployed as static files from `src/guessnova/web/`.

## Support matrix

| Platform | CLI | Textual TUI | Web/PWA | Recommended path |
| --- | --- | --- | --- | --- |
| Windows 10/11 | ✅ | ✅ | ✅ | Python app or installed PWA |
| macOS | ✅ | ✅ | ✅ | Python app or installed PWA |
| Linux | ✅ | ✅ | ✅ | Python app or browser PWA |
| Android | — | — | ✅ | Chrome/Edge/Firefox browser; install PWA where supported |
| iOS | — | — | ✅ | Safari; Add to Home Screen for app-like launch |
| iPadOS | — | — | ✅ | Safari; Add to Home Screen for app-like launch |
| ChromeOS | optional Linux container | optional Linux container | ✅ | Browser PWA |
| Other modern browsers | — | — | ✅ | Responsive web app |

`—` means that the Python terminal interface is not an official native distribution for that mobile platform. The PWA is the supported mobile interface.

## Desktop setup

Python 3.13+ is required for the CLI, TUI, Doctor, and bundled local web server.

```bash
python -m pip install -e .
guessnova play
guessnova-tui
```

To launch the browser/PWA interface from an installed Python package:

```bash
guessnova web
# or
guessnova-web
```

The local server binds to `127.0.0.1` by default so it is not exposed to the network unintentionally.

## Mobile and browser use

The static PWA files live in:

```text
src/guessnova/web/
```

They contain no server-side application logic and can be hosted by any normal HTTPS static host. HTTPS is recommended for deployment because service workers and installability require a secure context outside `localhost`.

The PWA provides:

- Classic, Timed, Streak, Daily, and Reverse modes.
- Easy, Normal, Hard, and Expert difficulty ranges matching the Python domain definitions.
- Smart hints and explicit range hints.
- Local statistics, current/best streaks, and recent-round history.
- Touch-friendly responsive layouts for phones, tablets, laptops, and desktops.
- Dark/light color-scheme support and reduced-motion handling.
- Offline caching through a service worker.
- Local-only browser persistence with no account, analytics, telemetry, ads, or cloud sync.
- Install prompting where the browser exposes the PWA install API.

## Cross-platform daily challenge parity

Daily challenge rules use a small language-independent FNV-1a 32-bit hash namespace:

```text
guessnova-daily-v2:<YYYY-MM-DD>:<difficulty>
```

The resulting unsigned value is mapped into the selected difficulty's inclusive range. Python and JavaScript both carry a fixed test vector:

```text
Date:       2026-08-19
Difficulty: normal
Hash:       230553734
Target:     35
```

This avoids relying on Python's `random.Random` implementation for shared daily targets and makes the daily result reproducible across the Python and browser clients.

The legacy `daily_seed()` helper remains available for compatibility with older Python-side replay/data expectations, while new daily games use the portable v2 algorithm.

## Local server networking

The default command is private to the current computer:

```bash
guessnova web
```

For deliberate LAN testing, an explicit bind address can be supplied:

```bash
guessnova web --host 0.0.0.0 --port 8765 --no-open
```

Binding to `0.0.0.0` exposes the server to reachable network interfaces. Use it only on a trusted network and prefer an HTTPS static deployment for normal phone/tablet installation.

## Storage model

The Python and browser clients intentionally use different local persistence backends:

- Python: GuessNova schema-2 JSON in the application data directory, with profiles, backups, Doctor, recovery, and integrity checks.
- Browser/PWA: origin-scoped `localStorage` for lightweight game statistics and recent rounds.

Browser storage never silently writes into the Python data directory. This keeps browser sandboxing intact and avoids a network bridge merely for persistence.

## Accessibility and adaptive layout

The PWA includes semantic labels, a skip link, minimum touch-target sizing, live status announcements, keyboard focus indicators, `prefers-reduced-motion`, and automatic light/dark color schemes. The layout collapses from three columns to a single-column phone layout without requiring a separate mobile codebase.

The Python terminal accessibility options remain available independently through `--plain`, `--compact`, high-contrast settings, and Textual keyboard navigation.

## Verification

CI protects both platform families:

- Python lint, formatting, strict typing, pytest, compile and smoke checks.
- Browser engine tests with Node.js.
- JavaScript syntax checks for the app, engine, and service worker.
- Wheel build/install verification on Ubuntu, Windows, and macOS.
- Verification that installed wheels contain the PWA assets.
- Verification of both `guessnova web --help` and `guessnova-web --help` after wheel installation.

## Platform philosophy

GuessNova does not duplicate a separate native codebase for every operating system. Desktop terminals use the Python interface; phones, tablets, Chromebooks, and browsers use the standards-based PWA. This keeps the project maintainable while providing a supported UI path across the major consumer platform families.
