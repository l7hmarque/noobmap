import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def run_cli(*args, cwd=None):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    return subprocess.run(
        [sys.executable, "-m", "noobmap", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )


class CliScaffoldTest(unittest.TestCase):
    def test_version(self):
        result = run_cli("--version")
        self.assertEqual(result.returncode, 0)
        self.assertIn("noobmap", result.stdout)

    def test_help_without_args(self):
        result = run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())


class RoeGateTest(unittest.TestCase):
    def test_scan_without_autorizado_aborts(self):
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "out"
            result = run_cli(
                "scan", "--cliente", "Mercado X", "--saida", str(saida), cwd=tmp
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("autoriza", (result.stdout + result.stderr).lower())
            self.assertFalse(saida.exists())

    def test_scan_autorizado_without_cliente_aborts(self):
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "out"
            result = run_cli("scan", "--autorizado", "--saida", str(saida), cwd=tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(saida.exists())

    def test_scan_autorizado_records_client_and_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            saida = Path(tmp) / "out"
            result = run_cli(
                "scan",
                "--autorizado",
                "--cliente",
                "Mercado X",
                "--saida",
                str(saida),
                cwd=tmp,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            records = list(saida.rglob("autorizacao.json"))
            self.assertEqual(len(records), 1)
            data = json.loads(records[0].read_text(encoding="utf-8"))
            self.assertEqual(data["cliente"], "Mercado X")
            self.assertRegex(
                data["autorizado_em"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
            )


if __name__ == "__main__":
    unittest.main()
