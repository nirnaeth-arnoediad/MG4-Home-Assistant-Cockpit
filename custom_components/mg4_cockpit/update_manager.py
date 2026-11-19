"""Explicitly approved MG4 dashboard/package updates with local backups.

Never writes configuration.yaml or .storage directly. Existing files are never
replaced until the user confirms through the integration options flow.
"""
from __future__ import annotations
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from homeassistant.helpers.storage import Store

_LOGGER = logging.getLogger(__name__)
STORE_KEY = "mg4_cockpit_update_state"
DASHBOARD_URL = "mg4-cockpit-hacs"
DASHBOARD_FILE = "mg4_cockpit_dashboard.yaml"
PACKAGE_NAMES = ("mg4_analiz_yardimcilari.yaml", "mg4_batarya_isitma.yaml", "mg4_ek_analizler.yaml", "mg4_sarj_oturumu.yaml", "mg4_turkce_durumlar.yaml")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_vin(root: Path):
    """Recover VIN from generated package entity references, not UI state."""
    import re
    for file in sorted((root / "packages").glob("mg4_cockpit_*.yaml")):
        content = file.read_text(encoding="utf-8")
        match = re.search(r"(?:sensor|binary_sensor|switch|button|number|select)\.([a-hj-npr-z0-9]{17})_", content, re.I)
        if match:
            return match.group(1).lower()
    return None


def asset_targets(root: Path):
    assets = Path(__file__).parent / "assets"
    pairs = [(assets / "dashboards" / "mg4_cockpit.yaml", root / DASHBOARD_FILE)]
    pairs += [(assets / "packages" / name, root / "packages" / ("mg4_cockpit_" + name)) for name in PACKAGE_NAMES]
    return pairs


async def get_state(hass):
    return await Store(hass, 1, STORE_KEY).async_load() or {}


async def save_state(hass, state):
    await Store(hass, 1, STORE_KEY).async_save(state)


async def dashboard_config(hass):
    """Read the current UI-created dashboard via the HA Lovelace API."""
    from homeassistant.components.lovelace import LOVELACE_DATA
    lovelace = hass.data.get(LOVELACE_DATA)
    if not lovelace or DASHBOARD_URL not in lovelace.dashboards:
        raise RuntimeError("MG4 Cockpit panosu bulunamadı; güncelleme iptal edildi")
    board = lovelace.dashboards[DASHBOARD_URL]
    config = await board.async_load(False)
    if not isinstance(config, dict) or not isinstance(config.get("views"), list):
        raise RuntimeError("Mevcut pano yapılandırması okunamadı")
    return board, config


async def status(hass):
    root = Path(hass.config.config_dir)
    pairs = asset_targets(root)
    if not all(target.is_file() and source.is_file() for source, target in pairs):
        return {"ready": False, "reason": "Kurulum dosyalarından biri eksik"}
    state = await get_state(hass)
    local_hashes = {str(target.relative_to(root)): digest(target.read_bytes()) for _, target in pairs}
    vin = find_vin(root)
    source_hashes = {str(target.relative_to(root)): digest(source.read_text(encoding="utf-8").replace("YOUR_VIN", vin).encode("utf-8")) for source, target in pairs} if vin else {}
    baseline = state.get("hashes") or {}
    changed = sorted(key for key, val in local_hashes.items() if baseline.get(key) != val)
    unverified = not bool(baseline)
    ui_modified = None
    if state.get("ui_hash"):
        try:
            _, current_ui = await dashboard_config(hass)
            ui_modified = digest(json.dumps(current_ui, sort_keys=True, ensure_ascii=False).encode("utf-8")) != state["ui_hash"]
        except Exception:
            ui_modified = None
    available = not source_hashes or any(local_hashes[key] != source_hashes[key] for key in local_hashes)
    return {"ready": True, "available": available, "modified": changed, "unverified": unverified, "ui_modified": ui_modified,
            "local_hashes": local_hashes, "source_hashes": source_hashes,
            "last_backup": state.get("last_backup")}


async def establish_baseline(hass):
    """Called after first installation, not for migrated installs."""
    state = await get_state(hass)
    if state.get("hashes"):
        return
    root = Path(hass.config.config_dir)
    pairs = asset_targets(root)
    if not all(target.is_file() for _, target in pairs):
        return
    state["hashes"] = {str(target.relative_to(root)): digest(target.read_bytes()) for _, target in pairs}
    state["asset_version"] = "0.6.0-beta.1"
    await save_state(hass, state)


async def establish_ui_baseline(hass):
    state = await get_state(hass)
    if state.get("ui_hash"):
        return
    try:
        _, config = await dashboard_config(hass)
    except Exception:
        return
    state["ui_hash"] = digest(json.dumps(config, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    await save_state(hass, state)


async def apply_update(hass):
    """Backup first, then apply; restore all files and dashboard on error."""
    import yaml
    root = Path(hass.config.config_dir)
    info = await status(hass)
    if not info["ready"]:
        raise RuntimeError(info["reason"])
    board, old_config = await dashboard_config(hass)
    pairs = asset_targets(root)
    new_config = yaml.safe_load((Path(__file__).parent / "assets/dashboards/mg4_cockpit.yaml").read_text(encoding="utf-8"))
    if not isinstance(new_config, dict) or not isinstance(new_config.get("views"), list):
        raise RuntimeError("Yeni pano dosyası geçersiz")
    # Existing generated dashboard file contains the selected VIN. Preserve it
    # in the new dashboard, rather than copying a YOUR_VIN template.
    vin = find_vin(root)
    if not vin:
        raise RuntimeError("Araç VIN'i mevcut MG4 paketlerinde bulunamadı; otomatik güncelleme durduruldu")
    rendered = {}
    for source, target in pairs:
        content = source.read_text(encoding="utf-8").replace("YOUR_VIN", vin)
        if "YOUR_VIN" in content:
            raise RuntimeError("Yeni pakette VIN alanı çözümlenemedi")
        rendered[target] = content.encode("utf-8")
    new_config = yaml.safe_load(rendered[root / DASHBOARD_FILE])
    if not isinstance(new_config, dict) or not isinstance(new_config.get("views"), list):
        raise RuntimeError("Yeni pano yapılandırması geçersiz")
    # Unique, non-overwriting backup. The backup includes actual UI storage
    # config (not just the generated YAML file).
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = root / "mg4_cockpit_backups" / stamp
    backup.mkdir(parents=True, exist_ok=False)
    old_files = {target: target.read_bytes() for _, target in pairs}
    for target, content in old_files.items():
        path = backup / target.relative_to(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (backup / "dashboard_ui.json").write_text(json.dumps(old_config, ensure_ascii=False, indent=2), encoding="utf-8")
    (backup / "manifest.json").write_text(json.dumps({"created_utc": stamp, "files": sorted(str(t.relative_to(root)) for t in old_files)}, indent=2), encoding="utf-8")
    try:
        for target, content in rendered.items():
            target.write_bytes(content)
        await board.async_save(new_config)
    except Exception:
        for target, content in old_files.items():
            target.write_bytes(content)
        try:
            await board.async_save(old_config)
        except Exception:
            _LOGGER.exception("Pano geri yüklenemedi; yedek: %s", backup)
        raise
    state = await get_state(hass)
    state["hashes"] = {str(t.relative_to(root)): digest(t.read_bytes()) for _, t in pairs}
    state["asset_version"] = "0.6.0-beta.1"
    state["last_backup"] = stamp
    state["ui_hash"] = digest(json.dumps(new_config, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    await save_state(hass, state)
    return stamp


async def rollback(hass):
    root = Path(hass.config.config_dir)
    state = await get_state(hass)
    stamp = state.get("last_backup")
    if not stamp or "/" in stamp or ".." in stamp:
        raise RuntimeError("Geri dönüş için yedek bulunamadı")
    backup = root / "mg4_cockpit_backups" / stamp
    board, current_config = await dashboard_config(hass)
    old_config = json.loads((backup / "dashboard_ui.json").read_text(encoding="utf-8"))
    pairs = asset_targets(root)
    original = {}
    for _, target in pairs:
        old = backup / target.relative_to(root)
        if not old.is_file():
            raise RuntimeError("Yedek eksik; geri dönüş iptal edildi")
        original[target] = old.read_bytes()
    current_files = {target: target.read_bytes() for _, target in pairs}
    try:
        for target, content in original.items():
            target.write_bytes(content)
        await board.async_save(old_config)
    except Exception:
        for target, content in current_files.items():
            target.write_bytes(content)
        try:
            await board.async_save(current_config)
        except Exception:
            _LOGGER.exception("Geri dönüşte pano kurtarma başarısız")
        raise
    state["hashes"] = {str(t.relative_to(root)): digest(t.read_bytes()) for _, t in pairs}
    state["last_backup"] = None
    state["ui_hash"] = digest(json.dumps(old_config, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    state["asset_version"] = "rollback"
    await save_state(hass, state)
