"""Trimmed from blackrock-open/tools/prep_v16.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import sys

from common import *  # noqa: F401,F403

import timing as TM

import prep_v10 as P10

T, B, F = TM.T, TM.B, TM.F

LD = TM.LEAD

RI = lambda i: TM.R(TM.ALIGN["rest"][i]["start"])

Lr = lambda i: F(RI(i) - LD)

STEP = 5                                   # 12 fps states

V16 = f"{DL}/v16"

DIMON = os.path.abspath(f"{REPO}/dimon-src")

S16 = dict(P10.SRC)

S16.update({
    "QC": f"{DL}/v3/new/quietcapital.mp4", "AX": f"{DL}/v3/new/axirohq.mp4", "BRE": f"{DL}/v6/docs/br_edit.mp4",
    "CIT": f"{DIMON}/_direct/citadel_trading.mp4", "BM": f"{DIMON}/_drive/banking montage 1-2 sec clip can be used.mp4",
    "UNT": f"{DIMON}/_direct/untold_career_story.mp4", "HF1": f"{DL}/v6/hf60/shot1_b.mp4",
})

HB = f"{ROOT}/assets/fonts/TeXGyreHeros-Bold.otf"

LUM = np.float32([0.299, 0.587, 0.114])

nf = P10.nf

# the rise (the reel's duo, n30-n49 at 30 fps): states at these seconds, the remaining share of the rise
RISE = 324

def ease_out(u, p=3):
    u = min(1.0, max(0.0, u))
    return 1 - (1 - u) ** p

# ------------------------------------------------------------------------------------------------ the opening
def r_open():
    n = nf(0.0, P10.FINK_IN)
    frs = grab(f"{CLIPS}/v15_wall.mp4", 0.0, n)
    bg = np.asarray(Image.open(f"{IMG}/v15_bg_wall.jpg").convert("RGB")).astype(np.float32)
    FWc, FHc = P10.FW, P10.FH
    Mz = cv2.getRotationMatrix2D((FWc / 2, FHc / 2), 0, 1.08)
    bgz = cv2.GaussianBlur(cv2.warpAffine(bg, Mz, (FWc, FHc), borderMode=cv2.BORDER_REFLECT), (0, 0), 9)
    cut = np.asarray(Image.open(f"{IMG}/v10_fink_cut.png").convert("RGBA")).astype(np.float32)
    cut = cv2.warpAffine(cut, np.float32([[1, 0, 0], [0, 1, RISE]]), (FWc, FHc), borderMode=cv2.BORDER_CONSTANT)
    al = cut[..., 3:4] / 255.0
    comp = bgz * (1 - al) + cut[..., :3] * al
    fv = comp[P10.FY0:P10.FY0 + H, P10.FX0:P10.FX0 + W]
    g = np.clip(fv @ LUM * 1.6 + 25, 0, 255).astype(np.uint8)
    falsec = cv2.GaussianBlur(cv2.applyColorMap(255 - g, cv2.COLORMAP_TURBO)[..., ::-1].astype(np.float32), (0, 0), 3.0)
    texture = (np.sin(np.arange(H, dtype=np.float32) * np.pi / 2.0) * 3.0)[:, None, None]
    k_false = n - 4
    wr = Writer(f"{CLIPS}/v16_wall.mp4")
    for i in range(n):
        wr.write(frs[i] if i < k_false else falsec + texture + grain(seed=5000 + i // STEP, amt=5))
    wr.close()

# ------------------------------------------------------------------------------------------------ the counter
def glow_white2(base, a, k_glow=1.0, bloom=0.0):
    g1 = cv2.GaussianBlur(a, (0, 0), 5 + 10 * bloom)
    g2 = cv2.GaussianBlur(a, (0, 0), 18 + 40 * bloom)
    g3 = cv2.GaussianBlur(a, (0, 0), 52 + 60 * bloom)
    halo = np.clip(0.80 * g1 + 0.55 * g2 + 0.40 * g3, 0, 1) * (1.1 + 1.4 * bloom)
    h = np.clip(halo, 0, 0.9)[..., None]
    out = base * (1 - h) + 255 * h
    return out * (1 - a[..., None]) + np.float32([250, 247, 240]) * a[..., None]

# ------------------------------------------------------------------------------------------------ 2008: the date
def text_mask_c(text, path, size, cx, cy, track=-0.02):
    """the text's ink centred on (cx, cy)"""
    f = ImageFont.truetype(path, size)
    widths = [f.getlength(ch) for ch in text]
    tw = sum(widths) + track * size * (len(text) - 1)
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    _, t, _, b = f.getbbox(text)
    x = cx - tw / 2
    y = cy - (t + b) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, fill=255, font=f)
        x += w + track * size
    return np.asarray(im).astype(np.float32) / 255.0

def glow_on(base, m, strength=1.0):
    g1 = cv2.GaussianBlur(m, (0, 0), 6)
    g2 = cv2.GaussianBlur(m, (0, 0), 22)
    g3 = cv2.GaussianBlur(m, (0, 0), 75)
    halo = np.clip((0.9 * g1 + 0.65 * g2 + 0.5 * g3) * strength, 0, 0.95)[..., None]
    out = base * (1 - halo) + 255 * halo
    return out * (1 - m[..., None]) + 255 * m[..., None]

def curved_frame_mask():
    xx = np.arange(W, dtype=np.float32)
    u = (xx - W / 2) / (W / 2)
    top = 60 + 27 * (1 - u * u)
    bot = 1023 - 30 * (1 - u * u)
    yy = np.arange(H, dtype=np.float32)[:, None]
    m = ((yy >= top[None, :]) & (yy <= bot[None, :])).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), 2.5)[..., None]

# ------------------------------------------------------------------------------------------------ the datamosh
def datamosh(a, b, p, seed):
    """a datamosh-like frame between a (out) and b (in), p in 0..1: bands of the pictures dragged sideways into streaks,
    gaps of black, the incoming picture more and more"""
    rng = np.random.default_rng(seed)
    out = np.zeros_like(a)
    y = 0
    while y < H:
        bh = int(rng.integers(10, 34))
        src = b if rng.random() < 0.25 + 0.6 * p else a
        row = src[y:y + bh]
        x = 0
        while x < W:
            seg = int(rng.integers(50, 360))
            x1 = min(W, x + seg)
            mode = rng.random()
            if mode < 0.30:
                pass                                                  # black
            elif mode < 0.72:                                         # one column dragged across
                cx = int(np.clip(x + rng.integers(-80, 80), 0, W - 1))
                out[y:y + bh, x:x1] = row[:, cx:cx + 1]
            else:                                                     # the picture, shifted
                dx = int(rng.integers(-160, 160))
                xs = np.clip(np.arange(x, x1) + dx, 0, W - 1)
                out[y:y + bh, x:x1] = row[:, xs]
            x = x1
        y += bh
    out = grade(out, sat=1.6, contrast=1.15)
    return cv2.filter2D(out, -1, np.full((1, 9), 1 / 9, np.float32))

# ------------------------------------------------------------------------------------------------ 2008: the grid
TILES = {"TL": (0, 0, 938, 548), "BL": (0, 552, 438, 1080), "LED": (442, 552, 938, 1080),
         "C": (942, 0, 1458, 1080), "R": (1462, 0, 1920, 1080)}

GRID_SHOTS = {"TL": ("AX", 4.5, 0.42, 0.55, 1.05), "BL": ("BR15", 462.0, 0.50, 0.58, 1.25),
              "C": ("BRE", 8.0, 0.72, 0.50, 1.0), "R": ("CIT", 7.0, 0.60, 0.50, 1.0)}

GRID_SWAP = {"R": (40, ("BM", 7.5, 0.55, 0.50, 1.0)), "BL": (42, ("UNT", 1131.0, 0.30, 0.62, 1.2))}

GRID_WHITE = [("TL", 9), ("BL", 14), ("C", 19), ("R", 24), ("LED", 29)]          # each 5 frames, one after another

LED_VALUES = [(0, "-153"), (9, "-498"), (31, "-777")]

GRID_DATE, GRID_OUT = "v16_date.mp4", "v16_grid.mp4"      # (v17 renders it again after its moving clock)

def tile_clip(key, t0, n, tw, th, cx, cy, zoom=1.0):
    w, h, _ = probe(S16[key])
    ar = tw / th
    ch = h / zoom
    cw = ch * ar
    if cw > w / zoom:
        cw = w / zoom
        ch = cw / ar
    cw, ch = int(cw) // 2 * 2, int(ch) // 2 * 2
    x0 = int(np.clip(cx * w - cw / 2, 0, w - cw))
    y0 = int(np.clip(cy * h - ch / 2, 0, h - ch))
    return [f.astype(np.float32) for f in grab(S16[key], t0, n, fps=FPS, size=(tw, th), vf=f"crop={cw}:{ch}:{x0}:{y0}")]

def led_tile(text, tw, th):
    pitch, r = 12, 3.7
    panel = np.full((th, tw, 3), np.float32([12, 16, 12]))
    m = Image.new("L", (tw, th), 0)
    f = ImageFont.truetype(HB, 330)
    wtxt = f.getlength(text)
    f = ImageFont.truetype(HB, int(330 * min(1.0, (tw - 40) / wtxt)))
    wtxt = f.getlength(text)
    _, t, _, b = f.getbbox(text)
    ImageDraw.Draw(m).text(((tw - wtxt) / 2, th / 2 - (t + b) / 2), text, fill=255, font=f)
    mm = np.asarray(m).astype(np.float32) / 255.0
    on = np.zeros((th, tw), np.float32)
    off = np.zeros((th, tw), np.float32)
    for cy in range(pitch // 2, th, pitch):
        for cx in range(pitch // 2, tw, pitch):
            tgt = on if mm[cy, cx] > 0.5 else off
            cv2.circle(tgt, (cx, cy), int(round(r)), 1.0, -1, lineType=cv2.LINE_AA)
    glow = cv2.GaussianBlur(on, (0, 0), 6) * 0.55
    out = panel + off[..., None] * np.float32([18, 34, 20]) + on[..., None] * np.float32([150, 255, 90]) \
        + glow[..., None] * np.float32([60, 140, 40])
    return np.clip(out, 0, 255)

def r_grid():
    g0, g1 = Lr(97), Lr(99)
    n = nf(g0, g1)
    clips = {}
    for name, (key, t0, cx, cy, z) in GRID_SHOTS.items():
        x0, y0, x1, y1 = TILES[name]
        clips[name] = tile_clip(key, t0, n, x1 - x0, y1 - y0, cx, cy, z)
    swaps = {}
    for name, (f0, (key, t0, cx, cy, z)) in GRID_SWAP.items():
        x0, y0, x1, y1 = TILES[name]
        swaps[name] = (f0, tile_clip(key, t0, n, x1 - x0, y1 - y0, cx, cy, z))
    lx0, ly0, lx1, ly1 = TILES["LED"]
    leds = {v: led_tile(v, lx1 - lx0, ly1 - ly0) for _, v in LED_VALUES}
    date_last = grab(f"{CLIPS}/{GRID_DATE}", 0.0, nf(Lr(94), Lr(97)))[-1].astype(np.float32)
    nxt = grab(f"{CLIPS}/v6_rest2.mp4", g1 - B["rest2"][0], 1)[0].astype(np.float32)

    def grid(i):
        fr = np.full((H, W, 3), 8.0, np.float32)
        for name, (x0, y0, x1, y1) in TILES.items():
            if name == "LED":
                v = [val for f0, val in LED_VALUES if i >= f0][-1]
                tile = leds[v]
            else:
                tile = clips[name][min(i, len(clips[name]) - 1)]
                if name in swaps and i >= swaps[name][0]:
                    sc = swaps[name][1]
                    tile = sc[min(i - swaps[name][0], len(sc) - 1)]
            if name in ("C", "R"):
                tile = tile * (0.70 if name == "C" else 0.82)       # (under the caption, as the reel's darker middle)
            for nm, f0 in GRID_WHITE:
                if nm == name and f0 <= i < f0 + 5:
                    tile = np.full_like(tile, 250.0)
            fr[y0:y1, x0:x1] = tile
        return fr

    k_in, k_out = 5, n - 6
    wr = Writer(f"{CLIPS}/{GRID_OUT}")
    for i in range(n):
        if i < k_in:
            fr = datamosh(date_last, grid(k_in), (i + 1) / (k_in + 1), seed=9300 + i // 2)
        elif i >= k_out:
            fr = datamosh(grid(k_out - 1), nxt, (i - k_out + 1) / (n - k_out + 1), seed=9400 + i // 2)
        else:
            fr = grid(i)
        wr.write(fr + grain(seed=9500 + i // 2, amt=4))
    wr.close()
    print(f"   grid: {n} frames ({g0:.3f}-{g1:.3f})")

# ------------------------------------------------------------------------------------------------ the government
def r_gov():
    a, b = Lr(99), F(RI(106))                 # (to v6_rest2's own cut into "Wall Street")
    n = nf(a, b)
    frs = [f.astype(np.float32) for f in grab(f"{CLIPS}/v6_rest2.mp4", a - B["rest2"][0], n)]
    small = [cv2.resize(f, (96, 54), interpolation=cv2.INTER_AREA) for f in frs]
    d = [0.0] + [float(np.abs(small[i] - small[i - 1]).mean()) for i in range(1, n)]
    cuts = [i for i in range(2, n - 2) if d[i] > 28 and d[i] > 3 * max(d[i - 1], d[i + 1], 4)]
    out = list(frs)
    for c in cuts:
        for k, i in enumerate(range(c - 3, c + 3)):
            if 0 <= i < n:
                out[i] = datamosh(frs[c - 1], frs[c], (k + 0.5) / 6, seed=9600 + c * 7 + k // 2)
    wr = Writer(f"{CLIPS}/v16_gov.mp4")
    for fr in out:
        wr.write(fr)
    wr.close()
    print(f"   gov: {n} frames ({a:.3f}-{b:.3f}), datamosh at cuts {[round(a + c / FPS, 3) for c in cuts]}")

# ------------------------------------------------------------------------------------------------ the money
def sprite(path):
    a = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)
    ys, xs = np.where(a[..., 3] > 8)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

_SC = {}

def scaled(spr, w, rot=0.0, key=""):
    k = (key, int(w), round(rot, 1))
    if k not in _SC:
        h = int(spr.shape[0] * w / spr.shape[1])
        s = cv2.resize(spr, (int(w), h), interpolation=cv2.INTER_AREA)
        if rot:
            pad = int(0.25 * w)
            s = cv2.copyMakeBorder(s, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
            M = cv2.getRotationMatrix2D((s.shape[1] / 2, s.shape[0] / 2), rot, 1.0)
            s = cv2.warpAffine(s, M, (s.shape[1], s.shape[0]), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        _SC[k] = s
    return _SC[k]

def paste_rgba(fr, s, cx, cy, clip_x=None):
    h, w = s.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if clip_x is not None:
        xb = min(xb, int(clip_x))
    if xb <= xa or yb <= ya:
        return
    part = s[ya - y0:yb - y0, xa - x0:xb - x0]
    al = part[..., 3:4] / 255.0
    fr[ya:yb, xa:xb] = fr[ya:yb, xa:xb] * (1 - al) + part[..., :3] * al

def shadow_rgba(fr, s, cx, cy, off=(18, 26), blur=18, amt=0.22):
    h, w = s.shape[:2]
    a = np.zeros((H, W), np.float32)
    x0, y0 = int(round(cx - w / 2 + off[0])), int(round(cy - h / 2 + off[1]))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya:
        return
    a[ya:yb, xa:xb] = s[ya - y0:yb - y0, xa - x0:xb - x0, 3] / 255.0
    a = cv2.GaussianBlur(a, (0, 0), blur) * amt
    fr *= (1 - a[..., None])

def page_bg():
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    return np.clip(252 - 34 * np.exp(-yy / 230.0) - 10 * np.exp(-(H - yy) / 160.0), 0, 255) * np.ones((1, W, 3), np.float32)

def stack_layout():
    """the pile: rows from the bottom up, each stack's landing time (the first one alone in the middle, then faster)"""
    rng = np.random.default_rng(1607)
    out = [(960, 520, 560, 0.0, 0.36)]
    rows = [(1040, 640), (900, 600), (760, 560), (620, 520), (480, 480), (340, 450), (200, 420), (70, 400)]
    k = 0
    cand = []
    for ri, (y, w) in enumerate(rows):
        xs = np.arange(-60 + (ri % 2) * w * 0.45, W + w, w * 0.86)
        for x in xs:
            cand.append((float(x + rng.uniform(-40, 40)), float(y + rng.uniform(-22, 22)), float(w * rng.uniform(0.92, 1.06)),
                         float(rng.uniform(-4, 4))))
    order = rng.permutation(len(cand))
    N = len(cand)
    for j, ci in enumerate(order):
        x, y, w, rot = cand[ci]
        t_land = 0.48 + 0.78 * (j / (N - 1)) ** 0.62
        out.append((x, y, w, rot, t_land))
        k += 1
    return out

MONEY = dict(fink_s=0.92, fink_x=-205, cash_w=700, cash_x=990, cash_y=452, out="v16_money.mp4")

def r_money():
    h0, s0, e0 = Lr(119), Lr(125), F(RI(130))  # (to v6_rest2's own cut into "Today,")
    n, nA = nf(h0, e0), nf(h0, s0)
    cash = sprite(f"{V16}/money_stack.png")
    fink = np.asarray(Image.open(f"{DL}/v10/larry_new_cut.png").convert("RGBA")).astype(np.float32)
    fs = MONEY["fink_s"]
    fink = cv2.resize(fink, (int(fink.shape[1] * fs), int(fink.shape[0] * fs)), interpolation=cv2.INTER_AREA)
    fh, fw = fink.shape[:2]
    bg = page_bg()
    lay = stack_layout()
    tA = (s0 - h0)

    def handoff(t):
        fr = bg.copy()
        # Fink from the left, his raised hand reaching to the right (the reel's robot hand)
        fx_final = MONEY["fink_x"] + 20 * min(1.0, t / 0.9)
        fx = fx_final - 760 * (1 - ease_out(t / 0.45))
        wipe = None
        if t >= 0.78:
            wipe = 1350 - 1500 * min(1.0, (t - 0.78) / 0.15)
        if wipe is None or wipe > 0:
            shadow_rgba(fr, fink, fx + fw / 2, (H - fh) + fh / 2, off=(22, 18), blur=26, amt=0.16)
            paste_rgba(fr, fink, fx + fw / 2, (H - fh) + fh / 2, clip_x=wipe)
        # the cash from the right, into his fingers
        cw = MONEY["cash_w"]
        cs = scaled(cash, cw, 0.0, "c")
        cx_final = MONEY["cash_x"] + cw / 2 - 40 * min(1.0, t / 0.9)
        cx = cx_final + 1250 * (1 - ease_out(t / 0.45))
        cy = MONEY["cash_y"]
        if t > 0.95:                                      # the drop
            u = (t - 0.95) / max(0.05, tA - 0.95)
            cy += 900 * u * u
        shadow_rgba(fr, cs, cx, cy, off=(16, 24), blur=16, amt=0.25)
        paste_rgba(fr, cs, cx, cy)
        return fr

    def stacks(t):
        fr = bg.copy()
        drift = -60 * (t / max(0.1, (e0 - s0)))
        for x, y, w, rot, tl in lay:
            if t < tl - 0.30:
                continue
            u = min(1.0, (t - (tl - 0.30)) / 0.30)
            yy = y - 560 * (1 - ease_out(u, 2)) + drift
            if tl == 0.36:                                # the first: it comes down slowly from the top
                u = min(1.0, t / 0.40)
                yy = -200 + (y + 200) * ease_out(u, 2) + drift
            s = scaled(cash, w, rot, "c")
            shadow_rgba(fr, s, x, yy, off=(14, 22), blur=14, amt=0.20)
            paste_rgba(fr, s, x, yy)
        return fr

    cache = {}
    wr = Writer(f"{CLIPS}/{MONEY['out']}")
    for i in range(n):
        st = i // STEP
        t = st * STEP / FPS
        key = ("A", st) if i < nA else ("B", (i - nA) // STEP)
        if key not in cache:
            cache[key] = handoff(t) if i < nA else stacks(((i - nA) // STEP) * STEP / FPS)
        wr.write(cache[key] + grain(seed=9900 + i // STEP, amt=3))
    wr.close()
    print(f"   money: {n} frames ({h0:.3f}-{e0:.3f}), the hand-off {nA}, the stacks {n - nA} ({len(lay)} stacks)")
