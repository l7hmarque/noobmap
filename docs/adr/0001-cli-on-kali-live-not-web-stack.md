# ADR-0001: Platform is a CLI on Kali Live, not a web stack (Next.js + Postgres + Docker)

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (review of the `security-scan-and-fix` PRD)

## Context

The NULL template defaults to the web stack **Next.js + Postgres + Docker → GitHub → Coolify**.
The product, however, is operated by a **non-technical** independent provider, in the field,
booting **Kali Live via USB (no install)** on the client's network. There is no server, no
guaranteed internet, and no technical operator to host a web application. The PRD (Technical
Decisions) already states the web stack "**does not apply to the MVP**".

## Decision

The MVP is a **script/CLI that runs directly on the existing Kali Live**, triggered by a single
command. There is no database, container, or backend. The Next.js + Postgres + Docker stack is
**not used**.

## Alternatives Considered

### Alternative 1: Web stack (Next.js + Postgres + Docker, as in the template)
- **Pros**: rich UI, multi-user, centralized history, dashboard, deploy via Coolify.
- **Cons**: requires hosting and connectivity; a persistent server to maintain; incompatible with
  offline USB boot and a non-technical operator.
- **Why not**: no MVP requirement needs a server; it adds cost, attack surface, and complexity
  without delivering value for the use case.

### Alternative 2: CLI installed on a fixed OS (not Live)
- **Pros**: persistent tools and data; easier updates.
- **Cons**: requires installation and a dedicated machine the operator does not have.
- **Why not**: Kali Live is already the real usage environment; duplicating setup solves nothing.

## Consequences

### Positive
- Runs **offline** from USB, no install — ready for field use.
- Minimal surface: no server, no database, no Docker — easier to understand and maintain.
- Consistent with **AC6 (non-destructive)**: no exposed services or endpoints.

### Negative
- No native persistence beyond the USB; the report must be saved explicitly (see ADR-0004).
- No centralized multi-client history or login.

### Risks
- **Risk**: if the product grows into a multi-client panel, the CLI alone is not enough.
  **Mitigation**: treat it as a scope change that triggers the reconsideration condition below.

## Condition for reconsideration

A web stack (Next.js + Postgres + Docker) will only be reconsidered if a **multi-client panel with
login and centralized history** becomes a requirement — explicitly **out of scope** for the MVP.
