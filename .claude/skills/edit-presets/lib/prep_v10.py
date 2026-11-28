"""Trimmed from blackrock-open/tools/prep_v10.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import sys

from common import *  # noqa: F401,F403

import timing as TM

V10 = f"{DL}/v10"

PIN = os.path.abspath(f"{REPO}/dimon-src/money_pinterest videos")

DIR = os.path.abspath(f"{REPO}/dimon-src/_direct")

T, B, F = TM.T, TM.B, TM.F

FINK_IN = F(T["powerful"] - TM.LEAD)          # the Fink frame lands on "powerful" (the reel: its subject at 1.0 s)

SRC = {
    "FIN": f"{DL}/fink_interview.mp4", "LFI": f"{DL}/lf_interview2.mp4", "FSP": f"{DL}/fink_speaking.mp4",
    "MF1": f"{DL}/m_fink1.mp4", "MF2": f"{DL}/m_fink2.mp4", "FE2": f"{DL}/fink_edit2.mp4",
    "FE3": f"{DL}/fink_edit3.mp4", "EYE": f"{PIN}/eye.mp4", "FC": f"{V10}/fast_cinematic.mp4",
    "CASH": f"{PIN}/From Klickpin.com- Try these 11 Classy side hustle ideas that can help you create a more curated "
            f"classy and Pinterest-worthy result for beginners.mp4",
    "FED": f"{PIN}/From Klickpin.com- Stylish entryway makeover ideas for your next inspiration board with stylish "
           f"details that feel current without trying too hard-.mp4",
    "CHESS": f"{PIN}/pint videos.mp4",
    "RUN": f"{PIN}/From Klickpin.com- Relaxed shell-toned style ideas for people who love beauty on a budget for "
           f"endless summer vibes-pin-id-376121006396995349.mp4",
    "FIRE": f"{PIN}/From Klickpin.com- Explore Modern rustic wedding decor for your next inspiration board with simple "
            f"details that elevate the final look-pin-id-9615.mp4",
    "MONEY": f"{PIN}/money can be used in difference effect in bg less opacity. bklend.mp4",
    "HOW": f"{DIR}/how_jpm_became_largest.mp4", "ASH": f"{DL}/v3/new/asher.mp4",
    "GE": f"{DL}/good_edit_42s.mp4", "FG": f"{DL}/fiscalgrind.mp4", "XEX": f"{DL}/v3/br_explainer.mp4",
    "BRS": f"{DL}/blackrock_short.mp4", "BR15": f"{DL}/v6/docs/br_15t_machine.mp4",
    "BRC": f"{DL}/v6/docs/br_conspiracies.mp4", "C618": f"{V10}/cin_618.mp4", "CMJ": f"{V10}/cin_midjourney.mp4",
    "COPP": f"{V10}/cin_opportunities.mp4", "CPIN": f"{V10}/cin_pinterest.mp4", "BRL": f"{DL}/v6/docs/br_largest.mp4", "FLAG": f"{V10}/usa_flag.mp4",
}

def nf(a, b):
    return round(b * FPS) - round(a * FPS)

# ------------------------------------------------------------------ the Fink frame's plates
FW, FH = 2200, 1238                     # the plates' canvas: the frame is its middle 1920x1080

FX0, FY0 = (FW - W) // 2, (FH - H) // 2

PHOTO_S = 1.0                           # the user's photo (1536x1024) at full size, bottom on the canvas's bottom edge

def fink_place():
    pw, ph = round(1536 * PHOTO_S), round(1024 * PHOTO_S)
    return (FW - pw) // 2, FH - ph, pw, ph

def r_built():
    """"built.": the reel's NOISE frame (a dark black-and-white shot, a light behind the word): BlackRock's tower with
    its flags and its sign (the explainer's 111.2 s, no channel logo), black and white, dark"""
    a0, a1 = F(T["built"] - TM.LEAD), B["built"][1]
    n = nf(a0, a1)
    frs = grab(SRC["XEX"], 111.2, n, fps=FPS)
    wr = Writer(f"{CLIPS}/v10_built.mp4")
    for i in range(n):
        fr = cover(frs[min(i, len(frs) - 1)].astype(np.float32), scale=1.04)
        g = fr @ np.float32([0.299, 0.587, 0.114])
        g = np.clip((g - 128) * 1.2 + 78, 0, 255)
        fr = vignette(np.repeat(g[..., None], 3, axis=2), strength=0.45)
        wr.write(fr + grain(seed=6300 + i, amt=5))
    wr.close()
    print(f"   built: {n} frames (the explainer's tower, 111.2 s, black and white)")

# ------------------------------------------------------------------ "It holds more of Nvidia than Jensen Huang ...":
# the v6/v8 founders block, as the user asked to have it back (Nov 24): Think School's "Founders vs Blackrock" column
# for each company, then the founder in the Nvidia reel's opening treatment (Jensen: the reel's own clip), each slot
# re-cut on the new recording's words; then v4's texture pass (corner blur, no money overlay)
def founder_slots():
    L = lambda k: F(T[k] - TM.LEAD)
    ks = [L("it"), L("jensen"), L("more2"), L("bill"), L("and"), L("steve"), TM.OPEN_END]
    names = ["tsg_nv", "r1_jensen", "tsg_ms", "r1_gates", "tsg_ap", "r1_jobs"]
    return {nm: (a, b) for nm, a, b in zip(names, ks, ks[1:])}

STEP = 5                       # frames a wall state holds (12 fps)

# ---- the Fink frame (v11): the user's photo of Fink cut out, over a BlackRock building shot, blurred, dark and textured
BGW, BGH = 2208, 1242                    # the background video's canvas (the frame zooms below 1.0)

def screen_lines(w):
    return (1.0 - 0.07 * (np.arange(w) % 3 == 0).astype(np.float32))[None, :, None]

def fink_cut2():
    """the cut-out on the 2200x1238 canvas (photo at (332, 214)), with the screen's fine lines; no plates"""
    cut = np.asarray(Image.open(f"{V10}/larry_new_cut.png").convert("RGBA")).astype(np.float32)
    px, py, pw, ph = fink_place()
    cut_s = cv2.resize(cut, (pw, ph), interpolation=cv2.INTER_AREA)
    cutc = np.zeros((FH, FW, 4), np.float32)
    cutc[py:py + ph, px:px + pw] = cut_s
    cutc[..., :3] *= screen_lines(FW)
    save_png(cutc, f"{IMG}/v10_fink_cut.png")
    return cutc

def bg_frame(im, phase, i):
    """a BlackRock shot as the Fink frame's background: blurred, dark, textured; phase 2 warmer with a glow at the sides"""
    im = im.astype(np.float32)
    h, w = im.shape[:2]
    k = max(BGW / w, BGH / h) * 1.22                         # cropped in: clear of the channel logos
    big = cv2.resize(im, (round(w * k), round(h * k)), interpolation=cv2.INTER_CUBIC)
    oy, ox = (big.shape[0] - BGH) // 2 + int(0.04 * big.shape[0]), (big.shape[1] - BGW) // 2
    fr = cv2.GaussianBlur(big[oy:oy + BGH, ox:ox + BGW], (0, 0), 9)
    g = fr @ np.float32([0.299, 0.587, 0.114])
    if phase == 1:
        fr = (g[..., None] * 0.75 + fr * 0.25) * np.float32([0.92, 0.97, 1.08]) * 0.42
    else:
        fr = (g[..., None] * 0.55 + fr * 0.45) * np.float32([1.10, 0.95, 0.80]) * 0.48
        yy, xx = np.mgrid[0:BGH, 0:BGW].astype(np.float32)
        for sx in (0.0, BGW):
            r = np.sqrt(((xx - sx) / 700) ** 2 + ((yy - BGH * 0.60) / 640) ** 2)
            fr += np.float32([255, 135, 55]) * (0.36 * np.exp(-r * r * 2.2))[..., None]
    fr = fr * screen_lines(BGW)
    return fr + grain(BGH, BGW, seed=8800 + i, amt=5)

def tile_still(key, t, cx, cy, zoom, tw, th, look):
    im = grab(SRC[key], t, 1)[0].astype(np.float32)
    h, w = im.shape[:2]
    ar = tw / th
    cw = min(w, h * ar) * zoom
    ch = cw / ar
    x0 = int(min(max(cx * w - cw / 2, 0), w - cw))
    y0 = int(min(max(cy * h - ch / 2, 0), h - ch))
    crop = im[y0:int(y0 + ch), x0:int(x0 + cw)]
    out = cv2.resize(crop, (tw, th), interpolation=cv2.INTER_AREA if cw > tw else cv2.INTER_CUBIC)
    if look == "bw":
        g = out @ np.float32([0.299, 0.587, 0.114])
        out = np.repeat(((g - 128) * 1.12 + 128)[..., None], 3, axis=2)
    elif look == "green":                                    # the reel's banknote, tinted green
        g = out @ np.float32([0.299, 0.587, 0.114])
        out = np.stack([g * 0.78, np.clip(g * 1.08 + 12, 0, 255), g * 0.70], axis=2)
    else:
        out = grade(out, sat=1.0, contrast=1.06)
    return np.clip(out, 0, 255)

def fink_plates3():
    """the Fink frame's two backgrounds as photos (v12): before "Earth" BlackRock's entrance on the street, after it the
    tower with its flags and sign, each blurred, dark and textured; the second warmer with a glow at the sides"""
    for name, key, t, phase in (("v12_bg_a", "ASH", 10.30, 1), ("v12_bg_b", "XEX", 111.0, 2)):
        fr = bg_frame(grab(SRC[key], t, 1)[0], phase, 0)
        save_jpg(cv2.resize(fr, (FW, FH), interpolation=cv2.INTER_AREA), f"{IMG}/{name}.jpg", q=94)
    print("   plates: v12_bg_a.jpg, v12_bg_b.jpg")

# ============================================================================== v14: "cost him $100 million loss."
# The Kalanick reel's year counter (19.2-20.8 s, read frame by frame): one reel frame of soft white, the first year
# sharp for one frame, then the years roll up through a band -- the old one leaving upwards, the next coming from
# below, smeared vertically with the speed -- fast first and slowing, the last one settling with the old one's edge
# still showing at the top of the band; it holds, then slides out to the left. Every change on the reel's 10-12 fps.
# Ours: "$1 million" rolling up to "$100 million" over the user's money clip (dark, textured), "loss." blooming in under
# it on the word.
ISF = f"{ROOT}/assets/fonts/InstrumentSerif-Regular.woff2"

LOSS_TEXT = "$100 million loss."                 # (v17: "$100 million loss" -- no full stops, the user)

COUNT_VALUES = ["$1", "$7", "$18", "$31", "$46", "$60", "$73", "$84", "$92", "$97", "$100"]

def text_mask(text, path, size, track=-0.045):
    f = ImageFont.truetype(path, size)
    widths = [f.getlength(ch) for ch in text]
    tw = int(sum(widths) + track * size * (len(text) - 1)) + 40
    im = Image.new("L", (tw, int(size * 1.35)), 0)
    d = ImageDraw.Draw(im)
    x = 20
    for ch, w in zip(text, widths):
        d.text((x, int(size * 0.08)), ch, fill=255, font=f)
        x += w + track * size
    a = np.asarray(im).astype(np.float32) / 255.0
    cols = np.where(a.max(axis=0) > 0.02)[0]
    return a[:, cols.min():cols.max() + 1]

def glow_white(base, a, k_glow=1.0, bloom=0.0):
    """white type with a white halo (a soft one, wider and brighter when it blooms)"""
    g1 = cv2.GaussianBlur(a, (0, 0), 6 + 10 * bloom)
    g2 = cv2.GaussianBlur(a, (0, 0), 22 + 40 * bloom)
    halo = np.clip(0.55 * g1 + 0.35 * g2, 0, 1) * (k_glow + 1.4 * bloom)
    out = base * (1 - np.clip(halo, 0, 0.9)[..., None]) + 255 * np.clip(halo, 0, 0.9)[..., None]
    return out * (1 - a[..., None]) + np.float32([248, 244, 236]) * a[..., None]

def r_count():
    t0 = F(TM.RT("cost") - TM.LEAD)
    t1 = F(TM.R(TM.ALIGN["rest"][50]["start"]) - TM.LEAD)             # the cut to "That was enough"
    n = nf(t0, t1)
    t_land = TM.R(TM.ALIGN["rest"][48]["start"]) - 0.03             # "million": the counter has landed
    t_loss = TM.R(TM.ALIGN["rest"][49]["start"]) - 0.03             # "loss."
    size = 250
    masks = [text_mask(f"{v} million", ISF, size) for v in COUNT_VALUES]
    full = text_mask(LOSS_TEXT, ISF, size)
    cut_x = masks[-1].shape[1] + int(0.10 * size)             # where "loss." starts in the full line
    L = int(size * 1.08)                                            # the roll's step: one line
    cy = 470                                                        # the number line's centre
    band = (cy - int(0.62 * L), cy + int(0.62 * L))
    bg_src = grab(SRC["COPP"], 0.1, (n + STEP - 1) // STEP + 2, fps=12)
    lines = screen_lines(W)
    N = len(COUNT_VALUES) - 1
    t_roll = t0 + 2 * STEP / FPS                                     # the white frame, then "$1 million" sharp
    wr = Writer(f"{CLIPS}/v14_count.mp4")
    prev = None
    for i in range(n):
        st = i // STEP                                              # the 12 fps step
        ts = t0 + st * STEP / FPS
        bg = cover(bg_src[min(st, len(bg_src) - 1)].astype(np.float32))
        g = bg @ np.float32([0.299, 0.587, 0.114])
        bg = (g[..., None] * 0.35 + bg * 0.65) * 0.50
        bg = vignette(bg * lines, strength=0.40)
        if st == 0:                                                 # the reel's soft white frame
            fr = cv2.GaussianBlur(bg, (0, 0), 20) * 0.25 + 205
            wr.write(fr + grain(seed=9100 + st, amt=4))
            continue
        u = min(1.0, max(0.0, (ts - t_roll) / max(0.1, t_land - t_roll)))
        pos = N * (1 - (1 - u) ** 3)
        u2 = min(1.0, max(0.0, (ts + STEP / FPS - t_roll) / max(0.1, t_land - t_roll)))
        speed = N * ((1 - (1 - u) ** 3) - 0)                         # (placeholder, replaced below)
        speed = abs(N * (1 - (1 - u2) ** 3) - pos)                  # values per step
        k0 = int(np.floor(pos))
        frac = pos - k0
        canvas = np.zeros((H, W), np.float32)
        for k, off in ((k0, -frac * L), (min(N, k0 + 1), (1 - frac) * L)):
            if k0 >= N and k != k0:
                continue
            m = masks[k]
            mh, mw = m.shape
            x0 = (W - mw) // 2
            y0 = int(cy - mh / 2 + off)
            ys0, ys1 = max(0, y0), min(H, y0 + mh)
            if ys1 > ys0:
                canvas[ys0:ys1, x0:x0 + mw] = np.maximum(canvas[ys0:ys1, x0:x0 + mw], m[ys0 - y0:ys1 - y0])
        blur = int(min(140, speed * L * 0.9))                       # the roll's vertical smear
        if blur > 2:
            ker = np.full((blur, 1), 1.0 / blur, np.float32)
            canvas = cv2.filter2D(canvas, -1, ker)
        yy = np.arange(H, dtype=np.float32)[:, None]
        bm = np.clip(np.minimum(yy - band[0], band[1] - yy) / 18.0, 0, 1)      # clipped to the band, soft edges
        canvas *= bm
        # "loss." on the same line (the user: "$100 million loss." in one line): the line re-centres and "loss."
        # blooms in at its end
        bloom = 0.0
        if ts >= t_loss - 1e-6:
            canvas = np.zeros((H, W), np.float32)
            mh, mw = full.shape
            x0, y0 = (W - mw) // 2, int(cy - mh / 2)
            lpart = full.copy()
            lpart[:, :cut_x] = 0
            fpart = full - lpart
            if ts < t_loss + STEP / FPS:
                bloom = 1.0
                lpart = cv2.GaussianBlur(lpart, (0, 0), 7)
            canvas[y0:y0 + mh, x0:x0 + mw] = np.maximum(fpart, lpart)
        a = canvas
        # the exit: the last two steps slide to the left
        steps_left = (n - 1) // STEP - st
        if steps_left <= 1:
            dx = -340 if steps_left == 1 else -980
            M = np.float32([[1, 0, dx], [0, 1, 0]])
            a = cv2.warpAffine(a, M, (W, H))
            a = cv2.filter2D(a, -1, np.full((1, 60), 1 / 60, np.float32))
        fr = glow_white(bg, a, k_glow=0.9, bloom=bloom)
        wr.write(fr + grain(seed=9100 + st, amt=4))
    wr.close()
    print(f"   count: {n} frames ({t0:.3f}-{t1:.3f}), lands at {t_land:.3f}, 'loss.' at {t_loss:.3f}")

# ============================================================================== v15 (the user's notes on the v10 render)
# The wall: "covering the whole screen ... curved inward ... away from perspective": photos over the whole frame (a
# 3 x 4 cover, each tile overlapping its neighbours, no gaps), more cutting in on top every reel frame (12 fps), the
# whole picture bent inward (a pincushion: the edges near, the middle far), the edges soft.
WALL5_BASE = [   # (key, t, cx, cy, zoom, look), row by row
    ("ASH", 9.3, 0.42, 0.40, 0.86, "c"), ("XEX", 125.0, 0.50, 0.48, 0.72, "c"),
    ("BRL", 845.0, 0.44, 0.55, 0.80, "c"), ("CPIN", 11.1, 0.50, 0.50, 0.60, "c"),
    ("FE3", 13.4, 0.50, 0.42, 0.62, "bw"), ("C618", 3.3, 0.55, 0.45, 0.85, "bw"),
    ("ASH", 8.2, 0.52, 0.42, 0.80, "c"), ("BR15", 214.0, 0.50, 0.50, 0.55, "c"),
    ("COPP", 7.0, 0.52, 0.50, 0.70, "green"), ("CMJ", 2.6, 0.50, 0.50, 0.92, "c"),
    ("BRL", 160.0, 0.46, 0.60, 0.80, "c"), ("BRS", 13.5, 0.46, 0.50, 0.70, "c"),
]

ROWS5, COLS5 = [0, 380, 720, 1080], [0, 520, 980, 1460, 1920]

WALL5_OVER = [   # (key, t, cx, cy, zoom, x, y, w, h, step, look)
    ("LFI", 10.3, 0.50, 0.38, 0.50, 120, 560, 380, 280, 1, "c"),
    ("CPIN", 2.9, 0.50, 0.50, 0.80, 1500, 520, 420, 470, 2, "c"),
    ("FIN", 1.0, 0.68, 0.36, 0.56, 640, 90, 640, 620, 3, "c"),      # the big one in the middle (the reel's duo)
    ("MF2", 7.4, 0.42, 0.40, 0.50, 1290, 60, 330, 420, 4, "bw"),
    ("ASH", 11.5, 0.42, 0.45, 0.78, 260, 0, 420, 270, 5, "c"),
    ("BRS", 0.5, 0.50, 0.58, 0.82, 560, 760, 460, 280, 6, "c"),
    ("ASH", 10.6, 0.47, 0.42, 0.62, 1020, 640, 360, 300, 7, "c"),
]

_CONC = {}

def concave(img, k=0.20):
    """bend the picture inward (pincushion): the edges magnified, the middle pushed back; the frame stays full"""
    h, w = img.shape[:2]
    key = (h, w, k)
    if key not in _CONC:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        dx, dy = (xx - w / 2) / (w / 2), (yy - h / 2) / (w / 2)
        f = 1 - k * (dx * dx + dy * dy)
        _CONC[key] = ((w / 2 + dx * f * (w / 2)).astype(np.float32), (h / 2 + dy * f * (w / 2)).astype(np.float32))
    mx, my = _CONC[key]
    return cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def wall5_lens(fr, step):
    k = 1.0 + 0.006 * step
    fr = affine(fr, k, W / 2, H / 2, W / 2, H / 2, border=(0, 0, 0))
    fr = concave(fr, 0.20)
    fr = center_focus(fr, r0=560, r1=1150, zoom=0.008, n=6, gblur=1.6)
    return vignette(fr, strength=0.22)

def fink_white():
    cut = np.asarray(Image.open(f"{IMG}/v10_fink_cut.png").convert("RGBA")).astype(np.float32)
    out = np.zeros_like(cut)
    out[..., :3] = 255
    out[..., 3] = cut[..., 3]
    Image.fromarray(out.astype(np.uint8), "RGBA").save(f"{IMG}/v15_fink_white.png")

def r_wall5():
    n = nf(0.0, FINK_IN)
    k_wall, k_thresh, k_false = 10, n - 8, n - 4
    base = []
    for i, (key, t, cx, cy, z, look) in enumerate(WALL5_BASE):
        r, c = divmod(i, 4)
        x0, y0 = COLS5[c] - 18, ROWS5[r] - 18
        w, h = COLS5[c + 1] - COLS5[c] + 36, ROWS5[r + 1] - ROWS5[r] + 36
        base.append((tile_still(key, t, cx, cy, z, w, h, look), x0, y0, w, h, k_wall))
    over = [(tile_still(k, t, cx, cy, z, w, h, look), x, y, w, h, k_wall + STEP * st)
            for k, t, cx, cy, z, x, y, w, h, st, look in WALL5_OVER]

    def paste(fr, im, x, y, w, h):
        x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
        fr[y0:y1, x0:x1] = im[y0 - y:y1 - y, x0 - x:x1 - x]

    def wall(i):
        st = max(0, (i - k_wall) // STEP)
        fr = np.zeros((H, W, 3), np.float32)
        for im, x, y, w, h, f0 in base + over:
            if f0 <= max(i, k_wall):
                paste(fr, im, x, y, w, h)
        return wall5_lens(fr, st)

    texture = (np.sin(np.arange(H, dtype=np.float32) * np.pi / 2.0) * 3.0)[:, None, None]
    first, last = wall(k_wall), wall(k_thresh - 1)
    soft = cv2.GaussianBlur(last, (0, 0), 7) * 0.62
    soft_c = cv2.resize(soft, (FW, FH), interpolation=cv2.INTER_CUBIC) * screen_lines(FW)
    save_jpg(soft_c, f"{IMG}/v15_bg_wall.jpg", q=94)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    L = 140
    pan = cv2.filter2D(first, -1, np.full((1, L), 1.0 / L, np.float32), borderType=cv2.BORDER_REFLECT)
    bend = (xx - W / 2) / (W / 2)
    pan = cv2.remap(pan, xx, (H / 2 + (yy - H / 2) * (1 + 0.22 * bend * bend)).astype(np.float32), cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REFLECT)
    pan = np.stack([np.roll(pan[..., 0], 16, axis=1), pan[..., 1], np.roll(pan[..., 2], -16, axis=1)], axis=2)
    pan = grade(pan, sat=1.9, contrast=1.35, bright=10)
    pan = pan + cv2.GaussianBlur(np.clip(pan - 150, 0, 255), (0, 0), 14) * 0.9
    grey = grade(cv2.GaussianBlur(first, (0, 0), 1.6), sat=0.35, contrast=0.5) * 0.7 + 150 * 0.3
    grey = np.stack([np.roll(grey[..., 0], 4, axis=1), grey[..., 1], np.roll(grey[..., 2], -4, axis=1)], axis=2)
    cutc = fink_cut2()
    al = cutc[..., 3:4] / 255.0
    comp = soft_c * (1 - al) + cutc[..., :3] * al
    M = np.float32([[1.0, 0, W / 2 - (FX0 + W / 2)], [0, 1.0, H / 2 - (FY0 + H / 2)]])
    fv = cv2.warpAffine(comp, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    g = np.clip(fv @ np.float32([0.299, 0.587, 0.114]) * 1.6 + 25, 0, 255).astype(np.uint8)
    falsec = cv2.GaussianBlur(cv2.applyColorMap(255 - g, cv2.COLORMAP_TURBO)[..., ::-1].astype(np.float32), (0, 0), 3.0)
    gg = last @ np.float32([0.299, 0.587, 0.114])
    gg = np.where(gg > 58, 255.0, gg * 0.25)
    blk = cv2.resize(cv2.resize(gg, (W // 18, H // 18), interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST)
    m = ((xx > W * 0.55) & (((xx // 90).astype(int) + (yy // 70).astype(int)) % 3 == 0)).astype(np.float32)
    photocopy = np.repeat((gg * (1 - m) + np.where(blk > 140, 255.0, 20.0) * m)[..., None], 3, axis=2)
    fink_white()
    wr = Writer(f"{CLIPS}/v15_wall.mp4")
    cache = {}
    for i in range(n):
        if i < 6:
            fr = pan
        elif i < k_wall:
            fr = grey
        elif i < k_thresh:
            st = (i - k_wall) // STEP
            if st not in cache:
                cache[st] = wall(i)
            fr = cache[st]
        elif i < k_false:
            fr = photocopy
        else:
            fr = falsec
        wr.write(fr + texture + grain(seed=5000 + (i // STEP), amt=5))
    wr.close()
    print(f"   wall5: {n} frames, {len(WALL5_BASE)} photos covering the frame + {len(WALL5_OVER)} cutting in")

def r_company2():
    """"company ever": Fink from behind facing the crowd (FG 2.55: his glasses and profile show), black and white,
    only lightly lifted (the user: less texture, less opacity, so he can be seen)"""
    a0, a1 = B["built"][0], F(T["built"] - TM.LEAD)
    n = nf(a0, a1)
    frs = grab(SRC["FG"], 2.55, n, fps=FPS)
    wr = Writer(f"{CLIPS}/v15_company.mp4")
    for i, im in enumerate(frs):
        im = im.astype(np.float32)
        h, w = im.shape[:2]
        ch = int(w * 9 / 16)
        y0 = max(0, int(h * 0.36 - ch / 2))
        fr = cv2.resize(im[y0:y0 + ch], (W, H), interpolation=cv2.INTER_CUBIC)
        k = 1.10 + 0.02 * i / max(1, n - 1)                   # (cropped in: clear of the channel's "tfg" bug)
        fr = affine(fr, k, W * 0.56, H / 2, W / 2, H / 2, border=(0, 0, 0))
        g = cv2.GaussianBlur(fr, (0, 0), 0.6) @ np.float32([0.299, 0.587, 0.114])
        g = np.clip(g * 0.95 + 16, 0, 255)
        wr.write(vignette(np.repeat(g[..., None], 3, axis=2), strength=0.25) + grain(seed=6100 + i, amt=2.5))
    wr.close()
    print(f"   company2: {n} frames (FG 2.55, light)")

# ---- the founders' square transition (the user: "slightly before, on his face ... a transition between the clips"):
# over the last 0.2 s of each founder's clip the frame breaks into the Nvidia reel's 3 x 3 squares -- first his face,
# white and black, then more and more of the next shot (our next page; for Jobs, Elon on Rogan)
TILE_SEQ = ["CWCCBCCWC", "WCBNCWBCN", "NWNBNNWNB", "NNWNNBNNN"]

def tiles2(cur, nxt, pat, gap=6):
    out = np.full((H, W, 3), 10, np.float32)
    tw, th = W // 3, H // 3
    for k, c in enumerate(pat):
        r, q = divmod(k, 3)
        x, y = q * tw + gap // 2, r * th + gap // 2
        src = {"C": cur, "N": nxt}.get(c)
        if src is None:
            out[y:y + th - gap, x:x + tw - gap] = 246 if c == "W" else 6
        else:
            out[y:y + th - gap, x:x + tw - gap] = src[y:y + th - gap, x:x + tw - gap]
    return out

def tile_out(name, frames_, nxt, step=3):
    n = len(frames_)
    k0 = n - step * len(TILE_SEQ)
    wr = Writer(f"{CLIPS}/{name}.mp4")
    for i, fr in enumerate(frames_):
        fr = fr.astype(np.float32)
        f24 = int(i * 24 / FPS)
        if f24 in (2, 4):                                   # the reel's two negatives at the start
            fr = 255 - fr
        if i >= k0:
            fr = tiles2(fr, nxt, TILE_SEQ[min(len(TILE_SEQ) - 1, (i - k0) // step)])
        wr.write(fr)
    wr.close()

def r_founders2():
    """the v6 founders' clips re-cut: Jensen (the Nvidia reel's own opening, held before its own squares), Gates and
    Jobs, each ending in the squares into the shot that really follows (the page images from snapshots)"""
    import prep_v3 as P3
    import prep_v4 as P4
    slots = founder_slots()
    nxt = {k: np.asarray(Image.open(f"{WORK}/next_{k}.png").convert("RGB").resize((W, H))).astype(np.float32)
           for k in ("ms", "ap")}
    nxt["rogan"] = grab(f"{CLIPS}/v5_rogan.mp4", 0.0, 1)[0].astype(np.float32)
    a, b = slots["r1_jensen"]
    n = nf(a, b)
    src = grab(f"{P3.V3}/nvidia_reel.mp4", 0.0, 26)
    fr = []
    for i in range(n):
        j = min(int(i * 24 / FPS), 21)                     # (its own squares, frames 22-24, left out)
        im = cv2.resize(src[j][0:540].astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
        fr.append(np.clip(im + (im - cv2.GaussianBlur(im, (0, 0), 2.0)) * 0.6, 0, 255))
    tile_out("v3_r1_jensen", fr, nxt["ms"])
    a, b = slots["r1_gates"]
    n = nf(a, b)
    tile_out("v3_r1_gates", P3.live(f"{P3.V3}/bill_gates.mp4", 9.40, n, crop="crop=1186:667:90:0")[:n], nxt["ap"])
    a, b = slots["r1_jobs"]
    n = nf(a, b)
    tile_out("v3_r1_jobs", P3.live(f"{P3.V3}/steve_jobs.mp4", 0.30, n)[:n], nxt["rogan"])
    for k, name in enumerate(["v3_r1_jensen", "v3_r1_gates", "v3_r1_jobs"]):
        P4.texture_pass(name, opacity=0.0, seed=3 + k)
    print("   founders2: squares into the next shot over each clip's last 0.2 s")
