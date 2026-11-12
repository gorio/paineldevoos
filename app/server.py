"""Dependency-free local MVP. Run python3 -m app.server in GitHub Codespaces."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit
import json
import os

from .core import SOURCE_URL, InvalidFlight, demo_payload, flight_record, normalize_payload, now_utc
from .aena_csv import parse_aena_csv
from .storage import load_import, save_import

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
        stored = load_import() if mode == "manual" else None
        payload = demo_payload() if mode == "demo" else (stored[0] if stored else _manual)
        collected = None if mode == "demo" else (stored[1] if stored else _manual_collected)
        source_id = stored[2] if stored else "manual_transcription"
    if payload is None:
        return {"airport": "SBSP", "mode": mode, "is_realtime": False,
                "last_updated_at": None, "flight_date": None, "count": 0, "flights": []}
    records = [flight_record(f, payload["flight_date"], mode, collected) for f in payload["flights"]]
    if mode == "manual":
        for record in records:
            record["source"]["id"] = source_id
            if source_id == "aena_manual_csv":
                record["source"]["name"] = "Transcrição CSV manual (não verificada)"
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
                {"id": "aena_manual_csv", "status": "available", "is_realtime": False},
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
        path = urlsplit(self.path).path
        if path not in ("/api/v1/manual-import", "/api/v1/aena-csv"):
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
            posted = json.loads(self.rfile.read(length))
            if path == "/api/v1/aena-csv":
                if not isinstance(posted, dict) or set(posted) != {"flight_date", "csv"}:
                    raise InvalidFlight("Enviar flight_date e csv.")
                payload = parse_aena_csv(posted["csv"], posted["flight_date"])
            else:
                payload = normalize_payload(posted)
        except (UnicodeDecodeError, json.JSONDecodeError, InvalidFlight) as exc:
            return self.send_json(400, {"error": str(exc)})
        timestamp = now_utc()
        source_id = "aena_manual_csv" if path == "/api/v1/aena-csv" else "manual_transcription"
        save_import(payload, timestamp, source_id)
        with _state_lock:
            _manual = payload
            _manual_collected = timestamp
        return self.send_json(200, {"imported": len(payload["flights"]), "mode": "manual",
                                    "source_id": source_id,
                                    "last_updated_at": timestamp, "is_realtime": False})

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
