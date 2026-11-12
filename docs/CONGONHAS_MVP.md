# Congonhas — MVP testável (SBSP/CGH)

## O que funciona

Painel com filtro de partidas/chegadas, pesquisa por voo ou rota, indicadores e listagem. API Python com biblioteca padrão, endpoints de saúde, fontes e voos. Importação **manual** validada por JSON, em memória, com fonte e horário de importação. Demonstração sintética. Testes automatizados executados no CI.

## Como executar sem baixar nada

No GitHub, abra o repositório em **Code > Codespaces > Create codespace on main**. No terminal da Codespace execute:

```bash
python3 -m unittest discover -s tests -v
python3 -m app.server
```

Abra a porta **8000** no painel **Ports** do Codespaces, mantendo-a **Private**. Use **Open in Browser** para visualizar o painel. O serviço escuta apenas `127.0.0.1` e não deve ser exposto publicamente; em Codespaces, dependendo do encaminhamento, o acesso pela aba Ports poderá exigir ajuste de binding após autenticação/rede segura. Para experimentação fora da Codespace, o navegador pode abrir `http://127.0.0.1:8000` quando executado num ambiente local.

## API

- `GET /health` — status e indicação de conector oficial indisponível.
- `GET /api/v1/sources` — origem demonstrativa, importação manual, Aena (não conectado).
- `GET /api/v1/flights?mode=demo&direction=departure&q=ABC` — consultas; `mode=manual` exibe dados importados.
- `POST /api/v1/manual-import` — JSON: `{"flight_date":"2026-11-11","flights":[{"flight_number":"ABC1234","direction":"departure","scheduled_local":"08:20","estimated_local":"08:35","route":"Exemplo","status":"Previsto","terminal":"T1"}]}`.

A importação substitui o conjunto manual anterior na memória do processo. Não persiste após reinício. Limite: 1.000 linhas e 128 KB por requisição.

## Segurança e proveniência

O MVP não tem autenticação, persistência, autorização de multiusuário ou integração real com a Aena; **nunca exponha o servidor publicamente**, ainda que a porta 8000 possa ser encaminhada por um ambiente de desenvolvimento. Use ambiente privado. Não confunda importação manual com verificação oficial. A origem e o campo `is_realtime=false` são sempre explícitos. Nenhum endpoint ou scraping não documentado é chamado.

## Próximas entregas

1. Confirmar acesso autorizado a API/feed Aena e semântica real dos campos.
2. Adapter versionado e fixtures autorizadas.
3. Base PostgreSQL, operação por dia e logs de coleta.
4. Conciliação RPL com observação pública, registrando ambiguidades.
5. Deploy autenticado/seguro para testadores externos.
