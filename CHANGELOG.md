# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.3.0] - 2026-10-09

### Added
- Demo GIF in the README (`docs/img/demo.gif`).
- Full English documentation. Optional Portuguese (pt-BR) translations kept at
  `README.pt-BR.md`, `docs/TUTORIAL.pt-BR.md`, `docs/FAQ.pt-BR.md` and the
  authorization term `docs/roe/termo-de-autorizacao.md`.

### Changed
- README is now English-first, with a language switcher linking to the pt-BR version.
- Documentation reorganized: `docs/usage.md`, `docs/TUTORIAL.md`, `docs/FAQ.md`,
  `docs/roe/terms-of-engagement.md`.

## [0.2.0] - 2026-10-09

### Added
- Severity rules and remediation for more services: rpcbind (111); rsh/rlogin/rexec
  (512/513/514); Oracle (1521); NFS (2049); Docker API (2375, Critical); WinRM (5985);
  Redis (6379); alternate HTTPS panel (8443); Jupyter (8888); Elasticsearch (9200);
  Memcached (11211); MongoDB (27017).
- Full English documentation (`README.en.md`).

### Changed
- README reorganized with a language switcher.

## [0.1.0] - 2026-10-08

### Added
- First public release.
- Guided Nmap scan (non-intrusive, no exploit scripts).
- Fail-closed written-authorization (RoE) gate.
- Severity classification (Critical → Informational) for ~16 common services.
- Offline HTML report in plain language, with step-by-step fixes.
- Terminal summary with counts and priorities.
- Per-client/date output with restrictive permissions (0700/0600).
- Target validation (private networks only, up to /24).
- Packaging (`scripts/build_release.py`) and health checks (`scripts/canary.py`,
  `scripts/audit.py`).
- Docs: tutorial, FAQ, authorization term and diagrams.
