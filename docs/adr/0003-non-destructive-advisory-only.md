# ADR-0003: Ferramenta não destrutiva / apenas orientativa

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (revisão do PRD `security-scan-and-fix`)

## Context

O maior risco do produto é **corrigir e quebrar a internet ou os dispositivos do cliente**
(PRD Risks: probabilidade Alta, impacto Alto). O MVP é operado por um leigo, em rede de produção
do cliente (pequeno comércio ou residência), sem janela de manutenção garantida. Aplicar mudanças
automaticamente de configuração de rede é irrecuperável para esse perfil.

## Decision

O MVP é **não destrutivo e apenas orientativo (advisory-only)**: ele **nunca aplica** mudanças de
configuração na rede, em roteadores/firewalls ou em dispositivos. O resultado é sempre **orientação
passo a passo** para um humano executar. Isso implementa **AC6**.

## Alternatives Considered

### Alternative 1: Aplicar correções automaticamente (auto-remediation)
- **Pros**: conveniência; correção imediata sem trabalho manual.
- **Cons**: risco altíssimo de derrubar a rede/dispositivos; requer credenciais de admin, rollback e
  janela de manutenção; erros são irreversíveis para um leigo.
- **Why not**: viola **AC6**, amplifica o maior risco do PRD e está fora de escopo
  ("Correção automática aplicada na rede — o MVP só orienta, não executa mudanças").

### Alternative 2: Ferramenta de exploração ativa (Metasploit etc.)
- **Pros**: valida a explorabilidade real dos achados.
- **Cons**: intrusivo, pode causar indisponibilidade, implicações legais e de escopo maiores.
- **Why not**: explicitamente **fora de escopo** ("risco alto"); o MVP orienta, não explora.

## Consequences

### Positive
- Elimina a principal causa de dano ao cliente — a rede permanece intacta por construção.
- Alinha com o modelo de negócio: o prestador orienta e o cliente/ele aplica sob controle.
- Simplifica o produto: sem credenciais, sem rollback, sem transações de mudança.

### Negative
- A proteção só se concretiza se o humano executar as correções (depende do checklist).
- Sem validação ativa de explorabilidade — possíveis falsos positivos a comunicar.

### Risks
- **Risco**: usuário pode interpretar uma recomendação como ordem e aplicar algo incorreto.
  **Mitigação**: linguagem simples, glossário, aviso de falso-positivo e, no máximo, **backup da
  configuração** antes de qualquer mudança manual — nunca aplicação automática.
