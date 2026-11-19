# MG4 Home Assistant Cockpit

MG4 elektrikli araç için Home Assistant üzerinde geliştirilmiş, Türkçe bir kontrol ve analiz panelidir. Batarya durumu, menzil, şarj yönetimi, konfor kontrolleri ve sürüş analizlerini tek arayüzde toplar.

> **Durum:** Geliştirme sürümü. Mevcut sistemden uyarlanmıştır; farklı Home Assistant kurulumlarında sensör adları ve özel kart bağımlılıkları değişebilir. Önce Private repoda test edilmesi önerilir.

## Araç ile iletişim

Bu proje MG iSMART hesabından araç verilerini alabilmek ve Home Assistant'a MQTT üzerinden aktarabilmek için **[SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway)** projesini kullanır.

Gateway; araç verilerini MQTT üzerinden yayımlar ve Home Assistant MQTT Discovery ile sensör ve kontrol varlıklarının oluşmasını sağlar. Bu depo gateway'in yerine geçmez; onun sağladığı veriler üzerinde dashboard, yardımcı sensör ve otomasyonlar oluşturur.

**Teşekkür:** SAIC Python MQTT Gateway projesinin geliştiricisi **nanomad** başta olmak üzere tüm katkıda bulunanlara teşekkür ederiz. Bu proje, onların sağladığı iletişim altyapısı sayesinde geliştirilmiştir.

## Kodların hazırlanması

Bu depodaki dashboard, YAML yardımcıları, analizler ve EPİAŞ entegrasyonunun proje özelindeki kodları, proje sahibinin gereksinimleri doğrultusunda **OpenAI ChatGPT (GPT-6) desteğiyle hazırlanmış ve düzenlenmiştir**. Testler ve işlevsel doğrulamalar proje sahibi tarafından kendi Home Assistant ortamında yürütülmüştür. SAIC Python MQTT Gateway ayrı bir açık kaynak projesidir; onun kodlarının yazarlığı bu depoya ait değildir.

## Özellikler

- MG4 batarya seviyesi, menzil ve araç durumu
- Şarj planlaması ve şarj oturumu takibi
- İklimlendirme ve batarya ön ısıtma kontrolleri
- Sürüş ve tüketim analizleri
- Türkçe durum göstergeleri
- **İsteğe bağlı:** EPİAŞ saatlik PTF takibi ve tahmini enerji maliyeti

## Kurulum

1. Home Assistant sisteminizin yedeğini alın.
2. [SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway) kurulumunu tamamlayın. MQTT sensörlerinin Home Assistant'ta oluştuğunu doğrulayın.
3. Dashboardun kullandığı özel kartların sisteminizde bulunduğundan emin olun. Sensör adları gateway sürümüne göre farklılık gösterebilir.
4. Bilgisayarınızda `python3 tools/configure_vin.py --vin KENDI_17_HANELI_VIN --output local` komutunu çalıştırın. Oluşan `local/` klasörünü **GitHub'a yüklemeyin**.
5. `local/packages/*.yaml` dosyalarını `/config/packages/` klasörüne kopyalamadan önce mevcut yardımcılar ve otomasyonlarla çakışmaları inceleyin. `homeassistant: packages: !include_dir_named packages` tanımını mevcut yapılandırmanızla birleştirin.
6. `local/dashboards/mg4_cockpit.yaml` dosyasını YAML modundaki bir dashboarda aktarın. Gerektiğinde sensör adlarını uyarlayın.
7. Home Assistant yapılandırmasını doğrulayın. Araç kontrol komutlarını dikkatli ve gözetim altında test edin.

## EPİAŞ modülü (isteğe bağlı)

EPİAŞ modülü Türkiye'deki kullanıcılar içindir ve ana dashboardun çalışması için zorunlu değildir. Betik, sensör, saatlik otomasyon ve ek fiyat kartları `epias/` klasöründe bulunur. Kurulum adımları: [EPİAŞ rehberi](epias/README.md).

## Klasörler

| Klasör | İçerik |
|---|---|
| `dashboards/` | MG4 kontrol paneli |
| `packages/` | Yardımcı sensörler, sürüş analizleri ve otomasyonlar |
| `epias/` | İsteğe bağlı elektrik fiyatı entegrasyonu |
| `tools/` | VIN'i yalnızca yerel kopyalara uygulama aracı |
| `examples/` | Örnek Home Assistant yapılandırmaları |
| `docs/` | Yayımlama öncesi kontrol listesi |

## Gizlilik ve güvenlik

Gerçek VIN, iSMART ve EPİAŞ giriş bilgileri, `secrets.yaml`, erişim anahtarları, konum geçmişi ve kişisel otomasyonlar GitHub'a yüklenmemelidir. Bu depodaki `YOUR_VIN` yer tutucusu gerçek VIN ile yalnızca yerel ortamda değiştirilmelidir.

## Lisans

Proje özelinde oluşturulan kodlar MIT lisansı ile sunulmuştur. Kullanılan üçüncü taraf yazılımlar ve özel Home Assistant kartları kendi lisanslarına tabidir. MG, SAIC veya EPİAŞ ile resmî bağlantısı yoktur.
