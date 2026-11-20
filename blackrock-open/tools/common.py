"""Shared helpers for the BlackRock opening's media prep (run with the scratch venv: numpy, opencv<5, pillow).

Paths: the project is blackrock-open/, the raw downloads sit in blackrock-src/ (git-ignored).
Every pre-rendered beat is written at 1920x1080, 60 fps, H.264 CRF 12, so the HyperFrames scenes only place it.
"""
import json
import math
import os
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.abspath(os.path.join(ROOT, "..", "blackrock-src"))
DL = f"{SRC}/dl"
CUT = f"{SRC}/work/cut"
CART = f"{SRC}/cartel"
WORK = f"{SRC}/work"
CLIPS = f"{ROOT}/assets/clips"
IMG = f"{ROOT}/assets/img"
AUD = f"{ROOT}/assets/audio"
for d in (CLIPS, IMG, AUD, WORK):
    os.makedirs(d, exist_ok=True)

W, H, FPS = 1920, 1080, 60
PANEL = f"{DL}/panel_fii7.mp4"

HAAR = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in
        ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml")]


def probe(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", src],
                         capture_output=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(n) / float(d)


def grab(src, t, n=1, fps=None, size=None, alpha=False, vf=None):
    """n decoded frames starting at t seconds (accurate seek), as uint8 arrays (RGB, or RGBA with alpha=True).
    fps resamples (duplicating frames) so n frames at that rate cover n/fps seconds."""
    w, h, _ = probe(src)
    args = ["ffmpeg", "-v", "error"]
    if alpha:
        args += ["-c:v", "libvpx-vp9"]
    args += ["-ss", f"{max(0.0, t):.4f}", "-i", src]
    filt = []
    if vf:
        filt.append(vf)
    if fps:
        filt.append(f"fps={fps}")
    if size:
        filt.append(f"scale={size[0]}:{size[1]}:flags=lanczos")
        w, h = size
    if filt:
        args += ["-vf", ",".join(filt)]
    c = 4 if alpha else 3
    args += ["-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgba" if alpha else "rgb24", "-"]
    raw = subprocess.run(args, capture_output=True, check=True).stdout
    k = len(raw) // (w * h * c)
    return [np.frombuffer(raw[i * w * h * c:(i + 1) * w * h * c], np.uint8).reshape(h, w, c) for i in range(k)]


_ST = {}


def stream_start(src):
    """The video stream's start_time (Instagram / Drive downloads often begin at 0.115-0.125 s)."""
    if src not in _ST:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=start_time",
                              "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
        try:
            _ST[src] = float(out)
        except ValueError:
            _ST[src] = 0.0
    return _ST[src]


def frame_at(src, f, src_fps=None, alpha=False):
    """Source frame number f (0-based decode order), exact: select by index (a timed -ss on these downloads, whose
    streams start at 0.115-0.125 s, lands a frame or three off)."""
    w, h, _ = probe(src)
    c = 4 if alpha else 3
    args = ["ffmpeg", "-v", "error"] + (["-c:v", "libvpx-vp9"] if alpha else []) + [
        "-i", src, "-vf", f"select=eq(n\\,{int(f)})", "-fps_mode", "passthrough", "-frames:v", "1",
        "-f", "rawvideo", "-pix_fmt", "rgba" if alpha else "rgb24", "-"]
    raw = subprocess.run(args, capture_output=True, check=True).stdout
    return np.frombuffer(raw[:w * h * c], np.uint8).reshape(h, w, c)


class Writer:
    def __init__(self, path, fps=FPS, w=W, h=H, crf=12):
        self.path = path
        self.n = 0
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                   "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                                   "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
                                   "-movflags", "+faststart", path], stdin=subprocess.PIPE)

    def write(self, fr, times=1):
        b = np.ascontiguousarray(np.clip(fr, 0, 255).astype(np.uint8)).tobytes()
        for _ in range(times):
            self.p.stdin.write(b)
            self.n += 1

    def close(self):
        self.p.stdin.close()
        self.p.wait()
        print(f"  wrote {os.path.relpath(self.path, ROOT)}: {self.n} frames = {self.n / FPS:.3f} s")


# ---------- geometry / compositing ----------

def cover(img, w=W, h=H, cx=0.5, cy=0.5, scale=1.0):
    """Scale an image to cover w x h (times scale) and crop around (cx, cy) fractions."""
    ih, iw = img.shape[:2]
    k = max(w / iw, h / ih) * scale
    nw, nh = max(w, round(iw * k)), max(h, round(ih * k))
    r = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_CUBIC if k > 1 else cv2.INTER_AREA)
    x0 = int(min(max(cx * nw - w / 2, 0), nw - w))
    y0 = int(min(max(cy * nh - h / 2, 0), nh - h))
    return r[y0:y0 + h, x0:x0 + w].copy()


def affine(img, k, cx, cy, tx, ty, w=W, h=H, border=(255, 255, 255)):
    """Scale img by k about its point (cx, cy) and put that point at (tx, ty) on a w x h canvas."""
    M = np.float32([[k, 0, tx - k * cx], [0, k, ty - k * cy]])
    flags = cv2.INTER_CUBIC if k > 1 else cv2.INTER_AREA
    if img.shape[2] == 4:
        return cv2.warpAffine(img, M, (w, h), flags=flags, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return cv2.warpAffine(img, M, (w, h), flags=flags, borderMode=cv2.BORDER_CONSTANT, borderValue=border)


def over(base, rgba):
    """Alpha-composite an RGBA layer (same size) over an RGB base (float math, returns float32)."""
    a = rgba[..., 3:4].astype(np.float32) / 255.0
    return base.astype(np.float32) * (1 - a) + rgba[..., :3].astype(np.float32) * a


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def radial(cx, cy, r0, r1, w=W, h=H, sy=1.0):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt((xx - cx) ** 2 + ((yy - cy) / sy) ** 2)
    return smooth((r - r0) / max(1.0, r1 - r0))


_MASKS = {}


def center_focus(img, cx=W / 2, cy=H / 2, r0=360, r1=760, zoom=0.012, n=8, gblur=2.2, sy=0.9):
    """Sharp at (cx, cy), zoom-blurred and softened towards the edges (the Nvidia / Dario centre focus)."""
    h, w = img.shape[:2]
    key = (cx, cy, r0, r1, w, h, sy)
    if key not in _MASKS:
        _MASKS[key] = radial(cx, cy, r0, r1, w, h, sy)[..., None]
    m = _MASKS[key]
    src = img.astype(np.float32)
    acc = np.zeros_like(src)
    for i in range(n):
        k = 1 + zoom * i
        M = np.float32([[k, 0, cx - k * cx], [0, k, cy - k * cy]])
        acc += cv2.warpAffine(src, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    zb = cv2.GaussianBlur(acc / n, (0, 0), gblur)
    return src * (1 - m) + zb * m


def barrel(img, cx, cy, R, k):
    """Fisheye bulge inside radius R (centre magnified by 1/(1-k)), identity outside."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx - cx, yy - cy
    r = np.sqrt(dx * dx + dy * dy)
    q = np.clip(r / R, 0, 1)
    f = np.where(r < R, 1 - k + k * q * q, 1.0).astype(np.float32)
    return cv2.remap(img, cx + dx * f, cy + dy * f, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def vignette(img, strength=0.35, r0=0.55, r1=1.25):
    h, w = img.shape[:2]
    m = radial(w / 2, h / 2, r0 * w / 2, r1 * w / 2, w, h, sy=h / w * 1.6)[..., None]
    return img.astype(np.float32) * (1 - strength * m)


def grade(img, sat=1.0, contrast=1.0, bright=0.0):
    f = img.astype(np.float32)
    if sat != 1.0:
        g = f.mean(axis=2, keepdims=True)
        f = g + (f - g) * sat
    if contrast != 1.0 or bright:
        f = (f - 128) * contrast + 128 + bright
    return f


def grain(h=H, w=W, seed=0, amt=7.0):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, amt, (h // 2, w // 2)).astype(np.float32)
    return cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR)[..., None]


def face(img_rgb, min_size=60):
    """Largest frontal face (x, y, w, h) or None."""
    g = cv2.cvtColor(np.ascontiguousarray(img_rgb[..., :3]), cv2.COLOR_RGB2GRAY)
    g = cv2.equalizeHist(g)
    best = None
    for c in HAAR:
        for (x, y, w, h) in c.detectMultiScale(g, scaleFactor=1.06, minNeighbors=6, minSize=(min_size, min_size)):
            if best is None or w * h > best[2] * best[3]:
                best = (int(x), int(y), int(w), int(h))
        if best:
            break
    return best


def font(path, size):
    return ImageFont.truetype(path, size)


def save_png(arr, path):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)


def save_jpg(arr, path, q=93):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)[..., :3]).save(path, quality=q)
