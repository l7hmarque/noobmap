# Security Policy

## Responsible use

**noobmap** is a **defensive** tool for **authorized** use. It:
- accepts **private networks only** (`10.x`, `172.16–31.x`, `192.168.x`) and at most `/24`;
- **requires** written-authorization (RoE) confirmation and **fails closed** without it;
- is **advisory-only**: it **never** exploits flaws nor changes the network.

**It is illegal** to use this tool to scan networks without authorization. Responsibility for
use lies entirely with the operator.

## Reporting a vulnerability

If you found a flaw **in noobmap** (for example, a way to bypass the authorization gate, an
unintended write path, or code execution), **do not** open a public issue.

Use GitHub's private channel:
1. Open this repository's **Security** tab.
2. Click **Report a vulnerability**.
3. Describe the problem and impact, with reproduction steps and the noobmap version.

This opens a **private** conversation with the maintainer. If that option is unavailable,
open an issue **without sensitive details** asking for a private contact.

Fixed vulnerabilities will be documented in `CHANGELOG.md`.

## Scope

In scope:
- the code in `src/noobmap/` and the build/health-check scripts.

Out of scope:
- **Nmap** itself (report to the Nmap project);
- **Kali Linux**;
- misuse by third parties.
