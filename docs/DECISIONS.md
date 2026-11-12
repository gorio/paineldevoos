# Registro de decisões (ADRs)

## ADR-0001 — Rastreabilidade e separação entre previsão e observação

**Estado:** proposta, sujeita à revisão de colaboradores.

Cada informação de voo deve conservar fonte, ID externo, momento da coleta, horário que descreve e classe semântica: planejado, publicado, estimado, observado ou confirmado. Não colapsar conflitos em uma verdade artificial.

**Consequências:** armazenamento de observações imutáveis quando viável, reconciliador explícito e interface exibindo diferenças.

## ADR-0002 — Publicação da base histórica

**Estado:** pendente.

O HTML e os dados RPL históricos não serão incluídos automaticamente no repositório público sem revisão dos direitos de uso, redistribuição e remoção de eventuais dados sensíveis. Para testes colaborativos, usar fixtures sintéticas.
