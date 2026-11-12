import unittest
from app.core import InvalidFlight, demo_payload, flight_record, normalize_payload
from app.server import snapshot


class CongonhasTests(unittest.TestCase):
    def test_demo_explicitly_not_realtime(self):
        result = snapshot("demo")
        self.assertEqual(result["airport"], "SBSP")
        self.assertFalse(result["is_realtime"])
        self.assertGreater(result["count"], 0)
        self.assertTrue(all(f["source"]["id"] == "synthetic_demo" for f in result["flights"]))

    def test_filter_direction(self):
        self.assertTrue(all(f["direction"] == "arrival" for f in snapshot("demo", "arrival")["flights"]))

    def test_filter_search(self):
        self.assertEqual(snapshot("demo", search="ABC1234")["count"], 1)

    def test_empty_manual_source(self):
        self.assertEqual(snapshot("manual")["count"], 0)

    def test_payload_valid(self):
        p = {"flight_date": "2026-11-11", "flights": [demo_payload()["flights"][0]]}
        self.assertEqual(len(normalize_payload(p)["flights"]), 1)

    def test_reject_invalid_time(self):
        f = dict(demo_payload()["flights"][0], scheduled_local="25:90")
        with self.assertRaises(InvalidFlight):
            normalize_payload({"flight_date": "2026-11-11", "flights": [f]})

    def test_reject_unknown_field(self):
        f = dict(demo_payload()["flights"][0], unexpected="x")
        with self.assertRaises(InvalidFlight):
            normalize_payload({"flight_date": "2026-11-11", "flights": [f]})

    def test_reject_invalid_date(self):
        with self.assertRaises(InvalidFlight):
            normalize_payload({"flight_date": "2026-02-30", "flights": []})

    def test_reject_too_many_rows(self):
        with self.assertRaises(InvalidFlight):
            normalize_payload({"flight_date": "2026-11-11", "flights": demo_payload()["flights"] * 334})


if __name__ == "__main__":
    unittest.main()
