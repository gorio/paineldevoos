# Política de merge automatizado

## Quando o GitHub pode integrar sem intervenção manual

O workflow `Merge trusted PR after successful CI` é acionado quando o workflow `CI` termina com **sucesso** para um Pull Request. Ele só tenta o merge se:

- O PR estiver aberto, não for draft e mirar a branch `main`;
- O autor for o usuário `gorio`;
- O branch de origem pertencer ao mesmo repositório;
- O SHA que passou pelo CI corresponder exatamente ao SHA atual do PR;
- Nenhum arquivo sensível for alterado (`.github/workflows/`, `SECURITY.md`, `CODEOWNERS`);
- O GitHub permitir o merge segundo suas regras atuais, sem conflitos e sem bloqueios.

O merge usa **squash**. PRs externos e mudanças sensíveis continuam exigindo análise humana. Essa política **não concede bypass** de branch protection nem aprova revisões em nome de terceiros.

## Dependências

- GitHub Actions precisa estar habilitado.
- As permissões do `GITHUB_TOKEN` e eventuais regras de proteção devem permitir a operação.
- A execução real só pode ser considerada validada após um PR elegível passar pelo CI e ocorrer um merge.
- Se regras de proteção exigirem revisão, o merge permanece bloqueado; nunca ignorar proteções para contornar isso.

## Limites

Os testes atuais verificam apenas a estrutura inicial e uma declaração de status do README; com a entrada dos conectores e da API, serão necessárias suites reais de unidade, integração e regressão. **CI verde não comprova qualidade completa**, nem licença de dados, nem autorização de uso de APIs.
