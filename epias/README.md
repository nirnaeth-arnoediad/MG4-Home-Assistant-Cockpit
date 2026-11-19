# EPİAŞ PTF — OPTIONAL / İSTEĞE BAĞLI

This module is **not required** for the MG4 dashboard. Türkiye-specific hourly PTF data only; prices are **not** a guaranteed final bill.

1. Install `bash`, `curl` and `jq` in the environment that executes the command-line sensor.
2. Copy `epias_ptf.sh` to HA `/config/epias_ptf.sh`; make it executable if needed.
3. Add `epias_username` and `epias_password` to **your local** `/config/secrets.yaml`, never to this repo. The script reads them locally.
4. Merge `sensor.example.yaml` into your existing `configuration.yaml` (do not duplicate `command_line:` keys).
5. Add the automation from `automation.example.yaml` to your existing automations; confirm your actual entity ID in Developer Tools (it may be suffixed `_2`).
6. Test the script and sensor manually, then verify the HH:02 scheduled update.
7. **Only then** insert the cards in `dashboard_cards.optional.yaml` at the beginning of the Energy section. The cards use `sensor.epias_guncel_ptf_kwh_2` by default: adapt to your entity ID.

**Billing caution:** Example cards assume YEKDEM 0.48886 TL/kWh, supplier markup 4.95%, distribution 2.4249 TL/kWh, electricity tax 5% and VAT 10%. These are provisional assumptions and must be checked against current regulation and your contract. They are not real-time official tariff feeds. The hour label is inferred from sensor update time, not independently validated against the API's pricing period.

**Security:** Do not print tokens, log raw auth responses or commit a populated `secrets.yaml`. EPİAŞ account credentials are required for this implementation.
