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
        if i < k_zoom:
            fr = cover(im)
        else:                                                # closer on the flag (it flies at x 0.27-0.55, y 0.15-0.5)
            fr = affine(cover(im), 1.75, 0.40 * W, 0.36 * H, W / 2, H / 2, border=(0, 0, 0))
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


ALL = {"wall4": r_wall4, "plates3": fink_plates3, "wall3": r_wall3, "wall2": r_wall2, "finkbg": r_finkbg, "founders": r_founders, "factory": r_factory, "flag": r_flag, "wall": r_wall, "evil": r_evil, "company": r_company, "built": r_built, "cartel": r_cartel}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
