#!/usr/bin/env python3
"""v6 media, made after tools/prep2.py has cut the registered clips and stills (modelled on tools/prep5.py).

1. Note 4, "a guy who got FIRED" (S04, film 15.065-16.200 s): yd6_01 .. yd6_10, square photos of young Dimon centred
   on his face (tools/faces.square, the call prep5.young() makes), youngest first; the last one is the black-and-white
   hero (the same crop as v5's yd5_3). The first nine put the midpoint of his eyes on one line, 0.355 of the square
   down, drifting from the centre to 0.56 across the run so that the flip reads as one face leading into the hero's
   eyes (0.575, 0.40); the face fills about 0.45 of the square at first and 0.6 by the ninth (the hero 0.69), so it grows
   with the card. The eye points were measured on the squares (OpenCV's eye cascade, checked by eye) and the offsets
   solved from them; MPB@700, MPB@720 and old-image-05 have his face near the top of the frame, so their squares are
   tighter than the ramp to reach the eye line. build6.sp_fired_flip shows the first nine for two frames each and
   lands the hero on "fired". Three come from the user's old photos
   (dimon-src/jamie-old-images); the others are documentary frames (KEY@seconds, the keys of tools/prep2.py). The
   user's other old photos show him grey-haired after 1998, as a half face, or too small in a group.

Like prep5.py, it skips files that already exist: delete a file (or change its id) to make it again. The stills are
not registered with ST(), so tools/media_v6.json does not list them.

Run:  cd jpm-dimon && CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I tools/prep6.py
      (faces.py needs OpenCV 4 from CV4_DIR, for its Haar face detector)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep2, faces  # noqa: E402

PRJ, CLIPS, IMG = prep2.PRJ, prep2.CLIPS, prep2.IMG
OLD = "jamie-old-images/jamie-old-images"   # the user's 12 old photos (dimon-src/jamie-old-images, from the Drive)

YOUNG6 = [  # id, source[#search region fx,fy,fw,fh], square side / face width, dx, dy (in face widths) -- youngest first
    ("yd6_01", f"{OLD}/jamie-old-image-03.jpg", 2.22, -0.028, 0.219),                    # at college, long hair (B&W)
    ("yd6_02", "MPB@700.0", 1.89, -0.067, 0.154),                                        # young banker, smiling over his shoulder (v5 yd5_2)
    ("yd6_03", f"{OLD}/jamie-old-image-01.jpg#0,0,0.55,0.6", 2.04, -0.033, 0.165),       # Commercial Credit, 1986, at the podium (B&W)
    ("yd6_04", f"{OLD}/jamie-old-image-05.jpg#0.45,0,0.55,0.65", 1.53, -0.022, 0.089),   # laughing, Weill beside him
    ("yd6_05", "MPB@871.0", 1.88, -0.054, 0.165),                                        # the Primerica/Travelers years (v5 yd5_1)
    ("yd6_06", "MPB@720.0#0.5,0,0.5,0.8", 1.66, -0.086, 0.150),                          # beside Weill (right half of the frame)
    ("yd6_07", "UNT@580.0#0.5,0.15,0.4,0.7", 1.79, -0.136, 0.138),                       # beside the man in glasses (Travelers)
    ("yd6_08", "UNT@619.0#0,0,0.5,0.8", 1.72, -0.082, 0.163),                            # beside Jessica Weill (left half)
    ("yd6_09", "MPB@930.0", 1.67, -0.092, 0.162),                                        # Citigroup, 1998, at the citi podium
    ("yd6_10", "UNT@543.0#0.2,0,0.6,1", 1.45, -0.12, 0.12),                              # the B&W hero (same crop as v5 yd5_3)
]


def young6():
    for yid, src, scale, dx, dy in YOUNG6:
        out = f"{IMG}/{yid}.jpg"
        if os.path.exists(out):
            continue
        s, reg = faces.split(src)
        im = faces.load(s)
        f = faces.face(im, reg)
        if not f:
            raise SystemExit(f"no face in {src}")
        faces.square(im, f, scale, dx, dy).save(out, quality=93)
        print("made", out, "face", f, flush=True)

# ==== v6 note 2: the cyber portrait (S02) ====================================================================
# The B-roll plate renderer is the research reference (spec_s02.md section 6, tested), unchanged; the centre is the
# user's own picture (cy_user), which replaced the reference's portrait, band and logo.
import json, subprocess, tempfile  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont  # noqa: E402

ROOT = "/home/user/claude-test-2.0"
SRC = f"{ROOT}/dimon-src"
FONTS = f"{ROOT}/jpm-dimon/assets/fonts"
W, H = 1920, 1080


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-1500:]}")
    return r



def _gblur(a, sigma):
    r = int(3 * sigma + 1)
    x = np.arange(-r, r + 1, dtype=np.float32)
    k = np.exp(-x * x / (2 * sigma * sigma))
    k /= k.sum()
    a = np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 1, a)
    return np.apply_along_axis(lambda m: np.convolve(m, k, mode="same"), 0, a)



VID = {"MONT": ("_direct/jpm_montage.mp4", (0, 43, 1280, 720)),                       # 16:9 band above the subtitles
       "BM": ("_drive/banking montage 1-2 sec clip can be used.mp4", (0, 90, 960, 540))}
LOOKS = {  # saturation, (r, g, b) gains, contrast, brightness
    "night": (0.45, (0.62, 0.74, 0.92), 1.25, 0.80),
    "cool": (0.55, (0.88, 0.96, 1.05), 1.15, 0.86),
    "warm": (0.70, (1.04, 0.95, 0.84), 1.12, 0.88),
    "white": (0.85, (1.0, 1.0, 1.0), 1.05, 1.0),
    "bw": (0.0, (1.0, 1.0, 1.0), 1.20, 0.85),
    "navy": (0.25, (0.34, 0.47, 0.74), 1.30, 1.0),
    "grey": (0.35, (0.95, 0.93, 0.90), 1.05, 0.78),
}
RED = (232, 40, 42)
_FONT_CACHE = {}


def _font(name, size):
    key = (name, size)
    if key not in _FONT_CACHE:
        path = os.path.join(tempfile.gettempdir(), f"cy_{name}.ttf")
        if not os.path.exists(path):
            from fontTools.ttLib import TTFont
            f = TTFont(f"{FONTS}/{name}.woff2")
            f.flavor = None
            f.save(path)
        _FONT_CACHE[key] = ImageFont.truetype(path, size)
    return _FONT_CACHE[key]


def _cover(im, cy=0.5):
    k = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = int(min(max(cy * im.height - H / 2, 0), im.height - H))
    return im.crop((x, y, x + W, y + H))


def _look(im, name):
    if not name:
        return im
    sat, gains, con, bri = LOOKS[name]
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Contrast(im).enhance(con)
    im = ImageEnhance.Brightness(im).enhance(bri)
    a = np.asarray(im, np.float32) * np.array(gains, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def _move(im, z, dx=0.0):
    """Scale about the frame centre by z (>= 1) and shift dx px; 1920x1080 out."""
    w, h = round(W * z), round(H * z)
    big = im.resize((w, h), Image.BICUBIC)
    l = min(max(round((w - W) / 2 - dx), 0), w - W)
    t = round((h - H) / 2)
    return big.crop((l, t, l + W, t + H))


def _video(spec, n, tmp):
    """KEY@t[#cx,cy,z] -> n frames at 30 fps from t, cropped to the key's 16:9 band (or a tighter window in it)."""
    key, rest = spec.split("@", 1)
    t, _, xyz = rest.partition("#")
    path, (bx, by, bw, bh) = VID[key]
    x, y, w, h = bx, by, bw, bh
    if xyz:
        cx, cy, z = (float(v) for v in xyz.split(","))
        w, h = int(bw / z) // 2 * 2, int(bh / z) // 2 * 2
        x = int(min(max(bx + cx * bw - w / 2, bx), bx + bw - w))
        y = int(min(max(by + cy * bh - h / 2, by), by + bh - h))
    d = tempfile.mkdtemp(dir=tmp)
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", t, "-i", f"{SRC}/{path}", "-vf",
         f"crop={w}:{h}:{x}:{y},scale={W}:{H}:flags=lanczos,fps=30,setsar=1", "-frames:v", str(n), "-q:v", "2",
         f"{d}/%03d.png"])
    fr = [Image.open(f"{d}/{i:03d}.png").convert("RGB") for i in range(1, n + 1) if os.path.exists(f"{d}/{i:03d}.png")]
    if not fr:
        raise SystemExit(f"no frames for {spec}")
    while len(fr) < n:
        fr.append(fr[-1])
    return fr


def _frames(spec, n, look, tmp):
    """img:PATH[@cy] / hud1:PATH / hud2:PATH (stills, held) / frame:KEY@t (one video frame, held) / KEY@t (video)."""
    kind, _, rest = spec.partition(":") if ":" in spec.split("@")[0] else ("vid", "", spec)
    if kind in ("img", "hud1", "hud2"):
        path, _, cy = rest.partition("@")
        base = _look(_cover(Image.open(f"{SRC}/{path}").convert("RGB"), float(cy) if cy else 0.5), look)
        if kind == "hud1":
            base = _hud1(base)
        elif kind == "hud2":
            base = _hud2(base)
        return [base] * n, kind
    if kind == "frame":
        return [_look(_video(rest, 1, tmp)[0], look)] * n, kind
    return [_look(f, look) for f in _video(rest, n, tmp)], kind


def _brackets(d, box, arm, wd):
    x0, y0, x1, y1 = box
    for cx, cy, sx, sy in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.rectangle((min(cx, cx + sx * arm), min(cy, cy + sy * wd), max(cx, cx + sx * arm), max(cy, cy + sy * wd)), fill=RED + (255,))
        d.rectangle((min(cx, cx + sx * wd), min(cy, cy + sy * arm), max(cx, cx + sx * wd), max(cy, cy + sy * arm)), fill=RED + (255,))


def _hud1(im):
    """Karp 0.83-0.92 ('ENEMY DETECTED' radar frame), redrawn for JPMorgan: red HUD kept clear of the centre portrait."""
    im = im.copy()
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 127, W, 129), fill=RED + (230,))                       # the line across the top (Karp y 85/720)
    d.rectangle((110, 380, 420, 780), outline=RED + (200,), width=2)         # box A, left
    _brackets(d, (110, 380, 420, 780), 34, 6)
    d.text((110, 336), "NYSE: JPM", font=_font("InterTight-700", 30), fill=RED + (255,))
    d.rectangle((1520, 300, 1790, 640), outline=RED + (200,), width=2)       # box B, right
    _brackets(d, (1520, 300, 1790, 640), 30, 5)
    d.text((1520, 258), "270 PARK AVE", font=_font("InterTight-700", 26), fill=RED + (255,))
    d.polygon(((134, 168), (160, 214), (108, 214)), outline=RED + (255,), width=4)   # warning triangle
    d.text((128, 176), "!", font=_font("InterTight-800", 30), fill=RED + (255,))
    d.rectangle((176, 168, 590, 216), fill=RED + (235,))                     # the label bar
    f = _font("InterTight-800", 32)
    x = 190
    for ch in "INFLUENCE DETECTED":
        d.text((x, 172), ch, font=f, fill=(255, 255, 255, 255))
        x += d.textlength(ch, font=f) + 3
    for (x, y) in ((300, 860), (1660, 720), (1250, 990)):
        d.polygon(((x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)), fill=RED + (255,))
    for yy in range(300, 781, 40):                                            # range scale, right edge
        d.rectangle((1806, yy, 1820, yy + 1), fill=RED + (220,))
    d.rectangle((1820, 300, 1821, 780), fill=RED + (220,))
    return im


def _hud2(im):
    im = im.copy()
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle((0, 919, W, 920), fill=RED + (220,))
    _brackets(d, (90, 560, 600, 860), 40, 5)
    d.text((92, 470), "WASHINGTON, D.C.", font=_font("InterTight-700", 22), fill=RED + (255,))
    d.text((90, 500), "FEDERAL RESERVE", font=_font("InterTight-800", 32), fill=RED + (255,))
    d.ellipse((1489, 409, 1511, 431), outline=RED + (255,), width=2)          # crosshair
    d.rectangle((1440, 419, 1560, 420), fill=RED + (255,))
    d.rectangle((1499, 360, 1500, 480), fill=RED + (255,))
    for (x, y) in ((1700, 300), (1400, 780)):
        d.polygon(((x, y - 9), (x + 9, y), (x, y + 9), (x - 9, y)), fill=RED + (255,))
    return im


def _list_layer(cy, k):
    """Karp 1.46-1.79: a list of sectors in faint white sans scrolling up over several backgrounds."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = _font("InterTight-600", 92)
    lines, step, k0 = cy["list"], 112, cy["list_at"][0]
    y0 = 900 - cy["list_speed"] * (k - k0)
    i = 0
    while y0 + i * step < H:
        y = y0 + i * step
        if y > -step:
            d.text((80, y), lines[i % len(lines)], font=f, fill=(255, 255, 255, 255))
        i += 1
    return im


def cy_broll(cy, out_mp4):
    """Renders the S02 background plate: main items (hard cuts, each with its own slow push or pan), the faint
    secondary layer, the scrolling list. 30 fps H.264, frames 0..cy['frames']-1 plus cy['pad'] held frames."""
    tmp = tempfile.mkdtemp()
    N = cy["frames"]
    main = [None] * N
    for k0, n, spec, look, z0, z1, dx in cy["main"]:
        seq, _ = _frames(spec, n, look, tmp)
        for j in range(n):
            p = j / max(1, n - 1)
            if k0 + j < N:
                main[k0 + j] = _move(seq[j], z0 + (z1 - z0) * p, dx * j)
    missing = [k for k in range(N) if main[k] is None]
    if missing:
        raise SystemExit(f"cyber main schedule leaves frames empty: {missing}")
    sec = {}
    for k0, n, spec, look, op, blend in cy["sec"]:
        seq, _ = _frames(spec, n, look, tmp)
        for j in range(n):
            sec[k0 + j] = (_move(seq[j], 1.04 + 0.004 * j), op, blend)
    lk0, ln = cy["list_at"]
    ff = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                           "-pix_fmt", "yuv420p", "-g", "10", "-movflags", "+faststart", out_mp4], stdin=subprocess.PIPE)
    for k in range(N + cy["pad"]):
        kk = min(k, N - 1)
        A = np.asarray(main[kk], np.float32)
        if kk in sec:
            layer, op, blend = sec[kk]
            B = np.asarray(layer, np.float32)
            if blend == "screen":
                A = A + (255 - (255 - A) * (255 - B) / 255 - A) * op
            else:
                A = A + (B - A) * op
        if lk0 <= kk < lk0 + ln:
            L = _list_layer(cy, kk)
            al = np.asarray(L.getchannel("A"), np.float32)[..., None] / 255 * cy["list_opacity"]
            A = A + (255 - A) * al
        ff.stdin.write(np.clip(A, 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit("ffmpeg failed writing " + out_mp4)
    import shutil   # the same plate under a second name for the ghost layer over his face (two <video>s with one
    shutil.copyfile(out_mp4, out_mp4.replace(".mp4", "_ovl.mp4"))   # src trip duplicate_media_discovery_risk)




CY_PIC = "_cyber/Glitchy JPMorgan Chase Cyber Portrait.png"   # the user's picture (main Drive folder, 10 Nov)
CY_BAND_BOX = (470, 345, 1460, 610)                            # the band, its streaks and the wordmark, at 1920x1080


def cy_user(img_dir):
    """The user's cyber portrait for S02: cy_pic.jpg (the picture at 1920x1080), cy_cut.png (Dimon cut out of it with
    the local matting model) and cy_band.png (the band and JPMorganChase wordmark, laid back over his eyes because the
    matte trims the band's ends; solid over the wordmark and eyes, its ends fraying into 3-6 px glitch streaks)."""
    pic, cut, band = f"{img_dir}/cy_pic.jpg", f"{img_dir}/cy_cut.png", f"{img_dir}/cy_band.png"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{SRC}/{CY_PIC}", "-vf", "scale=1920:1080:flags=lanczos",
         "-q:v", "2", pic])
    run(["npx", "--yes", "hyperframes@0.9.2", "remove-background", pic, "-o", cut, "--json"])
    x0, y0, x1, y1 = CY_BAND_BOX
    crop = np.asarray(Image.open(pic).convert("RGB").crop((x0, y0, x1, y1))).astype(np.float32)
    hh, ww = crop.shape[:2]
    xs, ys = np.arange(ww) + x0, np.arange(hh) + y0
    rng = np.random.default_rng(23)                              # deterministic frays
    v = np.clip((ys - 352) / 16, 0, 1) * np.clip((603 - ys) / 16, 0, 1)
    a = np.zeros((hh, ww), np.float32)
    y = 0
    while y < hh:
        h = int(rng.integers(3, 7))
        left_end = 590 - rng.uniform(15, 120) * (1.0 if rng.random() < 0.65 else 0.35)
        right_end = 1385 + rng.uniform(15, 75) * (1.0 if rng.random() < 0.65 else 0.35)
        a[y:y + h] = np.minimum(np.clip((xs - left_end) / 28, 0, 1), np.clip((right_end - xs) / 28, 0, 1))[None, :]
        y += h
    alpha = np.asarray(Image.fromarray((a * v[:, None] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)))
    Image.fromarray(np.dstack([crop.astype(np.uint8), alpha]), "RGBA").save(band, optimize=True)


if __name__ == "__main__":
    young6()
    print("done", flush=True)

    # v6 note 2: the user's cyber portrait and the B-roll plate (re-rendered whenever build6's CYBER changes)
    if not os.path.exists(f"{prep2.IMG}/cy_band.png"):
        cy_user(prep2.IMG)
    SPEC6 = json.load(open(f"{prep2.PRJ}/tools/media_v6.json"))
    stamp, want = f"{prep2.CLIPS}/cy_broll.json", json.dumps(SPEC6["cyber"], sort_keys=True)
    if not (os.path.exists(f"{prep2.CLIPS}/cy_broll_ovl.mp4") and os.path.exists(stamp) and open(stamp).read() == want):
        cy_broll(SPEC6["cyber"], f"{prep2.CLIPS}/cy_broll.mp4")
        open(stamp, "w").write(want)
