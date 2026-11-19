"""Unit tests for dashboard registration; no Home Assistant runtime required."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "custom_components" / "mg4_cockpit" / "dashboard_registration.py"
spec = importlib.util.spec_from_file_location("dashboard_registration", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DashboardRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "mg4_cockpit_dashboard.yaml").write_text("views: []\n", encoding="utf-8")

    def test_adds_dashboard_and_backup_once(self):
        cfg = self.root / "configuration.yaml"
        cfg.write_text("default_config:\n", encoding="utf-8")
        self.assertEqual(module.register_dashboard(str(self.root)), "added")
        content = cfg.read_text(encoding="utf-8")
        self.assertIn("mg4-cockpit-hacs:", content)
        self.assertIn("filename: mg4_cockpit_dashboard.yaml", content)
        self.assertEqual((self.root / "configuration.yaml.mg4_cockpit_backup").read_text(), "default_config:\n")
        self.assertEqual(module.register_dashboard(str(self.root)), "existing_lovelace")
        self.assertEqual(cfg.read_text(), content)

    def test_does_not_touch_existing_lovelace(self):
        cfg = self.root / "configuration.yaml"
        old = "default_config:\nlovelace:\n  dashboards: !include dashboards.yaml\n"
        cfg.write_text(old, encoding="utf-8")
        self.assertEqual(module.register_dashboard(str(self.root)), "existing_lovelace")
        self.assertEqual(cfg.read_text(), old)
        self.assertFalse((self.root / "configuration.yaml.mg4_cockpit_backup").exists())

    def test_ignores_commented_lovelace(self):
        cfg = self.root / "configuration.yaml"
        cfg.write_text("# lovelace:\ndefault_config:\n", encoding="utf-8")
        self.assertEqual(module.register_dashboard(str(self.root)), "added")

    def test_missing_dashboard_does_not_change_config(self):
        cfg = self.root / "configuration.yaml"
        cfg.write_text("default_config:\n", encoding="utf-8")
        (self.root / "mg4_cockpit_dashboard.yaml").unlink()
        self.assertEqual(module.register_dashboard(str(self.root)), "missing_dashboard")
        self.assertEqual(cfg.read_text(), "default_config:\n")

    def test_missing_configuration(self):
        self.assertEqual(module.register_dashboard(str(self.root)), "missing_configuration")


if __name__ == "__main__":
    unittest.main()
