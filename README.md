# MG4 Cockpit · HACS kurulum test sürümü

> **Deneysel sürüm:** Otomatik dashboard kaydı kodlandı ve yerel testlerden geçti; gerçek Home Assistant üzerinde henüz doğrulanmadı. Mevcut yapılandırmanızı yedekleyin.

![Gerçek MG4 Cockpit ekranı](docs/images/kokpit.png)

MG4 Cockpit, SAIC iSmart MQTT Gateway ile Home Assistant'a aktarılan araç bilgilerini tek panelde birleştirir. Kokpit, şarj yönetimi, klima/konfor, araç durumu, konum, sürüş analizi ve sistem izleme ekranlarını içerir. Görseller gerçek Home Assistant ekran görüntüleridir; konum görseli gizlilik için bulanıklaştırılmıştır.

| Kokpit | Şarj | Analiz |
|---|---|---|
| ![Kokpit](docs/images/kokpit.png) | ![Şarj](docs/images/sarj.png) | ![Analiz](docs/images/menzil-analizi.png) |

## Ön koşullar

- Home Assistant ve HACS kurulu olmalı.
- [SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway) kurulmuş, MQTT Discovery ile araç varlıkları Home Assistant'ta görünür olmalı.
- Dashboard için şu HACS frontend kartları gerekli: `button-card`, `mushroom`, `apexcharts-card`, `config-template-card`, `ha-openfreemap-card`.
- Home Assistant yapılandırmasının tam yedeğini alın. **Aynı MG4 paketlerini zaten kullanan sisteme paralel kurmayın.**

## HACS ile kurulum (v0.5 beta)

1. HACS / Marketplace üzerinden depoyu **Integration** olarak ekle ve MG4 Cockpit'i indir.
2. Home Assistant'ı yeniden başlat. Ayarlar → Cihazlar ve Hizmetler → Entegrasyon ekle → MG4 Cockpit Kurulum.
3. Aracını seç. Entegrasyon, MG4 dosyalarını hazırlar ve **MG4 Cockpit (HACS)** panosunu sol menüye eklemeyi dener.
4. Gerekli özel kartların (`button-card`, `mushroom`, `apexcharts-card`, `config-template-card`, `ha-openfreemap-card`) yüklü olduğunu kontrol et.

`configuration.yaml` dosyasına pano kaydı eklenmez. MG4 paketlerinin çalışması için Home Assistant'ta `homeassistant.packages` ayarı **önceden etkin** olmalıdır; bu sürüm o ayarı da değiştirmez. İlk kurulumda üretilen YAML paketleri için yeniden başlatma gerekebilir. EPİAŞ isteğe bağlıdır.

### v0.4 sürümünden yükseltme

v0.4'ün `configuration.yaml` dosyasına eklediği `lovelace: dashboards: mg4-cockpit-hacs:` kaydı **otomatik silinmez**. Kayıt duruyorsa v0.5 aynı adresi kullanarak ikinci pano oluşturmaz. Geçişten önce Home Assistant yedeği alıp yalnızca v0.4'ün eklediği MG4 pano tanımını elle kaldırmak ve Home Assistant'ı yeniden başlatmak gerekir. Diğer `lovelace` ayarlarına dokunma. Eski pano ve paket dosyalarını silme.

**Beta notu:** Depolama tabanlı otomatik pano kaydı, Home Assistant Core 2026.11.2 üzerinde henüz gerçek sistem testi görmedi. Home Assistant'ın dahili API'lerine dayanır; sürümler arasında değişebilir. Pano oluşmazsa günlükleri kontrol et.

## Güvenlik

- VIN yalnızca yerel üretilen YAML dosyalarında kullanılır. Bu dosyaları herkese açık GitHub deposuna yüklemeyin.
- Kurulum sırasında mevcut YAML dosyalarının üzerine yazılmaz. Kısmi yazma hatasında yeni oluşturulan dosyalar geri alınır.
- Entegrasyon kaldırılınca oluşturulmuş kullanıcı dosyaları otomatik silinmez.
- Araç algılama mevcut Home Assistant varlık kayıtlarını okur; araca yeni veri sorgusu göndermez.
- EPİAŞ isteğe bağlıdır; bu kurulum paketine otomatik dahil edilmez.

## Kaynak ve teşekkür

Araç iletişiminde [SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway) kullanılır. Geliştirici **[nanomad](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway/commits?author=nanomad)** ve katkıda bulunanlara teşekkürler. MG4 Cockpit'e özgü dashboard, YAML ve kurulum bileşeni proje sahibinin yönlendirmeleriyle ChatGPT yardımıyla hazırlanmıştır.

### İsteğe bağlı EPİAŞ

EPİAŞ sensörü (`sensor.epias_guncel_ptf_kwh_2`) kullanılmıyorsa şarj ekranındaki Güncel PTF, Tahmini toplam fiyat ve ilgili tarife açıklaması gizlenir. Sensör kullanılabilir duruma geldiğinde kartlar görünür. Diğer şarj işlevleri EPİAŞ olmadan çalışır.


### İlk kurulumdan sonra

HACS üzerinden indirdikten sonra Home Assistant'ı yeniden başlatın ve MG4 Cockpit entegrasyonunu ekleyerek aracınızı seçin. Pano hemen oluşturulur; ancak beş YAML paketindeki sensörlerin etkinleşmesi için **araç seçiminin ardından bir kez daha yeniden başlatmanız gerekir**. Bu hatırlatma Home Assistant bildirimi olarak da gösterilir. `configuration.yaml` dosyasına pano kaydı eklenmez.

### İsteğe bağlı EPİAŞ

EPİAŞ sensörü `sensor.epias_guncel_ptf_kwh_2` mevcut ve kullanılabilir olduğunda Güncel PTF ve buna bağlı tahmini fiyat kartları gösterilir. Sensör yoksa veya `unknown` / `unavailable` durumundaysa ilgili kartlar gizlenir. Bu koşul yalnızca yeni oluşturulan dashboard için geçerlidir; daha önce oluşturulmuş UI panoları otomatik olarak değiştirilmez.


## v0.6 — Onaylı güncelleme (beta)

HACS güncellemesi mevcut UI panosunu veya kullanıcı YAML dosyalarını kendiliğinden değiştirmez.
Home Assistant yeniden başladıktan sonra güncelleme varsa bildirim görünür.
**Ayarlar → Cihazlar ve Hizmetler → MG4 Cockpit Kurulum → Yapılandır** menüsünden
**Güncelle** seçilir ve ikinci ekranda açık onay verilir. Önce mevcut UI pano
yapılandırması ve altı yerel YAML dosyası `/config/mg4_cockpit_backups/` altında
yedeklenir. Aynı menüden **Son yedeğe dön** kullanılabilir.

**Dikkat:** Güncelleme, kullanıcı tarafından düzenlenmiş pano ve MG4 paketlerinin
yerine yeni sürümü koyar; değişiklikler yedekte saklanır, otomatik birleştirilmez.
Eski sürümden gelen kurulumlarda önceki değişikliklerin kaynağı doğrulanamayabilir.
EPİAŞ dosyalarına ve `configuration.yaml` dosyasına dokunulmaz.
Yeni YAML sensörlerinin etkinleşmesi için yeniden başlatma gerekebilir.

Bu sürüm deneysel olup Home Assistant Core 2026.11.2 üzerinde canlı test gerektirir.
