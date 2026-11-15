"""The cheat-code notebook page for "aspirin and" / "panzer" (the user's clip Kid_viewing_notebook_cheat_codes, 24 fps).

The page is cut out of its black background and laid see-through over v2's footage for those words (the prepped shots
nbbg0 / nbbg1 = "aspirin and", nbbg2 = "panzer"): the paper at PAPER opacity, the writing and the clip's own white
highlight kept solid. The clip draws the highlight over ASPIRINE in frames 53-61 (held to 72) and over PANZER in 76-84
(held to 93); here each is drawn in 4 frames (about 2.5x faster) and then held. The cut to the page and the cut at
"panzer" are straight cuts; the clip's zoom into the page is not used.
Writes gta6-edit/assets/clips/nbpage.mp4.
usage: python -I tools/nb4.py [paper_opacity] [--stills j,j,...]      (after EDL=edl4 python -I tools/prep.py)
"""
import os, subprocess, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl4 as E

args = [a for a in sys.argv[1:] if not a.startswith("--")]
PAPER = float(args[0]) if args else 0.55        # the paper's opacity over the footage
STILLS = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--stills=")), None)
GRADE = "eq=contrast=1.04:saturation=1.03"      # prep.py's "none" grade, as every other shot
CLIPS = os.path.join(E.PROJ, "assets", "clips")
SRC = os.path.normpath(os.path.join(E.ROOT, E.SRC["notebook"]))
W_, H_ = 1920, 1080
FIRST, LAST = 52, 93                             # page frames used (52: the page before any highlight)


def decode(path, vf):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vf", vf, "-fps_mode", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H_, W_, 3)


page = decode(SRC, f"select=between(n\\,{FIRST}\\,{LAST}),{GRADE}")
assert len(page) == LAST - FIRST + 1, len(page)
bgs = [decode(os.path.join(CLIPS, f"nbbg{k}.mp4"), "null") for k in range(3)]

# the paper's own brightness, from frame 52 (no highlight yet): a median over the page at quarter size
K15 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
K5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))


def page_mask(L):
    m = (L > 100).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, K15)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    m = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)       # the page: the largest bright part
    inv = (1 - m).astype(np.uint8)
    n2, lab2 = cv2.connectedComponents(inv, connectivity=4)
    edge = np.unique(np.concatenate([lab2[0], lab2[-1], lab2[:, 0], lab2[:, -1]]))
    m[(inv > 0) & ~np.isin(lab2, edge)] = 1                                            # fill the writing back in
    return cv2.erode(m, K5)


L0 = cv2.cvtColor(page[0], cv2.COLOR_RGB2GRAY)
m0 = page_mask(L0)
Lf = L0.copy()
Lf[m0 == 0] = int(np.median(L0[m0 > 0]))
LP = cv2.resize(cv2.medianBlur(cv2.resize(Lf, (480, 270), interpolation=cv2.INTER_AREA), 21), (W_, H_),
                interpolation=cv2.INTER_LINEAR).astype(np.float32)
_alpha = {}


def alpha(f):
    if f not in _alpha:
        img = page[f - FIRST]
        L = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mf = cv2.GaussianBlur(page_mask(L).astype(np.float32), (0, 0), 1.3)
        Lw = L.astype(np.float32)
        ink = np.clip((LP - Lw - 10) / 55, 0, 1)            # the pen (and the ruled lines, a little)
        glow = np.clip((Lw - LP - 8) / 35, 0, 1)            # the clip's white highlight
        _alpha[f] = mf * (PAPER + (1 - PAPER) * np.maximum(ink, glow))
    return _alpha[f]


tp, tz, t1 = E.NB["tp"], E.NB["tz"], E.NB["t1"]
tm = next(s["start"] for s in E.SHOTS if s["id"] == "nbbg1")
jm, ja, jend = round((tm - tp) * E.FPS), round((tz - tp) * E.FPS), round((t1 - tp) * E.FPS)
n_out = jend + 5                                             # a few frames of handle, as prep.py's clips


def src_frame(j):
    if j < ja:                                               # ASPIRINE: drawn in 4 frames, held to frame 72
        return 53 + 2 * j if j < 4 else 61 + int(11.999 * (j - 4) / max(1, ja - 4))
    u = j - ja                                               # PANZER: drawn in 4 frames, held to frame 93
    return 76 + 2 * u if u < 4 else min(LAST, 84 + int(9.999 * (u - 4) / max(1, jend - ja - 4)))


def bg_frame(j):
    k, i = (0, j) if j < jm else ((1, j - jm) if j < ja else (2, j - ja))
    return bgs[k][min(i, len(bgs[k]) - 1)]


def frame(j):
    f = src_frame(j)
    a = alpha(f)[..., None]
    return (a * page[f - FIRST].astype(np.float32) + (1 - a) * bg_frame(j).astype(np.float32) + 0.5).astype(np.uint8)


if STILLS:
    out_dir = os.path.join(os.environ.get("NB_STILLS", "/tmp"), f"nb_{PAPER:.2f}")
    os.makedirs(out_dir, exist_ok=True)
    for j in (int(x) for x in STILLS.split(",")):
        cv2.imwrite(os.path.join(out_dir, f"j{j:02d}_f{src_frame(j)}.png"), cv2.cvtColor(frame(j), cv2.COLOR_RGB2BGR))
    print("stills", out_dir)
    sys.exit(0)

out = os.path.join(CLIPS, "nbpage.mp4")
enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W_}x{H_}",
                        "-r", str(E.FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "15",
                        "-keyint_min", "15", "-sc_threshold", "0", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
                       stdin=subprocess.PIPE)
for j in range(n_out):
    enc.stdin.write(frame(j).tobytes())
enc.stdin.close()
assert enc.wait() == 0
print(f"nbpage: {n_out} frames | page {PAPER:.2f} | split {jm} | panzer {ja} | end {jend} | page frames",
      [src_frame(j) for j in range(n_out)])
