# FAQ — Frequently Asked Questions

### Is this legal?
Yes, **as long as you have authorization**. Only scan networks that are **yours** or for which
the owner gave **written authorization**. The tool **requires** that confirmation (the RoE
term) and **won't run without it**. Scanning third-party networks without permission is illegal.

### Do I need to know Linux or be a "hacker"?
No. The [tutorial](TUTORIAL.md) is written for people who have **never used Linux**. You just
boot Kali Live and type **one command**.

### Does it work on Windows or Mac?
The recommended way is **Kali Live** (a USB stick), which already ships `nmap`. noobmap is just
Python 3 + Nmap, so it can run anywhere those exist, but the target platform is **Kali Live**
(installing nothing).

### Will it take down the internet or the devices?
**No.** The scan is **non-intrusive** and at a moderate pace (`-T3`). noobmap **changes nothing**
on the network — it only observes and reports. You apply the fixes manually.

### Will it install anything on my computer?
No. **Kali Live** runs from the USB stick; nothing is installed. When you shut down, the
computer is back to normal.

### How long does it take?
A few minutes for a `/24` network. It depends on how many devices respond.

### What is "authorization (RoE)"?
"Rules of Engagement": a one-page term (`docs/roe/terms-of-engagement.md`) that the person
responsible for the network signs, authorizing the scan. It's your legal protection.

### Is the report hard to understand?
It's built for non-experts: plain language, risks by severity, and a **step-by-step** fix guide
telling you **where to go**, **what to change**, and **what NOT to touch**.

### What do I do after getting the report?
1. Save/export the router configuration (**backup**).
2. Apply the fixes **one at a time**, following the report.
3. Test the internet and devices after each change.
4. Run noobmap again (**re-scan**) to confirm the improvement.

### I got a "false positive"?
An open port is **not necessarily** a flaw — it may be a needed service. The report warns about
this. When unsure, **don't change** anything and confirm what that service does.

### Does it assess wi-fi, phones, or weak passwords?
**No.** noobmap looks at **exposed ports/services** on the network (focusing on common remote
attacks). Wi-fi, phones, phishing, and passwords are out of scope.

### Does it make my network 100% secure?
No. It's a **baseline** ("minimum security"). It **substantially reduces** the risk of common
automated remote attacks **if** the fixes are applied — but it does not replace firmware updates,
strong passwords, antivirus, and user awareness.

### Can I use it commercially / charge for it?
The license is **MIT** (use freely). But remember: the value you deliver is the assessment +
remediation guidance — and that **requires authorization** from whoever hires you.

### How can I contribute?
See **[CONTRIBUTING.md](../CONTRIBUTING.md)**. Especially welcome: **remediation guidance for
specific router models**, new severity rules, and translations.
