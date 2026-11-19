"""MG4 Cockpit YAML installation helper; no vehicle polling or control."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """YAML files are installed during the explicit config flow."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Do not delete user YAML files on integration removal."""
    return True
