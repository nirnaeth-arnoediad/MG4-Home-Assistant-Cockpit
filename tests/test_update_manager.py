"""Offline tests for file comparison, VIN handling, and backup path layout."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1] / 'custom_components' / 'mg4_cockpit'
spec = importlib.util.spec_from_file_location('update_manager', BASE / 'update_manager.py')
# HA modules unavailable outside Home Assistant; stub only the import for offline pure tests.
import sys, types
ha = types.ModuleType('homeassistant'); ha.__path__=[]
helpers = types.ModuleType('homeassistant.helpers'); helpers.__path__=[]
storage = types.ModuleType('homeassistant.helpers.storage'); storage.Store = object
sys.modules.setdefault('homeassistant', ha)
sys.modules.setdefault('homeassistant.helpers', helpers)
sys.modules.setdefault('homeassistant.helpers.storage', storage)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class UpdateManagerTests(unittest.TestCase):
    def test_hash_stable(self):
        self.assertEqual(mod.digest(b'abc'), mod.digest(b'abc'))
        self.assertNotEqual(mod.digest(b'abc'), mod.digest(b'abd'))

    def test_targets_are_only_mg4(self):
        with tempfile.TemporaryDirectory() as td:
            targets = mod.asset_targets(Path(td))
            self.assertEqual(len(targets), 6)
            self.assertTrue(all(str(t).startswith(td) for _, t in targets))
            self.assertTrue(all('mg4_cockpit' in t.name for _, t in targets))

    def test_vin_recovery_from_package(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'packages').mkdir()
            (root/'packages'/'mg4_cockpit_example.yaml').write_text('sensor.lsjwh0000pn000001_battery_level')
            self.assertEqual(mod.find_vin(root), 'lsjwh0000pn000001')

if __name__ == '__main__': unittest.main()
