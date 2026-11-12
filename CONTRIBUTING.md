# Contribuindo com o Painel de Voos

Obrigado por colaborar. O projeto tem natureza técnica e requer rastreabilidade de dados.

## Fluxo de contribuição

1. Pesquise Issues abertas e descreva a proposta antes de implementar integrações grandes.
2. Crie uma branch curta (ex.: `feat/airport-sbsp`, `fix/flight-matching`).
3. Documente origem dos dados, URL/endpoints, autenticação, limites, fuso, campos e termos de uso.
4. Abra Pull Request com contexto, testes, evidências e impactos.
5. Nunca inclua tokens, credenciais, dados pessoais ou payloads de fornecedores sem autorização.

## Checklist de Pull Request

- [ ] Comportamento e escopo explicados
- [ ] Testes adicionados ou justificativa de ausência
- [ ] Dados de amostra sintéticos ou autorizados
- [ ] UTC e fusos tratados explicitamente
- [ ] Proveniência e atualização dos dados preservadas
- [ ] Falhas, limites e indisponibilidade da fonte tratados
- [ ] Sem afirmar que estimativas são fatos confirmados

## Convenções

Python para serviços de integração iniciais; contratos REST/JSON versionados. Padrão de código e framework do frontend serão decididos em uma ADR. Commits claros, PRs pequenos e revisão antes do merge. Não existe licença de código definida neste momento; evite copiar dependências ou conjuntos de dados com restrições.
