#!/usr/bin/env python3
"""counter-roll: the BlackRock edit's own code for this preset (../../lib), step by step. See PRESET.md.

With the BlackRock inputs this rebuilds the film's own files exactly (checked 2026-11-28: every frame identical).
For a new edit, change the inputs listed in PRESET.md in your copy of lib/ first.

    PRESET_ROOT=<project> PRESET_SRC=<its source media> python3 recipe.py            # every step
    python3 recipe.py count                                                    # one step

Without PRESET_ROOT it writes into this repo's blackrock-open project.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

import prep_v17  # noqa: E402

STEPS = [
    ("count", prep_v17.r_count3, "the counter with its white glow -> assets/clips/v17_count.mp4"),
]

if __name__ == "__main__":
    want = sys.argv[1:]
    for key, fn, what in STEPS:
        if not want or key in want:
            print(f"-- {key}: {what}", flush=True)
            fn()
