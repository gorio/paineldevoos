# Arquitetura inicial

## Fluxo

```text
RPL/histórico ─────────────┐
Aeroportos oficiais ───────┤
AirNav Radar / FR24 ───────┼─> conectores -> observações brutas
Outras fontes autorizadas ─┘                     |
                                                 v
                                   normalização + auditoria
                                                 |
                                                 v
                                  conciliação / correspondência
                                                 |
                                                 v
                                   API REST + banco + painel
```

## Camadas

- **Conectores:** um adaptador por fonte, com autenticação, limites, datas e status próprios; nunca pressupor acesso livre.
- **Raw observations:** preservar o valor original da fonte, timestamp de coleta, identificador, payload controlado e versão do conector.
- **Normalização:** códigos ICAO/IATA, companhias, número do voo, registro, UTC, tipo de evento e status.
- **Reconciliação:** relacionar programação, publicação aeroportuária e observação por identidade + contexto temporal, mantendo candidatos ambíguos.
- **API:** fornecer previsão, operação observada, divergências e proveniência.
- **Frontend:** dashboards, filtros, atualização visível e indicadores de cobertura.

## Entidades propostas

`Airport`, `DataSource`, `FlightPlan`, `FlightInstance`, `FlightObservation`, `MatchCandidate`, `Discrepancy`, `IngestionRun`.

**Chave de voo:** número do voo isoladamente NÃO é identificador universal; combinar data operacional, origem, destino, horário e, quando disponível, identificadores adicionais. Codeshare pode gerar múltiplos números para a mesma operação.

## Persistência sugerida

PostgreSQL com migrações versionadas; índices por aeroporto + UTC, fonte + ID externo, e chaves de deduplicação. Armazenamento histórico separado de dados operacionais recentes. Tecnologia sujeita a decisão registrada em ADR.

## Garantias e limites

- UTC na persistência; exibição no fuso local; horário de verão histórico quando pertinente.
- Um registro RPL é intenção/planejamento, não comprovação de movimento.
- EOBT + EET produz estimativa de chegada, não horário real nem previsão operacional garantida.
- Não converter ausência de observação em cancelamento.
- Conflitos entre fontes são apresentados com rastreabilidade, sem sobrescrever automaticamente.
- A API deve sinalizar `last_updated_at`, `source`, `data_quality` e `is_realtime`.
