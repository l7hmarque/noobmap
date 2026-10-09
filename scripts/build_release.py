import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"


def read_version():
    text = (SRC / "noobmap" / "__init__.py").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("__version__"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("versao nao encontrada em src/noobmap/__init__.py")


def _copy(src, dst):
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    else:
        shutil.copy2(src, dst)


def build():
    version = read_version()
    DIST.mkdir(exist_ok=True)
    name = "noobmap-{v}".format(v=version)
    stage = DIST / name
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    _copy(SRC / "noobmap", stage / "src" / "noobmap")
    for rel in [
        "noobmap",
        "pyproject.toml",
        "README.md",
        "README.pt-BR.md",
        "LICENSE",
        "docs/usage.md",
        "docs/TUTORIAL.md",
        "docs/TUTORIAL.pt-BR.md",
        "docs/FAQ.md",
        "docs/FAQ.pt-BR.md",
        "docs/roe/termo-de-autorizacao.md",
        "docs/roe/terms-of-engagement.md",
    ]:
        src = ROOT / rel
        dst = stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    zip_path = DIST / "{n}.zip".format(n=name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(stage.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(DIST))

    shutil.rmtree(stage)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    (DIST / "{n}.zip.sha256".format(n=name)).write_text(
        "{d}  {f}\n".format(d=digest, f=zip_path.name), encoding="utf-8"
    )
    return version, zip_path, digest


def main():
    version, zip_path, digest = build()
    print("release : {p}".format(p=zip_path))
    print("version : {v}".format(v=version))
    print("sha256  : {d}".format(d=digest))


if __name__ == "__main__":
    sys.exit(main())
