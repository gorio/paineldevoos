# Roadmap

## M0 — Governança e fonte histórica

- [ ] Publicar documentação inicial e política de contribuições
- [ ] Deliberar licença do código, direitos dos dados e governança
- [ ] Identificar estrutura real do `RAW` do HTML fornecido
- [ ] Extrair importador RPL com amostra sintética e testes

## M1 — Núcleo de dados

- [ ] Criar schema PostgreSQL e migrações
- [ ] Modelar ocorrências por data e fusos IANA
- [ ] Implementar deduplicação e trilha de proveniência
- [ ] Criar reconciliação com casos ambíguos e testes
- [ ] API de consulta e filtros

## M2 — Aeroportos

- [ ] Inventário de fontes oficiais por aeroporto
- [ ] Prova de conceito de conectores SBSP, SBGR e SBKP, conforme acesso permitido
- [ ] Medir atraso, completude e divergências

## M3 — Rastreamento

- [ ] Validar produto e licença AirNav Radar/FR24
- [ ] Implementar provedor autorizado com segredos externos e rate limits
- [ ] Comparar dados de rastreamento com RPL e aeroportos

## M4 — Produto

- [ ] Frontend responsivo, filtros e linhas do tempo
- [ ] Monitoramento de qualidade/observabilidade
- [ ] Cobertura progressiva das capitais e aeroportos regionais
- [ ] Política de retenção, custos e documentação pública

Nenhuma API externa está conectada nesta etapa. Prioridade de execução: segurança, modelo e qualidade dos dados antes de prometer atualização em tempo real.
