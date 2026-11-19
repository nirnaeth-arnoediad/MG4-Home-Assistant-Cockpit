#!/usr/bin/env python3
"""Yerel MG4 YAML kopyaları üretir; çıktıları GitHub’a yüklemeyin."""
import argparse, pathlib, re
p=argparse.ArgumentParser()
p.add_argument("--vin",required=True,help="17 karakterlik VIN; yalnızca yerel kullanım")
p.add_argument("--output",default="local",help="Yerel çıktı klasörü")
a=p.parse_args()
if not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}",a.vin.upper()):
    p.error("VIN 17 karakter olmalı (I, O, Q hariç)")
base=pathlib.Path(__file__).resolve().parents[1]
out=pathlib.Path(a.output).resolve()
for section in ("dashboards", "packages"):
    for src in (base/section).glob("*.yaml"):
        dest=out/section/src.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(src.read_text().replace("YOUR_VIN",a.vin.lower()),encoding="utf-8")
print("Yerel yapılandırma oluşturuldu:",out)
print("UYARI: Çıktı VIN içerir. GitHub’a yüklemeyin.")
