#!/usr/bin/env python3
"""Auditoria de produção (adaptada) do noobmap: suíte de testes + invariantes."""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "dist" / "ops"
STATE_CHANGING = re.compile(
    r"\b(nft|iptables|ufw|systemctl|apt-get install|apt install)\b"
)


def run_tests():
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    match = re.search(r"Ran (\d+) tests", out)
    ran = int(match.group(1)) if match else 0
    ok = proc.returncode == 0 and ran > 0
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    return ok, ran, tail


def check_non_destructive():
    hits = []
    for base in ["src", "tests"]:
        for path in sorted((ROOT / base).rglob("*.py")):
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                if STATE_CHANGING.search(line):
                    hits.append("{}:{}".format(path.relative_to(ROOT), number))
    return not hits, hits


def check_scan_args_safe():
    sys.path.insert(0, str(ROOT / "src"))
    from noobmap.scan import SAFE_SCAN_ARGS

    joined = " ".join(SAFE_SCAN_ARGS).lower()
    bad = [t for t in ["--script", "exploit", "vuln", "brute", "dos"] if t in joined]
    return not bad, bad


def main():
    OPS.mkdir(parents=True, exist_ok=True)
    tests_ok, ran, tail = run_tests()
    inv_ok, inv_hits = check_non_destructive()
    args_ok, args_bad = check_scan_args_safe()

    healthy = tests_ok and inv_ok and args_ok
    result = {
        "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "healthy": healthy,
        "tests": {"ok": tests_ok, "ran": ran, "tail": tail},
        "invariant_non_destructive": {"ok": inv_ok, "hits": inv_hits},
        "scan_args_safe": {"ok": args_ok, "bad": args_bad},
    }
    (OPS / "audit.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("AUDITORIA noobmap")
    print("  [{}] testes ({} rodados): {}".format("OK " if tests_ok else "FAIL", ran, tail))
    print("  [{}] invariante nao-destrutivo".format("OK " if inv_ok else "FAIL"))
    print("  [{}] argumentos do nmap seguros".format("OK " if args_ok else "FAIL"))
    print("resultado: {}".format("SAUDÁVEL" if healthy else "ATENÇÃO"))
    print("relatorio: {}".format((OPS / "audit.json").relative_to(ROOT)))
    return 0 if healthy else 1


if __name__ == "__main__":
    sys.exit(main())
