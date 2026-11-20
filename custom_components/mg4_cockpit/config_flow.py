"""Config flow for preparing the existing MG4 Cockpit YAML assets."""
from __future__ import annotations
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import persistent_notification
from homeassistant.helpers import selector
from .discovery import find_vehicles
from .installer import ExistingFilesError, prepare_files, VIN_RE
from .update_manager import status, apply_update, rollback, establish_baseline

_LOGGER = logging.getLogger(__name__)
DOMAIN = "mg4_cockpit"

class MG4CockpitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return MG4CockpitOptionsFlow()

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
            # Fresh install: save the generated files as the initial baseline.
            await establish_baseline(self.hass)
            return self.async_create_entry(title="MG4 Cockpit Kurulum", data={})
        if step_id == "vehicle":
            vehicles = find_vehicles(self.hass)
            return self.async_show_form(step_id="vehicle", data_schema=vol.Schema({vol.Required("vehicle"): selector.SelectSelector(selector.SelectSelectorConfig(options=vehicles, mode=selector.SelectSelectorMode.DROPDOWN))}), errors={"base": error})
        return self.async_show_form(step_id="manual", data_schema=vol.Schema({vol.Required("vin"): str}), errors={"base": error})


RELEASE_NOTES = 'BETA v0.6.0-beta.3: Sürüş analizinde yeterli veri mesajları, daha anlaşılır sayaçlar ve sonuç açıklamaları eklendi. Geçici rollback test butonu kaldırıldı.'

class MG4CockpitOptionsFlow(config_entries.OptionsFlow):
    """User approval is mandatory for update and rollback."""

    async def async_step_init(self, user_input=None):
        info = await status(self.hass)
        if user_input is not None:
            action = user_input.get("action")
            if action == "update":
                return await self.async_step_confirm()
            if action == "rollback":
                return await self.async_step_rollback()
            return self.async_create_entry(title="", data={})
        actions = ["update"]
        if info.get("last_backup"):
            actions.append("rollback")
        description = "Mevcut pano ve paketler korunuyor. Güncelleme yalnızca onayından sonra yapılır."
        if not info.get("ready"):
            description = "Kurulum dosyaları eksik. Güncelleme yapmadan önce dosyaları kontrol et."
        elif info.get("unverified"):
            description = "Bu kurulum eski sürümden geldiği için önceki dosya değişiklikleri doğrulanamıyor. Güncelleme, kişisel düzenlemelerini değiştirebilir. Önce yedek alınacak."
        elif info.get("ui_modified"):
            description = "Panonu Home Assistant üzerinden değiştirmişsin. Güncelleme mevcut düzenini yedekleyip yeni sürümle değiştirecek."
        elif info.get("modified"):
            description = "Bazı dosyaları kurulumdan sonra değiştirmişsin. Güncelleme bunların üzerine yazacak; önce yedek alınacak."
        elif not info.get("available"):
            description = "Yerel YAML dosyaları bu sürümle aynı. Yine de panoyu yenilemek istersen onay verebilirsin."
        return self.async_show_form(step_id="init", description_placeholders={"message": description}, data_schema=vol.Schema({vol.Required("action"): selector.SelectSelector(selector.SelectSelectorConfig(options=[selector.SelectOptionDict(value="update", label="Dashboardu güncelle"), *([selector.SelectOptionDict(value="rollback", label="Son yedeğe dön")] if "rollback" in actions else [])], mode=selector.SelectSelectorMode.DROPDOWN))}))

    async def async_step_confirm(self, user_input=None):
        info = await status(self.hass)
        if not info.get("ready"):
            return self.async_abort(reason="missing_files")
        if user_input is not None:
            if not user_input.get("confirm"):
                return self.async_abort(reason="cancelled")
            package_changed = any(
                key.startswith("packages/") and info.get("local_hashes", {}).get(key) != info.get("source_hashes", {}).get(key)
                for key in info.get("source_hashes", {})
            )
            try:
                backup = await apply_update(self.hass)
            except Exception:
                _LOGGER.exception("MG4 Cockpit güncellemesi başarısız")
                return self.async_show_form(step_id="confirm", data_schema=vol.Schema({vol.Required("confirm", default=False): bool}), errors={"base": "update_failed"})
            from homeassistant.components import persistent_notification
            persistent_notification.async_create(self.hass, ("Pano güncellendi. Yedeğin /config/mg4_cockpit_backups/ klasöründe.\n\n" + RELEASE_NOTES + ("\n\nYAML paketleri değişti. Yeni sensör tanımlarının yüklenmesi için Home Assistant'ı yeniden başlat." if package_changed else "\n\nYAML paketleri değişmedi; ikinci yeniden başlatma gerekmiyor.")), title="MG4 Cockpit güncellendi", notification_id="mg4_cockpit_update")
            return self.async_create_entry(title="", data={"last_action": "update", "backup": backup})
        return self.async_show_form(step_id="confirm", data_schema=vol.Schema({vol.Required("confirm", default=False): bool}), description_placeholders={"message": "Mevcut panonun ve beş YAML paketinin yedeği alınacak. Kişisel düzenlemelerin üzerine yazılabilir. İstersen son yedeğe dönebilirsin.\n\nBu sürümde: " + RELEASE_NOTES})

    async def async_step_rollback(self, user_input=None):
        if user_input is not None:
            if not user_input.get("confirm"):
                return self.async_abort(reason="cancelled")
            try:
                await rollback(self.hass)
            except Exception:
                _LOGGER.exception("MG4 Cockpit geri dönüş başarısız")
                return self.async_show_form(step_id="rollback", data_schema=vol.Schema({vol.Required("confirm", default=False): bool}), errors={"base": "rollback_failed"})
            return self.async_create_entry(title="", data={"last_action": "rollback"})
        return self.async_show_form(step_id="rollback", data_schema=vol.Schema({vol.Required("confirm", default=False): bool}))
