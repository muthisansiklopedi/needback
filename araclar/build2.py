import markdown, re, sys, html
root = sys.argv[1]; out = sys.argv[2]
PROD={"siber":"01-siber-saldirilar","kaan":"02-kaan","reels-stuxnet":"03-reels-stuxnet","reels-kaan":"04-reels-kaan","reels-sifre":"05-reels-sifre"}
items = [
 ("siber","Belgesel","Dünyayı Durduran Siber Saldırılar",'8–10 dk',"belgeseller/01-dunyayi-durduran-siber-saldirilar.md"),
 ("kaan","Belgesel","Savaş Uçaklarının Geleceği ve KAAN",'7–9 dk',"belgeseller/02-savas-ucaklarinin-gelecegi-kaan.md"),
 ("reels-stuxnet","Reels","Bir USB bellek nükleer tesisi durdurdu","~50 sn","reels/reels-01-usb-ile-nukleer-tesis.md"),
 ("reels-kaan","Reels","F-35'ten çıkarıldı, KAAN'ı yaptı","~50 sn","reels/reels-02-f35ten-kaana.md"),
 ("reels-sifre","Reels","Şifren sızdı mı?","~55 sn","reels/reels-03-sifren-sizdi-mi.md"),
]
def conv(md):
    md = re.sub(r'^# .*\n', '', md, count=1)  # drop H1, we render our own
    h = markdown.markdown(md, extensions=['tables','sane_lists','fenced_code'])
    h = h.replace('<table>','<div class="tw"><table>').replace('</table>','</table></div>')
    h = re.sub(r'(<h3>)(\d+:\d+ – \d+:\d+) \| ', r'\1<span class="tc">\2</span> ', h)
    h = re.sub(r'❌ (HATA #\d+)', r'<span class="err">\1</span>', h)
    return h
def prod(i):
    base=f"{root}/uretim/{PROD[i]}"
    def md(f):
        h=conv(open(f"{base}/{f}",encoding='utf-8').read())
        return h
    pr=md('sahne-promptlari.md').replace('<pre><code>','<div class="pw"><button type="button" class="cp">Kopyala</button><pre><code>').replace('</code></pre>','</code></pre></div>')
    srt=html.escape(open(f"{base}/altyazi.srt",encoding='utf-8').read())
    n=srt.count(' --&gt; ')
    return (f'<div class="prod"><p class="label">Prodüksiyon dosyaları</p>'
      f'<details><summary>Seslendirme metni</summary><div class="prose">{md("seslendirme.md")}</div></details>'
      f'<details><summary>Sahne promptları</summary><div class="prose">{pr}</div></details>'
      f'<details><summary>Altyazı (.srt, {n} satır)</summary><div class="pw"><button type="button" class="cp">Kopyala</button><pre class="srt"><code>{srt}</code></pre></div></details></div>')
nav = ''.join(f'<a class="nav-i" href="#{i}"><span class="kind k-{k.lower()}">{k}</span><span class="nt">{html.escape(t)}</span><span class="dur">{d}</span></a>' for i,k,t,d,_ in items)
secs = ''
for n,(i,k,t,d,f) in enumerate(items,1):
    body = conv(open(f"{root}/{f}",encoding='utf-8').read())
    secs += f'<section class="piece" id="{i}"><header class="ph"><div class="meta"><span class="kind k-{k.lower()}">{k}</span><span class="dur">{d}</span></div><h2>{html.escape(t)}</h2></header><div class="prose">{body}</div>'+prod(i)+'<a class="top" href="#ust">↑ Başa dön</a></section>'
tpl = open(sys.argv[3],encoding='utf-8').read()
open(out,'w',encoding='utf-8').write(tpl.replace('%%NAV%%',nav).replace('%%SECS%%',secs))
