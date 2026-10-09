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


class ReportTest(unittest.TestCase):
    def test_no_external_assets(self):
        doc = report.render_html("Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", FINDINGS)
        low = doc.lower()
        for bad in ["http://", "https://", "//cdn", 'src="//', 'href="//']:
            self.assertNotIn(bad, low)

    def test_contains_client_and_severity_label(self):
        doc = report.render_html("Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24", FINDINGS)
        self.assertIn("Mercado X", doc)
        self.assertIn("Crítico", doc)

    def test_escapes_html_in_data(self):
        finding = dict(FINDINGS[0], host="<script>alert(1)</script>")
        doc = report.render_html("C", "t", "r", [finding])
        self.assertNotIn("<script>alert(1)</script>", doc)
        self.assertIn("&lt;script&gt;", doc)

    def test_terminal_summary_counts_and_path(self):
        summary = report.terminal_summary(FINDINGS, "out/relatorio.html")
        self.assertIn("Crítico: 1", summary)
        self.assertIn("Informativo: 1", summary)
        self.assertIn("out/relatorio.html", summary)

    def test_disclaimer_present(self):
        doc = report.render_html("C", "t", "r", FINDINGS)
        self.assertIn("nunca", doc.lower())

    def test_unknown_severity_treated_as_informative(self):
        finding = dict(FINDINGS[0], severidade="Bizarro")
        doc = report.render_html("C", "t", "r", [finding])
        self.assertIn("Informativo", doc)
        self.assertNotIn("Bizarro", doc)


if __name__ == "__main__":
    unittest.main()
