#!/usr/bin/env python3
"""powerful-man-rise: the BlackRock edit's own code for this preset (../../lib), step by step. See PRESET.md.

With the BlackRock inputs this rebuilds the film's own files exactly (checked 2026-11-28: every frame identical).
For a new edit, change the inputs listed in PRESET.md in your copy of lib/ first.

    PRESET_ROOT=<project> PRESET_SRC=<its source media> python3 recipe.py            # every step
    python3 recipe.py cutout                                                    # one step

Without PRESET_ROOT it writes into this repo's blackrock-open project.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

import build, prep_v10, prep_v16, prep_v17  # noqa: E402

STEPS = [
    ("cutout", prep_v10.fink_cut2, "the person's cut-out on the 2200x1238 canvas -> assets/img/v10_fink_cut.png"),
    ("plates", prep_v10.fink_plates3, "the two background plates -> assets/img/v12_bg_a.jpg, v12_bg_b.jpg"),
    ("wall", prep_v10.r_wall5, "the photo wall -> assets/clips/v15_wall.mp4 (+ v15_bg_wall.jpg, v15_fink_white.png)"),
    ("false", prep_v16.r_open, "the false-colour frames of the rise's first state -> assets/clips/v16_wall.mp4"),
    ("plates2", prep_v17.r_bgs, "the plates without the screen lines -> assets/img/v17_bg_wall.jpg, v17_bg_b.jpg"),
    ("scene", build.s_first, "the scene (rise, drift, words, flash) -> compositions/s_first.html"),
]

if __name__ == "__main__":
    want = sys.argv[1:]
    for key, fn, what in STEPS:
        if not want or key in want:
            print(f"-- {key}: {what}", flush=True)
            fn()
