# ADR-0004: Self-contained offline HTML report (+ terminal summary)

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (review of the `security-scan-and-fix` PRD)

## Context

The operator runs Kali Live from a **USB stick**, with no persistence between boots. A report that
lives only in memory or in a volatile Live path **is lost on reboot** (a problem noted in **AC5**).
Also, the audience is **non-technical**, so the output must be human-readable, jargon-free, and
useful outside the terminal. The PRD (Technical Decisions) defines self-contained HTML + a terminal
summary.

## Decision

At the end of the scan, generate a **self-contained HTML file (single-file, offline, no server)** —
CSS/JS and data embedded — saved to a **persistent location (USB)**, accompanied by a **short
terminal summary**. This satisfies **AC3** (HTML with a plain-language summary, findings by severity,
and a terminal summary) and **AC5** (persistence across boots).

## Alternatives Considered

### Alternative 1: Terminal/text output only
- **Pros**: simple to produce; no dependencies.
- **Cons**: hard for a non-technical person to read and share; no visual severity grouping; not
  persistent unless saved.
- **Why not**: does not meet the readable, portable report requirement (**AC3**); terminal alone is
  not a client-deliverable artifact.

### Alternative 2: Hosted web report (server/backend)
- **Pros**: reachable by URL; centralization and history.
- **Cons**: requires a server and connectivity that don't exist in the field; depends on the client's
  network; reintroduces the web stack rejected in **ADR-0001**.
- **Why not**: incompatible with offline use on Kali Live; would only make sense in the multi-client
  panel (out of scope).

### Alternative 3: PDF generated locally
- **Pros**: portable and printable format.
- **Cons**: rigid typography/pagination; poorer navigation and severity highlighting; dependency on
  a PDF library.
- **Why not**: the single-file HTML already opens in any browser (no install), is more flexible, and
  can be printed/to PDF by the browser when needed.

## Consequences

### Positive
- **Persistence**: the file written to USB survives a Kali Live reboot (**AC5**).
- **Readability**: a layout with a simple summary and findings by severity suits non-experts (**AC3**).
- **Portable/offline**: opens in any browser with no internet and no install (**AC3**).

### Negative
- Manual HTML generation (templating) and care with escaping/UTF-8 encoding.
- The user must choose/remember the persistent USB path for the file.

### Risks
- **Risk**: saving to a volatile path and losing the report on reboot.
  **Mitigation**: default to the persistent/USB device with explicit path confirmation.
