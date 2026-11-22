# Mazgal üretim araçları

Senaryolardan seslendirme metni, sahne promptu, altyazı (.srt) ve yayın sayfası üreten betikler.
`*2.py` / `template2.html` dosyaları Paket 2 içindir. Python 3 ve `pip install markdown` gerekir.

1. `python3 extract2.py narr2.json` — senaryolardan anlatım metnini çıkarır
2. `python3 gen2.py` — zaman kodlarını hesaplar, `uretim/` dosyalarını yazar
3. `python3 build2.py <paket klasörü> cikti.html template2.html` — tek sayfalık HTML üretir

Not: `extract*.py` / `gen*.py` içindeki dosya yolları bu oturumdaki konuma göre yazılmıştır; başka yerde çalıştırırken yolları güncelleyin.
