import xml.etree.ElementTree as ET
from pathlib import Path

from .findings import parse_nmap_xml
from .report import render_html
from .scan import run_scan as _default_run_scan
from .scan import validate_target
from .storage import harden, write_text


class PipelineError(Exception):
    pass


def run_scan_and_report(cliente, quando, rede, dest, run_scan=_default_run_scan):
    dest = Path(dest)
    if not (dest / "autorizacao.json").exists():
        raise PipelineError(
            "Varredura recusada: registro de autorização ausente no destino."
        )
    rede = validate_target(rede)
    raw = dest / "nmap_bruto.xml"
    _, proc = run_scan(rede, raw)
    if getattr(proc, "returncode", 1) != 0:
        stderr = (getattr(proc, "stderr", "") or "").strip()
        raise PipelineError("A varredura falhou (nmap retornou erro). {s}".format(s=stderr))
    if not raw.exists():
        raise PipelineError("A varredura terminou sem gerar resultado.")
    harden(raw)
    try:
        findings = parse_nmap_xml(raw.read_text(encoding="utf-8"))
    except (ET.ParseError, ValueError, TypeError) as exc:
        raise PipelineError(
            "O resultado da varredura veio corrompido. Tente rodar de novo."
        ) from exc
    report_path = dest / "relatorio.html"
    write_text(report_path, render_html(cliente, quando, rede, findings))
    return findings, report_path
