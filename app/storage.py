"""SQLite persistence for explicitly user-imported Congonhas records."""
import json
import os
from pathlib import Path
import sqlite3
from threading import Lock

from .core import normalize_payload

_lock = Lock()

def db_path():
    return Path(os.environ.get("PAINEL_DB_PATH", "data/painel.sqlite3"))

def save_import(payload, collected_at, source_id="manual_transcription"):
    payload = normalize_payload(payload)
    if source_id not in ("manual_transcription", "aena_manual_csv"):
        raise ValueError("Unsupported import source.")
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, sqlite3.connect(path, timeout=10) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS manual_imports (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            payload TEXT NOT NULL,
            collected_at TEXT NOT NULL,
            source_id TEXT NOT NULL
        )""")
        con.execute("""INSERT INTO manual_imports (id, payload, collected_at, source_id)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,
            collected_at=excluded.collected_at, source_id=excluded.source_id""",
            (json.dumps(payload, ensure_ascii=False), collected_at, source_id))

def load_import():
    path = db_path()
    if not path.is_file():
        return None
    with _lock, sqlite3.connect(path, timeout=10) as con:
        try:
            row = con.execute("SELECT payload,collected_at,source_id FROM manual_imports WHERE id=1").fetchone()
        except sqlite3.OperationalError:
            return None
    if not row:
        return None
    return normalize_payload(json.loads(row[0])), row[1], row[2]
