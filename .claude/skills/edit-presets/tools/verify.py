"""Run a preset's steps from the skill's lib/ into a scratch project and compare every output with the BlackRock
project's own file (needs blackrock-src/ and dimon-src/, which are not in git, and numpy, opencv, pillow, ffmpeg).

Run from the skill folder: python3 tools/verify.py <preset>        (PRESET_VERIFY_DIR picks the scratch folder)
2026-11-28: all seven presets printed "PSNR inf" (frame-identical) for every clip, "max diff 0" for every image and
"identical" for every scene file."""
import filecmp
import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
LIB = os.path.join(REPO, ".claude", "skills", "edit-presets", "lib")
ORIG = os.path.join(REPO, "blackrock-open")
VROOT = os.environ.get("PRESET_VERIFY_DIR") or tempfile.mkdtemp(prefix="preset-verify-")   # a scratch project
for d in ("assets/clips", "assets/img", "compositions"):
    os.makedirs(f"{VROOT}/{d}", exist_ok=True)
if not os.path.exists(f"{VROOT}/assets/fonts"):
    os.symlink(f"{ORIG}/assets/fonts", f"{VROOT}/assets/fonts")
for clip in ("v6_rest2.mp4", "v5_rogan.mp4"):      # inputs made by other steps of the film
    if not os.path.exists(f"{VROOT}/assets/clips/{clip}"):
        os.symlink(f"{ORIG}/assets/clips/{clip}", f"{VROOT}/assets/clips/{clip}")
os.environ.update(PRESET_ROOT=VROOT, PRESET_SRC=f"{REPO}/blackrock-src", PRESET_REPO=REPO)
sys.path.insert(0, LIB)

STEPS = {   # preset -> [(module, function)], [outputs relative to the project]
    "powerful-man-rise": ([("prep_v10", "fink_cut2"), ("prep_v10", "fink_plates3"), ("prep_v10", "r_wall5"),
                           ("prep_v16", "r_open"), ("prep_v17", "r_bgs"), ("build", "s_first")],
                          ["assets/img/v10_fink_cut.png", "assets/img/v12_bg_b.jpg", "assets/img/v15_bg_wall.jpg",
                           "assets/clips/v15_wall.mp4", "assets/clips/v16_wall.mp4", "assets/img/v17_bg_wall.jpg",
                           "assets/img/v17_bg_b.jpg", "compositions/s_first.html"]),
    "name-mosaic": ([("prep_v9", "r_mosaic"), ("build", "s_name")],
                    ["assets/clips/v9_mosaic.mp4", "compositions/s_name.html"]),
    "built-red-word": ([("prep_v10", "r_company2"), ("prep_v10", "r_built"), ("build", "s_hook")],
                       ["assets/clips/v15_company.mp4", "assets/clips/v10_built.mp4", "compositions/s_hook.html"]),
    "founder-squares": ([("prep_v10", "r_founders2")],
                        ["assets/clips/v3_r1_jensen.mp4", "assets/clips/v3_r1_gates.mp4", "assets/clips/v3_r1_jobs.mp4"]),
    "counter-roll": ([("prep_v17", "r_count3")], ["assets/clips/v17_count.mp4"]),
    "crisis-date-grid": ([("prep_v17", "r_date2"), ("prep_v17", "r_grid2"), ("prep_v16", "r_gov"), ("build", "s_crisis")],
                         ["assets/clips/v17_date.mp4", "assets/clips/v17_grid.mp4", "assets/clips/v16_gov.mp4",
                          "compositions/s_crisis.html"]),
    "money-handoff": ([("prep_v17", "r_money2"), ("build", "s_money")],
                      ["assets/clips/v17_money.mp4", "compositions/s_money.html"]),
}


def compare(rel):
    a, b = f"{VROOT}/{rel}", f"{ORIG}/{rel}"
    if not os.path.exists(a):
        return "MISSING (not written)"
    if rel.endswith(".html"):
        return "identical" if filecmp.cmp(a, b, shallow=False) else "DIFFERS"
    if rel.endswith(".mp4"):
        r = subprocess.run(["ffmpeg", "-i", a, "-i", b, "-lavfi", "[0:v][1:v]psnr", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        m = re.search(r"average:(\S+)", r)
        n = lambda p: subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                      "stream=nb_read_frames", "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
        return f"PSNR {m.group(1) if m else '?'} dB, frames {n(a)} vs {n(b)}"
    import numpy as np
    from PIL import Image
    x = np.asarray(Image.open(a)).astype(int)
    y = np.asarray(Image.open(b)).astype(int)
    if x.shape != y.shape:
        return f"DIFFERENT SIZE {x.shape} vs {y.shape}"
    d = np.abs(x - y)
    return f"max diff {d.max()}, mean {d.mean():.3f}"


if __name__ == "__main__":
    import importlib
    preset = sys.argv[1]
    steps, outs = STEPS[preset]
    for mn, fn in steps:
        print(f"-- {mn}.{fn}", flush=True)
        getattr(importlib.import_module(mn), fn)()
    print(f"== {preset}")
    for rel in outs:
        print(f"   {rel}: {compare(rel)}")
