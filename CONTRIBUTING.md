# Contributing to noobmap

Thanks for your interest! This project wants to keep **network security accessible to anyone**.

## Ways to help

- **Remediation guidance for specific router models** (Mikrotik, TP-Link, Intelbras, Ubiquiti,
  Asus…). `src/noobmap/remediation.py` already has a generic extension point — add
  model-specific entries.
- **New severity rules** for services/ports (`src/noobmap/findings.py`).
- **Translations** of documentation and messages.
- **Bug fixes** and better tests.

## Project rules

- **Non-destructive.** noobmap **never** changes the network. No active exploitation, no
  brute force, no Nmap `--script`.
- **Fail-closed.** Never ship code that lets a scan run **without** the authorization gate.
- **Private networks only.** Keep the validation that rejects public ranges and networks
  larger than `/24`.
- **No secrets.** Don't commit keys, passwords, or real client data.

## Development environment

Requirements: **Python 3.9+** and (optional, for a real scan) **Nmap**.

```bash
git clone https://github.com/l7hmarque/noobmap
cd noobmap

# run the tests (no external dependencies: stdlib only)
PYTHONPATH=src python -m unittest discover -s tests

# run the tool locally
PYTHONPATH=src python -m noobmap --version
```

## Contribution flow

1. Open an **issue** describing what you want to change (or pick an existing one).
2. Create a **branch**: `git checkout -b feat/my-improvement`.
3. **Write the test first** (we use `unittest`; see `tests/`).
4. Implement the minimal change to make the test pass.
5. Make sure **everything passes**: `PYTHONPATH=src python -m unittest discover -s tests`.
6. Open a **Pull Request** explaining the "why" (not just the "what").

## Style

- Simple Python, stdlib only (no external dependencies).
- User-facing messages in **Portuguese, plain language** (the audience is non-technical).
- Keep the report **offline** (no external assets) and **escape** all data.

## Code of conduct

Be kind, patient, and didactic. This project's audience includes people **just getting started**.
