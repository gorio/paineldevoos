# Fontes de dados e integrações

| Fonte | Finalidade | Estado inicial | Condição para ativar |
| --- | --- | --- | --- |
| HTML histórico / RPL | Planos programados, referência para importação | Disponível no material original, não publicado | Verificar direito de distribuição e extrair amostra autorizada |
| Painéis oficiais de aeroportos | Partidas/chegadas e status publicados | Não conectado | Identificar operador, fonte oficial, regras de acesso e estabilidade |
| AirNav Radar | Observações de rastreamento | Não conectado | Confirmar produto API, plano contratado, campos e redistribuição |
| Flightradar24 | Observações de rastreamento | Não conectado | Confirmar acesso permitido e condições da API |
| Informações meteorológicas | METAR/TAF quando disponibilizados legalmente | Não conectado | Identificar fonte confiável e licença |
| NOTAM e dados aeronáuticos | Contexto aeroportuário/aeronáutico | Não conectado | Validar origem oficial, uso apropriado e atualização |

## Prioridade geográfica

Fase 1: SBSP (Congonhas), SBGR (Guarulhos), SBKP (Viracopos) para testar padrões diferentes; em seguida aeroportos das capitais, por capacidade de cobertura e acesso às fontes. Expansão regional posterior.

## Checklist de um conector

- Proprietário e URL da fonte;
- Oficialidade e permissão de acesso;
- API/documentação e formato real;
- Autenticação/segredos;
- Rate limits, custos, cache e retenção;
- Horários e timezone;
- Campos de identificação e semântica do status;
- Intervalo de atualização e indisponibilidade;
- Direito de publicação, armazenamento e redistribuição;
- Dados de teste sintéticos/autorizados.

**Importante:** páginas de consulta de voo não equivalem a APIs abertas. Não presumir parceria, autorização ou atualização em tempo real.
