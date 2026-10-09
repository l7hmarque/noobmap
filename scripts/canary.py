#!/usr/bin/env python3
"""Canary/smoke do noobmap — checagens rápidas de saúde para pós-distribuição."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OPS = ROOT / "dist" / "ops"
sys.path.insert(0, str(SRC))


def check_version():
    from noobmap import __version__

    return True, "versao {}".format(__version__), True


def check_fail_closed():
    from noobmap.authorization import AuthorizationError, require_authorization

    try:
        require_authorization(False, "x")
    except AuthorizationError:
        return True, "scan sem --autorizado aborta (fail-closed)", True
    return False, "NAO abortou sem autorizacao", True


def check_target_guard():
    from noobmap.scan import ScanError, validate_target

    try:
        validate_target("8.8.8.0/24")
    except ScanError:
        return True, "rejeita rede publica", True
    return False, "aceitou rede publica", True


def check_report_offline():
    from noobmap.report import render_html

    doc = render_html("Canary", "2026-01-01T00:00:00Z", "192.168.1.0/24", []).lower()
    bad = [t for t in ["http://", "https://", "//cdn", "<script"] if t in doc]
    if bad:
        return False, "relatorio com item proibido: " + ", ".join(bad), True
    return True, "relatorio offline, sem JS, sem assets externos", True


def check_release_checksum():
    zips = sorted((ROOT / "dist").glob("noobmap-*.zip"))
    if not zips:
        return True, "sem pacote em dist/ (skip)", False
    zip_path = zips[-1]
    sha_file = zip_path.with_suffix(".zip.sha256")
    if not sha_file.exists():
        return False, "checksum ausente para {}".format(zip_path.name), True
    expected = sha_file.read_text(encoding="utf-8").split()[0]
    actual = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    if actual != expected:
        return False, "checksum NAO confere", True
    return True, "checksum OK ({})".format(zip_path.name), True


def check_nmap():
    from noobmap.scan import ScanError, ensure_nmap

    try:
        ensure_nmap()
    except ScanError:
        return True, "nmap ausente (ok fora do Kali)", False
    return True, "nmap presente", True


CHECKS = [
    ("version", check_version),
    ("fail_closed", check_fail_closed),
    ("target_guard", check_target_guard),
    ("report_offline", check_report_offline),
    ("release_checksum", check_release_checksum),
    ("nmap", check_nmap),
]


def main():
    results = []
    failed = 0
    print("CANARY noobmap")
    for name, check in CHECKS:
        try:
            ok, msg, critical = check()
        except Exception as exc:  # noqa: BLE001
            ok, msg, critical = False, "excecao: {}".format(exc), True
        mark = "OK " if ok else "FAIL"
        if not ok and critical:
            failed += 1
        results.append({"name": name, "ok": ok, "critical": critical, "message": msg})
        print("  [{}] {}".format(mark, msg))
    healthy = failed == 0
    print("total: {}".format("FALHOU" if not healthy else "SAUDÁVEL"))

    OPS.mkdir(parents=True, exist_ok=True)
    (OPS / "canary.json").write_text(
        json.dumps(
            {
                "ts": datetime.now(timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "healthy": healthy,
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return 0 if healthy else 1


if __name__ == "__main__":
    sys.exit(main())
