import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import storage


class RunDirTest(unittest.TestCase):
    def test_per_client_per_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = storage.run_dir(tmp, "Mercado X", "2026-10-08T12:00:00Z")
            self.assertTrue(dest.exists())
            self.assertEqual(dest.parent.name, "mercado-x")
            self.assertEqual(dest.name, "2026-10-08")

    def test_additive_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = storage.run_dir(tmp, "Mercado X", "2026-10-08T12:00:00Z")
            second = storage.run_dir(tmp, "Mercado X", "2026-10-08T12:00:00Z")
            self.assertNotEqual(first, second)
            self.assertTrue(first.exists())
            self.assertTrue(second.exists())

    def test_stays_within_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = storage.run_dir(tmp, "../evil", "2026-10-08T00:00:00Z")
            self.assertTrue(
                str(dest.resolve()).startswith(str(Path(tmp).resolve()))
            )

    def test_write_text_returns_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = storage.write_text(Path(tmp) / "x" / "f.txt", "oi")
            self.assertEqual(path.read_text(encoding="utf-8"), "oi")

    @unittest.skipIf(os.name != "posix", "permissoes so se aplicam no POSIX")
    def test_output_is_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = storage.run_dir(tmp, "Mercado X", "2026-10-08T00:00:00Z")
            self.assertEqual(stat.S_IMODE(os.stat(dest).st_mode), 0o700)
            path = storage.write_text(dest / "f.txt", "oi")
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
