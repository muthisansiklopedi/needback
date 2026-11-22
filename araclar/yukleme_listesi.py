"""Mazgal yükleme kontrol listesi sayfasını senaryo dosyalarından üretir.
Kullanım: python3 araclar/yukleme_listesi.py <repo kökü> <çıktı.html>"""
import re, sys, html, json
ROOT = sys.argv[1].rstrip('/') + '/icerikler'
OUT = sys.argv[2]

def read(p): return open(f'{ROOT}/{p}', encoding='utf-8').read()
def section(md, head):
    m = re.search(rf'^## {head}.*?\n(.*?)(?=^## |\Z)', md, re.S | re.M)
    return m[1].strip() if m else ''
def unquote(block):
    return '\n'.join(re.sub(r'^> ?', '', l) for l in block.split('\n') if l.startswith('>')).strip()
def titles(md): return [re.sub(r'^\d+\. ', '', l).strip() for l in section(md, 'Başlık Önerileri').split('\n') if re.match(r'^\d+\.', l)]
def thumb(md):
    t = re.sub(r'\n-{3,}\s*$', '', section(md, 'Thumbnail Fikri')).strip(); big = re.search(r'Büyük yazı: \*\*"?([^"*]+)"?\*\*', t)
    return (big[1] if big else ''), re.sub(r'\*\*', '', re.sub(r'\n?- Büyük yazı:.*', '', t)).replace('- ', '• ')
def pinned(md): return section(md, 'Pinned Yorum').strip('> \n')

VIDEOS = [
 # paket, gün, id, tür, dosya, önerilen başlık (index veya metin), bitiş ekranı, kart / ilgili video, oynatma listesi
 (1, 1, 'p1-r1', 'reels', 'reels/reels-01-selfie-ile-yakalanan-hacker.md', 'Polisi Hackledi, Bir Fotoğrafla Yakalandı 📸 #shorts', None, 'Dünyanın En Kötü Hackerleri', 'Mazgal Shorts'),
 (1, 2, 'p1-b1', 'belgesel', 'belgeseller/01-dunyanin-en-kotu-hackerleri.md', 0, 'Katil Dronlar belgeseli + Abone ol', 'Bölüm 3 (w0rmer) sonunda → "Fotoğrafların konumunu ele veriyor" Short', 'Siber Güvenlik'),
 (1, 4, 'p1-r3', 'reels', 'reels/reels-03-fotograflarin-konumunu-ele-veriyor.md', 'Fotoğrafların Konumunu Ele Veriyor! Nasıl Kapatılır? #shorts', None, 'Dünyanın En Kötü Hackerleri', 'Mazgal Shorts'),
 (1, 6, 'p1-r2', 'reels', 'reels/reels-02-tb3-gemiden-kalkan-siha.md', "Uçakları Gelmeyen Gemiye Türkiye Kendi SİHA'sını Yaptı 🇹🇷 #shorts", None, 'Katil Dronlar, Avcı Dronlar ve Türkiye', 'Mazgal Shorts'),
 (1, 7, 'p1-b2', 'belgesel', 'belgeseller/02-katil-drone-avci-drone-turkiye.md', 1, 'Dünyanın En Kötü Hackerleri + TB3 Short + Abone ol', 'Bölüm 4 başında → "Gemiden kalkan SİHA" Short', 'Savunma Teknolojileri'),
 (2, 1, 'p2-r1', 'reels', 'paket-02/reels/reels-01-usb-ile-nukleer-tesis.md', 'Bir USB Bellek Nükleer Tesisi Durdurdu 💀 #shorts', None, 'Dünyayı Durduran Siber Saldırılar', 'Mazgal Shorts'),
 (2, 2, 'p2-b1', 'belgesel', 'paket-02/belgeseller/01-dunyayi-durduran-siber-saldirilar.md', 0, 'Savaş Uçaklarının Geleceği ve KAAN + Şifre Short + Abone ol', 'Bölüm 6 (Colonial) sonunda → "Şifren sızdı mı?" Short; açılışta → Dünyanın En Kötü Hackerleri', 'Siber Güvenlik'),
 (2, 4, 'p2-r3', 'reels', 'paket-02/reels/reels-03-sifren-sizdi-mi.md', 'Şifren Sızdı mı? 30 Saniyede Kontrol Et 🔐 #shorts', None, 'Dünyayı Durduran Siber Saldırılar', 'Mazgal Shorts'),
 (2, 6, 'p2-r2', 'reels', 'paket-02/reels/reels-02-f35ten-kaana.md', "F-35'ten Çıkarıldı, KAAN'ı Yaptı 🇹🇷 #shorts", None, 'Savaş Uçaklarının Geleceği ve KAAN', 'Mazgal Shorts'),
 (2, 7, 'p2-b2', 'belgesel', 'paket-02/belgeseller/02-savas-ucaklarinin-gelecegi-kaan.md', 0, 'Katil Dronlar belgeseli + KAAN Short + Abone ol', 'Bölüm 3 (6. nesil, Kızılelma anıldığında) → Katil Dronlar belgeseli', 'Savunma Teknolojileri'),
]

STEPS_B = [
 ('dosya', 'Video dosyasını yükle', 'MP4, 16:9, en az 1080p. Dosya adı: başlıkla aynı (SEO için).'),
 ('baslik', 'Başlığı yapıştır', 'Aşağıdaki önerilen başlık. 100 karakter sınırı; ilk 60–70 karakter aramada görünür.'),
 ('aciklama', 'Açıklamayı yapıştır', 'Bölüm zamanlarını kurgu bittikten sonra videodaki gerçek sürelerle kontrol et. İlk satır 00:00 olmalı.'),
 ('kucukresim', 'Küçük resmi yükle', '1280×720 px, 2 MB altı, JPG/PNG. Büyük yazı en fazla 3 kelime.'),
 ('liste', 'Oynatma listesine ekle', ''),
 ('kitle', 'Kitle: "Hayır, çocuklara özel değil"', 'Siber suç ve savaş konuları çocuklara yönelik değil.'),
 ('yas', 'Yaş kısıtlaması: Hayır', 'Savaş görüntüleri sansürlü olduğu sürece gerekmez.'),
 ('tanitim', 'Ücretli tanıtım: Hayır', 'Sponsor varsa "Evet" işaretle.'),
 ('sentetik', 'Değiştirilmiş veya sentetik içerik', 'Gerçek bir kişi, yer ya da olay gibi görünen yapay zekâ sahnesi veya gerçek birinin sesini taklit eden yapay zekâ sesi kullandıysan "Evet" seç. Sadece yapay zekâ seslendirme ya da açıkça stilize/temsili görseller için genelde gerekmez.'),
 ('etiket', 'Etiketleri yapıştır', 'Daha fazla göster → Etiketler. Virgülle ayrılmış, 500 karakter sınırı.'),
 ('dil', 'Dil: Türkçe · Kategori: Bilim ve Teknoloji', ''),
 ('altyazi', 'Altyazıyı yükle', 'Altyazılar → Dosya yükle → Zamanlamalı → uretim/…/altyazi.srt (Türkçe).'),
 ('bitis', 'Bitiş ekranı ekle', ''),
 ('kart', 'Bilgi kartlarını ekle', ''),
 ('planla', 'Görünürlük: Planla', 'Türkiye için akşam 19:00–21:00 arası iyi bir başlangıç; kendi Analytics verine göre ayarla.'),
 ('yorum', 'Yayından sonra: yorumu yapıştır ve sabitle', ''),
]
STEPS_R = [
 ('dosya', 'Dikey videoyu yükle', '9:16, 1080×1920, 3 dakikadan kısa. Kapak yazısı ilk karede okunur olsun.'),
 ('baslik', 'Başlığı yapıştır', '#shorts başlıkta veya açıklamada olsun.'),
 ('aciklama', 'Açıklamayı yapıştır', ''),
 ('kapak', 'Kapak karesini seç', 'YouTube mobil uygulamasında Shorts yüklerken kapak karesi seçilebilir; kapak yazısının göründüğü kareyi seç.'),
 ('ilgili', 'İlgili videoyu bağla', 'Shorts ayarlarında "İlgili video" → belgeseli seç. Belgesel henüz yayında değilse yayınlandıktan sonra geri dönüp ekle.'),
 ('kitle', 'Kitle: "Hayır, çocuklara özel değil"', ''),
 ('sentetik', 'Değiştirilmiş veya sentetik içerik', 'Gerçek olay ya da kişi gibi görünen yapay zekâ görüntüsü varsa "Evet".'),
 ('etiket', 'Etiketleri yapıştır', ''),
 ('altyazi', 'Altyazıyı yükle', 'uretim/…/altyazi.srt'),
 ('planla', 'Görünürlük: Planla', ''),
 ('yorum', 'Yayından sonra: yorumu yapıştır ve sabitle', ''),
]

def copybox(label, text, cid, limit=None):
    n = len(text); warn = ''
    if limit: warn = f'<span class="cnt{" over" if n > limit else ""}">{n}/{limit}</span>'
    return (f'<div class="field"><div class="fh"><span class="fl">{label}</span>{warn}</div>'
            f'<div class="pw"><button type="button" class="cp">Kopyala</button><pre id="{cid}">{html.escape(text)}</pre></div></div>')

cards = []; toc = []
for pk, day, vid, kind, path, tsel, endscr, link, plist in VIDEOS:
    md = read(path)
    if kind == 'belgesel':
        ts = titles(md); title = ts[tsel]; alts = [t for i, t in enumerate(ts) if i != tsel]
        big, idea = thumb(md)
        tags = section(md, 'Etiketler').split('\n')[0].strip()
        steps = STEPS_B
    else:
        title = tsel; alts = []
        big = re.sub(r'^\*\*"?|"?\*\*$', '', section(md, 'Kapak Yazısı')); idea = 'Kapak yazısını videonun ilk karesine ekle.'
        desc0 = unquote(section(md, 'Açıklama'))
        tags = ', '.join(h.lstrip('#') for h in re.findall(r'#\S+', desc0) if h.lower() != '#shorts')
        steps = STEPS_R
    desc = unquote(section(md, 'Açıklama'))
    name = re.sub(r'^# (BELGESEL|REELS) \d+ — ', '', md.split('\n', 1)[0])
    pin = pinned(md)
    extra = {'liste': plist, 'bitis': endscr or '', 'kart': link if kind == 'belgesel' else '', 'ilgili': link if kind == 'reels' else ''}
    st = ''.join(
        f'<li><label><input type="checkbox" id="{vid}-{k}" data-v="{vid}"><span><b>{html.escape(t)}</b>'
        + (f'<small>{html.escape(extra[k])}</small>' if extra.get(k) else '')
        + (f'<small>{html.escape(n)}</small>' if n else '') + '</span></label></li>' for k, t, n in steps)
    fields = copybox('Başlık', title, f'{vid}-t', 100)
    if alts: fields += '<p class="alts"><span class="fl">Alternatif başlıklar</span>' + ''.join(f'<span>{html.escape(a)}</span>' for a in alts) + '</p>'
    fields += copybox('Açıklama', desc, f'{vid}-d', 5000) + copybox('Etiketler', tags, f'{vid}-g', 500)
    if pin: fields += copybox('Sabitlenecek yorum', pin, f'{vid}-p')
    fields += (f'<div class="field"><div class="fh"><span class="fl">{"Küçük resim" if kind=="belgesel" else "Kapak"}</span></div>'
               f'<p class="thumb"><strong>{html.escape(big)}</strong><span>{html.escape(idea).replace(chr(10), "<br>")}</span></p></div>')
    kl = 'Belgesel' if kind == 'belgesel' else 'Reels'
    cards.append(f'''<section class="vid" id="{vid}"><header class="vh"><div class="meta"><span class="day">Paket {pk} · {day}. gün</span><span class="kind k-{kind}">{kl}</span><span class="prog" data-v="{vid}" data-n="{len(steps)}">0/{len(steps)}</span></div><h2>{html.escape(name)}</h2></header>
<div class="cols"><ol class="steps">{st}</ol><div class="fields">{fields}</div></div></section>''')
    toc.append(f'<a class="ti" href="#{vid}"><span class="day">P{pk} · {day}. gün</span><span class="kind k-{kind}">{kl}</span><span class="tn">{html.escape(name)}</span><span class="prog" data-v="{vid}" data-n="{len(steps)}">0/{len(steps)}</span></a>')

tpl = open(sys.argv[3] if len(sys.argv) > 3 else __file__.replace('yukleme_listesi.py', 'yukleme_template.html'), encoding='utf-8').read()
open(OUT, 'w', encoding='utf-8').write(tpl.replace('%%TOC%%', ''.join(toc)).replace('%%CARDS%%', ''.join(cards)))
print('ok', len(cards))
