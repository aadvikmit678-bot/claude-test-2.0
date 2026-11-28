#!/usr/bin/env python3
"""crisis-date-grid: the BlackRock edit's own code for this preset (../../lib), step by step. See PRESET.md.

With the BlackRock inputs this rebuilds the film's own files exactly (checked 2026-11-28: every frame identical).
For a new edit, change the inputs listed in PRESET.md in your copy of lib/ first.

    PRESET_ROOT=<project> PRESET_SRC=<its source media> python3 recipe.py            # every step
    python3 recipe.py date                                                    # one step

Without PRESET_ROOT it writes into this repo's blackrock-open project.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))

import build, prep_v16, prep_v17  # noqa: E402

STEPS = [
    ("date", prep_v17.r_date2, "the year frame -> assets/clips/v17_date.mp4"),
    ("grid", prep_v17.r_grid2, "the grid -> assets/clips/v17_grid.mp4"),
    ("gov", prep_v16.r_gov, "the next shots with a datamosh at their cuts -> assets/clips/v16_gov.mp4"),
    ("scene", build.s_crisis, "places the three clips -> compositions/s_crisis.html"),
]

if __name__ == "__main__":
    want = sys.argv[1:]
    for key, fn, what in STEPS:
        if not want or key in want:
            print(f"-- {key}: {what}", flush=True)
            fn()
