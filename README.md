# MG4 Cockpit · HACS kurulum test sürümü

> **Deneysel sürüm:** Home Assistant üzerinde uçtan uca test edilmedi. Bu sürümü ana GitHub deponuzun `main` dalına henüz yüklemeyin. Tam yedek almadan kurmayın.

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

## HACS ile kurulum (mevcut test sürümü)

1. Bu depoyu GitHub'a **ayrı bir test deposu** olarak yükleyin. HACS → Özel depolar → depo URL'si → **Integration** kategorisi → Ekle.
2. HACS'ten MG4 Cockpit'i indirin ve Home Assistant'ı yeniden başlatın.
3. Ayarlar → Cihazlar ve Hizmetler → Entegrasyon ekle → **MG4 Cockpit Kurulum**.
4. Gateway'in oluşturduğu VIN algılanırsa listeden aracı seçin; algılanmazsa VIN'i elle girin.
5. Entegrasyon, `/config/packages/mg4_cockpit_*.yaml` dosyalarını ve `/config/mg4_cockpit_dashboard.yaml` dosyasını oluşturur. **Var olan dosyaların üzerine yazmaz.**
6. `/config/configuration.yaml` içinde `homeassistant:` bölümünde `packages: !include_dir_named packages` yapılandırması yoksa mevcut ayarlarınızla birleştirerek ekleyin. Dosyanın başına ikinci bir `homeassistant:` anahtarı eklemeyin.
7. Ayarlar → Panolar → Pano ekle → YAML pano kullanıyorsanız yapılandırmanıza aşağıdaki örneği, **mevcut `lovelace:` ayarlarınızla birleştirerek** ekleyin:

```yaml
lovelace:
  dashboards:
    mg4-cockpit:
      mode: yaml
      title: MG4 Cockpit
      icon: mdi:car-electric
      show_in_sidebar: true
      filename: mg4_cockpit_dashboard.yaml
```

8. Gerekli özel kartları HACS'ten kurun. Home Assistant yapılandırmasını kontrol edin ve yeniden başlatın.

**Henüz otomatik olmayan adımlar:** `configuration.yaml` içindeki packages etkinleştirme, dashboard kaydı ve özel kart kurulumu. HACS bunları tek başına yapmaz. Bu sürümün tüm kurulumunu üç tıklamayla tamamladığını iddia etmiyoruz.

## Güvenlik

- VIN yalnızca yerel üretilen YAML dosyalarında kullanılır. Bu dosyaları herkese açık GitHub deposuna yüklemeyin.
- Kurulum sırasında mevcut YAML dosyalarının üzerine yazılmaz. Kısmi yazma hatasında yeni oluşturulan dosyalar geri alınır.
- Entegrasyon kaldırılınca oluşturulmuş kullanıcı dosyaları otomatik silinmez.
- Araç algılama mevcut Home Assistant varlık kayıtlarını okur; araca yeni veri sorgusu göndermez.
- EPİAŞ isteğe bağlıdır; bu kurulum paketine otomatik dahil edilmez.

## Kaynak ve teşekkür

Araç iletişiminde [SAIC Python MQTT Gateway](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway) kullanılır. Geliştirici **[nanomad](https://github.com/SAIC-iSmart-API/saic-python-mqtt-gateway/commits?author=nanomad)** ve katkıda bulunanlara teşekkürler. MG4 Cockpit'e özgü dashboard, YAML ve kurulum bileşeni proje sahibinin yönlendirmeleriyle ChatGPT yardımıyla hazırlanmıştır.
