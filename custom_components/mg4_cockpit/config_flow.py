"""Config flow for preparing the existing MG4 Cockpit YAML assets."""
from __future__ import annotations
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import persistent_notification
from homeassistant.helpers import selector
from .discovery import find_vehicles
from .installer import ExistingFilesError, prepare_files, VIN_RE

_LOGGER = logging.getLogger(__name__)
DOMAIN = "mg4_cockpit"

class MG4CockpitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        await self.async_set_unique_id("mg4_cockpit_installation")
        self._abort_if_unique_id_configured()
        vehicles = find_vehicles(self.hass)
        if vehicles:
            return await self.async_step_vehicle()
        return await self.async_step_manual()

    async def async_step_vehicle(self, user_input=None):
        vehicles = find_vehicles(self.hass)
        if not vehicles:
            return await self.async_step_manual()
        if user_input is not None:
            vin = user_input.get("vehicle", "")
            if vin in vehicles:
                return await self._install(vin, "vehicle")
        return self.async_show_form(
            step_id="vehicle",
            data_schema=vol.Schema({vol.Required("vehicle"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=vehicles, mode=selector.SelectSelectorMode.DROPDOWN))}),
            errors={},
        )

    async def async_step_manual(self, user_input=None):
        if user_input is not None:
            vin = user_input.get("vin", "").strip().upper()
            if VIN_RE.fullmatch(vin):
                return await self._install(vin, "manual")
            return self.async_show_form(step_id="manual", data_schema=vol.Schema({vol.Required("vin"): str}), errors={"base": "invalid_vin"})
        return self.async_show_form(step_id="manual", data_schema=vol.Schema({vol.Required("vin"): str}), errors={})

    async def _install(self, vin, step_id):
        try:
            await self.hass.async_add_executor_job(prepare_files, self.hass.config.config_dir, vin)
        except ExistingFilesError:
            error = "file_exists"
        except Exception:
            _LOGGER.exception("MG4 Cockpit files could not be prepared")
            error = "write_failed"
        else:
            # YAML packages are read during Home Assistant startup. Show this
            # once, immediately after the assets are generated, not on every boot.
            persistent_notification.async_create(
                self.hass,
                "MG4 Cockpit panon oluşturuldu. Türkçe durumlar ve sürüş analizleri gibi "
                "yeni sensörlerin çalışması için Home Assistant'ı bir kez daha yeniden başlat. "
                "Yeniden başlatmadan önce bazı kartlarda 'Unavailable' görmen normal.",
                title="MG4 Cockpit – Kurulum tamamlandı",
                notification_id="mg4_cockpit_restart_required",
            )
            # Do not store VIN in the config entry; it is present in the generated local YAML.
            return self.async_create_entry(title="MG4 Cockpit Kurulum", data={})
        if step_id == "vehicle":
            vehicles = find_vehicles(self.hass)
            return self.async_show_form(step_id="vehicle", data_schema=vol.Schema({vol.Required("vehicle"): selector.SelectSelector(selector.SelectSelectorConfig(options=vehicles, mode=selector.SelectSelectorMode.DROPDOWN))}), errors={"base": error})
        return self.async_show_form(step_id="manual", data_schema=vol.Schema({vol.Required("vin"): str}), errors={"base": error})
