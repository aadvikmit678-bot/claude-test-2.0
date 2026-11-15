"""v3: every beat gets its own treatment (Pattinson-edit vocabulary + Tesla captions + Palmer/WeWork layouts).

SHOTS feed prep.py (EDL=edl3); LAYERS and LINES feed build3.py. Times are on the final timeline.
"""
import os
from edl import W, cut, N, VO_OFFSET, NEWS_DUR, SRC, CROP, PROJ, ROOT, FPS, NEWS_IN, WT

TOTAL = 107.6                           # v3 runs 1.1 s longer than v2 (edl.TOTAL)

SHOTS, LAYERS = [], []
_n = {}


def _id(p):
    _n[p] = _n.get(p, 0) + 1
    return f"{p}{_n[p]:02d}"


def clip(prefix, src, sin, t0, t1, w=None, h=None, crop="auto", grade="none", speed=1.0):
    sid = _id(prefix)
    if crop == "auto":
        crop = CROP.get(src)
    SHOTS.append(dict(id=sid, src=src, sin=sin, start=round(t0, 3), end=round(t1, 3), fit="card" if w else "cover",
                      crop=crop, grade=grade, speed=speed, reverse=False, card=(w, h) if w else None, push=None))
    return sid


def full(src, sin, t0, t1, crt=False, push=None, **kw):
    sid = clip("f", src, sin, t0, t1, **kw)
    LAYERS.append(dict(kind="full", id=sid, t0=t0, t1=t1, crt=crt, push=push))


def seq(t_edges, shots, crt=False):
    """Full-frame shots cut at the given edges: shots = [(src, sin, {opts}), ...]."""
    for k, sh in enumerate(shots):
        opt = sh[2] if len(sh) > 2 else {}
        full(sh[0], sh[1], t_edges[k], t_edges[k + 1], crt=crt, **opt)


def rects(kind, t1, items, **extra):
    """items: (src, sin, t_in, x, y, w, h, {opts}) -> one layer of rectangles that build in."""
    els = []
    t_all = min(it[2] for it in items)
    for it in items:
        src, sin, tin, x, y, w, h = it[:7]
        opt = it[7] if len(it) > 7 else {}
        # every panel plays from the layout's first frame; it lights up on its own word (t_in)
        sid = clip("r", src, sin, t_all if kind != "cards" else tin, t1, w=w, h=h, **{k: v for k, v in opt.items() if k != "rot"})
        els.append(dict(id=sid, t_in=tin, x=x, y=y, w=w, h=h, rot=opt.get("rot", 0)))
    LAYERS.append(dict(kind=kind, els=els, t0=min(e["t_in"] for e in els), t1=t1, **extra))


BW, DIM = {"grade": "bw"}, {"grade": "dim"}

# ================================================================== cold open
full("news", NEWS_IN, 0.0, NEWS_DUR, crop=(0, 0, 1280, 720))
LAYERS[-1]["news"] = True
full("awshit", 0.0, NEWS_DUR, VO_OFFSET, crt=True, crop=(107, 0, 1707, 960))

# ================================================================== A
seq([VO_OFFSET, cut(1), cut(3)], [("nyc", 0.3), ("wait5", 1.6)])
WALL = [("millions", 0.4, BW), ("nyc", 9.0, {}), ("t1", 21.95, {}), ("adult", 1.0, {}), ("wait5", 2.15, {}), ("preload", 17.95, {}),
        ("t2", 99.8, {}), ("launch", 46.5, {}), ("montage2", 1.0, {}), ("wait5", 4.45, {}), ("nlook", 2.1, {}), ("t1", 29.05, {})]
wall_ids = [clip("w", s, i, cut(3), cut(6), w=600, h=338, **o) for s, i, o in WALL]
LAYERS.append(dict(kind="wall", ids=wall_ids, t0=cut(3), t1=cut(6)))
seq([cut(6), cut(9), cut(11)], [("wait5", 8.05), ("eyes", 3.62)])
full("next", 1570.9, cut(11), cut(13), push=(1.04, 1.12), **DIM)
seq([cut(13), cut(16), cut(18)], [("t1", 24.95), ("preload", 6.6)])
seq([cut(18), cut(20), cut(22)], [("nlook", 16.6), ("launch", 68.0)])

# ================================================================== B  (2013 GTA V | 2026 GTA VI)
rects("split", cut(25), [("nostalgia", 0.1, cut(22), 0, 0, 960, 1080), ("t1", 2.85, W(23) - 0.05, 960, 0, 960, 1080)],
      labels=[("2013", 0, cut(22) + 0.05), ("2026", 1, W(23))])
full("t1", 35.85, cut(25), cut(27), push=(1.08, 1.0), **DIM)
seq([cut(27), cut(29), cut(31)], [("money", 0.9), ("money", 2.7)])
seq([cut(31), cut(32), cut(33)], [("blade", 2.95), ("t1", 30.1)])

# ================================================================== C  (three release dates, three strips)
seq([cut(33), cut(36), cut(38)], [("launch", 20.6), ("t2", 45.4)])
rects("strips", cut(47), [("t2", 52.0, cut(38), 0, 0, 640, 1080), ("nlook", 12.9, cut(40), 640, 0, 640, 1080),
                          ("t2", 147.4, cut(46), 1280, 0, 640, 1080)],
      labels=[("2025", 0, W(38)), ("May|2026", 1, W(40)), ("November", 2, W(46))])

# ================================================================== D  (floating cards: nobody moved on)
rects("cards", cut(55), [("nyc", 4.3, cut(47), 560, 250, 800, 450),
                         ("wait5", 1.6, cut(47) + 0.10, 120, 120, 340, 191, {"rot": -4}),
                         ("waitgta6", 7.2, cut(47) + 0.17, 1460, 140, 340, 191, {"rot": 5}),
                         ("metav3rse", 3.0, cut(49), 150, 720, 340, 191, {"rot": 3}),
                         ("nyc", 8.1, cut(49) + 0.08, 1430, 740, 340, 191, {"rot": -5}),
                         ("wait5", 4.45, cut(50), 840, 830, 300, 169, {"rot": 2})])
seq([cut(55), cut(56) + 0.1, cut(57)], [("eyes", 3.62), ("eyes", 4.42)])

# ================================================================== F
seq([cut(57), cut(61)], [("wait5", 11.2)])
full("wait5", 13.6, cut(61), cut(64), crt=True)
seq([cut(64), cut(67), cut(69)], [("vox", 3.3), ("blade", 0.05)])
seq([cut(69), cut(71), cut(72), cut(73)], [("t2", 9.9), ("next", 492.5), ("nlook", 6.85)])

# ================================================================== G  (cars | guns)
seq([cut(73), cut(75), cut(77), cut(79)], [("t1", 70.4), ("t2", 34.7), ("blade", 14.3)])
rects("split", cut(82), [("t1", 32.7, cut(79), 0, 0, 960, 1080), ("launch", 72.15, cut(81), 960, 0, 960, 1080)],
      labels=[("cars", 0, W(79)), ("guns.", 1, W(81))], serif=True)

# ================================================================== H  (Freedom)
seq([cut(82), cut(86), cut(88), cut(90)], [("t1", 19.3, DIM), ("t1", 5.05), ("launch", 62.6)])
full("freedom", 0.3, cut(90), cut(91) + 0.12, push=(1.0, 1.05))

# ================================================================== I  (rewind to 2002, the family computer)
full("freedom", 0.3, cut(91) + 0.12, cut(94), grade="dim", speed=3.0)
LAYERS[-1]["rewind"] = True
SHOTS[-1]["reverse"] = True
full("goodbye", 0.25, cut(94), cut(97))
full("waitgta6", 0.6, cut(97), cut(104), crt=True)
seq([cut(104), cut(105), cut(107)], [("waitgta6", 2.6), ("vc10", 23.5)], crt=True)
seq([cut(107), cut(110), cut(113), cut(115)], [("vc10", 29.4), ("vcde", 11.7), ("panzer", 30.0)], crt=True)
LAYERS.append(dict(kind="osd_volume", t0=W(109) - 0.05, t1=cut(115), steps=(W(110), W(114) + 0.15)))
seq([cut(115), cut(118), cut(119), cut(121)], [("vc10", 36.9), ("vcde", 37.75), ("vcde", 48.9)], crt=True)

# ================================================================== J  (cheat codes on the TV)
seq([cut(121), cut(127), cut(128)], [("panzer", 5.0), ("panzer", 100.0)], crt=True)
seq([cut(128), cut(131), cut(135)], [("panzer", 121.0), ("vc10", 58.95)], crt=True)

# ================================================================== K
seq([cut(135), cut(138), cut(141), cut(143)], [("kidlake", 0.5), ("vc10", 28.25), ("vcde", 15.3)])
seq([cut(143), cut(146), cut(148)], [("escape", 0.2), ("escape", 2.75, DIM)])
seq([cut(148), cut(150), cut(151)], [("escape", 7.35), ("escape", 8.45, DIM)])

# ================================================================== L  (2x2 grid building)
seq([cut(151), cut(155), cut(158), cut(159)], [("t1", 37.6), ("launch", 66.5), ("vcde", 52.7)])
rects("grid4", cut(165), [("launch", 25.6, cut(159), 0, 0, 960, 540), ("launch", 59.4, cut(161), 960, 0, 960, 540),
                          ("t2", 139.8, cut(163), 0, 540, 960, 540), ("next", 996.5, cut(164) + 0.2, 960, 540, 960, 540)],
      labels=[("Driving|supercars,", 0, W(159)), ("firing|guns,", 1, W(161)), ("flying|planes,", 2, W(163))])
seq([cut(165), cut(168), cut(170)], [("next", 1129.0), ("city", 24.0)])

# ================================================================== M
seq([cut(170), cut(175), cut(179), cut(181)], [("emontage", 6.25), ("launch", 32.25), ("vcde", 7.85)])
seq([cut(181), cut(183) + 0.1, cut(186)], [("t1", 63.7), ("nlook", 11.7)])
seq([cut(186), cut(187), cut(188)], [("t2", 118.05), ("launch", 60.2)])
seq([cut(188), cut(193), cut(195)], [("t1", 68.8), ("montage", 7.6)])
rects("split", cut(203), [("nyc", 8.1, cut(195), 0, 0, 960, 1080), ("t1", 27.6, cut(199), 960, 0, 960, 1080)],
      labels=[])

# ================================================================== N
seq([cut(203), cut(208), cut(212)], [("goodbye", 2.4), ("goodbye", 18.3)])
seq([cut(212), cut(213), cut(217)], [("adult", 0.7, BW), ("adult", 3.0, BW)])
seq([cut(217), cut(219), cut(222)], [("adult", 6.1, BW), ("millions", 2.0, BW)])
seq([cut(222), cut(226), cut(229), cut(232)], [("t1", 11.2), ("t2", 83.2), ("montage", 25.4)])

# ================================================================== O
full("next", 1571.4, cut(232), cut(236), push=(1.0, 1.08), **DIM)
seq([cut(236), cut(239), cut(241)], [("vc10", 11.05, DIM), ("vcde", 5.7, DIM)])
full("t1", 39.9, cut(241), cut(243), push=(1.0, 1.06))
rects("split", cut(249), [("vc10", 16.65, cut(243), 0, 0, 960, 1080), ("t1", 2.85, cut(245), 960, 0, 960, 1080)],
      labels=[("2002", 0, W(243)), ("2026", 1, W(245))])

# ================================================================== P
seq([cut(249), cut(253), cut(259)], [("metav3rse", 3.0), ("nostalgia", 5.5)])
full("nostalgia", 27.5, cut(259), cut(261), speed=0.6)
full("next", 769.0, cut(261), cut(266))
seq([cut(266), cut(267), cut(268)], [("next", 781.0, {"speed": 0.7}), ("t1", 35.85)])

# ================================================================== Q
full("kidlake", 9.2, cut(268), cut(271))
seq([cut(271), cut(273), cut(274), cut(275)], [("vc10", 48.8), ("vcde", 13.7), ("vc10", 25.2)], crt=True)
seq([cut(275), cut(277), cut(278)], [("waitgta6", 12.0), ("wait5", 15.7)])
seq([cut(278), cut(281)], [("wait5", 12.7)])
full("wait5", 13.7, cut(281), cut(284), crt=True)
seq([cut(284), cut(287), 103.85], [("nlook", 17.5), ("freedom", 3.0)])
full("next", 1580.6, 103.85, 105.0)
full("next", 1570.9, 105.0, TOTAL, push=(1.0, 1.04), **DIM)
LAYERS[-1]["endcard"] = True

SECTIONS = [  # composition id, start, end
    ("news", 0.0, NEWS_DUR), ("cj", NEWS_DUR, VO_OFFSET), ("sa", VO_OFFSET, cut(22)), ("sb", cut(22), cut(33)),
    ("sc", cut(33), cut(47)), ("sd", cut(47), cut(57)), ("sf", cut(57), cut(73)), ("sg", cut(73), cut(82)),
    ("sh", cut(82), cut(91) + 0.12), ("si", cut(91) + 0.12, cut(121)), ("sj", cut(121), cut(135)), ("sk", cut(135), cut(151)),
    ("sl", cut(151), cut(170)), ("sm", cut(170), cut(203)), ("sn", cut(203), cut(232)), ("so", cut(232), cut(249)),
    ("sp", cut(249), cut(268)), ("sq", cut(268), TOTAL),
]
