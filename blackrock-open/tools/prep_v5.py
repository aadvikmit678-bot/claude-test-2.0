"""v5 renderers (the user's notes of Nov 21, late night).

  rest2    "Back in the 1980s" to the end, re-cut from scratch (the user: "a lot of edits … why do you stick to only one
           video for that line … more videos of Larry Fink and BlackRock … not just stock videos", "I don't want a
           slideshow of clips"). The shot list is shotlist.REST2_V5; every shot is cut on a word of the aligned voice, is
           0.25-0.8 s long and moves (a slow push-in, as the Porsche reel's shots all drift), the 1980s run carries an
           old film look (warm, faded, soft, grain at low opacity, a little gate weave). Most of it is the Larry Fink
           documentary from the Dimon drive (1980s Wall Street, the 1980s photo of young Fink on the trading floor,
           First Boston, 2008 on the floor, BlackRock's signs, Fink at the NYSE); its small burned-in words are painted
           out (the film writes its own captions).
  rogan    Elon's question and then Rogan listening (the user: "When Elon was saying 'company,' cut to Joe Rogan's face
           … not saying anything for about 1 second, contemplating … then with a flash cut to the next part"), in the
           Palmer Luckey reel's look: a slow push, the soft corners, grain. Rogan's shot is the clip's caption-free
           listening shot (9.23 s on), its picture-in-picture inset patched from the clean frame before it appears.
  dimon5   "That's Jamie Dimon": refff's band and timing, the band in the ON EARTH red, the name in the white glow.
  solomon5 "David Solomon": the same device.
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np

import prep_v3 as P
import prep_v4 as P4
import shotlist as SL
import timing as TM
from common import CLIPS, DL, FPS, H, PANEL, W, Writer, affine, center_focus, grab, grain, vignette

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIMON = os.path.abspath(f"{ROOT}/../dimon-src")
V3 = P.V3
EARTH_RED = np.array([125, 1, 1], np.float32)     # the ON EARTH background (red_bg_user.jpg is this flat red)

SRC = {
    "LFM": f"{DIMON}/_drive/larry fink metro media house.mp4",   # the Larry Fink documentary (1276x718)
    "WS": f"{DIMON}/_drive/wall street videos montge edits.mp4",
    "BM": f"{DIMON}/_drive/banking montage 1-2 sec clip can be used.mp4",
    "B2": f"{DIMON}/_v12/dl/broll2.mp4",
    "CR": f"{DIMON}/_direct/crash_2008.mp4",
    "FI": f"{DIMON}/_direct/fired_push_scene.mp4",
    "FE3": f"{DL}/fink_edit3.mp4",
    "FK2": f"{DL}/m_fink2.mp4",
    "MBS": f"{DL}/m_blackrock_start.mp4",
    "EYE": f"{V3}/pin/eye.mp4",
    "ML": f"{V3}/pin/money_laundering.mp4",
    "BZ": f"{V3}/new/bazzarbyte.mp4",
    "CO": f"{V3}/new/conspirant.mp4",
    "E": f"{V3}/ending_user.mp4",
    "P": PANEL,
    "TEX": f"{V3}/pin/money_tex.mp4",
    "MF": f"{DL}/m_finance.mp4",
    "GE": f"{DL}/good_edit_42s.mp4",
    "CALC": f"{DL}/v5/calc_user.mp4",            # the user's chalkboard clip (Nov 21): "calculating"
    "AL": f"{DL}/v5/aladdin_user.mp4",          # the user's Aladdin clip (Nov 21): the genie, its 8-9 s
}
for k in ("1_a", "1_b", "2_a", "2_b", "3_a", "3_b"):
    SRC[f"HF{k}"] = f"{V3}/higgsfield/shot{k}.mp4"

# fixed crops (source pixels): the montages' badges and subtitles, the vertical videos' 16:9 bands
CROP = {
    "MBS": "crop=iw*0.70:ih*0.70:iw*0.15:ih*0.08",       # econpill: its badge (top left) and subtitles (bottom)
    "ML": "crop=720:405:0:440",
    "E": "crop=700:394:18:4",                           # the user's ending video, centred (its watermark painted out)
}


def band(y):
    return f"crop=1080:608:0:{y}"


_AUTO = {}


def auto_crop(path, t):
    """The largest centred 16:9 crop inside the picture (drops pillar- and letter-boxing)."""
    key = (path, round(t, 1))
    if key in _AUTO:
        return _AUTO[key]
    fr = np.max([f.astype(np.float32).mean(axis=2) for f in grab(path, t, 3)], axis=0)
    rows = np.where(fr.mean(axis=1) > 14)[0]
    cols = np.where(fr.mean(axis=0) > 14)[0]
    h0, w0 = fr.shape
    y0, y1 = (rows[0], rows[-1] + 1) if len(rows) else (0, h0)
    x0, x1 = (cols[0], cols[-1] + 1) if len(cols) else (0, w0)
    bw, bh = x1 - x0, y1 - y0
    if bw / bh > 16 / 9:
        cw, ch = bh * 16 / 9, bh
    else:
        cw, ch = bw, bw * 9 / 16
    cw, ch = int(cw * 0.985) // 2 * 2, int(ch * 0.985) // 2 * 2
    cx, cy = x0 + (bw - cw) // 2, y0 + (bh - ch) // 2
    out = None if (cw >= w0 - 4 and ch >= h0 - 4) else f"crop={cw}:{ch}:{cx}:{cy}"
    _AUTO[key] = out
    return out


def decap(fr):
    """The Fink documentary's burned-in words (small white sans at the centre), painted out."""
    x0, x1, y0, y1 = int(W * .14), int(W * .86), int(H * .12), int(H * .72)
    reg = fr[y0:y1, x0:x1]
    mn, mx = reg.min(axis=2), reg.max(axis=2)
    m = ((mn > 228) & (mx - mn < 26)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for k in range(1, n):
        x, y, w, h, area = st[k]
        if h <= 110 and w <= 900 and area >= 5:
            keep[lab == k] = 1
    if not keep.any():
        return fr
    keep = cv2.dilate(keep, np.ones((9, 9), np.uint8))
    full = np.zeros((H, W), np.uint8)
    full[y0:y1, x0:x1] = keep
    return cv2.inpaint(np.ascontiguousarray(np.clip(fr, 0, 255).astype(np.uint8)), full, 6,
                       cv2.INPAINT_TELEA).astype(np.float32)


_WM = None


def dewatermark(fr):
    """The ending video's "@YS_MR4" + Instagram mark (top right), painted out; mask found once on its black frame."""
    global _WM
    if _WM is None:
        f = grab(SRC["E"], 1.9, 1, vf=CROP["E"] + ",setsar=1", size=(W, H))[0].astype(np.float32)
        m = np.zeros((H, W), np.uint8)
        reg = f[0:260, 1480:1920].max(axis=2)
        m[0:260, 1480:1920] = (reg > 70).astype(np.uint8)
        _WM = cv2.dilate(m, np.ones((15, 15), np.uint8))
    return cv2.inpaint(np.ascontiguousarray(np.clip(fr, 0, 255).astype(np.uint8)), _WM, 7,
                       cv2.INPAINT_TELEA).astype(np.float32)


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def look(fr, kind, i, seed):
    r = np.random.default_rng(seed * 1000 + i)
    if kind == "old":                                    # a 1980s print: warm, faded, soft, weaving, grain
        g = fr @ np.float32([0.299, 0.587, 0.114])
        fr = g[..., None] + (fr - g[..., None]) * 0.55
        fr = fr * np.float32([1.06, 1.0, 0.87]) + np.float32([12, 7, 0])
        fr = (fr - 128) * 0.92 + 128
        fr = cv2.GaussianBlur(fr, (0, 0), 0.7)
        fr = fr * (1 + 0.025 * r.uniform(-1, 1))
        dx, dy = r.uniform(-1.4, 1.4), r.uniform(-1.4, 1.4)
        fr = cv2.warpAffine(fr, np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
        fr = vignette(fr, 0.36)
        return fr + grain(seed=seed * 1000 + i, amt=5.0)
    if kind == "bw":
        g = fr @ np.float32([0.299, 0.587, 0.114])
        g = (g - 128) * 1.06 + 124
        fr = np.repeat(g[..., None], 3, axis=2)
        return vignette(fr, 0.3) + grain(seed=seed * 1000 + i, amt=4.2)
    fr = (fr - 128) * 1.03 + 128
    return vignette(fr, 0.16) + grain(seed=seed * 1000 + i, amt=2.6)


def transition(fr, kind, i):
    if kind == "flash":                                  # in on a white flash
        w = (1.0, 0.72, 0.42, 0.18, 0.06)
        return fr * (1 - w[i]) + 255 * w[i] if i < len(w) else fr
    if kind == "over":                                   # the Porsche reel's overexposed frame fading to normal
        if i < 9:
            e = 1 - i / 9
            return 255 - (255 - fr) * (1 - 0.88 * e)
        return fr
    if kind == "whip":                                   # a horizontal whip landing
        if i < 3:
            return P4.dir_blur(fr, (90, 55, 22)[i], 0)
        return fr
    if kind == "zoom":                                   # a zoom-blur punch in
        if i < 3:
            return P4.zoom_blur(fr, (0.10, 0.06, 0.025)[i])
        return fr
    return fr


def frames_for(spec, n, dur):
    """n frames (float RGB 1920x1080) for one shot."""
    src = spec["src"]
    if src == "BLACK":
        out = [np.zeros((H, W, 3), np.float32) for _ in range(n)]
        if spec.get("tex"):                              # the money texture, faint, in difference over black
            tex = grab(SRC["TEX"], spec["t0"], n, fps=FPS, size=(W, H))
            out = [np.asarray(t, np.float32) * spec["tex"] for t in tex] + out[len(tex):]
        return out
    path = SRC[src] if src in SRC else (f"{P.J2}/{src[2:]}.mp4" if src.startswith("J:") else src)
    t0 = spec["t0"]
    if "span" in spec:                                   # a source span time-mapped onto the shot
        speed = (spec["span"] - t0) / dur
    else:
        speed = spec.get("speed", 1.0)
    crop = spec.get("crop") or CROP.get(src)
    if crop is None and src not in ("P", "E") and not src.startswith(("HF", "J:")):
        crop = auto_crop(path, t0 + 0.05)
    vf = (crop + "," if crop else "") + "setsar=1"
    got = grab(path, t0, n, fps=FPS / speed, vf=vf, size=(W, H))
    got = [g.astype(np.float32) for g in got] or [np.zeros((H, W, 3), np.float32)]
    while len(got) < n:
        got.append(got[-1])
    return got


def shot_times(shots, a0, a1):
    def at(anchor):
        if anchor is None:
            return a0
        if isinstance(anchor, int):
            return TM.R(TM.ALIGN["rest"][anchor]["start"])
        if isinstance(anchor, tuple):
            return TM.F(TM.R(TM.ALIGN["rest"][anchor[0]]["start"]) + anchor[1])
        return TM.F(anchor)
    starts = [at(s["at"]) for s in shots]
    return list(zip(starts, starts[1:] + [a1]))


def render_montage(name, shots, a0, a1, seed=50):
    wr = Writer(f"{CLIPS}/{name}.mp4")
    bounds = shot_times(shots, a0, a1)
    for k, (spec, (a, b)) in enumerate(zip(shots, bounds)):
        n = round(b * FPS) - round(a * FPS)
        if n <= 0:
            print(f"   !! {name}: shot {k} ({spec['src']} {spec.get('t0')}) has no frames ({a:.3f}-{b:.3f})")
            continue
        frs = frames_for(spec, n, n / FPS)
        push, k0 = spec.get("push", 0.045), spec.get("k0", 1.0)
        fx, fy = spec.get("fx", 0.5) * W, spec.get("fy", 0.5) * H
        for i in range(n):
            fr = frs[i]
            if spec["src"] == "LFM":
                fr = decap(fr)
            if spec["src"] == "E":
                fr = dewatermark(fr)
            if spec["src"] == "P":                       # the panel's FII logo (top left)
                u8 = np.ascontiguousarray(np.clip(fr, 0, 255).astype(np.uint8))
                m = P.logo_mask(u8)
                reg = u8[:200, :420].astype(np.int16)        # and its green slash
                m[:200, :420] |= ((reg[..., 1] > 110) & (reg[..., 1] > reg[..., 0] + 30)).astype(np.uint8)
                m = cv2.dilate(m, np.ones((7, 7), np.uint8))
                fr = cv2.inpaint(u8, m, 9, cv2.INPAINT_TELEA).astype(np.float32)
            z = k0 * (1 + push * smooth(i / max(1, n - 1)))
            if abs(z - 1) > 1e-4:
                fr = affine(fr, z, fx, fy, fx, fy, border=(0, 0, 0))
            fr = look(fr, spec.get("look"), i, seed + k)
            fr = transition(fr, spec.get("fx_in"), i)
            wr.write(fr)
        print(f"   {k:2d} {a:7.3f}-{b:7.3f} {spec['src']:5s} {spec.get('t0', '')!s:>7} {spec.get('note', '')}")
    wr.close()


def r_rest2():
    render_montage("v5_rest2", SL.REST2_V5, *TM.B["rest2"])


# ------------------------------------------------------------------ Rogan: Elon's question, then Rogan listening
ROGAN_SRC = f"{DL}/rogan_elon.mp4"
ROGAN_BAND = "crop=1048:590:16:664"
REACT_T0 = 9.32           # Rogan, chin on hand, saying nothing (the clip's own caption is off from here)
REACT_CROP = "crop=800:450:16:680"   # the band's left 80 %: clear of the inset that slides in from the right


def palmer(fr, i, n, seed, push=0.05, fx=0.5, fy=0.45):
    """The Palmer Luckey reel's interview look: a slow push, soft corners, a filmic grade, grain."""
    z = 1 + push * smooth(i / max(1, n - 1))
    fr = affine(fr, z, fx * W, fy * H, fx * W, fy * H, border=(0, 0, 0))
    fr = (fr - 128) * 1.06 + 124
    fr = center_focus(np.clip(fr, 0, 255), zoom=0.016, gblur=3.0)
    return vignette(fr, 0.32) + grain(seed=seed + i, amt=3.2)


def r_rogan():
    n = round(TM.B["rogan"][1] * FPS) - round(TM.B["rogan"][0] * FPS)
    src = grab(f"{CLIPS}/rogan2.mp4", 0.0, n)               # the caption-free Elon clip (prep_v3 r_rogan2)
    wr = Writer(f"{CLIPS}/v5_rogan.mp4")
    for i in range(n):
        wr.write(palmer(src[min(i, len(src) - 1)].astype(np.float32), i, n, 7100, push=0.045, fx=0.56, fy=0.40))
    wr.close()
    # Rogan listening: his caption-free, inset-free moment (9.29-9.45 s; the clip's caption is off at 9.29 and a
    # picture-in-picture slides in from the right after 9.45), cropped clear of that edge and slowed into his second of
    # silence with frame blending, under a slow push-in
    n2 = round(TM.B["react"][1] * FPS) - round(TM.B["react"][0] * FPS)
    src2 = [f.astype(np.float32) for f in grab(ROGAN_SRC, REACT_T0, 9, fps=FPS, vf=REACT_CROP + ",setsar=1",
                                               size=(W, H))]
    fr = []
    for i in range(n2):
        u = i / max(1, n2 - 1) * (len(src2) - 1)
        j = int(u)
        w = u - j
        fr.append(src2[j] * (1 - w) + src2[min(j + 1, len(src2) - 1)] * w)
    wr = Writer(f"{CLIPS}/v5_react.mp4")
    for i in range(n2):
        wr.write(palmer(fr[i], i, n2, 7300, push=0.07, fx=0.42, fy=0.38))
    wr.close()


# ------------------------------------------------------------------ the intros: refff's band in the ON EARTH red, the name glowing
def intro(name, beat, person, s, ox, oy, title, that=None, words=(), seed=1700):
    n = P.beat_frames(beat)
    t0 = round(TM.B[beat][0] * FPS)
    rel = lambda w: round(TM.T[w] * FPS) - t0
    frs = P.person_frames(person, n, s, ox, oy, clean=True)
    name_base = 392
    name_a, name_box = P.word_layer(title, P.SERIF, 172, 108, name_base)
    that_a = None
    if that:
        that_a, _ = P.word_layer(that, P.SERIF_I, 84, 112, int(name_box[1]) - 18)
    off = name_base / H - P4.REF_BASE
    serif_base = int((P4.REF_BAND[-1][1] + off) * H) + 108
    layers, x = [], 112
    for w, key in words:
        a, box = P.word_layer(w, P.SERIF, 138, x, serif_base)
        layers.append((a, box, rel(key)))
        x = box[2] + 36
    keys = [k for k, _ in P4.REF_BAND]
    vals = [v for _, v in P4.REF_BAND]
    glow1 = cv2.GaussianBlur(name_a, (0, 0), 10)
    glow2 = cv2.GaussianBlur(name_a, (0, 0), 34)
    wr = Writer(f"{CLIPS}/{name}.mp4")
    for i in range(n):
        img, pa = frs[i]
        rf = i / 2.0
        bg = img.copy()
        if rf >= 4:
            edge = (np.interp(rf, keys, vals) + off) * H
            bnd = np.zeros((H, W), np.float32)
            bnd[:int(edge)] = 1.0
            bg = P.over_color(bg, cv2.GaussianBlur(bnd, (0, 0), 1.2), EARTH_RED)
        if that_a is not None:
            if 4 <= rf < 6:
                sq = np.zeros((H, W), np.float32)
                sq[300:332, 112:144] = 1
                bg = P.over_color(bg, sq, P.WHITE)
            elif rf >= 6:
                bg = P.over_color(bg, that_a, P.WHITE)
        f30 = int(rf)
        op = P4.REF_WORD.get(f30, 1.0 if f30 > 14 else 0.0)
        if op > 0:                                        # the name: refff's flicker, then the white glow (a bloom
            bloom = 1.0 + 1.6 * max(0.0, 1 - (rf - 14) / 6) if f30 >= 14 else 1.0   # as it lands, settling)
            g = np.clip(glow1 * 0.75 * bloom + glow2 * 0.55 * bloom, 0, 1) * op
            bg = bg + (np.float32([255, 255, 255]) - bg) * g[..., None] * 0.6
            bg = P.over_color(bg, name_a * op, (251, 248, 236))
        fg = img
        kind = P4.REF_FLASH.get(f30)
        if kind == "wash":
            bg, fg = bg * 0.6 + 255 * 0.4, fg * 0.55 + 255 * 0.45
        elif kind == "wash2":
            bg, fg = bg * 0.35 + 255 * 0.65, fg * 0.3 + 255 * 0.7
        elif kind == "sil":
            fg = fg * 0.05 + 255 * 0.95
        fr = bg * (1 - pa[..., None]) + fg * pa[..., None]
        for a, box, k in layers:
            st = P.block_entrance(i, k)
            if st == "ghost":
                fr = P.over_color(fr, a * 0.35, P.WHITE)
            elif st == "block":
                fr = P.glow_text(fr, P.block_layer(box), (255, 255, 255), glow=0.8)
            elif st == "word":
                sh = cv2.GaussianBlur(a, (0, 0), 9)
                fr = fr * (1 - 0.5 * np.clip(sh * 1.5, 0, 1))[..., None]
                fr = P.glow_text(fr, a, (246, 244, 240), glow=0.75)
        wr.write(fr + grain(seed=seed + i, amt=2.2))
    wr.close()


def r_dimon5():
    intro("v5_dimon", "dimon", "dimon", 1.2, 0.0, -60.0, "Jamie Dimon", that="That’s",
          words=[("the", "the1"), ("guy", "guy1"), ("running", "running")], seed=1700)


def r_solomon5():
    intro("v5_solomon", "solomon", "solomon", 1.3, -4.0, -40.0, "David Solomon", seed=1900)


ALL = {"rest2": r_rest2, "rogan": r_rogan, "dimon5": r_dimon5, "solomon5": r_solomon5}

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
