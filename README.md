# Painel de Voos

Projeto colaborativo de inteligência de voos no Brasil: comparação entre planos de voo (RPL), informações operacionais publicadas pelos aeroportos e observações de rastreamento autorizadas.

> **Status: planejamento e integração inicial.** Ainda não existe alimentação em tempo real nem validação automática das fontes. Um plano de voo não comprova decolagem, pouso ou operação efetiva.

## Objetivo

Criar uma visão confiável e auditável de voos previstos, estimados e observados nos principais aeroportos do Brasil, começando pelas capitais e expandindo para aeroportos regionais conforme houver fontes disponíveis e permissão de uso.

## Princípios

- Separar **planejado**, **publicado pelo aeroporto**, **observado no rastreador** e **confirmado**.
- Armazenar origem, horário da coleta, horário do evento e nível de confiança.
- Usar UTC internamente, exibindo o fuso horário local de cada aeroporto.
- Não inventar dados ausentes nem assumir que uma API pública/comercial pode ser redistribuída.
- Não versionar credenciais, tokens ou dumps de dados sem direitos de publicação.

## Como contribuir

Abra uma Issue descrevendo a melhoria desejada. Mudanças devem entrar por branches e Pull Requests; consulte `CONTRIBUTING.md` assim que a documentação inicial for integrada.

## Primeiro ciclo

1. Documentar fontes, nomenclaturas e arquitetura.
2. Extrair/normalizar o modelo de dados do HTML histórico, **sem publicar sua base integral até revisar os direitos**.
3. Implementar ingestão idempotente e conciliação de voos.
4. Integrar fontes oficiais de aeroportos e provedores de rastreamento conforme contratos e limites.
5. Publicar painel com indicação explícita da proveniência e atualização dos dados.

Projeto em desenvolvimento. Licença de código e condições de redistribuição dos dados serão avaliadas separadamente.
