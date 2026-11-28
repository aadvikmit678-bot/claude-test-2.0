"""Trimmed from blackrock-open/tools/prep_v3.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import sys

from common import *  # noqa: F401,F403

V3 = f"{DL}/v3"

# ------------------------------------------------------------------ 6. the reel's "the man behind OpenAI" device
def live(src, t0, n, crop=None, fc=False, u8=False):
    """n frames at 60 fps from a clip (optionally a crop filter), as float RGB 1920x1080 (uint8 with u8: a quarter of
    the memory, for devices that hold many sources at once)."""
    vf = (crop + "," if crop else "") + "setsar=1"
    ss = t0 + (stream_start(src) if fc else 0.0)
    got = grab(src, ss, n, fps=FPS, vf=vf, size=(W, H))
    return got if u8 else [f.astype(np.float32) for f in got]
