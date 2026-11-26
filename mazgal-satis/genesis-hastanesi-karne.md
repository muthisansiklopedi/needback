# Genesis Hospital (Diyarbakır) — Güvenlik Karnesi ve Dış İletişim Paketi

> **Veri kaynağı:** mazgalsiber.com/araclar/karne — `genesishospital.com.tr` için gerçek tarama çıktısı.
> **Yöntem:** Yalnızca pasif / herkese açık sinyaller. Hastanenin sistemlerine hiçbir erişim veya
> aktif test yapılmamıştır. Bu karne dışarıdan görülen yapılandırmayı ölçer; sitenin yazılımındaki
> açıkları test etmez.
> **Tarama adresi:** https://genesishospital.com.tr/

---

## 1) GÜVENLİK KARNESİ

**Kurum:** Özel Genesis Hospital — Kayapınar / Diyarbakır
**Alan adı:** genesishospital.com.tr

### Genel Not: **F  (26 / 100)  — Yüksek risk**
> Özet (araç): "Temel güvenlik ayarlarının çoğu eksik; site ve ziyaretçileri risk altında."

| Kategori | Puan | Durum |
|----------|------|-------|
| Bağlantı | 15/25 | ⚠️ HTTPS var, ama http→https yönlendirmesi yok |
| Tarayıcı korumaları | **0/45** | ❌ HSTS, CSP, clickjacking, nosniff, Referrer/Permissions — hiçbiri yok |
| Bilgi sızıntısı | 5/10 | ⚠️ Sunucu sürümü dışarı sızıyor (PHP 8.0) |
| E-posta ve DNS | 6/20 | ❌ DMARC sadece izleme modunda, SPF yumuşak |

### Bulgu dökümü (araç çıktısı birebir)

**Bağlantı — 15/25**
- ✅ HTTPS (şifreli bağlantı) — 15/15. Site HTTPS ile açılıyor.
- ❌ HTTP → HTTPS yönlendirme — 0/10. Şifresiz (http) adres HTTPS'ye yönlendirilmiyor; ziyaretçiler şifresiz sürümde kalabilir.

**Tarayıcı korumaları — 0/45**
- ❌ HSTS (zorunlu HTTPS) — 0/10. Yok: ilk ziyarette bağlantı şifresiz sürüme düşürülebilir.
- ❌ İçerik Güvenlik Politikası (CSP) — 0/15. Yok: siteye zararlı kod (XSS) enjekte edilirse tarayıcı engellemez.
- ❌ Tıklama tuzağı (clickjacking) koruması — 0/8. Yok: site sahte bir sayfanın içine gömülüp ziyaretçi kandırılabilir.
- ⚠️ X-Content-Type-Options (nosniff) — 0/5. Yok: tarayıcı dosya türünü yanlış yorumlayıp kod çalıştırabilir.
- ⚠️ Referrer-Policy — 0/4. Yok/gevşek: sayfa adresleri (parametreleriyle) başka sitelere sızabilir.
- ⚠️ Permissions-Policy — 0/3. Yok: kamera/mikrofon/konum izinleri sayfa bazında kısıtlanmamış.

**Bilgi sızıntısı — 5/10**
- ⚠️ Sunucu sürüm bilgisi — 0/5. Yanıt başlıklarında görünüyor: **cloudflare · PHP/8.0.30**. (Not: PHP 8.0, Kasım 2023'ten beri resmî güvenlik güncellemesi almıyor.)
- ✅ Çerez güvenliği — 5/5. Ana sayfa çerez bırakmıyor.

**E-posta ve DNS — 6/20**
- ⚠️ SPF — 4/5. Yumuşak modda (`~all`); katı mod (`-all`) daha güvenli.
  `v=spf1 include:_spfcls.natrohost.com include:_netblockshalon.natrohost.com ~all`
- ❌ DMARC — 2/8. Yalnızca izleme modunda (`p=none`); sahte e-postalar engellenmiyor. `v=DMARC1; p=none`
- ⚠️ DNSSEC — 0/3. Kapalı (düşük öncelik).
- ⚠️ CAA (sertifika yetkisi) — 0/2. Kayıt yok: herhangi bir sertifika otoritesi sertifika verebilir.
- ⚠️ security.txt — 0/2. Yok: bir açık bulan kişi size nasıl ulaşacağını bilemeyebilir.

---

## 2) ZAFİYET AÇIKLAMA METNİ — Ne var, ne tahribata yol açar?

Aşağıdakiler karnedeki gerçek bulgulardır; her biri sade dille ve hastane bağlamında açıklanmıştır.
Abartı yok; bunların hepsi dışarıdan, sistemlere dokunmadan görülebilen eksikliklerdir.

**1. E-posta sahteciliği engellenmiyor (DMARC `p=none`) — En kritik**
DMARC "sadece izle" modunda olduğu için, bir saldırgan **"…@genesishospital.com.tr" adresinden sahte
e-posta** gönderebilir ve bu e-posta alıcıya gerçek gibi ulaşır. Hastane bağlamında olası sonuç:
muhasebeye "tedarikçi IBAN'ı değişti" diyen sahte yönetici e-postası (CEO/fatura dolandırıcılığı),
hastalara sahte "randevu/ödeme" e-postaları. Bu, en ucuz ve en hızlı sömürülen açıktır; çözümü de
kısadır (DMARC'ı önce `quarantine`, sonra `reject`'e almak).

**2. Tarayıcı koruma başlıkları tamamen eksik (0/45)**
Site, ziyaretçinin tarayıcısına hiçbir koruma talimatı vermiyor:
- **CSP yok:** Siteye bir XSS açığından kod enjekte edilirse tarayıcı bunu durdurmaz. Hasta giriş/randevu
  sayfalarında bu, form bilgilerinin çalınmasına kadar gider.
- **HSTS yok + http→https yönlendirmesi yok:** Hasta, hastane Wi-Fi'ı veya açık bir ağda siteye
  şifresiz bağlanabilir; arada biri (aradaki­adam) trafiği okuyabilir, sahte sayfaya yönlendirebilir.
- **Clickjacking koruması yok:** Site görünmez biçimde sahte bir sayfaya gömülüp ziyaretçinin
  farkında olmadan işlem yapması sağlanabilir.

**3. Sunucu eski PHP sürümünü açığa veriyor (PHP 8.0.30)**
Yanıt başlıkları sunucunun PHP 8.0 kullandığını söylüyor. PHP 8.0 **Kasım 2023'ten beri güvenlik
güncellemesi almıyor.** Olası sonuç: bu sürümün bilinen açıkları saldırgan için hazır bir hedef listesi
oluşturur; sürümü gizlemek ve güncel/destekli bir sürüme geçmek gerekir. (Bu karne açığı test etmez,
yalnızca sürümün dışarı sızdığını ve desteksiz olduğunu gösterir.)

**4. SPF yumuşak modda (`~all`)**
E-posta sahteciliğine karşı ikinci katman da gevşek. DMARC ile birlikte sıkılaştırılmalı.

**5. İkincil eksiklikler (DNSSEC, CAA, security.txt yok)**
Tek başlarına düşük riskli ama tamamlayıcı. Özellikle **CAA yok** → yetkisiz bir tarafın bu alan adına
sertifika çıkarmasını engelleyen kayıt yok. **security.txt yok** → iyi niyetli biri bir açık bulsa bile
size nasıl ulaşacağını bilemez.

### Hastaneye özel genel çerçeve
- Hasta sağlık verisi KVKK'da **özel nitelikli kişisel veri**dir; ihlali en yüksek idari ceza ve
  itibar kaybıyla sonuçlanır.
- Hastaneler fidye yazılımının **öncelikli hedefidir**; randevu/HBYS kesintisi doğrudan hasta
  hizmetini durdurur.
- Yukarıdaki eksiklikler tek tek "küçük" görünür; saldırgan bunları **zincirleyerek** ilerler.
- İyi haber: bu bulguların **neredeyse tamamı yazılım değişikliği gerektirmeden**, sunucu/DNS
  ayarlarıyla birkaç gün içinde kapatılabilir.

---

## 3) MAZGAL SİBER — DIŞ İLETİŞİM (TANITIM) E-POSTASI

> `[ ]` alanlarını gönderimden önce doldurun. Tüm maddeler karne çıktısıyla doğrulanmıştır.
> Ton: korkutmak değil, "fark ettik, yardımcı olalım".

**Kime:** [Genesis Hospital — Bilgi İşlem / Kurumsal İletişim]
**Konu:** genesishospital.com.tr için dışarıdan görünen güvenlik gözlemleri — Mazgal Siber

Sayın Yetkili,

Ben [Ad Soyad], Mazgal Siber Güvenlik ekibinden. Kurumların **yalnızca internete açık, herkesin
görebileceği** güvenlik sinyallerini değerlendiren bir "güvenlik karnesi" çalışması yürütüyoruz.
Bu değerlendirme tamamen pasiftir; sistemlerinize **hiçbir erişim veya test yapılmamıştır.**

genesishospital.com.tr için dışarıdan baktığımızda, **düşük maliyetle ve çoğu yazılım değişikliği
gerektirmeden** kapatılabilecek birkaç önemli nokta öne çıktı:

- **E-posta sahteciliğine karşı koruma etkin değil (DMARC yalnızca izleme modunda).** Bu haliyle
  üçüncü kişiler kurumunuz adına sahte e-posta gönderebilir; muhasebe ve hastalar hedef alınabilir.
- **Web tarayıcı koruma başlıkları tanımlı değil** (HSTS, CSP, clickjacking koruması). Ziyaretçi
  güvenliğinde temel katmanlar devrede değil.
- **Sunucu, artık güvenlik güncellemesi almayan bir PHP sürümünü (8.0) dışarı veriyor.**

Hastanelerde hasta verisinin KVKK'da özel nitelikli sayıldığını ve sektörün fidye yazılımında
öncelikli hedef olduğunu biliyoruz. Amacımız tedirgin etmek değil; bu gözlemleri sizinle paylaşıp,
isterseniz **önceliklendirilmiş ve uygulanabilir bir yol haritası** sunmak.

Dilerseniz genesishospital.com.tr için hazırladığımız **ücretsiz karne raporunu** ileteyim ve 20
dakikalık kısa bir görüşmede şunları konuşalım:
1. Yukarıdaki maddelerin kapatılması (çoğu birkaç gün içinde, ek donanım gerektirmeden),
2. İsterseniz **yazılı izninizle** yapılacak kapsamlı bir sızma testi ve KVKK uyum desteği,
3. Sürekli izleme (SOC) ve fidye yazılımına karşı dayanıklılık.

Uygun olduğunuz bir zaman dilimini paylaşırsanız sevinirim.

Saygılarımla,
[Ad Soyad]
Mazgal Siber Güvenlik
[telefon] · [e-posta] · mazgalsiber.com

> **Etik/yasal not:** E-postada yalnızca pasif, herkese açık gözlemlerden bahsedilir. "Sistemlerinize
> girdik / sizi hackleriz" gibi ifadeler kullanılmaz. Kapsamlı test her zaman kurumun **yazılı
> onayıyla** yapılır.
