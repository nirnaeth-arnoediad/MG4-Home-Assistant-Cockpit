# MG4 Cockpit v0.6.0-beta.1 — Test planı

1. v0.5.0-beta.3 kurulumundan tam yedek al.
2. v0.6'yı HACS'ten yükle ve HA'yı yeniden başlat. Pano değişmemeli.
3. Güncelleme bildirimi gelmeli.
4. Entegrasyon → Yapılandır → Güncelle → Onayla.
5. `/config/mg4_cockpit_backups/` altında UI JSON ve 6 YAML yedeğini doğrula.
6. Yedi sekme, sensörler, EPİAŞ koşulları çalışmalı.
7. `configuration.yaml` önce/sonra birebir aynı kalmalı.
8. Entegrasyon → Yapılandır → Son yedeğe dön → Onayla.
9. Önceki pano ve YAML dosyaları birebir geri gelmeli.
10. Pano üzerinde elle değişiklik yapıp güncelleme uyarısını test et.

Not: Bu sürümde güncelleme kullanıcı değişikliklerini birleştirmez, yedekleyip üzerine yazar.
