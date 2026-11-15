"""'And while every other game asks you to be' -- reference 3's curved wall of clips ("The most dangerous thing you
can do to a founder"), from its first zoom on.

A wall of GTA clip tiles with thin dark seams, seen through a strong barrel (fisheye) curve with a vignette, RGB
fringes and soft edges. It opens already zoomed on one tile, drifting slowly, then makes three whip-pans -- right, down
and left, up and right -- each a one-to-two-frame move smeared by motion blur, landing between two tiles and holding
(~0.3-0.5 s, as the reference at 30 fps: zoom at frame 36, pans at 46, 56, 66). One tile flashes white during the
third hold (the reference's frame 64). The pans land on the words "other", "asks" and "you".
Writes gta6-edit/assets/clips/gp.mp4.   usage: python -I tools/gp4.py
"""
import os, subprocess, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl4 as E

FPS = 30
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
N = int(round(DUR * FPS)) + 5
PANS = [E.cut(173) - t0, E.cut(175) - t0, E.cut(176) - t0]           # "other", "asks", "you"
VIEWS = [(0.0, 0.0), (1.5 * P, -0.04), (-0.5 * P, 1.0 * Q), (2.5 * P, -0.08)]
DRIFT = (0.055, -0.018)      # wall units per second during the holds
FLASH = ((0, 1), PANS[2] + 0.12, 2)                                    # tile, time, frames

# the clips on the wall: (src, in) -- faces and scenes from the trailers, Vice City and San Andreas
CLIPS = [("t2", 67.0), ("t1", 11.5), ("vcde", 44.4), ("t1", 33.2), ("launch", 66.6), ("t2", 98.6),
         ("t2", 125.2), ("t2", 126.9), ("launch", 25.9), ("launch", 71.5), ("launch", 59.3), ("t2", 92.6),
         ("t2", 102.6), ("vc10", 18.4), ("nostalgia", 15.6), ("t1", 22.2)]
# wall layout: tile (col, row) -> clip index; the path tiles get the strongest faces
LAYOUT = {(0, 0): 0, (1, 0): 1, (2, 0): 2, (3, 0): 3, (-1, 1): 4, (0, 1): 5, (1, 1): 6, (2, 1): 7, (-1, 0): 8,
          (4, 0): 9, (3, 1): 10, (-2, 1): 11, (0, -1): 12, (1, -1): 13, (2, -1): 14, (3, -1): 15}


def clip_index(i, j):
    return LAYOUT.get((i, j), (i * 7 + j * 3) % len(CLIPS))


class Decoder:
    def __init__(self, src, sin):
        path = os.path.normpath(os.path.join(E.ROOT, E.SRC[src]))
        crop = E.CROP.get(src)
        pre = f"crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}," if crop else ""
        vf = f"{pre}scale={TPW}:{TPH}:force_original_aspect_ratio=increase:flags=lanczos,crop={TPW}:{TPH},{GRADE},fps={FPS}"
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


def camera(t):
    """camera centre at time t: holds drift; each pan moves to the next view in ~2 frames (smoothstep)"""
    k = sum(1 for p in PANS if t >= p + 1 / FPS)
    for n, p in enumerate(PANS):
        if p - 1 / FPS <= t < p + 1 / FPS:
            u = (t - (p - 1 / FPS)) * FPS / 2
            u = u * u * (3 - 2 * u)
            a = hold(n, p - 1 / FPS)
            b = hold(n + 1, p + 1 / FPS)
            return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
    return hold(k, t)


def hold(n, t):
    start = 0.0 if n == 0 else PANS[n - 1] + 1 / FPS
    d = t - start
    v = VIEWS[n]
    return v[0] + DRIFT[0] * d, v[1] + DRIFT[1] * d


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
                        "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "15",
                        "-keyint_min", "15", "-sc_threshold", "0", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        os.path.join(E.PROJ, "assets", "clips", "gp.mp4")], stdin=subprocess.PIPE)
for n in range(N):
    t = n / FPS
    tiles = [d.next() for d in DEC]
    flash_on = FLASH[1] <= t < FLASH[1] + FLASH[2] / FPS
    moving = any(p - 1 / FPS - 1 / FPS < t < p + 1 / FPS for p in PANS)
    subs = 10 if moving else 1
    acc = np.zeros((OH, OW, 3), np.float32)
    for s in range(subs):
        cx, cy = camera(t + (s + 0.5) / subs / FPS if subs > 1 else t)
        acc += render(cx, cy, tiles, flash_on)
    img = acc / subs
    blur = cv2.GaussianBlur(img, (0, 0), 5.0)
    img = img * (1 - SOFT) + blur * SOFT
    img = img * VIG
    enc.stdin.write(np.clip(img + 0.5, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close()
assert enc.wait() == 0
for d in DEC:
    d.p.kill()
print(f"gp: {N} frames ({DUR:.3f} s + handle) | pans at {[round(p, 3) for p in PANS]} s | tile {TPW}x{TPH} px")
