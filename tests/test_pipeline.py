import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import authorization, pipeline, storage

XML = """<?xml version="1.0"?>
<nmaprun>
 <host>
  <status state="up"/>
  <address addr="192.168.1.1" addrtype="ipv4"/>
  <ports>
   <port protocol="tcp" portid="23"><state state="open"/><service name="telnet"/></port>
  </ports>
 </host>
</nmaprun>"""


def make_dest(tmp):
    dest = storage.run_dir(tmp, "Mercado X", "2026-10-08T00:00:00Z")
    authorization.record_authorization(dest, "Mercado X")
    return dest


def fake_scan(rede, xml_path):
    Path(xml_path).parent.mkdir(parents=True, exist_ok=True)
    Path(xml_path).write_text(XML, encoding="utf-8")
    return ["nmap"], SimpleNamespace(returncode=0, stderr="")


def failing_scan(rede, xml_path):
    return ["nmap"], SimpleNamespace(returncode=1, stderr="boom")


def silent_scan(rede, xml_path):
    return ["nmap"], SimpleNamespace(returncode=0, stderr="")


def garbage_scan(rede, xml_path):
    Path(xml_path).write_text("isto nao e xml valido", encoding="utf-8")
    return ["nmap"], SimpleNamespace(returncode=0, stderr="")


class PipelineTest(unittest.TestCase):
    def test_writes_report_and_raw(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = make_dest(tmp)
            findings, report_path = pipeline.run_scan_and_report(
                "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", dest, run_scan=fake_scan
            )
            self.assertTrue(report_path.exists())
            self.assertTrue((dest / "nmap_bruto.xml").exists())
            doc = report_path.read_text(encoding="utf-8")
            self.assertIn("Mercado X", doc)
            self.assertIn("Crítico", doc)
            self.assertEqual(findings[0]["chave"], "servico-telnet")

    def test_requires_authorization_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = storage.run_dir(tmp, "Mercado X", "2026-10-08T00:00:00Z")
            with self.assertRaises(pipeline.PipelineError):
                pipeline.run_scan_and_report(
                    "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", dest, run_scan=fake_scan
                )

    def test_failure_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = make_dest(tmp)
            with self.assertRaises(pipeline.PipelineError):
                pipeline.run_scan_and_report(
                    "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", dest, run_scan=failing_scan
                )

    def test_missing_output_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = make_dest(tmp)
            with self.assertRaises(pipeline.PipelineError):
                pipeline.run_scan_and_report(
                    "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", dest, run_scan=silent_scan
                )

    def test_corrupted_output_raises_friendly_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = make_dest(tmp)
            with self.assertRaises(pipeline.PipelineError):
                pipeline.run_scan_and_report(
                    "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", dest, run_scan=garbage_scan
                )

    def test_invalid_target_rejected_in_pipeline(self):
        from noobmap import scan

        with tempfile.TemporaryDirectory() as tmp:
            dest = make_dest(tmp)
            with self.assertRaises(scan.ScanError):
                pipeline.run_scan_and_report(
                    "Mercado X", "2026-10-08T00:00:00Z", "8.8.8.0/24", dest, run_scan=fake_scan
                )

    def test_no_writes_outside_dest(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = make_dest(tmp)
            pipeline.run_scan_and_report(
                "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", dest, run_scan=fake_scan
            )
            for path in Path(tmp).rglob("*"):
                if path.is_file():
                    self.assertTrue(
                        str(path.resolve()).startswith(str(dest.resolve()))
                    )


if __name__ == "__main__":
    unittest.main()
