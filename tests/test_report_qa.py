import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import report

FINDINGS = [
    {
        "host": "192.168.1.1",
        "porta": 23,
        "protocolo": "tcp",
        "servico": "telnet",
        "chave": "servico-telnet",
        "severidade": "Critico",
        "descricao": "Telnet exposto",
    },
    {
        "host": "192.168.1.1",
        "porta": 80,
        "protocolo": "tcp",
        "servico": "http",
        "chave": "servico-http",
        "severidade": "Informativo",
        "descricao": "HTTP exposto",
    },
]


class ReportQATest(unittest.TestCase):
    def setUp(self):
        self.doc = report.render_html(
            "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", FINDINGS
        )

    def test_language_declared(self):
        self.assertIn('<html lang="pt-BR">', self.doc)

    def test_viewport_for_mobile(self):
        self.assertIn('name="viewport"', self.doc)

    def test_single_h1(self):
        self.assertEqual(self.doc.count("<h1>"), 1)

    def test_has_title(self):
        self.assertIn("<title>", self.doc)

    def test_no_javascript(self):
        self.assertNotIn("<script", self.doc.lower())

    def test_offline_no_external_assets(self):
        low = self.doc.lower()
        for bad in ["http://", "https://", "//cdn", 'src="//', 'href="//']:
            self.assertNotIn(bad, low)

    def test_print_styles_present(self):
        self.assertIn("@media print", self.doc)


if __name__ == "__main__":
    unittest.main()
