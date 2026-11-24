"""v6 renderers (the user's notes of Nov 22).

  evil   "the man who runs the most evil": reel DfhzVs8q9NH's "one guy was such a terrible boss" (3.17-5.47 s), measured
         frame by frame (notes/REF_TERRIBLE_BOSS.md) and rebuilt on the user's own red (new red bg.jpg, 254/0/0) with the
         user's three Fink cut-outs (red, without horns / with horns / horns only):
         - the cut-in: flat red; Fink rises from the bottom on the reference's own curve (head top 89 % -> 17 % of the
           height, a fast ease-out over 1.2 s), soft, with motion blur while he is fast, and grain on him only;
         - the small words in the middle, as the reference's: "the" (regular), "man" (bold italic, a soft white glow
           spot -- the reference's "guy"), then "who" left, "runs" centre, "the" right (its "was such a");
         - the horns fade in over the last 0.1 s before the cut;
         - the cut: 1.69x closer, out of focus; "most" (the reference's "terrible": a Times-style serif, ~410 px, cream
           white with a heavy white bloom and a little colour fringing) fades in behind him (opacity 1 - e^(-t/0.062)),
           then "evil" (its "boss", ~900 px) on its word (1 - e^(-t/0.04)); the grain on him builds up to "evil".
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import prep_v3 as P
import timing as TM
from common import CLIPS, DL, FPS, H, W, Writer

V6 = f"{DL}/v6"
RED = np.float32([254, 0, 0])                          # the user's red (new red bg.jpg)
LIB = f"{P.FONTS}/LiberationSerif-Regular.ttf"         # Times-style serif (the reference's "terrible boss")
HEROS_R = f"{P.FONTS}/TeXGyreHeros-Regular.otf"        # Helvetica-style (the reference's small words)
HEROS_B = f"{P.FONTS}/TeXGyreHeros-Bold.otf"

# the reference's rise: the head's top as a share of the height, by seconds after the cut-in (29.97 fps frames 5-40)
RISE = [(0.000, .893), (.033, .771), (.067, .695), (.100, .622), (.133, .559), (.167, .512), (.200, .474),
        (.234, .439), (.267, .406), (.300, .384), (.334, .359), (.367, .335), (.400, .318), (.434, .303),
        (.467, .289), (.501, .276), (.667, .229), (.834, .202), (1.001, .183), (1.168, .167), (2.0, .150)]


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def text_alpha(text, font_path, size, cx, cy=None, baseline=None, shear=0.0):
    """A full-frame alpha of one line of text, centred on cx and either centred on cy or sitting on `baseline`."""
    f = ImageFont.truetype(font_path, size)
    l, t, r, b = f.getbbox(text)
    asc, desc = f.getmetrics()
    pad = int(size * 0.6)
    im = Image.new("L", (int(r - l) + 2 * pad, asc + desc + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad - l, pad), text, font=f, fill=255)
    m = np.asarray(im).astype(np.float32) / 255
    if shear:
        hh, ww = m.shape
        M = np.float32([[1, -shear, shear * hh * 0.55], [0, 1, 0]])
        m = cv2.warpAffine(m, M, (ww, hh), flags=cv2.INTER_LINEAR)
    ys, xs = np.nonzero(m > 0.3)
    a = np.zeros((H, W), np.float32)
    x0 = cx - (xs.min() + xs.max()) / 2
    y0 = (cy - (ys.min() + ys.max()) / 2) if baseline is None else (baseline - (pad + asc))
    P.paste_alpha(a, m, x0, y0)
    return a


def glow_of(a, parts):
    return np.clip(sum(k * cv2.GaussianBlur(a, (0, 0), s) for s, k in parts), 0, 1)


def put_text(fr, a, op, glow, color=(255, 248, 240), fringe=2):
    """White type with its white glow (no dark shadow), a little colour fringing (red right, blue left), opacity op."""
    if op <= 0.001:
        return fr
    g = glow * op
    fr = fr + (255.0 - fr) * g[..., None] * 0.85
    col = np.float32(color)
    out = fr.copy()
    for c, dx in ((0, fringe), (1, 0), (2, -fringe)):
        ac = np.roll(a, dx, axis=1) * op if dx else a * op
        out[..., c] = fr[..., c] * (1 - ac) + col[c] * ac
    return out


class Cutout:
    def __init__(self, path, gain=(0.95, 0.75, 0.95), extend=300):
        im = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)
        if extend:                                       # the cut-out stops at his waist: continue the torso
            tail = im[-extend:][::-1].copy()             # downwards (mirrored, darkening), so the frame's bottom
            k = np.linspace(1.0, 0.72, extend, dtype=np.float32)[:, None, None]   # edge is always covered
            tail[..., :3] *= k
            im = np.concatenate([im, tail], axis=0)
        self.rgb = im[..., :3] * np.float32(gain)
        self.a = im[..., 3] / 255.0
        self.h, self.w = self.a.shape

    def place(self, s, x0, y0):
        """Premultiplied colour and alpha of the cut-out scaled by s with its top-left at (x0, y0), full frame."""
        M = np.float32([[s, 0, x0], [0, s, y0]])
        pm = cv2.warpAffine(self.rgb * self.a[..., None], M, (W, H), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        al = cv2.warpAffine(self.a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        return pm, al


def soften(pm, al, sigma=0.0, vblur=0):
    if vblur >= 3:
        k = np.ones((int(vblur) | 1, 1), np.float32)
        k /= k.sum()
        pm = cv2.filter2D(pm, -1, k)
        al = cv2.filter2D(al, -1, k)
    if sigma > 0.3:
        pm = cv2.GaussianBlur(pm, (0, 0), sigma)
        al = cv2.GaussianBlur(al, (0, 0), sigma)
    return pm, al


def grain_field(seed, amp, size=3):
    r = np.random.default_rng(seed)
    g = r.normal(0, 1, (H // size + 1, W // size + 1)).astype(np.float32)
    return cv2.resize(g, (W + size, H + size), interpolation=cv2.INTER_NEAREST)[:H, :W] * amp


def over_man(bg, pm, al, gr):
    """The man over the frame: his colour plus grain (orange-black speckle, on him only)."""
    man = pm + gr[..., None] * np.float32([1.0, 0.36, 0.14]) * al[..., None]
    return bg * (1 - al[..., None]) + np.clip(man, 0, 255)


def r_evil():
    a0, a1 = TM.B["evil"]
    n = round(a1 * FPS) - round(a0 * FPS)
    at = lambda k: TM.T[k] - a0 - 0.03                  # a word's onset in this clip (seconds), a hair early
    t_cut = TM.T["most"] - a0 - 2 / FPS                 # the cut lands two frames before "most"
    noh, horn = Cutout(f"{V6}/cut_a.png"), Cutout(f"{V6}/cut_b.png")
    # the reference's sizes: the head 280 px wide in the wide shot (centre 0.42 of the width), 480 px after the cut
    # (1.69x); Fink's head is 443 px wide in his cut-out
    s_w, hx, ht = 0.70, (289 + 732) / 2, 133             # cut-out: head centre x, head top (its pixels)
    s_c = s_w * 1.69
    rx, ry = [p[0] for p in RISE], [p[1] for p in RISE]
    # the small words (the reference: centred, ~54 px regular; the key word bold italic ~78 px with a glow spot)
    small = []
    cy = H * 0.5
    # v9 ("The most evil company in the world."): only "The" is said before the cut, so it is the one small word
    for word, key, x, kind in (("the", "the3", 0.5, "r"),):
        if kind == "b":
            a = text_alpha(word, HEROS_B, 84, x * W, cy=cy, shear=0.21)
            gl = glow_of(a, [(9, 0.8), (40, 0.9), (110, 0.8)])
        else:
            a = text_alpha(word, HEROS_R, 54, x * W, cy=cy)
            gl = glow_of(a, [(7, 0.6), (26, 0.35)])
        small.append((a, gl, at(key), key))
    # as wide as the reference's words ("terrible" ~1400 px, "boss" ~1500 px) so they read around him
    most_a = text_alpha("most", LIB, 720, W / 2, baseline=0.39 * H)
    evil_a = text_alpha("evil", LIB, 960, W / 2, baseline=0.89 * H)
    most_g = glow_of(most_a, [(14, 0.9), (40, 0.75), (110, 0.45)])
    evil_g = glow_of(evil_a, [(16, 0.9), (48, 0.75), (130, 0.45)])
    t_most, t_evil = at("most"), at("evil")
    wr = Writer(f"{CLIPS}/v6_evil.mp4")
    prev_top = None
    for i in range(n):
        t = i / FPS
        fr = np.empty((H, W, 3), np.float32)
        fr[:] = RED
        if t < t_cut:                                    # ---- the rise
            top = np.interp(t, rx, ry) * H
            v = 0 if prev_top is None else abs(top - prev_top)   # px per 60 fps frame
            prev_top = top
            x0 = 0.44 * W - hx * s_w
            y0 = top - ht * s_w
            hf = smooth((t - (t_cut - 0.10)) / 0.10)         # the horns fade in over the last 0.1 s
            pm, al = noh.place(s_w, x0, y0)
            if hf > 0:
                pm2, al2 = horn.place(s_w, x0, y0)
                pm, al = pm * (1 - hf) + pm2 * hf, al * (1 - hf) + al2 * hf
            pm, al = soften(pm, al, sigma=2.2, vblur=min(60, v * 1.0))
            fr = over_man(fr, pm, al, grain_field(7000 + i, 0.0))      # no grain added (the user, Nov 22)
            # the small words: each on its onset (fading in over ~0.1 s), gone at the next word of its group / the cut
            for a, gl, ta, key in small:
                if t < ta:
                    continue
                nxt = t_cut
                if t >= nxt - 1 / FPS:
                    continue
                op = smooth((t - ta) / 0.10)
                fr = put_text(fr, a, op, gl, fringe=2)
        else:                                            # ---- the close-up
            u = t - t_cut
            top_f = 0.135 + 0.018 * np.exp(-u / 0.06) - 0.013 * smooth(u / 1.0)   # his skull's top (the horns'
            x0 = 0.48 * W - hx * s_c                                            # tips just inside the frame)
            y0 = top_f * H - ht * s_c
            pm, al = horn.place(s_c, x0, y0)
            # out of focus at the cut, a little less by "evil"; the grain builds from almost none to full by "evil"
            ue = (t - t_cut) / max(0.2, t_evil + 0.05 - t_cut)
            sigma = 10.0 - 3.5 * smooth(ue)
            gamp = 0.0                                   # (was building to heavy grain; the user: the photo's own)
            # the type behind him
            if t >= t_most:
                fr = put_text(fr, most_a, 1 - np.exp(-(t - t_most) / 0.062), most_g, fringe=3)
            if t >= t_evil:
                fr = put_text(fr, evil_a, 1 - np.exp(-(t - t_evil) / 0.040), evil_g, fringe=3)
            pm, al = soften(pm, al, sigma=sigma)
            fr = over_man(fr, pm, al, grain_field(7300 + i, gamp))
        wr.write(fr)
    wr.close()
    print(f"   evil: {n} frames; cut at {t_cut:.3f}s ('most' {t_most:.3f}, 'evil' {t_evil:.3f})")


ALL = {"evil": r_evil}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
