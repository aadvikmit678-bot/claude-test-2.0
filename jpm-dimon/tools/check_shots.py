#!/usr/bin/env python3
"""Report every registered clip whose source range [t, t+dur] crosses a cut in the source (ffmpeg scene score).

Run: python3 -I tools/check_shots.py media_v3.json [threshold]
A clip that crosses a cut flashes a frame of the wrong shot; move its in-point or shorten it."""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

PRJ = "/home/user/claude-test-2.0/jpm-dimon"
SRC = "/home/user/claude-test-2.0/dimon-src"
sys.path.insert(0, f"{PRJ}/tools")
V = {}
exec(open(f"{PRJ}/tools/prep2.py").read().split("FRAMES = ")[0].split("V = ", 1)[1].join(["V = ", ""]) if False else "", {})
src_txt = open(f"{PRJ}/tools/prep2.py").read()
V = eval(src_txt.split("\nV = ", 1)[1].split("\n}\n", 1)[0] + "\n}")
spec = json.load(open(f"{PRJ}/tools/{sys.argv[1] if len(sys.argv) > 1 else 'media_v3.json'}"))
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.32


def cuts(cid, c):
    path = f"{SRC}/{V[c['key']]}"
    t, d = c["t"], c["dur"]
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-ss", f"{max(0, t - 0.05):.3f}", "-t", f"{d + 0.05:.3f}", "-i", path,
                        "-vf", f"scale=320:-2,select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    hits = [round(float(m) + max(0, t - 0.05), 2) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    hits = [h for h in hits if t + 0.04 < h < t + d - 0.25]   # cuts inside the part that is shown (the tail is padding)
    return cid, c, hits


with ThreadPoolExecutor(max_workers=4) as ex:
    for cid, c, hits in ex.map(lambda kv: cuts(*kv), spec["clips"].items()):
        if hits:
            print(f"{cid:34s} {c['key']:6s} t={c['t']:8.2f} dur={c['dur']:5.2f}  cut at {hits}")
print("checked", len(spec["clips"]))
