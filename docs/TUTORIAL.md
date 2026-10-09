# noobmap tutorial — from zero to a safer network

> Assumes you've **never used Linux** and **never scanned a network**. Follow in order.
> **Authorized use only:** scan networks you own or have **written permission** to test.

---

## 0. What you need

- A **USB stick, 8 GB+** (it will be erased).
- A **computer** you can boot from USB.
- The **noobmap** package (`noobmap-<version>.zip`).
- **Authorization** from whoever is responsible for the network.

---

## 1. Download Kali Live

Kali Live is "Linux on a stick" — it runs without installing anything.

1. Go to **https://www.kali.org/get-kali/**.
2. Pick **"Live Boot"**.
3. Download the **`.iso`** file (a few GB).

## 2. Write Kali to the USB stick

1. Get a writer: **Rufus** (Windows) or **balenaEtcher** (any OS).
2. Select the **image** = the Kali `.iso`, and the **target** = your **USB stick**
   (double-check it's the right drive!).
3. **Flash**. This **erases** the stick.
4. Eject safely.

## 3. Boot from the USB stick

1. Plug the stick in and **reboot** the computer.
2. Press the **boot key** early (`F12`, `F2`, `F10`, `DEL`, `ESC` — depends on the brand).
3. Pick the **USB** in the boot list.
4. If it won't boot: enter **BIOS/UEFI**, **disable Secure Boot**, and/or put **USB first**.
5. On the Kali screen choose **"Live system"**. **Do not** choose "Install".
6. You'll land on the Kali desktop — running from the stick. Nothing was installed.

## 4. Connect to the target network

Plug in Ethernet or join the wi-fi of the place you're assessing. Open a **Terminal**
(`Ctrl+Alt+T`).

## 5. Find the network address

You need the network as `192.168.1.0/24`. Either check the router's admin page (often
`192.168.0.1` / `192.168.1.1`) or run:

```bash
ip route
```

Find something like `192.168.1.0/24`. noobmap accepts **private networks only**
(`10.x`, `172.16–31.x`, `192.168.x`) and at most **/24** (up to 254 devices).

## 6. Get noobmap

Download **`noobmap-<version>.zip`** from the repo's *Releases*. Copy it to the USB stick
or the Kali Desktop, then:

```bash
cd ~/Desktop
unzip noobmap-*.zip
cd noobmap-*
chmod +x noobmap
./noobmap --version
```

## 7. Authorize (required)

Print and have the responsible person sign `docs/roe/terms-of-engagement.md`
(Rules of Engagement). Without it, the next step **aborts** — that's your legal protection.

## 8. Run the scan

```bash
./noobmap scan --autorizado --cliente "Client name" --rede 192.168.1.0/24
```

It records the authorization, runs Nmap **non-intrusively**, then prints a summary and
creates the report. Don't unplug the stick or interrupt the terminal.

## 9. Read the report

Files land in `noobmap-out/<client>/<date>/`:

- **`relatorio.html`** — open in a browser; this is the client document.
- `nmap_bruto.xml` — raw data (evidence).
- `autorizacao.json` — proof of authorization.

Findings are grouped by severity: **Critical → High → Medium → Low → Informational**.
Each has "How to fix" with **where to go**, **what to change**, and **what NOT to touch**.

## 10. Apply the fixes (carefully)

1. **First:** save/export the router's current configuration (backup).
2. Change **one thing at a time**, exactly as instructed.
3. After each change, **test** that the internet and devices still work.
4. If something breaks, **restore the backup**.
5. When unsure, **stop** (the report also warns about false positives).

noobmap **never** applies changes — you do.

## 11. Re-scan to confirm

```bash
./noobmap scan --autorizado --cliente "Client name" --rede 192.168.1.0/24
```

Ideal outcome: **zero open Critical/High** findings.

## 12. Hand off and save

- **Copy the client folder to the USB stick** (Kali Live forgets files on shutdown).
- Deliver `relatorio.html` to the client.
- Shut down the Live system and remove the stick.

## Troubleshooting

| Symptom | Fix |
|---|---|
| "nmap not found" | You're not on Kali Live — run it inside Kali. |
| "scan blocked: authorization required" | Add `--autorizado` (and the signed term). |
| "private networks only" | Use the client's LAN (`192.168.x.0/24`), not a public IP. |
| "network too large" | Use at most `/24`. |
