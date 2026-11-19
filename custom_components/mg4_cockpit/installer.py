"""Prepare MG4 Cockpit assets without overwriting existing user files."""
from __future__ import annotations
from pathlib import Path
import re

VIN_RE = re.compile(r"[A-HJ-NPR-Z0-9]{17}\Z", re.IGNORECASE)
class ExistingFilesError(Exception):
    """Target already exists; user data must not be replaced."""

def prepare_files(config_dir: str, vin: str) -> list[str]:
    vin = vin.strip().upper()
    if not VIN_RE.fullmatch(vin):
        raise ValueError("invalid_vin")
    assets = Path(__file__).parent / "assets"
    root = Path(config_dir)
    jobs = [(p, root / "packages" / f"mg4_cockpit_{p.name}") for p in sorted((assets / "packages").glob("*.yaml"))]
    jobs.append((assets / "dashboards" / "mg4_cockpit.yaml", root / "mg4_cockpit_dashboard.yaml"))
    if len(jobs) != 6:
        raise RuntimeError("Expected five packages and one dashboard")
    if any(target.exists() for _, target in jobs):
        raise ExistingFilesError("One or more MG4 files already exist")
    # Read and validate every source BEFORE writing any file.
    contents = []
    for source, target in jobs:
        content = source.read_text(encoding="utf-8").replace("YOUR_VIN", vin.lower())
        if "YOUR_VIN" in content:
            raise RuntimeError("Unresolved VIN placeholder")
        contents.append((target, content))
    created = []
    try:
        for target, content in contents:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("x", encoding="utf-8") as stream:
                created.append(target)
                stream.write(content)
    except Exception:
        for target in created:
            target.unlink(missing_ok=True)
        raise
    return [str(target) for target, _ in contents]
