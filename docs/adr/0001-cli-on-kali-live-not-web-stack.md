# ADR-0001: Plataforma é um CLI no Kali Live, não uma stack web (Next.js + Postgres + Docker)

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (revisão do PRD `security-scan-and-fix`)

## Context

O template NULL sugere, por padrão, o stack web **Next.js + Postgres + Docker → GitHub → Coolify**.
O produto, porém, é operado por um prestador autônomo **leigo**, em campo, inicializando o
**Kali Live via USB (sem instalação)** na rede do cliente. Não há servidor, internet garantida
ou operador técnico para hospedar uma aplicação web. O PRD (Technical Decisions, linha 40)
já determina que o stack web "**não se aplica ao MVP**".

## Decision

O MVP é um **script/CLI executado diretamente no Kali Live já existente**, disparado a partir de
um único comando. Não há banco de dados, container ou backend. O stack Next.js + Postgres + Docker
**não é usado**.

## Alternatives Considered

### Alternative 1: Stack web (Next.js + Postgres + Docker, como no template)
- **Pros**: UI rica, multiusuário, histórico centralizado, dashboard, deploy via Coolify.
- **Cons**: exige instalação/hospedagem e conexão; servidor persistente a manter; incompatível com
  boot via USB offline e com um operador leigo.
- **Why not**: nenhum requisito do MVP precisa de servidor; adiciona custo, superfície de ataque e
  complexidade sem entregar valor ao caso de uso.

### Alternative 2: CLI instalado em sistema operacional fixo (não Live)
- **Pros**: ferramentas e dados persistentes; atualizações mais fáceis.
- **Cons**: exige instalação e uma máquina dedicada, que o operador não possui.
- **Why not**: o Kali Live já é o ambiente real de uso (AC2); duplicar setup não resolve nada.

## Consequences

### Positive
- Roda **offline** no USB, sem instalação (**AC2**) — pronto para uso em campo.
- Superfície mínima: sem servidor, sem banco, sem Docker — mais fácil de entender e manter.
- Coerente com **AC6 (não destrutivo)**, pois não há serviços nem endpoints expostos.

### Negative
- Sem persistência nativa além do USB; o relatório precisa ser salvo explicitamente (ver ADR-0004).
- Sem histórico multi-cliente centralizado nem login.

### Risks
- **Risco**: se o produto evoluir para painel multi-cliente, o CLI sozinho não basta.
  **Mitigação**: tratar como mudança de escopo que aciona a condição de reconsideração abaixo.

## Condition for reconsideration

Uma stack web (Next.js + Postgres + Docker) só será reconsiderada se surgir a necessidade de um
**painel multi-cliente com login e histórico centralizado** — explicitamente **fora de escopo** no MVP.
