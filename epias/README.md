# EPİAŞ PTF — İsteğe bağlı modül

Bu modül MG4 dashboardunun çalışması için **zorunlu değildir**. Türkiye için saatlik PTF fiyatını takip eder; hesaplanan toplam bedel kesin fatura değildir.

1. Komut satırı sensörünün çalıştığı ortamda `bash`, `curl` ve `jq` bulunmalıdır.
2. `epias_ptf.sh` dosyasını Home Assistant `/config/epias_ptf.sh` konumuna kopyalayın.
3. Gerçek `/config/secrets.yaml` dosyanıza `epias_username` ve `epias_password` ekleyin. Bu dosyayı repoya yüklemeyin.
4. `sensor.example.yaml` içeriğini mevcut `configuration.yaml` ile birleştirin. İkinci bir `command_line:` üst anahtarı oluşturmayın.
5. `automation.example.yaml` içeriğini mevcut otomasyonlara ekleyin. Gerçek sensör kimliğini Geliştirici Araçları'ndan kontrol edin; `_2` gibi ekler bulunabilir.
6. Önce betiği ve sensörü elle, ardından her saat `HH:02` otomatik güncellemeyi test edin.
7. Son olarak `dashboard_cards.optional.yaml` içindeki kartları Enerji bölümünün başına ekleyin. Kartlardaki sensör kimliğini kendi sisteminize göre düzeltin.

**Hesaplama varsayımları:** Fiyat kartlarında YEKDEM 0,48886 TL/kWh, tedarikçi payı %4,95, dağıtım 2,4249 TL/kWh, elektrik tüketim vergisi %5 ve KDV %10 örnek olarak kullanılmıştır. Güncel mevzuat ve sözleşmeyle doğrulanmalıdır. Saat aralığı sensör güncelleme zamanından türetilir; API dönem alanından ayrıca doğrulanmaz.

**Güvenlik:** Kimlik bilgilerini, erişim belirteçlerini veya ham kimlik doğrulama yanıtlarını kaynak koduna ya da loglara koymayın.
