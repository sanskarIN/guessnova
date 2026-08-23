from __future__ import annotations

from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from guessnova.web_server import (
    WEB_ROOT,
    _browser_host,
    _content_type,
    _safe_asset_path,
    create_server,
)


def test_safe_asset_path_rejects_traversal() -> None:
    assert _safe_asset_path("/") == "index.html"
    assert _safe_asset_path("/app.js?cache=1") == "app.js"
    assert _safe_asset_path("/../pyproject.toml") is None
    assert _safe_asset_path("/web/../../secret") is None
    assert _safe_asset_path(r"/..\secret.txt") is None
    assert _safe_asset_path("/%2e%2e/secret.txt") is None
    assert _safe_asset_path("/web/%2e%2e/secret.txt") is None
    assert _safe_asset_path("/%5c..%5csecret.txt") is None
    assert _safe_asset_path("/safe%2f..%2fsecret.txt") is None
    assert _safe_asset_path("/bad%00name.txt") is None
    assert _safe_asset_path("//[") is None


def test_content_type_adds_charset_only_to_text_formats() -> None:
    assert _content_type("index.html") == "text/html; charset=utf-8"
    assert _content_type("app.js") == "text/javascript; charset=utf-8"
    assert _content_type("game-engine.mjs") == "text/javascript; charset=utf-8"
    assert _content_type("manifest.webmanifest") == "application/manifest+json; charset=utf-8"
    assert _content_type("icon.svg") == "image/svg+xml; charset=utf-8"
    assert _content_type("icon-192.png") == "image/png"


def test_browser_host_formats_wildcard_and_ipv6_literals() -> None:
    assert _browser_host("0.0.0.0") == "127.0.0.1"
    assert _browser_host("::") == "[::1]"
    assert _browser_host("::1") == "[::1]"
    assert _browser_host("fe80::1%lo0") == "[fe80::1%25lo0]"
    assert _browser_host("127.0.0.1") == "127.0.0.1"


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
            assert response.headers["X-Frame-Options"] == "DENY"
            assert response.headers["Referrer-Policy"] == "no-referrer"
            assert "camera=()" in response.headers["Permissions-Policy"]
            assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    finally:
        thread.join(timeout=5)
        server.server_close()


def test_server_head_returns_headers_without_body() -> None:
    server = create_server(port=0)
    host, port = server.server_address[:2]
    thread = Thread(target=server.handle_request, daemon=True)
    thread.start()
    try:
        request = Request(f"http://{host}:{port}/app.js", method="HEAD")
        with urlopen(request, timeout=5) as response:  # noqa: S310 - loopback test server
            assert response.status == 200
            assert response.read() == b""
            assert response.headers["Content-Type"].endswith("charset=utf-8")
            assert int(response.headers["Content-Length"]) > 0
    finally:
        thread.join(timeout=5)
        server.server_close()


def test_binary_asset_content_type_has_no_charset() -> None:
    server = create_server(port=0)
    host, port = server.server_address[:2]
    thread = Thread(target=server.handle_request, daemon=True)
    thread.start()
    try:
        with urlopen(f"http://{host}:{port}/icon-192.png", timeout=5) as response:  # noqa: S310
            assert response.status == 200
            assert response.headers["Content-Type"] == "image/png"
            assert response.read().startswith(b"\x89PNG\r\n\x1a\n")
    finally:
        thread.join(timeout=5)
        server.server_close()


def test_not_found_response_retains_security_headers() -> None:
    server = create_server(port=0)
    host, port = server.server_address[:2]
    thread = Thread(target=server.handle_request, daemon=True)
    thread.start()
    try:
        with pytest.raises(HTTPError) as captured:
            urlopen(f"http://{host}:{port}/missing.txt", timeout=5)  # noqa: S310
        error = captured.value
        assert error.code == 404
        assert error.headers["X-Content-Type-Options"] == "nosniff"
        assert error.headers["X-Frame-Options"] == "DENY"
        assert "frame-ancestors 'none'" in error.headers["Content-Security-Policy"]
    finally:
        thread.join(timeout=5)
        server.server_close()
