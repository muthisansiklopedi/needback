# Mazgal — İçerik Paketi #1

Bu klasör, Mazgal YouTube kanalı için hazırlanmış 5 içeriği barındırır: **2 belgesel + 3 reels.**

## Belgeseller (uzun video)
| # | Başlık | Süre | Dosya |
|---|---|---|---|
| 1 | Dünyanın En Kötü Hackerleri | 7–9 dk | [belgeseller/01-dunyanin-en-kotu-hackerleri.md](belgeseller/01-dunyanin-en-kotu-hackerleri.md) |
| 2 | Katil Dronlar, Avcı Dronlar ve Türkiye'nin Yükselişi | 10–12 dk | [belgeseller/02-katil-drone-avci-drone-turkiye.md](belgeseller/02-katil-drone-avci-drone-turkiye.md) |

## Reels / Shorts
| # | Konu | Süre | Bağlandığı belgesel | Dosya |
|---|---|---|---|---|
| 1 | Bir fotoğraf yüzünden yakalanan hacker | ~45 sn | Belgesel 1 | [reels/reels-01-selfie-ile-yakalanan-hacker.md](reels/reels-01-selfie-ile-yakalanan-hacker.md) |
| 2 | Gemiden kalkan SİHA: Bayraktar TB3 | ~50 sn | Belgesel 2 | [reels/reels-02-tb3-gemiden-kalkan-siha.md](reels/reels-02-tb3-gemiden-kalkan-siha.md) |
| 3 | Fotoğrafların konumunu ele veriyor (nasıl kapatılır) | ~55 sn | Belgesel 1 | [reels/reels-03-fotograflarin-konumunu-ele-veriyor.md](reels/reels-03-fotograflarin-konumunu-ele-veriyor.md) |

## Önerilen Yayın Takvimi
| Gün | İçerik | Neden |
|---|---|---|
| 1. gün | Reels 1 (hacker teaser) | Merak uyandırır |
| 2. gün | **Belgesel 1** – Hackerler | Teaser'ın trafiğini yakalar |
| 4. gün | Reels 3 (EXIF ipucu) | Kaydedilme/paylaşım yüksek, Belgesel 1'e geri trafik |
| 6. gün | Reels 2 (TB3) | Belgesel 2 için ısınma, yüksek paylaşım |
| 7. gün | **Belgesel 2** – Dronlar & Türkiye | Haftanın ana videosu |

## Her Dosyada Neler Var?
- Başlık önerileri ve thumbnail fikri
- Zaman kodlu senaryo (anlatım + görsel + ekran yazısı)
- Müzik ve prodüksiyon notları
- YouTube açıklaması (bölüm zaman damgalarıyla), etiketler
- Kaynak listesi

> ⚠️ Tarih, rakam ve isimler yayından önce dosyalardaki kaynaklardan son kez kontrol edilmelidir — özellikle savunma sanayii verileri hızla güncelleniyor.

## Prodüksiyon Dosyaları (`uretim/`)
Her içerik için ayrı klasör:

| Klasör | İçerik |
|---|---|
| `uretim/01-hackerler/` | Belgesel 1 |
| `uretim/02-dronlar/` | Belgesel 2 |
| `uretim/03-reels-hacker/` | Reels 1 |
| `uretim/04-reels-tb3/` | Reels 2 |
| `uretim/05-reels-exif/` | Reels 3 |

Her klasörde:
- **`seslendirme.md`**: Yalnızca anlatıcının okuyacağı metin, bölüm zaman kodlarıyla. Kendi sesinizle ya da yapay zekâ seslendirme aracına yapıştırarak kullanın.
- **`sahne-promptlari.md`**: Her sahne için görsel üretim promptu (İngilizce), Mazgal renk temasıyla (koyu arduvaz yeşili + yanık turuncu).
- **`altyazi.srt`**: Türkçe altyazı. Zamanlar dakikada ~138 kelimelik okuma hızına göre **tahminidir**; seslendirmeyi kaydettikten sonra kurgu programında (CapCut / DaVinci / Premiere) ses ile hizalayın.
