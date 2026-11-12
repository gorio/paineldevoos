import os
import tempfile
import unittest
from unittest.mock import patch

from app.aena_csv import parse_aena_csv
from app.core import InvalidFlight
from app.storage import load_import, save_import
from app.server import snapshot

CSV = ("flight_number,direction,scheduled_local,estimated_local,route,status,terminal\n"
       "GLO1234,departure,10:15,10:45,Brasilia,Atrasado,T1\n"
       "TAM5678,arrival,11:20,,Rio de Janeiro,Previsto,T1\n")

class AenaCsvTests(unittest.TestCase):
    def test_parse(self):
        result = parse_aena_csv(CSV, "2026-11-11")
        self.assertEqual(len(result["flights"]), 2)
        self.assertEqual(result["flights"][0]["estimated_local"], "10:45")
        self.assertIsNone(result["flights"][1]["estimated_local"])

    def test_unexpected_header(self):
        with self.assertRaises(InvalidFlight):
            parse_aena_csv("flight,scheduled\na,10:00\n", "2026-11-11")

    def test_invalid_date(self):
        with self.assertRaises(InvalidFlight):
            parse_aena_csv(CSV, "2026-13-01")

    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"PAINEL_DB_PATH": os.path.join(tmp, "db.sqlite3")}):
                payload = parse_aena_csv(CSV, "2026-11-11")
                save_import(payload, "2026-11-11T22:00:00+00:00", "aena_manual_csv")
                loaded = load_import()
                self.assertEqual(loaded[0], payload)
                self.assertEqual(loaded[2], "aena_manual_csv")
                result = snapshot("manual")
                self.assertEqual(result["count"], 2)
                self.assertFalse(result["is_realtime"])
                self.assertEqual(result["flights"][0]["source"]["id"], "aena_manual_csv")

if __name__ == "__main__":
    unittest.main()
