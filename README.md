# MG4 Cockpit v0.6.0-beta.3 — BETA

> **BETA:** Bu sürüm test aşamasındadır. Kurulum veya güncelleme öncesinde Home Assistant yedeği alın.

MG4 Cockpit, SAIC iSmart MQTT Gateway üzerinden Home Assistant'a aktarılan araç bilgilerini tek bir Türkçe panoda toplar. Kokpit, enerji ve şarj, konfor, araç durumu, konum, sürüş analizi ve sistem ekranlarını içerir.

![MG4 Cockpit](docs/images/kokpit.png)

| Kokpit | Şarj | Analiz |
|---|---|---|
| ![Kokpit](docs/images/kokpit.png) | ![Şarj](docs/images/sarj.png) | ![Analiz](docs/images/menzil-analizi.png) |

## Gereksinimler

- Home Assistant ve HACS / Marketplace kurulu olmalı.
- [SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway) çalışmalı; MQTT Discovery aracılığıyla MG4 varlıkları Home Assistant'ta görünmeli.
- Şu özel kartlar HACS üzerinden yüklenmeli: `button-card`, `mushroom`, `apexcharts-card`, `config-template-card`, `ha-openfreemap-card`.
- Home Assistant'ta YAML paketleri etkin olmalı. `configuration.yaml` dosyasında mevcut bir `homeassistant:` bölümü varsa altına eklenerek şu ayar bulunmalı:

  ```yaml
  homeassistant:
    packages: !include_dir_named packages
  ```

  Bu ayar yalnızca yoksa ve mevcut yapılandırmayla birleştirilerek eklenmelidir. MG4 Cockpit entegrasyonu `configuration.yaml` dosyasını kendisi değiştirmez.
- Kuruluma başlamadan önce Home Assistant yedeği alın. Aynı MG4 paketlerinin başka bir kurulumdan kalan kopyalarıyla çakışma olmamalı.

## Kurulum

1. HACS / Marketplace'te bu GitHub deposunu **Integration** türünde özel depo olarak ekleyin ve **MG4 Cockpit Kurulum** entegrasyonunu indirin.
2. **Home Assistant'ı yeniden başlatın.** Bu işlem yeni entegrasyonun yüklenmesini sağlar.
3. **Ayarlar → Cihazlar ve Hizmetler → Entegrasyon ekle → MG4 Cockpit Kurulum** yolunu açın.
4. Algılanan MG4 aracını seçip kurulumu tamamlayın. **MG4 Cockpit (HACS)** panosu sol menüde otomatik oluşturulur.
5. Kurulum tamamlandı bildiriminin ardından **Home Assistant'ı bir kez daha yeniden başlatın.** Bu ikinci yeniden başlatma, kurulum sırasında oluşturulan YAML paketlerindeki Türkçe durum ve analiz sensörlerini etkinleştirir. Öncesinde bazı kartlarda `Unavailable` görünmesi normaldir.
6. Sol menüden **MG4 Cockpit (HACS)** panosunu açın.

Pano oluşturmak için YAML kodu yapıştırmanız gerekmez. Entegrasyon `configuration.yaml` dosyasına pano kaydı yazmaz.

## Güncelleme

Her güncellemenin özeti `CHANGELOG.md` dosyasında bulunur. Güncelleme tamamlandığında Home Assistant bildiriminde de sürüm notları gösterilir.


1. HACS / Marketplace üzerinden MG4 Cockpit'in yeni sürümünü yükleyin.
2. **Home Assistant'ı yeniden başlatın.** Böylece yeni entegrasyon kodu yüklenir.
3. **Ayarlar → Cihazlar ve Hizmetler → MG4 Cockpit Kurulum → Yapılandır** bölümünü açın.
4. **Dashboardu güncelle** seçeneğini seçin ve onay ekranında işlemi onaylayın.
5. Güncelleme tamamlanınca panoyu kontrol edin. **YAML paketleri de değiştiyse sensörlerin yeni tanımları için bir kez daha yeniden başlatmanız gerekebilir.** Yalnızca dashboard içeriği değiştiyse normalde ikinci yeniden başlatma gerekmez.

Güncelleme öncesinde mevcut pano ve MG4 YAML dosyaları `/config/mg4_cockpit_backups/` klasörüne yedeklenir. Kullanıcı düzenlemeleri yeni sürümle otomatik birleştirilmez; onaylanan güncelleme mevcut düzenin yerini alabilir. Önceki duruma dönmek için aynı **Yapılandır** ekranındaki **Son yedeğe dön** seçeneğini kullanın. Geri dönüş YAML sensörlerini de değiştirirse yeniden başlatma gerekebilir.

## EPİAŞ (isteğe bağlı)

EPİAŞ, MG4 Cockpit'in çalışması için gerekli değildir ve kurulum paketine otomatik eklenmez.

EPİAŞ PTF sensörü `sensor.epias_guncel_ptf_kwh_2` mevcut ve kullanılabilir olduğunda şarj ekranında **Güncel PTF**, buna bağlı **tahmini fiyat** ve ilgili tarife açıklaması gösterilir. Sensör yoksa, devre dışıysa veya `unknown` / `unavailable` durumundaysa bu alanlar gizlenir. Diğer şarj bilgileri ve kontrolleri çalışmaya devam eder.

## Güvenlik ve notlar

- VIN, oluşturulan yerel YAML dosyalarında kullanılabilir. Bu dosyaları veya VIN içeren ekran görüntülerini herkese açık depolara yüklemeyin.
- Entegrasyon kaldırıldığında kullanıcıya ait YAML dosyaları otomatik silinmez.
- Kurulum sırasında var olan MG4 dosyalarıyla çakışma tespit edilirse `file_exists` hatası alınabilir; önce eski dosyaları yedekleyip kontrol edin.
- Home Assistant Core 2026.11.2 üzerinde temiz kurulum, dashboard güncelleme ve yedekten geri dönüş test edilmiştir. Farklı sürümlerde uyumluluk değişebilir.

## Kaynak ve teşekkür

Araç iletişiminde [SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway) kullanılır. Geliştirici **[nanomad](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway/commits?author=nanomad)** ve katkıda bulunanlara teşekkürler. MG4 Cockpit'e özgü dashboard, YAML ve kurulum bileşeni proje sahibinin yönlendirmeleriyle ChatGPT yardımıyla hazırlanmıştır.
