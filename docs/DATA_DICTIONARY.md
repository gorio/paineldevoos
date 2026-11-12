# Contratos mínimos de dados (proposta v0)

## Airport

`icao` (string, 4), `iata` (string, opcional), `name`, `timezone` (IANA), `city`, `country`.

## DataSource

`source_id`, `name`, `kind` (rpl|airport|tracking|weather|other), `provider`, `access_status` (planned|approved|disabled|active|error), `license_reference`, `last_success_at`.

## FlightPlan

`id`, `source_id`, `flight_number`, `origin_icao`, `destination_icao`, `scheduled_departure_utc`, `estimated_elapsed_minutes`, `validity_start`, `validity_end`, `days_of_operation`, `aircraft_type` e `source_record_id`.

## FlightObservation

`observation_id`, `source_id`, `source_record_id`, `flight_number`, `origin_icao`, `destination_icao`, `event_kind`, `event_time_utc`, `observed_at_utc`, `source_status`, `registration`, `payload_hash`.

`event_kind`: `scheduled_departure`, `estimated_departure`, `actual_departure`, `scheduled_arrival`, `estimated_arrival`, `actual_arrival`, `position`, `status`.

## MatchCandidate

`flight_instance_id`, `observation_id`, `score` (0..1), `signals` (object), `decision` (matched|possible|rejected|manual_review), `matched_at_utc`.

## API

`GET /health`, `GET /api/v1/sources`, `GET /api/v1/flights` são contratos planejados, ainda não conectados a dados externos. A resposta deve distinguir `realtime=false` e ausências de dados.

As estruturas ainda não são schema SQL final e passarão por ADR/revisão.
