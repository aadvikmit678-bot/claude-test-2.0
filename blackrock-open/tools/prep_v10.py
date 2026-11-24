#!/usr/bin/env python3
"""v10 renderers (Nov 24, evening): the opening on the user's second new recording ("new audio.mp3"), each pre-rendered
at 60 fps, 1920x1080 (the type is in the compositions).

  wall      "This is the most": reel DgHoW0vhPvb's opening (read frame by frame at 30 fps): a curved, smeared pan across
            a wall of pictures (3 reel frames), the same wall washed grey (2), the wall itself -- a cinematic plate behind
            (theirs a brain scan, ours falling banknotes) and photographs of every size cut in one after another, some
            of the man, most of them cinematic stills -- curved like a lens, the edges soft (21 frames), then a white
            photocopy texture (2) and a false-colour frame of the shot that follows (2)
  fink      the Kalanick reel's "This guy just got handed" frame: the user's photo of Fink (larry new image.png) cut out
            in front of the line, a dark LED-dot wall behind him until the flash, then the photo's own warm glow with
            light flecks at the sides (plates on a canvas larger than the frame, so the zoom never shows an edge)
  evil      "or how people call it, the most evil": the red horned scene as v6 had it (the user: "like the original
            version ... a bit slow"): the whole rise under the small words, the cut to the close-up two frames before
            "most", MOST and EVIL behind him; no grain
  company   "company ever": reel DgHoW0vhPvb's "But behind ... all that" (8.4-9.1 s): a black-and-white crowd in a haze
            (ours the old NYSE floor), the words at the sides (in the composition)
  built     "built.": its "NOISE" (9.13-9.8 s): a dark black-and-white shot (ours BlackRock's letters on its tower,
            slowed), the word in red in the composition
  cartel    the cartel clip from its faces only (no table flash next to the $15 trillion cutouts: the user)

Run: <venv>/bin/python -E -s tools/prep_v10.py [names...]
"""
import sys

from common import *  # noqa: F401,F403
import timing as TM
import prep_v6 as P6

V10 = f"{DL}/v10"
PIN = os.path.abspath(f"{ROOT}/../dimon-src/money_pinterest videos")
DIR = os.path.abspath(f"{ROOT}/../dimon-src/_direct")
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


def still(key, t, cx, cy, zoom, tw, th, look="c"):
    """one frame of a source, cropped to the tile's aspect around (cx, cy) (fractions), zoom = crop width / the
    largest crop of that aspect; graded a little ('bw': black and white)"""
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
    else:
        out = grade(out, sat=1.05, contrast=1.06)
    return np.clip(out, 0, 255)


# ------------------------------------------------------------------ the Fink frame's plates
FW, FH = 2200, 1238                     # the plates' canvas: the frame is its middle 1920x1080
FX0, FY0 = (FW - W) // 2, (FH - H) // 2
PHOTO_S = 1.0                           # the user's photo (1536x1024) at full size, bottom on the canvas's bottom edge


def fink_place():
    pw, ph = round(1536 * PHOTO_S), round(1024 * PHOTO_S)
    return (FW - pw) // 2, FH - ph, pw, ph


def fink_assets():
    photo = np.asarray(Image.open(f"{V10}/larry_new_image.png").convert("RGB")).astype(np.float32)
    cut = np.asarray(Image.open(f"{V10}/larry_new_cut.png").convert("RGBA")).astype(np.float32)
    px, py, pw, ph = fink_place()
    photo_s = cv2.resize(photo, (pw, ph), interpolation=cv2.INTER_AREA)
    cut_s = cv2.resize(cut, (pw, ph), interpolation=cv2.INTER_AREA)
    # the cut-out on the canvas (RGBA)
    cutc = np.zeros((FH, FW, 4), np.float32)
    cutc[py:py + ph, px:px + pw] = cut_s
    al = cutc[..., 3:4] / 255.0
    # plate B: the photo's own dark warm-glow background carried out to the canvas, the photo feathered into it, warm
    # light flecks and a warm glow at the sides (the Kalanick frame after its flash)
    cover_k = max(FW / 1536, FH / 1024) * 1.02
    cov = cv2.resize(photo, (round(1536 * cover_k), round(1024 * cover_k)), interpolation=cv2.INTER_CUBIC)
    oy, ox = (cov.shape[0] - FH) // 2, (cov.shape[1] - FW) // 2
    base = cv2.GaussianBlur(cov[oy:oy + FH, ox:ox + FW], (0, 0), 48) * 0.55
    ramp = np.ones((ph, pw), np.float32)
    fe = 150
    xs = np.minimum(np.arange(pw), np.arange(pw)[::-1]).astype(np.float32)
    ramp *= np.clip(xs / fe, 0, 1)[None, :]
    ramp *= np.clip(np.arange(ph, dtype=np.float32) / fe, 0, 1)[:, None]
    ramp = smooth(ramp)[..., None]
    plate_b = base.copy()
    plate_b[py:py + ph, px:px + pw] = base[py:py + ph, px:px + pw] * (1 - ramp) + photo_s * ramp
    yy, xx = np.mgrid[0:FH, 0:FW].astype(np.float32)
    warm = np.float32([255, 140, 60])
    for sx in (0.0, FW):                                   # a soft warm glow on both sides
        r = np.sqrt(((xx - sx) / 760) ** 2 + ((yy - FH * 0.62) / 620) ** 2)
        plate_b += warm * (0.30 * np.exp(-r * r * 2.2))[..., None]
    rng = np.random.default_rng(1124)
    bok = np.zeros((FH, FW, 3), np.float32)
    for _ in range(150):                                  # light flecks, out of focus, more at the sides
        side = rng.random() < 0.5
        x = rng.normal(0.10 if side else 0.90, 0.10) * FW
        y = rng.uniform(0.15, 0.95) * FH
        rad = rng.uniform(5, 26)
        a = rng.uniform(0.15, 0.55)
        col = np.float32([255, rng.uniform(120, 190), rng.uniform(40, 90)])
        cv2.circle(bok, (int(x), int(y)), int(rad), [float(c * a) for c in col], -1, cv2.LINE_AA)
    bok = cv2.GaussianBlur(bok, (0, 0), 3.0)
    plate_b = plate_b + bok * (1 - al)
    # plate A: before the flash, a dark navy LED-dot wall (the Kalanick frame's first background), soft
    a_img = np.zeros((FH, FW, 3), np.float32)
    a_img[:] = np.float32([7, 10, 24])
    step = 30
    for gy in range(step // 2, FH, step):
        for gx in range(step // 2, FW, step):
            b = 0.35 + 0.65 * ((gx * 7 + gy * 13) % 17) / 16.0
            cv2.circle(a_img, (gx, gy), 4, [30 * b, 70 * b, 170 * b], -1, cv2.LINE_AA)
    a_img = cv2.GaussianBlur(a_img, (0, 0), 2.6)
    v = np.exp(-(((xx - FW / 2) / (FW * 0.55)) ** 2 + ((yy - FH * 0.42) / (FH * 0.62)) ** 2))[..., None]
    plate_a = a_img * (0.35 + 0.65 * v) + np.float32([40, 60, 120]) * (0.22 * v)
    lines = (1.0 - 0.07 * (np.arange(FW) % 3 == 0).astype(np.float32))[None, :, None]   # the screen's fine lines
    plate_a, plate_b = plate_a * lines, plate_b * lines
    cutc[..., :3] *= lines
    save_jpg(plate_a, f"{IMG}/v10_plate_a.jpg", q=94)
    save_jpg(plate_b, f"{IMG}/v10_plate_b.jpg", q=94)
    save_png(cutc, f"{IMG}/v10_fink_cut.png")
    print(f"   fink: plates {FW}x{FH}, photo at ({px},{py}) {pw}x{ph}")
    return plate_a, cutc


def fink_view(plate, cutc, k):
    """the frame as it lands: plate + cut-out, the canvas's middle scaled k about the frame's centre"""
    al = cutc[..., 3:4] / 255.0
    comp = plate * (1 - al) + cutc[..., :3] * al
    M = np.float32([[k, 0, W / 2 - k * (FX0 + W / 2)], [0, k, H / 2 - k * (FY0 + H / 2)]])
    return cv2.warpAffine(comp, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


# ------------------------------------------------------------------ the photo wall
# (key, t, cx, cy, zoom, x, y, w, h, frame in, look): the wall's first nine are there when it resolves (frame 10),
# the rest cut in one after another (the reel: one every two of its frames)
TILES = [
    ("FC", 2.7, 0.5, 0.5, 1.0, 0, 0, 560, 300, 10, "bw"),
    ("EYE", 3.6, 0.5, 0.5, 1.0, 540, 50, 500, 280, 10, "c"),
    ("FED", 3.0, 0.5, 0.5, 1.0, 1360, 0, 560, 315, 10, "c"),
    ("CASH", 1.7, 0.5, 0.5, 1.0, 1200, 340, 440, 250, 10, "c"),
    ("FE2", 0.3, 0.5, 0.47, 0.55, 60, 360, 340, 440, 10, "bw"),
    ("MF2", 7.4, 0.45, 0.45, 0.62, 1510, 640, 410, 440, 10, "c"),
    ("CHESS", 0.2, 0.5, 0.55, 1.0, 430, 700, 360, 380, 10, "c"),
    ("MF1", 5.6, 0.5, 0.5, 0.75, 820, 790, 430, 240, 10, "c"),
    ("RUN", 9.3, 0.5, 0.5, 1.0, 1250, 600, 250, 480, 10, "bw"),
    ("FE3", 13.4, 0.5, 0.45, 0.6, 170, 60, 380, 380, 14, "bw"),
    ("LFI", 10.3, 0.5, 0.4, 0.55, 1430, 200, 440, 300, 18, "c"),
    ("FIRE", 2.5, 0.5, 0.5, 1.0, 40, 640, 520, 300, 22, "c"),
    ("FIN", 1.0, 0.68, 0.42, 0.6, 650, 0, 620, 600, 26, "c"),        # the big one in the middle
    ("MF2", 0.3, 0.45, 0.4, 0.55, 1270, 30, 430, 320, 31, "c"),
    ("FC", 0.2, 0.5, 0.5, 1.0, 290, 520, 480, 260, 35, "bw"),
    ("FC", 8.8, 0.5, 0.5, 0.8, 1590, 430, 330, 250, 39, "c"),
    ("MF1", 9.1, 0.5, 0.38, 0.6, 830, 600, 420, 290, 43, "c"),
    ("FSP", 6.8, 0.5, 0.36, 0.6, 40, 320, 330, 320, 46, "c"),
]


def r_wall():
    n = nf(0.0, FINK_IN)                      # 57: the Fink frame from "powerful"
    tiles = [(still(k, t, cx, cy, z, w, h, look), x, y, w, h, f0) for k, t, cx, cy, z, x, y, w, h, f0, look in TILES]
    money = grab(SRC["MONEY"], 1.0, n, fps=FPS)

    def back(i):
        bg = cover(money[min(i, len(money) - 1)].astype(np.float32))
        return grade(bg, sat=0.7, contrast=1.15) * 0.62

    def wall(i, upto):
        fr = back(i)
        for im, x, y, w, h, f0 in tiles:
            if f0 <= upto:
                x1, y1 = min(W, x + w), min(H, y + h)
                fr[y:y1, x:x1] = im[:y1 - y, :x1 - x]
        return fr

    def lens(fr, i):
        k = 1.0 + 0.035 * max(0, i - 10) / 38
        fr = affine(fr, k, W / 2, H / 2, W / 2, H / 2, border=(0, 0, 0))
        fr = barrel(fr, W / 2, H / 2, 1250, 0.075)
        fr = center_focus(fr, r0=430, r1=1010, zoom=0.010, n=6, gblur=2.0)
        return vignette(fr, strength=0.30)

    texture = (np.sin(np.arange(H, dtype=np.float32) * np.pi / 2.0) * 3.0)[:, None, None]   # faint scan lines
    plate_a, cutc = fink_assets()
    k_thresh, k_false = n - 8, n - 4
    wr = Writer(f"{CLIPS}/v10_wall.mp4")
    for i in range(n):
        if i < 6:                                            # the curved, smeared pan, colours blown
            fr = lens(wall(10, 10), 10)
            L = int(150 - 18 * i)
            ker = np.zeros((1, L), np.float32); ker[0, :] = 1.0 / L
            fr = cv2.filter2D(fr, -1, ker, borderType=cv2.BORDER_REFLECT)
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            bend = (xx - W / 2) / (W / 2)
            mapy = (H / 2 + (yy - H / 2) * (1 + 0.22 * bend * bend)).astype(np.float32)
            fr = cv2.remap(fr, xx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            sh = 16 - 2 * i
            fr = np.stack([np.roll(fr[..., 0], sh, axis=1), fr[..., 1], np.roll(fr[..., 2], -sh, axis=1)], axis=2)
            fr = grade(fr, sat=1.9, contrast=1.35, bright=10)
            fr = fr + cv2.GaussianBlur(np.clip(fr - 150, 0, 255), (0, 0), 14) * 0.9
        elif i < 10:                                         # the same wall, washed grey
            fr = lens(wall(10, 10), 10)
            fr = grade(cv2.GaussianBlur(fr, (0, 0), 1.6), sat=0.35, contrast=0.5) * 0.7 + 150 * 0.3
            sh = 4
            fr = np.stack([np.roll(fr[..., 0], sh, axis=1), fr[..., 1], np.roll(fr[..., 2], -sh, axis=1)], axis=2)
        elif i < k_thresh:                                   # the wall, the pictures cutting in
            fr = lens(wall(i, i), i)
        elif i < k_false:                                    # a white photocopy texture
            fr = lens(wall(i, i), i)
            g = fr @ np.float32([0.299, 0.587, 0.114])
            g = np.where(g > 58, 255.0, g * 0.25)
            blk = cv2.resize(cv2.resize(g, (W // 18, H // 18), interpolation=cv2.INTER_AREA), (W, H),
                             interpolation=cv2.INTER_NEAREST)
            yy, xx = np.mgrid[0:H, 0:W]
            m = ((xx > W * 0.55) & (((xx // 90) + (yy // 70) + i) % 3 == 0)).astype(np.float32)
            g = g * (1 - m) + np.where(blk > 140, 255.0, 20.0) * m
            fr = np.repeat(g[..., None], 3, axis=2)
        else:                                                # false colour of the frame that follows
            v = fink_view(plate_a, cutc, 1.30)
            g = np.clip(v @ np.float32([0.299, 0.587, 0.114]) * 1.25 + 20, 0, 255).astype(np.uint8)
            fc = cv2.applyColorMap(255 - g, cv2.COLORMAP_TURBO)[..., ::-1].astype(np.float32)
            fr = cv2.GaussianBlur(fc, (0, 0), 3.0)
        wr.write(fr + texture + grain(seed=5000 + i, amt=5))
    wr.close()
    print(f"   wall: {n} frames ({len(TILES)} pictures), the Fink frame from {FINK_IN:.3f}s")


# ------------------------------------------------------------------ the red scene, as v6 had it
def r_evil():
    a0, a1 = B["evil"]
    n = nf(a0, a1)
    at = lambda k: T[k] - a0 - 0.03
    t_cut = T["most"] - a0 - 2 / FPS
    noh, horn = P6.Cutout(f"{P6.V6}/cut_a.png"), P6.Cutout(f"{P6.V6}/cut_b.png")
    s_w, hx, ht = 0.70, (289 + 732) / 2, 133
    s_c = s_w * 1.69
    rx, ry = [p[0] for p in P6.RISE], [p[1] for p in P6.RISE]
    # the small words (v6: "the" / "man" (bold italic) / "who runs the" across): "or" / "how" / "people" (bold
    # italic) / "call it the" across, each leaving when the next of its group comes
    small = []
    cy = H * 0.5
    for word, key, x, kind in (("or", "or", 0.5, "r"), ("how", "how", 0.5, "r"), ("people", "people", 0.5, "b"),
                               ("call", "call", 0.13, "r"), ("it", "it0", 0.5, "r"), ("the", "the3", 0.87, "r")):
        if kind == "b":
            a = P6.text_alpha(word, P6.HEROS_B, 84, x * W, cy=cy, shear=0.21)
            gl = P6.glow_of(a, [(9, 0.8), (40, 0.9), (110, 0.8)])
        else:
            a = P6.text_alpha(word, P6.HEROS_R, 54, x * W, cy=cy)
            gl = P6.glow_of(a, [(7, 0.6), (26, 0.35)])
        small.append((a, gl, at(key), key))
    leave = {"or": at("how"), "how": at("people"), "people": at("call")}
    most_a = P6.text_alpha("most", P6.LIB, 720, W / 2, baseline=0.39 * H)
    evil_a = P6.text_alpha("evil", P6.LIB, 960, W / 2, baseline=0.89 * H)
    most_g = P6.glow_of(most_a, [(14, 0.9), (40, 0.75), (110, 0.45)])
    evil_g = P6.glow_of(evil_a, [(16, 0.9), (48, 0.75), (130, 0.45)])
    t_most, t_evil = at("most"), at("evil")
    wr = Writer(f"{CLIPS}/v10_evil.mp4")
    prev_top = None
    for i in range(n):
        t = i / FPS
        fr = np.empty((H, W, 3), np.float32)
        fr[:] = P6.RED
        if t < t_cut:
            top = np.interp(t, rx, ry) * H
            v = 0 if prev_top is None else abs(top - prev_top)
            prev_top = top
            x0 = 0.44 * W - hx * s_w
            y0 = top - ht * s_w
            hf = P6.smooth((t - (t_cut - 0.10)) / 0.10)
            pm, al = noh.place(s_w, x0, y0)
            if hf > 0:
                pm2, al2 = horn.place(s_w, x0, y0)
                pm, al = pm * (1 - hf) + pm2 * hf, al * (1 - hf) + al2 * hf
            pm, al = P6.soften(pm, al, sigma=2.2, vblur=min(60, v * 1.0))
            fr = P6.over_man(fr, pm, al, P6.grain_field(7000 + i, 0.0))
            for a, gl, ta, key in small:
                if t < ta or t >= leave.get(key, t_cut) - 1 / FPS:
                    continue
                fr = P6.put_text(fr, a, P6.smooth((t - ta) / 0.10), gl, fringe=2)
        else:
            u = t - t_cut
            top_f = 0.135 + 0.018 * np.exp(-u / 0.06) - 0.013 * P6.smooth(u / 1.0)
            x0 = 0.48 * W - hx * s_c
            y0 = top_f * H - ht * s_c
            pm, al = horn.place(s_c, x0, y0)
            ue = (t - t_cut) / max(0.2, t_evil + 0.05 - t_cut)
            sigma = 10.0 - 3.5 * P6.smooth(ue)
            if t >= t_most:
                fr = P6.put_text(fr, most_a, 1 - np.exp(-(t - t_most) / 0.062), most_g, fringe=3)
            if t >= t_evil:
                fr = P6.put_text(fr, evil_a, 1 - np.exp(-(t - t_evil) / 0.040), evil_g, fringe=3)
            pm, al = P6.soften(pm, al, sigma=sigma)
            fr = P6.over_man(fr, pm, al, P6.grain_field(7300 + i, 0.0))
        wr.write(fr)
    wr.close()
    print(f"   evil: {n} frames; the rise {t_cut:.3f}s, 'most' {t_most:.3f}, 'evil' {t_evil:.3f}")


# ------------------------------------------------------------------ "company ever" / "built."
def haze(fr, lift=112, k=0.52, blur=1.4):
    g = cv2.GaussianBlur(fr, (0, 0), blur) @ np.float32([0.299, 0.587, 0.114])
    yy = np.linspace(1.0, 0.0, H, dtype=np.float32)[:, None]
    out = g * k + lift + 26 * yy                             # the haze thicker towards the top
    return np.repeat(np.clip(out, 0, 255)[..., None], 3, axis=2)


def r_company():
    """"company ever": the reel's "But behind ... all that" frame (a man seen from behind, a crowd of suits in a haze):
    Fink from behind, facing the Economic Club of Chicago's audience (FG 4.80), black and white, hazed"""
    a0, a1 = B["built"][0], F(T["built"] - TM.LEAD)
    n = nf(a0, a1)
    frs = grab(SRC["FG"], 4.80, n, fps=FPS)
    wr = Writer(f"{CLIPS}/v10_company.mp4")
    for i, im in enumerate(frs):
        im = im.astype(np.float32)
        h, w = im.shape[:2]
        ch = int(w * 9 / 16)
        y0 = int(h * 0.40 - ch / 2)
        fr = cv2.resize(im[y0:y0 + ch], (W, H), interpolation=cv2.INTER_CUBIC)
        k = 1.0 + 0.025 * i / max(1, n - 1)
        fr = affine(fr, k, W / 2, H / 2, W / 2, H / 2, border=(128, 128, 128))
        wr.write(haze(fr, lift=104, k=0.60, blur=1.2) + grain(seed=6100 + i, amt=5))
    wr.close()
    print(f"   company: {n} frames (FG 4.80, Fink from behind, the crowd, hazed)")


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


# ------------------------------------------------------------------ the cartel clip without its table flash
def r_cartel():
    a0, a1 = B["cartel"]
    n = nf(a0, a1)
    src = grab(f"{DL}/v3/cartel_user.mp4", 0.0, 80)
    wr = Writer(f"{CLIPS}/v10_cartel.mp4")
    for i in range(n):
        j = 28 + int(i * 24 / FPS)
        wr.write(src[min(j, len(src) - 1)].astype(np.float32))
    wr.close()
    print(f"   cartel: {n} frames from its faces (frame 28 on)")


# ------------------------------------------------------------------ the card in "A company that's never made"
# (the user: "the videos can be a bit fast ... only the part of this caption that's being spoken"): things being made,
# a shot every ~0.22 s, from the cut on "touch" to the end of "made"
FACTORY = [("GE", 31.0), ("BRL", 171.0), ("HOW", 193.0), ("HOW", 407.0), ("BRL", 167.0), ("GE", 33.2),
           ("HOW", 221.0), ("HOW", 167.0)]


def r_factory():
    a, b = B["made"][0], F(T["a4"] - TM.LEAD)
    n = nf(a, b)
    per = n / len(FACTORY)
    wr = Writer(f"{CLIPS}/v10_factory.mp4", w=960, h=540)
    done = 0
    for k, (key, t0) in enumerate(FACTORY):
        m = round((k + 1) * per) - done
        frs = grab(SRC[key], t0, m, fps=FPS)
        for im in frs:
            fr = cover(im.astype(np.float32), 960, 540, scale=1.32)      # clear of the channel logo
            wr.write(grade(fr, sat=0.85, contrast=1.08))
        done += m
    wr.close()
    print(f"   factory: {n} frames, {len(FACTORY)} shots of ~{per:.1f}")


# ------------------------------------------------------------------ "U.S. company": the Kalanick reel's Earth (16.7 s)
# a cut to the picture with the words small in the middle, small coloured squares jumping about it (a new place every
# reel frame), then a cut to a closer framing of the same shot, the words staying. Ours: the user's flag clip.
SQ_COLS = [(255, 255, 255), (70, 230, 90), (240, 60, 60), (60, 220, 230), (250, 220, 60), (170, 80, 240),
           (60, 90, 250), (255, 255, 255)]


def r_flag():
    a, b = F(T["us"] - TM.LEAD), B["share"][1]
    n = nf(a, b)
    k_zoom = round((T["company3"] + 0.20 - a) * FPS)       # the closer framing a beat after "company"
    frs = grab(SRC["FLAG"], 0.3, n, fps=FPS)
    rng = np.random.default_rng(2124)
    sq = None
    wr = Writer(f"{CLIPS}/v10_flag.mp4")
    for i in range(n):
        im = frs[min(i, len(frs) - 1)].astype(np.float32)
        fr = affine(cover(im), 1.0 + 0.04 * i / max(1, n - 1), W / 2, H / 2, W / 2, H / 2, border=(0, 0, 0))   # (v15: no cut zoom)
        fr = grade(fr, sat=0.9, contrast=1.05) * 0.86
        if i % 6 == 0:                                       # the squares jump every reel frame (10 fps)
            m = 22
            sq = [(rng.uniform(0.08, 0.92) * W, rng.uniform(0.12, 0.88) * H, rng.choice(len(SQ_COLS)),
                   rng.uniform(9, 15)) for _ in range(m)]
        for x, y, c, sz in sq:
            x0, y0 = int(x - sz / 2), int(y - sz / 2)
            fr[y0:y0 + int(sz), x0:x0 + int(sz)] = np.float32(SQ_COLS[c])
        wr.write(fr + grain(seed=6500 + i, amt=4))
    wr.close()
    print(f"   flag: {n} frames, the closer framing from frame {k_zoom}")


# ------------------------------------------------------------------ "It holds more of Nvidia than Jensen Huang ...":
# the v6/v8 founders block, as the user asked to have it back (Nov 24): Think School's "Founders vs Blackrock" column
# for each company, then the founder in the Nvidia reel's opening treatment (Jensen: the reel's own clip), each slot
# re-cut on the new recording's words; then v4's texture pass (corner blur, no money overlay)
def founder_slots():
    L = lambda k: F(T[k] - TM.LEAD)
    ks = [L("it"), L("jensen"), L("more2"), L("bill"), L("and"), L("steve"), TM.OPEN_END]
    names = ["tsg_nv", "r1_jensen", "tsg_ms", "r1_gates", "tsg_ap", "r1_jobs"]
    return {nm: (a, b) for nm, a, b in zip(names, ks, ks[1:])}


def r_founders():
    import prep_v3 as P3
    import prep_v4 as P4
    slots = founder_slots()
    P3.rest1_slot = lambda name: slots[name]           # the v3 renderers take their slots from here
    for name in ("tsg_nv", "tsg_ms", "tsg_ap"):
        P3.r_tsg(name)
    P3.r_jensen()
    P3.r_gates()
    P3.r_jobs()
    for k, name in enumerate(["v3_tsg_nv", "v3_tsg_ms", "v3_tsg_ap", "v3_r1_jensen", "v3_r1_gates", "v3_r1_jobs"]):
        P4.texture_pass(name, opacity=0.0, seed=k)
    for nm, (a, b) in slots.items():
        print(f"   {nm}: {a:.3f}-{b:.3f} ({nf(a, b)} frames)")


# ============================================================================== v11 (the user's notes on v10's first scene)
# "I don't want this money background ... random cinematic clips ... use BlackRock-oriented clips, reduce his photos a
# bit ... in the background a part of [fast cinematic] from the middle, where it slows down": the reel's wall again,
# read frame by frame -- its pictures are rectangles and squares of many sizes, overlapping, the newest on top, some cut
# by the frame's edge, the background showing in the gaps; the whole wall bulges like a lens and goes soft towards the
# edges; and it moves at ~12 fps (a new state every 2-3 of its 30 fps frames: here every 5 of ours).
# (key, t, cx, cy, crop zoom, x, y, w, h, step): crop around (cx, cy) as fractions, clear of channel logos/subtitles
WALL2 = [
    ("BRS", 13.5, 0.46, 0.52, 0.80, 0, 0, 680, 430, 0),          # BlackRock's entrance, flags
    ("ASH", 9.3, 0.42, 0.46, 0.80, 480, 0, 650, 400, 0),         # BLACKROCK on the glass
    ("BRL", 845.0, 0.46, 0.55, 0.78, 1340, 0, 580, 380, 0),      # the building, flags
    ("ASH", 8.2, 0.50, 0.42, 0.78, 1150, 330, 700, 300, 0),      # BlackRock on the screens
    ("LFI", 10.3, 0.50, 0.40, 0.55, 790, 840, 340, 240, 0),      # Fink on stage
    ("FE3", 13.4, 0.50, 0.42, 0.62, 1650, 800, 270, 280, 0),     # Fink, black and white
    ("BR15", 214.0, 0.50, 0.50, 0.70, 420, 430, 240, 240, 1),    # the letters, close
    ("FIN", 1.0, 0.68, 0.40, 0.58, 0, 670, 580, 410, 2),         # Fink at the microphone
    ("XEX", 125.0, 0.50, 0.50, 0.62, 800, 40, 640, 600, 3),      # the black BlackRock sign, big in the middle
    ("MF2", 7.4, 0.42, 0.42, 0.55, 1590, 130, 330, 420, 4),      # Fink, close
    ("BRL", 160.0, 0.46, 0.56, 0.80, 1020, 660, 600, 330, 5),    # the exchange floor
    ("ASH", 11.5, 0.42, 0.45, 0.78, 40, 300, 470, 300, 6),       # the flags over BLACKROCK
    ("BRS", 0.5, 0.50, 0.58, 0.82, 560, 640, 440, 260, 7),       # the BLACKROCK sign
]
STEP = 5                       # frames a wall state holds (12 fps)


def tile_frames(key, t, cx, cy, zoom, tw, th, n):
    """n frames of a source (stepped later), cropped to the tile around (cx, cy)"""
    frs = grab(SRC[key], t, max(1, (n + STEP - 1) // STEP), fps=12)
    out = []
    for im in frs:
        im = im.astype(np.float32)
        h, w = im.shape[:2]
        ar = tw / th
        cw = min(w, h * ar) * zoom
        ch = cw / ar
        x0 = int(min(max(cx * w - cw / 2, 0), w - cw))
        y0 = int(min(max(cy * h - ch / 2, 0), h - ch))
        crop = cv2.resize(im[y0:int(y0 + ch), x0:int(x0 + cw)], (tw, th), interpolation=cv2.INTER_AREA)
        out.append(grade(crop, sat=0.95, contrast=1.06))
    return out


def wall2_lens(fr, step):
    k = 1.0 + 0.006 * step                                   # the slow push, one step at a time
    fr = affine(fr, k, W / 2, H / 2, W / 2, H / 2, border=(0, 0, 0))
    fr = barrel(fr, W / 2, H / 2, 1250, 0.075)
    fr = center_focus(fr, r0=430, r1=1010, zoom=0.010, n=6, gblur=2.0)
    return vignette(fr, strength=0.30)


# ---- the Fink frame (v11): the user's photo of Fink cut out, over a BlackRock building shot, blurred, dark and textured
BGW, BGH = 2208, 1242                    # the background video's canvas (the frame zooms below 1.0)
LINES = None


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


def r_finkbg():
    a0, a1 = FINK_IN, B["first"][1]
    n = nf(a0, a1)
    k_e = round((F(T["earth"] - 0.03) - a0) * FPS)
    p1 = grab(SRC["ASH"], 10.30, k_e, fps=FPS)                # BlackRock's entrance on the street
    p2 = grab(SRC["XEX"], 111.0, n - k_e, fps=FPS)            # the tower, its flags, its sign
    wr = Writer(f"{CLIPS}/v11_finkbg.mp4", w=BGW, h=BGH)
    for i in range(n):
        wr.write(bg_frame(p1[min(i, len(p1) - 1)], 1, i) if i < k_e else bg_frame(p2[min(i - k_e, len(p2) - 1)], 2, i))
    wr.close()
    print(f"   finkbg: {n} frames {BGW}x{BGH}, the switch at frame {k_e}")
    return n, k_e


def fink_view2(k):
    """the Fink frame's first look (for the false colour): background frame 0 + the cut-out, scaled k"""
    bg = bg_frame(grab(SRC["ASH"], 10.30, 1)[0], 1, 0)
    cutc = fink_cut2()
    canvas = cv2.resize(bg, (FW, FH), interpolation=cv2.INTER_AREA)
    al = cutc[..., 3:4] / 255.0
    comp = canvas * (1 - al) + cutc[..., :3] * al
    M = np.float32([[k, 0, W / 2 - k * (FX0 + W / 2)], [0, k, H / 2 - k * (FY0 + H / 2)]])
    return cv2.warpAffine(comp, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def r_wall2():
    n = nf(0.0, FINK_IN)                                     # 57
    k_wall, k_thresh, k_false = 10, n - 8, n - 4
    tiles = []
    for key, t, cx, cy, z, x, y, w, h, step in WALL2:
        f0 = k_wall + STEP * step
        tiles.append((tile_frames(key, t, cx, cy, z, w, h, n - f0), x, y, w, h, f0))
    back_src = grab(SRC["FC"], 3.70, (n + STEP - 1) // STEP + 2, fps=12)   # fast cinematic, its slow middle

    def back(st):
        bg = cover(back_src[min(st, len(back_src) - 1)].astype(np.float32))
        return grade(bg, sat=0.85, contrast=1.10) * 0.80

    def wall(i):
        st = max(0, (i - k_wall) // STEP)                    # the 12 fps step
        fr = back(st)
        for frs, x, y, w, h, f0 in tiles:
            if f0 <= max(i, k_wall):
                im = frs[min(max(0, (max(i, k_wall) - f0) // STEP), len(frs) - 1)]
                x1, y1 = min(W, x + w), min(H, y + h)
                fr[y:y1, x:x1] = im[:y1 - y, :x1 - x]
        return wall2_lens(fr, st), st

    texture = (np.sin(np.arange(H, dtype=np.float32) * np.pi / 2.0) * 3.0)[:, None, None]
    first, _ = wall(k_wall)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # the opening's one held frame: the wall smeared sideways on a curve, its colours blown
    L = 140
    ker = np.full((1, L), 1.0 / L, np.float32)
    pan = cv2.filter2D(first, -1, ker, borderType=cv2.BORDER_REFLECT)
    bend = (xx - W / 2) / (W / 2)
    pan = cv2.remap(pan, xx, (H / 2 + (yy - H / 2) * (1 + 0.22 * bend * bend)).astype(np.float32), cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REFLECT)
    pan = np.stack([np.roll(pan[..., 0], 16, axis=1), pan[..., 1], np.roll(pan[..., 2], -16, axis=1)], axis=2)
    pan = grade(pan, sat=1.9, contrast=1.35, bright=10)
    pan = pan + cv2.GaussianBlur(np.clip(pan - 150, 0, 255), (0, 0), 14) * 0.9
    grey = grade(cv2.GaussianBlur(first, (0, 0), 1.6), sat=0.35, contrast=0.5) * 0.7 + 150 * 0.3
    grey = np.stack([np.roll(grey[..., 0], 4, axis=1), grey[..., 1], np.roll(grey[..., 2], -4, axis=1)], axis=2)
    fv = fink_view2(1.30)
    g = np.clip(fv @ np.float32([0.299, 0.587, 0.114]) * 1.6 + 25, 0, 255).astype(np.uint8)
    falsec = cv2.GaussianBlur(cv2.applyColorMap(255 - g, cv2.COLORMAP_TURBO)[..., ::-1].astype(np.float32), (0, 0), 3.0)
    wr = Writer(f"{CLIPS}/v11_wall.mp4")
    for i in range(n):
        if i < 6:
            fr = pan
        elif i < k_wall:
            fr = grey
        elif i < k_thresh:
            fr, _ = wall(i)
        elif i < k_false:                                    # the white photocopy, two of the reel's frames
            fr, _ = wall(k_thresh - 1)
            gg = fr @ np.float32([0.299, 0.587, 0.114])
            gg = np.where(gg > 58, 255.0, gg * 0.25)
            blk = cv2.resize(cv2.resize(gg, (W // 18, H // 18), interpolation=cv2.INTER_AREA), (W, H),
                             interpolation=cv2.INTER_NEAREST)
            m = ((xx > W * 0.55) & (((xx // 90).astype(int) + (yy // 70).astype(int)) % 3 == 0)).astype(np.float32)
            gg = gg * (1 - m) + np.where(blk > 140, 255.0, 20.0) * m
            fr = np.repeat(gg[..., None], 3, axis=2)
        else:                                                # false colour of the Fink frame
            fr = falsec
        wr.write(fr + texture + grain(seed=5000 + (i // STEP), amt=5))
    wr.close()
    print(f"   wall2: {n} frames, {len(WALL2)} pictures ({sum(1 for w in WALL2 if w[0] in ('LFI', 'FE3', 'FIN', 'MF2'))} of Fink), "
          f"stepped every {STEP} frames")


# ============================================================================== v12 (the user: "they have obviously used photos,
# don't use videos ... Larry Fink photos, BlackRock building photos ... cinematic photos" from the user's clips)
# The reel's wall, picture by picture (its frames 5-25), each of ours on its place and in its order:
# (key, t, cx, cy, zoom, x, y, w, h, step, look)            # <- the reel's picture on that place
WALL3 = [
    ("ASH", 9.3, 0.42, 0.40, 0.86, 0, 0, 700, 560, 0, "c"),          # anatomy sketch   <- BLACKROCK on the glass
    ("XEX", 125.0, 0.50, 0.48, 0.72, 480, 0, 640, 400, 0, "c"),      # wireframe eye    <- the black BlackRock sign
    ("BRL", 845.0, 0.44, 0.55, 0.80, 1300, 0, 620, 380, 0, "c"),     # hand + wireframe <- the building, its flags
    ("ASH", 8.2, 0.52, 0.42, 0.80, 1020, 380, 900, 260, 0, "c"),     # muscle drawing   <- BlackRock on the screens
    ("LFI", 10.3, 0.50, 0.38, 0.50, 796, 843, 330, 237, 0, "c"),     # the duo saluting <- Fink on stage
    ("ASH", 10.6, 0.47, 0.42, 0.62, 1645, 822, 275, 258, 0, "c"),    # the man in denim <- BlackRock's entrance
    ("C618", 3.3, 0.55, 0.45, 0.85, 860, 520, 400, 260, 1, "bw"),    # the beach        <- the black hole
    ("FE3", 13.4, 0.50, 0.42, 0.62, 0, 682, 560, 398, 2, "bw"),      # B&W portrait     <- Fink, black and white
    ("CMJ", 2.6, 0.50, 0.50, 0.92, 1063, 642, 622, 305, 2, "c"),     # the blurred crowd <- the crowd under umbrellas
    ("FIN", 1.0, 0.68, 0.36, 0.56, 802, 50, 622, 612, 3, "c"),       # the duo, big     <- Fink, big in the middle
    ("MF2", 7.4, 0.42, 0.40, 0.50, 1585, 130, 335, 422, 3, "bw"),    # the dark portrait <- Fink, close, black and white
    ("BR15", 214.0, 0.50, 0.50, 0.55, 421, 542, 201, 140, 3, "c"),   # the chess pawns  <- BlackRock's letters
    ("BRS", 13.5, 0.46, 0.50, 0.70, 0, 0, 411, 481, 4, "c"),         # the duo laughing <- BlackRock's entrance, flags
    ("COPP", 7.0, 0.52, 0.50, 0.70, 341, 0, 522, 522, 5, "green"),   # the banknote     <- the dollar's portrait
    ("CPIN", 11.1, 0.50, 0.50, 0.60, 1404, 0, 201, 241, 6, "c"),     # the green swirl  <- the eye
    ("CPIN", 2.9, 0.50, 0.50, 0.80, 461, 542, 482, 538, 6, "c"),     # the green face   <- the face in sparks
    ("BRL", 160.0, 0.46, 0.60, 0.80, 1444, 660, 476, 182, 7, "c"),   # the orange strip <- the exchange floor
]


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


def r_wall3():
    n = nf(0.0, FINK_IN)                                     # 57
    k_wall, k_thresh, k_false = 10, n - 8, n - 4
    tiles = [(tile_still(k, t, cx, cy, z, w, h, look), x, y, w, h, k_wall + STEP * st)
             for k, t, cx, cy, z, x, y, w, h, st, look in WALL3]
    back_src = grab(SRC["FC"], 3.70, (n + STEP - 1) // STEP + 2, fps=12)   # fast cinematic, its slow middle

    def wall(i):
        st = max(0, (i - k_wall) // STEP)
        fr = grade(cover(back_src[min(st, len(back_src) - 1)].astype(np.float32)), sat=0.85, contrast=1.10) * 0.80
        for im, x, y, w, h, f0 in tiles:
            if f0 <= max(i, k_wall):
                x1, y1 = min(W, x + w), min(H, y + h)
                fr[y:y1, x:x1] = im[:y1 - y, :x1 - x]
        return wall2_lens(fr, st)

    texture = (np.sin(np.arange(H, dtype=np.float32) * np.pi / 2.0) * 3.0)[:, None, None]
    first = wall(k_wall)
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
    # the false colour: the Fink frame's first look (its first background, the cut-out, at 1.30)
    cutc = fink_cut2()
    bga = np.asarray(Image.open(f"{IMG}/v12_bg_a.jpg").convert("RGB")).astype(np.float32)
    al = cutc[..., 3:4] / 255.0
    comp = bga * (1 - al) + cutc[..., :3] * al
    k = 1.30
    M = np.float32([[k, 0, W / 2 - k * (FX0 + W / 2)], [0, k, H / 2 - k * (FY0 + H / 2)]])
    fv = cv2.warpAffine(comp, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    g = np.clip(fv @ np.float32([0.299, 0.587, 0.114]) * 1.6 + 25, 0, 255).astype(np.uint8)
    falsec = cv2.GaussianBlur(cv2.applyColorMap(255 - g, cv2.COLORMAP_TURBO)[..., ::-1].astype(np.float32), (0, 0), 3.0)
    last = wall(k_thresh - 1)
    gg = last @ np.float32([0.299, 0.587, 0.114])
    gg = np.where(gg > 58, 255.0, gg * 0.25)
    blk = cv2.resize(cv2.resize(gg, (W // 18, H // 18), interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST)
    m = ((xx > W * 0.55) & (((xx // 90).astype(int) + (yy // 70).astype(int)) % 3 == 0)).astype(np.float32)
    photocopy = np.repeat((gg * (1 - m) + np.where(blk > 140, 255.0, 20.0) * m)[..., None], 3, axis=2)
    wr = Writer(f"{CLIPS}/v12_wall.mp4")
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
    nf_ = sum(1 for w in WALL3 if w[0] in ("LFI", "FE3", "FIN", "MF2"))
    print(f"   wall3: {n} frames, {len(WALL3)} photos ({nf_} of Fink), a new state every {STEP} frames")


# ============================================================================== v13 (the user: Fink's photo comes "exactly like
# the Chainsmokers": in the reel, after the photocopy white and the false colour, the duo stand cut out in front of the
# same wall, now soft, and the frame pushes in slowly; only then (here on "Earth", with the Kalanick flash) does the
# background change -- ours to BlackRock's building)
def r_wall4():
    """v12's wall, plus the blurred wall behind Fink (v13_bg_wall.jpg) and the false colour of that new first look"""
    global WALL_LAST
    n = nf(0.0, FINK_IN)
    k_wall, k_thresh, k_false = 10, n - 8, n - 4
    tiles = [(tile_still(k, t, cx, cy, z, w, h, look), x, y, w, h, k_wall + STEP * st)
             for k, t, cx, cy, z, x, y, w, h, st, look in WALL3]
    back_src = grab(SRC["FC"], 3.70, (n + STEP - 1) // STEP + 2, fps=12)

    def wall(i):
        st = max(0, (i - k_wall) // STEP)
        fr = grade(cover(back_src[min(st, len(back_src) - 1)].astype(np.float32)), sat=0.85, contrast=1.10) * 0.80
        for im, x, y, w, h, f0 in tiles:
            if f0 <= max(i, k_wall):
                x1, y1 = min(W, x + w), min(H, y + h)
                fr[y:y1, x:x1] = im[:y1 - y, :x1 - x]
        return wall2_lens(fr, st)

    texture = (np.sin(np.arange(H, dtype=np.float32) * np.pi / 2.0) * 3.0)[:, None, None]
    first = wall(k_wall)
    last = wall(k_thresh - 1)
    # the wall behind Fink: the last state, soft and a little darker (the reel's wall behind the duo), on the canvas
    soft = cv2.GaussianBlur(last, (0, 0), 7) * 0.62
    soft_c = cv2.resize(soft, (FW, FH), interpolation=cv2.INTER_CUBIC) * screen_lines(FW)
    save_jpg(soft_c, f"{IMG}/v13_bg_wall.jpg", q=94)
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
    wr = Writer(f"{CLIPS}/v13_wall.mp4")
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
    print(f"   wall4: {n} frames; the soft wall for Fink's frame: v13_bg_wall.jpg")


# ============================================================================== v14: "cost him $100 million loss."
# The Kalanick reel's year counter (19.2-20.8 s, read frame by frame): one reel frame of soft white, the first year
# sharp for one frame, then the years roll up through a band -- the old one leaving upwards, the next coming from
# below, smeared vertically with the speed -- fast first and slowing, the last one settling with the old one's edge
# still showing at the top of the band; it holds, then slides out to the left. Every change on the reel's 10-12 fps.
# Ours: "$1 million" rolling up to "$100 million" over the user's money clip (dark, textured), "loss." blooming in under
# it on the word.
ISF = f"{ROOT}/assets/fonts/InstrumentSerif-Regular.woff2"
ISF_I = f"{ROOT}/assets/fonts/InstrumentSerif-Italic.woff2"
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
    full = text_mask("$100 million loss.", ISF, size)
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


def r_bet():
    """"but one bad bet": the Kalanick reel's "he's coming back hungrier." frame (9.0-9.7 s): the cut goes through one
    reel frame of the next shot in black and white, smeared sideways; then the shot, dark and warm with a red light at
    the right edge (its stage) -- ours the user's money clip on the dollar's "1", textured"""
    a0, a1 = F(TM.RT("but1") - TM.LEAD), F(TM.RT("cost") - TM.LEAD)
    n = nf(a0, a1)
    frs = grab(SRC["COPP"], 4.0, n, fps=FPS)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    red = np.exp(-(((xx - W) / 420) ** 2 + ((yy - 0.45 * H) / 700) ** 2))[..., None] * np.float32([150, 22, 18])
    lines = screen_lines(W)
    wr = Writer(f"{CLIPS}/v15_bet.mp4")
    for i in range(n):
        fr = cover(frs[min(i, len(frs) - 1)].astype(np.float32))
        if i < 6:
            g = fr @ np.float32([0.299, 0.587, 0.114])
            g = cv2.filter2D(g, -1, np.full((1, 110), 1 / 110, np.float32), borderType=cv2.BORDER_REFLECT)
            fr = np.repeat((g * 0.55)[..., None], 3, axis=2)
        else:
            g = fr @ np.float32([0.299, 0.587, 0.114])
            fr = (g[..., None] * 0.35 + fr * 0.65) * np.float32([1.05, 0.92, 0.80]) * 0.52 + red
            fr = vignette(fr * lines, strength=0.35)
        wr.write(fr + grain(seed=6700 + i // STEP, amt=4))
    wr.close()
    print(f"   bet: {n} frames ({a0:.3f}-{a1:.3f})")


def rembg(src_png, out_png):
    subprocess.run(["npx", "--yes", "hyperframes@0.9.46", "remove-background", src_png, "-o", out_png],
                   cwd=ROOT, check=True, capture_output=True)


def r_r88():
    """"in 1988,": the Anthropic reel's "2018" (12.82-13.57): the first reel frame the man's white silhouette on the
    shot, then the shot (the number in the composition) -- ours Fink seated at the Economic Club (FG 6.2)"""
    a0, a1 = F(TM.RT("1988") - 0.033), F(TM.RT("he1") - 0.033)
    n = nf(a0, a1)
    frs = grab(SRC["FG"], 6.20, n, fps=FPS)

    def crop(im):
        im = im.astype(np.float32)
        h, w = im.shape[:2]
        ch = int(w * 9 / 16)
        y0 = max(0, int(h * 0.42 - ch / 2))
        return cv2.resize(im[y0:y0 + ch], (W, H), interpolation=cv2.INTER_CUBIC)

    first = crop(frs[0])
    save_png(first, f"{WORK}/r88_first.png")
    rembg(f"{WORK}/r88_first.png", f"{WORK}/r88_cut.png")
    al = np.asarray(Image.open(f"{WORK}/r88_cut.png").convert("RGBA")).astype(np.float32)[..., 3:4] / 255.0
    wr = Writer(f"{CLIPS}/v15_r88.mp4")
    for i in range(n):
        fr = grade(crop(frs[min(i, len(frs) - 1)]), sat=0.9, contrast=1.06)
        if i < STEP:
            fr = fr * 0.75 * (1 - al) + 255 * al
        wr.write(fr + grain(seed=6900 + i, amt=2.5))
    wr.close()
    print(f"   r88: {n} frames ({a0:.3f}-{a1:.3f}), the silhouette for {STEP} frames")


def r_called():
    """"He called it": the reel's "Now elon's" (16.23-16.32): the man's white silhouette over the shot for two reel
    frames -- the shot is v6_rest2's (BRL 786.6); its first frame cut out here (v15_called_white.png)"""
    t = F(TM.RT("he_called") - TM.LEAD) + 0.05 - TM.B["rest2"][0]
    im = grab(f"{CLIPS}/v6_rest2.mp4", t, 1)[0].astype(np.float32)
    save_png(im, f"{WORK}/called_first.png")
    rembg(f"{WORK}/called_first.png", f"{WORK}/called_cut.png")
    a = np.asarray(Image.open(f"{WORK}/called_cut.png").convert("RGBA"))
    out = np.zeros_like(a)
    out[..., :3] = 255
    out[..., 3] = a[..., 3]
    Image.fromarray(out, "RGBA").save(f"{IMG}/v15_called_white.png")
    print(f"   called: silhouette from rest2 at {t:.3f}s, {np.mean(a[..., 3] > 128):.3f} of the frame")



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



def r_touch4():
    """"everything you touch." running on until "A company" (the user: the touch video continues): the fingers meet on
    "touch" (v3's r_touch3), then the burst -- its own frames 21-27 only (from 28 the source cuts to an office) --
    slowed to fill the beat, blended frame to frame, easing into its white"""
    import prep_v3 as P3
    n = nf(*B["touch"])
    t0 = round(B["touch"][0] * FPS)
    k_touch = round(T["touch"] * FPS) - t0
    hands = cover(P3.frame_at(P3.TOUCH, 0, 24).astype(np.float32))
    strip = hands[:, 922:992]
    plate = np.concatenate([strip] * (W // strip.shape[1] + 1), axis=1)[:, :W]
    lum = cv2.GaussianBlur(hands.mean(axis=2), (0, 0), 1.2)
    mask = np.clip((lum - 34) / 40, 0, 1)[..., None]
    left_m, right_m = mask.copy(), mask.copy()
    left_m[:, 960:] = 0
    right_m[:, :960] = 0
    burst = [cover(P3.frame_at(P3.TOUCH, f, 24).astype(np.float32)) for f in range(21, 28)]
    wr = Writer(f"{CLIPS}/r_touch3.mp4")
    for j in range(n):
        if j < k_touch:
            u = smooth((j + 1) / k_touch)
            d = 260 - 305 * u
            fr = plate.copy()
            for m, dx in ((left_m, -d), (right_m, d)):
                M = np.float32([[1, 0, dx], [0, 1, 0]])
                hs = cv2.warpAffine(hands, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                ms = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)[..., None]
                fr = fr * (1 - ms) + hs * ms
        else:
            p = (j - k_touch) / max(1, n - k_touch - 1)
            x = 6.0 * p ** 0.75
            a = int(np.floor(x))
            b = min(6, a + 1)
            w = x - a
            fr = burst[a] * (1 - w) + burst[b] * w
            fr = fr + (255 - fr) * (0.55 * smooth((p - 0.7) / 0.3))   # into its white, ahead of the paper
        wr.write(fr + grain(seed=400 + j, amt=4))
    wr.close()
    print(f"   touch4: {n} frames, the fingers meet at {k_touch}, the burst slowed over {n - k_touch}")


def r_job():
    """"one job": the same source as v6_rest2's "a system" shot running on to its ring of trading screens (BZ 60.55),
    in place of the brain shot with its burned-in text"""
    a0, a1 = F(TM.R(TM.ALIGN["rest"][86]["start"]) - 0.03), F(TM.R(TM.ALIGN["rest"][88]["start"]) - 0.03)
    n = nf(a0, a1)
    frs = grab(f"{DL}/v3/new/bazzarbyte.mp4", 60.55, n, fps=FPS)
    wr = Writer(f"{CLIPS}/v15_job.mp4")
    for i, im in enumerate(frs):
        band = im[520:1128].astype(np.float32)
        fr = cv2.resize(band, (W, H), interpolation=cv2.INTER_CUBIC)
        wr.write(grade(fr, sat=0.95, contrast=1.05) + grain(seed=7100 + i, amt=3))
    wr.close()
    print(f"   job: {n} frames ({a0:.3f}-{a1:.3f})")



def r_factory2():
    """the card in "A company that's never made" (the user: the clips added earlier, each the same length, nothing
    like the knob-press shot): v9's three -- circuit boards on a bench, the press, the line -- an equal third each"""
    import prep_v9 as P9
    a, b = B["made"][0], F(T["a4"] - TM.LEAD)
    n = nf(a, b)
    shots = [("BRL", 167.05, 880, 600, 1500), ("HOW", 192.74, 860, 600, 1500), ("BRL", 170.60, 880, 600, 1500)]
    per = [n // 3 + (1 if k < n % 3 else 0) for k in range(3)]
    wr = Writer(f"{CLIPS}/v10_factory.mp4", w=960, h=540)
    for (key, t0, cx, cy, span), m in zip(shots, per):
        for fr in P9.crop_clip(key, t0, m, cx, cy, span, 960, 540):
            wr.write(fr)
    wr.close()
    print(f"   factory2: {n} frames, three shots of {per}")



def r_negs():
    """the reel's one-frame negatives (11.32 s) as stills of v6_rest2's own frames, inverted (a blend in another
    composition cannot see the video under it)"""
    r0 = TM.B["rest2"][0]
    for name, i in (("br", 80), ("risk", 89)):
        t = F(TM.R(TM.ALIGN["rest"][i]["start"]) - 0.03) - 2.5 / FPS
        im = grab(f"{CLIPS}/v6_rest2.mp4", t - r0, 1)[0].astype(np.float32)
        save_jpg(255 - im, f"{IMG}/v15_neg_{name}.jpg", q=92)
        print(f"   neg {name}: rest2 frame at film {t:.3f}")


ALL = {"negs": r_negs, "factory2": r_factory2, "touch4": r_touch4, "job": r_job, "founders2": r_founders2, "wall5": r_wall5, "company2": r_company2, "bet": r_bet, "r88": r_r88, "called": r_called, "count": r_count, "wall4": r_wall4, "plates3": fink_plates3, "wall3": r_wall3, "wall2": r_wall2, "finkbg": r_finkbg, "founders": r_founders, "factory": r_factory, "flag": r_flag, "wall": r_wall, "evil": r_evil, "company": r_company, "built": r_built, "cartel": r_cartel}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
