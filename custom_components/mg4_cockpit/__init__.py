"""MG4 Cockpit installation helper."""
from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .dashboard_registration import register_dashboard
from .update_manager import status, establish_ui_baseline

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
        if result == "created":
            await establish_ui_baseline(hass)
        if result in ("created", "existing_storage", "existing_panel"):
            info = await status(hass)
            if info.get("ready") and info.get("available"):
                from homeassistant.components import persistent_notification
                persistent_notification.async_create(
                    hass,
                    "MG4 Cockpit için yeni pano dosyaları var. Mevcut panon değişmedi. "
                    "Ayarlar → Cihazlar ve Hizmetler → MG4 Cockpit Kurulum → Yapılandır "
                    "bölümünden güncellemeyi inceleyip onaylayabilirsin.",
                    title="MG4 Cockpit güncellemesi hazır",
                    notification_id="mg4_cockpit_update_available",
                )
        if result not in ("created", "existing_panel", "existing_storage"):
            _LOGGER.warning("MG4 Cockpit pano durumu: %s", result)
    except Exception:
        _LOGGER.exception("MG4 Cockpit panosu oluşturulamadı")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
