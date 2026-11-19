"""MG4 Cockpit installation helper; does not poll or control the vehicle."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .dashboard_registration import register_dashboard, DASHBOARD_URL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Register the generated dashboard without modifying existing panels.

    This also runs for users who installed the previous beta and already have
    an integration entry. The YAML dashboard is visible after the next restart.
    """
    try:
        from homeassistant.components import frontend

        if frontend.async_panel_exists(hass, DASHBOARD_URL):
            return True
        result = await hass.async_add_executor_job(
            register_dashboard, hass.config.config_dir
        )
        if result == "existing_lovelace":
            _LOGGER.warning(
                "MG4 Cockpit dashboard was not registered automatically because "
                "configuration.yaml already contains a Lovelace section. "
                "Existing Lovelace settings are not modified"
            )
        elif result != "added":
            _LOGGER.warning("MG4 Cockpit dashboard registration: %s", result)
    except Exception:
        # Never prevent Home Assistant from loading because dashboard setup failed.
        _LOGGER.exception("MG4 Cockpit dashboard auto-registration failed")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Keep user-created files and dashboard settings on removal."""
    return True
