# MG4 Home Assistant Cockpit

**Türkçe / English** · Community project · Private-first development

MG4 Home Assistant dashboard with charging, battery preheating, Turkish labels, drive analytics and an **optional** EPİAŞ hourly electricity-price module.

> **Status:** Source distribution / advanced manual setup. Not a HACS integration or one-click install. Tested on the owner's setup only; your gateway entity names may differ. No Anker EVSE integration is bundled yet.

## Türkçe kurulum

1. Home Assistant'ın tam yedeğini alın. SAIC/iSmart MQTT gateway'i ve dashboardun kullandığı özel kartları önceden kurun; gerekli entity ID'lerin mevcut olduğunu doğrulayın.
2. Yerel bilgisayarınızda `python3 tools/configure_vin.py --vin KENDI_17_HANELI_VIN --output local` komutunu çalıştırın. **`local/` klasörünü GitHub'a yüklemeyin.**
3. `local/packages/*.yaml` dosyalarını HA `/config/packages/` içine kopyalamadan önce mevcut helper/automation tanımlarınızla çakışmaları kontrol edin. `homeassistant: packages: !include_dir_named packages` ayarı mevcut olmalı.
4. `local/dashboards/mg4_cockpit.yaml` içeriğini yeni bir YAML-mode dashboarda aktarın. Entity ID'leriniz VIN tabanlı değilse ayrıca eşleştirme yapın.
5. HA yapılandırma kontrolünü çalıştırın; ardından uygun zamanda yeniden başlatın. Şarj/ön ısıtma kontrollerini gözetim altında test edin.
6. EPİAŞ kullanacaksanız `epias/README.md` adımlarını **ayrıca** uygulayın. Varsayılan dashboard EPİAŞ olmadan çalışacak şekilde ayrılmıştır.

**Not:** Dashboardda özel kart bağımlılıkları ve mevcut HA helper'ları bulunabilir. Paketler yeni bir kurulumda otomatik olarak eksiksiz çalışacağı garanti edilmez. Bu repo mevcut çalışan yapılandırmadan ayrıştırılmış bir başlangıç sürümüdür.

## English setup

1. Back up Home Assistant. Install your SAIC/iSmart MQTT gateway and any required custom Lovelace cards.
2. Locally run `python3 tools/configure_vin.py --vin YOUR_17_CHARACTER_VIN --output local`. **Never commit `local/`**.
3. Review `local/packages/*.yaml` for helper and automation conflicts, then copy to `/config/packages/` with packages enabled in your HA configuration.
4. Import `local/dashboards/mg4_cockpit.yaml` into a YAML dashboard. Adapt entity names if your gateway uses a different naming scheme.
5. Validate HA configuration and test vehicle controls carefully.
6. For Turkish electricity pricing, see the independent opt-in `epias/README.md`.

## Modules

| Module | Path | Optional? |
|---|---|---|
| MG4 dashboard | `dashboards/` | Main UI |
| Drive/charging helpers | `packages/` | Depends on selected features |
| EPİAŞ PTF | `epias/` | **Yes** |
| Local VIN renderer | `tools/configure_vin.py` | Installation aid |

## Privacy & safety

Do not commit your VIN, SAIC account credentials, `secrets.yaml`, location data, access tokens, IP addresses, or personal automations. The source templates contain `YOUR_VIN`, not a real vehicle identifier. Keep this repository **Private** until a fresh-install test and final review. Vehicle commands may have real-world effects; never expose HA or Modbus control endpoints directly to the internet.

## License

MIT for original repository material; check third-party custom-card and gateway licenses separately. No affiliation with MG, SAIC, Anker or EPİAŞ.
