# Usage guide (step by step)

noobmap scans your clients' networks and **never changes** the router or the network.

## Before anything: authorization (required)

1. Open `docs/roe/terms-of-engagement.md`, print it and have the **client sign** it.
   (Without it, the tool **won't run** — that's your legal protection.)
2. Guide the scan only on the network of the client who signed.

## Boot Kali and open a terminal

1. Boot from the Kali USB stick (no install needed).
2. Open the **Terminal**.

## Find the client's network

1. In the client's router admin page (or on your phone connected to their wi-fi), see the
   network address. It's usually something like `192.168.1.0/24` or `192.168.0.0/24`.
2. The tool accepts **private networks only** and **at most /24 (254 devices)**.

## Run the scan

Type (replacing with the client name and their network):

```bash
noobmap scan --autorizado --cliente "Client name" --rede 192.168.1.0/24
```

What happens:

1. It records the authorization (client name + date/time).
2. It runs Nmap **non-intrusively** (no exploitation).
3. It creates a **report** and prints a summary in the terminal.

## Where the files go

In `noobmap-out/<client-name>/<YYYY-MM-DD>/`:

- `relatorio.html` — **open in a browser**. This is the document for the client.
- `nmap_bruto.xml` — raw technical data (keep it; you don't need to understand it).
- `autorizacao.json` — proof that authorization existed.

> Tip: copy the folder to a **USB stick** so you don't lose the report when Kali shuts down.

## Understand the report

- Risks come by severity: **Critical → High → Medium → Low → Informational**.
- Each item has "How to fix", with **where to go**, **what to change**, and what **not** to touch.
- **Back up** the router configuration before changing anything.
- When unsure, **stop** and don't change anything — the report also warns about false positives.

## Need help?

```bash
noobmap --help
noobmap scan --help
noobmap --version
```
