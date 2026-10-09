import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

EXIT_ABORT = 3
MAX_CLIENTE = 64
ROOT = Path(__file__).resolve().parents[2]
ROE_TERM_PATH = ROOT / "docs" / "roe" / "termo-de-autorizacao.md"


class AuthorizationError(Exception):
    pass


def slugify(name):
    slug = re.sub(r"[^a-z0-9]+", "-", str(name).strip().lower()).strip("-")
    return slug or "cliente"


def now_iso():
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def require_authorization(autorizado, cliente):
    if not autorizado:
        raise AuthorizationError(
            "Varredura bloqueada: é obrigatória autorização escrita do cliente (RoE).\n"
            "  1. Faça o cliente ler e aceitar o termo: {termo}\n"
            "  2. Rode novamente com:\n"
            '     noobmap scan --autorizado --cliente "NOME DO CLIENTE" --rede 192.168.1.0/24'.format(
                termo=ROE_TERM_PATH
            )
        )
    if not cliente or not str(cliente).strip():
        raise AuthorizationError(
            "Autorização confirmada, mas falta o nome do cliente.\n"
            '  Use: --cliente "NOME DO CLIENTE"'
        )
    if len(str(cliente).strip()) > MAX_CLIENTE:
        raise AuthorizationError(
            "Nome do cliente muito longo (máximo de {n} caracteres).".format(n=MAX_CLIENTE)
        )


def _private(path):
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def record_authorization(dest_dir, cliente, quando=None, rede=None):
    cliente = str(cliente).strip()
    target = Path(dest_dir)
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    record = {"cliente": cliente, "autorizado_em": quando or now_iso()}
    if rede:
        record["rede"] = str(rede)
    path = target / "autorizacao.json"
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    _private(path)
    return path, record
