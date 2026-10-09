<p align="center">
  <img src="docs/img/logo.svg" width="120" alt="noobmap logo">
</p>

<h1 align="center">noobmap</h1>

<p align="center"><strong>Basic network security, explained for non-experts — running on Kali Live (USB), installing nothing.</strong></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platform-Kali%20Linux-557C94.svg" alt="Platform: Kali Linux">
  <a href="https://github.com/l7hmarque/noobmap/actions/workflows/ci.yml"><img src="https://github.com/l7hmarque/noobmap/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
</p>

<p align="center">
  <a href="README.md">🇧🇷 Português</a> · 🇬🇧 <strong>English</strong>
</p>

---

**noobmap** is a command-line tool that runs a **basic security scan** on your home or
small-business network and produces a **plain-language report** with **step-by-step fixes**
anyone can follow.

The idea is simple: **everyone deserves minimum security** — and it shouldn't be complicated
or expensive. You boot **Kali Live** from a USB stick (**nothing installed**), run one command,
and get a report telling you **what is exposed** and **how to close that door**.

> ⚠️ **Authorized use only.** Scanning networks you don't own or have permission to test is
> illegal. The tool **requires** you to confirm written authorization and **refuses to run**
> without it.

### 📋 Table of contents

- [What it does (and what it does **not** do)](#what-it-does-and-what-it-does-not-do)
- [How it works](#how-it-works)
- [Setup: Kali Live on a USB stick](#setup-kali-live-on-a-usb-stick)
- [Usage](#usage)
- [Example report](#example-report)
- [Limitations (in the open)](#limitations-in-the-open)
- [Project layout](#project-layout)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)

### What it does (and what it does **not** do)

✅ **Does**
- Finds **which devices** are on the network and **which ports/services** are open.
- Flags common **risky services**: Telnet, SMB, RDP, VNC, exposed databases
  (MySQL, PostgreSQL, SQL Server, Oracle, MongoDB, Redis, Elasticsearch, Memcached),
  an exposed Docker API, WinRM, Jupyter, NFS, and legacy remote services (rsh/rlogin/rexec).
- Rates every finding by **severity**: Critical → High → Medium → Low → Informational.
- Produces an **offline HTML report** (opens with no internet) plus a terminal summary.
- For each finding, gives a walkthrough: **where to go, what to change, what NOT to touch**.

🚫 **Does not**
- **Exploit anything** (no Metasploit, no intrusion).
- **Read encrypted traffic** or capture passwords.
- **Change anything** on your network — it only **advises**; *you* apply the changes.
- Cover **wi-fi**, phones, phishing, or local malware.
- Replace a professional penetration test (see [Limitations](#limitations-in-the-open)).

### How it works

```
Authorization (RoE) → Nmap scan → Analysis + Severity → HTML report → Fixes → Re-scan
```

Interactive diagrams (open in a browser):
- [Overview — how noobmap works](docs/diagramas/noobmap-como-funciona.html)
- [Under the hood — from the nmap command to the report](docs/diagramas/noobmap-por-dentro.html)

The engine is **[Nmap](https://nmap.org/)** (already on Kali), called with **conservative** options:

| Option | What it does |
|---|---|
| `-sV` | detects the **version** of each service |
| `--top-ports 100` | scans only the **100 most common services** |
| `-Pn` | scans even if the device **blocks ping** |
| `-T3` | **moderate pace**, doesn't overload the network |
| `-oX` | saves the raw result as **XML** (evidence) |
| *(no `--script`)* | **no** exploit/intrusion testing at all |

noobmap accepts **private networks only** (`10.x`, `172.16–31.x`, `192.168.x`) and at most **/24 (254 devices)**.

### Setup: Kali Live on a USB stick

1. A **USB stick, 8 GB+**, and a writer: [Rufus](https://rufus.ie/) (Windows) or [balenaEtcher](https://etcher.balena.io/) (any OS).
2. Download the **Kali Linux Live** ISO from [kali.org/get-kali](https://www.kali.org/get-kali/) (the *Live Boot* option).
3. Flash the ISO to the stick (this **erases** it).
4. **Boot from the USB** (boot key: `F12`, `F2`, `DEL`, `ESC`… depends on the brand).
5. Choose **"Live system"** (installs nothing on the computer).

The detailed, screen-by-screen guide is in **[docs/tutorial.en.md](docs/tutorial.en.md)**.

### Usage

In the Kali Live terminal, inside the noobmap folder:

```bash
chmod +x noobmap
./noobmap --version

# 1) Have the client read and sign the term: docs/roe/termo-de-autorizacao.md
# 2) Run the scan (replace with their name and network):
./noobmap scan --autorizado --cliente "Client name" --rede 192.168.1.0/24
```

Output goes to `noobmap-out/<client>/<date>/`:
- `relatorio.html` — the client document (open in a browser).
- `nmap_bruto.xml` — raw data (keep as evidence).
- `autorizacao.json` — proof that authorization existed.

Without `--autorizado`, the tool **aborts** with exit code 3 and scans nothing.

### Example report

<p align="center">
  <img src="docs/img/relatorio-exemplo.png" width="760" alt="Example noobmap report">
</p>

### Limitations (in the open)

noobmap is a **baseline** — the "minimum security everyone should have". It:
- covers **~30 common services** in a **generic** way (the guidance fits most routers, with a
  documented extension point for your specific model);
- is **advisory-only**: it finds exposure and advises; it does **not** guarantee the network is
  100% safe;
- does **not** replace **firmware updates**, **password management**, **antivirus**, and
  **user awareness**.

It **substantially reduces** the risk of common automated remote attacks (**if** the fixes are
applied), but **0-days, phishing, and local flaws stay out of scope**. That said, a network
without this check is exposed to problems that **should** already be closed.

### Project layout

```
noobmap            # command (bash wrapper)
pyproject.toml
src/noobmap/       # cli, authorization, scan, findings, remediation, report, storage, pipeline
tests/             # 71 tests (unittest)
scripts/           # build_release.py, canary.py, audit.py
docs/              # tutorial, FAQ, diagrams, RoE term, ADRs
```

### Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests     # 71 tests, no external dependencies
python scripts/build_release.py                          # builds dist/noobmap-<version>.zip + checksum
python scripts/canary.py                                 # health checks
python scripts/audit.py                                  # tests + invariants
```

### Contributing

Read **[CONTRIBUTING.md](CONTRIBUTING.md)**. Especially welcome: **remediation guidance for
specific router models** (Mikrotik, TP-Link, Intelbras, Ubiquiti…), new severity rules, and
translations.

### License

**[MIT](LICENSE)** — use it, study it, modify it, share it.

---

<p align="center"><a href="README.md">← Ler em Português</a></p>
