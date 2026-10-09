# ADR-0004: Relatório em HTML offline self-contained (+ resumo no terminal)

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (revisão do PRD `security-scan-and-fix`)

## Context

O operador roda o Kali Live a partir de um **pendrive/USB**, sem persistência entre boots
(PRD Risks e Open Questions). Um relatório que vive só na memória ou num caminho volátil do Live
**se perde no reboot** (problema apontado em **AC5**). Além disso, o público é **leigo**, então a
saída precisa ser legível por humano, sem jargão, e útil fora do terminal. O PRD (Technical
Decisions, linha 42) define HTML self-contained + resumo no terminal.

## Decision

Ao fim do scan, gerar um **arquivo HTML self-contained (single-file, offline, sem servidor)** —
CSS/JS e dados embutidos — salvo em **local persistente (USB)**, acompanhado de um **resumo curto no
terminal**. Isso atende **AC3** (arquivo HTML com resumo em linguagem simples, achados por severidade
e resumo no terminal) e **AC5** (persistência entre boots).

## Alternatives Considered

### Alternative 1: Saída somente em texto/terminal
- **Pros**: simples de produzir; sem dependências.
- **Cons**: difícil de ler e compartilhar para um leigo; não organiza achados por severidade de forma
  visual; não sobrevive ao reboot se não for salvo.
- **Why not**: não atende ao requisito de relatório legível e portátil (**AC3**); terminal sozinho não
  é um artefato entregável ao cliente.

### Alternative 2: Relatório web hospedado (servidor/backend)
- **Pros**: acessível por URL; centralização e histórico.
- **Cons**: exige servidor e conexão inexistentes em campo; dependente de rede do cliente; reintroduz
  a stack web rejeitada em **ADR-0001**.
- **Why not**: incompatível com uso offline no Kali Live; só faria sentido no painel multi-cliente
  (fora de escopo).

### Alternative 3: PDF gerado localmente
- **Pros**: formato portátil e imprimível.
- **Cons**: tipografia/paginação mais rígidas; navegação e destaque por severidade mais pobres;
  dependência de biblioteca de geração de PDF.
- **Why not**: o HTML single-file já abre em qualquer navegador (sem instalação), é mais flexível e
  pode ser impresso/PDF pelo próprio browser quando desejado.

## Consequences

### Positive
- **Persistência**: arquivo escrito no USB sobrevive ao reboot do Kali Live (**AC5**).
- **Legibilidade**: layout com resumo simples e achados por severidade atende ao leigo (**AC3**).
- **Portátil/offline**: abre em qualquer navegador sem internet nem instalação (**AC3**).

### Negative
- Geração manual de HTML (templating) e cuidado com escaping/encoding UTF-8 (pt-BR).
- O usuário precisa escolher/lembrar o caminho persistente do USB para o arquivo.

### Risks
- **Risco**: salvar em caminho volátil e perder o relatório no reboot.
  **Mitigação**: default para o dispositivo persistente/USB com confirmação explícita do caminho.
