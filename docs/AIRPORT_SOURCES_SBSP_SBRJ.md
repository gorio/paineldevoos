# Inventário verificado de portais aeroportuários — SBSP e SBRJ

Consulta realizada em 2026-11-11. O inventário documenta o conteúdo público visível dos portais; **não indica acesso a API, permissão de scraping nem ingestão em funcionamento**.

## SBSP — Congonhas / Aena Brasil

- Aeroporto: São Paulo/Congonhas — Deputado Freitas Nobre
- ICAO: `SBSP`; IATA: `CGH`
- Operador da página: Aena Brasil
- URL informada: https://www.aenabrasil.com.br/pt/aeroportos/aeroporto-de-congonhas/informacoes-de-voos.html
- Estado: portal público consultável; integração automática **não implementada**
- Inspeção textual: formulário com pesquisa por partida/chegada, aeroporto, data ou intervalo, horário, número do voo/companhia. Cabeçalhos visíveis incluem hora, voo, destino, origem, terminal e estimado.
- Ressalva: a consulta textual não confirmou endpoint de API, condições de licenciamento, atualização/refresh, mapeamento dos dados ou semântica completa dos status. Esses pontos exigem avaliação técnica e autorização conforme termos.

## SBRJ — Santos Dumont / Infraero

- Aeroporto: Santos Dumont (Rio de Janeiro)
- ICAO: `SBRJ`; IATA: `SDU`
- URL fornecida originalmente: https://voos.infraero.gov.br/voos/index_2.aspx
- Resultado da verificação: tentativa de abrir a URL acima apresentou ciclo de redirecionamento na ferramenta de consulta. **Isso não prova indisponibilidade no navegador do usuário**.
- Portal Infraero alternativo identificado: https://voosonlinecore.infraero.gov.br/
- Estado: consulta pública disponível; integração automática **não implementada**
- Campos visíveis: companhia aérea, número do voo, origem, data, previsto, confirmado, escalas, status e detalhes. A interface distingue chegadas e partidas, com filtros por aeroporto, companhia, número do voo e data.
- Nota de origem publicada pelo portal: informações exibidas são fornecidas diretamente pelas companhias aéreas; erros e omissões podem ocorrer.
- Ressalva: `confirmado` é o **nome do campo exibido**. Não inferir que o valor corresponde a pouso/decolagem reais sem observar a semântica de cada status. Não confundir horário publicado pela Infraero com telemetria de rastreador.

## Modelo de comparação proposto

| Campo normalizado | RPL | Aena SBSP | Infraero SBRJ |
| --- | --- | --- | --- |
| aeroporto | origem/destino | contexto da consulta | contexto da consulta |
| voo/companhia | conforme plano | campo visível | campos visíveis |
| data e horário programados | EOBT (UTC) | hora / data da consulta | previsto |
| horário estimado | EOBT+EET apenas para chegada estimada calculada | estimado (rótulo da página) | não assumir correspondência |
| horário confirmado/publicado | não disponível | a verificar | confirmado (rótulo da página) |
| status | não representa operação real | a verificar | status publicado |
| terminal/esteira | não disponível em RPL | terminal | detalhes, quando houver |

As colunas indicam **possibilidades de mapeamento**, não conexões implementadas. Datas/horários precisam de timezone explícito (São Paulo e Rio de Janeiro usam `America/Sao_Paulo` no presente) e da data operacional do voo. Manter valor bruto e proveniência antes de normalizar.

## Implementação segura por fases

1. Confirmar termos de uso, permissão de acesso, endpoint documentado (se houver), limites e exigências de atribuição para cada portal.
2. Criar interface do conector independente da tecnologia do fornecedor: `fetch`, `parse`, `normalize`, `health` e reporte de falhas.
3. Implementar fixtures **sintéticas** para chegada, partida, atraso, cancelamento, voo sem horário confirmado e codeshare.
4. Validar manualmente campos, timezone e status contra uma amostra consentida/autorizada.
5. Ativar coleta apenas dentro dos termos permitidos; salvar timestamp da coleta e atualização da fonte.
6. Comparar com RPL e, depois, com rastreamento autorizado, sem eleger uma fonte como verdade absoluta.

## Fontes consultadas

- Aena Brasil: https://www.aenabrasil.com.br/pt/aeroportos/aeroporto-de-congonhas/informacoes-de-voos.html
- Infraero (URL informada): https://voos.infraero.gov.br/voos/index_2.aspx
- Infraero (portal alternativo observado): https://voosonlinecore.infraero.gov.br/
