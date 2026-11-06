#!/usr/bin/env python3
"""Face-aligned stills (OpenCV Haar detector).

  python3 -I tools/faces.py sheet OUT.jpg  label=SRC ...        candidates with their detected faces, for choosing
  python3 -I tools/faces.py square OUT.jpg SRC [scale] [dx dy]  a square crop centred on the face (face = 1/scale of it)
  python3 -I tools/faces.py align OUT.jpg SRC [face_w] [cx cy] [dx dy]
                                                                1920x1080: the face's centre at (cx, cy), the face face_w
                                                                wide, the edges defocused (Dario's 'every AI tech bro')
SRC is an image path, or KEY@t for a frame of a source video (the keys of tools/prep2.py).
"""
import os, subprocess, sys, tempfile
# OpenCV 4.x (Haar cascades) from a private folder: the system OpenCV 5 build has no CascadeClassifier
CV4 = os.environ.get("CV4_DIR", "/tmp/claude-0/-home-user-aadvikmit678-bot-claude-test-2-0/e423ac76-ee7d-59ce-a6a4-204a237d7ec0/scratchpad/cv4")
if os.path.isdir(CV4):
    sys.path.insert(0, CV4)
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep2  # noqa: E402

CASC = [cv2.CascadeClassifier(cv2.data.haarcascades + n) for n in
        ("haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml", "haarcascade_profileface.xml")]


def split(src):
    if "#" in src:
        a, b = src.split("#", 1)
        return a, tuple(float(v) for v in b.split(","))
    return src, None


def load(src):
    if "@" in src and not os.path.exists(src):
        key, t = src.split("@")
        tmp = tempfile.mktemp(suffix=".png")
        prep2.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", t, "-i", f"{prep2.SRC}/{prep2.V[key]}",
                   "-frames:v", "1", tmp])
        im = Image.open(tmp).convert("RGB")
        os.remove(tmp)
        return im
    p = src if src.startswith("/") else f"{prep2.SRC}/{src}"
    return Image.open(p).convert("RGB")


def face(im, region=None):
    """The largest face: (x, y, w, h) in image pixels, or None. region = (fx, fy, fw, fh) fractions to search in."""
    if region:
        fx, fy, fw, fh = region
        ox, oy = int(im.width * fx), int(im.height * fy)
        sub = im.crop((ox, oy, ox + int(im.width * fw), oy + int(im.height * fh)))
        f = face(sub)
        return (f[0] + ox, f[1] + oy, f[2], f[3]) if f else None
    g = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    g = cv2.equalizeHist(g)
    best = None
    for c in CASC:
        for (x, y, w, h) in c.detectMultiScale(g, scaleFactor=1.08, minNeighbors=6, minSize=(60, 60)):
            if best is None or w * h > best[2] * best[3]:
                best = (int(x), int(y), int(w), int(h))
        if best:
            break
    return best


def square(im, f, scale=2.4, dx=0.0, dy=0.12, size=860):
    x, y, w, h = f
    cx, cy = x + w / 2 + dx * w, y + h / 2 + dy * h
    s = w * scale
    s = min(s, im.width, im.height)
    x0 = min(max(cx - s / 2, 0), im.width - s)
    y0 = min(max(cy - s / 2, 0), im.height - s)
    return im.crop((int(x0), int(y0), int(x0 + s), int(y0 + s))).resize((size, size), Image.LANCZOS)


def align(im, f, face_w=400, cx=960, cy=470, dx=0.0, dy=0.0, W=1920, H=1080, defocus=True):
    x, y, w, h = f
    k = face_w / w
    big = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    fx, fy = (x + w / 2 + dx * w) * k, (y + h / 2 + dy * h) * k
    out = Image.new("RGB", (W, H), (0, 0, 0))
    # a blurred, enlarged copy fills any edge the photo does not reach
    fill = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    out.paste(fill, (0, 0))
    out.paste(big, (round(cx - fx), round(cy - fy)))
    if defocus:  # sharp at the face, soft towards the edges
        soft = out.filter(ImageFilter.GaussianBlur(9))
        yy, xx = np.mgrid[0:H, 0:W]
        r = np.sqrt(((xx - cx) / (face_w * 1.25)) ** 2 + ((yy - cy) / (face_w * 1.35)) ** 2)
        m = np.clip((r - 0.75) / 0.9, 0, 1)
        out = Image.composite(soft, out, Image.fromarray((m * 255).astype(np.uint8)))
    return out



def dario(im, f, face_w=600, cx=960, cy=505, W=1920, H=1080, max_shift=(140, 100)):
    """Dario's 'every AI tech bro' frame: the face at (cx, cy) at close-up size, the photo always covering the frame
    (the face may sit up to max_shift off centre, or the photo scales up, rather than leave an edge); the edges
    zoom-blurred around a sharp circle on the face (measured on the reference: face centres within 15 px of
    (960, 505), face boxes 390-830 px, the centre about twice as sharp as the edges)."""
    x, y, w, h = f
    fcx, fcy = x + w / 2, y + h / 2
    best = None
    for dx in range(-max_shift[0], max_shift[0] + 1, 10):
        for dy in range(-max_shift[1], max_shift[1] + 1, 10):
            tx, ty = cx + dx, cy + dy
            k = max(face_w / w, tx / fcx, ty / fcy, (W - tx) / (im.width - fcx), (H - ty) / (im.height - fcy))
            cost = k * (1 + 0.0015 * (abs(dx) + abs(dy)))
            if best is None or cost < best[0]:
                best = (cost, k * 1.004, tx, ty)
    _, k, cx, cy = best
    big = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    if k > 1.4:
        big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    base = Image.new("RGB", (W, H))
    base.paste(big, (round(cx - fcx * k), round(cy - fcy * k)))
    acc = np.zeros((H, W, 3), np.float32)
    n = 10
    for i in range(n):  # zoom blur about the face
        sc = 1 + 0.011 * i
        z = base.resize((round(W * sc), round(H * sc)), Image.BILINEAR)
        l, t = round(cx * sc - cx), round(cy * sc - cy)
        acc += np.asarray(z.crop((l, t, l + W, t + H)), np.float32)
    zb = Image.fromarray((acc / n).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5))
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.sqrt((xx - cx) ** 2 + ((yy - (cy - 20)) / 1.08) ** 2)
    m = np.clip((rr - 250) / 360, 0, 1)
    m = m * m * (3 - 2 * m)
    out = np.asarray(base, np.float32) * (1 - m[..., None]) + np.asarray(zb, np.float32) * m[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    mode, out = sys.argv[1], sys.argv[2]
    if mode == "sheet":
        cells = []
        for a in sys.argv[3:]:
            label, src = a.split("=", 1)
            src, reg = split(src)
            im = load(src)
            f = face(im, reg)
            th = im.copy()
            d = ImageDraw.Draw(th)
            if f:
                x, y, w, h = f
                d.rectangle((x, y, x + w, y + h), outline=(255, 40, 40), width=max(3, im.width // 300))
            th.thumbnail((360, 300))
            cells.append((f"{label} {'' if f else 'NO FACE'} {f[2] if f else ''}", th))
        cols = 5
        rows = (len(cells) + cols - 1) // cols
        S = Image.new("RGB", (cols * 364, rows * 318), (16, 16, 16))
        d = ImageDraw.Draw(S)
        for k, (lab, th) in enumerate(cells):
            x0, y0 = (k % cols) * 364, (k // cols) * 318
            S.paste(th, (x0, y0 + 16))
            d.text((x0 + 3, y0 + 2), lab, fill=(255, 220, 0))
        S.save(out, quality=86)
    elif mode == "square":
        src, reg = split(sys.argv[3])
        im = load(src)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 2.4
        dx, dy = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (0.0, 0.12)
        f = face(im, reg)
        if not f:
            raise SystemExit(f"no face in {sys.argv[3]}")
        square(im, f, scale, dx, dy).save(out, quality=93)
    elif mode == "align":
        src, reg = split(sys.argv[3])
        im = load(src)
        fw = float(sys.argv[4]) if len(sys.argv) > 4 else 400
        cx, cy = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (960, 470)
        dx, dy = (float(sys.argv[7]), float(sys.argv[8])) if len(sys.argv) > 8 else (0.0, 0.0)
        f = face(im, reg)
        if not f:
            raise SystemExit(f"no face in {sys.argv[3]}")
        align(im, f, fw, cx, cy, dx, dy).save(out, quality=92)
    print(out)
