"""v4, the whole video: v2's cut on the user's cut-down voiceover (tools/vo4.py), with the user's notes.

Times are on the final timeline. SHOTS feed prep.py (EDL=edl4); build4.py writes the HTML.
W(i) / cut(i) take the ORIGINAL word index i (words.json); removed words have no time.
"""
import json, os
import edl as V2
from edl import SRC as _SRC, CROP as _CROP, PROJ, ROOT, FPS, VO_OFFSET, NEWS_IN, NEWS_DUR, N, S

SRC = dict(_SRC)
SRC.update({"ajit": "Video by madebyajit [0-29s].mp4", "leno": "Video by lenojoga [0-15s].mp4",
            "beatdrop": "beat drop reference.mp4",                                  # the user's "Ah shit" reference
            "pinA": "Pinterest video #1084804629023881773 [0-9.4s].mp4",            # cinematic clips pinterest/
            "pinB": "Pinterest video #1092122978546016645 [0-6s].mp4",
            "notebook": "Kid_viewing_notebook_cheat_codes_e009eda5_t0-3.9_1080p.mp4",        # the user's cheat-code notebook
            "dreams": "chasing dreams.mp4",                                                # the user's "chasing dreams" clip
            "kidtalk": "Video by theunknownbrands [0-49s].mp4"})                           # the user's clip: talking to the kid
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


END_V = round(_W4[288]["end"] + VO_OFFSET + 0.33, 3)   # v2: the last beat runs 0.33 s past "again.", then a flash,
TOTAL = round(END_V + 2.65, 2)                          # the GTA VI logo (1.35 s) and the date card (1.3 s)
NEWS_TM = round(N(11) - 0.06, 3)                 # "a billion dollars": cut from the news to the money clip
T_BD = round(NEWS_DUR + 1.54 - 0.06, 3)          # "here we go again": cut to the beat-drop clip until "millions"
F = 1 / FPS


def S4(id, src, sin, start, end, crop="auto", grade="none", speed=1.0, card=None, push=None, rot=None):
    if crop == "auto":
        crop = CROP.get(src)
    d = dict(id=id, src=src, sin=sin, start=round(start, 3), end=round(end, 3), fit="card" if card else "cover",
             crop=crop, grade=grade, speed=speed, reverse=False, card=card, push=push)
    if rot:
        d["rot"] = rot              # "ccw": a source stored sideways, turned upright before the crop (prep.py)
    return d


B = lambda a, b, shots, **kw: dict(a=a, b=b, shots=shots, **kw)
DIM = {"grade": "dim"}
BW = {"grade": "bw"}
VC_LOGO_IN = round(57.8 - (cut(241) + 0.03 - cut(236)), 2)   # the Vice City logo forms at 57.8 s: lands on "Vice"


def v2_at(cid, bi):
    """the cut points inside v2's beat (cid, bi): the word index where v2 cut on a word onset, else the fraction of
    the beat -- so a beat the user approved in v2 keeps v2's cuts on the shortened voiceover"""
    shots = sorted((x for x in V2.SHOTS if x["id"].startswith(f"{cid}{bi}") and len(x["id"]) == len(cid) + 2),
                   key=lambda x: x["start"])
    t0, t1 = shots[0]["start"], shots[-1]["end"]
    out = []
    for x in shots[1:]:
        hit = [i for i in range(len(V2._W)) if abs(V2.cut(i) - x["start"]) < 0.002]
        out.append(hit[0] if hit else round((x["start"] - t0) / (t1 - t0), 4))
    return out

# ---------------------------------------------------------------------------------------------- footage sections
SECTIONS = [
    ("sa", [
        B(3, 5, "GRID"),
        B(6, 9, [("wait5", 8.05, {"crop": (0, 170, 1080, 608)}), ("eyes", 3.62)]),     # the fan's face, not his neck
        B(10, 12, [("next", 1573.0, DIM), ("em6", 10.0)]),
        B(13, 17, [("t1", 24.95), ("preload", 6.15, {"speed": 2.0})]),          # the GTA VI logo, sped up to land on "GTA 6"
        B(18, 21, [("nlook", 16.6), ("launch", 68.0)]),
    ]),
    # "r7": GTA 6 took 13 years to make. And yet, nobody seems to have moved on.  (built by build4.r7_scene)
    ("se", [
        B(55, 57, [("eyes", 3.62)]),
        B(58, 60, [("goodbye", 0.25, {"grade": "nolabel"}), ("goodbye", 5.6, {"grade": "nolabel"})]),   # the kid handed GTA V; "2013" painted out
        B(61, 63, [("waitgta6", 9.0), ("wait5", 11.2), ("nostalgia", 15.5)]),        # waiting; the GTA V crew
        B(64, 68, [("vox", 3.3), ("blade", 0.05), ("launch", 25.9)]),                # launch 25.9 replaces the split frame
        B(69, 72, [("t2", 9.9), ("next", 492.5), ("nlook", 6.85)]),
    ]),
    ("sf", [
        B(73, 74, [("t1", 70.4)]),
        B(75, 78, [("t2", 34.7), ("blade", 14.3)]),
        B(79, 79, [("t1", 32.7)]),
        B(80, 81, [("launch", 72.15), ("leno", 11.5)]),                              # "guns": the shotgun from lenojoga
    ]),
    ("si", [
        B(91, 93, [("vc10", 18.2)]),                                                 # "Back to being": the Vice City car
    ]),
    ("sj", [
        B(104, 106, [("beatdrop", 14.45), ("vc10", 23.5)]),                          # "playing Vice City": the VICE letters, then Vice City
        B(107, 114, [("vc10", 29.4), ("vcde", 13.8), ("panzer", 30.0)]),               # the Cheetah past its "ROCKSTAR NORTH" credit
        B(115, 120, [("vc10", 36.9), ("vcde", 37.75), ("vcde", 48.9)], at=[118, 120]),     # v2's cuts: "hear", "gunshots."
    ]),
    # "nb": With cheat codes like aspirin and panzer  (the user's notebook clip; build4.nb_scene, tools/nb4.py)
    ("sk", [                                                                         # v2's shots (the user: "fine")
        B(128, 134, [("panzer", 121.0), ("vc10", 44.3)], at=[134]),                  # the tank through "back of your" (the zooming boat shot out), | notebook.
        B(135, 137, [("kidlake", 0.5)]),                                             # For a kid,
        B(138, 142, [("vc10", 28.25), ("vcde", 15.3)], at=[142]),                    # it wasn't just a | game.
        B(143, 147, [("escape", 2.75, DIM), ("escape", 7.35)], at=[147]),            # It was a psychological | escape,
    ]),
    # "ar": an alternate reality.  (the user's chasing-dreams clip over a Vice City zoom-out; build4.ar_scene)
    ("sl", [                                                                         # v2's shots (the user: "good")
        B(151, 153, [("t1", 37.6)]),                                                 # It was everything
        B(154, 158, [("launch", 66.5), ("vcde", 52.7), ("launch", 9.4)], at=[156, 157]),   # you imagined | adulthood | would be. (v2, approved)
    ]),
    # "q4": Driving supercars, firing guns, flying planes, and owning an entire city.  (build4.quad_scene)
    # "gp": And while every other game asks you to be  (reference 3's tile wall; tools/gp4.py)
    # "hero": the hero, But GTA lets you be the problem. It lets you be the bad guy  (tools/hero4.py)
    ("sm2", [B(195, 202, [("t1", 27.6), ("nlook", 2.1), ("t1", 21.9)], at=v2_at("sm", 5))]),          # in a world that looks just like yours.
    ("sn", [                                                                                         # v2 (the user: correct)
        B(203, 207, [("goodbye", 2.4, {"grade": "nolabel"}), ("oldchars", 11.8)], at=v2_at("sn", 0)), # the "2013" painted out
        B(208, 211, [("goodbye", 18.3), ("nostalgia", 5.5)], at=v2_at("sn", 1)),
        B(212, 212, [("adult", 0.7, BW)]),
        B(213, 216, [("adult", 3.0, BW), ("adult", 6.1, BW)], at=v2_at("sn", 3)),
        B(217, 221, [("adult", 7.5, BW), ("millions", 2.0, BW)], at=v2_at("sn", 4)),
    ]),
    # "pb": back to the world they once dreamed of living in.  (the Ackman reel's pin board; build4.pb_scene)
    ("so", [
        B(232, 235, [("next", 1573.5), ("em6", 10.2)], at=v2_at("so", 0)),
        B(236, 242, [("vcde", VC_LOGO_IN)]),                             # Rockstar takes you back to Vice City, -- the user: the
                                                                          # Vice City intro ("Rockstar Games presents", the logo on "Vice City")
        B(243, 248, [("vc10", 16.65), ("vc10", 28.3), ("vcde", 54.6)], at=v2_at("so", 3)),
    ]),
    ("sp", [
        B(249, 253, [("metav3rse", 3.0), ("nostalgia", 0.1)], at=v2_at("sp", 0)),
        B(254, 258, [("nostalgia", 5.5), ("oldchars", 26.0)], at=v2_at("sp", 1)),
        B(259, 260, [("nostalgia", 27.5, {"speed": 0.6})]),
        B(261, 265, [("next", 769.0), ("next", 745.0)], at=v2_at("sp", 3)),
        B(266, 267, [("next", 781.0, {"speed": 0.7}), ("t1", 35.85)], at=v2_at("sp", 4)),
    ]),
    ("sq", [
        # "tv2": Because that 10-year-old,  (the user's real-people clip from its start, reference 2's card; build4.tv2_scene)
        B(273, 274, [("ajit", 22.6), ("vc10", 25.2)], at=[274]),                      # "Vice": the VICE letters (madebyajit), "City"
        B(275, 277, [("nostalgia", 16.8, {"crop": (0, 120, 1080, 608)})]),             # never really left. -- the user: the two of them at sunset (~17 s)
        B(278, 281, [("kidtalk", 15.0)]),                                             # He's just been waiting -- the user's clip (~15 s)
        B(282, 283, [("kidtalk", 4.3)]),                                              # 13 years -- them talking to the kid
        B(284, 288, [("nlook", 17.5), ("freedom", 3.0)], at=[287]),               # the freedom B-roll on "freedom" (the big title over it)
    ]),
]
SPAN = {"sa": (cut(3), cut(22)), "r7": (cut(22), cut(55)), "se": (cut(55), cut(73)), "sf": (cut(73), cut(82)),
        "sg": (cut(82), cut(90)), "sh": (cut(90), cut(91)), "si": (cut(91), cut(94)), "sj": (cut(104), cut(121)),
        "nb": (cut(121), cut(128)), "sk": (cut(128), cut(148)), "ar": (cut(148), cut(151)), "sl": (cut(151), cut(159)),
        "q4": (cut(159), cut(170)), "gp": (cut(170), cut(179)), "hero": (cut(179), cut(195)), "sm2": (cut(195), cut(203)),
        "sn": (cut(203), cut(222)), "pb": (cut(222), cut(232)), "so": (cut(232), cut(249)), "sp": (cut(249), cut(268)),
        "tv2": (cut(268), cut(273)), "sq": (cut(273), END_V), "end": (END_V, TOTAL)}
TV2 = {"t0": cut(268), "tc": cut(271), "t1": cut(273)}             # full screen on "Because that 10-year-old,", the card on "playing GTA"
HERO = {"t0": cut(179), "tx": cut(186), "t1": cut(195)}          # the hero -> (at "the problem.") the bad guys
TV = (cut(94), cut(104))                         # "10 years old, sitting in front of the family computer," (tools/tv4.py)
TCARD = cut(97)                                  # the picture becomes a card on "sitting"

# "millions of adults": 3x3 grid; the centre (wait5 2.15) and Times Square / club / Ocean Drive kept from v2
GRID_CELLS = [("t1", 34.2, {}), ("nyc", 9.0, {}), ("t1", 27.7, {}), ("t2", 79.8, {}), ("wait5", 2.15, {}),
              ("t2", 124.62, {}), ("t2", 99.8, {}), ("launch", 46.5, {}), ("launch", 54.6, {})]

# reference 7 tiles, clockwise from top-left (TL, TM, TR, MR, BR, BM, BL, ML): long single shots, cut 960x540 for the zoom
R7_TILES = [("t2", 53.0), ("t1", 11.2), ("t2", 66.3), ("t2", 27.5), ("t2", 129.5), ("t2", 63.14), ("launch", 6.31),
            ("t2", 41.7)]

# "It was about what it really gave you." -- the scoopedfriday burst: 1-4 frame cuts, posterised and B&W flash frames,
# then one held shot into "Freedom."   (src, in, frames, grade)
BURST = [("pinB", 0.05, 2, "none"), ("t2", 140.3, 3, "none"), ("pinA", 0.35, 2, "none"), ("launch", 48.6, 3, "none"),
         ("t1", 25.6, 1, "poster"), ("pinB", 0.7, 2, "none"), ("t1", 25.62, 3, "none"), ("pinA", 2.35, 2, "none"),
         ("t2", 141.95, 3, "none"), ("pinB", 1.05, 2, "none"), ("t2", 138.3, 1, "bwhi"), ("t1", 36.0, 3, "none"),
         ("pinA", 4.7, 2, "none"), ("t2", 149.45, 3, "none"), ("pinB", 1.7, 2, "none"), ("launch", 73.6, 3, "none"),
         ("t2", 153.2, 1, "poster"), ("pinB", 2.3, 3, "none")]
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
        # v2 cut each beat at the word onsets nearest an even split; with the pauses shortened that rule can pick other
        # words, so a beat whose cuts the user has approved pins v2's words ("at")
        edges = ([t0] + [cut(i) if isinstance(i, int) else round(t0 + i * (t1 - t0), 3) for i in bt["at"]] + [t1]
                 if bt.get("at") else _edges(t0, t1, bt["a"], bt["b"], len(bt["shots"])))
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
SHOTS.append(S4("fr", "freedom", 0.3, cut(90), cut(91), push=(1.0, 1.04)))
SHOTS.append(S4("nmoney", "money", 0.9, NEWS_TM, NEWS_DUR))
SHOTS.append(S4("bd", "beatdrop", 0.43, T_BD, cut(3)))

# "With cheat codes like aspirin and panzer" -- the user's notebook clip (24 fps, 94 frames). "With cheat codes like": the
# desk (frames 0-35: the polaroids light up, the notebook opens), sped up so the open notebook is the last frame before
# "aspirin"; the clip's zoom into the page (36-41) is left out. "aspirin and" / "panzer": straight to the page, cut out of
# its black background and see-through over v2's footage for those words, the clip's own highlight on ASPIRINE (frames
# 53-61, held to 72) and PANZER (76-84, held to 93) drawn faster (tools/nb4.py -> nbpage.mp4; nbbg* are its backgrounds)
NB = {"t0": cut(121), "tp": cut(125), "tz": cut(127), "t1": cut(128)}
NB["desk_speed"] = round(35 * FPS / (24 * (int(round((NB["tp"] - NB["t0"]) * FPS)) - 1)), 4)
SHOTS.append(S4("nbdesk", "notebook", 0.0, NB["t0"], NB["tp"], speed=NB["desk_speed"]))
_e = _edges(NB["tp"], NB["tz"], 125, 126, 2)                    # v2's split of "aspirin and" between its two shots
SHOTS += [S4("nbbg0", "vc10", 53.95, _e[0], _e[1]), S4("nbbg1", "vcde", 44.4, _e[1], _e[2]),
          S4("nbbg2", "panzer", 100.0, NB["tz"], NB["t1"])]

# "an alternate reality." -- the user's chasing-dreams clip from its start, see-through (AR_DREAM), over the city: the
# "gta city" clip (stored sideways, turned upright) on its wide dusk aerial of the skyline and the Vice City blimp,
# zooming out (build4.ar_scene)
AR_DREAM = 0.5
SHOTS += [S4("arcity", "city", 0.0, *SPAN["ar"], crop=None, rot="ccw"), S4("ardream", "dreams", 0.0, *SPAN["ar"])]

# v2's ending: the GTA VI logo builds, then the date card
SHOTS += [S4("end1", "preload", 6.75, END_V, END_V + 1.35), S4("end2", "next", 1597.2, END_V + 1.35, TOTAL, grade="nopreorder")]
SHOTS.append(S4("tv2c", "wait5", 4.55, TV2["t0"], TV2["t1"], crop=(0, 600, 1080, 608)))  # the user: the people showing GTA V, not the line
SHOTS.append(S4("tv2v", "wait5", 4.55, TV2["t0"], TV2["t1"], crop=(177, 120, 726, 1200), card=(520, 860)))   # the same, upright, for the card

# "Driving supercars, firing guns, flying planes, and owning an entire city." -- the screen in four: each phrase's clip
# comes in as a glowing cut-out panel on its first word and stays to the end (build4.quad_scene). Shots picked from the
# GTA 6 folder: (src, in, out[, rot]); each panel's shots share its time at one speed (slow motion where they are short)
QW, QH, QM, QG = 906, 486, 54, 0                                  # panel size, outer margin, gap (the user: joined, no gap, floating)
QUAD = {"t0": cut(159), "ins": [cut(159), cut(161), cut(163), cut(165)],
        "xy": [(QM, QM), (QM + QW + QG, QM), (QM, QM + QH + QG), (QM + QW + QG, QM + QH + QG)]}
QPANELS = [
    [("launch", 46.30, 47.45), ("launch", 63.37, 64.20), ("t1", 32.60, 34.17)],          # supercars: red + green on Ocean Drive; the night chase; Ocean Drive at night
    [("launch", 72.10, 73.13), ("launch", 60.20, 61.03), ("launch", 71.40, 72.10), ("launch", 64.20, 65.58)],   # guns: Lucia firing; the firefight; the sniper; the pistol raised
    [("launch", 54.50, 56.40), ("launch", 38.40, 39.77)],                                # planes: the smoke-trail biplane over the beach; the jet over the runway
    [("city", 8.0, 10.2, "ccw")],                                                        # the city: the Vice City blimp over the skyline
]
QUAD["shots"] = []
for k, shots in enumerate(QPANELS):
    t_in = QUAD["ins"][k]
    span = SPAN["q4"][1] - t_in
    src_total = sum(sh[2] - sh[1] for sh in shots)
    if src_total > span:                                          # never faster than real time: trim the last shot instead
        last = shots[-1]
        shots[-1] = (last[0], last[1], round(last[2] - (src_total - span), 3)) + tuple(last[3:])
        src_total = span
    speed = round(src_total / span, 4)
    t, ids = t_in, []
    for j, sh in enumerate(shots):
        d = (sh[2] - sh[1]) / speed
        sid = f"q{k}{chr(97 + j)}"
        rot = sh[3] if len(sh) > 3 else None                      # an upright-turned source takes no crop (v2's is sideways)
        SHOTS.append(S4(sid, sh[0], sh[1], t, t + d, card=(QW, QH), speed=speed, rot=rot, crop=None if rot else "auto"))
        ids.append(sid)
        t += d
    QUAD["shots"].append(ids)
