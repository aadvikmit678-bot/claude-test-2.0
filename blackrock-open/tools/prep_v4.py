"""v4 renderers (the user's notes of Nov 21, night).

  finkflip  "the man who runs the most evil": reel DeHkRtts3bI's opening -- a photo every 2 frames (at 30 fps), each
            tilted out of perspective, zoom-pushed and blurred on the cut, light leaks and a negative frame; Fink's
            pictures (colour and black-and-white) from the user's downloads. No red box.
  cartel4   "$60 trillion" runs longer; the cartel video cuts in on its table flash and, a split second later, to the
            main frame (the faces) on "cartel".
  dimon4    "That's Jamie Dimon, the guy running": refff's "if intelligence is automated", measured frame by frame --
            nothing before the flash; wash, white silhouette, wash, silhouette, normal, silhouette; the band comes in
            at the flash and eases down (15 % -> 27 % -> 33 % -> 38.6 % of the height, offset to the name line);
            the name flickers in (ghost, gone, half, gone, solid) in Inter Display SemiBold, white in the red band.
  solomon4  the Solomon intro without the vertical "a part-time DJ" (the captions write it now).
  ceo4      "the CEO of Goldman Sachs": exactly the JPMorgan device (flipbook of six 5 frames each, the two-up collage
            with its negatives, the logo, the grid), with no shot repeated: Solomon at the panel, his DJ nights, the
            Goldman sign once.
  dj4       "a part-time DJ": his decks and his crowd (the user's new clip, its caption-free tail).
  orbit4    "Amongst them": the table circling, clean (no flashing lights); a white light streak at its end.
  spot4     "is this guy": the spotlight reel's move -- the face flash, then the room goes dark and the frame punches
            in on his face (about 1.75x, as the reel), still pushing in slowly.
  panel     the opening's four panelists: Fink, Schwarzman, then Jamie Dimon (3rd), Ray Dalio (4th).
  founders  the founders block (Think School's columns, Jensen, Gates, Jobs): the money texture at low opacity in
            difference, and the soft corner blur (centre focus).
"""
import math
import subprocess
import sys

import cv2
import numpy as np

import prep_v3 as P
import timing as TM
from common import CLIPS, DL, FPS, H, PANEL, W, Writer, center_focus, cover, grab, grain

V3 = P.V3
NEW2 = f"{V3}/new2/dimon_solomon.mp4"
PIN = f"{V3}/pin"
nf = P.nf


def rng(seed):
    return np.random.default_rng(seed)


# ------------------------------------------------------------------ finkflip
PH = f"{DL}/v4/fink_photos"          # the user's Larry Fink photos (Drive, Nov 21 late night)
FLIP_SRC = [  # (file, time s, crop) -- Fink: the user's new photos first, between stills of his videos
    (f"{PH}/p06.png", 0, None), (f"{DL}/fink_edit3.mp4", 9.0, None), (f"{PH}/p03_foxbusiness.png", 0, None),
    (f"{PH}/p09.png", 0, None), (f"{DL}/m_fink1.mp4", 4.3, None), (f"{PH}/p10.png", 0, None),
    (f"{PH}/p11.png", 0, None), (f"{DL}/fink_edit3.mp4", 13.3, None), (f"{PH}/p01.png", 0, None),
    (f"{PH}/p12.png", 0, None), (f"{DL}/m_fink1.mp4", 12.2, None), (f"{PH}/p08.png", 0, None),
    (f"{PH}/p04.webp", 0, None), (f"{DL}/fink_edit3.mp4", 15.2, None), (f"{PH}/p05.png", 0, None),
    (f"{PH}/p02.png", 0, None), (f"{DL}/m_fink1.mp4", 2.7, None), (f"{DL}/fink_edit3.mp4", 8.3, None),
    (f"{DL}/m_fink1.mp4", 8.7, None), (f"{DL}/fink_edit3.mp4", 19.2, None), (PANEL, 1186.2, None),
    (f"{DL}/fink_edit3.mp4", 11.6, None),
    (f"{DL}/m_fink1.mp4", 13.6, None), (f"{DL}/fink_edit3.mp4", 21.8, None), (PANEL, 1188.0, None),
]


def still(path, t, crop=None):
    vf = (crop + "," if crop else "") + "setsar=1"
    f = grab(path, t, 1, vf=vf)[0].astype(np.float32)
    return cover(f, W, H)


def tilt(img, ax, ay, k, dx, dy, roll):
    """The picture as a card turned in 3D (ax, ay: degrees about the vertical / horizontal axis), scaled k, shifted
    (dx, dy), rolled; the uncovered corners take a blurred, darker copy of the same picture."""
    fx = 1400.0
    pts = np.float32([[-W / 2, -H / 2, 0], [W / 2, -H / 2, 0], [W / 2, H / 2, 0], [-W / 2, H / 2, 0]])
    a, b, r = math.radians(ay), math.radians(ax), math.radians(roll)
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Rz = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]])
    q = pts @ (Rz @ Ry @ Rx).T
    z = q[:, 2] + fx
    dst = np.float32(np.stack([q[:, 0] * fx / z * k + W / 2 + dx, q[:, 1] * fx / z * k + H / 2 + dy], axis=1))
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), dst)
    out = cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    m = cv2.warpPerspective(np.ones((H, W), np.float32), M, (W, H), flags=cv2.INTER_LINEAR)
    back = cv2.GaussianBlur(cover(img, W, H, scale=1.25), (0, 0), 28) * 0.45
    return out * m[..., None] + back * (1 - m[..., None])


def zoom_blur(img, amt, n=7):
    acc = np.zeros_like(img)
    for s in range(n):
        k = 1 + amt * s / max(1, n - 1)
        acc += cover(img, W, H, scale=k)
    return acc / n


def dir_blur(img, dx, dy):
    L = int(max(3, min(90, math.hypot(dx, dy)))) | 1
    ker = np.zeros((L, L), np.float32)
    c = L // 2
    ang = math.atan2(dy, dx)
    for s in range(L):
        t = s - c
        x, y = int(round(c + t * math.cos(ang))), int(round(c + t * math.sin(ang)))
        if 0 <= x < L and 0 <= y < L:
            ker[y, x] = 1
    ker /= ker.sum()
    return cv2.filter2D(img, -1, ker, borderType=cv2.BORDER_REFLECT)


def leak(seed):
    r = rng(seed)
    a = P.radial(r.uniform(0.1, 0.9) * W, r.uniform(0.0, 1.0) * H, r.uniform(150, 350), r.uniform(700, 1200))
    col = np.array([255, r.uniform(170, 220), r.uniform(110, 160)], np.float32)
    return a[..., None] * col


def r_finkflip():
    a0, a1 = TM.B["walk"][0], TM.B["box"][1]
    n = nf(a0, a1)
    pics = [np.clip(still(p, t, c), 0, 255).astype(np.uint8) for p, t, c in FLIP_SRC]   # uint8: memory
    hold = 4                                          # 2 frames at 30 fps, as the reel
    wr = Writer(f"{CLIPS}/r_finkflip.mp4")
    for i in range(n):
        k, j = divmod(i, hold)
        img = pics[k % len(pics)].astype(np.float32)
        r = rng(900 + k)
        ax, ay = r.uniform(-16, 16), r.uniform(-9, 9)
        roll = r.uniform(-4, 4)
        kz = r.uniform(1.06, 1.22) * (1 + 0.025 * j)  # each picture keeps pushing in for its two frames
        dx, dy = r.uniform(-60, 60) + 18 * j, r.uniform(-40, 40) - 10 * j
        fr = tilt(img, ax * (1 - 0.25 * j), ay, kz, dx, dy, roll)
        if j == 0:                                    # the cut lands blurred: a whip or a zoom, alternately
            fr = dir_blur(fr, r.uniform(30, 80), r.uniform(-20, 20)) if k % 2 else zoom_blur(fr, 0.09)
        if k % 5 == 3 and j < 2:                      # a light leak washing in
            fr = fr * 0.75 + leak(70 + k) * 0.6
        if k in (6, 15) and j == 0:                   # the reel's negative frame
            fr = 255 - np.clip(fr, 0, 255)
        fr = center_focus(np.clip(fr, 0, 255), zoom=0.02, gblur=2.6)
        wr.write(fr + grain(seed=5000 + i, amt=3.4))
    wr.close()
    print(f"   finkflip: {n} frames, {math.ceil(n / hold)} pictures")


# ------------------------------------------------------------------ cartel4
def r_cartel4():
    a0, a1 = TM.B["cartel"]
    n = nf(a0, a1)
    k_c = round(TM.T["cartel"] * FPS) - round(a0 * FPS)   # the main frame from "cartel"
    src = grab(f"{V3}/cartel_user.mp4", 0.0, 66)
    wr = Writer(f"{CLIPS}/r_cartel4.mp4")
    for i in range(n):
        j = min(14 + int(i * 24 / FPS), 16) if i < k_c else 28 + int((i - k_c) * 24 / FPS)
        wr.write(src[min(j, len(src) - 1)].astype(np.float32))
    wr.close()
    print(f"   cartel4: flash frames 14-16 for {k_c} frames, then the faces ({n - k_c})")


# ------------------------------------------------------------------ dimon4
INTER_SB = f"{P.FONTS}/InterDisplay-SemiBold.otf"
REF_BAND = [(4, .151), (8, .269), (10, .276), (11, .308), (13, .325), (14, .330), (18, .333), (19, .359), (20, .362),
            (24, .375), (30, .383), (39, .386)]         # refff 0-1.3 s at 30 fps: the band's lower edge / height
REF_BASE = 0.344                                       # its word's baseline (fraction of the height)
REF_WORD = {10: 0.2, 11: 0.0, 12: 0.5, 13: 0.0, 14: 0.93}   # "intelligence": ghost, gone, half, gone, solid (then 1)
# the flashes, per refff frame: "wash" (all towards white), "sil" (his silhouette flat white), None
REF_FLASH = {4: "wash", 5: "sil", 6: "wash2", 7: "sil", 8: None, 9: "sil"}


def r_dimon4():
    n = P.beat_frames("dimon")
    t0 = round(TM.B["dimon"][0] * FPS)
    rel = lambda w: round(TM.T[w] * FPS) - t0
    frs = P.person_frames("dimon", n, 1.2, 0.0, -60.0, clean=True)
    name_base = 392
    name_a, name_box = P.word_layer("Jamie Dimon", INTER_SB, 150, 104, name_base)
    that_a, that_box = P.word_layer("That’s", P.SERIF_I, 84, 112, int(name_box[1]) - 18)
    off = name_base / H - REF_BASE
    words = [("the", "the1"), ("guy", "guy1"), ("running", "running")]
    serif_base = int((REF_BAND[-1][1] + off) * H) + 108
    layers, x = [], 112
    for w, key in words:
        a, box = P.word_layer(w, P.SERIF, 138, x, serif_base)
        layers.append((a, box, rel(key)))
        x = box[2] + 36
    wr = Writer(f"{CLIPS}/r_dimon4.mp4")
    rf_keys = [k for k, _ in REF_BAND]
    rf_vals = [v for _, v in REF_BAND]
    for i in range(n):
        img, pa = frs[i]
        rf = i / 2.0                                   # refff frame (30 fps) at this 60 fps frame
        bg = img.copy()
        if rf >= 4:
            edge = (np.interp(rf, rf_keys, rf_vals) + off) * H
            band = np.zeros((H, W), np.float32)
            band[:int(edge)] = 1.0
            band = cv2.GaussianBlur(band, (0, 0), 1.2)
            bg = P.over_color(bg, band, P.RED)
        # "That's": its small square on the flash (refff "if"), the word from the next wash
        if 4 <= rf < 6:
            sq = np.zeros((H, W), np.float32)
            sq[int(that_box[1]) + 8:int(that_box[1]) + 40, int(that_box[0]):int(that_box[0]) + 32] = 1
            bg = P.over_color(bg, sq, P.WHITE)
        elif rf >= 6:
            bg = P.over_color(bg, that_a, P.WHITE)
        # "Jamie Dimon": flickers in, in place, no blur
        f30 = int(rf)
        op = REF_WORD.get(f30, 1.0 if f30 > 14 else 0.0)
        if op > 0:
            bg = P.over_color(bg, name_a * op, P.WHITE)
        fg = img
        kind = REF_FLASH.get(f30)
        if kind == "wash":
            bg = bg * 0.6 + 255 * 0.4
            fg = fg * 0.55 + 255 * 0.45
        elif kind == "wash2":
            bg = bg * 0.35 + 255 * 0.65
            fg = fg * 0.3 + 255 * 0.7
        elif kind == "sil":
            fg = fg * 0.05 + 255 * 0.95
        fr = bg * (1 - pa[..., None]) + fg * pa[..., None]
        for a, box, k in layers:                       # "the guy running": ghost, white block, the word with its glow
            st = P.block_entrance(i, k)
            if st == "ghost":
                fr = P.over_color(fr, a * 0.35, P.WHITE)
            elif st == "block":
                fr = P.glow_text(fr, P.block_layer(box), (255, 255, 255), glow=0.8)
            elif st == "word":
                sh = cv2.GaussianBlur(a, (0, 0), 9)
                fr = fr * (1 - 0.5 * np.clip(sh * 1.5, 0, 1))[..., None]
                fr = P.glow_text(fr, a, (246, 244, 240), glow=0.75)
        wr.write(fr + grain(seed=1700 + i, amt=2.2))
    wr.close()


# ------------------------------------------------------------------ CEO of Goldman Sachs, exactly the JPMorgan device
def gs_logo():
    """Goldman Sachs' mark: the light-blue square with the name in white serif, centred, glowing like the Chase logo."""
    a = np.zeros((H, W), np.float32)
    s = 330
    x0, y0 = (W - s) // 2, (H - s) // 2
    a[y0:y0 + s, x0:x0 + s] = 1.0
    sq = np.zeros((H, W, 3), np.float32)
    glow = cv2.GaussianBlur(a, (0, 0), 30)
    sq = sq + np.array([120, 160, 220], np.float32) * np.clip(glow * 1.4, 0, 1)[..., None]
    sq = P.over_color(sq, a, (115, 153, 198))
    for line, yb in (("Goldman", y0 + 150), ("Sachs", y0 + 262)):
        m, base, _ = P.text_mask(line, f"{P.FONTS}/LiberationSerif-Regular.ttf", 92, pad=10)
        t = np.zeros((H, W), np.float32)
        P.paste_alpha(t, m, (W - m.shape[1]) / 2, yb - base)
        sq = P.over_color(sq, t, (255, 255, 255))
    return sq


def r_ceo4():
    """Memory-lean: each picture grabbed only for the frames the device shows it (uint8, the collage halves and the
    grid cells already at their size), the flip pictures padded with references (no copies)."""
    n = P.beat_frames("ceo")
    k = 30
    band = "crop=840:472:0:200"

    def U(src, t, m, crop=None, fc=False, size=None):
        out = [np.clip(f, 0, 255).astype(np.uint8) for f in P.live(src, t, m, crop=crop, fc=fc)]
        return [cover(f, *size) for f in out] if size else out

    flip_src = [(PANEL, 2826.4, None, False), (f"{V3}/goldman.mp4", 2.0, None, False), (NEW2, 16.3, band, False),
                (PANEL, 2802.9, None, False), (NEW2, 23.3, band, False),
                (f"{DL}/solomon_dj.mp4", 1.48, "crop=1080:608:0:470", True)]
    flip = []
    for j, (src, t, crop, fc) in enumerate(flip_src):        # picture j shows on frames 5j..5j+4
        fr = U(src, t + 5 * j / FPS, 5, crop=crop, fc=fc)
        flip.append([fr[0]] * (5 * j) + fr)
    m = n - k
    collage = (U(PANEL, 2827.6 + 10 / FPS, m, size=(W // 2, H)),
               U(NEW2, 19.4 + 20 / FPS, m, crop="crop=840:472:0:120", size=(W // 2, H)))
    slots, cw, ch = P.grid_cells()
    cell_src = [(NEW2, 22.2 + 20 / FPS, "crop=840:472:0:160", False), (PANEL, 2802.9 + 30 / FPS, None, False),
                (NEW2, 26.4 + 20 / FPS, band, False), (NEW2, 23.3 + 40 / FPS, band, False),
                (f"{DL}/solomon_dj.mp4", 1.48 + 30 / FPS, "crop=1080:608:0:470", True), (NEW2, 16.3 + 40 / FPS, band, False)]
    cells = []
    for c, (src, t, crop, fc) in enumerate(cell_src):
        x, y, w_, h_ = slots[c]
        cells.append(U(src, t, max(1, m - 15 - 5 * c), crop=crop, fc=fc, size=(w_, h_)))
    P.altman_device("r_ceo4", n, flip, collage, gs_logo(), cells, "Goldman Sachs", seed=9)


def r_dj4():
    a, b = TM.B["dj"]
    m = TM.F((a + b) / 2)
    for name, t, (s, e), crop in (("v4_dj_a", 18.6, (a, m), "crop=840:472:0:220"),
                                   ("v4_dj_b", 24.5, (m, b), "crop=840:472:0:140")):
        k = nf(s, e)
        fr = P.live(NEW2, t, k, crop=crop)
        wr = Writer(f"{CLIPS}/{name}.mp4")
        for f in fr:
            wr.write(f + grain(seed=3100 + int(t * 10), amt=2.0))
        wr.close()


# ------------------------------------------------------------------ orbit4 / spot4
def streak(fr, u, seed=11):
    """A white light streak across the frame (the spotlight reel's 2.27 s transition): u 0..1 its sweep."""
    r = rng(seed)
    y = H * (0.42 + 0.1 * r.uniform(-1, 1))
    x = -400 + u * (W + 800)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    core = np.exp(-((yy - y) / 10) ** 2) * np.exp(-((xx - x) / 700) ** 2)
    halo = np.exp(-((yy - y) / 70) ** 2) * np.exp(-((xx - x) / 900) ** 2)
    a = np.clip(core * 1.0 + halo * 0.55, 0, 1)[..., None]
    return fr * (1 - a) + 255 * a


def r_orbit4():
    n = P.beat_frames("orbit")
    src = P.V2.src_frames(P.V2.ORBIT, 0, 40)
    Z, cx, cy = 1.25 * 1.24, 915, 498
    wr = Writer(f"{CLIPS}/r_orbit4.mp4")
    for i in range(n):
        j = min(int(i / FPS * 25), len(src) - 1)
        im = P.V2.xgrade(src[j].astype(np.float32))
        z = Z * (1 + 0.035 * i / n)                   # a slow push in, no flashing lights
        im = P.affine(im, z, cx, cy, cx, cy, border=(20, 18, 20))
        if i >= n - 5:                                 # the light streak that carries into the group picture
            im = streak(im, (i - (n - 5)) / 9)
        wr.write(im + grain(seed=2100 + j, amt=3.0))
    wr.close()


def r_spot4():
    a0, a1 = TM.B["thisguy"]
    n = nf(a0, a1)
    from PIL import Image
    img = np.asarray(Image.open(f"{V3}/fink_spot.png").convert("RGB")).astype(np.float32)
    ih, iw = img.shape[:2]
    k = H / ih
    big = cv2.resize(img, (int(round(iw * k)), H), interpolation=cv2.INTER_CUBIC)
    x0 = int(min(max(836 * k - W / 2, 0), big.shape[1] - W))
    base = big[:, x0:x0 + W].copy()
    fx, fy, fw, fh = P.find_face(base, (836 * k - x0, 430 * k), 120 * k)
    cx, cy = fx + fw / 2, fy + fh / 2
    pad = 0.18
    bx0, by0 = int(fx - fw * pad), int(fy - fh * pad)
    bx1, by1 = int(fx + fw * (1 + pad)), int(fy + fh * (1 + pad))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - cx) / (fw * 0.95)) ** 2 + ((yy - cy - fh * 0.08) / (fh * 1.15)) ** 2)
    lit = np.clip(1 - P.smooth((r - 0.55) / 0.75), 0, 1)[..., None]
    g = base.mean(axis=2, keepdims=True)
    dark = (g + (base - g) * 0.7) * 0.2
    spot = dark * (1 - lit) + base * lit
    k_flash = 3                                         # the face flash right after the light streak lands
    ty = H * 0.43                                       # where his face sits once the frame has punched in
    wr = Writer(f"{CLIPS}/r_spot4.mp4")
    for i in range(n):
        j = i - k_flash
        if i < 2:
            fr = streak(base, (i + 5) / 9)
        elif j < 0:
            fr = base
        elif j < 4:
            fr = base.copy()
            fr[by0:by1, bx0:bx1] = 250
        elif j < 6:
            fr = P.negative(base)
        elif j < 10:
            fr = base.copy()
            fr[by0:by1, bx0:bx1] = P.negative(base[by0:by1, bx0:bx1])
        elif j < 12:
            fr = dark.copy()
            fr[by0:by1, bx0:bx1] = P.negative(base[by0:by1, bx0:bx1])
        else:                                           # dark, punched in ~1.75x on his face, still pushing in
            u = (j - 12) / max(1, n - k_flash - 12)
            z = 1.75 * (1 + 0.09 * u)
            fr = P.affine(spot, z, cx, cy, W / 2, ty, border=(8, 6, 6))
        wr.write(fr + grain(seed=2600 + i, amt=2.6))
    wr.close()
    print(f"   spot4: Fink's face {fx},{fy} {fw}x{fh}; after the punch-in its centre at ({W / 2:.0f},{ty:.0f})")
    return (fx, fy, fw, fh)


# ------------------------------------------------------------------ the opening's panelists
def r_panel4():
    """Cut 3 Jamie Dimon (the panel, him talking), cut 4 Ray Dalio; the clips are cut to their slots by build.py's
    times (the same lengths as before)."""
    for name, t0, dur in (("v4_ob_dimon", 916.3, 0.92), ("v4_ob_dalio", 729.3, 1.12)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", PANEL, "-t", f"{dur + 0.1:.3f}",
                        "-vf", "scale=1920:1080:flags=lanczos,setsar=1,fps=60", "-an", "-c:v", "libx264", "-preset",
                        "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        f"{CLIPS}/{name}.mp4"], check=True)


# ------------------------------------------------------------------ the founders block: texture + corner blur
TEX = f"{PIN}/money_tex.mp4"


def texture_pass(name, opacity=0.16, seed=0):
    """The money texture (the user's "can be used in difference effect in bg, less opacity") over a clip, in
    difference at low opacity, and the soft corner blur."""
    path = f"{CLIPS}/{name}.mp4"
    src = grab(path, 0.0, 400)
    tex = grab(TEX, 1.0 + seed * 0.7, len(src), fps=FPS, size=(W, H))
    tmp = f"{CLIPS}/{name}.tex.mp4"
    wr = Writer(tmp)
    for i, f in enumerate(src):
        f = f.astype(np.float32)
        t = tex[min(i, len(tex) - 1)].astype(np.float32)
        f = f * (1 - opacity) + np.abs(f - t) * opacity
        f = center_focus(f, zoom=0.014, gblur=2.4)
        wr.write(f)
    wr.close()
    subprocess.run(["mv", tmp, path], check=True)
    print(f"   {name}: texture + corner blur ({len(src)} frames)")


def r_founders():
    for k, name in enumerate(["v3_tsg_nv", "v3_tsg_ms", "v3_tsg_ap", "v3_r1_jensen", "v3_r1_gates", "v3_r1_jobs"]):
        texture_pass(name, opacity=0.14 if "tsg" in name else 0.18, seed=k)


ALL = {"finkflip": r_finkflip, "cartel4": r_cartel4, "dimon4": r_dimon4, "ceo4": r_ceo4, "dj4": r_dj4,
       "orbit4": r_orbit4, "spot4": r_spot4, "panel4": r_panel4, "founders": r_founders}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
