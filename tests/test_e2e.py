import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

XML = """<?xml version="1.0"?>
<nmaprun>
 <host>
  <status state="up"/>
  <address addr="192.168.1.50" addrtype="ipv4"/>
  <ports>
   <port protocol="tcp" portid="23"><state state="open"/><service name="telnet"/></port>
   <port protocol="tcp" portid="445"><state state="open"/><service name="microsoft-ds"/></port>
   <port protocol="tcp" portid="8080"><state state="open"/><service name="http-proxy"/></port>
  </ports>
 </host>
</nmaprun>
"""

FAKE_PY = """import os, sys
here = os.path.dirname(os.path.abspath(__file__))
out = None
args = sys.argv[1:]
for i, a in enumerate(args):
    if a == "-oX" and i + 1 < len(args):
        out = args[i + 1]
if not out:
    sys.exit(0)
if os.environ.get("noobmap_FAKE_GARBAGE"):
    data = "isto nao e xml valido"
else:
    with open(os.path.join(here, "fake_nmap.xml"), encoding="utf-8") as fh:
        data = fh.read()
with open(out, "w", encoding="utf-8") as fh:
    fh.write(data)
"""


def make_fake_nmap(dirpath):
    dirpath = Path(dirpath)
    (dirpath / "fake_nmap.py").write_text(FAKE_PY, encoding="utf-8")
    (dirpath / "fake_nmap.xml").write_text(XML, encoding="utf-8")
    if os.name == "nt":
        (dirpath / "nmap.cmd").write_text(
            '@echo off\r\npython "%~dp0fake_nmap.py" %*\r\n', encoding="utf-8"
        )
    else:
        binary = dirpath / "nmap"
        binary.write_text(
            '#!/usr/bin/env bash\nexec python3 "$(dirname "$0")/fake_nmap.py" "$@"\n',
            encoding="utf-8",
        )
        os.chmod(binary, 0o755)
    return dirpath


def run_cli(args, env, cwd):
    return subprocess.run(
        [sys.executable, "-m", "noobmap", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )


class CliE2ETest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.fake = make_fake_nmap(self.tmp.name)
        self.env = dict(os.environ)
        self.env["PATH"] = str(self.fake) + os.pathsep + self.env.get("PATH", "")
        self.env["PYTHONPATH"] = str(SRC)

    def test_fail_closed_without_authorization(self):
        saida = Path(self.tmp.name) / "out"
        result = run_cli(
            ["scan", "--cliente", "Mercado X", "--rede", "192.168.1.0/24", "--saida", str(saida)],
            self.env,
            self.tmp.name,
        )
        self.assertEqual(result.returncode, 3)
        self.assertFalse(saida.exists())

    def test_happy_path_generates_report(self):
        saida = Path(self.tmp.name) / "out"
        result = run_cli(
            ["scan", "--autorizado", "--cliente", "Mercado X", "--rede", "192.168.1.0/24", "--saida", str(saida)],
            self.env,
            self.tmp.name,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        reports = list(saida.rglob("relatorio.html"))
        self.assertEqual(len(reports), 1)
        doc = reports[0].read_text(encoding="utf-8")
        self.assertIn("Crítico", doc)
        self.assertIn("Mercado X", doc)

    def test_invalid_target_rejected_without_artifacts(self):
        saida = Path(self.tmp.name) / "out"
        result = run_cli(
            ["scan", "--autorizado", "--cliente", "Mercado X", "--rede", "8.8.8.0/24", "--saida", str(saida)],
            self.env,
            self.tmp.name,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(saida.exists())

    def test_corrupted_output_is_friendly(self):
        saida = Path(self.tmp.name) / "out"
        env = dict(self.env)
        env["noobmap_FAKE_GARBAGE"] = "1"
        result = run_cli(
            ["scan", "--autorizado", "--cliente", "Mercado X", "--rede", "192.168.1.0/24", "--saida", str(saida)],
            env,
            self.tmp.name,
        )
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
