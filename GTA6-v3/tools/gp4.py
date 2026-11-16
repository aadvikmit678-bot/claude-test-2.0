"""'And while every other game asks you to be' -- reference 3's curved wall of clips ("The most dangerous thing you
can do to a founder"), from its first zoom on.

A wall of GTA clip tiles with thin dark seams, seen through a strong barrel (fisheye) curve with a vignette, RGB
fringes and soft edges. It opens zoomed on one tile (the reference after its first zoom), then three pans 10 frames apart,
each as measured on the reference frame by frame: most of the way in one smeared frame, then easing out over ~7
frames as the blur fades (CAMERA below).
Writes gta6-edit/assets/clips/gp.mp4.   usage: python -I tools/gp4.py
"""
import os, subprocess, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl4 as E

FPS = 30                     # the design's frame units (the reference's); the clip is drawn at OUT fps
OUT = int(os.environ.get("GP_FPS", "60"))
UP = OUT // FPS              # output frames per design frame
OW, OH = 1920, 1080
VW = 2.25                    # wall units across the output width at the centre (the centre tile ~44% of the width)
K = 0.32                     # barrel strength
TW, TH, SEAM = 1.0, 0.78, 0.022
PX = OW / VW                 # canvas pixels per wall unit
TPW, TPH = 854, 666                # even sizes (yuv420p decodes; odd widths shear the raw frames)
P, Q = TW + SEAM, TH + SEAM  # tile pitch
GRADE = "eq=contrast=1.04:saturation=1.03"

t0, t1 = E.SPAN["gp"]
DUR = t1 - t0
N = int(round(DUR * OUT)) + 5 * UP
# reference 3, measured frame by frame (30 fps): the view starts zoomed on one tile; every 10 frames a pan of about
# 1.3 tiles -- right, then down-left, then up-right -- that covers ~47% of its way in the first frame (smeared), ~80%
# in the second, then eases out over ~6 more frames as the blur fades; still between pans. One tile flashes white for
# two frames just before the third pan.
PANS_F = [9, 19, 29]                                                   # pan starts, in frames (the reference's f45/55/65)
EASE = [0.0, 0.47, 0.80, 0.885, 0.93, 0.955, 0.975, 0.99, 1.0]        # per frame after a pan starts (measured)
VIEWS = [(0.0, 0.0), (1.27 * P, -0.05 * Q), (0.17 * P, 0.95 * Q), (2.05 * P, 0.97 * Q)]
# the user: a triangle -- the water, the two holding hands, then something new (not back to the water): the last
# pan runs right along the lower row to Jason with the rifle
FLASH = ((1, 2), 27, 2)                                                # tile, first frame, frames
PANS = [f / FPS for f in PANS_F]

# the clips on the wall: (src, in) -- faces and scenes from the trailers, Vice City and San Andreas
CLIPS = [("t2", 67.0), ("t1", 11.5), ("vcde", 44.4), ("t1", 33.2), ("launch", 66.6), ("t2", 98.6),
         ("t2", 125.2), ("t2", 126.9), ("launch", 25.9), ("launch", 71.5), ("launch", 59.3), ("t2", 92.6),
         ("t2", 102.6), ("vc10", 18.4), ("nostalgia", 15.6), ("t1", 22.2)]
# wall layout: tile (col, row) -> clip index; the path tiles get the strongest faces
LAYOUT = {(0, 0): 0, (1, 0): 1, (2, 0): 2, (3, 0): 3, (-1, 1): 4, (0, 1): 5, (1, 1): 6, (2, 1): 9, (-1, 0): 8,
          (4, 0): 7, (3, 1): 10, (-2, 1): 11, (0, -1): 12, (1, -1): 13, (2, -1): 14, (3, -1): 15}


def clip_index(i, j):
    return LAYOUT.get((i, j), (i * 7 + j * 3) % len(CLIPS))


class Decoder:
    def __init__(self, src, sin):
        path = os.path.normpath(os.path.join(E.ROOT, E.SRC[src]))
        crop = E.CROP.get(src)
        pre = f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}," if crop else ""
        vf = f"{pre}scale={TPW}:{TPH}:force_original_aspect_ratio=increase:flags=lanczos,crop={TPW}:{TPH},{GRADE},fps={OUT}"
        self.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{sin:.3f}", "-t", f"{N / FPS + 0.5:.3f}", "-i", path,
                                   "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = np.zeros((TPH, TPW, 3), np.uint8)

    def next(self):
        raw = self.p.stdout.read(TPW * TPH * 3)
        if len(raw) == TPW * TPH * 3:
            self.last = np.frombuffer(raw, np.uint8).reshape(TPH, TPW, 3)
        return self.last


DEC = [Decoder(*c) for c in CLIPS]

# fixed barrel maps: output pixel -> wall offset (in canvas pixels) from the camera centre; R and B slightly apart
ys, xs = np.mgrid[0:OH, 0:OW].astype(np.float32)
xn, yn = (xs - OW / 2) / (OW / 2), (ys - OH / 2) / (OW / 2)
R2 = xn * xn + yn * yn
F = 1 + K * R2
MAPS = {}
for ch, s in (("g", 1.0), ("r", 1.0 + 0.0042 * 1), ("b", 1.0 - 0.0042)):
    f = F * (1 + (s - 1) * R2)                              # the fringes grow toward the edges
    MAPS[ch] = (xn * (VW / 2) * f * PX, yn * (VW / 2) * f * PX)
HALF_X = int((VW / 2) * (1 + K * R2.max()) * 1.01 * PX) + 4
HALF_Y = int((VW / 2) * (OH / OW) * (1 + K * R2.max()) * 1.01 * PX) + 4
R = np.sqrt(R2)
VIG = (1 - 0.6 * np.clip((R - 0.5) / 0.75, 0, 1) ** 1.6)[..., None].astype(np.float32)
SOFT = np.clip((R - 0.62) / 0.5, 0, 1)[..., None].astype(np.float32)        # the edges go soft


def ease(u):
    if u <= 0:
        return 0.0
    if u >= len(EASE) - 1:
        return 1.0
    i = int(u)
    return EASE[i] + (EASE[i + 1] - EASE[i]) * (u - i)


def camera(f):
    """the view centre at (fractional) frame f"""
    x, y = VIEWS[0]
    for n, pf in enumerate(PANS_F):
        if f >= pf:
            e = ease(f - pf)
            a, b = VIEWS[n], VIEWS[n + 1]
            x, y = a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e
    return x, y


def render(cx, cy, tiles, flash_on):
    ox, oy = int(np.floor(cx * PX)) - HALF_X, int(np.floor(cy * PX)) - HALF_Y
    cw, chh = 2 * HALF_X + 2, 2 * HALF_Y + 2
    canvas = np.full((chh, cw, 3), 9, np.uint8)
    i0, i1 = int(np.floor((ox / PX) / P)) - 1, int(np.ceil(((ox + cw) / PX) / P)) + 1
    j0, j1 = int(np.floor((oy / PX) / Q)) - 1, int(np.ceil(((oy + chh) / PX) / Q)) + 1
    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            x0 = int(round((i * P - TW / 2) * PX)) - ox
            y0 = int(round((j * Q - TH / 2) * PX)) - oy
            xa, ya, xb, yb = max(0, x0), max(0, y0), min(cw, x0 + TPW), min(chh, y0 + TPH)
            if xa >= xb or ya >= yb:
                continue
            img = tiles[clip_index(i, j)]
            if flash_on and (i, j) == FLASH[0]:
                img = np.full_like(img, 250)
            canvas[ya:yb, xa:xb] = img[ya - y0:yb - y0, xa - x0:xb - x0]
    fx, fy = cx * PX - ox, cy * PX - oy
    out = np.empty((OH, OW, 3), np.float32)
    for c, ch in enumerate("rgb"):
        mx, my = MAPS[ch]
        out[..., c] = cv2.remap(canvas[..., c], mx + fx, my + fy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=9)
    return out


enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}",
                        "-r", str(OUT), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "15",
                        "-keyint_min", "15", "-sc_threshold", "0", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        os.path.join(E.PROJ, "assets", "clips", "gp.mp4")], stdin=subprocess.PIPE)
for m in range(N):
    n = m / UP                   # the time in design (30 fps) frames: every other 60 fps frame is a 30 fps frame exactly
    tiles = [d.next() for d in DEC]
    flash_on = FLASH[1] <= n < FLASH[1] + FLASH[2]
    # motion blur as the reference's: each frame integrates the move over the last 1/60 s (half a design frame), so
    # the even frames are the 30 fps clip's frames and the odd ones fall between them
    x0, y0 = camera(n - 0.5)
    x1, y1 = camera(n)
    dist = np.hypot(x1 - x0, y1 - y0) * PX
    subs = int(min(28, max(1, dist / 9)))
    acc = np.zeros((OH, OW, 3), np.float32)
    for s_ in range(subs):
        f = n - 0.5 + 0.5 * (s_ + 1) / subs if subs > 1 else n
        acc += render(*camera(f), tiles, flash_on)
    img = acc / subs
    blur = cv2.GaussianBlur(img, (0, 0), 5.0)
    img = img * (1 - SOFT) + blur * SOFT
    img = img * VIG
    enc.stdin.write(np.clip(img + 0.5, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close()
assert enc.wait() == 0
for d in DEC:
    d.p.kill()
print(f"gp: {N} frames at {OUT} fps ({DUR:.3f} s + handle) | pans at design frames {PANS_F} | tile {TPW}x{TPH} px")
