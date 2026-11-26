"""Mazgal belgeseli için kod ile çizilen canlandırmalı SAHNELER (siluet/illüstrasyon).
Her sahne dikişsiz döngü (period = T). Ham RGB24 ffmpeg'e borulanır.

Kullanım: python3 animasyon_sahneler.py <sahne_adi> <cikti.mp4> [T] [fps] [W] [H]
Sahneler: arac, operasyon, haritalama, hedef, hacker, korunma, yorum, kapanis
"""
import sys, math, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont

name = sys.argv[1]; out = sys.argv[2]
T   = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
FPS = int(sys.argv[4])   if len(sys.argv) > 4 else 25
W   = int(sys.argv[5])   if len(sys.argv) > 5 else 1920
H   = int(sys.argv[6])   if len(sys.argv) > 6 else 1080
nframes = int(round(T * FPS))
GREEN=(0,255,156); ORANGE=(233,132,71); STEEL=(47,59,53); INK=(12,16,15)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# gradyan arka plan + soluk düğüm alanı (süreklilik için)
grad=np.zeros((H,W,3),np.uint8)
for y in range(H):
    f=y/(H-1); grad[y,:]=(int(20-10*f),int(25-11*f),int(23-7*f))
base=Image.fromarray(grad,'RGB')
rng=np.random.default_rng(3); M=26
nbx=rng.uniform(0,1,M)*W; nby=rng.uniform(0,1,M)*H
nax=rng.uniform(6,26,M); nphi=rng.uniform(0,6.28,M)

def faint_field(d,ph):
    xs=nbx+nax*np.sin(ph+nphi); ys=nby+nax*np.cos(ph+nphi)
    for i in range(M):
        d.ellipse([xs[i]-2,ys[i]-2,xs[i]+2,ys[i]+2],fill=(0,255,156,55))

def rings(d,ox,oy,ph,maxr,col,n=3,wd=3):
    for k in range(n):
        fr=((ph/(2*math.pi))+k/n)%1.0; r=fr*maxr; a=int(150*(1-fr)*fr*4)
        if a>5: d.ellipse([ox-r,oy-r,ox+r,oy+r],outline=col+(min(a,150),),width=wd)

def wifi_arcs(d,x,y,col,a=180):
    for i,r in enumerate((14,26,38)):
        d.arc([x-r,y-r,x+r,y+r],225,315,fill=col+(a-i*30,),width=3)
    d.ellipse([x-4,y-4,x+4,y+4],fill=col+(a,))

def sc_arac(d,ph):  # gece, anten taşıyan araç + Wi-Fi halkaları (wardriving)
    gy=int(H*0.60); d.rectangle([0,gy,int(H*0.0)+W,gy+90],fill=(8,11,10,255))
    d.line([0,gy,W,gy],fill=(0,255,156,60),width=2)
    for sx in range(80,W,160):  # yol çizgileri
        d.rectangle([sx,gy+90,sx+70,gy+96],fill=(47,59,53,180))
    cx=int(W*0.30+40*math.sin(ph)); cy=gy-6+int(3*math.sin(ph*2))
    body=(10,12,11,255); rim=(0,255,156,120)
    d.polygon([(cx-150,cy),(cx-120,cy-55),(cx+60,cy-58),(cx+95,cy),(cx+150,cy),(cx+150,cy+10),(cx-150,cy+10)],fill=body,outline=rim)
    d.polygon([(cx-95,cy-54),(cx-30,cy-92),(cx+40,cy-92),(cx+55,cy-56)],fill=(16,22,20,255),outline=rim)  # kabin
    for wx in (cx-95,cx+95):
        d.ellipse([wx-26,cy-6,wx+26,cy+46],fill=(5,6,6,255),outline=rim,width=3)
        d.ellipse([wx-9,cy+11,wx+9,cy+29],fill=(30,36,33,255))
    d.ellipse([cx+150,cy-20,cx+230,cy+6],fill=(233,132,71,40))  # far
    ax,ay=cx+10,cy-92; d.line([ax,ay,ax,ay-70],fill=(0,255,156,200),width=3)  # anten
    d.ellipse([ax-6,ay-76,ax+6,ay-64],fill=ORANGE+(255,))
    rings(d,ax,ay-70,ph,520,ORANGE,4,3); rings(d,ax,ay-70,ph+2.0,520,GREEN,4,2)

def sc_operasyon(d,ph):  # iki şehir pini + şebeke + kalkan/kilit
    pts=[(int(W*0.30),int(H*0.40)),(int(W*0.64),int(H*0.56))]
    d.line([pts[0],pts[1]],fill=(0,255,156,90),width=2)
    for i,(x,y) in enumerate(pts):
        bl=int(120+120*abs(math.sin(ph+i)))
        d.line([x,y,x,y-54],fill=(233,132,71,220),width=4)
        d.ellipse([x-16,y-78,x+16,y-46],outline=ORANGE+(255,),width=4,fill=(30,20,14,bl))
        d.ellipse([x-6,y-2,x+6,y+6],fill=ORANGE+(220,))
    # kalkan
    sx,sy=int(W*0.80),int(H*0.46); s=80
    d.polygon([(sx,sy-s),(sx+s*0.8,sy-s*0.6),(sx+s*0.8,sy+s*0.3),(sx,sy+s),(sx-s*0.8,sy+s*0.3),(sx-s*0.8,sy-s*0.6)],fill=(16,22,20,255),outline=GREEN+(200,))
    pl=int(120+100*abs(math.sin(ph*1.5)))
    d.line([sx-24,sy+2,sx-6,sy+22],fill=GREEN+(pl,),width=7); d.line([sx-6,sy+22,sx+30,sy-22],fill=GREEN+(pl,),width=7)

def sc_haritalama(d,ph):  # binalar + Wi-Fi + tarama çizgisi + mini harita
    gy=int(H*0.60); d.line([0,gy,W,gy],fill=(0,255,156,50),width=2)
    bx=[int(W*0.14),int(W*0.30),int(W*0.46),int(W*0.62)]; bh=[220,300,180,260]
    for i,x in enumerate(bx):
        d.rectangle([x,gy-bh[i],x+120,gy],fill=(14,19,17,255),outline=(0,255,156,90))
        for wy in range(gy-bh[i]+24,gy-20,46):
            for wx in range(x+16,x+108,34): d.rectangle([wx,wy,wx+16,wy+20],fill=(0,255,156,40))
        wifi_arcs(d,x+60,gy-bh[i]-6,GREEN,160)
    sweep=int((ph/(2*math.pi))*W)  # tarama çizgisi
    d.rectangle([sweep-3,0,sweep+3,gy],fill=(233,132,71,120))
    d.line([sweep,0,sweep,gy],fill=ORANGE+(220,),width=2)
    # mini harita paneli
    px,py,pw,pph=int(W*0.72),int(H*0.16),int(W*0.22),int(H*0.34)
    d.rectangle([px,py,px+pw,py+pph],fill=(10,14,13,220),outline=(0,255,156,120))
    for i in range(10):
        rx=px+18+(i*53)%(pw-36); ry=py+22+((i*101)%(pph-40))
        col=ORANGE if i%4==0 else GREEN
        d.ellipse([rx-5,ry-5,rx+5,ry+5],fill=col+(200,))

def sc_hedef(d,ph):  # güçlü duvar ama sızan Wi-Fi sinyali (zayıf halka)
    wx,wy,ww,wh=int(W*0.16),int(H*0.20),int(W*0.40),int(H*0.36)
    d.rectangle([wx,wy,wx+ww,wy+wh],fill=(16,22,20,255),outline=(0,255,156,150))
    for yy in range(wy,wy+wh,46):  # tuğla
        off=0 if (yy-wy)//46%2==0 else 45
        for xx in range(wx+off,wx+ww,90): d.line([xx,yy,xx,yy+46],fill=(0,255,156,40),width=1)
        d.line([wx,yy,wx+ww,yy],fill=(0,255,156,40),width=1)
    gap=(wx+ww,wy+int(wh*0.55))  # yan taraftan sızıntı
    glow=int(150+90*abs(math.sin(ph*1.6)))
    d.rectangle([gap[0]-6,gap[1]-18,gap[0]+10,gap[1]+18],fill=ORANGE+(glow,))
    rings(d,gap[0]+6,gap[1],ph,460,ORANGE,4,3)
    d.text((wx+20,wy+16),'KRİTİK AĞ',font=ImageFont.truetype(FB,30),fill=(0,255,156,180))

def sc_hacker(d,ph):  # casus yazılım arkasındaki kapüşonlu hacker + laptop + iş ilanı + coin
    dy=int(H*0.60); d.line([int(W*0.10),dy,int(W*0.92),dy],fill=(47,59,53,200),width=3)
    cx,cy=int(W*0.36),dy
    rim=(0,255,156,110)
    d.polygon([(cx-120,cy),(cx-96,cy-150),(cx-30,cy-210),(cx+30,cy-210),(cx+96,cy-150),(cx+120,cy)],fill=(9,12,11,255),outline=rim)  # gövde/kapüşon
    d.ellipse([cx-52,cy-214,cx+52,cy-120],fill=(6,8,7,255),outline=rim)  # yüz boşluğu (karanlık)
    fl=int(120+90*abs(math.sin(ph*3)))  # monitör parıltısı yüze vuruyor
    d.polygon([(cx-40,cy-150),(cx+40,cy-150),(cx+70,cy-70),(cx-70,cy-70)],fill=(0,255,156,int(fl*0.18)))
    lx,ly=cx,cy-58  # laptop
    d.polygon([(lx-95,ly),(lx+95,ly),(lx+120,ly+34),(lx-120,ly+34)],fill=(16,22,20,255),outline=rim)
    d.rectangle([lx-80,ly-70,lx+80,ly],fill=(8,11,10,255),outline=rim)
    for i in range(5):  # kayan kod satırları
        yy=ly-62+i*12; off=int((ph/(2*math.pi))*40)
        d.line([lx-70,yy,lx-70+((20+i*27+off)%130),yy],fill=(0,255,156,150),width=3)
    # telefon + iş ilanı balonu + coin
    phx,phy=int(W*0.68),dy-40
    d.rectangle([phx-50,phy-150,phx+50,phy],fill=(14,19,17,255),outline=rim)
    br=int(((ph/(2*math.pi))*1.0)%1.0)  # balon yükselir
    byoff=int(60*((ph/(2*math.pi))%1.0))
    ba=int(220*(1-((ph/(2*math.pi))%1.0)))
    d.rounded_rectangle([phx-44,phy-96-byoff,phx+44,phy-60-byoff],8,fill=(0,255,156,max(ba//3,20)),outline=GREEN+(max(ba,40),))
    d.text((phx-36,phy-92-byoff),'İŞ İLANI',font=ImageFont.truetype(FB,16),fill=(0,255,156,max(ba,60)))
    # kripto coin (dönüyor: genişlik salınır)
    ccx,ccy=int(W*0.80),dy-120; cw=int(6+30*abs(math.cos(ph)))
    d.ellipse([ccx-cw,ccy-34,ccx+cw,ccy+34],fill=(30,20,10,255),outline=ORANGE+(255,),width=4)
    if cw>14: d.text((ccx-9,ccy-18),'B',font=ImageFont.truetype(FB,38),fill=ORANGE+(255,))

def sc_korunma(d,ph):  # router+kilit, ayrık misafir/iç ağ, kalkan onay
    rx,ry=int(W*0.24),int(H*0.40)
    d.rounded_rectangle([rx-120,ry-40,rx+120,ry+40],12,fill=(16,22,20,255),outline=GREEN+(200,))
    for i,ax in enumerate((rx-150,rx+150)): d.line([rx-60+i*120,ry-40,ax,ry-110],fill=(0,255,156,160),width=3)
    for i in range(4): d.ellipse([rx-80+i*45,ry-6,rx-68+i*45,ry+6],fill=GREEN+(200,))
    lk=int(150+90*abs(math.sin(ph*1.6)))  # kilit
    d.rectangle([rx-20,ry+4,rx+20,ry+34],fill=ORANGE+(lk,)); d.arc([rx-14,ry-14,rx+14,ry+16],180,360,fill=ORANGE+(lk,),width=5)
    # iki ayrık ağ bulutu
    d.line([int(W*0.52),int(H*0.22),int(W*0.52),int(H*0.56)],fill=(47,59,53,220),width=4)
    for cxp,lbl in ((int(W*0.66),'İÇ AĞ'),(int(W*0.84),'MİSAFİR')):
        d.ellipse([cxp-90,int(H*0.30),cxp+90,int(H*0.46)],outline=GREEN+(160,),width=3)
        d.text((cxp-54,int(H*0.36)),lbl,font=ImageFont.truetype(FB,26),fill=(0,255,156,200))

def sc_yorum(d,ph):  # şehir silueti üstünde tarayan göz/radar
    gy=int(H*0.60)
    for x in range(0,W,70):
        hh=120+((x*37)%180); d.rectangle([x,gy-hh,x+54,gy],fill=(12,16,15,255),outline=(0,255,156,45))
    ex,ey=int(W*0.5),int(H*0.32)
    d.ellipse([ex-150,ey-80,ex+150,ey+80],outline=GREEN+(180,),width=4)  # göz dış
    ix=ex+int(60*math.sin(ph))
    d.ellipse([ix-46,ey-46,ix+46,ey+46],outline=ORANGE+(220,),width=4)  # iris
    d.ellipse([ix-14,ey-14,ix+14,ey+14],fill=ORANGE+(230,))
    rings(d,ix,ey,ph,260,GREEN,3,2)

def sc_kapanis(d,ph):  # Mazgal kalkan logosu
    cx,cy=W//2,int(H*0.38); s=140; g=int(170+70*abs(math.sin(ph*1.2)))
    d.polygon([(cx,cy-s),(cx+s*0.8,cy-s*0.55),(cx+s*0.8,cy+s*0.35),(cx,cy+s),(cx-s*0.8,cy+s*0.35),(cx-s*0.8,cy-s*0.55)],fill=(12,16,15,255),outline=GREEN+(g,))
    d.line([cx-46,cy+4,cx-10,cy+42],fill=GREEN+(g,),width=12); d.line([cx-10,cy+42,cx+54,cy-40],fill=GREEN+(g,),width=12)
    d.text((cx-150,cy+s+30),'MAZGAL',font=ImageFont.truetype(FB,72),fill=ORANGE+(255,))

SCENES={'arac':sc_arac,'operasyon':sc_operasyon,'haritalama':sc_haritalama,'hedef':sc_hedef,
        'hacker':sc_hacker,'korunma':sc_korunma,'yorum':sc_yorum,'kapanis':sc_kapanis}
fn=SCENES[name]

ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),
 '-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
for fi in range(nframes):
    ph=2*math.pi*fi/nframes
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    faint_field(d,ph); fn(d,ph)
    ff.stdin.write(Image.alpha_composite(base.convert('RGBA'),ov).convert('RGB').tobytes())
ff.stdin.close(); ff.wait()
print('sahne ok:',name,out)
