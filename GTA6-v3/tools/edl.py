"""GTA 6 edit (v2, Tesla Roadster grammar): footage under every word, cut fast on the spoken words.

Every time is on the final timeline (seconds). The voiceover sits at VO_OFFSET; W(i) is the onset of VO word i
(words.json) and cut(i) the picture cut two frames ahead of it.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # .../GTA 6 edit
PROJ = os.path.join(ROOT, "gta6-edit")
FPS = 30
VO_OFFSET = 7.34
NEWS_IN, NEWS_DUR = 0.55, 4.87          # the reporter's line: news.mp4 0.55 -> 5.42
TOTAL = 106.5                           # v2 ends here (the date card 105.2 -> 106.5); v3 sets its own

_W = json.load(open(os.path.join(PROJ, "words.json"), encoding="utf-8"))
_N = json.load(open(os.path.join(PROJ, "words_news.json"), encoding="utf-8"))


def W(i):  return round(_W[i]["start"] + VO_OFFSET, 3)
def WT(i): return _W[i]["text"]
def cut(i): return round(W(i) - 0.06, 3)
def N(i):  return round(_N[i]["start"] - NEWS_IN, 3)


SRC = {  # alias -> file under ROOT
    "news": "_dl/news/news.mp4",
    "money": "_dl/money/money.mp4",
    "awshit": "Aw shit, here we go again (Original) Grand Theft Auto San Andreas.mp4",
    "t1": "Grand Theft Auto VI Trailer 1.mp4",
    "t2": "Grand Theft Auto VI Trailer 2.mp4",
    "launch": "Grand Theft Auto VI Launch Trailer (1).mp4",          # 4K
    "nlook": "Grand Theft Auto VI An Extended Look   Now Playing   Netflix.mp4",   # 4K
    "preload": "Grand Theft Auto VI Pre-Load Now.mp4",
    "next": "GTA 6 4K Gameplay Trailer FULL NETFLIX EXTENDED.mp4",  # 4K
    "vc10": "Grand Theft Auto Vice City 10th Anniversary Edition Trailer [0-72.7s].mp4",
    "vcde": "How the Vice City Definitive Edition should have looked [0-72.7s].mp4",
    "panzer": "The Rhino Tank - Steal it like a Man - Keep it Forever GTA VC [0-149.2s].mp4",
    "kidlake": "Pinterest video #1125829606870167260 [0-17.4s].mp4",
    "millions": "Men in black [0-8s].mp4",
    "freedom": "From Klickpin.com- Need fresh inspiration Refresh these simple healthy habit ideas perfect for saving sharing and recreating later designed to fee.mp4",
    "escape": "From Klickpin.com- Polished nail design inspiration that look expensive while staying practical realistic and beginner friendly for busy people wh (1).mp4",
    "adult": "From Klickpin.com- Polished nail design inspiration that look expensive while staying practical realistic and beginner friendly for busy people wh.mp4",
    "goodbye": "Video by shamsycreates [0-22s].mp4",
    "waitgta6": "Video by lucanox.2 [0-34.05s].mp4",
    "wait5": "Video by saudalhomud [0-16.96s].mp4",
    "nostalgia": "Video by bykeipker [0-37.3s].mp4",
    "nyc": "Video by will__nyc [0-15s].mp4",
    "vox": "Video by kiuzr [0-15s].mp4",
    "eyes": "Video by ntprimee [0-20s].mp4",
    "city": "Video by __lio.x__ [0-83.9s].mp4",
    "montage": "Video by _brooklynfilms_ [0-28.9s].mp4",
    "montage2": "Video by swxft_404 [0-16s].mp4",
    "emontage": "Video by nevalcuts [0-12s].mp4",
    "em6": "Video by 6u.x9 [0-13s].mp4",
    "edits": "Video by matthewhoyos [0-15s].mp4",
    "blade": "Video by blade.fxs [0-32.6s].mp4",
    "oldchars": "Video by kaye.creatives [0-54.4s].mp4",
    "metav3rse": "Video by metav3rse [0-23.2s].mp4",
}

# default crop to a 16:9 picture (letterbox bars removed, vertical/square sources banded)
CROP = {
    "t2": (192, 108, 1536, 864), "launch": (384, 120, 3072, 1728), "preload": (107, 60, 1706, 960),
    "vc10": (178, 100, 924, 520), "millions": (0, 187, 720, 405),
    "montage": (0, 236, 1080, 608), "nostalgia": (0, 236, 1080, 608), "emontage": (0, 146, 1400, 788),
    "blade": (0, 135, 1440, 810), "vox": (0, 135, 1440, 810), "oldchars": (0, 135, 1440, 810), "goodbye": (0, 135, 1440, 810),
    "city": (0, 875, 1440, 810), "waitgta6": (0, 700, 1440, 810), "nyc": (0, 820, 1440, 810),
    "edits": (0, 656, 1080, 608), "montage2": (0, 656, 1080, 608), "metav3rse": (0, 656, 1080, 608), "wait5": (0, 656, 1080, 608),
}


def S(id, src, sin, start, end, crop="auto", grade="none", speed=1.0, card=None, push=None):
    if crop == "auto":
        crop = CROP.get(src)
    return dict(id=id, src=src, sin=sin, start=round(start, 3), end=round(end, 3), fit="card" if card else "cover",
                crop=crop, grade=grade, speed=speed, reverse=False, card=card, push=push)


# ---------------------------------------------------------------------------------------------------------
# Beats: (first word, last word, [(src, in, {opts}), ...]).  A beat runs from cut(first) to cut(last + 1);
# its shots are cut on the word onsets that split it most evenly.
# ---------------------------------------------------------------------------------------------------------
B = lambda a, b, shots, **kw: dict(a=a, b=b, shots=shots, **kw)
BW = {"grade": "bw"}
DIM = {"grade": "dim"}

SECTIONS = [
    ("sa", [
        B(0, 2, [("nyc", 0.3), ("wait5", 1.6)]),
        B(3, 5, "GRID"),
        B(6, 9, [("wait5", 8.05), ("eyes", 3.62)]),
        B(10, 12, [("next", 1573.0, DIM), ("em6", 10.0)]),
        B(13, 17, [("t1", 24.95), ("preload", 6.6)]),
        B(18, 21, [("nlook", 16.6), ("launch", 68.0)]),
    ]),
    ("sb", [
        B(22, 24, [("eyes", 15.85), ("t1", 2.85)]),
        B(25, 26, [("t1", 35.85), ("t2", 8.3)]),
        B(27, 30, [("money", 0.9), ("money", 2.7)]),
        B(31, 32, [("blade", 2.95), ("t1", 30.1)]),
    ]),
    ("sc", [
        B(33, 37, [("t2", 45.4), ("launch", 20.6)]),
        B(38, 38, [("t1", 63.7)]),
        B(39, 41, [("t2", 66.3), ("nlook", 12.9), ("montage", 13.3)]),
        B(42, 46, [("t2", 147.4), ("launch", 46.4), ("em6", 8.95)]),
    ]),
    ("sd", [
        B(47, 48, [("nyc", 4.3)]),
        B(49, 54, [("nyc", 8.1), ("waitgta6", 7.2), ("metav3rse", 3.0)]),
        B(55, 56, [("eyes", 3.62), ("eyes", 4.42)]),
    ]),
    ("sf", [
        B(57, 60, [("wait5", 11.2), ("waitgta6", 9.0)]),
        B(61, 63, [("wait5", 13.6), ("t2", 49.95)]),
        B(64, 68, [("vox", 3.3), ("blade", 0.05), ("emontage", 0.2)]),
        B(69, 72, [("t2", 9.9), ("next", 492.5), ("nlook", 6.85)]),
    ]),
    ("sg", [
        B(73, 74, [("t1", 70.4)]),
        B(75, 78, [("t2", 34.7), ("blade", 14.3)]),
        B(79, 79, [("t1", 32.7)]),
        B(80, 81, [("launch", 72.15), ("t1", 76.8, DIM)]),
        B(82, 85, [("t1", 19.3, DIM)]),
        B(86, 89, [("t1", 5.05), ("launch", 62.6)]),
        B(90, 90, [("freedom", 0.3, {"push": (1.0, 1.05)})]),
    ]),
    ("si", [
        B(91, 93, [("vc10", 18.2)]),
        B(94, 96, [("goodbye", 0.25), ("kidlake", 14.6)]),
        B(97, 103, [("waitgta6", 0.6)]),
        B(104, 106, [("waitgta6", 2.6), ("vc10", 23.5)]),
        B(107, 114, [("vc10", 29.4), ("vcde", 11.7), ("panzer", 30.0)]),
        B(115, 120, [("vc10", 36.9), ("vcde", 37.75), ("vcde", 48.9)]),
    ]),
    ("sj", [
        B(121, 124, [("panzer", 5.0)]),
        B(125, 126, [("vc10", 53.95), ("vcde", 44.4)]),
        B(127, 127, [("panzer", 100.0)]),
        B(128, 134, [("panzer", 121.0), ("vc10", 58.95), ("vc10", 44.3)]),
    ]),
    ("sk", [
        B(135, 137, [("kidlake", 0.5)]),
        B(138, 142, [("vc10", 28.25), ("vcde", 15.3)]),
        B(143, 147, [("escape", 2.75, DIM), ("escape", 7.35)]),
        B(148, 150, [("escape", 8.45, DIM), ("next", 1140.0, DIM)]),
    ]),
    ("sl", [
        B(151, 153, [("t1", 37.6)]),
        B(154, 158, [("launch", 66.5), ("vcde", 52.7), ("launch", 9.4)]),
        B(159, 160, [("launch", 25.8), ("montage", 3.95)]),
        B(161, 162, [("launch", 59.4), ("blade", 13.05)]),
        B(163, 164, [("t2", 142.0), ("launch", 54.6)]),
        B(165, 169, [("next", 1129.0), ("city", 24.0), ("next", 996.5)]),
    ]),
    ("sm", [
        B(170, 174, [("emontage", 6.25)]),
        B(175, 180, [("launch", 32.25), ("vcde", 7.85)]),
        B(181, 185, [("t1", 63.7), ("nlook", 11.7)]),
        B(186, 187, [("t2", 118.05), ("launch", 60.2)]),
        B(188, 194, [("t1", 68.8), ("montage", 7.6)]),
        B(195, 202, [("t1", 27.6), ("nlook", 2.1), ("t1", 21.9)]),
    ]),
    ("sn", [
        B(203, 207, [("goodbye", 2.4), ("oldchars", 11.8)]),
        B(208, 211, [("goodbye", 18.3), ("nostalgia", 5.5)]),
        B(212, 212, [("adult", 0.7, BW)]),
        B(213, 216, [("adult", 3.0, BW), ("adult", 6.1, BW)]),
        B(217, 221, [("adult", 7.5, BW), ("millions", 2.0, BW)]),
        B(222, 231, [("t1", 11.2), ("t2", 83.2), ("montage", 25.4)]),
    ]),
    ("so", [
        B(232, 235, [("next", 1573.5), ("em6", 10.2)]),
        B(236, 240, [("vc10", 11.05, DIM), ("vcde", 5.7, DIM)]),
        B(241, 242, [("t1", 39.9, {"push": (1.0, 1.06)})]),
        B(243, 248, [("vc10", 16.65), ("vc10", 28.3), ("vcde", 54.6)]),
    ]),
    ("sp", [
        B(249, 253, [("metav3rse", 3.0), ("nostalgia", 0.1)]),
        B(254, 258, [("nostalgia", 5.5), ("oldchars", 26.0)]),
        B(259, 260, [("nostalgia", 27.5, {"speed": 0.6})]),
        B(261, 265, [("next", 769.0), ("next", 745.0)]),
        B(266, 267, [("next", 781.0, {"speed": 0.7}), ("t1", 35.85)]),
    ]),
    ("sq", [
        B(268, 270, [("kidlake", 9.2)]),
        B(271, 274, [("vc10", 48.8), ("vcde", 13.7), ("vc10", 25.2)]),
        B(275, 277, [("waitgta6", 12.0), ("wait5", 15.7)]),
        B(278, 281, [("wait5", 12.7), ("waitgta6", 20.0)]),
        B(282, 283, [("wait5", 13.7), ("eyes", 16.0)]),
        B(284, 288, [("nlook", 17.5), ("freedom", 3.0)], end=103.85),
    ]),
]

GRID_CELLS = [("millions", 0.4, BW), ("nyc", 9.0, {}), ("t1", 21.95, {}), ("adult", 1.0, {}), ("wait5", 2.15, {}),
              ("preload", 17.95, {}), ("t2", 99.8, {}), ("launch", 46.5, {}), ("montage2", 1.0, {})]


def _beat_end(sec_i, beat_i):
    sec = SECTIONS[sec_i][1]
    bt = sec[beat_i]
    if "end" in bt:
        return bt["end"]
    if beat_i + 1 < len(sec):
        return cut(sec[beat_i + 1]["a"])
    if sec_i + 1 < len(SECTIONS):
        return cut(SECTIONS[sec_i + 1][1][0]["a"])
    return 103.85


SHOTS = [
    S("news", "news", NEWS_IN, 0.0, NEWS_DUR, crop=(0, 0, 1280, 720)),
    S("cj", "awshit", 0.0, NEWS_DUR, VO_OFFSET, crop=(107, 0, 1707, 960)),
]
SECTION_SPAN = {}
GRID = None
for si_, (cid, beats) in enumerate(SECTIONS):
    s0 = cut(beats[0]["a"]) if si_ else VO_OFFSET
    for bi, bt in enumerate(beats):
        t0 = cut(bt["a"]) if (si_ or bi) else VO_OFFSET
        t1 = _beat_end(si_, bi)
        if bt["shots"] == "GRID":
            GRID = (t0, t1)
            for k, (src, sin, opt) in enumerate(GRID_CELLS):
                SHOTS.append(S(f"grid{k}", src, sin, t0, t1, card=(640, 360), **opt))
            continue
        n = len(bt["shots"])
        # cut points: the word onsets inside the beat closest to an even split
        onsets = [cut(i) for i in range(bt["a"] + 1, bt["b"] + 1)]
        cuts = []
        for k in range(1, n):
            target = t0 + (t1 - t0) * k / n
            cands = [o for o in onsets if o > (cuts[-1] if cuts else t0) + 0.25 and o < t1 - 0.25]
            cuts.append(min(cands, key=lambda o: abs(o - target)) if cands else round(target, 3))
        edges = [t0] + cuts + [t1]
        for k, sh in enumerate(bt["shots"]):
            src, sin = sh[0], sh[1]
            opt = sh[2] if len(sh) > 2 else {}
            SHOTS.append(S(f"{cid}{bi}{chr(97 + k)}", src, sin, edges[k], edges[k + 1], **opt))
    SECTION_SPAN[cid] = (s0, _beat_end(si_, len(beats) - 1))

# the end: the neon VI, then Rockstar's own date card
SHOTS.append(S("end1", "preload", 6.75, 103.85, 105.2))
SHOTS.append(S("end2", "next", 1597.2, 105.2, TOTAL))
SECTION_SPAN["sq"] = (SECTION_SPAN["sq"][0], TOTAL)
