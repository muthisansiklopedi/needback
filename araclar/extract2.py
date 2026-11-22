import re, sys, json
def belgesel(path):
    lines=open(path,encoding='utf-8').read().split('\n')
    out=[]; sec=None; on=False
    for l in lines:
        if l.startswith('## Prodüksiyon'): break
        m=re.match(r'^### (\d+:\d+) – (\d+:\d+) \| (.*)',l)
        if m: sec={'start':m[1],'end':m[2],'title':m[3],'paras':[]}; out.append(sec); continue
        if sec is None: continue
        if l.startswith('**Anlatıcı') or l.startswith('**Mazgal yorumu') : on=True; continue
        if l.startswith('**') or l.startswith('---') or l.startswith('#'): 
            if not l.startswith('#### '): on=False
            continue
        if on and l.startswith('>'):
            t=re.sub(r'^>+\s?','',l).strip()
            t=t.replace('**','')
            if t and not t.startswith('**'):
                t=re.sub(r'^- ','',t)
                t=re.sub(r'^\d+\. ','',t) if False else t
                sec['paras'].append(t)
    return out
def reels(path):
    out=[]
    for l in open(path,encoding='utf-8'):
        if l.startswith('|') and re.match(r'\|\s*\d',l):
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            out.append({'time':c[0],'visual':c[1],'voice':c[2].strip('"“”').replace('**',''),'text':c[3]})
    return out
r='/home/user/needback/icerikler/paket-02/'
d={'b1':belgesel(r+'belgeseller/01-dunyayi-durduran-siber-saldirilar.md'),'b2':belgesel(r+'belgeseller/02-savas-ucaklarinin-gelecegi-kaan.md'),
 'r1':reels(r+'reels/reels-01-usb-ile-nukleer-tesis.md'),'r2':reels(r+'reels/reels-02-f35ten-kaana.md'),'r3':reels(r+'reels/reels-03-sifren-sizdi-mi.md')}
json.dump(d,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
for k in ('b1','b2'):
    for s in d[k]: print(k,s['start'],s['title'][:40],len(s['paras']),sum(len(p.split()) for p in s['paras']))
for k in ('r1','r2','r3'): print(k,len(d[k]),sum(len(x['voice'].split()) for x in d[k]))
