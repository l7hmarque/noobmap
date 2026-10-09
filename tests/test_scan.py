import sys
import unittest
from pathlib import Path
from unittest import mock

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import scan


class ValidateTargetTest(unittest.TestCase):
    def test_accepts_private_class_c(self):
        self.assertEqual(scan.validate_target("192.168.1.0/24"), "192.168.1.0/24")

    def test_normalizes_host_bits(self):
        self.assertEqual(scan.validate_target("192.168.1.10/24"), "192.168.1.0/24")

    def test_accepts_private_class_a_small(self):
        self.assertEqual(scan.validate_target("10.0.0.0/24"), "10.0.0.0/24")

    def test_rejects_public_range(self):
        with self.assertRaises(scan.ScanError):
            scan.validate_target("8.8.8.0/24")

    def test_rejects_too_large(self):
        with self.assertRaises(scan.ScanError):
            scan.validate_target("10.0.0.0/16")

    def test_rejects_loopback(self):
        with self.assertRaises(scan.ScanError):
            scan.validate_target("127.0.0.0/24")

    def test_rejects_link_local(self):
        with self.assertRaises(scan.ScanError):
            scan.validate_target("169.254.0.0/24")

    def test_accepts_172_16_range(self):
        self.assertEqual(scan.validate_target("172.16.5.0/24"), "172.16.5.0/24")

    def test_rejects_public_172(self):
        with self.assertRaises(scan.ScanError):
            scan.validate_target("172.32.0.0/24")


class BuildCommandTest(unittest.TestCase):
    def test_has_xml_output_and_target(self):
        cmd = scan.build_command("192.168.1.0/24", "out.xml")
        self.assertIn("-oX", cmd)
        self.assertIn("out.xml", cmd)
        self.assertEqual(cmd[-1], "192.168.1.0/24")

    def test_no_intrusive_or_exploit_options(self):
        cmd = " ".join(scan.build_command("192.168.1.0/24", "out.xml")).lower()
        for bad in ["--script", "exploit", "vuln", "brute", "dos"]:
            self.assertNotIn(bad, cmd)


class EnsureNmapTest(unittest.TestCase):
    def test_raises_when_missing(self):
        with mock.patch("shutil.which", return_value=None):
            with self.assertRaises(scan.ScanError):
                scan.ensure_nmap()

    def test_ok_when_present(self):
        with mock.patch("shutil.which", return_value="/usr/bin/nmap"):
            scan.ensure_nmap()


if __name__ == "__main__":
    unittest.main()
