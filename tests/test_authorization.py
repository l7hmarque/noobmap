import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from noobmap import authorization as auth


class SlugifyTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(auth.slugify("Mercado X"), "mercado-x")

    def test_strips_and_collapses(self):
        self.assertEqual(auth.slugify("  Pizzaria  do Joao!  "), "pizzaria-do-joao")

    def test_empty_falls_back(self):
        self.assertEqual(auth.slugify("   "), "cliente")


class NowIsoTest(unittest.TestCase):
    def test_utc_zulu_seconds(self):
        value = auth.now_iso()
        self.assertTrue(value.endswith("Z"))
        self.assertNotIn("+00:00", value)


class RequireAuthorizationTest(unittest.TestCase):
    def test_missing_flag_raises(self):
        with self.assertRaises(auth.AuthorizationError):
            auth.require_authorization(False, "Mercado X")

    def test_message_points_to_roe_term(self):
        try:
            auth.require_authorization(False, "Mercado X")
        except auth.AuthorizationError as exc:
            self.assertIn("termo", str(exc).lower())

    def test_missing_cliente_raises(self):
        with self.assertRaises(auth.AuthorizationError):
            auth.require_authorization(True, "   ")

    def test_valid_passes(self):
        auth.require_authorization(True, "Mercado X")

    def test_rejects_overlong_cliente(self):
        with self.assertRaises(auth.AuthorizationError):
            auth.require_authorization(True, "x" * (auth.MAX_CLIENTE + 1))


class RecordAuthorizationTest(unittest.TestCase):
    def test_writes_client_and_timestamp_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "run"
            path, record = auth.record_authorization(dest, "Mercado X")
            self.assertTrue(path.exists())
            self.assertEqual(path, dest / "autorizacao.json")
            self.assertEqual(set(record.keys()), {"cliente", "autorizado_em"})
            self.assertEqual(record["cliente"], "Mercado X")
            self.assertTrue(record["autorizado_em"].endswith("Z"))

    def test_creates_missing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "a" / "b"
            path, _ = auth.record_authorization(dest, "Mercado X")
            self.assertTrue(path.exists())

    def test_record_includes_rede_when_given(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, record = auth.record_authorization(
                Path(tmp) / "run", "Mercado X", "2026-10-08T00:00:00Z", "192.168.1.0/24"
            )
            self.assertEqual(record["rede"], "192.168.1.0/24")


if __name__ == "__main__":
    unittest.main()
