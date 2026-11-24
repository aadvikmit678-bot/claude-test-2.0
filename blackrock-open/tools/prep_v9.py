#!/usr/bin/env python3
"""v9 renderers: the new opening (the user's new recording of Nov 24), each pre-rendered at 60 fps, 1920x1080.

  wall      "This is the most powerful man": the Nvidia reel's photo-wall build (43.3-44.4 s: black, a 3x3 wall filling
            from the bottom right, a tile every 3 reel frames, each tile white first) with nine different live shots of
            Larry Fink, ending on "IT ISN'T"'s lead-in (the strobe, one reel frame negative, two cyan) for ON EARTH
  articles  "A $15 trillion dollar": the user's seventeen "$15 trillion" headlines as the Opal reel's article flipbook
            (1.9-2.9 s: a page every 2 frames at 30 fps, the figure registered on the same spot on every page)
  evil      "The most evil": the red horned scene (prep_v6), re-timed to the new line
  grid      "BlackRock.": its clips fill a 3x2 grid cell by cell (the Attention Compounds reel's OpenAI grid)
  cuts      the plain shots ("company", "in the world")

Run: <venv>/bin/python -E -s tools/prep_v9.py [names...]
"""
import json
import sys

from common import *  # noqa: F401,F403
import timing as TM
import prep_v3 as P

V9 = f"{DL}/v9"
D = os.path.abspath(f"{ROOT}/../dimon-src")
DOCS = f"{DL}/v6/docs"
SRCS = {
    "FIN": f"{DL}/fink_interview.mp4", "LFI": f"{DL}/lf_interview2.mp4", "FSP": f"{DL}/fink_speaking.mp4",
    "BRL": f"{DOCS}/br_largest.mp4", "BRE": f"{DOCS}/br_edit.mp4", "BR15": f"{DOCS}/br_15t_machine.mp4",
    "BRC": f"{DOCS}/br_conspiracies.mp4", "MBS": f"{DL}/m_blackrock_start.mp4", "PANEL": PANEL,
    "X": f"{DL}/v3/br_explainer.mp4", "FI": f"{D}/_direct/fired_push_scene.mp4", "TS": f"{DL}/v3/thinkschool.mp4",
    "HOW": f"{D}/_direct/how_jpm_became_largest.mp4", "GE": f"{DL}/good_edit_42s.mp4",
}


def nf(a, b):
    return round(b * FPS) - round(a * FPS)


def jumps(frames_, thr=38.0):
    """indices where the picture changes abruptly (a hidden cut inside a span)"""
    out = []
    for i in range(1, len(frames_)):
        a = cv2.resize(frames_[i - 1], (64, 36)).astype(np.float32)
        b = cv2.resize(frames_[i], (64, 36)).astype(np.float32)
        if np.abs(a - b).mean() > thr:
            out.append(i)
    return out


def tile_clip(key, t0, n, cx, cy, span, tw, th, keep=None):
    """n frames of a source from t0, cropped to a 16:9 window (span wide, centred cx, cy) and scaled to a tile
    (keep: use only the first `keep` frames -- the shot ends there -- and hold the last one)"""
    src = SRCS[key]
    w, h, _ = probe(src)
    fr = grab(src, t0, min(n, keep) if keep else n, fps=FPS)
    ch = span * th / tw
    x0 = int(min(max(cx - span / 2, 0), w - span))
    y0 = int(min(max(cy - ch / 2, 0), h - ch))
    out = [grade(cv2.resize(im[y0:int(y0 + ch), x0:int(x0 + span)], (tw, th), interpolation=cv2.INTER_AREA),
                 sat=0.92, contrast=1.08) for im in fr]
    j = jumps(fr)
    if j:
        print(f"   !! {key}@{t0}: picture jumps at frames {j} (of {len(fr)})")
    while len(out) < n:
        out.append(out[-1])
    return out


# ------------------------------------------------------------------ 1. the wall of Finks
# tile (row-major 0..8) -> (source, start s, crop centre x, y, crop width): nine different rooms, framed on his face;
# the wall fills from the bottom right (the Nvidia reel), so the long takes are at the bottom
WALL = {
    8: ("LFI", 7.00, 880, 400, 1050),      # on stage, blue, his hands working
    7: ("BRL", 420.40, 800, 400, 1000),    # the interview with the orange tie
    6: ("PANEL", 1186.60, 960, 470, 1000), # the FII7 panel (a later moment than the second half's shot)
    5: ("BRL", 21.00, 820, 400, 1000),     # the grey BlackRock backdrop (between its date slug and lower third)
    4: ("BRE", 247.50, 600, 420, 1150),    # the dark close-up with the headset (the centre, under the words)
    3: ("BRE", 37.36, 760, 380, 1150, 49), # the warm close-up (a 0.85 s shot: its last frame holds under the strobe)
    2: ("FSP", 9.00, 360, 215, 700),       # the podium
    1: ("MBS", 10.45, 470, 315, 690),      # the close-up in front of the screens (its corner badge cropped out)
    0: ("FIN", 9.60, 1290, 370, 1000),     # his office
}
WALL_STEP = 7.5        # frames between tiles (3 reel frames at 24 fps)
WALL_WHITE = 3         # a tile is white for its first frames (1 reel frame)


def r_wall():
    a0, a1 = TM.B["wall"]
    n = nf(a0, a1)                                   # 100: to "on"
    G, tw, th = 6, 640 - 6, 360 - 6
    k0 = round((TM.T["this"] - 0.035) * FPS)         # the first tile just before "This"
    order = [8, 7, 6, 5, 4, 3, 2, 1, 0]
    start = {tile: k0 + round(j * WALL_STEP) for j, tile in enumerate(order)}
    clips = {}
    for tile, (key, t0, cx, cy, span, *keep) in WALL.items():
        m = n - start[tile]
        clips[tile] = tile_clip(key, t0, m, cx, cy, span, tw, th, keep=keep[0] if keep else None)
    neg = set(range(n - 21, n - 18)) | set(range(n - 8, n - 5))      # r_tiles3's ending: "IT ISN'T"'s lead-in
    blk = {n - 12, n - 11, n - 9}
    wr = Writer(f"{CLIPS}/v9_wall.mp4")
    for i in range(n):
        fr = np.full((H, W, 3), 10, np.float32)
        for tile in range(9):
            j = i - start[tile]
            if j < 0:
                continue
            r, c = divmod(tile, 3)
            x, y = c * 640 + G // 2, r * 360 + G // 2
            if j < WALL_WHITE:
                fr[y:y + th, x:x + tw] = 246
            else:
                fr[y:y + th, x:x + tw] = clips[tile][min(j, len(clips[tile]) - 1)]
        z = 1.0 + 0.035 * i / n                      # the same subtle push on the whole wall
        fr = affine(fr, z, W / 2, H / 2, W / 2, H / 2, border=(10, 10, 10))
        if i in neg:
            fr = 255 - np.clip(fr, 0, 255)
        elif i in blk:
            fr[:] = 0
        elif i >= n - 5:
            fr[:] = (95, 255, 255)
        wr.write(fr)
    wr.close()
    print(f"   wall: {n} frames; tiles start at", {t: start[t] for t in order}, "negatives", sorted(neg))


# ------------------------------------------------------------------ 2. the "$15 trillion" headlines
# The Opal reel's article flipbook (1.93-2.87 s, read frame by frame): a new page every 2 frames at 30 fps, each page
# hard-cut, and the figure ("$3 trillion") on the same spot and at the same size on every page, so the eye reads one
# number while the mastheads change around it. Ours: the user's seventeen screenshots (Reuters, Yahoo Finance,
# Bloomberg, ...), each scaled and placed so its own "$15 trillion" sits at the centre at one height, highlighted in
# the lime the "$60 trillion" pages had. The phrase boxes were read once by OCR (tools/words/shots15.json).
LIME = np.float32([196, 242, 62])
ART_H = 74                       # the figure's ink height on screen
# page order: light pages with the dark and the red ones spread through (the Nvidia flipbook's dark-page runs)
ART_ORDER = ["s01", "s08", "s03", "s13", "s02", "s10", "s17", "s06", "s11", "s07", "s09", "s16", "s04", "s15",
             "s05", "s14"]


def article_page(path, box):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    x0, y0, x1, y1 = box
    h = y1 - y0
    s = ART_H / h
    strip = im[max(0, y0 - 7):max(1, y0 - 2), x0:x1].reshape(-1, 3)
    bg = np.median(strip, axis=0)                               # the page's colour around the headline
    # the highlight: lime behind the figure, its letters in near-black whatever the page's colours were
    px, py = int(round(h * 0.20)), int(round(h * 0.16))
    bx0, by0, bx1, by1 = max(0, x0 - px), max(0, y0 - py), min(im.shape[1], x1 + px), min(im.shape[0], y1 + py)
    reg = im[by0:by1, bx0:bx1]
    ink = np.clip(np.abs(reg - bg).max(axis=2) / 120.0, 0, 1)[..., None]
    im[by0:by1, bx0:bx1] = LIME * (1 - ink) + np.float32([18, 18, 18]) * ink
    big = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
    big = np.clip(big * 1.45 - cv2.GaussianBlur(big, (0, 0), 1.3) * 0.45, 0, 255)      # crisp after the upscale
    bh, bw = big.shape[:2]
    # feather its edges into the page colour, so the screenshot reads as a whole page
    ramp = np.minimum.outer(np.minimum(np.arange(bh), np.arange(bh)[::-1]), np.minimum(np.arange(bw), np.arange(bw)[::-1]))
    a = np.clip(ramp / 70.0, 0, 1).astype(np.float32)[..., None]
    page = np.empty((H, W, 3), np.float32)
    page[:] = bg
    cx, cy = (x0 + x1) / 2 * s, (y0 + y1) / 2 * s               # the figure's centre -> the frame's centre
    ox, oy = int(round(W / 2 - cx)), int(round(H / 2 - cy))
    sx0, sy0, sx1, sy1 = max(0, -ox), max(0, -oy), min(bw, W - ox), min(bh, H - oy)
    dst = page[oy + sy0:oy + sy1, ox + sx0:ox + sx1]
    aa = a[sy0:sy1, sx0:sx1]
    page[oy + sy0:oy + sy1, ox + sx0:ox + sx1] = dst * (1 - aa) + big[sy0:sy1, sx0:sx1] * aa
    return page


def r_articles15():
    a0, a1 = TM.B["money"]
    n = nf(a0, a1)                                   # 72: "A $15 trillion dollar"
    boxes = json.load(open(f"{ROOT}/tools/words/shots15.json"))
    names = {k[:3]: k for k in boxes}
    pages = [article_page(f"{V9}/shots15/{names[k]}", boxes[names[k]]["box"]) for k in ART_ORDER]
    per = n / len(pages)                             # 4.5 frames a page (the reel: 2 frames at 30 fps = 4 at 60)
    wr = Writer(f"{CLIPS}/v9_articles.mp4")
    for i in range(n):
        pg = pages[min(int(i / per), len(pages) - 1)]
        z = 1.0 + 0.04 * i / n                       # a slight push about the figure
        fr = affine(pg, z, W / 2, H / 2, W / 2, H / 2)
        wr.write(fr + grain(seed=1500 + i, amt=2.5))
    wr.close()
    print(f"   articles: {len(pages)} pages over {n} frames ({per:.2f} frames a page)")


# ------------------------------------------------------------------ 3. "Larry Fink, the CEO of BlackRock."
# The Hemant video's name device (5.4-8.7 s, read every 0.1 s): a mosaic takes over the frame -- one big tile in the
# middle, three small ones down each side, every tile arriving as a white card for a frame or two and then playing a
# different clip of him; the name sits over the middle in the serif with a bloom (the whole frame washes out for two
# frames as it lands), then his title builds word by word in the grotesque while the tiles keep changing. Ours: Fink's
# clips, and on "BlackRock" every tile flips to BlackRock's own buildings. (The type is in the composition.)
SRCS.update({"MF": f"{DL}/m_finance.mp4", "BRS": f"{DL}/blackrock_short.mp4", "FK2": f"{DL}/m_fink2.mp4"})
MG = 6
MOSAIC_RECTS = {                     # tile -> (x, y, w, h)
    "C": (480, 0, 960, 1080),
    "L1": (0, 0, 480, 360), "L2": (0, 360, 480, 360), "L3": (0, 720, 480, 360),
    "R1": (1440, 0, 480, 360), "R2": (1440, 360, 480, 360), "R3": (1440, 720, 480, 360),
}
# tile -> its clips in turn: (first frame, source, start s, crop centre x, y, crop width)
MOSAIC_FINK = {
    "C": [(0, "FIN", 11.00, 1310, 540, 900), (49, "BRL", 422.00, 890, 592, 836)],
    "L1": [(4, "LFI", 9.20, 880, 380, 900)],
    "R3": [(8, "PANEL", 1187.30, 900, 400, 820)],
    "L3": [(12, "BRL", 22.40, 820, 425, 860)],
    "R1": [(16, "MBS", 10.45, 470, 315, 620), (62, "LFI", 12.00, 880, 380, 900)],
    "L2": [(20, "FSP", 11.00, 360, 235, 640)],
    "R2": [(24, "BRE", 247.60, 600, 420, 1000), (88, "FSP", 14.00, 360, 235, 640)],
}
MOSAIC_BR = {                        # from "BlackRock": (delay in frames, source, start s, cx, cy, crop width)
    "C": (0, "X", 174.70, 960, 540, 960),
    "L1": (2, "BRL", 122.50, 760, 590, 1300), "R1": (3, "BR15", 214.10, 900, 560, 1300),
    "L2": (4, "MF", 11.50, 958, 560, 1300), "R2": (5, "BRL", 588.50, 860, 560, 1300),
    "L3": (6, "BRS", 4.90, 512, 288, 760), "R3": (7, "BRS", 0.00, 512, 290, 760),
}


def crop_clip(key, t0, n, cx, cy, span, tw, th):
    src = SRCS[key]
    w, h, _ = probe(src)
    fr = grab(src, t0, n, fps=FPS)
    ch = span * th / tw
    x0 = int(min(max(cx - span / 2, 0), max(0, w - span)))
    y0 = int(min(max(cy - ch / 2, 0), max(0, h - ch)))
    out = [grade(cv2.resize(im[y0:int(y0 + ch), x0:int(x0 + span)], (tw, th), interpolation=cv2.INTER_AREA),
                 sat=0.92, contrast=1.08) for im in fr]
    j = jumps(fr)
    if j:
        print(f"   !! {key}@{t0}: picture jumps at frames {j} (of {len(fr)})")
    while len(out) < n:
        out.append(out[-1])
    return out


def r_mosaic():
    a0, a1 = TM.B["name"]
    n = nf(a0, a1)                                           # 150
    t0 = round(a0 * FPS)
    k_larry = round((TM.T["larry"] - 0.03) * FPS) - t0       # the name lands here: the frame washes out just before
    k_br = round((TM.T["blackrock"] - 0.03) * FPS) - t0      # every tile flips to BlackRock from here
    segs = {}
    for tile, lst in MOSAIC_FINK.items():
        x, y, w, h = MOSAIC_RECTS[tile]
        tw, th = w - MG, h - MG
        out = []
        for j, (f0, key, ts, cx, cy, span) in enumerate(lst):
            f1 = lst[j + 1][0] if j + 1 < len(lst) else k_br
            out.append((f0, f1, crop_clip(key, ts, f1 - f0, cx, cy, span, tw, th)))
        d, key, ts, cx, cy, span = MOSAIC_BR[tile]
        out.append((k_br + d, n, crop_clip(key, ts, n - k_br - d, cx, cy, span, tw, th)))
        segs[tile] = out
    wash = {k_larry - 2: 0.55, k_larry - 1: 0.85, k_larry: 0.35}          # the bloom as the name lands
    wr = Writer(f"{CLIPS}/v9_mosaic.mp4")
    for i in range(n):
        fr = np.full((H, W, 3), 10, np.float32)
        for tile, (x, y, w, h) in MOSAIC_RECTS.items():
            tw, th = w - MG, h - MG
            cur = None
            for f0, f1, clip in segs[tile]:
                if f0 <= i < f1:
                    cur = (f0, clip)
            if cur is None:
                # between its Fink clip and its BlackRock clip a tile holds its last frame
                prev = [sg for sg in segs[tile] if sg[1] <= i]
                if not prev:
                    continue
                img = prev[-1][2][-1]
            else:
                f0, clip = cur
                img = np.full((th, tw, 3), 246, np.float32) if i - f0 < 3 else clip[min(i - f0, len(clip) - 1)]
            fr[y + MG // 2:y + MG // 2 + th, x + MG // 2:x + MG // 2 + tw] = img
        k = wash.get(i, 0.0)
        if k:
            fr = fr * (1 - k) + 255 * k
        wr.write(fr)
    wr.close()
    print(f"   mosaic: {n} frames; the name at {k_larry}, BlackRock at {k_br}")


# ------------------------------------------------------------------ 4. the plain shots
def cut_clip(name, key, t0, dur, vf=None, crf=12):
    filt = ([vf] if vf else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", "fps=60"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", SRCS[key], "-t", f"{dur:.3f}", "-vf",
                    ",".join(filt), "-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", f"{CLIPS}/{name}.mp4"], check=True)
    print("  ", name)


def r_cuts():
    a0, a1 = TM.B["company"]
    dur = a1 - a0 + 0.1
    # "company in the world.": the Earth at night. The source holds it for 0.5 s (87.72-88.25, then a puppeteer's
    # hands come in), and his strings already cross its top corners: they are painted out frame by frame (thin bright
    # lines on the dark sky), then that half second runs slowed to the beat's length with motion interpolation (the
    # planet barely moves: no stutter, no still)
    src = grab(SRCS["BRE"], 87.72, 16)
    tmp = f"{CLIPS}/_earth_tmp.mp4"
    wr = Writer(tmp, fps=30, w=1440, h=1080, crf=8)
    for im in src[:16]:
        g = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        hat = cv2.morphologyEx(g, cv2.MORPH_TOPHAT, np.ones((13, 13), np.uint8))
        dark = cv2.GaussianBlur(g, (0, 0), 22) < 95
        m = ((hat > 14) & dark).astype(np.uint8)
        m[330:] = 0                                            # only the sky above the horizon
        m = cv2.dilate(m, np.ones((7, 7), np.uint8))
        wr.write(cv2.inpaint(np.ascontiguousarray(im), m, 7, cv2.INPAINT_TELEA).astype(np.float32))
    wr.close()
    k = (dur + 0.12) / 0.53
    vf = (f"crop=1440:810:0:40,scale=1920:1080:flags=lanczos,setsar=1,setpts={k:.4f}*PTS,"
          "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-vf", vf, "-t", f"{dur:.3f}", "-an", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    f"{CLIPS}/v9_earth.mp4"], check=True)
    os.remove(tmp)
    print("   v9_earth")


# ------------------------------------------------------------------ 5. the founders page: products and screens
# Think School's "Founders vs Blackrock" page (the user: "the TV, MacBook and the bar ... we can make a much better
# motion graphic of that"): its three product pictures, taken from the page at twice their size on the page's own
# grey, and -- the Elon reel's old-TV device (DeHkRtts3bI, 9.7-17.5 s: his interview playing on a CRT) -- each founder
# playing on his own machine's screen: Gates on the MS-DOS monitor in its green phosphor, Jobs on the Macintosh in
# black and white; Jensen (the graphics card has no screen) on a card of his own.
TS_T = 53.5
PRODUCTS = {  # name -> the product's box on Think School's page (x0, y0, x1, y1)
    "gpu": (128, 312, 552, 602), "mac": (800, 198, 1116, 598), "pc": (1352, 188, 1768, 592),
}
PSCALE = 2.0
SRCS.update({"GATES": f"{DL}/v3/bill_gates.mp4", "JOBS": f"{DL}/v3/steve_jobs.mp4",
             "JENSEN": f"{V9}/jensen_reel.mp4"})


def r_products():
    fr = grab(SRCS["TS"], TS_T, 1)[0].astype(np.float32)
    bg = np.median(np.concatenate([fr[20:60, 600:1300].reshape(-1, 3), fr[950:990, 700:1300].reshape(-1, 3)]), axis=0)
    info = {"page": [int(round(v)) for v in bg], "scale": PSCALE}
    for name, (x0, y0, x1, y1) in PRODUCTS.items():
        crop = fr[y0:y1, x0:x1]
        h, w = crop.shape[:2]
        big = cv2.resize(crop, None, fx=PSCALE, fy=PSCALE, interpolation=cv2.INTER_CUBIC)
        big = np.clip(big * 1.5 - cv2.GaussianBlur(big, (0, 0), 1.6) * 0.5, 0, 255)
        bh, bw = big.shape[:2]
        ramp = np.minimum.outer(np.minimum(np.arange(bh), np.arange(bh)[::-1]), np.minimum(np.arange(bw), np.arange(bw)[::-1]))
        a = np.clip(ramp / 34.0, 0, 1)
        # the page's faint grid lines and texture go to the flat page colour away from the product (anything close
        # to the page grey), so only the product and its own shadow are left
        d = np.abs(big - bg).max(axis=2)
        core = (d > 16).astype(np.uint8)                                  # the product itself
        core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))   # (thin page lines drop out)
        keep = cv2.GaussianBlur(cv2.dilate(core, np.ones((41, 41), np.uint8)).astype(np.float32), (0, 0), 9.0)
        keep = np.clip(keep * 1.4, 0, 1)                                   # ... and its soft shadow around it
        a = a * keep
        rgba = np.dstack([big, a * 255]).clip(0, 255).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(f"{IMG}/v9_{name}.png")
        entry = {"w": bw, "h": bh}
        if name in ("pc", "mac"):
            # its screen: the dark glass inside the pale bezel
            lum = crop.mean(axis=2)
            sat = crop.max(axis=2) - crop.min(axis=2)
            if name == "pc":
                m = ((lum < 80) & (np.arange(h)[:, None] < h * 0.55)).astype(np.uint8)
            else:
                m = ((lum < 150) & (sat < 28) & (np.arange(h)[:, None] < h * 0.62)).astype(np.uint8)
            m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            nlab, lab, st, _ = cv2.connectedComponentsWithStats(m)
            k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            sx, sy, sw, sh = [int(v) for v in st[k, :4]]
            entry["screen"] = [round(sx * PSCALE), round(sy * PSCALE), round(sw * PSCALE), round(sh * PSCALE)]
        info[name] = entry
        print(f"   {name}: {bw}x{bh}", entry.get("screen", ""))
    json.dump(info, open(f"{ROOT}/tools/words/stake.json", "w"), indent=1)


def crt(img, kind, seed):
    """a tube's picture: green phosphor (the MS-DOS monitor) or black-and-white (the Macintosh), scan lines, a soft
    bloom and darker corners"""
    f = img.astype(np.float32)
    lum = (f[..., 0] * 0.3 + f[..., 1] * 0.59 + f[..., 2] * 0.11)
    lum = np.clip((lum - 18) * 1.25, 0, 255)
    if kind == "green":
        out = np.dstack([lum * 0.16, lum * 1.0, lum * 0.30])
    elif kind == "mono":
        out = np.dstack([lum * 0.97, lum * 0.98, lum * 0.94])
    else:
        out = f * 1.0
    h, w = lum.shape
    out = out + cv2.GaussianBlur(out, (0, 0), 6) * 0.22                       # the tube's bloom
    lines = 0.80 + 0.20 * (np.arange(h) % 3 != 0).astype(np.float32)
    if kind != "colour":
        out = out * lines[:, None, None]
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    out = out * (1 - 0.38 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]
    return np.clip(out, 0, 255)


def r_founders():
    info = json.load(open(f"{ROOT}/tools/words/stake.json"))
    T = TM.T
    specs = {  # name -> (source, start s, crop centre x, y, crop width, look, (w, h), film seconds from, to)
        "jensen": ("JENSEN", 14.50, 640, 175, 450, "colour", (480, 360), T["jensen"] - 0.03, T["more2"] - TM.LEAD),
        "gates": ("GATES", 9.50, 485, 250, 600, "green", tuple(info["pc"]["screen"][2:]), T["bill"] - 0.03, T["and"] - TM.LEAD),
        "jobs": ("JOBS", 0.40, 885, 235, 560, "mono", tuple(info["mac"]["screen"][2:]), T["steve"] - 0.03, TM.OPEN_END),
    }
    for name, (key, t0, cx, cy, span, look, (tw, th), a, b) in specs.items():
        n = nf(a, b) + 2
        tw, th = tw + tw % 2, th + th % 2
        frs = crop_clip(key, t0, n, cx, cy, span, tw, th)
        wr = Writer(f"{CLIPS}/v9_{name}.mp4", w=tw, h=th)
        for i, fr in enumerate(frs):
            wr.write(crt(fr, look, 900 + i))
        wr.close()
        print(f"   {name}: {n} frames {tw}x{th} ({look})")


# ------------------------------------------------------------------ 6. the factory card
def r_factory():
    """"A company that's never made a single physical product": things being made -- circuit boards on a bench, a
    press, an assembly line -- as one small clip for the card in the middle of the frame (the channel bug cropped out)."""
    a, b = TM.T["a3"] - 0.03, TM.T["product"]
    n = nf(a, b) + 2
    shots = [("BRL", 167.05, 880, 600, 1500), ("HOW", 192.74, 860, 600, 1500), ("BRL", 170.60, 880, 600, 1500)]
    per = n // len(shots)
    wr = Writer(f"{CLIPS}/v9_factory.mp4", w=960, h=540)
    for k, (key, t0, cx, cy, span) in enumerate(shots):
        m = per if k < len(shots) - 1 else n - per * (len(shots) - 1)
        for fr in crop_clip(key, t0, m, cx, cy, span, 960, 540):
            wr.write(fr)
    wr.close()


ALL = {"wall": r_wall, "articles": r_articles15, "mosaic": r_mosaic, "cuts": r_cuts, "products": r_products,
       "founders": r_founders, "factory": r_factory}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
