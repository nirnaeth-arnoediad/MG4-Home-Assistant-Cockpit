#!/usr/bin/env python3
"""Render local MG4 YAML copies; do not commit generated files."""
import argparse, pathlib, re
p=argparse.ArgumentParser()
p.add_argument("--vin",required=True,help="17-character VIN, used only locally")
p.add_argument("--output",default="local",help="Local output directory")
a=p.parse_args()
if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}",a.vin.upper()):
    p.error("VIN must be 17 alphanumeric characters (excluding I, O, Q)")
base=pathlib.Path(__file__).resolve().parents[1]
out=pathlib.Path(a.output).resolve()
for section in ("dashboards", "packages"):
    for src in (base/section).glob("*.yaml"):
        dest=out/section/src.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(src.read_text().replace("YOUR_VIN",a.vin.lower()),encoding="utf-8")
print("Local configuration created in:",out)
print("WARNING: Output includes your VIN. Never commit or share it.")
