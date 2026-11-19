# İlk Home Assistant testi

**Önce tam yedek alın.** Testi temiz bir Home Assistant örneğinde gerçekleştirin; SAIC Gateway ve MQTT Discovery kurulu olmalı.

1. HACS özel depo olarak yükleme ve HA yeniden başlatma.
2. Entegrasyon ekleme ekranında MG4 VIN'inin algılanması; algılanmazsa manuel VIN ile devam.
3. `/config/packages` içinde beş dosya ve `/config/mg4_cockpit_dashboard.yaml` oluştuğunu doğrulama.
4. `configuration.yaml` içinde packages ve YAML dashboard tanımlarını etkinleştirme; config kontrolü.
5. Özel kartların HACS'ten kurulması, dashboardun 7 sekmesinin açılması.
6. Kontrollerin doğru araçla eşleştiğini doğrulama; **aracı etkileyen komutları yalnızca güvenli koşullarda deneyin**.
7. Aynı kurulumun tekrar denenmesinde mevcut dosyaların üzerine yazılmadığını doğrulama.
8. HA günlüklerinde hata ve eksik varlık kontrolü; analiz verilerinin birikmesini bekleme.

Bu sürüm **tam otomatik HACS kurulumu değildir**. Dashboard ve packages yapılandırması manuel kaldığı için başarı kriteri tüm dosyaların sorunsuz kurulması ve dashboardun açılmasıdır.
