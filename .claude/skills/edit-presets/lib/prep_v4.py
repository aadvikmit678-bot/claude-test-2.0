"""Trimmed from blackrock-open/tools/prep_v4.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import math

import subprocess

import sys

import cv2

import numpy as np

import prep_v3 as P

from common import CLIPS, DL, FPS, H, PANEL, W, Writer, center_focus, cover, grab, grain

V3 = P.V3

PIN = f"{V3}/pin"

# ------------------------------------------------------------------ the founders block: texture + corner blur
TEX = f"{PIN}/money_tex.mp4"

def texture_pass(name, opacity=0.16, seed=0):
    """The money texture (the user's "can be used in difference effect in bg, less opacity") over a clip, in
    difference at low opacity, and the soft corner blur."""
    path = f"{CLIPS}/{name}.mp4"
    src = grab(path, 0.0, 400)
    tex = grab(TEX, 1.0 + seed * 0.7, len(src), fps=FPS, size=(W, H)) if opacity > 0 else []
    tmp = f"{CLIPS}/{name}.tex.mp4"
    wr = Writer(tmp)
    for i, f in enumerate(src):
        f = f.astype(np.float32)
        if opacity > 0:
            t = tex[min(i, len(tex) - 1)].astype(np.float32)
            f = f * (1 - opacity) + np.abs(f - t) * opacity
        f = center_focus(f, zoom=0.014, gblur=2.4)
        wr.write(f)
    wr.close()
    subprocess.run(["mv", tmp, path], check=True)
    print(f"   {name}: texture + corner blur ({len(src)} frames)")
