"""v4, part 1 (to "Freedom."): v2's cut on the user's cut-down voiceover (tools/vo4.py), with the user's notes.

Times are on the final timeline. SHOTS feed prep.py (EDL=edl4); build4.py writes the HTML.
W(i) / cut(i) take the ORIGINAL word index i (words.json); removed words have no time.
"""
import json, os
from edl import SRC as _SRC, CROP as _CROP, PROJ, ROOT, FPS, VO_OFFSET, NEWS_IN, NEWS_DUR, N, S

SRC = dict(_SRC)
SRC.update({"ajit": "Video by madebyajit [0-29s].mp4", "leno": "Video by lenojoga [0-15s].mp4"})
CROP = dict(_CROP)
CROP.update({"ajit": (0, 117, 1500, 844), "leno": (0, 30, 972, 547)})

_V = json.load(open(os.path.join(PROJ, "words4.json"), encoding="utf-8"))
_W4 = {w["i"]: w for w in _V["words"]}
VO_DUR = _V["duration"]


def W(i):  return round(_W4[i]["start"] + VO_OFFSET, 3)
def WE(i): return round(_W4[i]["end"] + VO_OFFSET, 3)
def WT(i): return _W4[i]["text"]
def cut(i): return round(W(i) - 0.06, 3)
def has(i): return i in _W4


TOTAL = round(VO_OFFSET + VO_DUR + 0.9, 2)       # "freedom." holds ~1.9 s, then the part ends
F = 1 / FPS


def S4(id, src, sin, start, end, crop="auto", grade="none", speed=1.0, card=None, push=None):
    if crop == "auto":
        crop = CROP.get(src)
    return dict(id=id, src=src, sin=sin, start=round(start, 3), end=round(end, 3), fit="card" if card else "cover",
                crop=crop, grade=grade, speed=speed, reverse=False, card=card, push=push)


B = lambda a, b, shots, **kw: dict(a=a, b=b, shots=shots, **kw)
DIM = {"grade": "dim"}

# ---------------------------------------------------------------------------------------------- footage sections
SECTIONS = [
    ("sa", [
        B(0, 2, [("nyc", 0.3), ("wait5", 1.6)]),
        B(3, 5, "GRID"),
        B(6, 9, [("wait5", 8.05, {"crop": (0, 170, 1080, 608)}), ("eyes", 3.62)]),     # the fan's face, not his neck
        B(10, 12, [("next", 1573.0, DIM), ("em6", 10.0)]),
        B(13, 17, [("t1", 24.95), ("preload", 6.6)]),
        B(18, 21, [("nlook", 16.6), ("launch", 68.0)]),
    ]),
    # "r7": GTA 6 took 13 years to make. And yet, nobody seems to have moved on.  (built by build4.r7_scene)
    ("se", [
        B(55, 57, [("eyes", 3.62)]),
        B(58, 60, [("goodbye", 0.25), ("goodbye", 5.6)]),                            # the kid handed GTA V
        B(61, 63, [("waitgta6", 9.0), ("wait5", 11.2), ("nostalgia", 15.5)]),        # waiting; the GTA V crew
        B(64, 68, [("vox", 3.3), ("blade", 0.05), ("launch", 25.9)]),                # launch 25.9 replaces the split frame
        B(69, 72, [("t2", 9.9), ("next", 492.5), ("nlook", 6.85)]),
    ]),
    ("sf", [
        B(73, 74, [("t1", 70.4)]),
        B(75, 78, [("t2", 34.7), ("blade", 14.3)]),
        B(79, 79, [("t1", 32.7)]),
        B(80, 81, [("launch", 72.15), ("t1", 76.8, DIM)]),
    ]),
]
SPAN = {"sa": (VO_OFFSET, cut(22)), "r7": (cut(22), cut(55)), "se": (cut(55), cut(73)), "sf": (cut(73), cut(82)),
        "sg": (cut(82), cut(90)), "sh": (cut(90), TOTAL)}

# "millions of adults": 3x3 grid; the centre (wait5 2.15) and Times Square / club / Ocean Drive kept from v2
GRID_CELLS = [("t1", 34.2, {}), ("nyc", 9.0, {}), ("t1", 27.7, {}), ("t2", 79.8, {}), ("wait5", 2.15, {}),
              ("t2", 124.62, {}), ("t2", 99.8, {}), ("launch", 46.5, {}), ("launch", 54.6, {})]

# reference 7 tiles, clockwise from top-left (TL, TM, TR, MR, BR, BM, BL, ML): long single shots, cut 960x540 for the zoom
R7_TILES = [("t2", 53.0), ("t1", 11.2), ("t2", 66.3), ("t2", 27.5), ("t2", 129.5), ("t2", 63.14), ("launch", 6.31),
            ("t2", 41.7)]

# "It was about what it really gave you." -- the scoopedfriday burst: 1-4 frame cuts, posterised and B&W flash frames,
# then one held shot into "Freedom."   (src, in, frames, grade)
BURST = [("t2", 140.3, 4, "none"), ("launch", 48.6, 3, "none"), ("t1", 25.6, 1, "poster"), ("t1", 25.62, 4, "none"),
         ("t2", 141.95, 3, "none"), ("t2", 138.3, 2, "bwhi"), ("t2", 138.4, 3, "none"), ("t1", 36.0, 3, "none"),
         ("t2", 149.4, 1, "poster"), ("t2", 149.45, 4, "none"), ("t1", 23.5, 3, "none"), ("ajit", 13.2, 2, "bwhi"),
         ("launch", 73.6, 4, "none"), ("t1", 3.0, 3, "none"), ("t2", 153.2, 1, "poster")]
BURST_HOLD = ("t2", 153.25)


def _edges(t0, t1, a, b, n):
    """cut points: the word onsets inside the beat closest to an even split"""
    onsets = [cut(i) for i in range(a + 1, b + 1) if has(i)]
    cuts = []
    for k in range(1, n):
        target = t0 + (t1 - t0) * k / n
        c = [o for o in onsets if o > (cuts[-1] if cuts else t0) + 0.25 and o < t1 - 0.25]
        cuts.append(min(c, key=lambda o: abs(o - target)) if c else round(target, 3))
    return [t0] + cuts + [t1]


SHOTS = [
    S4("news", "news", NEWS_IN, 0.0, NEWS_DUR, crop=(0, 0, 1280, 720)),
    S4("newsblur", "news", NEWS_IN, 0.0, NEWS_DUR, crop=(0, 0, 1280, 720), grade="blur"),
    S4("cj", "awshit", 0.0, NEWS_DUR, VO_OFFSET, crop=(107, 0, 1707, 960)),
]
GRID = None
for cid, beats in SECTIONS:
    s0, s1 = SPAN[cid]
    for bi, bt in enumerate(beats):
        t0 = s0 if bi == 0 else cut(bt["a"])
        t1 = cut(beats[bi + 1]["a"]) if bi + 1 < len(beats) else s1
        if bt["shots"] == "GRID":
            GRID = (t0, t1)
            for k, (src, sin, opt) in enumerate(GRID_CELLS):
                SHOTS.append(S4(f"grid{k}", src, sin, t0, t1, card=(640, 360), **opt))
            continue
        edges = _edges(t0, t1, bt["a"], bt["b"], len(bt["shots"]))
        for k, sh in enumerate(bt["shots"]):
            opt = sh[2] if len(sh) > 2 else {}
            SHOTS.append(S4(f"{cid}{bi}{chr(97 + k)}", sh[0], sh[1], edges[k], edges[k + 1], **opt))

R7 = {"t0": cut(22), "t1": cut(55), "tw": cut(47)}
R7["tz"] = round(round((W(24) - 0.14) * FPS) / FPS, 4)          # the zoom onto the logo card, just before "took"
for k, (src, sin) in enumerate(R7_TILES):
    SHOTS.append(S4(f"r7t{k}", src, sin, R7["t0"], R7["tw"], card=(960, 540)))

g0, g1 = SPAN["sg"]
t = g0
for k, (src, sin, nf, grade) in enumerate(BURST):
    SHOTS.append(S4(f"g{k:02d}", src, sin, t, round(t + nf / FPS, 4), grade=grade))
    t = round(t + nf / FPS, 4)
SHOTS.append(S4("g99", BURST_HOLD[0], BURST_HOLD[1], t, g1))
SHOTS.append(S4("fr", "freedom", 0.3, cut(90), TOTAL, push=(1.0, 1.05)))
