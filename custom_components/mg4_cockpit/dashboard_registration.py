"""Register a storage dashboard through Home Assistant's Lovelace collection.

No configuration.yaml or .storage files are edited directly.
This uses HA internal collection APIs and requires validation on Core 2026.11.2.
"""
from __future__ import annotations
import logging
from pathlib import Path
import yaml

_LOGGER = logging.getLogger(__name__)
DASHBOARD_URL = "mg4-cockpit-hacs"
DASHBOARD_FILENAME = "mg4_cockpit_dashboard.yaml"

async def register_dashboard(hass):
    from homeassistant.components import frontend
    from homeassistant.components.lovelace import LOVELACE_DATA
    from homeassistant.components.lovelace.dashboard import DashboardsCollection, LovelaceStorage

    path = Path(hass.config.config_dir) / DASHBOARD_FILENAME
    if not path.is_file():
        _LOGGER.warning("MG4 Cockpit pano dosyası bulunamadı: %s", path)
        return "missing_dashboard"

    lovelace = hass.data.get(LOVELACE_DATA)
    if lovelace is None:
        _LOGGER.warning("MG4 Cockpit: Lovelace henüz hazır değil")
        return "lovelace_not_ready"
    # v0.4 installed a YAML panel at this same URL. Do not overwrite or
    # remove that user's configuration. Explicit migration is required.
    if frontend.async_panel_exists(hass, DASHBOARD_URL):
        return "existing_panel"

    def load_yaml():
        with path.open(encoding="utf-8") as stream:
            return yaml.safe_load(stream)
    config = await hass.async_add_executor_job(load_yaml)
    if not isinstance(config, dict) or not isinstance(config.get("views"), list):
        raise ValueError("MG4 Cockpit dashboard YAML must contain views")

    collection = DashboardsCollection(hass)
    await collection.async_load()
    existing = next((item for item in collection.async_items()
                     if item.get("url_path") == DASHBOARD_URL), None)
    if existing is not None:
        return "existing_storage"

    # Register a listener before creation so the sidebar appears immediately.
    async def changed(change_type, item_id, item):
        if item.get("url_path") != DASHBOARD_URL:
            return
        if change_type == "added":
            lovelace.dashboards[DASHBOARD_URL] = LovelaceStorage(hass, item)
            frontend.async_register_built_in_panel(
                hass, "lovelace", frontend_url_path=DASHBOARD_URL,
                require_admin=False, show_in_sidebar=True,
                sidebar_title="MG4 Cockpit (HACS)",
                sidebar_icon="mdi:car-electric", config={"mode": "storage"})
    # HA collection event constants can differ; explicitly register the
    # panel after creation below instead of relying on event notifications.
    item = await collection.async_create_item({
        "url_path": DASHBOARD_URL, "title": "MG4 Cockpit (HACS)",
        "icon": "mdi:car-electric", "show_in_sidebar": True,
        "require_admin": False,
    })
    store = LovelaceStorage(hass, item)
    await store.async_save(config)
    lovelace.dashboards[DASHBOARD_URL] = store
    if not frontend.async_panel_exists(hass, DASHBOARD_URL):
        frontend.async_register_built_in_panel(
            hass, "lovelace", frontend_url_path=DASHBOARD_URL,
            require_admin=False, show_in_sidebar=True,
            sidebar_title="MG4 Cockpit (HACS)",
            sidebar_icon="mdi:car-electric", config={"mode": "storage"})
    return "created"
