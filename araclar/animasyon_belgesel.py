"""Bir belgeseli baştan sona ANIMASYONLU üretir: Piper seslendirme + sahneli canlandırma
+ üst bant + animasyonlu altyazı. Dış araç/kredi kullanmaz.

Kullanım:
  python3 animasyon_belgesel.py <narr.json> <key> "<Baslik>" <piper.onnx> <scene_map virgullu> <out_dir>
scene_map: bölüm sayısı kadar sahne adı (animasyon_sahneler.py'deki), virgülle ayrık.
"""
import sys, os, re, json, wave, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from piper import PiperVoice
from piper.config import SynthesisConfig

narr_path,key,title,model,scene_csv,out = sys.argv[1:7]
os.makedirs(out,exist_ok=True)
SCENE_DIR=os.path.join(out,'_scenes'); os.makedirs(SCENE_DIR,exist_ok=True)
HERE=os.path.dirname(os.path.abspath(__file__))
W,H,FPS=1920,1080,25
secs=json.load(open(narr_path,encoding='utf-8'))[key]
smap=[s.strip() for s in scene_csv.split(',')]
assert len(smap)==len(secs), f'scene_map {len(smap)} != bölüm {len(secs)}'

voice=PiperVoice.load(model); SR=voice.config.sample_rate
cfg=SynthesisConfig(length_scale=1.05,noise_scale=0.6,noise_w_scale=0.7)
SUB={'—':', ','…':'...','“':'','”':'','"':'','w0rmer':'vörmır','Lapsus$':'Lapsus','GTA':'Ci Ti Ey',
 'F-35':'Ef otuz beş','F-16':'Ef on altı','F-22':'Ef yirmi iki','F-47':'Ef kırk yedi','Su-57':'Su elli yedi',
 'J-20':'Jı yirmi','TB2':'Te Be iki','TB3':'Te Be üç','AESA':'A E S A','S-400':'Es dört yüz','KVKK':'Ke Ve Ke Ke',
 'HBYS':'Ha Be Ye Se','MİT':'Mit','FBI':'Ef Bi Ay','NSA':'En Es Ey','USB':'U Es Be','DMARC':'Di Mark',
 'SPF':'Es Pe Ef','VPN':'Ve Pe En','DNS':'Di En Es','IP':'Ay Pi','MIT':'Em Ay Ti','CIA':'Si Ay Ey','TCG':'Te Ce Ge'}
def speakable(t):
    for a,b in SUB.items(): t=t.replace(a,b)
    return t
def tts(text):
    ch=[np.frombuffer(c.audio_int16_bytes,dtype=np.int16) for c in voice.synthesize(text,syn_config=cfg)]
    return np.concatenate(ch) if ch else np.zeros(0,np.int16)
def sil(sec): return np.zeros(int(SR*sec),np.int16)
def sentences(p): return [s.strip() for s in re.split(r'(?<=[.!?…])\s+',p) if s.strip()]

audio=[]; cues=[]; spans=[]; t=0.0
for s in secs:
    st=t; audio.append(sil(0.25)); t+=0.25
    for p in s['paras']:
        for snt in sentences(p):
            a=tts(speakable(snt)); dur=len(a)/SR
            cues.append((t,t+dur,snt)); audio.append(a); audio.append(sil(0.33)); t+=dur+0.33
        t+=0.3; audio.append(sil(0.3))
    spans.append((st,None,s['title']))
    t+=1.4; audio.append(sil(1.4))
END=t
spans=[(spans[i][0], (spans[i+1][0] if i+1<len(spans) else END), spans[i][2]) for i in range(len(spans))]
wav=os.path.join(out,'ses.wav')
with wave.open(wav,'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.concatenate(audio).tobytes())

# header.png
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
hdr=Image.new('RGBA',(W,150),(0,0,0,0)); d=ImageDraw.Draw(hdr)
d.rectangle([0,0,W,120],fill=(47,59,53,235))
for x in range(0,W,56): d.rectangle([x,120,x+34,134],fill=(47,59,53,235))
d.text((80,36),'MAZGAL',font=ImageFont.truetype(FB,46),fill=(233,132,71,255))
hdr.save(os.path.join(out,'header.png'))

def at(s):
    cs=int(round(s*100)); h,cs=divmod(cs,360000); m,cs=divmod(cs,6000); se,cs=divmod(cs,100)
    return f'{h:d}:{m:02d}:{se:02d}.{cs:02d}'
def wrap(txt,n=42):
    out=[];
    for sent in [txt]:
        words=sent.split(); cur=[]
        for w in words:
            if cur and len(' '.join(cur+[w]))>n: out.append(' '.join(cur)); cur=[]
            cur.append(w)
        if cur: out.append(' '.join(cur))
    return '\\N'.join(out[:3])
head=('[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n'
 '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
 'Style: Narr,DejaVu Sans,46,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3,2,2,260,260,96,0\n'
 'Style: Sek,DejaVu Sans Mono,30,&H004784E9,&H000000FF,&H00141917,&H00000000,-1,0,0,0,100,100,1,0,1,0,0,7,360,60,42,0\n\n'
 '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
L=[head]; fad='{\\fad(220,220)}'
for a,b,tt in spans: L.append(f'Dialogue: 0,{at(a)},{at(b)},Sek,,0,0,0,,{fad}{re.sub(r" ?\\(HOOK\\)","",tt).replace("—","-")}')
for a,b,tx in cues: L.append(f'Dialogue: 1,{at(a)},{at(b)},Narr,,0,0,0,,{fad}{wrap(tx)}')
open(os.path.join(out,'sub.ass'),'w',encoding='utf-8').write('\n'.join(L)+'\n')

# sahne loop'ları (önbellek)
for sc in set(smap):
    pth=os.path.join(SCENE_DIR,f'{sc}.mp4')
    if not os.path.exists(pth):
        subprocess.run(['python3',os.path.join(HERE,'animasyon_sahneler.py'),sc,pth,'8','25','1920','1080'],check=True)

# birleştir
args=['ffmpeg','-y','-loglevel','error']
for (a,b,_),sc in zip(spans,smap):
    args+=['-stream_loop','-1','-t',f'{b-a:.3f}','-i',os.path.join(SCENE_DIR,f'{sc}.mp4')]
args+=['-i',os.path.join(out,'header.png'),'-i',wav]
n=len(spans)
fc=''.join(f'[{i}:v]' for i in range(n))+f'concat=n={n}:v=1:a=0[bg];[bg][{n}:v]overlay=0:0[v1];[v1]subtitles='+os.path.join(out,'sub.ass')+'[v]'
mp4=os.path.join(out,'video.mp4')
args+=['-filter_complex',fc,'-map','[v]','-map',f'{n+1}:a','-t',f'{END:.2f}',
 '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-r','25',
 '-c:a','aac','-b:a','128k','-movflags','+faststart',mp4]
subprocess.run(args,check=True)
print(json.dumps({'mp4':mp4,'saniye':round(END,1),'bolum':n,'boyut_mb':round(os.path.getsize(mp4)/1e6,1)}))
