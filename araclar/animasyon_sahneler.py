"""Mazgal belgeselleri için kod ile çizilen canlandırmalı SAHNE kütüphanesi (siluet/illüstrasyon).
Her sahne dikişsiz döngü (period = kare sayısı). Ham RGB24 ffmpeg'e borulanır.
Sahne alanı (stage): üst 175px başlık bandına, alt ~%40 altyazıya bırakılır.

Kullanım: python3 animasyon_sahneler.py <sahne> <cikti.mp4> [T] [fps] [W] [H]
Sahneler: arac operasyon haritalama hedef hacker korunma yorum kapanis
          dron avcidron jet fabrika kure usb fidye kripto telefon sebeke
"""
import sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

name=sys.argv[1]; out=sys.argv[2]
T=float(sys.argv[3]) if len(sys.argv)>3 else 8.0
FPS=int(sys.argv[4]) if len(sys.argv)>4 else 25
W=int(sys.argv[5]) if len(sys.argv)>5 else 1920
H=int(sys.argv[6]) if len(sys.argv)>6 else 1080
NF=int(round(T*FPS))
GREEN=(0,255,156); ORANGE=(233,132,71); STEEL=(47,59,53)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def F(s): return ImageFont.truetype(FB,s)
GY=int(H*0.60)          # zemin çizgisi
CY=int(H*0.40)          # sahne dikey merkezi

grad=np.zeros((H,W,3),np.uint8)
for y in range(H):
    f=y/(H-1); grad[y,:]=(int(20-10*f),int(25-11*f),int(23-7*f))
base=Image.fromarray(grad,'RGB')
rng=np.random.default_rng(3); M=26
nbx=rng.uniform(0,1,M)*W; nby=rng.uniform(0,1,M)*H; nax=rng.uniform(6,26,M); nphi=rng.uniform(0,6.28,M)
def field(d,ph):
    xs=nbx+nax*np.sin(ph+nphi); ys=nby+nax*np.cos(ph+nphi)
    for i in range(M): d.ellipse([xs[i]-2,ys[i]-2,xs[i]+2,ys[i]+2],fill=(0,255,156,55))
def rings(d,ox,oy,ph,maxr,col,n=4,wd=3):
    for k in range(n):
        fr=((ph/(2*math.pi))+k/n)%1.0; r=fr*maxr; a=int(150*(1-fr)*fr*4)
        if a>5: d.ellipse([ox-r,oy-r,ox+r,oy+r],outline=col+(min(a,150),),width=wd)
def wifi(d,x,y,col,a=200,sc=1.0):
    for i,r in enumerate((18,34,50)):
        r=int(r*sc); d.arc([x-r,y-r,x+r,y+r],225,315,fill=col+(a-i*35,),width=4)
    d.ellipse([x-5,y-5,x+5,y+5],fill=col+(a,))
def ground(d):
    d.line([0,GY,W,GY],fill=(0,255,156,60),width=2)

def sc_arac(d,ph):
    d.rectangle([0,GY,W,GY+140],fill=(8,11,10,255)); ground(d)
    for sx in range(80,W,170): d.rectangle([sx,GY+100,sx+80,GY+107],fill=(47,59,53,180))
    cx=int(W*0.32+60*math.sin(ph)); cy=GY-8+int(4*math.sin(ph*2)); rim=(0,255,156,140); body=(10,12,11,255)
    d.polygon([(cx-210,cy),(cx-168,cy-78),(cx+84,cy-82),(cx+132,cy),(cx+210,cy),(cx+210,cy+14),(cx-210,cy+14)],fill=body,outline=rim)
    d.polygon([(cx-132,cy-76),(cx-42,cy-130),(cx+56,cy-130),(cx+78,cy-78)],fill=(16,22,20,255),outline=rim)
    for wx in (cx-132,cx+132):
        d.ellipse([wx-38,cy-8,wx+38,cy+66],fill=(5,6,6,255),outline=rim,width=4); d.ellipse([wx-13,cy+16,wx+13,cy+42],fill=(30,36,33,255))
    d.ellipse([cx+210,cy-28,cx+320,cy+8],fill=(233,132,71,45))
    ax,ay=cx+14,cy-130; d.line([ax,ay,ax,ay-100],fill=GREEN+(220,),width=4); d.ellipse([ax-8,ay-108,ax+8,ay-92],fill=ORANGE+(255,))
    rings(d,ax,ay-100,ph,620,ORANGE,4,4); rings(d,ax,ay-100,ph+2.0,620,GREEN,4,3)

def sc_operasyon(d,ph):
    pts=[(int(W*0.26),CY),(int(W*0.56),int(H*0.52))]
    d.line([pts[0],pts[1]],fill=(0,255,156,90),width=2)
    for i,(x,y) in enumerate(pts):
        bl=int(120+120*abs(math.sin(ph+i)))
        d.line([x,y,x,y-80],fill=ORANGE+(220,),width=6); d.ellipse([x-24,y-116,x+24,y-68],outline=ORANGE+(255,),width=5,fill=(30,20,14,bl)); d.ellipse([x-8,y-4,x+8,y+8],fill=ORANGE+(220,))
    sx,sy,s=int(W*0.80),CY,120
    d.polygon([(sx,sy-s),(sx+s*0.8,sy-s*0.6),(sx+s*0.8,sy+s*0.3),(sx,sy+s),(sx-s*0.8,sy+s*0.3),(sx-s*0.8,sy-s*0.6)],fill=(16,22,20,255),outline=GREEN+(210,))
    pl=int(130+100*abs(math.sin(ph*1.5))); d.line([sx-36,sy+4,sx-8,sy+34],fill=GREEN+(pl,),width=11); d.line([sx-8,sy+34,sx+46,sy-34],fill=GREEN+(pl,),width=11)

def sc_haritalama(d,ph):
    ground(d); bx=[int(W*0.10),int(W*0.26),int(W*0.42),int(W*0.58)]; bh=[300,400,240,350]
    for i,x in enumerate(bx):
        d.rectangle([x,GY-bh[i],x+150,GY],fill=(14,19,17,255),outline=GREEN+(100,))
        for wy in range(GY-bh[i]+30,GY-26,54):
            for wx in range(x+20,x+134,42): d.rectangle([wx,wy,wx+20,wy+26],fill=GREEN+(45,))
        wifi(d,x+75,GY-bh[i]-10,GREEN,170,1.2)
    sweep=int((ph/(2*math.pi))*W); d.rectangle([sweep-4,175,sweep+4,GY],fill=ORANGE+(120,)); d.line([sweep,175,sweep,GY],fill=ORANGE+(220,),width=2)
    px,py,pw,ph2=int(W*0.72),int(H*0.18),int(W*0.22),int(H*0.30)
    d.rectangle([px,py,px+pw,py+ph2],fill=(10,14,13,220),outline=GREEN+(130,))
    for i in range(12):
        rx=px+22+(i*61)%(pw-44); ry=py+26+((i*97)%(ph2-48)); col=ORANGE if i%4==0 else GREEN
        d.ellipse([rx-6,ry-6,rx+6,ry+6],fill=col+(210,))

def sc_hedef(d,ph):
    wx,wy,ww,wh=int(W*0.14),int(H*0.20),int(W*0.44),int(H*0.40)
    d.rectangle([wx,wy,wx+ww,wy+wh],fill=(16,22,20,255),outline=GREEN+(150,))
    for yy in range(wy,wy+wh,54):
        off=0 if (yy-wy)//54%2==0 else 55
        for xx in range(wx+off,wx+ww,110): d.line([xx,yy,xx,yy+54],fill=GREEN+(40,),width=1)
        d.line([wx,yy,wx+ww,yy],fill=GREEN+(40,),width=1)
    gap=(wx+ww,wy+int(wh*0.55)); glow=int(150+90*abs(math.sin(ph*1.6)))
    d.rectangle([gap[0]-8,gap[1]-24,gap[0]+14,gap[1]+24],fill=ORANGE+(glow,)); rings(d,gap[0]+8,gap[1],ph,560,ORANGE,4,4)
    d.text((wx+24,wy+20),'KRİTİK AĞ',font=F(36),fill=GREEN+(190,))

def sc_hacker(d,ph):
    d.line([int(W*0.06),GY,int(W*0.94),GY],fill=STEEL+(200,),width=4); rim=(0,255,156,120)
    cx,cy=int(W*0.34),GY
    d.polygon([(cx-170,cy),(cx-136,cy-212),(cx-44,cy-298),(cx+44,cy-298),(cx+136,cy-212),(cx+170,cy)],fill=(9,12,11,255),outline=rim)
    d.ellipse([cx-74,cy-302,cx+74,cy-170],fill=(6,8,7,255),outline=rim)
    fl=int(120+90*abs(math.sin(ph*3))); d.polygon([(cx-58,cy-212),(cx+58,cy-212),(cx+100,cy-100),(cx-100,cy-100)],fill=(0,255,156,int(fl*0.18)))
    lx,ly=cx,cy-82
    d.polygon([(lx-134,ly),(lx+134,ly),(lx+170,ly+48),(lx-170,ly+48)],fill=(16,22,20,255),outline=rim)
    d.rectangle([lx-112,ly-100,lx+112,ly],fill=(8,11,10,255),outline=rim)
    for i in range(6):
        yy=ly-88+i*15; off=int((ph/(2*math.pi))*56); d.line([lx-98,yy,lx-98+((28+i*37+off)%184),yy],fill=GREEN+(150,),width=3)
    phx,phy=int(W*0.66),GY-56
    d.rounded_rectangle([phx-66,phy-210,phx+66,phy],10,fill=(14,19,17,255),outline=rim)
    byoff=int(84*((ph/(2*math.pi))%1.0)); ba=int(230*(1-((ph/(2*math.pi))%1.0)))
    d.rounded_rectangle([phx-60,phy-134-byoff,phx+60,phy-84-byoff],10,fill=(0,255,156,max(ba//3,20)),outline=GREEN+(max(ba,40),))
    d.text((phx-50,phy-128-byoff),'İŞ İLANI',font=F(22),fill=GREEN+(max(ba,60),))
    ccx,ccy=int(W*0.80),GY-150; cw=int(8+42*abs(math.cos(ph)))
    d.ellipse([ccx-cw,ccy-46,ccx+cw,ccy+46],fill=(30,20,10,255),outline=ORANGE+(255,),width=5)
    if cw>18: d.text((ccx-13,ccy-26),'B',font=F(52),fill=ORANGE+(255,))

def sc_korunma(d,ph):
    rx,ry=int(W*0.24),CY
    d.rounded_rectangle([rx-160,ry-54,rx+160,ry+54],14,fill=(16,22,20,255),outline=GREEN+(210,))
    for i,ax in enumerate((rx-200,rx+200)): d.line([rx-80+i*160,ry-54,ax,ry-150],fill=GREEN+(170,),width=4)
    for i in range(4): d.ellipse([rx-104+i*60,ry-8,rx-88+i*60,ry+8],fill=GREEN+(210,))
    lk=int(150+90*abs(math.sin(ph*1.6))); d.rectangle([rx-26,ry+6,rx+26,ry+44],fill=ORANGE+(lk,)); d.arc([rx-18,ry-16,rx+18,ry+22],180,360,fill=ORANGE+(lk,),width=7)
    d.line([int(W*0.52),int(H*0.22),int(W*0.52),int(H*0.56)],fill=STEEL+(220,),width=4)
    for cxp,lbl in ((int(W*0.66),'İÇ AĞ'),(int(W*0.84),'MİSAFİR')):
        d.ellipse([cxp-110,CY-80,cxp+110,CY+80],outline=GREEN+(170,),width=3); d.text((cxp-64,CY-16),lbl,font=F(30),fill=GREEN+(210,))

def sc_yorum(d,ph):
    for x in range(0,W,80):
        hh=150+((x*37)%220); d.rectangle([x,GY-hh,x+62,GY],fill=(12,16,15,255),outline=GREEN+(45,))
    ground(d); ex,ey=int(W*0.5),int(H*0.34)
    d.ellipse([ex-200,ey-108,ex+200,ey+108],outline=GREEN+(190,),width=5)
    ix=ex+int(90*math.sin(ph)); d.ellipse([ix-62,ey-62,ix+62,ey+62],outline=ORANGE+(230,),width=5); d.ellipse([ix-20,ey-20,ix+20,ey+20],fill=ORANGE+(235,))
    rings(d,ix,ey,ph,320,GREEN,3,2)

def sc_kapanis(d,ph):
    cx,cy=W//2,int(H*0.38); s=180; g=int(180+70*abs(math.sin(ph*1.2)))
    d.polygon([(cx,cy-s),(cx+s*0.8,cy-s*0.55),(cx+s*0.8,cy+s*0.35),(cx,cy+s),(cx-s*0.8,cy+s*0.35),(cx-s*0.8,cy-s*0.55)],fill=(12,16,15,255),outline=GREEN+(g,))
    d.line([cx-56,cy+4,cx-12,cy+52],fill=GREEN+(g,),width=14); d.line([cx-12,cy+52,cx+66,cy-48],fill=GREEN+(g,),width=14)
    d.text((cx-180,cy+s+36),'MAZGAL',font=F(84),fill=ORANGE+(255,))

# ---- Yeni sahneler ----
def _quad(d,cx,cy,sc,ph,col=GREEN):  # dört pervaneli dron gövdesi
    rim=col+(200,)
    d.ellipse([cx-28*sc,cy-16*sc,cx+28*sc,cy+16*sc],fill=(14,19,17,255),outline=rim,width=3)
    for dx,dy in ((-1,-1),(1,-1),(1,1),(-1,1)):
        ax,ay=cx+dx*62*sc,cy+dy*34*sc; d.line([cx,cy,ax,ay],fill=rim,width=int(4*sc))
        sp=(ph*6)%(2*math.pi); rr=24*sc
        d.ellipse([ax-rr,ay-rr,ax+rr,ay+rr],outline=col+(70,),width=2)
        d.line([ax-rr*math.cos(sp),ay-rr*math.sin(sp),ax+rr*math.cos(sp),ay+rr*math.sin(sp)],fill=col+(150,),width=2)

def sc_dron(d,ph):  # katil/kamikaze dron hedefe dalıyor
    ground(d); cx=int(W*0.30+W*0.30*((ph/(2*math.pi))%1.0)); cy=int(H*0.26+120*((ph/(2*math.pi))%1.0))
    _quad(d,cx,cy,1.3,ph,ORANGE)
    tx,ty=int(W*0.74),GY-30  # hedef (tank/araç kutusu)
    d.rectangle([tx-70,ty-40,tx+70,ty],fill=(14,19,17,255),outline=GREEN+(160,)); d.rectangle([tx-30,ty-64,tx+30,ty-40],fill=(14,19,17,255),outline=GREEN+(160,))
    d.line([cx,cy,tx,ty-30],fill=ORANGE+(90,),width=2)

def sc_avcidron(d,ph):  # avcı dron kamikaze dronu kovalıyor
    ground(d); t=(ph/(2*math.pi))%1.0
    px,py=int(W*0.70-W*0.4*t),int(H*0.24+80*math.sin(ph*2))  # kaçan (turuncu)
    cxx,cyy=px-220,py+60  # kovalayan (yeşil)
    _quad(d,px,py,1.0,ph,ORANGE); _quad(d,cxx,cyy,1.1,ph+1,GREEN)
    d.line([cxx,cyy,px,py],fill=GREEN+(120,),width=2)
    for k in range(3):
        fr=(t+k/3)%1.0; xx=cxx+(px-cxx)*fr; yy=cyy+(py-cyy)*fr
        d.ellipse([xx-4,yy-4,xx+4,yy+4],fill=GREEN+(int(200*(1-fr)),))

def sc_jet(d,ph):  # insansız/5. nesil savaş uçağı (delta kanat siluet)
    cx=int(W*0.30+W*0.34*((ph/(2*math.pi))%1.0)); cy=CY+int(20*math.sin(ph)); rim=GREEN+(200,)
    pts=[(cx-170,cy),(cx+40,cy-16),(cx+210,cy),(cx+40,cy+16)]  # gövde
    d.polygon(pts,fill=(14,19,17,255),outline=rim)
    d.polygon([(cx-30,cy),(cx-120,cy-70),(cx-70,cy-6)],fill=(12,16,15,255),outline=rim)  # kanat üst
    d.polygon([(cx-30,cy),(cx-120,cy+70),(cx-70,cy+6)],fill=(12,16,15,255),outline=rim)  # kanat alt
    d.polygon([(cx+150,cy),(cx+210,cy),(cx+160,cy-8)],fill=ORANGE+(int(140+100*abs(math.sin(ph*4))),))  # art yakıcı
    for k in range(3):
        fr=((ph/(2*math.pi))+k/3)%1.0; d.ellipse([cx+210+fr*160-6,cy-6,cx+210+fr*160+6,cy+6],fill=ORANGE+(int(160*(1-fr)),))

def sc_fabrika(d,ph):  # üretim hattı: sıra sıra platformlar + ışık
    ground(d)
    for i in range(4):
        x=int(W*0.14)+i*int(W*0.19); d.rectangle([x,GY-40,x+180,GY],fill=(16,22,20,255),outline=GREEN+(120,))
        d.polygon([(x+40,GY-40),(x+90,GY-150),(x+140,GY-40)],fill=(12,16,15,255),outline=GREEN+(160,))  # ürün (uçak burnu/gövde)
        gl=int(120+120*abs(math.sin(ph*2+i))); d.ellipse([x+70,GY-170,x+110,GY-150],fill=ORANGE+(gl,))
    for bx in range(80,W,70): d.rectangle([bx,175,bx+40,185],fill=GREEN+(40,))  # tavan kiriş

def sc_kure(d,ph):  # dünya + yayılan saldırı yayları
    cx,cy,r=int(W*0.34),CY,170; rim=GREEN+(180,)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=rim,width=3)
    for a in range(-60,61,30): d.arc([cx-r,cy-r+a,cx+r,cy+r+a],0,180,fill=GREEN+(60,),width=1)
    for k in range(6):
        ang=ph+k*1.05; tx=cx+int(360*math.cos(ang)); ty=cy+int(150*math.sin(ang))
        col=ORANGE if k%2 else GREEN; d.line([cx,cy,tx,ty],fill=col+(90,),width=2); d.ellipse([tx-6,ty-6,tx+6,ty+6],fill=col+(200,))
    rings(d,cx,cy,ph,420,ORANGE,3,2)

def sc_usb(d,ph):  # USB bellek + bulaşan kırmızı/turuncu kod
    cx,cy=int(W*0.30),CY; rim=GREEN+(200,)
    d.rectangle([cx-120,cy-40,cx+60,cy+40],fill=(16,22,20,255),outline=rim,width=3)
    d.rectangle([cx+60,cy-22,cx+150,cy+22],fill=(30,36,33,255),outline=rim,width=3)
    tx=int(W*0.64); d.rectangle([tx-10,cy-150,tx+230,cy+150],fill=(12,16,15,255),outline=GREEN+(90,))  # hedef sistem
    for i in range(10):
        yy=cy-130+i*28; off=int((ph/(2*math.pi))*40); ln=(30+i*21+off)%210
        col=ORANGE if i%2 else GREEN; d.line([tx,yy,tx+ln,yy],fill=col+(150,),width=3)
    d.line([cx+150,cy,tx,cy],fill=ORANGE+(120,),width=2)

def sc_fidye(d,ph):  # fidye yazılımı: ekranlar kırmızı kilit
    for i in range(3):
        x=int(W*0.14)+i*int(W*0.26); y=CY
        d.rectangle([x,y-110,x+230,y+70],fill=(26,12,10,255),outline=ORANGE+(180,),width=3)
        d.polygon([(x+95,y+70),(x+135,y+70),(x+150,y+110),(x+80,y+110)],fill=(20,26,24,255),outline=GREEN+(80,))
        pl=int(150+90*abs(math.sin(ph*1.6+i)))
        lx,ly=x+115,y-20; d.rectangle([lx-26,ly,lx+26,ly+44],fill=ORANGE+(pl,)); d.arc([lx-18,ly-26,lx+18,ly+14],180,360,fill=ORANGE+(pl,),width=6)

def sc_kripto(d,ph):  # kripto para yağmuru + cüzdan izi
    for i in range(10):
        x=int((i*193+((ph/(2*math.pi))*0)) % W);
    coins=[(int((i*197)%W),int(175+((i*131+(ph/(2*math.pi))*260))% (GY-175))) for i in range(14)]
    for (x,y) in coins:
        cw=int(10+16*abs(math.cos(ph*2+x))); d.ellipse([x-cw,y-24,x+cw,y+24],fill=(30,20,10,255),outline=ORANGE+(220,),width=3)
        if cw>10: d.text((x-9,y-16),'B',font=F(28),fill=ORANGE+(230,))

def sc_telefon(d,ph):  # ele geçirilen sosyal medya: doğrulama rozetli hesaplar kırmızıya
    for r in range(2):
        for c in range(4):
            x=int(W*0.16)+c*int(W*0.18); y=int(H*0.26)+r*int(H*0.16)
            on=((ph/(2*math.pi))*8)% (8)
            red=(int((r*4+c)) <= on)
            col=ORANGE if red else GREEN
            d.rounded_rectangle([x,y,x+180,y+90],10,fill=(16,22,20,255),outline=col+(170,))
            d.ellipse([x+16,y+24,x+56,y+64],outline=col+(200,),width=3)  # avatar
            d.ellipse([x+46,y+16,x+70,y+40],fill=col+(220,))  # doğrulama rozeti
            d.line([x+54,y+28,x+60,y+34],fill=(12,16,15,255),width=3); d.line([x+60,y+34,x+66,y+22],fill=(12,16,15,255),width=3)
            d.line([x+76,y+34,x+164,y+34],fill=col+(120,),width=4); d.line([x+76,y+58,x+140,y+58],fill=col+(80,),width=4)

def sc_sebeke(d,ph):  # elektrik şebekesi: direkler + sönen ışıklar (blackout)
    ground(d)
    for i in range(5):
        x=int(W*0.12)+i*int(W*0.17); d.line([x,GY,x,GY-220],fill=GREEN+(140,),width=4)
        d.line([x-50,GY-180,x+50,GY-180],fill=GREEN+(140,),width=4); d.line([x-50,GY-210,x+50,GY-210],fill=GREEN+(140,),width=4)
    for i in range(1,5): d.line([int(W*0.12)+(i-1)*int(W*0.17),GY-195,int(W*0.12)+i*int(W*0.17),GY-195],fill=GREEN+(90,),width=2)
    off=int(((ph/(2*math.pi))*6))
    for i in range(6):
        x=int(W*0.14)+i*int(W*0.13); lit=(i>off); col=(0,255,156,200) if lit else (233,132,71,120)
        d.rectangle([x,GY-80,x+70,GY],fill=(14,19,17,255),outline=GREEN+(90,))
        for wy in (GY-62,GY-38):
            for wx in (x+14,x+42): d.rectangle([wx,wy,wx+16,wy+18],fill=col)

SC={'arac':sc_arac,'operasyon':sc_operasyon,'haritalama':sc_haritalama,'hedef':sc_hedef,'hacker':sc_hacker,
    'korunma':sc_korunma,'yorum':sc_yorum,'kapanis':sc_kapanis,'dron':sc_dron,'avcidron':sc_avcidron,
    'jet':sc_jet,'fabrika':sc_fabrika,'kure':sc_kure,'usb':sc_usb,'fidye':sc_fidye,'kripto':sc_kripto,
    'telefon':sc_telefon,'sebeke':sc_sebeke}
fn=SC[name]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),
 '-i','-','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
for fi in range(NF):
    ph=2*math.pi*fi/NF; ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    field(d,ph); fn(d,ph)
    ff.stdin.write(Image.alpha_composite(base.convert('RGBA'),ov).convert('RGB').tobytes())
ff.stdin.close(); ff.wait(); print('sahne ok:',name)
