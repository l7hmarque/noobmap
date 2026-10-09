# ADR-0003: Non-destructive / advisory-only tool

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (review of the `security-scan-and-fix` PRD)

## Context

The product's biggest risk is **fixing something and breaking the client's internet or devices**
(PRD Risks: High likelihood, High impact). The MVP is operated by a non-technical person, on the
client's production network (small business or home), with no guaranteed maintenance window.
Applying network configuration changes automatically is unrecoverable for this profile.

## Decision

The MVP is **non-destructive and advisory-only**: it **never applies** configuration changes to
the network, routers/firewalls, or devices. The output is always **step-by-step guidance** for a
human to execute. This implements **AC6**.

## Alternatives Considered

### Alternative 1: Apply fixes automatically (auto-remediation)
- **Pros**: convenience; immediate fixes with no manual work.
- **Cons**: very high risk of taking down the network/devices; requires admin credentials,
  rollback, and a maintenance window; mistakes are irreversible for a non-technical person.
- **Why not**: violates **AC6**, amplifies the PRD's biggest risk, and is out of scope
  ("Automatic remediation applied to the network — the MVP only advises, it does not apply changes").

### Alternative 2: Active exploitation tool (Metasploit etc.)
- **Pros**: validates the real exploitability of findings.
- **Cons**: intrusive, can cause downtime, larger legal and scope implications.
- **Why not**: explicitly **out of scope** ("high risk"); the MVP advises, it does not exploit.

## Consequences

### Positive
- Removes the main cause of client harm — the network stays intact by construction.
- Fits the business model: the provider advises and the client (or the provider) applies under control.
- Simplifies the product: no credentials, no rollback, no change transactions.

### Negative
- Protection only materializes if a human executes the fixes (depends on the checklist).
- No active exploitability validation — possible false positives to communicate.

### Risks
- **Risk**: a user may read a recommendation as an order and apply something incorrect.
  **Mitigation**: plain language, glossary, false-positive warning, and at most a **configuration
  backup** before any manual change — never automatic application.
