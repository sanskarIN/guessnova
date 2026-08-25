"""Verify the installed GuessNova package contains a coherent PWA asset set."""

from __future__ import annotations

import json
from typing import Final

from guessnova.web_server import WEB_ROOT

REQUIRED_ASSETS: Final = (
    "index.html",
    "app.css",
    "app.js",
    "browser-state.mjs",
    "challenge-descriptor.mjs",
    "game-engine.mjs",
    "manifest.webmanifest",
    "sw.js",
    "icon.svg",
    "icon-192.png",
    "icon-512.png",
)
APP_SHELL_REFERENCES: Final = (
    "./",
    "./index.html",
    "./app.css",
    "./app.js",
    "./browser-state.mjs",
    "./game-engine.mjs",
    "./manifest.webmanifest",
    "./icon.svg",
    "./icon-192.png",
    "./icon-512.png",
)
PNG_SIGNATURE: Final = b"\x89PNG\r\n\x1a\n"
EXPECTED_ICONS: Final = {
    "./icon-192.png": 192,
    "./icon-512.png": 512,
}


def _png_dimensions(payload: bytes) -> tuple[int, int]:
    if len(payload) < 24 or payload[:8] != PNG_SIGNATURE or payload[12:16] != b"IHDR":
        raise RuntimeError("invalid PNG header")
    width = int.from_bytes(payload[16:20], "big")
    height = int.from_bytes(payload[20:24], "big")
    return width, height


def _manifest() -> dict[str, object]:
    payload = json.loads(WEB_ROOT.joinpath("manifest.webmanifest").read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("manifest.webmanifest must contain a JSON object")
    return payload


def _verify_manifest(manifest: dict[str, object]) -> None:
    expected_fields = {
        "name": "GuessNova",
        "short_name": "GuessNova",
        "id": "./",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
    }
    for field, expected in expected_fields.items():
        if manifest.get(field) != expected:
            raise RuntimeError(f"manifest.webmanifest {field!r} must be {expected!r}")

    icons = manifest.get("icons")
    if not isinstance(icons, list) or len(icons) != len(EXPECTED_ICONS):
        raise RuntimeError("manifest.webmanifest must declare the required install icons")

    seen: set[str] = set()
    for raw_icon in icons:
        if not isinstance(raw_icon, dict):
            raise RuntimeError("manifest icon entries must be JSON objects")
        src = raw_icon.get("src")
        if not isinstance(src, str) or src not in EXPECTED_ICONS:
            raise RuntimeError(f"unexpected manifest icon path: {src!r}")
        dimension = EXPECTED_ICONS[src]
        if raw_icon.get("sizes") != f"{dimension}x{dimension}":
            raise RuntimeError(f"manifest icon {src} has incorrect sizes metadata")
        if raw_icon.get("type") != "image/png":
            raise RuntimeError(f"manifest icon {src} must use image/png")
        seen.add(src)

        payload = WEB_ROOT.joinpath(src.removeprefix("./")).read_bytes()
        if _png_dimensions(payload) != (dimension, dimension):
            raise RuntimeError(f"manifest icon {src} does not match its declared dimensions")

    if seen != set(EXPECTED_ICONS):
        raise RuntimeError("manifest.webmanifest is missing a required install icon")


def _verify_references() -> None:
    html = WEB_ROOT.joinpath("index.html").read_text(encoding="utf-8")
    service_worker = WEB_ROOT.joinpath("sw.js").read_text(encoding="utf-8")

    html_markers = (
        'rel="manifest" href="./manifest.webmanifest"',
        'rel="apple-touch-icon" href="./icon-192.png"',
        'type="module" src="./app.js"',
    )
    for marker in html_markers:
        if marker not in html:
            raise RuntimeError(f"index.html is missing required reference: {marker}")

    for reference in APP_SHELL_REFERENCES:
        if reference not in service_worker:
            raise RuntimeError(f"sw.js app shell is missing {reference}")


def main() -> int:
    missing = [name for name in REQUIRED_ASSETS if not WEB_ROOT.joinpath(name).is_file()]
    if missing:
        raise RuntimeError(f"installed PWA assets are missing: {', '.join(missing)}")

    _verify_manifest(_manifest())
    _verify_references()
    print("GuessNova installed web package assets verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
