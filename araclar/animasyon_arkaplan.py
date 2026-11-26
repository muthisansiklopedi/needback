"""Mazgal temalı, dikişsiz döngülü (seamless loop) hareketli arka plan üretir.
Ağ düğümleri + bağlantı çizgileri + dönen radar taraması + yayılan Wi-Fi halkaları.
Çıktı: ham RGB24 kareler ffmpeg'e borulanır -> bg_loop.mp4

Kullanım: python3 animasyon_arkaplan.py <cikti.mp4> [saniye] [fps] [W] [H]
"""
import sys, math, subprocess, numpy as np
from PIL import Image, ImageDraw

out = sys.argv[1]
T   = float(sys.argv[2]) if len(sys.argv) > 2 else 12.0   # döngü süresi (sn)
FPS = int(sys.argv[3])   if len(sys.argv) > 3 else 25
W   = int(sys.argv[4])   if len(sys.argv) > 4 else 1920
H   = int(sys.argv[5])   if len(sys.argv) > 5 else 1080
N   = 46                                                  # düğüm sayısı
nframes = int(round(T * FPS))

# Mazgal paleti
GREEN = (0, 255, 156)
ORANGE = (233, 132, 71)
rng = np.random.default_rng(7)

# Düğümler: dikişsiz hareket için periyodik (sin/cos, periyot = T)
bx = rng.uniform(0.04, 0.96, N) * W
by = rng.uniform(0.06, 0.94, N) * H
ax = rng.uniform(8, 42, N); ay = rng.uniform(8, 42, N)
px = rng.uniform(0, 2*math.pi, N); py = rng.uniform(0, 2*math.pi, N)
targets = rng.choice(N, 6, replace=False)          # turuncu "hedef" düğümler
emitters = rng.choice(N, 2, replace=False)         # Wi-Fi halkası kaynakları
LINK = 230.0                                        # bağlantı mesafesi (px)
MAXR = math.hypot(W, H) * 0.55                      # halka maksimum yarıçapı

# Statik dikey gradyan arka plan
grad = np.zeros((H, W, 3), np.uint8)
for y in range(H):
    f = y / (H - 1)
    grad[y, :] = (int(20 - 10*f), int(25 - 11*f), int(23 - 7*f))
base_bg = Image.fromarray(grad, 'RGB')

ff = subprocess.Popen(
    ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
     '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', out],
    stdin=subprocess.PIPE)

for fi in range(nframes):
    t = fi / FPS
    ph = 2 * math.pi * t / T
    xs = bx + ax * np.sin(ph + px)
    ys = by + ay * np.cos(ph + py)
    img = base_bg.copy()
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    # Radar taraması: dönen soluk yelpaze + kenar çizgisi (merkez sol-alt)
    cx, cy = int(W*0.14), int(H*0.84)
    sweep = math.degrees(ph) % 360
    d.pieslice([cx-900, cy-900, cx+900, cy+900], sweep-26, sweep, fill=(0, 255, 156, 16))
    ex = cx + 900*math.cos(math.radians(sweep)); ey = cy + 900*math.sin(math.radians(sweep))
    d.line([cx, cy, ex, ey], fill=(0, 255, 156, 40), width=2)

    # Wi-Fi halkaları: kaynaklardan yayılan, periyodik (dikişsiz)
    for ei in emitters:
        ox, oy = xs[ei], ys[ei]
        for k in range(3):
            fr = ((t/T) + k/3.0) % 1.0
            r = fr * MAXR
            a = int(90 * (1 - fr) * fr * 4)        # doğ-sön
            if a > 4:
                d.ellipse([ox-r, oy-r, ox+r, oy+r], outline=(0, 255, 156, min(a, 70)), width=2)

    # Bağlantı çizgileri (yakın düğümler)
    for i in range(N):
        for j in range(i+1, N):
            dx = xs[i]-xs[j]; dy = ys[i]-ys[j]
            dd = dx*dx + dy*dy
            if dd < LINK*LINK:
                a = int(70 * (1 - math.sqrt(dd)/LINK))
                if a > 3:
                    d.line([xs[i], ys[i], xs[j], ys[j]], fill=(0, 255, 156, a), width=1)

    # Düğümler
    for i in range(N):
        if i in targets:
            pr = 4 + 2.2*(1 + math.sin(ph*2 + i))         # nabız
            d.ellipse([xs[i]-pr-6, ys[i]-pr-6, xs[i]+pr+6, ys[i]+pr+6], outline=(233,132,71,70), width=2)
            d.ellipse([xs[i]-pr, ys[i]-pr, xs[i]+pr, ys[i]+pr], fill=(233,132,71,235))
        else:
            d.ellipse([xs[i]-3, ys[i]-3, xs[i]+3, ys[i]+3], fill=(0,255,156,200))

    frame = Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')
    ff.stdin.write(frame.tobytes())

ff.stdin.close()
ff.wait()
print("bg ok:", out, nframes, "kare")
