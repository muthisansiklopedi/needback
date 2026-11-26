# Mazgal Siber — Örnek Hastane Güvenlik Karnesi ve Dış İletişim Paketi

> ⚠️ **Bu bir ŞABLON / ÖRNEKTİR.** Buradaki hastane ("Özel Örnek Hastanesi", `ornekhastane.com.tr`) ve
> bulgular temsilîdir. Gerçek kampanyada her alan, mazgalsiber.com/araclar/karne aracının o hedefe
> çalıştırılmasıyla elde edilen **gerçek** verilerle doldurulmalıdır. Doğrulanmamış hiçbir açık iddiası
> e-postaya yazılmaz. Tüm kontroller pasiftir (hedefin herkese açık olarak sunduğu sinyaller);
> aktif sızma/zafiyet testi yalnızca yazılı izinle yapılır.

---

## 1) GÜVENLİK KARNESİ

**Kurum:** Özel Örnek Hastanesi
**Alan adı:** ornekhastane.com.tr
**Tarama tarihi:** (otomatik)
**Yöntem:** Pasif / herkese açık sinyaller

### Genel Not: **C  (56 / 100)  — Ortaltı risk**

| # | Kategori | Not | Durum |
|---|----------|-----|-------|
| 1 | SSL / TLS yapılandırması | B | ⚠️ Eski TLS 1.0/1.1 hâlâ açık |
| 2 | HTTP güvenlik başlıkları | D | ❌ HSTS, CSP, X-Frame-Options yok |
| 3 | E-posta güvenliği (SPF/DKIM/DMARC) | F | ❌ DMARC yok, SPF `~all` zayıf |
| 4 | DNS güvenliği (DNSSEC) | C | ⚠️ DNSSEC imzasız |
| 5 | Açıkta görünen servis / port | C | ⚠️ Yönetim paneli (RDP/WebAdmin) dışarı açık |
| 6 | Yazılım / CMS sürümü | D | ❌ Eski WordPress + güncellenmemiş eklenti |
| 7 | Alt alan adları (subdomain) | C | ⚠️ Terk edilmiş `test.`, `eski.` kayıtları |
| 8 | Veri sızıntısı / kurumsal e-posta | D | ❌ Personel e-postaları eski ihlallerde geçiyor |

> Not aralığı: A (çok iyi) → F (kritik). Hastaneler için **F ve D** satırları öncelikli ele alınmalıdır.

---

## 2) ZAFİYET AÇIKLAMA METNİ — Ne var, ne tahribata yol açar?

Aşağıdaki her madde, yukarıdaki karnedeki bir bulgunun **sade bir dille açıklaması** ve
**hastane bağlamında olası sonucudur.** Abartı değil, gerçekçi senaryolardır.

**1. E-posta güvenliği zayıf (SPF/DKIM/DMARC eksik) — Not F**
DMARC kaydı olmadığı için herhangi biri, hastanenizin alan adından ("…@ornekhastane.com.tr")
**sahte e-posta** gönderebilir. Olası sonuç: Dolandırıcılar, muhasebeye "hesap değişti, ödemeyi
şu IBAN'a yapın" diyen sahte bir yönetici e-postası (CEO fraud) atabilir; hastalara sahte randevu/ödeme
e-postaları gidip kurumun itibarı zedelenebilir. Bu, **en ucuz ve en hızlı sömürülen** açıktır.

**2. HTTP güvenlik başlıkları yok (HSTS/CSP/X-Frame-Options) — Not D**
Site, tarayıcıya "beni yalnızca güvenli bağlantıyla aç" (HSTS) ve "içeriğimi başka siteye gömme"
(X-Frame-Options) talimatını vermiyor. Olası sonuç: Açık Wi-Fi'de hasta ile site arasına girilerek
(ara­dakiadam) **randevu/giriş bilgileri** okunabilir; sahte bir sayfa gerçek site gibi çerçevelenip
hasta bilgileri toplanabilir (clickjacking).

**3. Eski TLS sürümleri açık (TLS 1.0/1.1) — Not B**
Artık güvenli sayılmayan şifreleme sürümleri kapatılmamış. Olası sonuç: Modern olmayan şifrelemeyle
kurulan bağlantılarda veri trafiği çözülebilir. Tek başına düşük risk ama **KVKK/ISO 27001
denetimlerinde** doğrudan bulgu olarak çıkar.

**4. Yönetim paneli dışarı açık (RDP / web yönetim) — Not C**
Sunucu yönetim arayüzü internete açık görünüyor. Olası sonuç: Otomatik botlar bu panellere sürekli
**parola deneme (brute-force)** yapar; zayıf tek bir parola, tüm sunucuya — dolayısıyla hasta
kayıtlarına — kapıyı açar. Hastanelere yönelik **fidye yazılımı** saldırılarının en sık giriş yolu budur.

**5. Güncellenmemiş web yazılımı / eklentiler — Not D**
Sitedeki içerik yönetim sistemi ve eklentileri eski sürümde. Olası sonuç: Bu sürümlerin **herkesçe
bilinen** açıkları vardır; saldırgan hazır araçla siteyi ele geçirip hasta verisini sızdırabilir ya da
siteyi fidye/defacement için kilitleyebilir.

**6. Terk edilmiş alt alan adları (test., eski.) — Not C**
Kullanılmayan ama hâlâ açık duran alt siteler var. Olası sonuç: Bunlar genelde **güncellenmez ve
unutulur**; saldırgan için en zayıf halka olur, oradan asıl sisteme sıçranır (subdomain takeover).

**7. DNSSEC yok — Not C**
Alan adı çözümlemesi imzalı değil. Olası sonuç: Belirli saldırılarda kullanıcılar sahte bir
sunucuya yönlendirilebilir. Orta öncelikli ama tamamlayıcı bir eksiklik.

**8. Personel e-postaları eski veri ihlallerinde — Not D**
Kurumsal e-postalar, geçmiş sızıntı veritabanlarında görünüyor. Olası sonuç: Çalışanlar aynı parolayı
tekrar kullandıysa, bu parolalarla **doğrudan giriş denenir.** Hesap ele geçirmenin en yaygın yolu.

### Hastaneye özel genel risk çerçevesi
- Hasta sağlık verisi, KVKK'da **özel nitelikli kişisel veri**dir; sızması en yüksek idari para
  cezası ve itibar kaybıyla sonuçlanır.
- Hastaneler dünyada **fidye yazılımının bir numaralı hedefidir**; randevu/HBYS sistemlerinin durması
  doğrudan hasta hizmetini aksatır.
- Yukarıdaki açıkların çoğu **tek tek küçük** görünür; saldırgan bunları **zincirleyerek** içeri girer.

---

## 3) MAZGAL SİBER — DIŞ İLETİŞİM (TANITIM) E-POSTASI

> Kullanım notu: `[ ]` içindeki alanlar her hedef için doldurulur. Her bulgu, e-postaya konmadan önce
> karne çıktısında **doğrulanmış** olmalıdır. Ton: korkutmak değil, "fark ettik, yardımcı olalım".

**Konu:** [Özel Örnek Hastanesi] için dışarıdan görünen güvenlik gözlemleri — Mazgal Siber

Sayın [Yetkili Adı / Bilgi İşlem Müdürlüğü],

Ben [Ad Soyad], Mazgal Siber Güvenlik ekibinden. Çalışmalarımızın bir parçası olarak, kurumların
**yalnızca internete açık, herkesin görebileceği** güvenlik sinyallerini değerlendiren ücretsiz bir
"güvenlik karnesi" aracı geliştirdik. Bu değerlendirme tamamen pasiftir; sistemlerinize herhangi bir
erişim ya da test **yapılmamıştır.**

[ornekhastane.com.tr] için dışarıdan baktığımızda öne çıkan, **düşük maliyetle kapatılabilecek**
birkaç nokta gördük:

- **E-posta sahteciliğine karşı koruma (DMARC) tanımlı değil.** Bu haliyle üçüncü kişiler kurumunuzun
  adına sahte e-posta gönderebilir; hasta ve çalışanlar hedef alınabilir.
- **Web güvenlik başlıkları eksik.** Tarayıcı tarafı bazı koruma katmanları devre dışı.
- **İnternete açık bir yönetim arayüzü** görünüyor; bu, otomatik parola denemelerinin ana hedefidir.

Hastanelerde hasta verisinin KVKK'da özel nitelikli veri sayıldığını ve sektörün fidye yazılımında
öncelikli hedef olduğunu biliyoruz. Bu yüzden amacımız tedirgin etmek değil; bu gözlemleri sizinle
paylaşıp, isterseniz **önceliklendirilmiş bir yol haritası** sunmak.

Dilerseniz [ornekhastane.com.tr] için hazırladığımız **ücretsiz karne raporunu** ileteyim ve 20
dakikalık kısa bir görüşmede şunları konuşalım:
1. Yukarıdaki maddelerin kapatılması (çoğu birkaç gün içinde, ek donanım gerektirmeden),
2. İsterseniz **yazılı izninizle** yapılacak kapsamlı bir sızma testi ve KVKK/ISO 27001 uyum desteği,
3. Sürekli izleme (SOC) ve fidye yazılımına karşı dayanıklılık.

Uygun olduğunuz bir zaman dilimi paylaşırsanız sevinirim.

Saygılarımla,
[Ad Soyad]
Mazgal Siber Güvenlik
[telefon] · [e-posta] · mazgalsiber.com

> **Yasal/etik not:** E-postada yalnızca pasif, herkese açık gözlemlerden bahsedilir. "Sistemlerinize
> girdik", "sizi hacklersek" gibi ifadeler **kullanılmaz** — hem yanlış hem de hukuken risklidir.
> Kapsamlı test her zaman kurumun **yazılı onayıyla** yapılır.

---

## 4) GERÇEK KAMPANYADA İŞ AKIŞI (başlayınca)

1. Hedef hastane listesi hazırlanır (isim + alan adı).
2. Her alan adı için `mazgalsiber.com/araclar/karne` çalıştırılır → gerçek karne verisi alınır.
3. Karne verisinden bu dosyadaki 3 bölüm **gerçek bulgularla** otomatik doldurulur.
4. Doğrulanamayan hiçbir bulgu e-postaya girmez.
5. E-postalar gönderim için hazırlanır (gönderimi siz onaylarsınız).
