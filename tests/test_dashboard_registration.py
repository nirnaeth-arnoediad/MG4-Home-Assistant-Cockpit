"""Static regression checks for storage-only dashboard registration."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'custom_components' / 'mg4_cockpit'

class DashboardRegistrationTests(unittest.TestCase):
    def test_storage_dashboard_registration(self):
        source = (ROOT / 'dashboard_registration.py').read_text(encoding='utf-8')
        self.assertIn('DashboardsCollection', source)
        self.assertIn('LovelaceStorage', source)
        self.assertIn('async_save(config)', source)

    def test_no_configuration_yaml_write(self):
        for name in ('dashboard_registration.py', 'config_flow.py', 'update_manager.py'):
            source = (ROOT / name).read_text(encoding='utf-8')
            self.assertNotIn('root / "configuration.yaml"', source)
            self.assertNotIn('config_dir) / "configuration.yaml"', source)
