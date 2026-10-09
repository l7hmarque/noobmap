# ADR-0002: Nmap as the scanning engine (not a custom scanner)

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (review of the `security-scan-and-fix` PRD)

## Context

The product must discover hosts, ports, and services on a **small network (≤254 hosts)** and turn
that into findings a non-technical person can understand. Re-implementing network discovery is
risky, and the target environment (**Kali Live**) already ships consolidated scanning tools. The
PRD (Technical Decisions) defines **Nmap** as the engine.

## Decision

Use **Nmap**, already present on Kali Live, as the scanning engine, invoked by the script. The
script only orchestrates Nmap and interprets its output — it does no network discovery of its own.

## Alternatives Considered

### Alternative 1: Custom scanner (sockets / raw packets)
- **Pros**: full control over output format; zero external dependency.
- **Cons**: reinventing the wheel; risk of bugs, false negatives/positives, and invalid findings;
  high maintenance and validation cost.
- **Why not**: Nmap is the de facto standard, tested for decades, and already on Kali —
  reimplementing adds no value and increases the risk of an incorrect report for the client.

### Alternative 2: Another tool (masscan, zmap, nbtscan)
- **Pros**: masscan/zmap are very fast at large scale.
- **Cons**: optimized for scale/speed and potentially aggressive — risk of degrading the client's
  network; less suited to a small network; weaker service/version detection.
- **Why not**: the target is a small network and a non-technical operator; Nmap balances discovery,
  ports, and services at a controllable pace, and ships preinstalled.

## Consequences

### Positive
- Reliable, recognized detection (hosts, ports, services/versions) for ≤254 hosts.
- Zero additional installation — aligns with AC2 (runs on Kali Live with no setup).
- Broad community and docs reduce maintenance effort.

### Negative
- Dependency on Nmap and its version present on Kali Live.
- Requires stable parsing of the output (e.g., XML) to feed the report.

### Risks
- **Risk**: an aggressive scan can impact the network/devices.
  **Mitigation**: use conservative profiles/timing by default and never enable exploitation (out of
  scope), reinforcing **ADR-0003 (non-destructive)**.
