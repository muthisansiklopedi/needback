"""Mazgal taslak video üretici.

Senaryodan çıkarılan anlatım metnini (extract*.py çıktısı) Piper ile seslendirir,
her cümle için Mazgal temalı bir 1920x1080 kart çizer, altyazıyı karta yazar ve
ffmpeg ile MP4 üretir. Ayrıca gerçek ses sürelerine göre zamanlanmış .srt yazar.

Kullanım:
  python3 video_uret.py <narr.json> <anahtar: b1|b2> <başlık> <piper .onnx modeli> <çıktı klasörü>
"""
import json, os, re, sys, wave, subprocess, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from piper import PiperVoice
from piper.config import SynthesisConfig

narr_path, key, title, model, out = sys.argv[1:6]
os.makedirs(out, exist_ok=True)
fr = os.path.join(out, 'frames'); os.makedirs(fr, exist_ok=True)
sections = json.load(open(narr_path, encoding='utf-8'))[key]

W, H = 1920, 1080
BG = (20, 25, 23); STEEL = (47, 59, 53); FG = (228, 233, 228); MUTED = (154, 165, 158); ACC = (233, 132, 71)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FM = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def font(p, s): return ImageFont.truetype(p, s)

voice = PiperVoice.load(model)
SR = voice.config.sample_rate
cfg = SynthesisConfig(length_scale=1.05, noise_scale=0.6, noise_w_scale=0.7)

def tts(text):
    chunks = [np.frombuffer(c.audio_int16_bytes, dtype=np.int16) for c in voice.synthesize(text, syn_config=cfg)]
    return np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.int16)
def silence(sec): return np.zeros(int(SR * sec), dtype=np.int16)

def speakable(t):
    t = t.replace('—', ', ').replace('…', '...').replace('w0rmer', 'vörmır').replace('“', '').replace('”', '').replace('"', '')
    t = re.sub(r'\bMIT\b', 'Em Ay Ti', t); t = t.replace('NSA', 'En Se A').replace('FBI', 'Ef Bi Ay').replace('IP', 'İ Pe')
    return t

def wall(d, y):
    # Mazgal (bedenli duvar) motifi
    for x in range(0, W, 56): d.rectangle([x, y, x + 34, y + 14], fill=STEEL)

def base(section_title, idx, total):
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 120], fill=STEEL); wall(d, 120)
    d.text((80, 38), 'MAZGAL', font=font(FB, 40), fill=ACC)
    d.text((300, 46), section_title[:70], font=font(FM, 30), fill=FG)
    d.rectangle([0, H - 10, W, H], fill=STEEL)
    d.rectangle([0, H - 10, int(W * idx / max(total, 1)), H], fill=ACC)
    return im, d

def draw_center(d, text, size, color, y_center, maxw_chars, fnt=FR, spacing=18):
    f = font(fnt, size); lines = textwrap.wrap(text, maxw_chars)
    lh = size + spacing; y = y_center - len(lines) * lh / 2
    for ln in lines:
        w = d.textlength(ln, font=f); d.text(((W - w) / 2, y), ln, font=f, fill=color); y += lh

def sentences(p):
    return [s.strip() for s in re.split(r'(?<=[.!?…])\s+', p) if s.strip()]

items = []  # (kind, payload)
items.append(('title', None))
for s in sections:
    items.append(('section', s['title']))
    for p in s['paras']:
        for snt in sentences(p): items.append(('line', (s['title'], snt)))
        items.append(('pause', 0.7))
items.append(('outro', None))
nlines = sum(1 for k, _ in items if k == 'line')

chapters = []; audio = []; concat = []; cues = []; t = 0.0; n = 0; li = 0; cur_sec = ''
def add_frame(im, dur):
    global n
    path = os.path.join(fr, f'{n:04d}.png'); im.save(path); n += 1
    concat.append(f"file '{os.path.abspath(path)}'\nduration {dur:.3f}")

for kind, val in items:
    if kind == 'title':
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 330], fill=STEEL); wall(d, 330)
        draw_center(d, 'MAZGAL', 150, ACC, 175, 20, FB)
        draw_center(d, title, 84, FG, 640, 30, FB, 24)
        draw_center(d, 'Bu video eğitim ve bilgilendirme amaçlıdır.', 34, MUTED, 960, 80)
        dur = 4.0; add_frame(im, dur); audio.append(silence(dur)); t += dur
    elif kind == 'section':
        cur_sec = re.sub(r'\s*\(HOOK\)', '', val); chapters.append((round(t), cur_sec))
        parts = re.split(r'\s*[:—]\s*', cur_sec, maxsplit=1)
        im, d = base('', li, nlines)
        draw_center(d, parts[0].upper(), 56, ACC, 470, 40, FM)
        if len(parts) > 1: draw_center(d, parts[1], 80, FG, 600, 30, FB, 22)
        dur = 2.8; add_frame(im, dur); audio.append(silence(dur)); t += dur
    elif kind == 'pause':
        if concat:
            last = concat[-1].rsplit('duration ', 1); concat[-1] = f"{last[0]}duration {float(last[1]) + val:.3f}"
        audio.append(silence(val)); t += val
    elif kind == 'line':
        sec, snt = val; li += 1; sec = re.sub(r'\s*\(HOOK\)', '', sec)
        a = tts(speakable(snt)); dur = len(a) / SR + 0.35
        im, d = base(sec, li, nlines)
        draw_center(d, snt, 64 if len(snt) < 140 else 54, FG, 560, 42 if len(snt) < 140 else 52, FR, 22)
        add_frame(im, dur); audio.append(a); audio.append(silence(0.35))
        cues.append((t, t + len(a) / SR, snt)); t += dur
    elif kind == 'outro':
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W, 330], fill=STEEL); wall(d, 330)
        draw_center(d, 'MAZGAL', 150, ACC, 175, 20, FB)
        draw_center(d, 'Abone ol, bildirimleri aç.', 80, FG, 620, 30, FB)
        draw_center(d, 'Sence en çarpıcı kısım hangisiydi? Yorumlara yaz.', 40, MUTED, 760, 70)
        dur = 6.0; add_frame(im, dur); audio.append(silence(dur)); t += dur

# concat listesi: son kare tekrar edilmeli (ffmpeg concat kuralı)
lst = os.path.join(out, 'kareler.txt')
open(lst, 'w').write('\n'.join(concat) + '\n' + concat[-1].split('\n')[0] + '\n')
wav = os.path.join(out, 'ses.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.concatenate(audio).tobytes())

def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
with open(os.path.join(out, 'altyazi.srt'), 'w', encoding='utf-8') as f:
    for i, (a, b, c) in enumerate(cues, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n')

json.dump(chapters, open(os.path.join(out, 'bolumler.json'), 'w'), ensure_ascii=False)
mp4 = os.path.join(out, 'video.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', wav,
                '-vf', 'fps=25,format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'stillimage', '-crf', '26',
                '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-shortest', '-movflags', '+faststart', mp4], check=True)
print(json.dumps({'mp4': mp4, 'saniye': round(t, 1), 'kare': n, 'boyut_mb': round(os.path.getsize(mp4) / 1e6, 1)}))
