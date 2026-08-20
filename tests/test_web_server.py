from __future__ import annotations

from threading import Thread
from urllib.request import Request, urlopen

from guessnova.web_server import WEB_ROOT, _safe_asset_path, create_server


def test_safe_asset_path_rejects_traversal() -> None:
    assert _safe_asset_path("/") == "index.html"
    assert _safe_asset_path("/app.js?cache=1") == "app.js"
    assert _safe_asset_path("/../pyproject.toml") is None
    assert _safe_asset_path("/web/../../secret") is None


def test_required_pwa_assets_are_bundled() -> None:
    for name in (
        "index.html",
        "app.css",
        "app.js",
        "browser-state.mjs",
        "game-engine.mjs",
        "manifest.webmanifest",
        "sw.js",
        "icon.svg",
        "icon-192.png",
        "icon-512.png",
    ):
        assert WEB_ROOT.joinpath(name).is_file(), name


def test_server_serves_index_with_security_headers() -> None:
    server = create_server(port=0)
    host, port = server.server_address[:2]
    thread = Thread(target=server.handle_request, daemon=True)
    thread.start()
    try:
        request = Request(f"http://{host}:{port}/", headers={"User-Agent": "GuessNova-test"})
        with urlopen(request, timeout=5) as response:  # noqa: S310 - loopback test server
            body = response.read().decode("utf-8")
            assert response.status == 200
            assert "GuessNova" in body
            assert response.headers["X-Content-Type-Options"] == "nosniff"
            assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    finally:
        thread.join(timeout=5)
        server.server_close()
