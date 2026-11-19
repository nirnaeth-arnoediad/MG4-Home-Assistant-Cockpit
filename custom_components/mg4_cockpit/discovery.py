"""Discover SAIC vehicle identifiers from Home Assistant's entity registry."""
from __future__ import annotations
import re
from homeassistant.helpers import entity_registry as er

VIN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$", re.I)
# Require multiple SAIC-specific entities, not merely any 17-character identifier.
SUFFIXES = ("_soc", "_range", "_battery_charging", "_last_vehicle_state", "_charger_connected")

def find_vehicles(hass):
    registry = er.async_get(hass)
    found = {}
    for entry in registry.entities.values():
        eid = entry.entity_id.lower()
        for suffix in SUFFIXES:
            if not eid.endswith(suffix):
                continue
            prefix = eid.split('.', 1)[-1][:-len(suffix)]
            if VIN.fullmatch(prefix):
                found.setdefault(prefix.upper(), set()).add(suffix)
    return sorted(vin for vin, suffixes in found.items() if len(suffixes) >= 2)
