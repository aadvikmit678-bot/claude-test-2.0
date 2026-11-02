#!/usr/bin/env python3
"""Build the Pattinson edit (HyperFrames).

1. prepares every clip/still from ./source (4:3 crops, 24 fps, burned-text avoidance)
2. writes compositions/*.html (scenes, captions, fx) and index.html (hosts + audio mix)
3. applies the looks through `npx hyperframes media-treatment` (data-look selectors)

Run from the project root:  python3 tools/build.py [--no-media] [--no-looks]
Style source: ../reference/sam-altman-reel-breakdown.md and SPEC.md.
"""
import hashlib
import html
import json
import os
import subprocess
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "source")
FPS = 24
W, H = 1440, 1080
FRAME = 1 / FPS
DO_MEDIA = "--no-media" not in sys.argv
DO_LOOKS = "--no-looks" not in sys.argv


def fr(t):
    """Snap a time to the frame grid."""
    return round(t * FPS) / FPS


def ts(t):
    return f"{t:.6f}".rstrip("0").rstrip(".") if t else "0"


EPS = 0.0002   # start each element a hair early so a clip ending on a frame boundary and the next one starting there always touch


def t0s(a):
    return ts(max(0.0, a - EPS))


def tds(a, d):
    return ts(d + (a - max(0.0, a - EPS)))


# --------------------------------------------------------------------------------------------
# Timeline: cold open, VO in four blocks, three receipts, sting
# --------------------------------------------------------------------------------------------
VO_START = 5.875
SPLITS = [(0.0, 24.92), (24.92, 30.40), (30.40, 48.25), (48.25, 59.716)]
INS = [2.40, 3.67, 1.45]                      # spider monkey, Kimmel, Chris Hansen
OFF = [VO_START,
       VO_START + INS[0],
       VO_START + INS[0] + INS[1],
       VO_START + INS[0] + INS[1] + INS[2]]
INS_T = [SPLITS[0][1] + OFF[0], SPLITS[1][1] + OFF[1], SPLITS[2][1] + OFF[2]]
VO_END_T = SPLITS[3][1] + OFF[3]
TOTAL = 76.8
STING_T = 73.9


def ve(v):
    """VO seconds -> output seconds for an END time (a split end stays in its own block)."""
    return vt(v - 1e-6) + 1e-6


def vt(v):
    """VO seconds -> output seconds."""
    for (a, b), o in zip(SPLITS, OFF):
        if v < b - 1e-9:
            return v + o
    return v + OFF[-1]


# --------------------------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------------------------
V = {
    "SF": "Starting frame.mp4", "GM": "General montage.mp4", "MP": "Montage of pattison.mp4",
    "MB": "Montage + batman clip at 25thsec.mp4", "CB": "Robert Pattison crazy batman edit.mp4",
    "FM": "Pattison face montage from multiple films.mp4", "PM2": "Pattison montage 2.mp4",
    "AMC": "Robert Pattison all movie clips with names on top right.mp4", "PT": "Primetime.mp4",
    "CV": "patison clear video wo text.mp4", "NCW": "Pattison News carpet walk.mp4",
    "RAW": "Pattison raw video.mp4", "PF": "Pattison photo frame. In centre.mp4",
    "ST": "Pattison story twilight.mp4", "TW": "Watch Edward & Bella Fall in Love in Twilight.mp4",
    "KM": "Robert Pattinson on Telling People He’s a Pathological Liar & Working with Zendaya on Three Films.mp4",
}
LETTERBOX = {"TW": (0, 92, 1280, 536)}       # picture area inside the 1280x720 letterboxed video
_dims = {}


def dims(path):
    if path not in _dims:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height", "-of", "csv=p=0", path],
                             capture_output=True, text=True).stdout.strip().split(",")
        _dims[path] = (int(out[0]), int(out[1]))
    return _dims[path]


def crop_rect(sw, sh, fx=0.5, fy=0.5, zoom=1.0, area=None, aspect=4 / 3):
    ax, ay, aw, ah = area if area else (0, 0, sw, sh)
    if aw / ah > aspect:
        ch = ah / zoom
        cw = ch * aspect
    else:
        cw = aw / zoom
        ch = cw / aspect
    x = ax + (aw - cw) * fx
    y = ay + (ah - ch) * fy
    return int(round(cw)) // 2 * 2, int(round(ch)) // 2 * 2, int(round(x)), int(round(y))


def _stamp(out, params):
    return out + ".json", json.dumps(params, sort_keys=True)


def _fresh(out, params):
    side, blob = _stamp(out, params)
    return os.path.exists(out) and os.path.exists(side) and open(side).read() == blob


def _mark(out, params):
    side, blob = _stamp(out, params)
    open(side, "w").write(blob)


MEDIA_LOG = []


# The movie-clips reel carries a title/character block top-left and a watermark top-right:
# zoom 1.2 anchored to the bottom drops the top 17 % of the frame.
KEY_DEFAULTS = {"AMC": dict(zoom=1.3, fy=1.0)}


def _kd(key, fy, zoom):
    d = KEY_DEFAULTS.get(key)
    if d and zoom == 1.0 and fy == 0.5:
        return d["fy"], d["zoom"]
    return fy, zoom


def clip(cid, key, ss, dur, fx=0.5, fy=0.5, zoom=1.0, area=None, vf="", aspect=4 / 3, size=(W, H)):
    """Cut a source segment into assets/clips/<cid>.mp4 at 24 fps, cropped to `aspect`."""
    fy, zoom = _kd(key, fy, zoom)
    src = os.path.join(SRC, V[key])
    out = os.path.join(ROOT, "assets", "clips", f"{cid}.mp4")
    sw, sh = dims(src)
    cw, ch, x, y = crop_rect(sw, sh, fx, fy, zoom, area or LETTERBOX.get(key), aspect)
    params = dict(src=V[key], ss=round(ss, 3), dur=round(dur, 3), crop=[cw, ch, x, y], vf=vf, size=size)
    MEDIA_LOG.append((cid, params))
    if DO_MEDIA and not _fresh(out, params):
        chain = f"crop={cw}:{ch}:{x}:{y},scale={size[0]}:{size[1]}:flags=lanczos,fps={FPS}"
        if vf:
            chain = f"{vf},{chain}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur + 0.25:.3f}",
                        "-i", src, "-vf", chain + ",format=yuv420p", "-an", "-c:v", "libx264",
                        "-crf", "17", "-preset", "veryfast", "-g", "12", out], check=True)
        _mark(out, params)
    return f"assets/clips/{cid}.mp4"


def still(cid, rel, fx=0.5, fy=0.5, zoom=1.0, aspect=4 / 3, size=(1584, 1188)):
    """Crop a photo to `aspect` around a focus point into assets/img/<cid>.jpg."""
    src = os.path.join(SRC, rel)
    out = os.path.join(ROOT, "assets", "img", f"{cid}.jpg")
    params = dict(src=rel, fx=fx, fy=fy, zoom=zoom, aspect=aspect, size=size)
    MEDIA_LOG.append((cid, params))
    if DO_MEDIA and not _fresh(out, params):
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        cw, ch, x, y = crop_rect(im.width, im.height, fx, fy, zoom, None, aspect)
        im.crop((x, y, x + cw, y + ch)).resize(size, Image.LANCZOS).save(out, quality=92)
        _mark(out, params)
    return f"assets/img/{cid}.jpg"


def frame(cid, key, t, fx=0.5, fy=0.5, zoom=1.0, area=None, aspect=4 / 3, size=(1584, 1188)):
    """Grab one video frame as a still (for montages on twos)."""
    fy, zoom = _kd(key, fy, zoom)
    src = os.path.join(SRC, V[key])
    out = os.path.join(ROOT, "assets", "img", f"{cid}.jpg")
    sw, sh = dims(src)
    cw, ch, x, y = crop_rect(sw, sh, fx, fy, zoom, area or LETTERBOX.get(key), aspect)
    params = dict(src=V[key], t=round(t, 3), crop=[cw, ch, x, y], size=size)
    MEDIA_LOG.append((cid, params))
    if DO_MEDIA and not _fresh(out, params):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
                        "-vf", f"crop={cw}:{ch}:{x}:{y},scale={size[0]}:{size[1]}:flags=lanczos",
                        "-q:v", "2", out], check=True)
        _mark(out, params)
    return f"assets/img/{cid}.jpg"


# --------------------------------------------------------------------------------------------
# Looks (persisted via `npx hyperframes media-treatment`, one JSON per look)
# --------------------------------------------------------------------------------------------
BASE_ADJ = {"contrast": 0.28, "blacks": -0.35, "highlights": -0.05, "saturation": -0.10}
BASE_DET = {"vignette": 0.5, "vignetteFeather": 0.6, "grain": 0.16, "grainSize": 0.3}
BASE_FX = {"chromaticAberration": 0.10, "filmArtifacts": 0.30, "bloom": 0.35, "bloomRadius": 12}
LOOKS = {
    "base": {"adjust": BASE_ADJ, "details": BASE_DET, "effects": BASE_FX},
    "mono": {"preset": "mono-clean", "intensity": 1, "adjust": dict(BASE_ADJ, contrast=0.38),
             "details": BASE_DET, "effects": BASE_FX},
    "halftone": {"preset": "mono-clean", "intensity": 1, "adjust": dict(BASE_ADJ, contrast=0.42, saturation=-1),
                 "details": dict(BASE_DET, grain=0.22),
                 "effects": dict(BASE_FX, halftone=0.92, halftoneSize=0.24, bloom=0.2)},
    "oldfilm": {"preset": "mono-clean", "intensity": 1, "adjust": dict(BASE_ADJ, contrast=0.4),
                "details": dict(BASE_DET, grain=0.4, grainSize=0.45, vignette=0.62),
                "effects": dict(BASE_FX, filmArtifacts=0.9)},
    "vhs": {"preset": "vhs-playback", "intensity": 0.85, "details": dict(BASE_DET, vignette=0.55)},
    "neon": {"adjust": dict(BASE_ADJ, saturation=0.15), "details": BASE_DET,
             "effects": dict(BASE_FX, bloom=1.1, bloomRadius=18)},
    "glitch": {"adjust": BASE_ADJ, "details": BASE_DET,
               "effects": dict(BASE_FX, digitalGlitch=0.5, digitalGlitchColorSplit=0.35,
                               digitalGlitchLineTear=0.3, digitalGlitchBlockAmount=0.45)},
    "red": {"adjust": {"exposure": 0.45, "contrast": 0.15}, "details": dict(BASE_DET, vignette=0.45),
            "effects": {"monoScreen": 1, "monoScreenSize": 0.14, "monoScreenSpread": 0.55,
                        "chromaticAberration": 0.15}, "palette": ["#000000", "#e3121b"]},
    "print": {"adjust": dict(BASE_ADJ, saturation=0.1), "details": BASE_DET,
              "effects": dict(BASE_FX, halftone=0.6, halftoneSize=0.26)},
}

# --------------------------------------------------------------------------------------------
# Scene model
# --------------------------------------------------------------------------------------------
SCENES = []   # dicts: id, t0, t1, items(list)


def scene(sid, t0, t1):
    s = dict(id=sid, t0=fr(t0), t1=fr(t1), items=[])
    SCENES.append(s)
    return s


def media_shot(sc, t0, t1, src, look="base", move="push", z=1, kind=None, extra=None):
    kind = kind or ("video" if src.endswith(".mp4") else "img")
    sc["items"].append(dict(type="shot", t0=fr(t0), t1=fr(t1), src=src, look=look, move=move, z=z,
                            kind=kind, extra=extra or {}))


def card(sc, t0, t1, z=1, glow=True):
    sc["items"].append(dict(type="card", t0=fr(t0), t1=fr(t1), z=z, glow=glow))


def twos(sc, t0, t1, srcs, look="base", z=1, step=2):
    """Montage on twos: each still holds `step` frames."""
    t = fr(t0)
    i = 0
    while t < fr(t1) - 1e-6 and i < len(srcs):
        nxt = min(fr(t1), fr(t + step * FRAME))
        if i == len(srcs) - 1:
            nxt = fr(t1)
        lk = srcs[i][1] if isinstance(srcs[i], tuple) else look
        sp = srcs[i][0] if isinstance(srcs[i], tuple) else srcs[i]
        media_shot(sc, t, nxt, sp, look=lk, move="none", z=z)
        t = nxt
        i += 1


def compound(sc, t0, t1, kind, z=1, **kw):
    sc["items"].append(dict(type=kind, t0=fr(t0), t1=fr(t1), z=z, **kw))


FX = []        # global overlay items (slams, flashes, sting)
SFX = []       # (T, name, volume)


def slam(t, word, frames=2):
    FX.append(dict(type="slam", t0=fr(t), t1=fr(t + frames * FRAME), word=word))


def flash(t, frames=1, kind="white"):
    FX.append(dict(type="flash", t0=fr(t), t1=fr(t + frames * FRAME), kind=kind))


def sfx(t, name, vol=0.4):
    SFX.append((t, name, vol))


# --------------------------------------------------------------------------------------------
# EDL
# --------------------------------------------------------------------------------------------
WORDS = json.load(open(os.path.join(ROOT, "work", "vo", "words_refined.json")))


def build_edl():
    # ---- S01 cold open (original voices, music removed) -----------------------------------
    s = scene("s01", 0, VO_START)
    media_shot(s, 0, 3.0833, "assets/clips/c0_autograph.mp4", move="push")
    media_shot(s, 3.0833, VO_START, "assets/clips/c4_antinous.mp4", move="push")
    sfx(3.083 + FRAME, "whoosh-short", 0.3)
    flash(VO_START - FRAME, 1)
    sfx(VO_START - FRAME, "glitch-1", 0.32)

    # ---- S02 hook  (VO 0 - 5.90) ----------------------------------------------------------
    s = scene("s02", vt(0), vt(5.90))
    hero = still("hero", "solo-portraits/solo-portraits-04.jpg", fy=0.32, zoom=1.0)
    media_shot(s, vt(0), vt(0.70), hero, move="push", extra={"pixel": [vt(0) + 0.0, 0.5]})
    slam(vt(0.62), "PATTINSON")
    sfx(vt(0.62), "impact-bass-1", 0.5)
    pol = clip("pf_close", "PF", 4.05, 2.1, fy=0.18, aspect=1.0, size=(720, 720))
    compound(s, vt(0.70), vt(2.62), "polaroid", src=pol)
    sfx(vt(0.70), "click", 0.35)
    media_shot(s, vt(2.62), vt(2.90), clip("run_tenet", "MP", 11.80, 0.4), move="none")
    media_shot(s, vt(2.90), vt(3.13), still("run_gt", "good-time/good-time-06.jpg", fx=0.45), move="push")
    sfx(vt(2.62), "whoosh-short", 0.3)
    media_shot(s, vt(3.13), vt(3.48), clip("venice_phones", "RAW", 14.25, 0.45, fy=0.42), move="push")
    media_shot(s, vt(3.48), vt(3.84), still("redcarpet_pair", "solo-portraits/solo-portraits-08.jpg", fx=0.7, fy=0.2, zoom=1.2))
    media_shot(s, vt(3.84), vt(4.18), clip("kimmel_laugh", "KM", 37.0, 0.45, fx=0.5, zoom=1.15), move="none")
    card(s, vt(4.18), vt(5.90))
    sfx(vt(4.16), "whoosh", 0.32)

    # ---- S03 Edward + roles (VO 5.90 - 13.30) ---------------------------------------------
    s = scene("s03", vt(5.90), vt(13.30))
    media_shot(s, vt(5.90), vt(6.50), clip("fans_premiere", "ST", 20.6, 0.7, fy=0.28), look="mono")
    media_shot(s, vt(6.50), vt(6.85), clip("fans_signs", "ST", 18.8, 0.45, fy=0.0), look="mono")
    media_shot(s, vt(6.85), vt(7.75), clip("edward_stare", "TW", 71.0, 1.0, fx=0.62), move="push")
    media_shot(s, vt(7.75), vt(8.78), clip("edward_sparkle", "TW", 210.4, 1.1, fx=0.55), look="neon", move="push")
    sfx(vt(7.78), "sparkle", 0.42)
    flash(vt(8.78), 1)
    sfx(vt(8.76), "whoosh-short", 0.28)
    media_shot(s, vt(8.82), vt(9.14), clip("fm_batman", "FM", 0.6, 0.4), move="none")
    media_shot(s, vt(9.14), vt(9.40), clip("fm_dune", "FM", 3.2, 0.3), move="none")
    media_shot(s, vt(9.40), vt(9.66), clip("fm_cedric", "FM", 6.2, 0.3), move="none")
    media_shot(s, vt(9.66), vt(10.33), clip("fm_edward", "FM", 7.6, 0.75), move="push")
    media_shot(s, vt(10.33), vt(10.89), still("twi_poster", "twilight-edward-cullen/twilight-edward-cullen-11.jpg", fy=0.25), look="glitch")
    slam(vt(10.35), "TWILIGHT")
    sfx(vt(10.35), "impact-bass-1", 0.45)
    sfx(vt(10.36), "glitch-3", 0.25)
    media_shot(s, vt(10.89), vt(11.29), clip("fm_goodtime", "FM", 9.3, 0.45), move="none")
    media_shot(s, vt(11.29), vt(11.61), clip("fm_tenet", "FM", 12.0, 0.36), move="none")
    media_shot(s, vt(11.61), vt(11.96), clip("fm_lighthouse", "FM", 14.0, 0.4), look="mono", move="none")
    media_shot(s, vt(11.96), vt(12.30), clip("fm_mickey", "FM", 17.3, 0.4), move="none")
    media_shot(s, vt(12.30), vt(12.57), clip("fm_highlife", "FM", 18.6, 0.3), move="none")
    roles = [frame("r_dali", "AMC", 17.6), frame("r_louis", "AMC", 13.4), frame("r_teagardin", "AMC", 7.5),
             frame("r_heron", "AMC", 30.2), frame("r_lawrence", "AMC", 48.6), frame("r_alabaster", "AMC", 40.0),
             frame("r_rey", "AMC", 52.6), frame("r_duroy", "AMC", 63.6), frame("r_jacob", "AMC", 70.2)]
    twos(s, vt(12.57), vt(13.30), roles)

    # ---- S04 titles + swings (VO 13.30 - 22.70) -------------------------------------------
    s = scene("s04", vt(13.30), vt(22.70))
    media_shot(s, vt(13.30), vt(14.27), still("t_goodtime", "good-time/good-time-01.jpg", fx=0.55), look="neon")
    sfx(vt(13.30), "whoosh-short", 0.28)
    media_shot(s, vt(14.27), vt(15.36), still("t_lighthouse", "the-lighthouse/the-lighthouse-02.jpg", fy=0.3), look="oldfilm")
    media_shot(s, vt(15.36), vt(15.36) + 3 * FRAME, clip("t_tenet_neg", "AMC", 20.6, 0.3, vf="negate"), move="none")
    media_shot(s, vt(15.36) + 3 * FRAME, vt(16.04), clip("t_tenet", "AMC", 20.73, 0.7), move="push")
    sfx(vt(15.36), "glitch-1", 0.3)
    media_shot(s, vt(16.04), vt(16.96), still("t_batman", "the-batman/the-batman-01.jpg", fy=0.25), move="push")
    sfx(vt(16.04), "whoosh", 0.3)
    media_shot(s, vt(16.96), vt(18.36), still("t_mickey", "mickey-17/mickey-17-04.jpg", fx=0.5, fy=0.4), look="print")
    SA = dict(aspect=0.2667, size=(288, 1080))
    strips_roles = [still("st_connie", "good-time/good-time-09.jpg", fx=0.42, **SA),
                    still("st_winslow", "the-lighthouse/the-lighthouse-08.jpg", fx=0.5, **SA),
                    frame("st_neil", "FM", 12.4, fx=0.48, **SA),
                    still("st_bat", "the-batman/the-batman-02.jpg", fx=0.36, **SA),
                    still("st_mickey", "mickey-17/mickey-17-01.jpg", fx=0.5, **SA)]
    compound(s, vt(18.36), vt(19.40), "strips", srcs=strips_roles, look="base")
    sfx(vt(18.36), "whoosh", 0.3)
    media_shot(s, vt(19.40), vt(19.70), clip("sw_dali", "AMC", 17.2, 0.35), move="none")
    weird = [(frame("w_heron", "AMC", 31.0), "glitch"), frame("w_soot", "SF", 21.0),
             frame("w_helmet", "SF", 19.9), still("w_bleach", "good-time/good-time-04.jpg", fx=0.3),
             (frame("w_king", "AMC", 14.2), "glitch"), frame("w_preacher", "AMC", 9.0)]
    twos(s, vt(19.70), vt(20.20), weird)
    sfx(vt(19.70), "glitch-3", 0.25)
    media_shot(s, vt(20.20), vt(20.51), clip("sw_king", "AMC", 12.5, 0.35), move="none")
    media_shot(s, vt(20.51), vt(20.86), clip("sw_highlife", "SF", 19.4, 0.4), move="none")
    media_shot(s, vt(20.86), vt(21.64), clip("sw_lawrence", "AMC", 48.0, 0.85), move="push")
    media_shot(s, vt(21.64), vt(22.20), clip("sw_heron", "AMC", 29.4, 0.6), move="none")
    media_shot(s, vt(22.20), vt(22.70), clip("km_grin", "KM", 39.0, 0.55, zoom=1.2), move="push")

    # ---- S05 internet jokes + receipt 1 (VO 22.70 - 24.92, spider monkey) ------------------
    s = scene("s05", vt(22.70), INS_T[0] + INS[0])
    cards = [frame("meme_sleep", "CB", 0.45, size=(720, 540)), frame("meme_sparkle", "TW", 207.0, fx=0.5, size=(720, 540)),
             frame("meme_tree", "TW", 398.9, fx=0.45, size=(720, 540)), frame("meme_notatall", "CB", 5.0, size=(720, 540))]
    compound(s, vt(22.70), ve(24.92), "memes", bg=clip("meme_bg", "TW", 74.0, 2.35, fx=0.6), look="vhs",
             cards=cards, times=[vt(23.33), vt(23.71), vt(23.97), vt(24.17)])
    for t in (23.33, 23.71, 23.97, 24.17):
        sfx(vt(t), "pop", 0.22)
    media_shot(s, INS_T[0], INS_T[0] + INS[0], clip("spider", "TW", 398.45, INS[0] + 0.1, fx=0.42), move="push")
    sfx(INS_T[0] + INS[0] - FRAME, "whoosh-short", 0.3)

    # ---- S06 directors + Batman + receipt 2 (VO 24.92 - 30.40, Kimmel) ---------------------
    s = scene("s06", vt(24.92), INS_T[1] + INS[1])
    media_shot(s, vt(24.92), vt(25.70), still("bw_set1", "Pattison as Bruce wayne photo 1.jpg", fy=0.3, zoom=1.15), look="halftone")
    media_shot(s, vt(25.70), vt(26.10), still("bw_set3", "Pattison as Bruce wayne photo 3.jpg", fy=0.45, zoom=1.1), look="mono")
    media_shot(s, vt(26.10), vt(26.50), still("bw_set6", "Pattison as Bruce wayne photo 6.jpg", fy=0.6), look="mono")
    TOP = dict(area=(0, 0, 1080, 880), fy=0.0)          # above the burned red names
    media_shot(s, vt(26.50), vt(26.75), clip("d_nolan", "ST", 83.30, 0.32, **TOP), look="mono", move="none")
    media_shot(s, vt(26.75), vt(27.00), clip("d_reeves", "ST", 83.95, 0.32, **TOP), look="mono", move="none")
    media_shot(s, vt(27.00), vt(27.25), clip("d_bong", "ST", 84.55, 0.32, **TOP), look="mono", move="none")
    media_shot(s, vt(27.25), vt(27.50), clip("d_denis", "ST", 85.15, 0.32, **TOP), look="mono", move="none")
    sfx(vt(26.50), "whoosh", 0.3)
    media_shot(s, vt(27.50), vt(28.05), still("nolan_imax", "the-odyssey-antinous/the-odyssey-antinous-47.jpg", fx=0.0, fy=0.4, zoom=1.6), look="mono")
    card(s, vt(28.05), vt(28.62))
    media_shot(s, vt(28.62), vt(29.25), still("bat_light", "the-batman/the-batman-11.jpg", fy=0.4), move="push")
    media_shot(s, vt(29.25), vt(29.78), clip("bat_mask", "MB", 21.5, 0.6), move="push")
    media_shot(s, vt(29.78), ve(30.40), clip("bat_fire", "MB", 24.70, 0.7), move="push")
    slam(vt(29.80), "BATMAN")
    sfx(vt(29.80), "impact-bass-2", 0.55)
    sfx(vt(29.80) - 10.03 + 0.12, "riser", 0.3)
    k0 = INS_T[1]
    media_shot(s, k0, k0 + 2.68, clip("km_intro", "KM", 0.0, 2.75), move="push")
    media_shot(s, k0 + 2.68, k0 + INS[1], clip("km_wave", "KM", 19.05, 1.05, zoom=1.1), move="none")
    sfx(k0 + INS[1] - FRAME, "whoosh-short", 0.28)

    # ---- S07 respect + this year + Odyssey (VO 30.40 - 41.80) -----------------------------
    s = scene("s07", vt(30.40), vt(41.85))
    media_shot(s, vt(30.40), vt(31.30), still("young_rob", "pat image 5.jpg", fy=0.3), look="halftone")
    media_shot(s, vt(31.30), vt(31.72), clip("laugh_stare", "TW", 74.5, 0.5, fx=0.6), look="vhs", move="none")
    media_shot(s, vt(31.72), vt(32.10), clip("laugh_van", "MP", 33.10, 0.45), look="vhs", move="none")
    media_shot(s, vt(32.10), vt(32.62), still("laugh_cast", "twilight-edward-cullen/twilight-edward-cullen-07.jpg", fx=0.6), look="halftone")
    media_shot(s, vt(32.62), vt(33.50), clip("venice_arrive", "RAW", 14.6, 0.95, fy=0.45), move="push")
    media_shot(s, vt(33.50), vt(34.38), still("respect_portrait", "solo-portraits/solo-portraits-06.jpg", fy=0.2, zoom=1.3), move="push")
    media_shot(s, vt(34.38), vt(35.55), clip("drama_carpet", "NCW", 6.2, 1.25, fy=0.3), move="push")
    card(s, vt(35.55), vt(36.62))
    compound(s, vt(36.03), vt(36.62), "poster", src=still("slate_2026", "Instagram photo (eatmovies).jpg", aspect=1350 / 1688, size=(760, 950)))
    sfx(vt(36.03), "whoosh", 0.3)
    media_shot(s, vt(36.62), vt(37.15), clip("ody_arch", "SF", 5.9, 0.6), move="push")
    media_shot(s, vt(37.15), vt(38.18), clip("nolan_set", "ST", 66.0, 1.1, fy=0.2), look="mono", move="push")
    media_shot(s, vt(38.18), vt(38.85), still("ody_poster", "the-odyssey-antinous/the-odyssey-antinous-11.jpg", fy=0.35), move="push")
    slam(vt(38.55), "ODYSSEY")
    sfx(vt(38.55), "impact-bass-1", 0.5)
    media_shot(s, vt(38.85), vt(39.60), clip("antinous_laugh", "SF", 4.92, 0.8), move="push")
    media_shot(s, vt(39.60), vt(40.40), clip("antinous_feast", "GM", 8.5, 0.85), move="push")
    media_shot(s, vt(40.40), vt(41.45), clip("antinous_feast2", "SF", 8.0, 1.1), move="push")
    media_shot(s, vt(41.45), vt(41.85), clip("antinous_red", "SF", 5.10, 0.45), look="red", move="none")
    sfx(vt(41.47), "glitch-2", 0.3)

    # ---- S08 Primetime + receipt 3 (VO 41.80 - 48.25, Chris Hansen) -----------------------
    s = scene("s08", vt(41.85), INS_T[2] + INS[2])
    media_shot(s, vt(41.85), vt(42.80), clip("pt_title", "PT", 30.75, 1.0, fy=0.5), move="push")
    sfx(vt(41.87), "glitch-3", 0.28)
    media_shot(s, vt(42.80), vt(43.90), clip("pt_suit", "PM2", 6.3, 1.15), move="push")
    media_shot(s, vt(43.90), vt(44.52), clip("pt_board", "PM2", 12.0, 0.65), move="none")
    media_shot(s, vt(44.52), vt(45.15), clip("pt_board2", "PM2", 12.62, 0.65), move="push")
    media_shot(s, vt(45.15), vt(45.98), clip("pt_crew", "PM2", 5.2, 0.85), move="push")
    media_shot(s, vt(45.98), vt(46.70), clip("pt_chat", "PM2", 10.06, 0.62), move="push")
    media_shot(s, vt(46.70), vt(47.15), clip("pt_cam", "PM2", 13.9, 0.5), move="none")
    media_shot(s, vt(47.15), vt(47.60), clip("pt_kitchen", "PM2", 3.4, 0.5), move="none")
    media_shot(s, vt(47.60), ve(48.25), clip("pt_run", "PT", 15.5, 0.55, fy=0.5), move="none")
    sfx(vt(47.60), "whoosh-short", 0.28)
    h0 = INS_T[2]
    media_shot(s, h0, h0 + INS[2], clip("hansen", "PM2", 0.50, 1.55), move="push")

    # ---- S09 Dune + thesis + close + sting (VO 48.25 - end) -------------------------------
    s = scene("s09", vt(48.25), TOTAL)
    media_shot(s, vt(48.25), vt(49.36), clip("dune_desert", "GM", 12.3, 1.05), move="push")
    media_shot(s, vt(49.36), vt(49.95), clip("dune_robe", "GM", 13.4, 0.62), move="none")
    media_shot(s, vt(49.95), vt(50.55), still("dune_still", "dune/dune-52.jpg", fx=0.5), move="push")
    media_shot(s, vt(50.55), vt(51.32), still("dune_poster", "dune/dune-11.jpg", fy=0.35), move="push")
    slam(vt(50.73), "DUNE")
    sfx(vt(50.73), "impact-bass-2", 0.5)
    media_shot(s, vt(51.32), vt(52.20), clip("talk_posters", "GM", 0.4, 0.95), move="push")
    choose = [frame("c1", "FM", 0.5), frame("c2", "FM", 3.5), frame("c3", "FM", 6.5), frame("c4", "FM", 9.9),
              frame("c5", "FM", 12.8), (frame("c6", "FM", 14.6), "mono"), frame("c7", "FM", 17.6),
              frame("c8", "FM", 19.0), frame("c9", "FM", 20.3), frame("c10", "AMC", 3.0)]
    twos(s, vt(52.20), vt(53.06), choose)
    media_shot(s, vt(53.06), vt(53.55), clip("stop_fight", "MP", 18.70, 0.5), move="none")
    media_shot(s, vt(53.55), vt(54.10), clip("stop_boom", "CB", 11.62, 0.6), move="none")
    grid = [frame("g1", "FM", 9.5), frame("g2", "AMC", 26.5), (frame("g3", "FM", 14.2), "mono"),
            frame("g4", "FM", 12.3), frame("g5", "MB", 23.5), frame("g6", "FM", 17.4),
            frame("g7", "GM", 12.6), frame("g8", "SF", 5.3), frame("g9", "PM2", 6.6)]
    compound(s, vt(54.10), vt(55.24) + 2 * FRAME, "grid", srcs=grid, look="base", flash_t=vt(55.24))
    card(s, vt(55.24) + 2 * FRAME, vt(55.58), glow=False)
    sfx(vt(55.24) - 5.54 + 0.25, "whoosh-cinematic", 0.22)
    sfx(vt(55.24), "impact-bass-1", 0.5)
    media_shot(s, vt(55.58), vt(56.15), clip("close_edward", "TW", 70.6, 0.6, fx=0.6), look="vhs", move="push")
    compound(s, vt(56.15), vt(56.74), "split",
             left=clip("split_edward", "TW", 70.7, 0.65, fx=0.62, aspect=0.6667, size=(720, 1080)),
             right=clip("split_batman", "CB", 9.5, 0.65, aspect=0.6667, size=(720, 1080)))
    sfx(vt(56.15), "whoosh", 0.3)
    rein = [frame("re1", "AMC", 3.8), frame("re2", "AMC", 21.5), frame("re3", "AMC", 15.5), frame("re4", "MP", 0.3),
            frame("re5", "AMC", 58.5), frame("re6", "GM", 13.8), (frame("re7", "AMC", 44.0), "mono"),
            frame("re8", "SF", 15.0), frame("re9", "PM2", 7.5), frame("re10", "MB", 31.5)]
    twos(s, vt(56.74), vt(57.58), rein)
    media_shot(s, vt(57.58), vt(58.28), clip("venice_boat", "RAW", 2.0, 0.75, fy=0.5), move="push")
    media_shot(s, vt(58.28), STING_T, hero, move="slowpush")
    card(s, STING_T, TOTAL, glow=False)
    FX.append(dict(type="sting", t0=STING_T, t1=TOTAL))
    sfx(STING_T, "impact-bass-2", 0.4)
    sfx(STING_T - 0.6, "whoosh-cinematic", 0.2)


# --------------------------------------------------------------------------------------------
# Captions
# --------------------------------------------------------------------------------------------
# VO caption groups, in script order. *word* = bold grotesk, plain = serif italic.
# "L | R" = flank layout (words left and right of a centred object). Options per group.
PHRASES = [
    ("Robert *Pattinson*", {"until": 0.70}), ("is having a | *generational*", {"flank": "pol"}), ("run,", {}), ("and honestly", {}),
    ("nobody saw it *coming.*", {}),
    ("To some *people,*", {}), ("he’ll always be", {}), ("*Edward* *Cullen.*", {}),
    ("But *everything*", {}), ("he did after *Twilight*", {}), ("proved he was", {}), ("never *stuck*", {}),
    ("with one *role.*", {}),
    ("Good *Time.*", {"size": 1.55}), ("The *Lighthouse.*", {"size": 1.55, "dark": True}), ("*Tenet.*", {"size": 1.55}),
    ("The *Batman.*", {"size": 1.55}), ("*Mickey* *17.*", {"size": 1.55}),
    ("*Every* one of them", {}), ("was a *weird,*", {}), ("*bold* *swing*", {}), ("nobody *expected*", {}),
    ("from him.", {}), ("And while the *internet*", {}), ("kept making", {}), ("*Twilight* *jokes,*", {}),
    ("he was *quietly*", {}), ("working with the", {}), ("best *directors*", {}), ("*alive,*", {}),
    ("until one day", {}), ("he became", {}), ("*Batman.*", {"dark": True}),
    ("The *vampire* kid", {}), ("everyone *laughed* at", {}), ("is now one of the", {}), ("most *respected*", {}),
    ("actors in *Hollywood.*", {}), ("And this | *year?*", {"flank": "poster"}),
    ("He walked into", {}), ("Christopher *Nolan’s*", {}), ("The *Odyssey*", {}), ("as *Antinous,*", {}),
    ("one of the story’s", {}), ("central *antagonists.*", {}),
    ("Then came *Primetime,*", {}), ("with *Pattinson* playing", {}), ("a *television* *journalist*", {}),
    ("at the center of", {}), ("controversial *predator*", {"y": 0.30}), ("*sting* operations.", {}),
    ("And now he’s", {"dark": True}), ("*closing* out the year", {}), ("with *Dune.*", {}),
    ("*Pattinson* keeps", {}), ("choosing *roles*", {}), ("that *stop* anyone", {}), ("from putting him", {}),
    ("in one *box.*", {}), ("And that", {}), ("*post-Twilight*", {}), ("*reinvention*", {}),
    ("might be one of the", {}), ("*best* we’ve ever seen.", {"hold": True}),
]
# Receipts (original voices). (origin T, [(word, style, dt)], end dt, options); B = big bold.
RECEIPTS = [
    (0.0, [("Somebody", "b", 0.17)], 0.50, {"y": 0.49, "size": 1.7, "nodark": True}),
    (0.0, [("get", "b", 0.50), ("these", "b", 0.62)], 1.00, {"y": 0.49, "size": 1.7, "nodark": True}),
    (0.0, [("beggars", "B", 1.00)], 1.33, {"y": 0.49, "size": 1.5, "nodark": True}),
    (0.0, [("out", "b", 1.33), ("of", "b", 1.45), ("here!", "b", 1.58)], 2.30, {"y": 0.49, "size": 1.7, "nodark": True}),
    (3.0833, [("Somebody", "i", 0.08), ("get", "i", 0.40), ("these", "i", 0.57)], 0.74, {"y": 0.50, "size": 1.3}),
    (3.0833, [("beggars", "B", 0.74)], 1.24, {"y": 0.50, "size": 1.5}),
    (3.0833, [("out", "i", 1.24), ("of", "i", 1.40), ("here!", "i", 1.57)], 2.70, {"y": 0.50, "size": 1.3}),
    (INS_T[0], [("You", "i", 0.20), ("better", "i", 0.35), ("hold", "b", 0.70), ("on", "i", 0.92), ("tight,", "b", 1.05)], 1.45, {}),
    (INS_T[0], [("spider", "b", 1.45), ("monkey.", "b", 1.85)], INS[0], {}),
    (INS_T[1], [("Our", "i", 0.05), ("first", "i", 0.24), ("guest", "i", 0.54), ("tonight", "i", 0.88)], 1.36, {}),
    (INS_T[1], [("is", "i", 1.36), ("Batman,", "B", 1.67)], 2.70, {}),
    (INS_T[1], [("and", "i", 2.70), ("the", "i", 2.88), ("vampire", "b", 3.06)], INS[1], {}),
    (INS_T[2], [("I’m", "i", 0.55), ("Chris", "b", 0.77), ("Hansen.", "b", 1.04)], INS[2], {"y": 0.80}),
]


def caption_groups():
    """Match PHRASES to the VO words (by position), map to output time, add receipts."""
    groups = []
    wi = 0
    for spec, opt in PHRASES:
        parts = spec.split(" | ")
        ws = []
        left = None
        for pi, part in enumerate(parts):
            for tok in part.split():
                bold = tok.startswith("*") and tok.endswith("*")
                text = tok.strip("*")
                w = WORDS[wi]
                assert w["w"] == text, f"phrase word {text!r} != VO word {w['w']!r} at {wi}"
                ws.append(dict(text=text, style="b" if bold else "i", t=fr(vt(w["s"]))))
                wi += 1
            if pi == 0 and len(parts) > 1:
                left = len(ws)
        groups.append(dict(words=ws, opt=opt, left=left, t0=ws[0]["t"]))
    assert wi == len(WORDS), f"phrases cover {wi} of {len(WORDS)} VO words"
    for i, g in enumerate(groups):
        g["t1"] = groups[i + 1]["t0"] if i + 1 < len(groups) else fr(STING_T)
        for ins_t in INS_T:                      # a receipt takes over at each VO split
            if g["t0"] < ins_t < g["t1"]:
                g["t1"] = fr(ins_t)
        if g["opt"].get("hold"):
            g["t1"] = fr(STING_T)
        if g["opt"].get("until") is not None:
            g["t1"] = min(g["t1"], fr(vt(g["opt"]["until"])))
    for origin, ws, end, opt in RECEIPTS:
        words_ = [dict(text=w, style=s, t=fr(origin + dt)) for w, s, dt in ws]
        groups.append(dict(words=words_, opt=opt, left=None, t0=words_[0]["t"], t1=fr(origin + end)))
    groups.sort(key=lambda g: g["t0"])
    return groups


# --------------------------------------------------------------------------------------------
# HTML writers
# --------------------------------------------------------------------------------------------
FONT_FACE = """
@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;src:url("assets/fonts/InstrumentSerif-Italic.ttf") format("truetype");}
@font-face{font-family:"Instrument Serif";font-style:normal;font-weight:400;src:url("assets/fonts/InstrumentSerif-Regular.ttf") format("truetype");}
@font-face{font-family:"Inter Tight";font-style:normal;font-weight:100 900;src:url("assets/fonts/InterTight[wght].ttf") format("truetype");}
"""
GLOW = "0 0 2px rgba(255,255,255,0.95), 0 0 9px rgba(255,255,255,0.55), 0 0 26px rgba(255,255,255,0.32), 0 0 64px rgba(255,255,255,0.18)"
GLOW_BOOST = "0 0 4px rgba(255,255,255,1), 0 0 20px rgba(255,255,255,0.95), 0 0 52px rgba(255,255,255,0.75), 0 0 120px rgba(255,255,255,0.5)"
DGLOW = "0 0 2px rgba(255,255,255,0.9), 0 0 10px rgba(255,255,255,0.75), 0 0 28px rgba(255,255,255,0.5), 0 0 64px rgba(255,255,255,0.3)"


# --------------------------------------------------------------------------------------------
# Baking: every graded media element is rendered once through HyperFrames' own media-treatment
# shader (CPU-only here, ~1.5 s/frame live) and the film then plays the baked files.
# --------------------------------------------------------------------------------------------
BAKE = {}          # hash -> request
NORM = {}


def norm_look(name):
    """Normalise a look once through the CLI (same validation as --apply)."""
    if name in NORM:
        return NORM[name]
    d = os.path.join(ROOT, "work", "looks", "norm", name)
    os.makedirs(d, exist_ok=True)
    jf = os.path.join(ROOT, "work", "looks", f"{name}.json")
    os.makedirs(os.path.dirname(jf), exist_ok=True)
    json.dump(LOOKS[name], open(jf, "w"))
    cache = os.path.join(d, "norm.json")
    if os.path.exists(cache) and json.load(open(cache)).get("_src") == LOOKS[name]:
        NORM[name] = json.load(open(cache))["g"]
        return NORM[name]
    open(os.path.join(d, "index.html"), "w").write(
        '<!doctype html><html><body><div id="root" data-composition-id="main" data-start="0" data-duration="1" '
        'data-width="10" data-height="10"><img id="a" class="clip" data-start="0" data-duration="1" src="x.jpg"></div>'
        '<script>window.__timelines={};window.__timelines["main"]=gsap.timeline({paused:true});</script></body></html>')
    r = subprocess.run(["npx", "hyperframes", "media-treatment", "--project", d, "--file", "index.html", "--selector", "#a",
                        "--grading", jf, "--apply", "--json"], cwd=ROOT, capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert out.get("ok"), out
    g = out["after"]
    json.dump({"_src": LOOKS[name], "g": g}, open(cache, "w"))
    NORM[name] = g
    return g


def baked(src, look, kind, w, h, dur=None, pixel=False):
    """Register a bake request; return the baked asset path (img -> .jpg, video/pixel -> .mp4)."""
    side = os.path.join(ROOT, src + ".json")
    stamp = open(side).read() if os.path.exists(side) else src
    nframes = int(round((dur or 0) * FPS)) + (1 if kind != "img" or pixel else 0)
    key = json.dumps(dict(src=src, stamp=stamp, look=LOOKS.get(look), kind=kind, w=w, h=h, n=nframes, pixel=pixel), sort_keys=True)
    hsh = hashlib.sha1(key.encode()).hexdigest()[:12]
    ext = "jpg" if (kind == "img" and not pixel) else "mp4"
    path = f"assets/baked/{hsh}.{ext}"
    BAKE[hsh] = dict(src=src, look=look, kind="pixel" if pixel else kind, w=w, h=h, n=max(1, nframes), out=path)
    return path


def _img_size(src):
    return Image.open(os.path.join(ROOT, src)).size


def bake_all(max_parallel=2):
    os.makedirs(os.path.join(ROOT, "assets", "baked"), exist_ok=True)
    todo = [dict(r, hash=k) for k, r in BAKE.items() if not os.path.exists(os.path.join(ROOT, r["out"]))]
    print(f"bake: {len(BAKE)} baked media, {len(todo)} to render")
    if not todo:
        return
    groups = {}
    for r in todo:
        k = ("img" if r["kind"] == "img" else "vid", r["w"], r["h"])
        groups.setdefault(k, []).append(r)
    batches = []
    for (kind, w, h), items in groups.items():
        if kind == "img":
            for i in range(0, len(items), 40):
                batches.append((kind, w, h, items[i:i + 40]))
        else:
            items.sort(key=lambda r: -r["n"])
            nb = max(1, min(max_parallel + 1, sum(r["n"] for r in items) // 240 + 1))
            bins = [[] for _ in range(nb)]
            for r in items:
                min(bins, key=lambda b: sum(x["n"] for x in b)).append(r)
            for b in bins:
                if b:
                    batches.append((kind, w, h, b))
    procs = []
    for bi, (kind, w, h, items) in enumerate(batches):
        bdir = os.path.join(ROOT, "work", "bk", f"b{bi:02d}")
        os.makedirs(bdir, exist_ok=True)
        link = os.path.join(bdir, "assets")
        if not os.path.islink(link):
            os.symlink(os.path.join(ROOT, "assets"), link)
        els, js, t = [], [], 0
        for j, r in enumerate(items):
            g = html.escape(json.dumps(norm_look(r["look"])), quote=True)
            a = t / FPS
            d = r["n"] / FPS
            r["frame0"] = t
            if r["kind"] == "video":
                els.append(f'<video id="b{j}" class="clip m" data-start="{a:.5f}" data-duration="{d:.5f}" data-media-start="0" '
                           f'data-track-index="1" src="{r["src"]}" muted playsinline data-color-grading="{g}"></video>')
            else:
                st = ' style="--hf-color-grading-pixelate: 0.85"' if r["kind"] == "pixel" else ""
                els.append(f'<img id="b{j}" class="clip m" data-start="{a:.5f}" data-duration="{d:.5f}" data-track-index="1" '
                           f'src="{r["src"]}" alt="" data-color-grading="{g}"{st}>')
                if r["kind"] == "pixel":
                    js.append(f'tl.fromTo("#b{j}",{{"--hf-color-grading-pixelate":0.85}},{{"--hf-color-grading-pixelate":0,duration:0.5,ease:"steps(6)"}},{a:.5f});')
            t += r["n"]
        open(os.path.join(bdir, "index.html"), "w").write(f"""<!doctype html><html lang="en"><head><meta charset="UTF-8">
<script src="assets/vendor/gsap.min.js"></script>
<style>*{{margin:0;padding:0}} html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#000}}
.m{{position:absolute;left:0;top:0;width:{w}px;height:{h}px;object-fit:cover}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{t / FPS:.5f}" data-width="{w}" data-height="{h}" data-fps="{FPS}">
{chr(10).join(els)}
</div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});{"".join(js)}window.__timelines["main"]=tl;</script></body></html>""")
        batches[bi] = (kind, w, h, items, bdir)
    # render with a small worker pool
    queue = list(range(len(batches)))
    running = []
    while queue or running:
        while queue and len(running) < max_parallel:
            bi = queue.pop(0)
            bdir = batches[bi][4]
            log = open(bdir + ".log", "w")
            pr = subprocess.Popen(["npx", "hyperframes", "render", bdir, "--fps", str(FPS), "--quality", "high",
                                   "--workers", "1", "-o", bdir + ".mp4"], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
            running.append((bi, pr))
            print(f"  bake batch b{bi:02d}: {len(batches[bi][3])} items, {sum(r['n'] for r in batches[bi][3])} frames ({batches[bi][1]}x{batches[bi][2]})", flush=True)
        for bi, pr in list(running):
            if pr.poll() is not None:
                running.remove((bi, pr))
                assert pr.returncode == 0, f"bake batch b{bi:02d} failed, see {batches[bi][4]}.log"
                _split(batches[bi])
        if running:
            import time
            time.sleep(2)


def _split(batch):
    kind, w, h, items, bdir = batch
    src = bdir + ".mp4"
    for r in items:
        out = os.path.join(ROOT, r["out"])
        if r["kind"] == "img":
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"select=eq(n\\,{r['frame0']})", "-frames:v", "1",
                            "-q:v", "2", out], check=True)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"select=between(n\\,{r['frame0']}\\,{r['frame0'] + r['n'] - 1}),setpts=N/{FPS}/TB",
                            "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-g", "12", "-pix_fmt", "yuv420p", out], check=True)
    print(f"  split {os.path.basename(bdir)} -> {len(items)} baked files", flush=True)


def scene_html(sc):
    """Media elements carry their own timing; moving wrappers are untimed and shown/hidden explicitly."""
    sid = sc["id"]
    t0 = sc["t0"]
    els = []
    js = []
    n = 0

    def timed(tag, eid, a, d, cls, z, inner="", attrs="", track=1):
        return (f'<{tag} id="{eid}" class="clip {cls}" data-start="{t0s(a)}" data-duration="{tds(a, d)}" '
                f'data-track-index="{track}" style="z-index:{z}" {attrs}>{inner}</{tag}>')

    def media(tag, eid, a, d, src, look, z=None, style="", track=2, pixel=False):
        if tag == "img" and not pixel:
            w, h = _img_size(src)
            out = baked(src, look, "img", w, h)
        elif pixel:
            w, h = _img_size(src)
            out = baked(src, look, "img", 1440, 1080, dur=d, pixel=True)
            tag = "video"
        else:
            vw, vh = dims(os.path.join(ROOT, src))
            out = baked(src, look, "video", vw, vh, dur=d)
        mattr = 'muted playsinline' if tag == "video" else 'alt=""'
        return (f'<{tag} id="{eid}" class="clip m" data-start="{t0s(a)}" data-duration="{tds(a, d)}" data-track-index="{track}" '
                f'src="{out}" data-look="{look}" {mattr}></{tag}>')

    def show_window(sel, a, d):
        js.append(f'tl.set("{sel}",{{opacity:1}},{a:.4f});')
        js.append(f'tl.set("{sel}",{{opacity:0}},{a + d:.4f});')

    for it in sc["items"]:
        n += 1
        eid = f"{sid}-{n:03d}"
        a = it["t0"] - t0
        d = it["t1"] - it["t0"]
        if d <= 0:
            continue
        z = it["z"] * 1000 + n * 6
        if it["type"] == "shot":
            tag = "video" if it["kind"] == "video" else "img"
            els.append(f'<div class="kb" id="{eid}-kb" style="z-index:{z}">'
                       + media(tag, f"{eid}-m", a, d, it["src"], it["look"], track=1 + n % 3, pixel=bool(it["extra"].get("pixel"))) + '</div>')
            mv = it["move"]
            if mv == "push":
                js.append(f'tl.fromTo("#{eid}-kb",{{scale:1.0}},{{scale:1.07,duration:{d:.4f},ease:"power1.inOut"}},{a:.4f});')
            elif mv == "slowpush":
                js.append(f'tl.fromTo("#{eid}-kb",{{scale:1.0}},{{scale:1.09,duration:{d:.4f},ease:"power1.out"}},{a:.4f});')
        elif it["type"] == "card":
            glow = '<div class="glow"></div>' if it["glow"] else ""
            els.append(timed("div", eid, a, d, "card", z, glow))
        elif it["type"] == "polaroid":
            els.append(timed("div", f"{eid}-bg", a, d, "card", z, '<div class="glow"></div>'))
            els.append(f'<div class="pol-wrap" id="{eid}-pw" style="z-index:{z + 1}">'
                       + timed("div", f"{eid}-frame", a, d, "pol-frame", 1)
                       + media("video", f"{eid}-m", a, d, it["src"], "base") + '</div>')
            js.append(f'tl.fromTo("#{eid}-pw",{{scale:0.94,rotation:-3}},{{scale:1.04,rotation:-2,duration:{d:.4f},ease:"power1.out"}},{a:.4f});')
        elif it["type"] == "poster":
            els.append(timed("div", f"{eid}-bg", a, d, "card", z, '<div class="glow"></div>'))
            els.append(f'<div class="poster" id="{eid}-pw" style="z-index:{z + 1}">'
                       + media("img", f"{eid}-m", a, d, it["src"], "print") + '</div>')
            js.append(f'tl.fromTo("#{eid}-pw",{{scale:1.08}},{{scale:1.0,duration:0.25,ease:"expo.out"}},{a:.4f});')
        elif it["type"] == "strips":
            k = len(it["srcs"])
            els.append(timed("div", f"{eid}-bg", a, d, "card", z))
            for i, sp in enumerate(it["srcs"]):
                look = it["look"]
                if isinstance(sp, tuple):
                    sp, look = sp
                els.append(f'<div class="strip" id="{eid}-s{i}" style="left:{i * W / k:.1f}px;width:{W / k - 4:.1f}px;z-index:{z + 1}">'
                           + media("img", f"{eid}-m{i}", a, d, sp, look) + '</div>')
                js.append(f'tl.fromTo("#{eid}-s{i}",{{xPercent:{110 + 25 * (k - i)},opacity:1}},{{xPercent:0,opacity:1,duration:0.25,ease:"expo.out",immediateRender:false}},{a + i * 2 * FRAME:.4f});')
                js.append(f'tl.set("#{eid}-s{i}",{{opacity:0}},{a + d:.4f});')
        elif it["type"] == "grid":
            order = [4, 0, 8, 2, 6, 1, 7, 3, 5]
            els.append(timed("div", f"{eid}-bg", a, d, "card", z))
            for i, sp in enumerate(it["srcs"]):
                look = it["look"]
                if isinstance(sp, tuple):
                    sp, look = sp
                r, c = divmod(i, 3)
                els.append(f'<div class="tile" id="{eid}-t{i}" style="left:{c * W / 3 + 3:.1f}px;top:{r * H / 3 + 3:.1f}px;width:{W / 3 - 6:.1f}px;height:{H / 3 - 6:.1f}px;z-index:{z + 1}">'
                           + media("img", f"{eid}-m{i}", a, d, sp, look) + f'<div class="tflash" id="{eid}-f{i}"></div></div>')
            for j, i in enumerate(order):
                tt = a + j * 2 * FRAME
                js.append(f'tl.set("#{eid}-t{i}",{{opacity:1}},{tt:.4f});')
                js.append(f'tl.fromTo("#{eid}-f{i}",{{opacity:0.95}},{{opacity:0,duration:0.12,ease:"power2.out",immediateRender:false}},{tt:.4f});')
                js.append(f'tl.set("#{eid}-t{i}",{{opacity:0}},{a + d:.4f});')
            ft = it["flash_t"] - t0
            els.append(timed("div", f"{eid}-white", ft, 2 * FRAME, "whiteout", z + 5))
        elif it["type"] == "memes":
            els.append(f'<div class="kb" id="{eid}-kb" style="z-index:{z}">' + media("video", f"{eid}-m", a, d, it["bg"], it["look"]) + '</div>')
            js.append(f'tl.fromTo("#{eid}-kb",{{scale:1.0}},{{scale:1.08,duration:{d:.4f},ease:"power1.inOut"}},{a:.4f});')
            pos = [(-470, -250, -6), (430, -230, 5), (-440, 260, 4), (450, 240, -5)]
            for i, sp in enumerate(it["cards"]):
                x, y, r = pos[i]
                tt = it["times"][i] - t0
                els.append(f'<div class="meme" id="{eid}-c{i}" style="left:{W / 2 + x - 180}px;top:{H / 2 + y - 135}px;z-index:{z + 2 + i}">'
                           + media("img", f"{eid}-m{i}", tt, a + d - tt, sp, "base") + '</div>')
                js.append(f'tl.fromTo("#{eid}-c{i}",{{opacity:0,scale:0.6,rotation:{r * 2}}},{{opacity:1,scale:1,rotation:{r},duration:0.18,ease:"back.out(1.6)",immediateRender:false}},{tt:.4f});')
                js.append(f'tl.set("#{eid}-c{i}",{{opacity:0}},{a + d:.4f});')
        elif it["type"] == "split":
            els.append(f'<div class="half" style="left:0;z-index:{z}">' + media("video", f"{eid}-l", a, d, it["left"], "vhs") + '</div>')
            els.append(f'<div class="half" style="left:{W // 2 + 4}px;z-index:{z}">' + media("video", f"{eid}-r", a, d, it["right"], "base") + '</div>')
    css = f"""
#root{{position:absolute;inset:0;overflow:hidden;background:#000}}
.shot{{position:absolute;inset:0;overflow:hidden;background:#000}}
.kb{{position:absolute;inset:0;transform-origin:50% 50%}}
.kb .m{{position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover}}
.card{{position:absolute;inset:0;background:#000}}
.card .glow{{z-index:1}}
.glow{{position:absolute;inset:0;background:radial-gradient(ellipse 46% 40% at 50% 48%, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.06) 42%, rgba(0,0,0,0) 74%)}}
.pol-wrap{{position:absolute;left:{W / 2 - 230}px;top:{H / 2 - 270}px;width:460px;height:540px;transform-origin:50% 50%}}
.pol-frame{{position:absolute;inset:0;background:#f4f1ea;box-shadow:0 30px 80px rgba(0,0,0,0.7)}}
.pol-wrap .m{{position:absolute;left:20px;top:20px;width:420px;height:420px;object-fit:cover;z-index:2}}
.poster{{position:absolute;left:{(W - 760) / 2}px;top:{(H - 950) / 2}px;width:760px;height:950px;transform-origin:50% 50%}}
.poster .m{{position:absolute;left:0;top:0;width:760px;height:950px;object-fit:cover}}
.strip{{position:absolute;top:0;height:{H}px;overflow:hidden;opacity:0}}
.strip .m{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.tile{{position:absolute;overflow:hidden;opacity:0}}
.tile .m{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.tflash{{position:absolute;inset:0;background:#fff;opacity:0}}
.whiteout{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,#fff 0%,#fff 55%,#e9e9e9 100%)}}
.meme{{position:absolute;width:360px;height:270px;border:6px solid #f2f2f2;box-shadow:0 20px 50px rgba(0,0,0,0.6);opacity:0}}
.meme .m{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.half{{position:absolute;top:0;width:{W // 2 - 4}px;height:{H}px;overflow:hidden}}
.half .m{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
"""
    body = "\n    ".join(els)
    script = "\n    ".join(js)
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {script}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


def captions_html(groups):
    els = []
    js = []
    for gi, g in enumerate(groups):
        gid = f"cap-{gi:03d}"
        opt = g["opt"]
        size = opt.get("size", 1.0)
        y = opt.get("y", 0.47)
        cls = "cg" + (" dark" if (opt.get("dark") or g.get("auto_dark")) else "")
        spans = []
        for wi, w in enumerate(g["words"]):
            st = w["style"]
            c = {"i": "i", "b": "b", "B": "b big", "I": "i big"}[st]  # noqa: E501
            spans.append(f'<span class="w {c}" id="{gid}-w{wi}">{html.escape(w["text"])}</span>')
            wt = w["t"] - 0.0
            shadow = DGLOW if (opt.get("dark") or g.get("auto_dark")) else GLOW
            js.append(f'tl.fromTo("#{gid}-w{wi}",{{opacity:0,filter:"blur(10px)"}},{{opacity:1,filter:"blur(0px)",duration:0.125,ease:"expo.out"}},{wt:.4f});')
            js.append(f'tl.fromTo("#{gid}-w{wi}",{{textShadow:"{GLOW_BOOST}"}},{{textShadow:"{shadow}",duration:0.34,ease:"power2.out"}},{wt:.4f});')
        if g.get("left") is not None:
            L = " ".join(spans[:g["left"]])
            R = " ".join(spans[g["left"]:])
            inner = f'<div class="fl L">{L}</div><div class="fl R">{R}</div>'
            cls += " flank " + opt.get("flank", "pol")
        else:
            inner = " ".join(spans)
        d = g["t1"] - g["t0"]
        els.append(f'<div id="{gid}" class="clip {cls}" data-start="{t0s(g["t0"])}" data-duration="{tds(g["t0"], d)}" data-track-index="0" '
                   f'style="--y:{y * 100:.1f}%;--s:{size}" data-layout-allow-overlap>{inner}</div>')
    css = f"""{FONT_FACE}
#root{{position:absolute;inset:0;pointer-events:none}}
.cg{{position:absolute;left:0;right:0;top:calc(var(--y) - 60px * var(--s));height:calc(120px * var(--s));line-height:calc(120px * var(--s));text-align:center;white-space:nowrap;overflow:visible;font-family:"Instrument Serif";font-style:italic;font-size:calc(80px * var(--s));word-spacing:0.02em}}
.cg .w{{display:inline-block;opacity:0;color:#fff;text-shadow:{GLOW};vertical-align:baseline}}
.cg .i{{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-size:calc(80px * var(--s));letter-spacing:-0.01em}}
.cg .b{{font-family:"Inter Tight";font-weight:760;font-size:calc(62px * var(--s));letter-spacing:-0.045em}}
.cg .big.b{{font-size:calc(62px * var(--s) * 1.35)}}
.cg .big.i{{font-size:calc(80px * var(--s) * 1.2)}}
.cg.dark .w{{color:#050505;text-shadow:{DGLOW}}}
.cg.flank .fl{{position:absolute;top:0}}
.cg.flank .L{{text-align:right;padding-right:34px}}
.cg.flank .R{{text-align:left;padding-left:34px}}
.cg.flank.pol .L{{left:0;width:490px}}
.cg.flank.pol .R{{left:950px;width:490px}}
.cg.flank.poster .L{{left:0;width:340px}}
.cg.flank.poster .R{{left:1100px;width:340px}}
"""
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
    {chr(10).join("    " + e for e in els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""


def fx_html():
    els = []
    js = []
    for i, it in enumerate(sorted(FX, key=lambda x: x["t0"])):
        fid = f"fx-{i:03d}"
        d = it["t1"] - it["t0"]
        common = f'id="{fid}" class="clip" data-start="{t0s(it["t0"])}" data-duration="{tds(it["t0"], d)}" data-track-index="0"'
        if it["type"] == "slam":
            els.append(f'<div {common} data-layout-allow-overflow data-layout-ignore><div class="slam" id="{fid}-t">{html.escape(it["word"])}</div></div>')
            js.append(f'tl.fromTo("#{fid}-t",{{scale:1.18,opacity:1}},{{scale:1.0,opacity:0.9,duration:{d:.4f},ease:"power2.out"}},{it["t0"]:.4f});')
        elif it["type"] == "flash":
            els.append(f'<div {common}><div class="flash"></div></div>')
        elif it["type"] == "sting":
            els.append(f'<div {common} data-layout-allow-overflow><div class="sting" id="{fid}-t"><span class="si">Robert</span> <span class="sb">PATTINSON</span></div></div>')
            # stepped at 12 fps: steps() over the scale-down, then a 0.8 s fade
            js.append(f'tl.fromTo("#{fid}-t",{{scale:1.6,opacity:0}},{{scale:1.0,opacity:1,duration:0.5,ease:"steps(6)"}},{it["t0"]:.4f});')
            js.append(f'tl.to("#{fid}-t",{{opacity:0,duration:0.6,ease:"steps(7)"}},{it["t1"] - 0.62:.4f});')
    css = f"""{FONT_FACE}
#root{{position:absolute;inset:0;pointer-events:none}}
.slam{{position:absolute;left:-200px;right:-200px;top:50%;transform-origin:50% 50%;text-align:center;font-family:"Instrument Serif";font-style:italic;font-size:430px;line-height:1;margin-top:-230px;color:#fff;letter-spacing:-0.02em;white-space:nowrap;text-shadow:0 0 18px rgba(255,255,255,0.95),0 0 60px rgba(255,255,255,0.8),0 0 140px rgba(255,255,255,0.6)}}
.flash{{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,#ffffff 0%,#ffffff 50%,#e6e6e6 100%)}}
.sting{{position:absolute;left:0;right:0;top:50%;margin-top:-60px;text-align:center;white-space:nowrap;color:#fff;transform-origin:50% 50%;text-shadow:{GLOW};font-family:"Instrument Serif";font-style:italic;font-size:110px}}
.sting .si{{font-family:"Instrument Serif";font-style:italic;font-size:110px}}
.sting .sb{{font-family:"Inter Tight";font-weight:780;font-size:92px;letter-spacing:-0.04em}}
"""
    return f"""<template>
  <style>{css}</style>
  <div id="root" data-composition-id="fx" data-width="{W}" data-height="{H}">
    {chr(10).join("    " + e for e in els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join("    " + j for j in js)}
    window.__timelines["fx"] = tl;
  </script>
</template>
"""


def sfx_peak(name):
    import numpy as np
    p = os.path.join(ROOT, "assets", "sfx", name + ".mp3")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    y = np.frombuffer(raw, np.int16).astype(float)
    hop = 80
    env = [abs(y[i:i + hop]).mean() for i in range(0, len(y) - hop, hop)]
    dur = len(y) / 8000
    return (int(max(range(len(env)), key=lambda i: env[i])) * hop / 8000), dur


def index_html():
    hosts = []
    for i, sc in enumerate(SCENES):
        hosts.append(f'<div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" '
                     f'data-start="{t0s(sc["t0"])}" data-duration="{tds(sc["t0"], sc["t1"] - sc["t0"])}" data-track-index="{1 + i % 2}" '
                     f'data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{10 + i}"></div>')
    hosts.append(f'<div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{ts(TOTAL)}" '
                 f'data-track-index="5" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:80"></div>')
    hosts.append(f'<div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{ts(TOTAL)}" '
                 f'data-track-index="6" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:100"></div>')
    audio = []
    # VO blocks
    for k, ((a, b), o) in enumerate(zip(SPLITS, OFF)):
        audio.append(f'<audio id="vo{k + 1}" class="clip" data-start="{a + o:.4f}" data-duration="{b - a:.4f}" data-media-start="{a:.4f}" '
                     f'data-track-index="10" data-volume="1" src="assets/audio/vo.mp3"></audio>')
    rec = [("rec-cold", 0.0, "assets/audio/cold.wav", 5.875, 1.15),
           ("rec-spider", INS_T[0], "assets/audio/spider.wav", INS[0], 1.35),
           ("rec-kimmel", INS_T[1], "assets/audio/kimmel.wav", INS[1], 1.15),
           ("rec-hansen", INS_T[2], "assets/audio/hansen.wav", INS[2], 1.5)]
    for rid, t, srcp, d, vol in rec:
        audio.append(f'<audio id="{rid}" class="clip" data-start="{t:.4f}" data-duration="{d:.4f}" data-track-index="11" '
                     f'data-volume="{vol}" src="{srcp}"></audio>')
    lanes = []                                   # end time per lane
    for j, (t, name, vol) in enumerate(sorted(SFX)):
        peak, dur = sfx_peak(name)
        start = max(0.0, t + FRAME - peak)
        dur = min(dur, TOTAL - start)
        lane = next((k for k, e in enumerate(lanes) if e <= start), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = start + dur
        audio.append(f'<audio id="sfx-{j:02d}-{name}" class="clip" data-start="{start:.4f}" data-duration="{dur:.4f}" '
                     f'data-track-index="{12 + lane}" data-volume="{vol}" src="assets/sfx/{name}.mp3"></audio>')
    hosts_s = "\n      ".join(hosts)
    audio_s = "\n      ".join(audio)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #ground {{ position: absolute; inset: 0; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{ts(TOTAL)}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
      <div id="ground"></div>
      {hosts_s}
      {audio_s}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def prep_audio():
    """Receipt audio: voice stems (music removed) trimmed to their windows; VO copied."""
    a = os.path.join(ROOT, "assets", "audio")
    os.makedirs(a, exist_ok=True)
    sep = os.path.join(ROOT, "work", "ins", "sep", "htdemucs")
    jobs = [
        ("vo.mp3", os.path.join(ROOT, "work", "vo", "vo.mp3"), 0, None, []),
        ("cold.wav", os.path.join(sep, "cold", "vocals.wav"), 0, 5.875, ["afade=t=out:st=5.70:d=0.17"]),
        ("spider.wav", os.path.join(sep, "spider", "vocals.wav"), 1.45, INS[0], ["afade=t=in:d=0.03", f"afade=t=out:st={INS[0] - 0.08}:d=0.08"]),
        ("kimmel.wav", os.path.join(ROOT, "work", "ins", "kimmel.wav"), 0, INS[1], [f"afade=t=out:st={INS[1] - 0.08}:d=0.08"]),
        ("hansen.wav", os.path.join(sep, "hansen", "vocals.wav"), 0.50, INS[2], ["afade=t=in:d=0.03", f"afade=t=out:st={INS[2] - 0.08}:d=0.08"]),
    ]
    for name, src, ss, dur, af in jobs:
        out = os.path.join(a, name)
        if name == "vo.mp3":
            if not os.path.exists(out):
                subprocess.run(["cp", src, out], check=True)
            continue
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(dur), "-i", src]
        if af:
            cmd += ["-af", ",".join(af)]
        cmd += ["-ar", "48000", out]
        subprocess.run(cmd, check=True)


def apply_looks():
    os.makedirs(os.path.join(ROOT, "work", "looks"), exist_ok=True)
    files = [f"compositions/{s['id']}.html" for s in SCENES]
    for name, g in LOOKS.items():
        p = os.path.join(ROOT, "work", "looks", f"{name}.json")
        json.dump(g, open(p, "w"))
    for f in files:
        txt = open(os.path.join(ROOT, f)).read()
        for name in LOOKS:
            if f'data-look="{name}"' not in txt:
                continue
            r = subprocess.run(["npx", "hyperframes", "media-treatment", "--file", f,
                                "--selector", f'[data-look="{name}"]', "--grading",
                                os.path.join(ROOT, "work", "looks", f"{name}.json"), "--apply", "--json"],
                               cwd=ROOT, capture_output=True, text=True)
            ok = '"ok":true' in r.stdout.replace(" ", "") or '"ok": true' in r.stdout
            print(f"  look {name:9s} -> {f}: {'ok' if ok else 'FAILED ' + r.stdout[:300] + r.stderr[:300]}")


def _luma_of(path, offset=0.0):
    """Mean luma (0-255) of the caption band (x 22-78 %, y 40-56 %) of an image or a clip frame."""
    full = os.path.join(ROOT, path)
    if path.endswith(".mp4"):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, offset):.3f}", "-i", full, "-frames:v", "1",
                              "-vf", "scale=144:108", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                             capture_output=True).stdout
        if len(raw) < 144 * 108:
            return 0
        import numpy as np
        a = np.frombuffer(raw[:144 * 108], np.uint8).reshape(108, 144)
    else:
        import numpy as np
        a = np.asarray(Image.open(full).convert("L").resize((144, 108)))
    return float(a[43:61, 32:112].mean())


def bg_luma(t):
    best = None
    for sc in SCENES:
        if not (sc["t0"] <= t < sc["t1"]):
            continue
        for n, it in enumerate(sc["items"], start=1):
            if it["t0"] <= t < it["t1"]:
                z = it["z"] * 1000 + n * 6
                if best is None or z >= best[0]:
                    best = (z, it)
    if best is None:
        return 0
    it = best[1]
    if it["type"] == "shot":
        return _luma_of(it["src"], t - it["t0"])
    if it["type"] == "memes":
        return _luma_of(it["bg"], t - it["t0"])
    if it["type"] == "split":
        return _luma_of(it["left"], t - it["t0"])
    return 0                                   # cards, Polaroid, poster, strips, grid: dark ground


def mark_dark(groups):
    n = 0
    for g in groups:
        if g.get("left") is not None or g["opt"].get("nodark"):
            continue
        t = min(g["t0"] + 0.12, g["t1"] - FRAME)
        lum = bg_luma(t)
        g["luma"] = round(lum)
        if lum > 128:
            g["auto_dark"] = True
            n += 1
    print(f"auto-dark captions: {n}")


def main():
    for d in ("assets/clips", "assets/img", "compositions"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    build_edl()
    if DO_MEDIA:
        prep_audio()
    groups = caption_groups()
    mark_dark(groups)
    for sc in SCENES:
        open(os.path.join(ROOT, "compositions", f"{sc['id']}.html"), "w").write(scene_html(sc))
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(captions_html(groups))
    open(os.path.join(ROOT, "compositions", "fx.html"), "w").write(fx_html())
    open(os.path.join(ROOT, "index.html"), "w").write(index_html())
    nshots = sum(len(s["items"]) for s in SCENES)
    print(f"scenes {len(SCENES)}, items {nshots}, caption groups {len(groups)}, fx {len(FX)}, sfx {len(SFX)}, media {len(MEDIA_LOG)}")
    if DO_LOOKS:
        bake_all()


if __name__ == "__main__":
    main()
