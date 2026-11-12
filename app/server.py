"""Dependency-free local MVP. Run python3 -m app.server in GitHub Codespaces."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit
import json
import os

from .core import SOURCE_URL, InvalidFlight, demo_payload, flight_record, normalize_payload, now_utc

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
MAX_REQUEST = 128_000
_state_lock = Lock()
_manual = None
_manual_collected = None


def snapshot(mode="demo", direction=None, search=""):
    global _manual
    if mode not in ("demo", "manual"):
        raise InvalidFlight("mode deve ser demo ou manual.")
    with _state_lock:
        payload = demo_payload() if mode == "demo" else _manual
        collected = None if mode == "demo" else _manual_collected
    if payload is None:
        return {"airport": "SBSP", "mode": mode, "is_realtime": False,
                "last_updated_at": None, "flight_date": None, "count": 0, "flights": []}
    records = [flight_record(f, payload["flight_date"], mode, collected) for f in payload["flights"]]
    if direction:
        if direction not in ("departure", "arrival"):
            raise InvalidFlight("direction inválida.")
        records = [f for f in records if f["direction"] == direction]
    if search:
        needle = search.upper()[:50]
        records = [f for f in records if needle in f["flight_number"] or needle in f["route"].upper()]
    return {"airport": "SBSP", "mode": mode, "is_realtime": False,
            "last_updated_at": collected, "flight_date": payload["flight_date"],
            "count": len(records), "flights": records}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        blob = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def do_GET(self):
        from urllib.parse import parse_qs
        parsed = urlsplit(self.path)
        if parsed.path == "/health":
            return self.send_json(200, {"status": "ok", "airport": "SBSP", "is_realtime": False, "official_connector": "not_configured"})
        if parsed.path == "/api/v1/sources":
            return self.send_json(200, {"sources": [
                {"id": "synthetic_demo", "status": "available", "is_realtime": False},
                {"id": "manual_transcription", "status": "available", "is_realtime": False},
                {"id": "aena_sbsp", "status": "not_connected", "url": SOURCE_URL, "is_realtime": False}]})
        if parsed.path == "/api/v1/flights":
            q = parse_qs(parsed.query)
            try:
                return self.send_json(200, snapshot(q.get("mode", ["demo"])[0],
                                                    q.get("direction", [None])[0],
                                                    q.get("q", [""])[0]))
            except InvalidFlight as exc:
                return self.send_json(400, {"error": str(exc)})
        if parsed.path in ("/", "/index.html"):
            blob = (WEB / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(blob)))
            self.end_headers()
            return self.wfile.write(blob)
        if parsed.path == "/app.js":
            blob = (WEB / "app.js").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Length", str(len(blob)))
            self.end_headers()
            return self.wfile.write(blob)
        return self.send_json(404, {"error": "not found"})

    def do_POST(self):
        global _manual, _manual_collected
        if urlsplit(self.path).path != "/api/v1/manual-import":
            return self.send_json(404, {"error": "not found"})
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self.send_json(415, {"error": "Content-Type deve ser application/json"})
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            return self.send_json(400, {"error": "Content-Length inválido"})
        if length < 0 or length > MAX_REQUEST:
            return self.send_json(413, {"error": "Corpo excede limite ou não informado"})
        try:
            payload = normalize_payload(json.loads(self.rfile.read(length)))
        except (UnicodeDecodeError, json.JSONDecodeError, InvalidFlight) as exc:
            return self.send_json(400, {"error": str(exc)})
        with _state_lock:
            _manual = payload
            _manual_collected = now_utc()
        return self.send_json(200, {"imported": len(payload["flights"]), "mode": "manual",
                                    "last_updated_at": _manual_collected, "is_realtime": False})

    def log_message(self, format, *args):
        pass


def main():
    port = int(os.environ.get("PORT", "8000"))
    # Deliberately loopback-only. This MVP has no authentication and MUST NOT be
    # exposed directly to the public internet. Codespaces must keep port private.
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Painel Congonhas MVP: http://127.0.0.1:{port} (somente local; não é tempo real)", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
