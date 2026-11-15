"""The pictures for the pin board ("back to the world they once dreamed of living in."): edl4.PB_RAPID (one a frame)
and edl4.PB_TILT (the tilted prints), grabbed at 1.6x their board size (the board starts zoomed in 1.75x).
Writes gta6-edit/assets/img/pb/r00.jpg ... and t0.jpg ...   usage: python -I tools/pb4.py
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edl4 as E

REPO = os.path.dirname(os.path.dirname(HERE))
HERO = os.path.join(REPO, "gta6-src", "v4ref", "hero")
D = os.path.join(E.PROJ, "assets", "img", "pb")
os.makedirs(D, exist_ok=True)
K = 1.6


def grab(name, src, t, w, h):
    W, H = int(round(w * K / 2) * 2), int(round(h * K / 2) * 2)
    if src in ("hero1b", "hero2"):
        path, pre, seek = os.path.join(HERO, src + ".jpg"), "", []
    else:
        path = os.path.normpath(os.path.join(E.ROOT, E.SRC[src]))
        c = E.CROP.get(src)
        pre = f"crop={c[2]}:{c[3]}:{c[0]}:{c[1]}," if c else ""
        seek = ["-ss", f"{t:.3f}"]
    vf = f"{pre}scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},eq=contrast=1.05:saturation=1.06"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + seek + ["-i", path, "-frames:v", "1", "-vf", vf, "-q:v", "3",
                    os.path.join(D, name + ".jpg")], check=True)


for k, (src, t, w, h) in enumerate(E.PB_RAPID):
    grab(f"r{k:02d}", src, t, w, h)
for k, (src, t, w, h, _r) in enumerate(E.PB_TILT):
    grab(f"t{k}", src, t, w, h)
print("pb:", len(E.PB_RAPID), "rapid,", len(E.PB_TILT), "tilted ->", D)
