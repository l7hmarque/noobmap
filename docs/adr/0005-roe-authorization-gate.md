# ADR-0005: Gate obrigatório de autorização (RoE) via `--autorizado`

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (revisão do PRD `security-scan-and-fix`)

## Context

Escanear uma rede sem autorização é o maior risco de natureza **legal/ética** do produto
(PRD Risks: probabilidade Alta, impacto Alto). Mesmo que o cliente tenha contratado o serviço, é
preciso um **consentimento escrito** claro (Rules of Engagement) que delimite escopo e responsabilidade.
O operador é leigo, então a barreira deve ser explícita e impossível de ignorar por acidente.

## Decision

A autorização é um **gate obrigatório**: o script só inicia a varredura com a flag **`--autorizado`**,
que confirma a existência de um **termo de 1 página assinado/aceito por escrito**. Sem a flag, o
script **aborta sem escanear**. Isso implementa **AC1**; a flag registra **data/hora e nome do cliente**
(Open Question resolvida) para rastreabilidade.

## Alternatives Considered

### Alternative 1: Sem gate — confiar no bom senso / contrato verbal
- **Pros**: zero fricção para o operador.
- **Cons**: não deixa evidência; risco de varredura não autorizada; exposição legal/ética alta.
- **Why not**: viola **AC1** e deixa o maior risco do PRD sem mitigação.

### Alternative 2: Aviso interativo "tem certeza? (s/n)" apenas
- **Pros**: simples; alguma fricção.
- **Cons**: fácil de aceitar por reflexo; não exige um termo escrito; fraca rastreabilidade.
- **Why not**: consentimento clicado às pressas não equivale a autorização escrita; não evidencia
  escopo/ROE nem registra cliente.

### Alternative 3: Bloqueio total sem qualquer escape (hard gate sem flag)
- **Pros**: máxima segurança.
- **Cons**: inviável operacionalmente; o operador legitimamente autorizado precisa prosseguir.
- **Why not**: precisamos de um gate **auditável e explícito**, não de uma impossibilidade — a flag
  `--autorizado` + registro é o equilíbrio correto.

## Consequences

### Positive
- Impede varredura acidental sem autorização — aplica **AC1** de forma determinística.
- Gera trilha auditável (data/hora + nome do cliente) anexável ao termo assinado.
- Reduz exposição legal/ética do operador e do produto.

### Negative
- Adiciona um passo (obter/assinar o termo) antes de cada atendimento.
- Requer manter o modelo do termo de 1 página fora do código.

### Risks
- **Risco**: alguém contornar o gate ou reutilizar `--autorizado` indevidamente.
  **Mitigação**: exigir e registrar explicitamente os campos de autorização (data/hora + cliente) e
  documentar no termo que o consentimento é específico por cliente/atendimento.
