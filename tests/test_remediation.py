import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import findings, remediation

REQUIRED_FIELDS = ["titulo", "onde_ir", "passos", "backup", "desfazer", "nao_mexer"]


class CoverageTest(unittest.TestCase):
    def test_all_port_rule_keys_covered(self):
        for port, (key, severidade, _desc) in findings.PORT_RULES.items():
            self.assertTrue(remediation.has(key), "sem remediacao: " + key)

    def test_all_service_rule_keys_covered(self):
        for servico, (key, severidade, _desc) in findings.SERVICE_RULES.items():
            self.assertTrue(remediation.has(key), "sem remediacao: " + key)

    def test_entries_well_formed(self):
        for key in remediation.REMEDIATION:
            entry = remediation.get(key)
            for field in REQUIRED_FIELDS:
                self.assertIn(field, entry, key + ":" + field)
            self.assertTrue(entry["passos"], key)

    def test_unknown_returns_placeholder(self):
        self.assertEqual(remediation.get("chave-inexistente"), remediation.PLACEHOLDER)

    def test_disclaimer_forbids_auto_apply(self):
        self.assertIn("nunca", remediation.DISCLAIMER.lower())


if __name__ == "__main__":
    unittest.main()
