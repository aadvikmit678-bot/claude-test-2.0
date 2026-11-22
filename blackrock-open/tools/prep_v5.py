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
# v6 (Nov 22): the second half on real footage -- the new BlackRock documentaries and the Dimon drive's long ones
SRC.update({
    "BR15": f"{DL}/v6/docs/br_15t_machine.mp4", "BRC": f"{DL}/v6/docs/br_conspiracies.mp4",
    "BRL": f"{DL}/v6/docs/br_largest.mp4", "BRE": f"{DL}/v6/docs/br_edit.mp4",
    "STO": f"{DIMON}/_direct/stories_2008_recession.mp4", "MPB": f"{DIMON}/_direct/most_powerful_banker_doc.mp4",
    "HOW": f"{DIMON}/_direct/how_jpm_became_largest.mp4", "UNT": f"{DIMON}/_direct/untold_career_story.mp4",
    "AX": f"{V3}/new/axirohq.mp4", "ASH": f"{V3}/new/asher.mp4", "MFC": f"{DL}/m_finance_clips.mp4",
    "MONEY": f"{DL}/v6/money_user.mp4",          # the user's fire clip (Nov 22): "three times the money"
})
for k in ("1_b", "3_a", "3_b"):                  # the Higgsfield takes at 60 fps (motion-interpolated), real speed
    SRC[f"HF6_{k[0]}{k[2]}"] = f"{DL}/v6/hf60/shot{k}.mp4"

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


def shift_down(fr, dy):
    """The picture moved down dy px (to centre what sits high in it); the uncovered top takes its top edge's colours."""
    dy = int(dy)
    out = np.empty_like(fr)
    out[dy:] = fr[:H - dy]
    edge = cv2.GaussianBlur(fr[:24], (0, 0), 6).mean(axis=0, keepdims=True)   # the top edge's colours, stretched up
    out[:dy] = cv2.GaussianBlur(np.repeat(edge, dy, axis=0), (0, 0), 14)
    return out


# the user's ending video puts its objects high in the frame; each source window below is moved down by that share of
# the height so the object sits in the centre (read off its frames at 30 fps): the camera on red, its white glow, its
# line drawings, the glasses' glow, the glasses on red and glowing, their drawings, the phone
E_PAN = [(0.395, 0.465, 0.22), (0.465, 0.495, 0.20), (0.495, 0.625, 0.18), (0.625, 0.660, 0.30), (0.660, 0.765, 0.12),
         (0.765, 0.895, 0.06), (0.895, 1.200, 0.10)]


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
    if kind == "dimw":                                   # bright footage under the white type: brought down until the
        c = float(fr[H // 4:3 * H // 4, W // 5:4 * W // 5].mean())    # type's white glow reads (the user: white glow
        if c > 92.0:                                                   # only, never a dark shadow behind the words)
            fr = fr * (92.0 / c)
        kind = None
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
    got = got or [np.zeros((H, W, 3), np.uint8)]          # uint8 until used (a long take is 200+ frames)
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
            fr = np.asarray(frs[i], np.float32)
            if spec["src"] == "LFM":
                fr = decap(fr)
            if spec["src"] == "E":
                fr = dewatermark(fr)
            if spec.get("pan"):                          # source windows shown moved down (see E_PAN)
                ts = spec["t0"] + i * spec.get("speed", 1.0) / FPS
                for p0, p1, dy in (E_PAN if spec["pan"] == "E" else spec["pan"]):
                    if p0 <= ts < p1:
                        fr = shift_down(fr, dy * H)
                        break
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


def r_owns():
    """\"that owns a piece of\": the user's ending video from its glasses (0.6 s), panned so the glasses sit in the
    centre, for 0.45 s; then the two brand maps ("but everything you own") from the Fink edit."""
    a0, a1 = TM.B["logos"]
    shots = [dict(at=None, src="E", t0=0.633, push=0.04, pan="E", note="the glasses, centred, then the phone"),
             dict(at=a0 + 0.45, src="FE3", t0=22.5, look="bw", fx_in="zoom", note="the brands"),
             dict(at=a0 + 0.783, src="FE3", t0=24.1, look="bw", note="the media map")]
    render_montage("v6_owns", shots, a0, a1, seed=80)


def r_rest2(part=None, parts=4):
    """The second half; `part` k of `parts` renders a contiguous run of shots to v6_rest2_p{k}.mp4 (run the parts in
    parallel, then `rest2join` concatenates them -- identical frames to a single pass)."""
    shots, (a0, a1) = SL.REST2_V6, TM.B["rest2"]
    if part is None:
        render_montage("v6_rest2", shots, a0, a1)
        return
    bounds = shot_times(shots, a0, a1)
    cut = [round(len(shots) * k / parts) for k in range(parts + 1)]
    sub = shots[cut[part]:cut[part + 1]]
    s0 = bounds[cut[part]][0]
    s1 = bounds[cut[part + 1] - 1][1]
    sub = [dict(sh, at=(s0 if j == 0 else sh["at"])) for j, sh in enumerate(sub)]
    render_montage(f"v6_rest2_p{part}", sub, s0, s1, seed=50 + cut[part])


def r_rest2join(parts=4):
    lst = f"{CLIPS}/v6_rest2_parts.txt"
    with open(lst, "w") as f:
        for k in range(parts):
            f.write(f"file 'v6_rest2_p{k}.mp4'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    f"{CLIPS}/v6_rest2.mp4"], check=True)
    for k in range(parts):
        os.remove(f"{CLIPS}/v6_rest2_p{k}.mp4")
    os.remove(lst)


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
def hero_words(text, size, y, seed):
    """A centred line in the JPMorgan Chase / Goldman Sachs title type (Inter Display Bold, speckled white) and the
    x where each of its words ends, so the words can come in one by one in their final, centred places."""
    from PIL import ImageFont
    a = P.hero_text(text, size, seed, y=y)
    f = ImageFont.truetype(P.INTER_B, size)
    left = W / 2 - f.getlength(text) / 2
    ends, acc = [], ""
    for w in text.split():
        acc = (acc + " " + w).strip()
        ends.append(left + f.getlength(acc) + size * 0.12)
    return a, ends


def intro(name, beat, person, s, ox, oy, title, that=None, words=(), until=None, seed=1700):
    """refff's device (the band, the flashes, the flicker) with the type the user picked on Nov 22: the names set
    exactly like the "JPMorgan Chase" / "Goldman Sachs" titles, centred -- "That's Jamie Dimon, the guy running"."""
    n = P.beat_frames(beat)
    t0 = round(TM.B[beat][0] * FPS)
    rel = lambda w: round(TM.T[w] * FPS) - t0
    frs = P.person_frames(person, n, s, ox, oy, clean=True)
    off = 392 / H - P4.REF_BASE
    ys = (420, 540, 668) if that else (None, 540, 668)
    that_a = P.hero_text(that, 76, seed + 1, y=ys[0]) if that else None
    name_a = P.hero_text(title, 150, seed + 2, y=ys[1])
    line_a, ends = hero_words(" ".join(w for w, _ in words), 96, ys[2], seed + 3) if words else (None, [])
    keys = [k for k, _ in P4.REF_BAND]
    vals = [v for _, v in P4.REF_BAND]
    k_until = rel(until) - 2 if until else n
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
        f30 = int(rf)
        fg = img
        kind = P4.REF_FLASH.get(f30)
        if kind == "wash":
            bg, fg = bg * 0.6 + 255 * 0.4, fg * 0.55 + 255 * 0.45
        elif kind == "wash2":
            bg, fg = bg * 0.35 + 255 * 0.65, fg * 0.3 + 255 * 0.7
        elif kind == "sil":
            fg = fg * 0.05 + 255 * 0.95
        fr = bg * (1 - pa[..., None]) + fg * pa[..., None]
        if i < k_until:
            if that_a is not None and rf >= 6:            # "That's" from refff's second wash
                fr = P.with_caption(fr, that_a, shadow=0.6)
            op = P4.REF_WORD.get(f30, 1.0 if f30 > 14 else 0.0)
            if op > 0:                                    # the name: refff's flicker (ghost, gone, half, gone, solid)
                fr = P.with_caption(fr, name_a * op, shadow=0.6 * op)
            if line_a is not None:                        # "the guy running": each word on its own onset, in place
                shown = [e for (w, key), e in zip(words, ends) if i >= rel(key)]
                if shown:
                    m = line_a.copy()
                    m[:, int(shown[-1]):] = 0
                    fr = P.with_caption(fr, m, shadow=0.6)
        wr.write(fr + grain(seed=seed + i, amt=2.2))
    wr.close()


def r_dimon5():
    intro("v5_dimon", "dimon", "dimon", 1.2, 0.0, -60.0, "Jamie Dimon", that="That’s",
          words=[("the", "the1"), ("guy", "guy1"), ("running", "running")], seed=1700)


def r_solomon5():
    # "David Solomon" until "a part-time" (the captions write "a part-time DJ" in the centre)
    intro("v5_solomon", "solomon", "solomon", 1.3, -4.0, -40.0, "David Solomon", until="a3", seed=1900)


ALL = {"rest2": r_rest2, "rogan": r_rogan, "dimon5": r_dimon5, "solomon5": r_solomon5, "owns": r_owns,
       "rest2join": r_rest2join}
ALL.update({f"rest2p{k}": (lambda k=k: r_rest2(part=k)) for k in range(4)})

if __name__ == "__main__":
    for name in (sys.argv[1:] or ALL):
        print("--", name)
        ALL[name]()
