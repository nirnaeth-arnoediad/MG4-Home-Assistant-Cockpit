"""MG4 Cockpit installation helper."""
from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .dashboard_registration import register_dashboard

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    try:
        hass.async_create_task(_create_dashboard_when_ready(hass))
    except Exception:
        _LOGGER.exception("MG4 Cockpit pano kurulumu başlatılamadı")
    return True

async def _create_dashboard_when_ready(hass):
    try:
        result = await register_dashboard(hass)
        if result not in ("created", "existing_panel", "existing_storage"):
            _LOGGER.warning("MG4 Cockpit pano durumu: %s", result)
    except Exception:
        _LOGGER.exception("MG4 Cockpit panosu oluşturulamadı")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
