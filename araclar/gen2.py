import json, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prompts2 import *
S=os.path.dirname(__file__); R='/home/user/needback/icerikler/paket-02'
d=json.load(open(f'{S}/narr2.json',encoding='utf-8'))
WPS=2.3; PARA=0.8; SEC=3.0
def fmt_mmss(t): t=int(round(t)); return f"{t//60}:{t%60:02d}"
def fmt_srt(t):
    ms=int(round(t*1000)); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
def chunks(text, maxc=80):
    out=[]
    for sent in re.split(r'(?<=[.!?…])\s+', text):
        words=sent.split(); cur=[]
        for w in words:
            if cur and len(' '.join(cur+[w]))>maxc: out.append(' '.join(cur)); cur=[]
            cur.append(w)
        if cur: out.append(' '.join(cur))
    return out
def two_lines(s):
    if len(s)<=42: return s
    ws=s.split(); best=None
    for i in range(1,len(ws)):
        a,b=' '.join(ws[:i]),' '.join(ws[i:]); sc=max(len(a),len(b))
        if best is None or sc<best[0]: best=(sc,a,b)
    return best[1]+'\n'+best[2]
def dur(text): return max(1.2, len(text.split())/WPS)

def build_belgesel(key):
    t=0.0; cues=[]; secs=[]
    for s in d[key]:
        st=t
        for p in s['paras']:
            for c in chunks(p):
                dd=dur(c); cues.append((t,t+dd,c)); t+=dd
            t+=PARA
        t+=SEC; secs.append((st,t))
    return cues, secs, t
def build_reels(key):
    cues=[]
    for row in d[key]:
        a,b=[float(x) for x in re.findall(r'\d+',row['time'])[:2]]
        cs=chunks(row['voice'],70); tw=sum(len(c.split()) for c in cs); t=a
        for c in cs:
            dd=(b-a)*len(c.split())/tw; cues.append((t,t+dd-0.05,c)); t+=dd
    return cues
def srt(cues): return '\n'.join(f"{i}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{two_lines(c)}\n" for i,(a,b,c) in enumerate(cues,1))

def write(path,txt):
    os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w',encoding='utf-8').write(txt)

meta={}
def prompt_md(title, groups, style, vertical=False):
    o=[f"# {title} — Sahne Promptları\n",
       "Görsel üretim araçları (Midjourney, Leonardo, Firefly, Ideogram vb.) için İngilizce promptlar. Mazgal görsel teması her prompta eklidir: **koyu arduvaz yeşili + yanık turuncu renk, film greni, sinematik ışık.**\n",
       f"**Ortak stil eki:** `{style}`  \n**Negatif prompt:** `{NEG}`\n",
       "> ⚠️ `*` işaretli sahnelerde (gerçek uçak/SİHA) yapay zekâ modelleri bu araçları doğru çizemez. Bu sahnelerde TUSAŞ, Baykar, MSB ve üretici firmaların resmi görüntülerini kaynak belirterek kullanın; prompt yalnızca yedek/arka plan içindir. Gerçek kişileri yapay zekâ ile canlandırmayın, silüet kullanın.\n"]
    n=1
    for head, items in groups:
        o.append(f"\n## {head}\n")
        for lab,p in items:
            o.append(f"**{n:02d}. {lab}**\n```\n{p}, {style} --no {NEG}\n```\n"); n+=1
    return '\n'.join(o), n-1

slugs={'b1':('01-siber-saldirilar','Dünyayı Durduran Siber Saldırılar','belgeseller/01-dunyayi-durduran-siber-saldirilar.md',B1),
       'b2':('02-kaan','Savaş Uçaklarının Geleceği ve KAAN','belgeseller/02-savas-ucaklarinin-gelecegi-kaan.md',B2)}
for k,(slug,title,mdf,P) in slugs.items():
    cues,secs,total=build_belgesel(k)
    # 1) update script timecodes
    md=open(f'{R}/{mdf}',encoding='utf-8').read()
    olds=[(s['start'],s['end']) for s in d[k]]
    for (os_,oe),(ns,ne) in zip(olds,secs):
        md=md.replace(f"### {os_} – {oe} |", f"### {fmt_mmss(ns)} – {fmt_mmss(ne)} |",1)
    lines=md.split('\n'); i_ch=0
    for j,l in enumerate(lines):
        m=re.match(r'^> (\d\d:\d\d) (.*)',l)
        if m and i_ch<len(secs):
            ts=int(round(secs[i_ch][0])); lines[j]=f"> {ts//60:02d}:{ts%60:02d} {m[2]}"; i_ch+=1
    md='\n'.join(lines)
    lo=int(total//60); md=re.sub(r'\*\*Hedef süre:\*\* .*', f"**Hedef süre:** {lo}–{lo+2} dakika (anlatım ≈ {fmt_mmss(total)}; geçiş ve müzik araları dahil)", md)
    write(f'{R}/{mdf}',md)
    meta[k]=(lo,total)
    # 2) narration
    o=[f"# {title} — Seslendirme Metni\n",
       f"Sadece anlatıcının okuyacağı metin. Tahmini okuma süresi: **{fmt_mmss(total)}** (dakikada ~{int(WPS*60)} kelime).\n",
       "Okuma işaretleri: `/` kısa nefes, `//` uzun durak. **Kalın** kelimeler vurgulu okunur.\n"]
    for s,(a,b) in zip(d[k],secs):
        o.append(f"\n## [{fmt_mmss(a)}] {s['title']}\n")
        for p in s['paras']: o.append(p+" //\n")
    write(f'{R}/uretim/{slug}/seslendirme.md','\n'.join(o))
    # 3) prompts
    groups=[(f"[{fmt_mmss(a)}] {s['title']}", pv) for s,(a,b),pv in zip(d[k],secs,P.values())]
    pm,cnt=prompt_md(title,groups,STYLE_169); write(f'{R}/uretim/{slug}/sahne-promptlari.md',pm)
    # 4) srt
    write(f'{R}/uretim/{slug}/altyazi.srt',srt(cues))
    print(k,fmt_mmss(total),len(cues),'cues',cnt,'prompts')

rs={'r1':('03-reels-stuxnet','Reels 1 — Bir USB Bellek Nükleer Tesisi Durdurdu',R1),
    'r2':('04-reels-kaan',"Reels 2 — F-35'ten Çıkarıldı, KAAN'ı Yaptı",R2),
    'r3':('05-reels-sifre','Reels 3 — Şifren Sızdı mı?',R3)}
for k,(slug,title,P) in rs.items():
    rows=d[k]; cues=build_reels(k)
    o=[f"# {title} — Seslendirme Metni\n","Hızlı ve enerjik okunur. Her satır kendi süresine sığmalı.\n"]
    for r in rows: o.append(f"**[{r['time']}]** {r['voice']}\n")
    write(f'{R}/uretim/{slug}/seslendirme.md','\n'.join(o))
    groups=[(f"[{r['time']}]", [(lab,p)]) for r,(lab,p) in zip(rows,P)]
    pm,cnt=prompt_md(title,groups,STYLE_916,True); write(f'{R}/uretim/{slug}/sahne-promptlari.md',pm)
    write(f'{R}/uretim/{slug}/altyazi.srt',srt(cues))
    print(k,len(cues),'cues',cnt)
json.dump(meta,open(f'{S}/meta2.json','w'))
