# HACS 0.4.0-beta.1 — Otomatik dashboard test planı

**Ön koşul:** Mevcut MG4 Cockpit entegrasyonu çalışıyor ve `/config/mg4_cockpit_dashboard.yaml` dosyası mevcut. Önce `configuration.yaml` dosyasını yedekleyin.

1. `main` dalına güncel dosyaları yükleyin, HACS üzerinden güncelleyin, Home Assistant'ı yeniden başlatın.
2. `/config/configuration.yaml` içinde `lovelace:` yoksa entegrasyonun `mg4-cockpit-hacs` panosunu otomatik eklediğini doğrulayın.
3. `/config/configuration.yaml.mg4_cockpit_backup` dosyasının oluştuğunu doğrulayın.
4. Home Assistant yapılandırma kontrolünü çalıştırın. Hata yoksa yeniden başlatın.
5. Sol menüde `MG4 Cockpit (HACS)` panosunu ve yedi sekmeyi doğrulayın.
6. Yeniden başlatma sonrasında `lovelace:` bölümünün iki kez eklenmediğini doğrulayın.
7. Eski dashboardların, EPİAŞ sensörünün ve SAIC Gateway'in etkilenmediğini kontrol edin.
8. Özel kart eksikse HACS'ten kurun; bu entegrasyon özel kartları otomatik kurmaz.

**Beklenen güvenli davranış:** Mevcut bir `lovelace:` bölümü varsa dosya değiştirilmez; günlükte uyarı görünür. Otomatik pano kaydı gerçek Home Assistant üzerinde henüz test edilmemiştir.
