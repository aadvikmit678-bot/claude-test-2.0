#!/usr/bin/env python3
"""Pre-rendered beats of the hook (6.70-15.75 s), each frame-exact at 60 fps:

  r_tiles   "powerful people"  the Nvidia 3x3 tile flash resolving into nine panel members, a flash on each in turn,
                               then negatives, black blinks and the cyan bridge into the red card
  r_money   "a 60 trillion dollar"  the user's money animation keyed onto white, a new bill every 5 frames,
                               centre sharp / edges zoom-blurred, two negative pages
  r_cartel  "cartel"           the user's cartel background fixed; in its centre the eleven cut-outs, every face
                               on the same spot and size (match cuts), a 4-frame flipbook with a fisheye bulge
  r_weap    "weaponized capital"  the opal clip's tank: blueprint pages -> the tank firing -> B&W turret
  r_logos   "that owns a piece of everything"  company / ownership pages, centre focus
  r_touch   "you touch"        the touch clip's painting and pixel hands, the touch burst, white

The split-second glow after "you touch" and everything from "That's Jamie Dimon" on are built by prep_v2.py.

Run: <venv>/bin/python -I tools/prep_hook.py [names...]
"""
import sys

from common import *  # noqa: F401,F403
import timing as TM

RNG = np.random.default_rng(20261120)


def nframes(beat):
    a, b = TM.B[beat]
    return round(b * FPS) - round(a * FPS)


# ---------------------------------------------------------------- tiles
TILES = [  # (name, panel time of a 1 s close-up)
    ("dalio", 729.0), ("schwarzman", 2184.0), ("fraser", 1640.0),
    ("dimon", 916.0), ("fink", 1185.0), ("solomon", 2826.0),
    ("motsepe", 1816.0), ("shen", 2626.0), ("wikramanayake", 3007.0),
]


def tile_clip(t0, n, tw, th):
    fr = grab(PANEL, t0, n, fps=FPS)
    f = face(fr[0], 90)
    if f:
        x, y, w, h = f
        cx, cy, span = x + w / 2, y + h * 0.78, max(w * 3.4, 900)
    else:
        cx, cy, span = 960, 470, 1280
    cw = min(1920, span)
    ch = cw * th / tw
    x0 = int(min(max(cx - cw / 2, 0), 1920 - cw))
    y0 = int(min(max(cy - ch / 2, 0), 1080 - ch))
    out = []
    for im in fr:
        c = im[y0:int(y0 + ch), x0:int(x0 + cw)]
        out.append(grade(cv2.resize(c, (tw, th), interpolation=cv2.INTER_AREA), sat=0.92, contrast=1.08))
    return out


def r_tiles():
    n = nframes("tiles")  # 60
    G, tw, th = 6, 640 - 6, 360 - 6
    clips = [tile_clip(t, n, tw, th) for _, t in TILES]
    Wt, Bk, Fc = "W", "B", "F"
    pat = {  # Nvidia frames 15 / 16 / 17 (24 fps) at 60 fps
        0: [Wt, Wt, Bk, Wt, Bk, Bk, Bk, Wt, Bk],
        3: [Bk, Fc, Wt, Fc, Wt, Bk, Wt, Fc, Bk],
        6: [Fc, Fc, Wt, Fc, Fc, Fc, Bk, Fc, Fc],
        9: [Fc] * 9,
    }
    flashes = {4: 10, 0: 13, 8: 16, 2: 19, 6: 22, 1: 25, 7: 28, 3: 31, 5: 34}  # tile -> first frame
    env = [0.95, 0.62, 0.32, 0.14, 0.05]
    wr = Writer(f"{CLIPS}/r_tiles.mp4")
    state = pat[0]
    for i in range(n):
        if i in pat:
            state = pat[i]
        fr = np.full((H, W, 3), 10, np.float32)
        for k in range(9):
            r, c = divmod(k, 3)
            x, y = c * 640 + G // 2, r * 360 + G // 2
            if state[k] == "W":
                tile = np.full((th, tw, 3), 246, np.float32)
            elif state[k] == "B":
                tile = np.full((th, tw, 3), 6, np.float32)
            else:
                tile = clips[k][min(i, len(clips[k]) - 1)].copy()
                j = i - flashes[k]
                if 0 <= j < len(env):
                    tile = tile * (1 + 0.6 * env[j]) + 255 * env[j] * 0.85
            fr[y:y + th, x:x + tw] = tile
        if 40 <= i <= 42 or 53 <= i <= 55:
            fr = 255 - np.clip(fr, 0, 255)
        elif i in (49, 50, 52):
            fr[:] = 0
        elif i >= 56:
            fr[:] = (95, 255, 255)
        wr.write(fr)
    wr.close()


# ---------------------------------------------------------------- money
def key_bill(img):
    """The money asset's bill corners on black velvet -> RGBA (paper kept, ink holes filled)."""
    L = img.astype(np.float32).mean(axis=2) / 255
    Lb = cv2.GaussianBlur(L, (0, 0), 2.0)
    m = (Lb > 0.33).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    h, w = m.shape
    ff = m.copy()
    msk = np.zeros((h + 2, w + 2), np.uint8)
    for (sx, sy) in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)):
        if ff[sy, sx] == 0:
            cv2.floodFill(ff, msk, (sx, sy), 2)
    m = np.where(ff == 0, 1, m).astype(np.uint8)  # enclosed dark ink -> part of the bill
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        m = (lab == big).astype(np.uint8)
    a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.1)
    return np.dstack([img, (a * 255).astype(np.uint8)])


def money_page(src_rgba, k, dx, dy, white=246.0):
    al = src_rgba[..., 3] > 128
    ys, xs = np.where(al)
    cx, cy = ((xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2) if len(xs) else (368, 207)
    bill = affine(src_rgba, k, cx, cy, W / 2 + dx, H / 2 + dy)
    a = bill[..., 3:4].astype(np.float32) / 255
    sh = cv2.GaussianBlur(a[..., 0], (0, 0), 16)[..., None]
    sh = np.roll(np.roll(sh, 14, axis=0), 8, axis=1)
    page = np.full((H, W, 3), white, np.float32) * (1 - 0.22 * sh)
    page = page * (1 - a) + bill[..., :3].astype(np.float32) * a
    return page


def r_money():
    n = nframes("money")  # 86
    src = f"{DL}/money_asset.mp4"
    shots = [s * 6 for s in range(16) if s != 2]  # shot 2 (Jackson's portrait at the edge) keys badly
    pages, k = [], 0
    while sum(len(p) for p in pages) < n:
        pages.append([k % len(shots)] * 5)
        k += 1
    wr = Writer(f"{CLIPS}/r_money.mp4")
    i = 0
    for pi, p in enumerate(pages):
        s0 = shots[p[0]]
        a, b = key_bill(frame_at(src, s0 + 2, 24)), key_bill(frame_at(src, s0 + 3, 24))
        kk = 2.25 * (1 + RNG.uniform(-0.05, 0.05))
        dx, dy = RNG.uniform(-50, 50), RNG.uniform(-30, 30)
        for j in range(5):
            if i >= n:
                break
            page = money_page(a if j < 3 else b, kk * (1 + 0.006 * j), dx, dy)
            fr = center_focus(page, r0=360, r1=840, zoom=0.014)
            if pi in (6, 12):
                fr = 255 - fr
            wr.write(fr + grain(seed=i, amt=5))
            i += 1
    wr.close()


# ---------------------------------------------------------------- cartel
CARTEL_ORDER = [  # (name, cut-out png or webm@frame, frames on screen)
    ("schwarzman", "stephen_schwarzman_cut.png", 4), ("fraser", "jane_fraser_cut.png", 4),
    ("dalio", "ray_dalio_cut.png", 4), ("motsepe", "patrice_motsepe_cut.png", 3),
    ("quinn", "noel_quinn_cut.png", 4), ("wikramanayake", "shemara_wikramanayake_cut.png", 3),
    ("shen", "neil_shen_cut.png", 4), ("alrumayyan", "alrumayyan_cut.png", 3),
    ("solomon", "david_solomon_cut.png", 3), ("dimon", "jamie_cut.png", 3), ("fink", "fink_cut.webm", 4),
]
FACE_W, FACE_C = 400, (960, 445)
FACE_OVERRIDE = {"alrumayyan_cut.png": (721, 270, 310, 310)}  # the headdress hides his face from the detector
# measured on the guide sheet (eyes 150 px apart at (960, 405)): (scale, dx, dy) to even out the detector's misses
CORR = {"stephen_schwarzman_cut.png": (0.96, 0, 0), "noel_quinn_cut.png": (0.68, 0, 0), "jamie_cut.png": (1.03, 0, 0),
        "jane_fraser_cut.png": (1.16, 0, 0),
        "fink_cut.webm": (0.76, 0, 8), "patrice_motsepe_cut.png": (1.0, 44, 0), "alrumayyan_cut.png": (1.1, 0, 0)}


def load_cut(name):
    if name.endswith(".webm"):
        return grab(f"{CUT}/{name}", 0.2, 1, alpha=True)[0]
    return np.asarray(Image.open(f"{CUT}/{name}").convert("RGBA"))


EYES = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
EYE_D, EYE_C = 150, (960, 405)  # every face: eyes 150 px apart, their midpoint at (960, 405)


def eyes(img, f):
    """Midpoint and distance of the two eyes inside face box f, or None."""
    x, y, w, h = f
    roi = cv2.cvtColor(np.ascontiguousarray(img[y:y + h // 2 + h // 10, x:x + w]), cv2.COLOR_RGB2GRAY)
    roi = cv2.equalizeHist(roi)
    es = EYES.detectMultiScale(roi, scaleFactor=1.05, minNeighbors=5, minSize=(max(12, w // 10), max(12, w // 10)))
    es = sorted(es, key=lambda e: -e[2] * e[3])[:4]
    best = None
    for i in range(len(es)):
        for j in range(i + 1, len(es)):
            (x1, y1, w1, h1), (x2, y2, w2, h2) = es[i], es[j]
            c1 = (x + x1 + w1 / 2, y + y1 + h1 / 2)
            c2 = (x + x2 + w2 / 2, y + y2 + h2 / 2)
            d = math.hypot(c1[0] - c2[0], c1[1] - c2[1])
            if 0.25 * w < d < 0.6 * w and abs(c1[1] - c2[1]) < 0.12 * w:
                if best is None or abs(d - 0.4 * w) < abs(best[2] - 0.4 * w):
                    best = ((c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2, d)
    return best


def aligned_cut(name, face_w=FACE_W, fc=FACE_C, fade=150):
    rgba = load_cut(name)
    probe_img = over(np.full(rgba.shape[:2] + (3,), 128, np.uint8), rgba).astype(np.uint8)
    f = FACE_OVERRIDE.get(name) or face(probe_img, 60)
    if not f:
        raise SystemExit(f"no face in {name}")
    x, y, w, h = f
    cs, cdx, cdy = CORR.get(name, (1.0, 0, 0))
    e = eyes(probe_img, f)
    if e:
        ex, ey, d = e
        out = affine(rgba, EYE_D / d * cs, ex, ey, EYE_C[0] + cdx, EYE_C[1] + cdy)
        f = (x, y, w, h, "eyes", round(ex), round(ey), round(d))
    else:
        k = face_w / w * cs
        out = affine(rgba, k, x + w / 2, y + h * 0.42, EYE_C[0] + cdx, EYE_C[1] + cdy)
        f = (x, y, w, h, "box")
    al = out[..., 3].astype(np.float32)
    rows = np.where(al.max(axis=1) > 20)[0]
    if len(rows) and rows[-1] < H - 4:  # the photo ends above the frame: fade its bottom edge out
        yb = rows[-1]
        yy = np.arange(H, dtype=np.float32)[:, None]
        al *= np.clip((yb - yy) / fade, 0, 1)
        out[..., 3] = al.astype(np.uint8)
    return out, f


def r_cartel():
    n = nframes("cartel")  # 39
    bg0 = np.asarray(Image.open(f"{CART}/cartel_background.png").convert("RGB"))
    cuts = []
    for name, f, d in CARTEL_ORDER:
        c, box = aligned_cut(f)
        print(f"   {name}: face {box}")
        cuts += [c] * d
    assert len(cuts) == n, (len(cuts), n)
    wr = Writer(f"{CLIPS}/r_cartel.mp4")
    for i in range(n):
        bg = cover(bg0, scale=1.0 + 0.025 * i / n)
        c = cuts[i]
        fr = over(bg, c)
        fr = grade(fr, sat=0.92, contrast=1.06)
        fr = barrel(fr.astype(np.float32), 960, 470, 600, 0.16)
        fr = center_focus(fr, cx=960, cy=470, r0=420, r1=900, zoom=0.012)
        new = i == 0 or cuts[i] is not cuts[i - 1]
        if new:  # each new face lands with a hint of exposure
            fr = fr * 1.06 + 8
        wr.write(fr + grain(seed=100 + i, amt=4))
    wr.close()


# ---------------------------------------------------------------- weaponized
OPAL = f"{DL}/opal_weaponized.mp4"


def opal_page(f, k=1.45):
    p = frame_at(OPAL, f, 30)
    page = np.full((H, W, 3), 250, np.float32)
    big = cv2.resize(p, (round(720 * k), round(1280 * k)), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    bh, bw = big.shape[:2]
    y0 = (bh - H) // 2
    crop = big[y0:y0 + H]
    x0 = (W - bw) // 2
    # fade the page's left/right edges into the white canvas
    ramp = np.clip(np.minimum(np.arange(bw), bw - 1 - np.arange(bw)) / 60.0, 0, 1)[None, :, None]
    page[:, x0:x0 + bw] = page[:, x0:x0 + bw] * (1 - ramp) + crop * ramp
    return page


def opal_page_band(f):
    """The vertical page cropped to a horizontal 16:9 band (720x405) where its drawing is densest, filling the frame
    (the user: crop the vertical video to horizontal, no white sides)."""
    p = frame_at(OPAL, f, 30)
    ink = (p.astype(np.float32).mean(axis=2) < 140).sum(axis=1)
    top = max(range(0, 1280 - 405, 5), key=lambda y: ink[y:y + 405].sum())
    band = p[top:top + 405]
    up = cv2.resize(band, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    blur = cv2.GaussianBlur(up, (0, 0), 1.4)
    return np.clip(up * 1.6 - blur * 0.6, 0, 255)


def opal_band(f, yc):
    p = frame_at(OPAL, f, 30)
    y0 = int(min(max(yc - 202, 0), 1280 - 405))
    band = p[y0:y0 + 405]
    up = cv2.resize(band, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    blur = cv2.GaussianBlur(up, (0, 0), 1.6)
    return np.clip(up * 1.7 - blur * 0.7, 0, 255)  # unsharp


def r_weap():
    n = nframes("weap")  # 65
    t0 = round(TM.B["weap"][0] * FPS)
    ized = round(TM.T["ized"] * FPS) - t0       # cut to the live tank
    cap = round(TM.T["capital"] * FPS) - t0     # cut to the turret
    seq = []
    for f in (95, 98, 100, 102, 105):            # blueprint pages (top view, side views, M4A3, Tiger), 3 frames each
        pg = center_focus(opal_page_band(f), r0=380, r1=880, zoom=0.012)  # a 16:9 band of the page, filling the frame
        seq += [pg] * 3
    seq = seq[:ized] + [seq[-1]] * max(0, ized - len(seq))
    live = []
    for j in range(cap - ized):                  # the tank firing, source 30 fps -> 2 output frames each
        f = 108 + j // 2
        live.append(opal_band(f, 660))
    for j in range(2, 4):                        # the blast: a 2-frame negative
        if j < len(live):
            live[j] = 255 - live[j]
    turret = []
    for j in range(n - cap):
        f = 131 + j // 2
        im = opal_band(f, 560)
        k = 1.0 + 0.05 * j / max(1, n - cap)
        turret.append(affine(im, k, W / 2, H / 2, W / 2, H / 2, border=(0, 0, 0)))
    frames = seq + live + turret
    wr = Writer(f"{CLIPS}/r_weap.mp4")
    for i, fr in enumerate(frames[:n]):
        wr.write(np.asarray(fr, np.float32) + grain(seed=200 + i, amt=6))
    wr.close()


# ---------------------------------------------------------------- logos
GE, BV, BR = f"{DL}/good_edit_42s.mp4", f"{DL}/blackrock_video.mp4", f"{DL}/blackrock_reel.mp4"
LOGO_PAGES = [  # (source, time, kind, band centre y for portrait sources, frames)
    (GE, 34.30, "sq", 0, 6), (GE, 35.10, "sq", 0, 6), (GE, 35.75, "sq", 0, 6), (BV, 0.40, "band", 960, 6),
    (GE, 36.20, "sq", 0, 6), (GE, 37.75, "sq", 0, 6), (BV, 1.40, "band", 960, 5), (GE, 48.35, "sq", 0, 5),
    (GE, 49.10, "sq", 0, 5), (BR, 7.00, "band", 330, 6), (BR, 8.30, "band", 330, 6), (BV, 21.50, "band", 960, 5),
    (BR, 13.00, "band", 470, 8),
]


def logo_page(src, t, kind, yc):
    im = grab(src, t, 1)[0]
    if kind == "sq":
        im = im.copy()
        im[985:1080, 0:150] = np.median(im[930:985, 0:150].reshape(-1, 3), axis=0)  # the 'tfg' watermark
        page = np.full((H, W, 3), 0, np.float32)
        edge = np.median(np.concatenate([im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)]), axis=0)
        page[:] = edge
        x0 = (W - 1080) // 2
        page[:, x0:x0 + 1080] = im
        return page
    y0 = int(min(max(yc - 304, 0), 1920 - 608))
    band = im[y0:y0 + 608]
    up = cv2.resize(band, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    blur = cv2.GaussianBlur(up, (0, 0), 1.4)
    return np.clip(up * 1.5 - blur * 0.5, 0, 255)


def r_logos():
    n = nframes("logos")  # 98
    total = sum(p[4] for p in LOGO_PAGES)
    assert total == n, (total, n)
    wr = Writer(f"{CLIPS}/r_logos.mp4")
    i = 0
    for pi, (src, t, kind, yc, d) in enumerate(LOGO_PAGES):
        page = logo_page(src, t, kind, yc)
        for j in range(d):
            k = 1.0 + 0.012 * j
            im = affine(page.astype(np.float32), k, W / 2, H / 2, W / 2, H / 2)
            fr = center_focus(im, r0=430, r1=930, zoom=0.012)
            if pi == 8:
                fr = 255 - fr
            wr.write(fr + grain(seed=300 + i, amt=4))
            i += 1
    wr.close()


# ---------------------------------------------------------------- touch
TOUCH = f"{DL}/touch_rawcanvas.mp4"


def r_touch():
    """The touch clip's hands (the user: the two hands coming together, then touching; extended): the Creation of
    Adam pushing in, then the clip's pixel hands sliding together so the fingertips meet exactly on "touch", then
    the clip's own touch burst, then white. The clip's "A year ago" text frames are not used."""
    n = nframes("touch")  # 53
    t0 = round(TM.B["touch"][0] * FPS)
    k_touch = round(TM.T["touch"] * FPS) - t0              # the frame the fingertips meet
    seq = []
    paint = cover(frame_at(TOUCH, 1, 24).astype(np.float32))
    n_paint = 16
    for j in range(n_paint):
        seq.append(affine(paint, 1.0 + 0.07 * j / n_paint, 980, 330, 980, 330))
    hands = cover(frame_at(TOUCH, 0, 24).astype(np.float32))
    # a clean plate of the clip's own dark pixel-grid background (the hand-free middle strip, tiled), so the hands
    # slide over the same texture with no black seam between them
    strip = hands[:, 922:992]                               # the empty middle (no lit pixels there)
    plate = np.concatenate([strip] * (W // strip.shape[1] + 1), axis=1)[:, :W]
    lum = cv2.GaussianBlur(hands.mean(axis=2), (0, 0), 1.2)
    mask = np.clip((lum - 34) / 40, 0, 1)[..., None]       # the lit pixels of the hands
    left_m, right_m = mask.copy(), mask.copy()
    left_m[:, 960:] = 0
    right_m[:, :960] = 0
    n_app = k_touch - n_paint
    for j in range(n_app):
        u = smooth((j + 1) / n_app)
        d = 170 - 215 * u                                   # 170 px apart each side -> 45 px past: the tips meet
        fr = plate.copy()
        for m, dx in ((left_m, -d), (right_m, d)):
            M = np.float32([[1, 0, dx], [0, 1, 0]])
            hs = cv2.warpAffine(hands, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            ms = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)[..., None]
            fr = fr * (1 - ms) + hs * ms
        seq.append(fr)
    burst = [cover(frame_at(TOUCH, f, 24).astype(np.float32)) for f in (21, 22, 23, 24, 25)]
    n_burst = n - len(seq) - 4
    for j in range(n_burst):
        seq.append(burst[min(len(burst) - 1, j * len(burst) // n_burst)])
    seq += [np.full((H, W, 3), 252, np.float32)] * 4
    assert len(seq) == n, (len(seq), n)
    wr = Writer(f"{CLIPS}/r_touch.mp4")
    for i, fr in enumerate(seq):
        wr.write(fr + grain(seed=400 + i, amt=4))
    wr.close()


# ---------------------------------------------------------------- these
def r_these():
    """"These are the most powerful people": the panel from high up, Nvidia's opening negatives on frames 2 and 4
    (24 fps) = 60 fps frames 3-4 and 8-9 after "These", a slow push."""
    n = nframes("these")  # 61
    fr = grab(f"{CLIPS}/p_these.mp4", 0.0, n, fps=FPS)
    t0 = round(TM.B["these"][0] * FPS)
    k0 = round(TM.T["these"] * FPS) - t0  # "These" lands 3 frames in
    wr = Writer(f"{CLIPS}/r_these.mp4")
    for i in range(n):
        im = affine(fr[min(i, len(fr) - 1)].astype(np.float32), 1.03 + 0.05 * i / n, W / 2, H * 0.55, W / 2, H * 0.55,
                    border=(0, 0, 0))
        if i - k0 in (0, 1, 5, 6):
            im = 255 - im
        wr.write(im + grain(seed=600 + i, amt=4))
    wr.close()


ALL = {"these": r_these, "tiles": r_tiles, "money": r_money, "cartel": r_cartel, "weap": r_weap, "logos": r_logos,
       "touch": r_touch}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
