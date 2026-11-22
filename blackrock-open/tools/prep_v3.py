#!/usr/bin/env python3
"""v3 beats (the user's notes of Nov 21), each pre-rendered at 60 fps, 1920x1080:

  opening   the plain shots for "of financial talent ... put together here": four panelists talking (muted), cut with
            white flashes in build.py
  tiles     the 3x3 tile flash from "These" through "people" (2.3 s), every tile framed on its face by hand
  articles  "a $60 trillion dollar": the user's ten article screenshots as the Opal reel's article flipbook, every one
            scaled and placed so its highlighted "$60 trillion" sits on the same spot at the centre, a subtle push-in
  touch     "you touch": the touch clip from its black pixel hands (no painting) to the touch burst
  puppet    the BlackRock explainer's opening puppet shot, until "That's Jamie Dimon"
  dimon     the reference edit's "if intelligence is automated": Dimon talking, a white silhouette flash, a white band
            sliding down behind him, "That's" / "Jamie Dimon" in red, "the guy running" in Instrument Serif with glow
  jpm       "JP Morgan Chase" as the Attention Compounds reel's "the man behind OpenAI": a curved-screen flipbook (2 frames
            a picture at 24 fps), negatives, a 1-frame logo, a 3x2 grid of live clips under a textured hero word
  solomon   the reference edit's "AI": Solomon talking, a giant gold name behind him, a red bar sliding in, the yellow
            vertical "a part-time DJ"
  ceo       "the CEO of Goldman Sachs" as the reel's OpenAI device, with the user's Goldman Sachs video
  orbit     the camera circling the table at its settled zoom (no zoom move), people lighting up at random
  amongst   "Amongst them is this guy": the reel's selection box on the white window-light backdrop cycling the other
            panelists (live), on black for "them", a light-leak flash, Fink's card held on the backdrop

Run: <venv>/bin/python -E -s tools/prep_v3.py [names...]
"""
import sys

from common import *  # noqa: F401,F403
import timing as TM
import prep_v2 as V2

V3 = f"{DL}/v3"
J2 = f"{ROOT}/../jpm-dimon/assets/clips2"
FONTS = f"{ROOT}/assets/fonts"
INTER_B = f"{FONTS}/InterDisplay-Bold.otf"
INTER_XB = f"{FONTS}/InterDisplay-ExtraBold.otf"
INTER_M = f"{FONTS}/InterDisplay-Medium.otf"
HEROS = f"{FONTS}/TeXGyreHeros-Regular.otf"
RED = np.array([206, 30, 38], np.float32)        # the reference's orange elements, made red (the user)
GOLD_TOP = np.array([244, 214, 140], np.float32)
GOLD_BOT = np.array([205, 158, 72], np.float32)
YELLOW = np.array([240, 216, 70], np.float32)
WHITE = np.array([247, 246, 243], np.float32)


def nf(a, b):
    return round(b * FPS) - round(a * FPS)


def beat_frames(beat):
    a, b = TM.B[beat]
    return nf(a, b)


def frames(src, t0, n, fps=None, alpha=False, size=None):
    return grab(src, t0, n, fps=fps, alpha=alpha, size=size)


def fit(img, w=W, h=H):
    return cover(img.astype(np.float32), w, h)


def iso(path, font_path, size):
    return ImageFont.truetype(font_path, size)


# ------------------------------------------------------------------ text helpers
def text_mask(text, font_path, size, pad=20, track=0.0):
    """White-on-black alpha of a text line (float 0..1) and its baseline offset."""
    f = ImageFont.truetype(font_path, size)
    l, t, r, b = f.getbbox(text)
    asc, desc = f.getmetrics()
    w = int(r - l + 2 * pad + abs(track) * size * len(text))
    h = int(asc + desc + 2 * pad)
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    if track:
        x = pad - l
        for ch in text:
            d.text((x, pad), ch, font=f, fill=255)
            x += f.getlength(ch) + track * size
    else:
        d.text((pad - l, pad), text, font=f, fill=255)
    return np.asarray(im).astype(np.float32) / 255, pad + asc, pad - l


def paste_alpha(canvas_a, m, x, y):
    """Max-composite a mask m into canvas_a at top-left (x, y), clipped."""
    h, w = m.shape
    x0, y0 = int(round(x)), int(round(y))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(canvas_a.shape[1], x0 + w), min(canvas_a.shape[0], y0 + h)
    if xb <= xa or yb <= ya:
        return
    canvas_a[ya:yb, xa:xb] = np.maximum(canvas_a[ya:yb, xa:xb], m[ya - y0:yb - y0, xa - x0:xb - x0])


def over_color(img, a, color):
    a = np.clip(a, 0, 1)[..., None]
    return img * (1 - a) + np.asarray(color, np.float32) * a


def glow_text(img, a, color, glow=0.55, sigma=(6, 18)):
    """Text with a soft glow of its own colour (the Dario / Instrument Serif glow)."""
    g = sum(cv2.GaussianBlur(a, (0, 0), s) for s in sigma) / len(sigma)
    img = img + (np.asarray(color, np.float32) - img) * np.clip(g * glow, 0, 1)[..., None] * 0.6
    return over_color(img, a, color)


def speckle(shape, seed, holes=0.22):
    """The reel's worn-print texture inside hero letters: small irregular holes."""
    rng = np.random.default_rng(seed)
    n = rng.random((shape[0] // 2 + 1, shape[1] // 2 + 1)).astype(np.float32)
    n = cv2.resize(n, (shape[1], shape[0]), interpolation=cv2.INTER_LINEAR)
    n = cv2.GaussianBlur(n, (0, 0), 0.8)
    return np.clip((n - holes) / 0.08, 0, 1)


# ------------------------------------------------------------------ looks
_CURVE = {}


def curved(img, k=0.13, seed=0):
    """The reel's curved old-screen photo: barrel bulge, rounded dark corners, heavy vignette, warm punchy grade."""
    f = img.astype(np.float32)
    f = barrel(f, W / 2, H / 2, math.hypot(W / 2, H / 2), k)
    if "m" not in _CURVE:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        u, v = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
        sq = (np.abs(u) ** 5 + np.abs(v) ** 5) ** (1 / 5)               # a rounded rectangle (superellipse)
        corner = 1 - smooth((sq - 0.90) / 0.12)
        vig = 1 - 0.62 * smooth((np.sqrt(u * u * 0.8 + v * v) - 0.45) / 0.85)
        _CURVE["m"] = (corner * vig)[..., None]
    g = f.mean(axis=2, keepdims=True)
    f = g + (f - g) * 1.12
    f = (f - 128) * 1.1 + 128
    f = f * np.array([1.04, 1.0, 0.94], np.float32)
    return np.clip(f, 0, 255) * _CURVE["m"] + 6 * (1 - _CURVE["m"])


def negative(img):
    return 255 - np.clip(img, 0, 255)


def whip(img, dx=90):
    """A whip smear: horizontal motion blur pushed towards white."""
    k = np.ones((1, dx), np.float32) / dx
    sm = cv2.filter2D(img.astype(np.float32), -1, k, borderType=cv2.BORDER_REFLECT)
    return sm * 0.55 + 255 * 0.45


# ------------------------------------------------------------------ 1. opening B-rolls + plain shots
SHOTS = [  # (name, source, start s, seconds, crop, frame-count start)
    # "of financial talent and skill as you've been able to put together here": panelists talking (muted)
    ("ob_fink", PANEL, 1185.30, 1.05, None, False),
    ("ob_schw", PANEL, 2183.74, 1.10, None, False),   # (ends before the panel's cut at 2184.86)
    ("ob_dalio", PANEL, 729.30, 0.92, None, False),
    ("ob_motsepe", PANEL, 1816.00, 1.12, None, False),
    # the BlackRock explainer's first shot: a puppet master's hand on a man's strings
    ("puppet", f"{V3}/br_explainer.mp4", 0.10, 0.64, None, False),
    # "DJ and the": him at the decks, him on the mic
    ("dj_a", f"{DL}/solomon_dj.mp4", 1.48, 0.34, "crop=1080:608:0:470", True),
    ("dj_b", f"{DL}/solomon_dj.mp4", 23.85, 0.34, "crop=1080:608:0:620", True),
]


def shots(names=None):
    for name, src, t0, dur, vf, fc in SHOTS:
        if names and name not in names:
            continue
        ss = t0 + (stream_start(src) if fc else 0.0)
        filt = ([vf] if vf else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", "fps=60"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", src, "-t", f"{dur:.3f}", "-vf",
                        ",".join(filt), "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", f"{CLIPS}/v3_{name}.mp4"], check=True)
        print("  ", name)
    # the user's plain red background for ON EARTH
    if not names or "red" in names:
        im = np.asarray(Image.open(f"{V3}/red_bg.jpg").convert("RGB")).astype(np.float32)
        save_jpg(cover(im), f"{IMG}/red_bg_user.jpg", q=96)
        print("   red_bg_user.jpg")


# ------------------------------------------------------------------ 2. tiles from "These"
TILES3 = [  # (name, panel start s, crop centre x, y, crop width) -- framed by hand on the face, 2.32 s inside one shot
    ("dalio", 729.00, 960, 430, 1100), ("schwarzman", 2182.40, 960, 400, 1100), ("fraser", 1640.00, 940, 420, 1100),
    ("dimon", 916.00, 975, 430, 1150), ("fink", 1185.00, 960, 470, 1000), ("solomon", 2826.00, 1026, 420, 1100),
    ("motsepe", 1816.00, 915, 440, 1150), ("shen", 2624.60, 900, 450, 1050), ("wikram", 3007.00, 960, 430, 1100),
]


def tile_clip3(t0, n, cx, cy, span, tw, th):
    fr = grab(PANEL, t0, n, fps=FPS)
    ch = span * th / tw
    x0 = int(min(max(cx - span / 2, 0), 1920 - span))
    y0 = int(min(max(cy - ch / 2, 0), 1080 - ch))
    out = []
    for im in fr:
        c = im[y0:int(y0 + ch), x0:int(x0 + span)]
        out.append(grade(cv2.resize(c, (tw, th), interpolation=cv2.INTER_AREA), sat=0.92, contrast=1.08))
    while len(out) < n:
        out.append(out[-1])
    return out


def r_tiles3():
    n = beat_frames("tiles")                         # 139: "These" (frame 3) to "on"
    t0 = round(TM.B["tiles"][0] * FPS)
    k_these = round(TM.T["these"] * FPS) - t0
    G, tw, th = 6, 640 - 6, 360 - 6
    clips = [tile_clip3(t, n, cx, cy, sp, tw, th) for _, t, cx, cy, sp in TILES3]
    Wt, Bk, Fc = "W", "B", "F"
    pat = {k_these: [Wt, Wt, Bk, Wt, Bk, Bk, Bk, Wt, Bk],          # Nvidia frames 15 / 16 / 17 (24 fps) at 60 fps
           k_these + 3: [Bk, Fc, Wt, Fc, Wt, Bk, Wt, Fc, Bk],
           k_these + 6: [Fc, Fc, Wt, Fc, Fc, Fc, Bk, Fc, Fc],
           k_these + 9: [Fc] * 9}
    order = [4, 0, 8, 2, 6, 1, 7, 3, 5]
    flashes = {}
    step = (n - 36 - (k_these + 12)) / len(order)
    for j, tile in enumerate(order):                 # one tile lights in turn, evenly until the negatives
        flashes.setdefault(tile, []).append(int(k_these + 12 + step * j))
    env = [0.95, 0.62, 0.32, 0.14, 0.05]
    neg = set(range(n - 21, n - 18)) | set(range(n - 8, n - 5))
    blk = {n - 12, n - 11, n - 9}
    wr = Writer(f"{CLIPS}/r_tiles3.mp4")
    state = [Bk] * 9
    for i in range(n):
        if i in pat:
            state = pat[i]
        fr = np.full((H, W, 3), 10, np.float32)
        if i >= k_these:
            for k in range(9):
                r, c = divmod(k, 3)
                x, y = c * 640 + G // 2, r * 360 + G // 2
                if state[k] == "W":
                    tile = np.full((th, tw, 3), 246, np.float32)
                elif state[k] == "B":
                    tile = np.full((th, tw, 3), 6, np.float32)
                else:
                    tile = clips[k][min(i, n - 1)].copy()
                    for f0 in flashes.get(k, []):
                        j = i - f0
                        if 0 <= j < len(env):
                            tile = tile * (1 + 0.6 * env[j]) + 255 * env[j] * 0.85
                fr[y:y + th, x:x + tw] = tile
            z = 1.0 + 0.035 * i / n                  # a subtle push on the whole grid
            fr = affine(fr, z, W / 2, H / 2, W / 2, H / 2, border=(10, 10, 10))
        if i in neg:
            fr = 255 - np.clip(fr, 0, 255)
        elif i in blk:
            fr[:] = 0
        elif i >= n - 5:
            fr[:] = (95, 255, 255)
        wr.write(fr)
    wr.close()
    print("   negatives at", sorted(neg), "black", sorted(blk))


# ------------------------------------------------------------------ 3. the $60 trillion articles
ARTICLE_ORDER = [6, 2, 7, 3, 9, 5, 10, 1, 8, 4, 6, 2, 7, 9]


def highlight_box(img):
    """The lime-green highlight behind "$60 trillion": (x0, y0, x1, y1)."""
    f = img.astype(np.int16)
    m = ((f[..., 1] > 200) & (f[..., 0] > 140) & (f[..., 0] < 235) & (f[..., 2] < 120)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 41), np.uint8))   # merge the box across the dark letters
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = st[k, :4]
    return x, y, x + w, y + h


def r_articles():
    n = beat_frames("money")                        # 85: "a $60 trillion dollar"
    HL = 104                                         # every highlight the same height on screen
    pages = {}
    for k in range(1, 11):
        im = np.asarray(Image.open(f"{V3}/cutouts/c{k:02d}.png").convert("RGB")).astype(np.float32)
        x0, y0, x1, y1 = highlight_box(im)
        s = HL / (y1 - y0)
        pages[k] = (im, s, (x0 + x1) / 2, (y0 + y1) / 2)
        print(f"   c{k:02d} highlight {x1 - x0}x{y1 - y0} at ({(x0 + x1) // 2},{(y0 + y1) // 2}) scale {s:.2f}")
    k_pages = max(1, n // 6)
    order = (ARTICLE_ORDER * 3)[:k_pages]
    durs = [6] * (k_pages - 1) + [n - 6 * (k_pages - 1)]
    canvas = np.full((H, W, 3), 246, np.float32)
    wr = Writer(f"{CLIPS}/r_articles.mp4")
    i = 0
    for k, d in zip(order, durs):
        im, s, hx, hy = pages[k]
        rgba = np.dstack([im, np.full(im.shape[:2], 255, np.float32)])
        layer = affine(rgba, s, hx, hy, W / 2, H / 2)
        a = layer[..., 3:4] / 255
        sh = np.roll(cv2.GaussianBlur(a[..., 0], (0, 0), 18), 10, axis=0)[..., None]
        canvas = canvas * (1 - 0.35 * sh * (1 - a))           # a soft shadow where it overlaps the pile
        canvas = canvas * (1 - a) + layer[..., :3] * a
        for _ in range(d):
            z = 1.0 + 0.06 * i / n                              # the subtle push-in, about the highlight
            fr = affine(canvas, z, W / 2, H / 2, W / 2, H / 2)
            wr.write(fr + grain(seed=1500 + i, amt=2.5))
            i += 1
    wr.close()


# ------------------------------------------------------------------ 4. touch without the painting
TOUCH = f"{DL}/touch_rawcanvas.mp4"


def r_touch3():
    n = beat_frames("touch")                          # 53
    t0 = round(TM.B["touch"][0] * FPS)
    k_touch = round(TM.T["touch"] * FPS) - t0         # the fingertips meet on "touch"
    hands = cover(frame_at(TOUCH, 0, 24).astype(np.float32))
    strip = hands[:, 922:992]
    plate = np.concatenate([strip] * (W // strip.shape[1] + 1), axis=1)[:, :W]
    lum = cv2.GaussianBlur(hands.mean(axis=2), (0, 0), 1.2)
    mask = np.clip((lum - 34) / 40, 0, 1)[..., None]
    left_m, right_m = mask.copy(), mask.copy()
    left_m[:, 960:] = 0
    right_m[:, :960] = 0
    seq = []
    for j in range(k_touch):
        u = smooth((j + 1) / k_touch)
        d = 260 - 305 * u                              # from wide apart to 45 px past: the tips meet on "touch"
        fr = plate.copy()
        for m, dx in ((left_m, -d), (right_m, d)):
            M = np.float32([[1, 0, dx], [0, 1, 0]])
            hs = cv2.warpAffine(hands, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            ms = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)[..., None]
            fr = fr * (1 - ms) + hs * ms
        seq.append(fr)
    nb = n - len(seq)                                 # after "touch": the clip runs on at its own 24 fps
    burst = [cover(frame_at(TOUCH, f, 24).astype(np.float32)) for f in range(21, 21 + int(nb * 24 / FPS) + 2)]
    for j in range(nb):
        seq.append(burst[min(len(burst) - 1, int(j * 24 / FPS))])
    wr = Writer(f"{CLIPS}/r_touch3.mp4")
    for i, fr in enumerate(seq):
        wr.write(fr + grain(seed=400 + i, amt=4))
    wr.close()


ALL = {"shots": shots, "tiles": r_tiles3, "articles": r_articles, "touch": r_touch3}


# ------------------------------------------------------------------ helpers for the cut-out shots
def logo_mask(img):
    """The panel's FII watermark at the top left (white letters), dilated, for inpainting."""
    reg = img[:200, :420].astype(np.float32).mean(axis=2)
    m = np.zeros(img.shape[:2], np.uint8)
    m[:200, :420] = (reg > 150).astype(np.uint8)
    return cv2.dilate(m, np.ones((9, 9), np.uint8))


def person_frames(name, n, s, ox, oy, clean=False):
    """The panel segment and its cut-out alpha (25 fps), reframed by scale s and offset (ox, oy), as 60 fps frames."""
    seg = f"{CUT}/{name}_seg.mp4"
    k = math.ceil(n / FPS * 25) + 2
    src = grab(seg, 0.0, k)
    if clean:
        lm = logo_mask(src[0])
        src = [cv2.inpaint(np.ascontiguousarray(f), lm, 9, cv2.INPAINT_TELEA) for f in src]
    al = grab(f"{CUT}/{name}_cut.webm", 0.0, k, alpha=True)
    M = np.float32([[s, 0, ox], [0, s, oy]])
    out = []
    for i in range(n):
        j = min(int(i / FPS * 25), len(src) - 1, len(al) - 1)
        img = cv2.warpAffine(src[j].astype(np.float32), M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        a = cv2.warpAffine(al[j][..., 3].astype(np.float32) / 255, M, (W, H), flags=cv2.INTER_LINEAR)
        out.append((img, a))
    return out


def block_entrance(i, i_word):
    """The reference edit's word entrance: a faint ghost (4 frames), a glowing white block (4 frames), the word."""
    if i < i_word - 8:
        return None
    if i < i_word - 4:
        return "ghost"
    if i < i_word:
        return "block"
    return "word"


def word_layer(text, font_path, size, x, baseline, pad=24):
    m, base, _ = text_mask(text, font_path, size, pad=pad)
    a = np.zeros((H, W), np.float32)
    paste_alpha(a, m, x - pad, baseline - base)
    ys, xs = np.where(m > 0.3)
    box = (x - pad + xs.min(), baseline - base + ys.min(), x - pad + xs.max(), baseline - base + ys.max())
    return a, box


def block_layer(box, grow=6):
    x0, y0, x1, y1 = box
    a = np.zeros((H, W), np.float32)
    a[max(0, int(y0) - grow):int(y1) + grow, max(0, int(x0) - grow):int(x1) + grow] = 1.0
    return cv2.GaussianBlur(a, (0, 0), 1.2)


# ------------------------------------------------------------------ 5. Dimon: the reference edit's "if intelligence is automated"
SERIF = f"{FONTS}/InstrumentSerif-Regular.woff2"
SERIF_I = f"{FONTS}/InstrumentSerif-Italic.woff2"


def r_dimon3():
    n = beat_frames("dimon")                          # 118: "That's Jamie Dimon, the guy running"
    t0 = round(TM.B["dimon"][0] * FPS)
    rel = lambda w: round(TM.T[w] * FPS) - t0
    frs = person_frames("dimon", n, 1.2, 0.0, -60.0)  # him on the right, room for the words on the left
    # the band is red (the user); it comes down from the flash and has covered the name's line by "Jamie"
    band_key = [(0, 0.0), (8, 0.15), (10, 0.22), (12, 0.28), (14, 0.33), (16, 0.37), (19, 0.40), (40, 0.43), (n, 0.44)]
    name_a, name_box = word_layer("Jamie Dimon", INTER_B, 150, 84, 392)
    that_a, that_box = word_layer("That’s", SERIF_I, 84, 92, int(name_box[1]) - 18)   # right above the name
    words = [("the", "the1", 104), ("guy", "guy1", None), ("running", "running", None)]
    serif_size, serif_base = 138, 600
    layers, x = [], 104
    for w, key, _ in words:
        a, box = word_layer(w, SERIF, serif_size, x, serif_base)
        layers.append((a, box, rel(key)))
        x = box[2] + 36
    k_jamie = rel("jamie")
    wr = Writer(f"{CLIPS}/r_dimon3.mp4")
    for i in range(n):
        img, pa = frs[i]
        bg = img.copy()
        edge = np.interp(i, [k for k, _ in band_key], [v for _, v in band_key]) * H
        if edge > 1:
            band = np.zeros((H, W), np.float32)
            band[:int(edge)] = 1.0
            band = cv2.GaussianBlur(band, (0, 0), 1.5)
            bg = over_color(bg, band, RED)
        # "That's": a small white square, then the word (the reference's "if"), inside the band
        if 8 <= i < 10:
            sq = np.zeros((H, W), np.float32)
            sq[int(that_box[1]) + 6:int(that_box[1]) + 40, int(that_box[0]):int(that_box[0]) + 34] = 1
            bg = over_color(bg, sq, WHITE)
        elif i >= 10:
            bg = over_color(bg, that_a, WHITE)
        # "Jamie Dimon": white inside the red band, blurring in on "Jamie", behind him
        if i >= k_jamie:
            u = min(1.0, (i - k_jamie + 1) / 7)
            a = name_a
            if u < 1:
                a = cv2.GaussianBlur(name_a, (0, 0), 10 * (1 - u) + 0.1) * (0.25 + 0.75 * u)
            bg = over_color(bg, a, WHITE)
        # the person in front
        fg = img
        if 8 <= i < 10:                                 # the flash: everything washes towards white
            bg = bg * 0.45 + 255 * 0.55
            fg = fg * 0.3 + 255 * 0.7
        elif 10 <= i < 16:                              # his silhouette flat white, the room lighter
            bg = bg * 0.85 + 255 * 0.15
            fg = fg * 0.1 + WHITE * 0.9
        elif 18 <= i < 20:                              # the second bright frame
            bg = bg * 0.6 + 255 * 0.4
            fg = fg * 0.6 + 255 * 0.4
        fr = bg * (1 - pa[..., None]) + fg * pa[..., None]
        # "the guy running": Instrument Serif, each word a ghost, a white block, then the word with its glow
        for a, box, k in layers:
            st = block_entrance(i, k)
            if st == "ghost":
                fr = over_color(fr, a * 0.35, WHITE)
            elif st == "block":
                b = block_layer(box)
                fr = glow_text(fr, b, (255, 255, 255), glow=0.8)
            elif st == "word":
                sh = cv2.GaussianBlur(a, (0, 0), 9)
                fr = fr * (1 - 0.5 * np.clip(sh * 1.5, 0, 1))[..., None]
                fr = glow_text(fr, a, (246, 244, 240), glow=0.75)
        wr.write(fr + grain(seed=1700 + i, amt=2.2))
    wr.close()


# ------------------------------------------------------------------ 6. the reel's "the man behind OpenAI" device
def live(src, t0, n, crop=None, fc=False, u8=False):
    """n frames at 60 fps from a clip (optionally a crop filter), as float RGB 1920x1080 (uint8 with u8: a quarter of
    the memory, for devices that hold many sources at once)."""
    vf = (crop + "," if crop else "") + "setsar=1"
    ss = t0 + (stream_start(src) if fc else 0.0)
    got = grab(src, ss, n, fps=FPS, vf=vf, size=(W, H))
    return got if u8 else [f.astype(np.float32) for f in got]


def hero_text(text, size, seed, y=540):
    m, base, _ = text_mask(text, INTER_B, size, pad=30)
    m = m * speckle(m.shape, seed)
    a = np.zeros((H, W), np.float32)
    paste_alpha(a, m, (W - m.shape[1]) / 2, y - m.shape[0] / 2)
    return a


def small_caption(text, size=50, y=540, font=None):
    m, base, _ = text_mask(text, font or INTER_B, size, pad=20)
    a = np.zeros((H, W), np.float32)
    paste_alpha(a, m, (W - m.shape[1]) / 2, y - m.shape[0] / 2)
    return a


def with_caption(fr, a, color=(250, 250, 250), shadow=0.55):
    sh = cv2.GaussianBlur(a, (0, 0), 7)
    fr = fr * (1 - shadow * np.clip(sh * 1.4, 0, 1))[..., None]
    return glow_text(fr, a, color, glow=0.45)


def chase_logo(size=360):
    """The Chase octagon (four wedges round a square hole), white, centred, with a blue glow."""
    a = np.zeros((H, W), np.float32)
    c = np.array([W / 2, H / 2])
    r, h = size / 2, size * 0.17
    base = np.array([[-r * 0.42, -r], [r * 0.42, -r], [r, -r * 0.42], [r * 0.42 - h * 0.0, -r * 0.42 + 0.0]])
    wedge = np.array([[-r * 0.42, -r], [r * 0.42, -r], [r, -r * 0.42], [h, -r * 0.42], [h, -h], [-r * 0.42, -h]])
    for k in range(4):
        th = k * math.pi / 2
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        pts = (wedge @ R.T + c).astype(np.int32)
        cv2.fillPoly(a, [pts], 1.0, lineType=cv2.LINE_AA)
    return a


def grid_cells(cols=3, rows=2, gap=6):
    cw, ch = (W - gap * (cols + 1)) // cols, (H - gap * (rows + 1)) // rows
    return [(gap + c * (cw + gap), gap + r * (ch + gap), cw, ch) for r in range(rows) for c in range(cols)], cw, ch


def altman_device(name, n, flip, collage, logo, cells, hero, cap=None, cap_until=0, seed=0, k_collage=30, glow=None):
    """flip: list of frame-lists (each source's 60 fps frames); collage: (left frames, right frames);
    logo: an RGB frame (the 1-frame logo); cells: 6 frame-lists for the grid; hero: the textured hero word."""
    hero_a = hero_text(hero, 150, seed)
    cap_a = small_caption(cap) if cap else None
    slots, cw, ch = grid_cells()
    k = k_collage
    wr = Writer(f"{CLIPS}/{name}.mp4")
    for i in range(n):
        if i < k:                                            # the flipbook, a new picture every 5 frames
            src = flip[min(i // 5, len(flip) - 1)]
            fr = curved(src[min(i, len(src) - 1)])
        else:
            lf, rf = collage
            j = i - k
            col = np.concatenate([cover(lf[min(j, len(lf) - 1)], W // 2, H), cover(rf[min(j, len(rf) - 1)], W // 2, H)], axis=1)
            col = curved(col)
            if j < 2:
                fr = col
            elif j < 8:
                fr = negative(col)
            elif j < 10:
                fr = col
            elif j < 12:
                fr = negative(col)
            elif j < 15:                                     # the logo, glowing, over the darkened collage
                fr = col * 0.35 + logo * 0.9
            else:                                            # the grid fills cell by cell over the collage
                fr = col * 0.5
                for c, (x, y, w_, h_) in enumerate(slots):
                    if j >= 15 + 5 * c:
                        clip = cells[c]
                        f = clip[min(j - 15 - 5 * c, len(clip) - 1)]
                        fr[y:y + h_, x:x + w_] = cover(f, w_, h_)
                fr = curved(fr, k=0.06)
            if j >= 8:                                       # the title: a subtle white glow (the user, Nov 22)
                fr = glow_text(fr, hero_a, (250, 250, 250), glow=glow, sigma=(8, 24)) if glow else \
                    with_caption(fr, hero_a, shadow=0.6)
        if cap_a is not None and i < cap_until:
            fr = with_caption(fr, cap_a)
        wr.write(fr + grain(seed=seed * 1000 + i, amt=3.5))
    wr.close()


JPM = {  # JPMorgan footage (videos, checked: they move)
    "hq": (f"{J2}/HOW_69230_151.mp4", 0.0), "doors": (f"{J2}/LASTFAST_370_112.mp4", 0.0),
    "board": (f"{J2}/MONT_1410_73.mp4", 0.0), "tower": (f"{J2}/JPH2_445_259.mp4", 0.0),
    "tower2": (f"{J2}/JPH2_945_97.mp4", 0.0), "ticker": (f"{J2}/MONT_1241_83.mp4", 0.0),
}


def r_jpm():
    n = beat_frames("jpm")                            # 86: "JP Morgan Chase" + the pause
    L = {k: live(p, t, 90, u8=True) for k, (p, t) in JPM.items()}
    flip = [L[k][j * 5:] for j, k in enumerate(["hq", "doors", "board", "tower", "ticker", "tower2"])]
    collage = (L["hq"][20:], L["board"][20:])
    logo = np.zeros((H, W, 3), np.float32)
    la = chase_logo(380)
    glow = cv2.GaussianBlur(la, (0, 0), 30)
    logo = logo + np.array([60, 140, 255], np.float32) * np.clip(glow * 1.6, 0, 1)[..., None]
    logo = over_color(logo, la, (250, 252, 255))
    cells = [L["tower"][30:], L["doors"][30:], L["board"][30:], L["hq"][30:], L["ticker"][30:], L["tower2"][30:]]
    altman_device("r_jpm", n, flip, collage, logo, cells, "JPMorgan Chase", seed=7, glow=0.75)


def r_ceo():
    n = beat_frames("ceo")                            # 84: "CEO of Goldman Sachs"
    GS = f"{V3}/goldman.mp4"
    sol_a = live(PANEL, 2826.4, 60)
    sol_b = live(PANEL, 2827.6, 60)
    sol_c = live(PANEL, 2802.9, 20)
    dj_a = live(f"{DL}/solomon_dj.mp4", 1.48, 60, crop="crop=1080:608:0:470", fc=True)
    gs_w = live(GS, 1.0, 80)
    gs_l = live(GS, 4.0, 80, crop="crop=1920:1080:960:400")
    gs_t = live(GS, 7.0, 80, crop="crop=2400:1350:720:0")
    flip = [sol_a, gs_w, dj_a, sol_c, gs_l]
    collage = (sol_b[10:], gs_w[30:])
    lg = gs_l[40]
    logo = np.clip(lg * 1.25 + cv2.GaussianBlur(lg, (0, 0), 25) * 0.6, 0, 255)
    cells = [gs_w[20:], sol_a[20:], gs_l[20:], dj_a[20:], gs_t[20:], sol_b[20:]]
    altman_device("r_ceo", n, flip, collage, logo, cells, "Goldman Sachs", cap="the CEO of", cap_until=24, seed=9,
                  k_collage=24)


# ------------------------------------------------------------------ 7. Solomon: the reference edit's "AI"
def r_solomon3():
    n = beat_frames("solomon")                        # 100: "David Solomon, a part-time"
    t0 = round(TM.B["solomon"][0] * FPS)
    rel = lambda w: round(TM.T[w] * FPS) - t0
    frs = person_frames("solomon", n, 1.3, -4.0, -40.0, clean=True)
    union = np.max([a for _, a in frs[::5]], axis=0) > 0.25
    size = 300
    while True:                                      # the biggest name that stays clear of him
        cap = 0.727 * size
        b1 = int(70 + cap)
        b2 = int(b1 + 0.98 * size)
        da, dbox = word_layer("David", INTER_XB, size, 150, b1)
        sa, sbox = word_layer("Solomon", INTER_XB, size, 150, b2)
        rows = union[int(sbox[1]):int(sbox[3])]
        cols = np.where(rows.any(axis=0))[0]
        edge = cols.min() if len(cols) else W
        if sbox[2] < edge - 30 or size <= 150:
            break
        size -= 8
    print("   name size", size, "Solomon ends", sbox[2], "his edge", edge)
    grad = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    gold = GOLD_TOP * (1 - grad) + GOLD_BOT * grad
    k_sol = rel("solomon")
    # the vertical yellow line, bottom to top beside the name
    ywords = [("a part-time", rel("a3")), ("DJ", rel("a3") + 22)]
    ylayers, cursor = [], 0
    for w, k in ywords:
        m, base, _ = text_mask(w, INTER_B, 66, pad=14)
        rot = np.rot90(m)                              # reads bottom to top
        a = np.zeros((H, W), np.float32)
        y_bottom = int(sbox[3]) - cursor
        paste_alpha(a, rot, 26, y_bottom - rot.shape[0])
        ys, xs = np.where(rot > 0.3)
        box = (26 + xs.min(), y_bottom - rot.shape[0] + ys.min(), 26 + xs.max(), y_bottom - rot.shape[0] + ys.max())
        ylayers.append((a, box, k))
        cursor += rot.shape[0] - 6
    bar_y0 = int(sbox[3]) + 46
    bar_y1, bar_end = bar_y0 + 250, 1760
    k_bar0, k_bar1 = 8, 46
    wr = Writer(f"{CLIPS}/r_solomon3.mp4")
    prev_x = 0.0
    for i in range(n):
        img, pa = frs[i]
        bg = img.copy()
        # the red bar slides out from the left edge, its leading edge blurred while it moves
        if i >= k_bar0:
            u = min(1.0, (i - k_bar0) / (k_bar1 - k_bar0))
            xe = bar_end * (1 - (1 - u) ** 3)
            bar = np.zeros((H, W), np.float32)
            bar[bar_y0:bar_y1, :int(xe)] = 1.0
            v = xe - prev_x
            if v > 1:
                kl = int(min(120, v * 2.2)) | 1
                bar = cv2.filter2D(bar, -1, np.ones((1, kl), np.float32) / kl)
            prev_x = xe
            bg = over_color(bg, bar, RED)
        # the giant name behind him, white with a soft glow: "David" from the cut, "Solomon" on its word
        name = da if i < k_sol else np.maximum(da, sa)
        bg = glow_text(bg, name, (250, 250, 248), glow=0.9, sigma=(8, 26))
        fr = bg * (1 - pa[..., None]) + img * pa[..., None]
        for a, box, k in ylayers:
            st = block_entrance(i, k)
            if st == "ghost":
                fr = over_color(fr, a * 0.35, YELLOW)
            elif st == "block":
                fr = glow_text(fr, block_layer(box, grow=4), (255, 255, 240), glow=0.6)
            elif st == "word":
                sh = cv2.GaussianBlur(a, (0, 0), 8)
                fr = fr * (1 - 0.6 * np.clip(sh * 1.6, 0, 1))[..., None]
                fr = glow_text(fr, a, YELLOW, glow=0.7, sigma=(5, 14))
        wr.write(fr + grain(seed=1900 + i, amt=2.2))
    wr.close()


# ------------------------------------------------------------------ 8. the orbit at its settled zoom
def r_orbit3():
    n = beat_frames("orbit")                          # the pause after "Goldman Sachs" and "Amongst them"
    src = V2.src_frames(V2.ORBIT, 0, 40)
    d = V2.orbit_tracks(40)
    keys = list(V2.ORBIT_POLY)
    nb = {(0, 1), (1, 2), (4, 6), (6, 7), (8, 9), (9, 10), (10, 11), (2, 4)}
    apart = {(keys.index(a), keys.index(b)) for a, b in nb if a in keys and b in keys}
    sched = V2.schedule(len(keys), 1, n - 1, seed=29, apart=apart)
    Z, cx, cy = 1.25 * 1.24, 915, 498                 # the zoom v2 settled at, held (no zoom move)
    wr = Writer(f"{CLIPS}/r_orbit3.mp4")
    for i in range(n):
        j = min(int(i / FPS * 25), len(src) - 1)
        im = src[j].astype(np.float32)
        for p in sched.get(math.floor(i / FPS * 24 + 1e-6), []):
            k = keys[p]
            im = V2.light(im, V2.poly_mask(V2.ORBIT_POLY[k], *d[j, k]), scale=0.8)
        im = V2.xgrade(im)
        im = affine(im, Z, cx, cy, cx, cy, border=(20, 18, 20))
        wr.write(im + grain(seed=2100 + j, amt=3.2))
    wr.close()


# ------------------------------------------------------------------ 9. "Amongst them is this guy": the reel's selection box
_BEAM = {}


def beam_backdrop():
    """White with two soft grey wedges (top right, bottom left): daylight through a window, as in the reel."""
    if "b" not in _BEAM:
        a = np.zeros((H, W), np.float32)
        cv2.fillPoly(a, [np.int32([[0.56 * W, -10], [W + 10, -10], [W + 10, 0.43 * H]])], 1.0)
        cv2.fillPoly(a, [np.int32([[-10, 0.57 * H], [-10, H + 10], [0.45 * W, H + 10]])], 1.0)
        a = cv2.GaussianBlur(a, (0, 0), 22)
        tex = cv2.GaussianBlur(np.random.default_rng(3).normal(0, 1, (H, W)).astype(np.float32), (0, 0), 1.1) * 9
        base = np.full((H, W, 3), 247, np.float32) - radial(W * 0.45, H * 0.5, 500, 1300)[..., None] * 10
        shade = (112 + tex)[..., None] * np.ones(3, np.float32)
        _BEAM["b"] = base * (1 - a[..., None]) + shade * a[..., None]
    return _BEAM["b"]


def face_crop(frames_, cx, cy, w, h):
    out = []
    for f in frames_:
        x0, y0 = int(min(max(cx - w / 2, 0), W - w)), int(min(max(cy - h / 2, 0), H - h))
        out.append(f[y0:y0 + h, x0:x0 + w])
    return out


def handles(fr, x0, y0, x1, y1, color, size=14, glow=None):
    for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        fr[int(y - size / 2):int(y + size / 2), int(x - size / 2):int(x + size / 2)] = color
    return fr


def r_amongst():
    a0, a1 = TM.B["amongst"][0], TM.B["thisguy"][1]
    n = nf(a0, a1)                                     # 108: "Amongst them is this guy"
    t0 = round(a0 * FPS)
    rel = lambda w: round(TM.T[w] * FPS) - t0
    k_them, k_is, k_this = rel("them"), rel("is"), rel("this")
    people = []                                       # the other panelists, live, framed on the face (4:3)
    for name, t, cx, cy, sp in TILES3:
        if name == "fink":
            continue
        fr_ = live(PANEL, t + 0.4, 12)
        people.append(face_crop(fr_, cx, cy - 60, int(sp * 0.62), int(sp * 0.62 * 0.75)))
    fink = live(PANEL, 1185.3, 70)
    caps = [("And amongst", 0), ("them", k_them), ("them is", k_is), ("this guy.", k_this)]
    cap_layers = [(small_caption(c, size=54), k) for c, k in caps]
    bd = beam_backdrop()
    wr = Writer(f"{CLIPS}/r_amongst.mp4")
    for i in range(n):
        if i < k_is:
            p = people[(i // 5) % len(people)]
            ph = p[min(i % 5 + (i // 30), len(p) - 1)]
            if i < k_them:                            # small box on the white window light
                pw = int(300 * (1 + 0.15 * i / k_them))
                fr = bd.copy()
                hdl, pad = (12, 12, 12), 14
            else:                                     # on black, bigger, a soft glow, white handles
                pw = int(430 * (1 + 0.08 * (i - k_them) / max(1, k_is - k_them)))
                fr = np.full((H, W, 3), 6, np.float32)
                hdl, pad = (250, 250, 250), 16
            ph_ = cv2.resize(ph, (pw, int(pw * 0.75)), interpolation=cv2.INTER_AREA)
            x0, y0 = (W - pw) // 2, (H - ph_.shape[0]) // 2
            if i >= k_them:
                g = np.zeros((H, W), np.float32)
                g[y0 - 30:y0 + ph_.shape[0] + 30, x0 - 30:x0 + pw + 30] = 1
                fr = fr + 140 * cv2.GaussianBlur(g, (0, 0), 40)[..., None]
            fr[y0:y0 + ph_.shape[0], x0:x0 + pw] = ph_
            fr = handles(fr, x0 - pad, y0 - pad, x0 + pw + pad, y0 + ph_.shape[0] + pad, hdl)
        else:
            j = i - k_is
            f = fink[min(j, len(fink) - 1)]
            if j < 6:                                  # the light-leak flash: the box grows into his card
                u = (j + 1) / 6
                cw = int(430 + (1180 - 430) * (1 - (1 - u) ** 2))
                ch = int(cw * 9 / 16)
                fr = np.full((H, W, 3), 6, np.float32)
                card = cv2.resize(cover(f, 1600, 900), (cw, ch), interpolation=cv2.INTER_AREA)
                x0, y0 = (W - cw) // 2, (H - ch) // 2
                fr[y0:y0 + ch, x0:x0 + cw] = card
                leak = radial(W * 0.35, H * 0.4, 0, 900)[..., None]
                warm = np.array([255, 236, 205], np.float32)
                fr = fr * (0.4 + 0.6 * leak) + warm * (1 - leak) * (0.9 - 0.12 * j)
                fr = cv2.GaussianBlur(fr, (0, 0), 6 - j)
            else:                                     # his card held on the window light, a slow push-in
                z = 1.0 + 0.045 * (j - 6) / max(1, n - k_is - 6)
                cw, ch = int(1180 * z), int(1180 * z * 9 / 16)
                fr = bd.copy()
                card = cv2.resize(cover(f, 1600, 900), (cw, ch), interpolation=cv2.INTER_AREA)
                x0, y0 = (W - cw) // 2, (H - ch) // 2
                sh = np.zeros((H, W), np.float32)
                sh[y0 + 14:y0 + ch + 14, x0 + 10:x0 + cw + 10] = 1
                fr = fr * (1 - 0.35 * cv2.GaussianBlur(sh, (0, 0), 16))[..., None]
                fr[y0:y0 + ch, x0:x0 + cw] = card
                if i >= n - 2:
                    fr = whip(fr)
        cur = None
        for a, k in cap_layers:
            if i >= k:
                cur = a
        if cur is not None and i < n - 2:
            fr = with_caption(fr, cur, shadow=0.5)
        wr.write(fr + grain(seed=2300 + i, amt=3.0))
    wr.close()


# ------------------------------------------------------------------ 10. the rest of the script: every shot cut on its word
import shotlist as SL


def shot_bounds(shots, part_start, part_end):
    """Film start / end of each shot of a part (a shot ends where the next one starts)."""
    t = [part_start if k in ("rest1", "rest2") else TM.RTX(k) for k, *_ in shots]
    return [(a, b) for a, b in zip(t, t[1:] + [part_end])]


# where a chosen shot ends in its source (the next frame is a cut): a slot longer than that slows the shot instead
SHOT_END = {"r2_lobby": 5.93, "r2_bull": 2.795, "r1_ap": 26.74, "r2_founding": 26.87, "r1_flags": 3.29,
            "r1_glass": 5.095, "r2_aladdin": 53.62, "r2_datacenter": 60.28, "r1_ft": 16.34}


def rest_shots(names=None):
    for shots, part in ((SL.REST1, "rest1"), (SL.REST2, "rest2")):
        a0, a1 = TM.B[part]
        for (key, name, src, t0, extra, fc), (a, b) in zip(shots, shot_bounds(shots, a0, a1)):
            if src in ("card", "clip", "FX") or (names and name not in names):
                continue
            crop = None
            if src == "E":
                path, crop = f"{V3}/ending_user.mp4", extra
            elif src == "N":
                path, crop = f"{V3}/new/{extra[0]}", extra[1]
            elif src == "X":
                path, crop = f"{V3}/br_explainer.mp4", extra
            elif src == "J":
                path = f"{J2}/{extra}.mp4"
                if t0:
                    path = path
            elif src == "D":
                path = f"{DL}/{extra}"
            else:
                path = PANEL
            ss = t0 + (stream_start(path) if fc else 0.0)
            dur = b - a + 0.15
            filt = ([crop] if crop else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", "fps=60"]
            inp = ["-ss", f"{ss:.3f}"]
            if name in SHOT_END and SHOT_END[name] - t0 < b - a + 0.02:
                avail = SHOT_END[name] - t0
                k = (b - a + 0.05) / avail
                inp += ["-t", f"{avail:.3f}"]
                filt = filt[:-1] + [f"setpts={k:.4f}*PTS", "fps=60", "tpad=stop_mode=clone:stop_duration=0.2"]
                print(f"   {name}: its shot is {avail:.2f}s for a {b - a:.2f}s slot, slowed x{k:.2f}")
            subprocess.run(["ffmpeg", "-v", "error", "-y"] + inp + ["-i", path, "-t", f"{dur:.3f}", "-vf",
                            ",".join(filt), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{CLIPS}/v3_{name}.mp4"], check=True)
            got = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                                 "csv=p=0", f"{CLIPS}/v3_{name}.mp4"]).strip())
            flag = ""
            if got < b - a - 0.02:                    # a short library clip: slow it just enough to fill the slot
                k = dur / max(0.1, got)
                filt2 = ([crop] if crop else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", f"setpts={k:.3f}*PTS",
                                                    "fps=60"]
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", path, "-vf", ",".join(filt2),
                                "-t", f"{dur:.3f}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                                "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{CLIPS}/v3_{name}.mp4"], check=True)
                flag = f"  slowed x{k:.2f}"
            print(f"   {name:12s} {a:7.3f}-{b:7.3f}{flag}")


# ------------------------------------------------------------------ 11. the notes of Nov 21 (evening)
def r_cartel3():
    """The user's cartel clip as it is: from the flash on the table (its frame 14, 24 fps); its cut to the faces (frame
    28) lands on "cartel"; the faces and their glitches run until "weaponized". Its first frames (rising out of black)
    are not used, as the user asked."""
    a0, a1 = TM.B["cartel"]
    n = nf(a0, a1)
    k_c = round(TM.T["cartel"] * FPS) - round(a0 * FPS)
    src = grab(f"{V3}/cartel_user.mp4", 0.0, 66)
    wr = Writer(f"{CLIPS}/r_cartel3.mp4")
    for i in range(n):
        j = min(14 + int(i * 24 / FPS), 27) if i < k_c else 28 + int((i - k_c) * 24 / FPS)
        wr.write(src[min(j, len(src) - 1)].astype(np.float32))
    wr.close()
    print("   faces cut in at film frame", k_c, "/", n)


def find_face(img, expect, size):
    """The detected face nearest to `expect` (x, y), or a box of `size` there."""
    g = cv2.equalizeHist(cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_RGB2GRAY))
    best = None
    for c in HAAR:
        for (x, y, w, h) in c.detectMultiScale(g, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40)):
            dd = math.hypot(x + w / 2 - expect[0], y + h / 2 - expect[1])
            if dd < 160 and (best is None or dd < best[0]):
                best = (dd, (int(x), int(y), int(w), int(h)))
    if best:
        return best[1]
    return (int(expect[0] - size / 2), int(expect[1] - size / 2), int(size), int(size))


def r_spot():
    """"is this guy": the user's group image, and the reel's move (DeJRKmqTPdg, 3.03-3.33 s) on Fink -- a white square
    on his face (2 frames at 30 fps), a whole-frame negative (1), a small negative box on his face (2), the room
    going dark under the box (1), then the room at about a fifth of its light with only his face lit, held."""
    a0, a1 = TM.B["thisguy"]
    n = nf(a0, a1)
    img = np.asarray(Image.open(f"{V3}/fink_spot.png").convert("RGB")).astype(np.float32)
    ih, iw = img.shape[:2]
    k = H / ih
    big = cv2.resize(img, (int(round(iw * k)), H), interpolation=cv2.INTER_CUBIC)
    x0 = int(min(max(836 * k - W / 2, 0), big.shape[1] - W))
    base = big[:, x0:x0 + W].copy()
    fx, fy, fw, fh = find_face(base, (836 * k - x0, 430 * k), 120 * k)
    cx, cy = fx + fw / 2, fy + fh / 2
    print(f"   Fink's face {fx},{fy} {fw}x{fh}")
    pad = 0.18
    bx0, by0 = int(fx - fw * pad), int(fy - fh * pad)
    bx1, by1 = int(fx + fw * (1 + pad)), int(fy + fh * (1 + pad))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - cx) / (fw * 0.95)) ** 2 + ((yy - cy - fh * 0.08) / (fh * 1.15)) ** 2)
    lit = np.clip(1 - smooth((r - 0.55) / 0.75), 0, 1)[..., None]
    g = base.mean(axis=2, keepdims=True)
    dark = (g + (base - g) * 0.7) * 0.2
    spot = dark * (1 - lit) + base * lit
    t0 = round(a0 * FPS)
    k_this = round(TM.T["this"] * FPS) - t0
    wr = Writer(f"{CLIPS}/r_spot.mp4")
    for i in range(n):
        j = i - k_this
        if j < 0:
            fr = base
        elif j < 4:                                   # the white square on his face
            fr = base.copy()
            fr[by0:by1, bx0:bx1] = 250
        elif j < 6:                                   # the whole frame in negative
            fr = negative(base)
        elif j < 10:                                  # a small negative box over his face
            fr = base.copy()
            fr[by0:by1, bx0:bx1] = negative(base[by0:by1, bx0:bx1])
        elif j < 12:                                  # the room goes dark, the box still there
            fr = dark.copy()
            fr[by0:by1, bx0:bx1] = negative(base[by0:by1, bx0:bx1])
        else:                                         # only his face lit
            fr = spot
        wr.write(fr + grain(seed=2600 + i, amt=2.6))
    wr.close()


# Think School's "Founders vs Blackrock" (the user's file, 44 s on): one company's column at a time, centred on its
# own grey page, while BlackRock's black bar grows past the founder's
TS = f"{V3}/thinkschool.mp4"
# each column of the "Founders vs Blackrock" page: its time window (the BlackRock bar growing) and its box, measured
# on the frames (product image, label, bar and both legend lines; the legend ends at y 886)
TSG = {"tsg_nv": (39.20, 40.95, 961, 310, 905), "tsg_ap": (44.60, 46.50, 1385, 197, 905),
       "tsg_ms": (50.20, 52.10, 1566, 183, 906)}
TS_HALF, TS_SCALE = 235, 1.11          # one scale for all three, so the bars and legends match
TS_AREA = (40, 845)                    # centred above the caption line (captions sit on y 900)


def rest1_slot(name):
    for (key, nm, *_), ab in zip(SL.REST1, shot_bounds(SL.REST1, *TM.B["rest1"])):
        if nm == name:
            return ab
    raise KeyError(name)


def r_tsg(name):
    a, b = rest1_slot(name)
    n = nf(a, b)
    t0, t1, cx, y0, y1 = TSG[name]
    m = int((t1 - t0) * 25) + 2
    src = grab(TS, t0, m)
    x0, x1 = cx - TS_HALF, cx + TS_HALF
    ch, cw = y1 - y0, x1 - x0
    sw, sh = int(cw * TS_SCALE), int(ch * TS_SCALE)
    canvas = np.full((H, W, 3), 222, np.float32) + grain(seed=31, amt=1.4)
    edge = 36
    ramp = np.clip(np.minimum.outer(np.minimum(np.arange(sh), np.arange(sh)[::-1]),
                                    np.minimum(np.arange(sw), np.arange(sw)[::-1])) / edge, 0, 1)
    fm = ramp.astype(np.float32)[..., None]
    px, py = (W - sw) // 2, TS_AREA[0] + (TS_AREA[1] - TS_AREA[0] - sh) // 2
    wr = Writer(f"{CLIPS}/v3_{name}.mp4")
    for i in range(n):
        j = min(round(i * (m - 2) / max(1, n - 1)), len(src) - 1)
        crop = src[j][y0:y1, x0:x1].astype(np.float32)
        crop = cv2.resize(crop, (sw, sh), interpolation=cv2.INTER_CUBIC)
        fr = canvas.copy()
        fr[py:py + sh, px:px + sw] = fr[py:py + sh, px:px + sw] * (1 - fm) + crop * fm
        wr.write(fr)
    wr.close()
    print(f"   {name}: source {t0}-{t1}s into {n} frames")


TILE_PATS = [list("WWBWBBBWB"), list("BFWFWBWFB"), list("FFWFFFBFF")]   # the Nvidia reel's tile flash, 3 frames at 24


def tiles(fr, nxt, pat, gap=6):
    out = np.full((H, W, 3), 10, np.float32)
    tw, th = W // 3, H // 3
    for k, c in enumerate(pat):
        r, q = divmod(k, 3)
        x, y = q * tw + gap // 2, r * th + gap // 2
        if c == "W":
            out[y:y + th - gap, x:x + tw - gap] = 246
        elif c == "B":
            out[y:y + th - gap, x:x + tw - gap] = 6
        else:
            out[y:y + th - gap, x:x + tw - gap] = nxt[y:y + th - gap, x:x + tw - gap]
    return out


def flash_clip(out_name, frames_, nxt):
    """The Nvidia reel's opening on any clip: negatives on its 3rd and 5th frames (24 fps), then a tile flash into the
    next shot over the last three 24-fps frames."""
    n = len(frames_)
    last24 = int((n - 1) * 24 / FPS)
    wr = Writer(f"{CLIPS}/{out_name}.mp4")
    for i, fr in enumerate(frames_):
        f24 = int(i * 24 / FPS)
        if f24 in (2, 4):
            fr = negative(fr)
        t = f24 - (last24 - 2)
        if t >= 0 and nxt is not None:
            fr = tiles(fr, nxt, TILE_PATS[min(t, 2)])
        wr.write(fr)
    wr.close()


def first_frame(path):
    return frame_at(path, 0).astype(np.float32)


def r_jensen():
    """"Jensen Huang,": the Nvidia reel's own opening (its frames 0-24: Jensen on stage, its two negatives, its tile
    flash), the band above its burned-in caption, at the reel's 24 fps."""
    a, b = rest1_slot("r1_jensen")
    n = nf(a, b)
    src = grab(f"{V3}/nvidia_reel.mp4", 0.0, 26)
    wr = Writer(f"{CLIPS}/v3_r1_jensen.mp4")
    for i in range(n):
        j = min(int(i * 24 / FPS), len(src) - 1)
        fr = cv2.resize(src[j][0:540].astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
        fr = np.clip(fr + (fr - cv2.GaussianBlur(fr, (0, 0), 2.0)) * 0.6, 0, 255)
        wr.write(fr)
    wr.close()


def r_gates():
    a, b = rest1_slot("r1_gates")
    n = nf(a, b)
    fr = live(f"{V3}/bill_gates.mp4", 9.40, n, crop="crop=1186:667:90:0")   # the crop drops the CBS eye (bottom left)
    flash_clip("v3_r1_gates", fr[:n], first_frame(f"{CLIPS}/v3_tsg_ap.mp4"))


def r_jobs():
    a, b = rest1_slot("r1_jobs")
    n = nf(a, b)
    fr = live(f"{V3}/steve_jobs.mp4", 0.30, n)
    flash_clip("v3_r1_jobs", fr[:n], first_frame(f"{CLIPS}/rogan2.mp4"))


ROG_Z = (750, 973, 280, 1660)   # the Rogan clip's caption zone (rows, cols): its words end on row 972, the shirt's
                                # RAPTOR ENGINE starts on 970-973, the typing cursor on 767


def rogan_plate(frames, free):
    """A clean plate of the caption zone: the median of the frames without words (only the @genzcongress handle is
    on them; it never moves, so it is found on the plate itself and inpainted away there)."""
    z0, z1, x0, x1 = ROG_Z
    plate = np.median(np.stack([np.asarray(frames[k][z0:z1, x0:x1], np.float32) for k in free]), axis=0)
    pl = plate.mean(axis=2)
    loc = cv2.medianBlur(np.clip(pl, 0, 255).astype(np.uint8), 41).astype(np.float32)
    mx, mn = plate.max(axis=2), plate.min(axis=2)
    hm = ((pl - loc) > 22) & ((mx - mn) / (mx + 1) < 0.25)
    keep = np.zeros_like(hm)
    keep[100:180, 400:1000] = True              # the handle only: rows 850-930, cols 680-1280 of the frame
    hm = cv2.dilate((hm & keep).astype(np.uint8), np.ones((7, 7), np.uint8))
    ys, xs = np.nonzero(hm)
    print(f"   handle on the plate: rows {ys.min() + z0}-{ys.max() + z0}, cols {xs.min() + x0}-{xs.max() + x0}")
    plate = cv2.inpaint(np.clip(plate, 0, 255).astype(np.uint8), hm, 7, cv2.INPAINT_TELEA).astype(np.float32)
    return plate, hm


def rogan_core(z, plate):
    """The caption's own pixels in the zone: white / grey words (neutral, brighter than the plate: skin is saturated,
    so Elon's chin is never taken) and the black BLACKROCK'S (near black, darker than the plate)."""
    L, Lp = z.mean(axis=2), plate.mean(axis=2)
    mx, mn = z.max(axis=2), z.min(axis=2)
    white = (L > 118) & ((mx - mn) / (mx + 1) < 0.16) & (L - Lp > 40)
    black = (L < 12) & (Lp - L > 6) & (Lp < 60)   # the letters sit on curtain / shirt / mic, never on his neck
    return cv2.morphologyEx((white | black).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))


def rogan_skin(x):
    """Elon's neck: bright enough, orange (R > G > B, G above 0.45 R; the red curtain's G is ~0.15 R)."""
    r, g, bb = x[..., 0], x[..., 1], x[..., 2]
    return (x.mean(axis=2) > 45) & (r > g) & (g > bb) & (g > 0.45 * r)


def rogan_clean(fr, plate, hm, core):
    """`core` (grown 8 px) and the handle are refilled: from the clean plate on the curtain, mic and shirt; by
    inpainting this frame where his neck is (here or on the plate: it moves, so the plate's neck would not line up).
    Then the soft shade at the bottom for our caption."""
    z0, z1, x0, x1 = ROG_Z
    z = fr[z0:z1, x0:x1]
    m = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))) | hm
    nk = cv2.dilate((rogan_skin(z) | rogan_skin(plate)).astype(np.uint8), np.ones((15, 15), np.uint8))
    # every caption pixel is inpainted first (so nothing of a letter survives where the plate fades out at the
    # neck's edge); the plate then goes over everything that is not neck
    base = cv2.inpaint(np.clip(z, 0, 255).astype(np.uint8), m, 6, cv2.INPAINT_TELEA).astype(np.float32)
    mp = (m & (1 - nk)).astype(np.float32)
    mf = np.clip(cv2.GaussianBlur(mp, (0, 0), 3.0) * 1.5, 0, 1)[..., None]
    out = fr.copy()
    out[z0:z1, x0:x1] = base * (1 - mf) + plate * mf
    shade = (np.clip((np.arange(H) - 700) / 340, 0, 1) * 0.32)[:, None, None]
    return out * (1 - shade)


def r_rogan2():
    """Elon's question with its caption removed (ours goes on top, in the film's own type), then the user's one-second
    pause: Elon's silent second just before he asks (the same shot), muted. The words fade in through dark grey, so
    each frame takes the caption pixels of its neighbours too (4 before, 12 after): every word is gone from its first
    faint frame (the words stay up once in, and behind them is the clean plate either way)."""
    na = nf(*TM.B["rogan"])
    npz = nf(*TM.B["pause"])
    a = grab(f"{CLIPS}/rogan.mp4", 0.0, na)
    b = live(f"{DL}/rogan_elon.mp4", 11.30, npz, crop="crop=1048:590:16:664") if npz > 0 else []
    frames = list(a[:na]) + list(b[:npz])
    free = list(range(na, na + npz)) + list(range(0, 30)) + [na - 1]   # no words: the pause, the first half second
    plate, hm = rogan_plate(frames, free)
    z0, z1, x0, x1 = ROG_Z
    cores = [rogan_core(np.asarray(f, np.float32)[z0:z1, x0:x1], plate) for f in frames]
    wr = Writer(f"{CLIPS}/rogan2.mp4")
    for k, fr in enumerate(frames):
        if k < na:
            core = np.zeros_like(cores[0])
            for j in range(max(0, k - 4), min(na, k + 13)):
                core |= cores[j]
        else:
            core = cores[k]
        wr.write(rogan_clean(np.asarray(fr, np.float32), plate, hm, core))
    wr.close()


# ------------------------------------------------------------------ the Higgsfield scene (48.1-54.0 s, and 71.5 s)
# "But one bad bet cost him a $100 million loss. That was enough to get him thrown out of Wall Street.": the user's
# ChatGPT keyframes, animated on Higgsfield with Kling 3.0 Pro (5 s, 24 fps, silent; two takes each, the picks below).
HF = f"{V3}/higgsfield"
BET = {  # clip: (take, source start s, source end s, treatment) -- the source span is time-mapped onto the slot
    "bet1": ("shot1_b.mp4", 2.30, 4.98, None),     # the screens flip red at 2.8 / 3.8 / 4.8 s -> during "bad bet cost him"
    "bet2": ("shot2_a.mp4", 1.20, 3.30, "neg"),    # his head goes down; the Nvidia reel's two negative frames as it lands
    "bet3": ("shot3_b.mp4", 0.10, 3.60, "flash"),  # locked-off: he walks out of the doors and away into the red street
    "bet3fb": ("shot3_a.mp4", 1.40, 2.60, "grey"),  # "the one guy Wall Street threw out years ago": the walk-out again, grey
}


def rest2_slot(name):
    for (key, nm, *_), ab in zip(SL.REST2, shot_bounds(SL.REST2, *TM.B["rest2"])):
        if nm == name:
            return ab
    raise KeyError(name)


def r_bet():
    for name, (take, s0, s1, fx) in BET.items():
        a, b = rest2_slot(name)
        n = nf(a, b)
        src = grab(f"{HF}/{take}", 0.0, 121)
        wr = Writer(f"{CLIPS}/v3_{name}.mp4")
        for i in range(n):
            j = min(int((s0 + (s1 - s0) * i / n) * 24 + 1e-6), len(src) - 1)
            fr = cover(np.asarray(src[j], np.float32))
            if fx == "grey":                       # a memory: no colour, a little crushed
                g = fr @ np.float32([0.30, 0.59, 0.11])
                g = np.clip((g - 18) * 1.12, 0, 255)
                fr = np.repeat(g[..., None], 3, axis=2)
            fr = fr + grain(seed=4000 + 97 * len(name) + i, amt=3.0)   # film grain, so it sits with the real footage
            f24 = int(i * 24 / FPS)
            if fx == "neg" and f24 in (2, 4):
                fr = negative(fr)
            if fx in ("flash", "grey") and i < 3:   # cut in on a white flash
                w = (1.0, 0.55, 0.2)[i]
                fr = fr * (1 - w) + 255 * w
            wr.write(fr)
        wr.close()
        print(f"   {name}: {take} {s0}-{s1}s ({(s1 - s0) / (n / FPS):.2f}x) into {n} frames")


ALL.update({"cartel": r_cartel3, "spot": r_spot, "rogan2": r_rogan2, "jensen": r_jensen,
            "tsg": lambda: [r_tsg(k) for k in TSG], "gates": r_gates, "jobs": r_jobs, "bet": r_bet})


ALL["rest"] = rest_shots
ALL.update({"dimon": r_dimon3, "jpm": r_jpm, "solomon": r_solomon3, "ceo": r_ceo, "orbit": r_orbit3,
            "amongst": r_amongst})

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
