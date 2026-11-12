"""Parse CSV manually transcribed from the official Aena flight-information page.

This module DOES NOT fetch, scrape, or access Aena services.
Input uses explicit header names and a selected operation date; rows are not verified.
"""
import csv
import io
from .core import InvalidFlight, normalize_payload

HEADERS = {"flight_number", "direction", "scheduled_local", "estimated_local", "route", "status", "terminal"}
MAX_CSV = 128_000

def parse_aena_csv(csv_text, flight_date):
    if not isinstance(csv_text, str) or len(csv_text.encode("utf-8")) > MAX_CSV:
        raise InvalidFlight("CSV deve ser texto de até 128 KB.")
    try:
        reader = csv.DictReader(io.StringIO(csv_text, newline=""))
        if reader.fieldnames is None or set(reader.fieldnames) != HEADERS:
            raise InvalidFlight("Colunas CSV obrigatórias: " + ", ".join(sorted(HEADERS)))
        flights = []
        for index, row in enumerate(reader, 2):
            if index > 1001:
                raise InvalidFlight("Limite de 1000 linhas excedido.")
            if None in row:
                raise InvalidFlight(f"Linha {index}: colunas extras.")
            flights.append({k: (v or "").strip() for k, v in row.items()})
    except csv.Error as exc:
        raise InvalidFlight("CSV inválido.") from exc
    if not flights:
        raise InvalidFlight("CSV sem voos.")
    return normalize_payload({"flight_date": flight_date, "flights": flights})
