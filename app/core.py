"""Congonhas MVP: explicit demo/manual observations, no automatic official fetch."""
from datetime import datetime, timezone
import re

SOURCE_URL = "https://www.aenabrasil.com.br/pt/aeroportos/aeroporto-de-congonhas/informacoes-de-voos.html"
ALLOWED_TYPES = {"departure", "arrival"}
ALLOWED_FIELDS = {"flight_number", "direction", "scheduled_local", "estimated_local", "route", "status", "terminal"}
FLIGHT_RE = re.compile(r"^[A-Z0-9]{2,4}[0-9]{1,5}[A-Z]?$")
TIME_RE = re.compile(r"^([01][0-9]|2[0-3]):[0-5][0-9]$")


class InvalidFlight(ValueError):
    pass


def normalize_flight(raw):
    if not isinstance(raw, dict):
        raise InvalidFlight("Cada voo deve ser um objeto JSON.")
    unknown = set(raw) - ALLOWED_FIELDS
    if unknown:
        raise InvalidFlight("Campos desconhecidos: " + ", ".join(sorted(unknown)))
    number = str(raw.get("flight_number", "")).upper().replace(" ", "").strip()
    if not FLIGHT_RE.fullmatch(number):
        raise InvalidFlight("flight_number inválido.")
    direction = raw.get("direction")
    if direction not in ALLOWED_TYPES:
        raise InvalidFlight("direction deve ser departure ou arrival.")
    scheduled = raw.get("scheduled_local")
    if not isinstance(scheduled, str) or not TIME_RE.fullmatch(scheduled):
        raise InvalidFlight("scheduled_local deve estar no formato HH:MM.")
    estimated = raw.get("estimated_local")
    if estimated not in (None, "") and (not isinstance(estimated, str) or not TIME_RE.fullmatch(estimated)):
        raise InvalidFlight("estimated_local deve estar no formato HH:MM ou vazio.")
    result = {"flight_number": number, "direction": direction, "scheduled_local": scheduled, "estimated_local": estimated or None}
    for key in ("route", "status", "terminal"):
        value = raw.get(key, "")
        if not isinstance(value, str) or len(value) > 160:
            raise InvalidFlight(key + " deve ser texto de até 160 caracteres.")
        result[key] = value.strip()
    return result


def normalize_payload(payload):
    if not isinstance(payload, dict) or set(payload) != {"flight_date", "flights"}:
        raise InvalidFlight("Esperado objeto com flight_date e flights.")
    date_str = payload["flight_date"]
    try:
        if not isinstance(date_str, str):
            raise ValueError
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.strftime("%Y-%m-%d") != date_str:
            raise ValueError
    except ValueError as exc:
        raise InvalidFlight("flight_date deve ser AAAA-MM-DD válido.") from exc
    flights = payload["flights"]
    if not isinstance(flights, list) or len(flights) > 1000:
        raise InvalidFlight("flights deve ser lista com até 1000 voos.")
    normalized = [normalize_flight(item) for item in flights]
    return {"flight_date": date_str, "flights": normalized}


def demo_payload():
    """Fictitious samples, not copied or inferred from actual flights."""
    return {"flight_date": "2026-11-11", "flights": [
        {"flight_number": "ABC1234", "direction": "departure", "scheduled_local": "08:20", "estimated_local": "08:35", "route": "Brasília (exemplo)", "status": "Exemplo: Atrasado", "terminal": "T1"},
        {"flight_number": "XYZ5678", "direction": "arrival", "scheduled_local": "09:10", "estimated_local": "09:10", "route": "Rio de Janeiro (exemplo)", "status": "Exemplo: Previsto", "terminal": "T1"},
        {"flight_number": "TST9012", "direction": "departure", "scheduled_local": "10:40", "estimated_local": None, "route": "Belo Horizonte (exemplo)", "status": "Exemplo: Confirmado", "terminal": "T1"},
    ]}


def flight_record(flight, flight_date, data_mode, collected_at):
    return {**flight, "airport_icao": "SBSP", "airport_iata": "CGH",
            "flight_date": flight_date, "timezone": "America/Sao_Paulo",
            "source": {"id": "synthetic_demo" if data_mode == "demo" else "manual_transcription",
                       "name": "Dados sintéticos" if data_mode == "demo" else "Transcrição manual (não verificada)",
                       "official_url": SOURCE_URL, "collected_at_utc": collected_at},
            "is_realtime": False, "data_mode": data_mode}


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
