"""Link this repository's copies of the source footage under the file names tools/edl.py's SRC expects.

The desktop session read its sources from next to tools/ under their original Drive names; in this repository
they live in gta6-src/_drive/ (short names, gitignored) and dimon-src/. Run once per machine:
    python -I GTA6-v3/tools/link_sources.py [ROOT]      (ROOT defaults to GTA6-v3/)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import edl

D = os.path.join(REPO, "gta6-src", "_drive")
LOCAL = {   # SRC alias -> file in this repository
    "news": "billion.mp4", "awshit": "awshit.mp4", "t1": "trailer1.mp4", "t2": "trailer2.mp4", "launch": "launch1.mp4",
    "nlook": "netflix.mp4", "preload": "preload.mp4", "next": "netflix4k.mp4", "vc10": "vc10.mp4", "vcde": "vcde.mp4",
    "panzer": "vcpanzer.mp4", "kidlake": "kidcine.mp4", "millions": "millions.mp4", "freedom": "freedom.mp4",
    "escape": "escape.mp4", "adult": "adultrush.mp4", "goodbye": "gta5bye.mp4", "waitgta6": "waiting.mp4",
    "wait5": "realwait.mp4", "nostalgia": "gta5nost.mp4", "nyc": "willnyc.mp4", "vox": "vox.mp4", "eyes": "ahhshit.mp4",
    "city": "city.mp4", "montage": "montage.mp4", "montage2": "montage2.mp4", "emontage": "editmontage.mp4",
    "em6": "editm6.mp4", "edits": "edits.mp4", "blade": "blade.mp4", "oldchars": "oldchars.mp4", "metav3rse": "metav3rse.mp4",
}
EXTRA = {"money": os.path.join(REPO, "dimon-src", "_pin", "p07_Try_these_11_Classy_side_hus.mp4")}
LOCAL.update({"ajit": "madebyajit.mp4", "leno": "lenojoga.mp4"})        # v4 (tools/edl4.py)
SRC = dict(edl.SRC, ajit="Video by madebyajit [0-29s].mp4", leno="Video by lenojoga [0-15s].mp4")
missing = []
for alias, name in SRC.items():
    target = EXTRA.get(alias) or os.path.join(D, LOCAL.get(alias, "?"))
    link = os.path.join(ROOT, name)
    if not os.path.exists(target):
        missing.append((alias, target)); continue
    os.makedirs(os.path.dirname(link), exist_ok=True)
    if os.path.islink(link) or os.path.exists(link):
        continue
    os.symlink(os.path.relpath(target, os.path.dirname(link)), link)
print(f"linked {len(SRC) - len(missing)} sources under {ROOT}" + (f"; missing: {missing}" if missing else ""))
