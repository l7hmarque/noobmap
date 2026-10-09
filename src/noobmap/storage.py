import os
import re
from pathlib import Path

from .authorization import slugify


class StorageError(Exception):
    pass


def harden(path, mode=0o600):
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def _date_part(quando_iso):
    return str(quando_iso)[:10]


def _time_part(quando_iso):
    return re.sub(r"[^0-9]", "", str(quando_iso)[11:19]) or "000000"


def run_dir(base, cliente, quando_iso):
    base = Path(base)
    client_dir = base / slugify(cliente)
    name = _date_part(quando_iso)
    target = client_dir / name
    if target.exists():
        target = client_dir / "{}_{}".format(name, _time_part(quando_iso))
    candidate = target
    counter = 2
    while candidate.exists():
        candidate = Path("{}_{}".format(target, counter))
        counter += 1
    if not candidate.resolve().is_relative_to(base.resolve()):
        raise StorageError("Caminho de saída inválido (fora do diretório base).")
    candidate.mkdir(parents=True, exist_ok=True, mode=0o700)
    harden(candidate, 0o700)
    return candidate


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    harden(path, 0o600)
    return path
