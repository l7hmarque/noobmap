# ADR-0005: Mandatory authorization (RoE) gate via `--autorizado`

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (review of the `security-scan-and-fix` PRD)

## Context

Scanning a network without authorization is the product's biggest **legal/ethical** risk (PRD Risks:
High likelihood, High impact). Even if the client hired the service, a clear **written consent**
(Rules of Engagement) is needed, delimiting scope and responsibility. The operator is non-technical,
so the barrier must be explicit and impossible to skip by accident.

## Decision

Authorization is a **mandatory gate**: the script only starts the scan with the **`--autorizado`**
flag, which confirms a **one-page term signed/accepted in writing** exists. Without the flag, the
script **aborts without scanning**. This implements **AC1**; the flag records **date/time and client
name** for traceability.

## Alternatives Considered

### Alternative 1: No gate — rely on common sense / verbal contract
- **Pros**: zero friction for the operator.
- **Cons**: leaves no evidence; risk of unauthorized scanning; high legal/ethical exposure.
- **Why not**: violates **AC1** and leaves the PRD's biggest risk unmitigated.

### Alternative 2: Interactive "are you sure? (y/n)" prompt only
- **Pros**: simple; some friction.
- **Cons**: easy to accept reflexively; no written term required; weak traceability.
- **Why not**: a rushed click is not written authorization; it does not evidence scope/RoE nor record
  the client.

### Alternative 3: Hard gate with no escape (no flag)
- **Pros**: maximum safety.
- **Cons**: operationally unworkable; the legitimately authorized operator must proceed.
- **Why not**: we need an **auditable and explicit** gate, not an impossibility — the `--autorizado`
  flag + record is the right balance.

## Consequences

### Positive
- Prevents accidental scanning without authorization — applies **AC1** deterministically.
- Produces an auditable trail (date/time + client name) attachable to the signed term.
- Reduces the operator's and the product's legal/ethical exposure.

### Negative
- Adds a step (obtaining/signing the term) before each engagement.
- Requires keeping the one-page term template out of the code.

### Risks
- **Risk**: someone bypasses the gate or misuses `--autorizado`.
  **Mitigation**: require and explicitly record the authorization fields (date/time + client) and
  document in the term that consent is specific per client/engagement.
