import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import findings

XML = """<?xml version="1.0"?>
<nmaprun>
 <host>
  <status state="up"/>
  <address addr="192.168.1.1" addrtype="ipv4"/>
  <ports>
   <port protocol="tcp" portid="23"><state state="open"/><service name="telnet"/></port>
   <port protocol="tcp" portid="80"><state state="open"/><service name="http"/></port>
   <port protocol="tcp" portid="445"><state state="open"/><service name="microsoft-ds"/></port>
   <port protocol="tcp" portid="22"><state state="closed"/><service name="ssh"/></port>
  </ports>
 </host>
</nmaprun>"""


class ParseTest(unittest.TestCase):
    def test_only_open_ports(self):
        fs = findings.parse_nmap_xml(XML)
        self.assertEqual({f["porta"] for f in fs}, {23, 80, 445})

    def test_telnet_is_critical(self):
        telnet = next(f for f in findings.parse_nmap_xml(XML) if f["porta"] == 23)
        self.assertEqual(telnet["severidade"], "Critico")
        self.assertEqual(telnet["chave"], "servico-telnet")

    def test_smb_is_high(self):
        smb = next(f for f in findings.parse_nmap_xml(XML) if f["porta"] == 445)
        self.assertEqual(smb["severidade"], "Alto")

    def test_unknown_port_surfaced(self):
        xml = XML.replace('portid="80"', 'portid="9999"').replace(
            'name="http"', 'name="unknown"'
        )
        fs = findings.parse_nmap_xml(xml)
        unknown = next((f for f in fs if f["porta"] == 9999), None)
        self.assertIsNotNone(unknown)
        self.assertEqual(unknown["chave"], "precisa-verificacao")

    def test_no_silent_drops(self):
        self.assertEqual(len(findings.parse_nmap_xml(XML)), 3)

    def test_sorted_by_severity(self):
        fs = findings.parse_nmap_xml(XML)
        ranks = [findings.SEVERITY_RANK[f["severidade"]] for f in fs]
        self.assertEqual(ranks, sorted(ranks))

    def test_rejects_doctype(self):
        with self.assertRaises(ValueError):
            findings.parse_nmap_xml('<?xml version="1.0"?><!DOCTYPE x><nmaprun/>')


if __name__ == "__main__":
    unittest.main()
