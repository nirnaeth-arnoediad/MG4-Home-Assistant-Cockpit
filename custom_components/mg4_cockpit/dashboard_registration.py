"""Safely register the generated YAML dashboard in Home Assistant config.

Home Assistant does not automatically register a YAML dashboard just because a
YAML file exists. This module adds a *new* dashboard entry only when the user
has no top-level Lovelace configuration. It never modifies an existing Lovelace
section, dashboard, or .storage file.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
import re

_LOGGER = logging.getLogger(__name__)
DASHBOARD_FILENAME = "mg4_cockpit_dashboard.yaml"
DASHBOARD_URL = "mg4-cockpit-hacs"
_DASHBOARD_CONFIG = """
# MG4 Cockpit (HACS) - otomatik pano kaydi
lovelace:
  dashboards:
    mg4-cockpit-hacs:
      mode: yaml
      filename: mg4_cockpit_dashboard.yaml
      title: MG4 Cockpit (HACS)
      icon: mdi:car-electric
      show_in_sidebar: true
"""
_TOP_LEVEL_LOVELACE = re.compile(r"^(?:lovelace|['\"]lovelace['\"])\s*:", re.MULTILINE)


def register_dashboard(config_dir: str) -> str:
    """Register dashboard for the next HA restart; preserve all user settings.

    Returns one of: added, existing_lovelace, missing_dashboard,
    missing_configuration. An existing Lovelace section is never edited because
    it may be a YAML include or have unrelated user dashboards/resources.
    """
    root = Path(config_dir)
    dashboard = root / DASHBOARD_FILENAME
    config = root / "configuration.yaml"
    if not dashboard.is_file():
        return "missing_dashboard"
    if not config.is_file():
        return "missing_configuration"
    original = config.read_text(encoding="utf-8-sig")
    if _TOP_LEVEL_LOVELACE.search(original):
        return "existing_lovelace"

    # The backup is created only once; never overwrite a previous backup.
    backup = root / "configuration.yaml.mg4_cockpit_backup"
    try:
        with backup.open("x", encoding="utf-8") as handle:
            handle.write(original)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        pass

    # Keep the original file, ownership, and permissions intact.
    suffix = "" if not original or original.endswith("\n") else "\n"
    content = suffix + _DASHBOARD_CONFIG
    original_size = config.stat().st_size
    try:
        with config.open("a", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        # Restore only the bytes added by this operation when possible.
        with config.open("r+b") as handle:
            handle.truncate(original_size)
        raise
    _LOGGER.warning(
        "MG4 Cockpit dashboard registered in configuration.yaml; "
        "restart Home Assistant to show it in the sidebar"
    )
    return "added"
