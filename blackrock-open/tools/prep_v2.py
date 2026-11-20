#!/usr/bin/env python3
"""v2 beats, rebuilt from the references (notes/REFERENCES_v2.md):

  glow     the panel from above after "you touch" -- the X-creative reel: faded-film grade, one snap push-in that
           settles, then people light up as flat white silhouettes with a soft bloom, a few at a time, stepped at
           24 fps (the reel's rate); no round light blobs
  orbit    "amongst them": the camera circling the table, the same grade and push, people lighting at random; on
           "is" the light stays on Fink alone, then the cut to him

Silhouettes: every person outlined by hand on a zoomed coordinate grid (the background remover and GrabCut both failed
on these wide shots: the remover keeps only one or two people, GrabCut takes chairs and table with them). The overhead
camera is still; in the circling shot each outline moves with its head's optical-flow track (a slow orbit, so a person
keeps their outline for the second it is used).

Also here: Dimon's tfg page, Solomon's Hemant flash, and every plain-cut shot from JPMorgan to BlackRock (shots).

Run: <venv>/bin/python -E -s tools/prep_v2.py [glow] [orbit] [dimon] [solomon] [shots]
"""
import sys

from common import *  # noqa: F401,F403
import timing as TM

OVER = f"{CUT}/over_seg.mp4"      # panel 954.40 s on (25 fps)
ORBIT = f"{CUT}/orbit_seg.mp4"    # panel 4.90 s on (25 fps)
WHITE = np.array([247, 244, 238], np.float32)


def nframes(beat):
    a, b = TM.B[beat]
    return round(b * FPS) - round(a * FPS)


def src_frames(src, f0, n):
    w, h, _ = probe(src)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"select='between(n\\,{f0}\\,{f0 + n - 1})'",
                          "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    k = len(raw) // (w * h * 3)
    return [np.frombuffer(raw[i * w * h * 3:(i + 1) * w * h * 3], np.uint8).reshape(h, w, 3) for i in range(k)]


# ------------------------------------------------------------------ the X-creative look
_XG = {}


def xgrade(img):
    """Faded film: low saturation, blacks lifted to ~21 with a warm-magenta cast, highlights held under ~240,
    the centre sharper than the edges, light grain added by the caller."""
    f = img.astype(np.float32)
    g = f.mean(axis=2, keepdims=True)
    f = g + (f - g) * 0.38
    f = 21 + f * (236 - 21) / 255.0
    sh = np.clip(1 - g / 120.0, 0, 1)
    f = f + sh * np.array([9, 0, 5], np.float32)
    if "m" not in _XG:
        _XG["m"] = radial(W / 2, H * 0.47, 330, 980, sy=0.85)[..., None]
        _XG["v"] = (1 - 0.16 * radial(W / 2, H / 2, 620, 1250, sy=0.75))[..., None]
    soft = cv2.GaussianBlur(f, (0, 0), 2.6)
    f = f * (1 - _XG["m"]) + soft * _XG["m"]
    return f * _XG["v"]


def snap_zoom(t, z1, tau=0.08, dur=0.33):
    """The reel's push-in: an exponential ease-out that has done ~80 % of the move after two frames at 24 fps."""
    if t <= 0:
        return 1.0
    u = (1 - math.exp(-min(t, dur) / tau)) / (1 - math.exp(-dur / tau))
    return 1.0 + (z1 - 1.0) * u


def q24(i):
    """Film frame i (60 fps) -> the time of the 24 fps step it falls on (the reel's motion updates 24 times a second)."""
    return math.floor(i / FPS * 24 + 1e-6) / 24


def light(img, mask, scale=1.0):
    """A person lit like the reel's screens: flat warm white inside the silhouette, a soft two-scale bloom around it
    (a tight halo and a wide glow, as on the Hemant reel's silhouette)."""
    m = mask[..., None]
    out = img * (1 - m) + WHITE * m
    b = (cv2.GaussianBlur(mask, (0, 0), 12 * scale) * 0.5 + cv2.GaussianBlur(mask, (0, 0), 36 * scale) * 0.32)[..., None]
    return out + (255 - out) * np.clip(b, 0, 1)


def schedule(n_people, start, end, seed, sizes=(2, 5), hold=(1, 4), allowed=None, apart=()):
    """24 fps steps from start to end (film frames, 60 fps): which people are lit on each step.
    Each light stays 1-4 steps; a new set every 1-3 steps; 2-5 lit at once (the reel's screens)."""
    rng = np.random.default_rng(seed)
    steps = {}
    s = math.ceil(start / FPS * 24)
    e = math.floor(end / FPS * 24)
    life = {}
    while s <= e:
        pool = [p for p in range(n_people) if (allowed is None or allowed(p, s)) and p not in life]
        pool = [p for p in pool if not any((p, q) in apart or (q, p) in apart for q in life)]
        want = int(rng.integers(sizes[0], sizes[1] + 1))
        while len(life) < want and pool:
            p = pool.pop(int(rng.integers(len(pool))))
            life[p] = int(rng.integers(hold[0], hold[1] + 1))
            pool = [q for q in pool if not ((p, q) in apart or (q, p) in apart)]
        steps[s] = sorted(life)
        life = {p: k - 1 for p, k in life.items() if k > 1}
        s += 1
    return steps


# ------------------------------------------------------------------ overhead: outlines by hand (static camera)
OVER_POLY = [  # panel 954.60 s (over_seg frame 5), read off 2x / 1.6x grids
    [(655, 116), (668, 118), (676, 128), (677, 143), (690, 150), (705, 160), (718, 172), (730, 185), (745, 200),
     (760, 210), (760, 228), (745, 228), (728, 215), (720, 205), (712, 212), (700, 222), (705, 238), (700, 255),
     (680, 255), (672, 240), (660, 228), (650, 215), (640, 200), (630, 185), (625, 165), (633, 152), (641, 147),
     (640, 132), (645, 121)],
    [(900, 78), (912, 79), (920, 88), (920, 100), (935, 104), (948, 112), (952, 130), (950, 150), (945, 168),
     (935, 180), (930, 195), (925, 210), (905, 212), (888, 205), (880, 190), (870, 175), (862, 155), (860, 130),
     (865, 112), (880, 103), (888, 99), (888, 88)],
    [(1108, 93), (1122, 95), (1130, 105), (1132, 118), (1145, 120), (1160, 125), (1165, 140), (1162, 160), (1158, 180),
     (1150, 198), (1140, 210), (1120, 213), (1105, 210), (1090, 205), (1085, 215), (1080, 228), (1065, 230),
     (1055, 220), (1053, 200), (1055, 180), (1058, 160), (1065, 140), (1078, 125), (1095, 118), (1096, 105)],
    [(1330, 186), (1345, 183), (1358, 190), (1362, 205), (1372, 210), (1380, 225), (1378, 250), (1370, 270),
     (1355, 290), (1340, 305), (1320, 310), (1300, 305), (1288, 290), (1285, 270), (1295, 250), (1310, 232),
     (1322, 215), (1326, 200)],
    [(1405, 342), (1420, 340), (1430, 348), (1433, 362), (1430, 375), (1440, 385), (1438, 410), (1433, 430),
     (1425, 448), (1405, 455), (1385, 450), (1375, 438), (1360, 432), (1352, 420), (1355, 408), (1370, 402),
     (1378, 390), (1390, 378), (1398, 368), (1398, 355)],
    [(1385, 568), (1405, 565), (1425, 572), (1435, 590), (1445, 600), (1460, 615), (1465, 640), (1462, 670),
     (1455, 700), (1440, 725), (1420, 738), (1395, 735), (1380, 720), (1375, 700), (1370, 680), (1360, 660),
     (1350, 640), (1338, 628), (1315, 625), (1305, 612), (1310, 598), (1330, 592), (1350, 590), (1368, 590), (1375, 580)],
    [(1290, 770), (1310, 768), (1325, 778), (1332, 795), (1345, 800), (1365, 812), (1378, 830), (1375, 855),
     (1360, 875), (1340, 892), (1315, 900), (1290, 897), (1270, 885), (1252, 868), (1238, 850), (1228, 832),
     (1232, 815), (1242, 800), (1240, 785), (1250, 775), (1265, 775), (1278, 778)],
    [(1040, 898), (1060, 895), (1075, 905), (1080, 890), (1072, 870), (1060, 845), (1058, 822), (1072, 818),
     (1085, 838), (1095, 860), (1108, 875), (1118, 895), (1118, 930), (1110, 960), (1095, 980), (1060, 988),
     (1020, 985), (990, 970), (980, 945), (982, 915), (990, 895), (992, 870), (1002, 862), (1012, 875), (1015, 895),
     (1030, 905)],
    [(735, 806), (752, 803), (768, 810), (776, 825), (785, 835), (795, 850), (805, 870), (810, 895), (805, 920),
     (790, 938), (765, 945), (735, 942), (712, 930), (702, 905), (703, 875), (712, 852), (725, 838), (728, 820)],
    [(470, 705), (490, 703), (508, 712), (515, 728), (525, 722), (545, 718), (560, 715), (585, 712), (605, 718),
     (612, 735), (605, 752), (590, 760), (575, 770), (570, 790), (555, 810), (535, 825), (510, 830), (488, 822),
     (470, 805), (455, 785), (448, 765), (452, 745), (460, 730), (463, 715)],
    [(400, 462), (420, 458), (440, 465), (455, 475), (470, 488), (482, 505), (492, 520), (500, 540), (508, 560),
     (512, 580), (510, 605), (498, 618), (480, 615), (460, 600), (440, 590), (420, 580), (400, 565), (388, 545),
     (382, 520), (385, 495), (392, 475)],
    [(530, 283), (545, 280), (558, 288), (563, 300), (562, 315), (575, 322), (590, 335), (600, 350), (615, 365),
     (622, 380), (612, 392), (595, 392), (585, 385), (580, 400), (570, 410), (545, 410), (525, 400), (510, 385),
     (498, 365), (495, 345), (505, 325), (520, 316), (522, 300)],
]

def r_glow():
    n = nframes("glow")  # 37
    src = src_frames(OVER, 5, 18)                      # 954.60 s on
    masks = [poly_mask(p, 0, 0) for p in OVER_POLY]
    sched = schedule(len(OVER_POLY), 7, n - 1, seed=15, sizes=(2, 5))
    cx, cy = 960, 500
    wr = Writer(f"{CLIPS}/r_glow.mp4")
    for i in range(n):
        t = i / FPS
        j = min(int(t * 25), len(src) - 1)             # the footage at its own 25 fps
        im = src[j].astype(np.float32)
        lit = sched.get(math.floor(i / FPS * 24 + 1e-6), [])
        for p in lit:
            im = light(im, masks[p])
        im = xgrade(im)
        z = snap_zoom(q24(i), 1.22)
        im = affine(im, z, cx, cy, cx, cy, border=(20, 18, 20))
        wr.write(im + grain(seed=900 + j, amt=3.2))
    wr.close()


# ------------------------------------------------------------------ the orbit: outlines moved with the head tracks
ORBIT_POLY = {  # outlines at orbit frame 0 (panel 4.90 s), 1920x1080 pixels, read off a 3x grid
    0: [(447, 470), (452, 460), (470, 457), (488, 459), (497, 468), (502, 480), (500, 495), (495, 505), (500, 512),
        (505, 525), (505, 560), (500, 600), (490, 640), (470, 655), (440, 655), (425, 630), (418, 600), (418, 560),
        (420, 530), (428, 512), (440, 500), (444, 488)],
    1: [(515, 480), (522, 474), (535, 473), (548, 476), (556, 484), (557, 495), (553, 505), (556, 512), (548, 518),
        (560, 535), (565, 555), (562, 570), (548, 580), (540, 610), (530, 645), (510, 650), (500, 620), (500, 560),
        (502, 530), (510, 512), (513, 495)],
    2: [(612, 470), (617, 463), (628, 461), (640, 465), (643, 475), (642, 488), (638, 497), (648, 505), (660, 515),
        (663, 530), (600, 530), (602, 512), (610, 500), (611, 488)],
    4: [(791, 476), (795, 468), (803, 465), (811, 469), (814, 478), (812, 488), (808, 493), (818, 497), (823, 505),
        (824, 520), (822, 538), (773, 538), (772, 520), (775, 503), (782, 495), (789, 490)],
    5: [(914, 478), (917, 469), (925, 466), (933, 469), (937, 478), (935, 489), (931, 494), (944, 498), (952, 505),
        (953, 525), (950, 540), (900, 540), (899, 520), (902, 505), (910, 497), (915, 492)],
    6: [(955, 500), (958, 485), (967, 474), (980, 470), (993, 473), (1003, 484), (1007, 500), (1005, 520), (1010, 540),
        (1000, 548), (960, 548), (952, 540), (953, 520)],
    7: [(1068, 482), (1072, 472), (1083, 468), (1095, 470), (1100, 478), (1098, 490), (1104, 495), (1113, 502),
        (1117, 515), (1118, 538), (1050, 538), (1050, 520), (1056, 503), (1066, 494)],
    8: [(1203, 478), (1207, 468), (1216, 464), (1226, 467), (1230, 476), (1229, 490), (1226, 498), (1238, 503),
        (1250, 512), (1255, 530), (1252, 550), (1200, 550), (1196, 530), (1197, 510), (1202, 500)],
    9: [(1287, 490), (1290, 475), (1300, 468), (1315, 466), (1328, 470), (1336, 480), (1338, 495), (1335, 510),
        (1342, 525), (1340, 560), (1338, 620), (1340, 700), (1330, 750), (1240, 750), (1225, 700), (1222, 650),
        (1240, 610), (1255, 560), (1265, 530), (1280, 515), (1285, 505)],
    10: [(1354, 478), (1358, 470), (1367, 467), (1376, 470), (1380, 480), (1378, 495), (1372, 503), (1380, 510),
         (1385, 525), (1385, 538), (1345, 538), (1347, 520), (1352, 505), (1355, 495)],
    11: [(1383, 478), (1390, 469), (1402, 466), (1414, 470), (1420, 480), (1420, 495), (1415, 508), (1425, 515),
         (1430, 530), (1428, 540), (1380, 540), (1382, 520), (1386, 508), (1384, 495)],
}
FINK = 5


ORBIT_HEADS = [(472, 478), (531, 490), (625, 474), (690, 515), (794, 480), (923, 484), (984, 504), (1082, 482),
               (1216, 486), (1312, 490), (1368, 484), (1404, 484)]   # head centres at orbit frame 0, marked on a grid


def orbit_tracks(n=30):
    """Each marked head followed through the orbit with pyramidal Lucas-Kanade; returns the displacement per frame."""
    frames = src_frames(ORBIT, 0, n)
    gray = [cv2.cvtColor(np.ascontiguousarray(f), cv2.COLOR_RGB2GRAY) for f in frames]
    p = np.float32(ORBIT_HEADS).reshape(-1, 1, 2)
    out = [p.reshape(-1, 2).copy()]
    for i in range(1, len(gray)):
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(gray[i - 1], gray[i], p, None, winSize=(41, 41), maxLevel=3,
                                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
        bad = st.reshape(-1) == 0
        nxt[bad] = p[bad]
        p = nxt
        out.append(p.reshape(-1, 2).copy())
    heads = np.stack(out)
    d = heads - heads[0]
    d[:, 7] = (d[:, 5] + d[:, 8]) / 2                    # Al-Rumayyan: hidden behind the chair from ~frame 12
    return d


def poly_mask(pts, dx, dy):
    m = np.zeros((H, W), np.uint8)
    p = np.round(np.float32(pts) + np.float32([dx, dy])).astype(np.int32)
    cv2.fillPoly(m, [p], 1, lineType=cv2.LINE_AA)
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.0)


def r_orbit():
    """The pause after "Goldman Sachs": the camera circling the table, graded, still. "Amongst": the reel's snap
    push-in and people start lighting at random; "them": a second push towards Fink, nothing lit while it moves;
    "is": the light stays on Fink alone -- then the cut to him on "this"."""
    n = nframes("search")                               # 90
    t0 = round(TM.B["search"][0] * FPS)
    pre = round(TM.T["amongst"] * FPS) - t0             # 37 frames before "Amongst"
    P = math.ceil(pre / FPS * 25)                       # 16 frames of the orbit before the marked one (4.90 s)
    pre_src = grab(PANEL, 4.90 - P / 25, P)
    src = pre_src + src_frames(ORBIT, 0, 24)
    d = orbit_tracks()
    keys = [k for k in ORBIT_POLY if k != FINK]
    k_is = round(TM.T["is"] * FPS) - t0
    k_them = round(TM.T["them"] * FPS) - t0
    nb = {(0, 1), (1, 2), (4, 6), (6, 7), (8, 9), (9, 10), (10, 11), (2, 4)}
    apart = {(keys.index(a), keys.index(b)) for a, b in nb if a in keys and b in keys}
    sched = schedule(len(keys), pre + 9, k_is - 3, seed=23, apart=apart)
    cx, cy = 915, 498
    wr = Writer(f"{CLIPS}/r_orbit.mp4")
    for i in range(n):
        g = i - pre                                     # frames since "Amongst"
        j = P + math.floor(g / FPS * 25 + 1e-6)         # index into src (25 fps)
        j = min(max(j, 0), len(src) - 1)
        jt = j - P                                      # orbit_seg frame (for the outlines)
        im = src[j].astype(np.float32)
        step = math.floor(i / FPS * 24 + 1e-6)
        if g < 0:
            lit = []
        elif i >= k_is:
            lit = [FINK]
        elif k_them <= i < k_them + 8:
            lit = []
        else:
            lit = [keys[p] for p in sched.get(step, [])]
            if math.floor(g / FPS * 24 + 1e-6) in (6, 7) and FINK not in lit:   # Fink once among the others
                lit = lit + [FINK]
        for k in lit:
            if jt >= 0:
                im = light(im, poly_mask(ORBIT_POLY[k], *d[jt, k]), scale=0.8)
        im = xgrade(im)
        z = 1.0
        if g >= 0:
            z = snap_zoom(q24(g), 1.25)
            if i >= k_them:
                z *= snap_zoom(q24(i - k_them), 1.24)
        im = affine(im, z, cx, cy, cx, cy, border=(20, 18, 20))
        wr.write(im + grain(seed=950 + j, amt=3.2))
    wr.close()


# ------------------------------------------------------------------ Dimon: the tfg page
TFG_RISE = [(0.0, 1.10), (0.1, 0.995), (0.2, 0.893), (0.3, 0.805), (0.4, 0.718), (0.5, 0.64), (0.6, 0.57),
            (0.7, 0.50), (0.8, 0.448), (0.9, 0.393), (1.0, 0.345), (1.1, 0.30), (1.2, 0.263), (1.3, 0.23),
            (1.4, 0.198), (1.5, 0.175), (1.6, 0.15), (1.7, 0.133), (1.8, 0.115), (1.9, 0.10), (2.0, 0.0925)]
PAGE = np.array([240, 225, 215], np.float32)       # the tfg page (measured)
CORAL = np.array([244, 138, 136], np.float32)      # its giant letters, solid (measured)
BODONI = f"{ROOT}/assets/fonts/BodoniModa-96-600.ttf"


def rise_frac(t):
    ts, fs = zip(*TFG_RISE)
    return float(np.interp(t, ts, fs))


def q30(t):
    return math.floor(t * 30 + 1e-6) / 30


def glyph_sprites(text, cap_h, sx, track):
    """Each letter of a tall condensed Didone line as its own alpha sprite with its x on the line (Bodoni Moda,
    compressed to the tfg letters' proportions: about 0.28 as wide as tall, hairline thin strokes)."""
    probe_f = ImageFont.truetype(BODONI, 200)
    l, t, r, b = probe_f.getbbox("H")
    size = int(round(200 * cap_h / (b - t)))
    f = ImageFont.truetype(BODONI, size)
    l, t, r, b = f.getbbox("H")
    out, x, word = [], 0.0, 0
    for ch in text:
        adv = f.getlength(ch) * sx
        if ch == " ":
            word += 1
        if ch != " ":
            gl, gt, gr, gb = f.getbbox(ch)
            im = Image.new("L", (gr - gl + 8, b - t + 8), 0)
            ImageDraw.Draw(im).text((4 - gl, 4 - t), ch, font=f, fill=255)
            a = np.asarray(im).astype(np.float32) / 255
            w2 = max(2, int(round(a.shape[1] * sx)))
            a = cv2.resize(a, (w2, a.shape[0]), interpolation=cv2.INTER_AREA)
            out.append({"ch": ch, "x": x + gl * sx - 4 * sx, "a": a, "w": word})
        x += adv + (track * cap_h if ch != " " else 0)
    return out, x


def despill(rgb, a):
    """Remove the green stage-light fringe along a cut-out's edge: in the soft edge band, green may not exceed
    the mean of red and blue."""
    edge = cv2.dilate(((a[..., 0] > 0.02) & (a[..., 0] < 0.98)).astype(np.uint8), np.ones((9, 9), np.uint8))[..., None]
    g = np.minimum(rgb[..., 1:2], (rgb[..., 0:1] + rgb[..., 2:3]) / 2 + 3)
    out = rgb.copy()
    out[..., 1:2] = np.where(edge > 0, g, rgb[..., 1:2])
    return out


def r_dimon_page():
    """"That's Jamie Dimon, the guy running": the tfg intro. Cream page; the giant name tiled across the width in
    tall condensed Didone caps, the letters arriving spread out and faint with a sideways smear, closing up and
    filling to coral, then the word growing slowly; Dimon's speaking cut-out rising from below on the reel's
    measured ~2 s ease-out until his head is ~9 % from the top. Everything moves on the reel's 30 fps steps."""
    a0, a1 = TM.B["dimon"][0], TM.T["jp"]
    n = round(a1 * FPS) - round(a0 * FPS)            # 118 frames, 1.97 s
    rng = np.random.default_rng(31)
    cap_h, sx, track = 520, 0.24, 0.09
    word_gap = 400                                    # the space behind his head, so JAMIE / DIMON read either side
    line = "DIMON JAMIE DIMON JAMIE DIMON JAMIE"
    sprites, _ = glyph_sprites(line, cap_h, sx, track)
    # put the gap between the 2nd JAMIE and the 3rd DIMON on his head (x ~1083); widen every word gap the same
    xs = np.array([sp["x"] for sp in sprites])
    wid = np.array([sp["w"] for sp in sprites])
    xs = xs + wid * (word_gap - 0.30 * cap_h)
    for sp, x in zip(sprites, xs):
        sp["x"] = x
    i_last_jamie = max(i for i in range(len(sprites)) if wid[i] == 3)
    i_first_dimon = min(i for i in range(len(sprites)) if wid[i] == 4)
    gap_mid = (sprites[i_last_jamie]["x"] + sprites[i_last_jamie]["a"].shape[1] + sprites[i_first_dimon]["x"]) / 2
    shift = 1083 - gap_mid
    for sp in sprites:
        sp["x"] += shift
    y_top = 140
    cxL, cyL = 960.0, y_top + cap_h / 2
    order = rng.permutation(len(sprites))
    appear = {int(o): 0.22 + 0.22 * k / max(1, len(sprites) - 1) for k, o in enumerate(order)}
    # the person
    person = grab(f"{CLIPS}/dimon_cut.webm", 0.0, 50, alpha=True)
    s_p, head0 = 0.97, 74
    paper_tex = cv2.GaussianBlur(np.random.default_rng(5).normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 0.8)
    paper_tex = cv2.resize(paper_tex, (W, H))[..., None] * 2.2
    page = PAGE + paper_tex
    page = page * (1 - 0.06 * radial(W / 2, H / 2, 700, 1300, sy=0.8))[..., None]

    def spread(t):       # 1.65 -> 1.0, closing up from 0.30 s to 1.15 s (ease-out)
        u = np.clip((t - 0.30) / 0.85, 0, 1)
        return 1.0 + 0.65 * (1 - u) ** 2

    def fill(t, t_in):   # faint (0.28) on arrival, solid by 1.15 s
        if t < t_in:
            return 0.0
        a = min(1.0, (t - t_in) / 0.08) * 0.28
        return a + (1 - 0.28) * float(np.clip((t - 0.55) / 0.6, 0, 1)) ** 1.3 * (a / 0.28)

    def grow(t):         # +25 % from 1.15 s to the cut
        return 1.0 + 0.25 * float(np.clip((t - 1.15) / 0.82, 0, 1))

    wr = Writer(f"{CLIPS}/r_dimon_page.mp4")
    for i in range(n):
        t = q30(i / FPS)
        tp = q30(max(0.0, (i - 1) / FPS))
        fr = page.copy()
        layer = np.zeros((H, W), np.float32)
        S, G = spread(t), grow(t)
        S_prev = spread(tp)
        for k, sp in enumerate(sprites):
            al = fill(t, appear[k])
            if al <= 0:
                continue
            a = sp["a"]
            xc = sp["x"] + a.shape[1] / 2
            x = cxL + (xc - cxL) * S
            v = abs((cxL + (xc - cxL) * S_prev) - x)               # px moved since the last step
            img = a
            if v > 2:                                              # the sideways smear while it travels
                kl = int(min(90, v * 1.4)) | 1
                ker = np.ones((1, kl), np.float32) / kl
                img = cv2.filter2D(np.pad(a, ((0, 0), (kl, kl))), -1, ker)
            # grow about the line's centre
            hh, ww = img.shape
            if G != 1.0:
                img = cv2.resize(img, (max(1, int(ww * G)), max(1, int(hh * G))), interpolation=cv2.INTER_LINEAR)
            gx = cxL + (x - cxL) * G - img.shape[1] / 2
            gy = cyL + (y_top - 4 - cyL) * G
            x0, y0 = int(round(gx)), int(round(gy))
            xa, ya = max(0, x0), max(0, y0)
            xb, yb = min(W, x0 + img.shape[1]), min(H, y0 + img.shape[0])
            if xb <= xa or yb <= ya:
                continue
            patch = img[ya - y0:yb - y0, xa - x0:xb - x0] * al
            layer[ya:yb, xa:xb] = np.maximum(layer[ya:yb, xa:xb], patch)
        # the reel's letters carry a soft pink glow and a faint echo beside them
        glow = cv2.GaussianBlur(layer, (0, 0), 9) * 0.35
        echo = np.roll(layer, 14, axis=1) * 0.18
        L = np.clip(np.maximum(layer, np.maximum(glow, echo)), 0, 1)[..., None]
        fr = fr * (1 - L) + CORAL * L
        # Dimon rises
        tr = i / FPS
        pf = person[min(int(tr * 25), len(person) - 1)].astype(np.float32)
        oy = rise_frac(t) * H - (H - (H - head0) * s_p)
        M = np.float32([[s_p, 0, W / 2 - s_p * W / 2], [0, s_p, H - s_p * H + oy]])
        pw = cv2.warpAffine(pf, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        pa = pw[..., 3:4] / 255.0
        rgb = despill(pw[..., :3], pa)
        fr = fr * (1 - pa) + rgb * pa
        wr.write(fr + grain(seed=1200 + int(t * 30), amt=2.4))
    wr.close()


# ------------------------------------------------------------------ Solomon: the Hemant reel's flash on a talking head
HEMANT = "vvvvvSSSvSSSSSvvSSSSvS"     # 24 fps steps: his speaking clip, then the reel's strobe (S = lit silhouette)
HEMANT_LEVEL = [0.80, 0.80, 0.83, 0.83, 0.74, 0.72, 1.0, 1.0, 0.96, 0.96, 0.94, 0.94, 0.94, 0.94]  # S steps, measured
CREAM = np.array([246, 240, 230], np.float32)


def r_solomon():
    """"David Solomon": his speaking close-up at the panel, then the Hemant reel's flash -- his whole silhouette
    turns flat glowing cream with a halo, the real picture showing through for a step now and then, the cream's
    brightness stepping every few frames, a white glitch block twice."""
    a0, a1 = TM.B["solomon"]
    n = round(a1 * FPS) - round(a0 * FPS)            # 56
    src = src_frames(f"{CUT}/solomon_seg.mp4", 8, 26)
    al = grab(f"{CLIPS}/solomon_cut.webm", 8 / 25, 26, alpha=True)
    rng = np.random.default_rng(41)
    wr = Writer(f"{CLIPS}/r_solomon.mp4")
    s_count = 0
    last_step = -1
    for i in range(n):
        step = math.floor(i / FPS * 24 + 1e-6)
        j = min(int(i / FPS * 25), len(src) - 1)
        im = src[j].astype(np.float32)
        kind = HEMANT[min(step, len(HEMANT) - 1)]
        if kind == "S":
            if step != last_step:
                s_count += 1
            lvl = HEMANT_LEVEL[min(s_count - 1, len(HEMANT_LEVEL) - 1)]
            m = al[min(j, len(al) - 1)][..., 3].astype(np.float32) / 255
            m = cv2.GaussianBlur(m, (0, 0), 1.5)
            op = 0.82 if lvl < 0.9 else 1.0              # the first flashes let his face show through
            col = CREAM * lvl
            im = im * (1 - m[..., None] * op) + col * (m[..., None] * op)
            halo = (cv2.GaussianBlur(m, (0, 0), 14) * 0.55 + cv2.GaussianBlur(m, (0, 0), 44) * 0.35)[..., None] * lvl
            im = im + (255 - im) * np.clip(halo * (1 - m[..., None]), 0, 1)
            if step in (8, 15):                          # the reel's white glitch blocks
                r2 = np.random.default_rng(100 + step)
                for _ in range(3):
                    x0, y0 = int(r2.integers(500, 1300)), int(r2.integers(250, 800))
                    w0, h0 = int(r2.integers(120, 420)), int(r2.integers(40, 120))
                    im[y0:y0 + h0, x0:x0 + w0] = CREAM
        last_step = step
        wr.write(im + grain(seed=1300 + j, amt=2.0))
    wr.close()


# ------------------------------------------------------------------ the plain-cut shots (real footage)
J2 = f"{ROOT}/../jpm-dimon/assets/clips2"
SHOTS = [  # (name, source, start s, seconds, crop filter, start given as frame count / fps rather than stream time)
    # "JP Morgan Chase": the bank running -- HQ with its flags, people at its doors, its NYSE board, its sign
    ("jp1", f"{J2}/HOW_69230_151.mp4", 0.00, 0.46, None, False),
    ("jp2", f"{J2}/LASTFAST_370_112.mp4", 0.00, 0.42, None, False),
    ("jp3", f"{J2}/MONT_1410_73.mp4", 0.00, 0.40, None, False),
    ("jp4", f"{J2}/MONT_2460_57.mp4", 0.00, 0.40, None, False),
    # "a part-time DJ": the user's video of him on stage as D-Sol, cropped from 9:16 to 16:9
    ("dj1", f"{DL}/solomon_dj.mp4", 1.48, 0.36, "crop=1080:608:0:470", True),
    ("dj2", f"{DL}/solomon_dj.mp4", 10.55, 0.36, "crop=1080:608:0:860", True),
    ("dj3", f"{DL}/solomon_dj.mp4", 23.85, 0.36, "crop=1080:608:0:620", True),
    # "and the CEO of Goldman Sachs": the panel's own title lands on "CEO"
    ("ceo", PANEL, 2802.86, 1.95, None, False),
    # "is this guy": Fink's close-up at the panel
    ("fink_pc", PANEL, 1186.20, 0.98, None, False),
    # "the man who": Fink walking in New York with his security (the clean run between the edit's mattes)
    ("fink_walk", f"{DL}/m_fink2.mp4", 5.44, 0.50, None, True),
    # "runs the most evil": the interview, his face steadiest here (the red square lands on it)
    ("fink_box", f"{DL}/fink_interview.mp4", 53.50, 1.12, None, False),
    # "company in the world": BlackRock's lobby (after the edit's punch-in), its building and flags, its doors;
    # "BlackRock.": the steel letters on its facade
    ("br_lobby", f"{DL}/m_finance.mp4", 12.26, 0.64, None, True),
    ("br_bldg", f"{DL}/blackrock_short.mp4", 10.48, 0.62, None, True),
    ("br_doors", f"{DL}/blackrock_short.mp4", 4.30, 0.64, None, True),
    ("br_sign", f"{DL}/blackrock_short.mp4", 0.00, 0.86, None, True),
]


def shots(names=None):
    for name, src, t0, dur, vf, fc in SHOTS:
        if names and name not in names:
            continue
        ss = t0 + (stream_start(src) if fc else 0.0)
        filt = ([vf] if vf else []) + ["scale=1920:1080:flags=lanczos", "setsar=1", "fps=60"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-i", src, "-t", f"{dur:.3f}", "-vf",
                        ",".join(filt), "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", f"{CLIPS}/v2_{name}.mp4"], check=True)
        print("  ", name)


ALL = {"glow": r_glow, "orbit": r_orbit, "dimon": r_dimon_page, "solomon": r_solomon, "shots": shots}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
