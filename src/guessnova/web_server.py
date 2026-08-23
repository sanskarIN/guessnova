"""Serve the bundled GuessNova progressive web app with the Python standard library."""

from __future__ import annotations

import argparse
import mimetypes
import socket
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import PurePosixPath
from typing import Final
from urllib.parse import unquote, urlsplit

DEFAULT_HOST: Final = "127.0.0.1"
DEFAULT_PORT: Final = 8765
WEB_ROOT = resources.files("guessnova").joinpath("web")

_TEXTUAL_CONTENT_TYPES: Final = frozenset(
    {
        "application/javascript",
        "application/json",
        "application/manifest+json",
        "image/svg+xml",
        "text/css",
        "text/html",
        "text/javascript",
    }
)

CONTENT_SECURITY_POLICY: Final = (
    "default-src 'self'; style-src 'self'; script-src 'self'; "
    "img-src 'self' data:; manifest-src 'self'; connect-src 'self'; "
    "worker-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
)


class _IPv6ThreadingHTTPServer(ThreadingHTTPServer):
    """Threading HTTP server variant for explicit IPv6 literal binds."""

    address_family = socket.AF_INET6


def _safe_asset_path(raw_path: str) -> str | None:
    """Return a normalized bundled asset path, rejecting traversal attempts."""
    try:
        path = unquote(urlsplit(raw_path).path)
    except ValueError:
        return None
    if path in {"", "/"}:
        return "index.html"
    if "\\" in path or "\x00" in path:
        return None
    candidate = PurePosixPath(path.lstrip("/"))
    if ".." in candidate.parts:
        return None
    return candidate.as_posix()


def _content_type(asset_path: str) -> str:
    """Return an HTTP Content-Type value with charset only for text formats."""
    guessed = mimetypes.guess_type(asset_path)[0] or "application/octet-stream"
    if asset_path.endswith(".webmanifest"):
        guessed = "application/manifest+json"
    if guessed in _TEXTUAL_CONTENT_TYPES or guessed.startswith("text/"):
        return f"{guessed}; charset=utf-8"
    return guessed


def _browser_host(host: str) -> str:
    """Return a URL-safe local host for the browser launch message."""
    if host == "0.0.0.0":
        return "127.0.0.1"
    if host == "::":
        return "[::1]"
    if ":" in host and not host.startswith("["):
        return f"[{host.replace('%', '%25')}]"
    return host


class GuessNovaWebHandler(BaseHTTPRequestHandler):
    """Read-only handler for the embedded PWA assets."""

    server_version = "GuessNovaWeb/1"

    def end_headers(self) -> None:
        """Apply the same browser security headers to success and error responses."""
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header(
            "Permissions-Policy",
            "camera=(), geolocation=(), microphone=(), payment=(), usb=()",
        )
        self.send_header("Content-Security-Policy", CONTENT_SECURITY_POLICY)
        super().end_headers()

    def _asset(self) -> tuple[bytes, str] | None:
        asset_path = _safe_asset_path(self.path)
        if asset_path is None:
            return None
        resource = WEB_ROOT.joinpath(asset_path)
        try:
            if not resource.is_file():
                return None
            payload = resource.read_bytes()
        except (FileNotFoundError, OSError):
            return None
        return payload, _content_type(asset_path)

    def _send_asset(self, *, include_body: bool) -> None:
        found = self._asset()
        if found is None:
            self.send_error(HTTPStatus.NOT_FOUND, "Asset not found")
            return
        payload, content_type = found
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if include_body:
            self.wfile.write(payload)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._send_asset(include_body=True)

    def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._send_asset(include_body=False)

    def log_message(self, format: str, *args: object) -> None:
        """Keep output concise while retaining useful request information."""
        print(f"[guessnova-web] {self.address_string()} - {format % args}")


def create_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Create a reusable IPv4/IPv6 web server instance for tests and embedding."""
    server_type = _IPv6ThreadingHTTPServer if ":" in host else ThreadingHTTPServer
    return server_type((host, port), GuessNovaWebHandler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="guessnova-web",
        description="Serve GuessNova's offline-first responsive web app.",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="Bind host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="TCP port (default: 8765)",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open the default browser",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the local cross-platform web interface until interrupted."""
    args = build_parser().parse_args(argv)
    if not 0 <= args.port <= 65535:
        raise SystemExit("--port must be between 0 and 65535")
    server = create_server(args.host, args.port)
    actual_host, actual_port = server.server_address[:2]
    display_host = _browser_host(str(actual_host))
    url = f"http://{display_host}:{actual_port}/"
    print(f"GuessNova web app: {url}")
    print("Press Ctrl+C to stop.")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping GuessNova web app.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
