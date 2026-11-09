#!/usr/bin/env python3
"""assets/tex/paper_light.png: the lit paper behind the black-word beats, borrowed from the Pattinson v5 edit.

The same generator as make_paper_light() in pattinson-v5/tools/prep_media.py (branch claude/pattinson-v5-notes5):
paper lit by a window (the Hemant Taneja reference at 0:13). Deterministic: with ffmpeg 6.1 the PNG is byte-identical
to the committed copy (git blob e38093a8, md5 63a1d9e9949ef55d94a8598a73c4c33a).

Run:  python3 -I tools/rebuild/paper_light.py
"""
import os, subprocess, tempfile
import numpy as np

OUT = "/home/user/claude-test-2.0/jpm-dimon/assets/tex/paper_light.png"


def window_light(W=1920, H=1080, base=(122, 117, 114), beam=(238, 228, 223), seed=11):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    x0, y0, x1, y1 = 330.0, 120.0, 1760.0, 1060.0          # the beam's axis
    dx, dy = x1 - x0, y1 - y0
    L = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / L, dx / L
    d = (xx - x0) * nx + (yy - y0) * ny                     # signed distance from the axis
    along = ((xx - x0) * dx + (yy - y0) * dy) / L           # position along the axis
    half, soft = 360.0, 230.0
    t = np.clip((half + soft - np.abs(d)) / soft, 0, 1)
    t = t * t * (3 - 2 * t)                                 # smoothstep edge
    t *= 0.78 + 0.22 * np.clip(along / L, 0, 1)             # the light gets stronger toward the lower right
    for c, w, k in ((0.47, 46.0, 0.16), (0.73, 30.0, 0.09)):  # window-frame shadows across the band
        bar = np.exp(-((along - c * L) / w) ** 2)
        t *= 1 - k * bar
    base, beam = np.array(base, np.float32), np.array(beam, np.float32)
    img = base[None, None, :] * (1 - t[..., None]) + beam[None, None, :] * t[..., None]
    vx, vy = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
    vig = 1 - 0.16 * np.clip((vx * vx + vy * vy - 0.25) / 1.75, 0, 1)
    img *= vig[..., None]
    rng = np.random.default_rng(seed)
    fib = rng.normal(0, 1, (H, W)).astype(np.float32)
    k9 = np.ones(9, np.float32) / 9
    fib = np.apply_along_axis(lambda row: np.convolve(row, k9, mode="same"), 1, fib)
    img += fib[..., None] * 2.6 * (np.array(base).mean() / 120.0)
    return np.clip(img, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    img = window_light()
    H, W, _ = img.shape
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".rgb", delete=False) as f:
        img.tofile(f.name)
    try:
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", f"{W}x{H}", "-i", f.name, OUT], check=True)
    finally:
        os.remove(f.name)
    print(OUT)
