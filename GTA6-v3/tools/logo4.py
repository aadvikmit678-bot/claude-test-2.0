"""The GTA VI logo as a transparent PNG, cut from Trailer 1 at 84.0 s (the full logo on black, before "COMING 2025").

The background is the black region connected to the frame edges (flood fill), so the logo's own dark outlines stay in.
Writes gta6-edit/assets/img/gta6_logo.png.   usage: python -I tools/logo4.py
"""
import io, os, subprocess, sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl

src = os.path.normpath(os.path.join(edl.ROOT, edl.SRC["t1"]))
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", "84.0", "-i", src, "-frames:v", "1", "-f", "image2pipe",
                      "-vcodec", "png", "-"], capture_output=True, check=True).stdout
im = Image.open(io.BytesIO(raw)).convert("RGB")
a = np.asarray(im).astype(np.int16)
H, Wd = a.shape[:2]
dark = a.max(axis=2) < 34
bg = np.zeros((H, Wd), bool)
q = deque((y, x) for y in range(H) for x in (0, Wd - 1) if dark[y, x])
q.extend((y, x) for x in range(Wd) for y in (0, H - 1) if dark[y, x])
for y, x in q:
    bg[y, x] = True
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < Wd and dark[ny, nx] and not bg[ny, nx]:
            bg[ny, nx] = True
            q.append((ny, nx))
alpha = Image.fromarray(((~bg) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
ys, xs = np.where(~bg)
box = (max(0, xs.min() - 4), max(0, ys.min() - 4), min(Wd, xs.max() + 5), min(H, ys.max() + 5))
out = im.convert("RGBA")
out.putalpha(alpha)
out = out.crop(box)
dst = os.path.join(edl.PROJ, "assets", "img")
os.makedirs(dst, exist_ok=True)
out.save(os.path.join(dst, "gta6_logo.png"))
print("logo", out.size, "from", box)
