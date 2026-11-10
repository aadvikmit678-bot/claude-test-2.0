#!/usr/bin/env python3
"""v4 derived stills: freeze frames, their cut-outs (local matting model), glowing white silhouettes and halos.

Each freeze is cut from its source with the same crop as tools/prep2.py uses for that source's clips, so a freeze
lines up exactly with the clip it interrupts.

  {name}_f.jpg     the frame (1920x1080)
  {name}_cut.png   the subject alone (npx hyperframes remove-background)
  {name}_sil.png   the subject as a cream-white silhouette with a soft glow (the Hemant Taneja / Pattinson look)
  {name}_halo.png  a soft white glow of the subject's shape, laid under the cut-out so it glows at the edges

Run:  python3 -I tools/prep4.py [--force]
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep2  # noqa: E402  (crop_expr, probe, V, FRAMES, run)

IMG = prep2.IMG
FREEZES = {  # name: (source key, time, framing)
    "stage": ("GAME", 75.85, "BBG"),   # under the stage lights, arms crossed (before the "Dimon Is Forever" title)
    "intv": ("BANK", 739.40, "BBG"),   # the sit-down interview, the frame it pauses on
}


def freeze(name, key, t, frame):
    out = f"{IMG}/{name}_f.jpg"
    src = f"{prep2.SRC}/{prep2.V[key]}"
    W, H = prep2.probe(src)
    cx, cy, z = prep2.FRAMES[frame]
    prep2.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
               "-vf", prep2.crop_expr(W, H, 1920, 1080, cx, cy, z), "-q:v", "2", out])
    return out


def cutout(name, frame_path):
    out = f"{IMG}/{name}_cut.png"
    prep2.run([("npx.cmd" if os.name == "nt" else "npx"), "--yes", "hyperframes@0.9.2", "remove-background", frame_path, "-o", out, "--json"])
    return out


def glows(name, cut_path):
    a = np.asarray(Image.open(cut_path).convert("RGBA"))[..., 3]
    A = Image.fromarray(a)
    soft = np.asarray(A.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32) / 255
    wide = np.asarray(A.filter(ImageFilter.GaussianBlur(34)), dtype=np.float32) / 255
    near = np.asarray(A.filter(ImageFilter.GaussianBlur(14)), dtype=np.float32) / 255
    h, w = a.shape
    # silhouette: a flat cream shape, feathered, with a wide soft glow around it
    sil_a = np.clip(np.maximum(soft, np.maximum(near * 0.85, wide * 0.6)), 0, 1)
    sil = np.zeros((h, w, 4), np.uint8)
    sil[..., 0], sil[..., 1], sil[..., 2] = 247, 241, 231
    sil[..., 3] = (sil_a * 255).astype(np.uint8)
    Image.fromarray(sil).save(f"{IMG}/{name}_sil.png", optimize=True)
    # halo: white glow of the shape (sits under the cut-out)
    halo_a = np.clip(np.maximum(near * 0.95, wide * 0.7), 0, 1)
    halo = np.zeros((h, w, 4), np.uint8)
    halo[..., 0:3] = 255
    halo[..., 3] = (halo_a * 255).astype(np.uint8)
    Image.fromarray(halo).save(f"{IMG}/{name}_halo.png", optimize=True)


GHOST_DIR = f"{prep2.SRC}/_globe"   # drop the user's globe picture here; it is used instead of the stand-in


def make_ghost(out=f"{IMG}/globe_ghost.jpg", W=1220, H=1080):
    """The S06 ghost (the Fink reel's Rogan screen): Dimon over a glowing globe, black and white, laid in difference
    blend at low opacity. The user's own globe picture is used when it is in dimon-src/_globe/; until then a stand-in
    is composed from his black-and-white photo (the user's Pinterest set) and a drawn globe."""
    import glob as _g
    mine = sorted(f for f in _g.glob(f"{GHOST_DIR}/*") if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
    if mine:
        im = Image.open(mine[0]).convert("L")
        r = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        im.crop((x0, y0, x0 + W, y0 + H)).save(out, quality=92)
        return out
    por = Image.open(f"{prep2.SRC}/money_pinterest videos/jamie black and white image.jpg").convert("L")
    ph = 800
    por = por.resize((round(por.width * ph / por.height), ph), Image.LANCZOS)
    canvas = np.zeros((H, W), np.float32)
    pa = np.asarray(por, np.float32) / 255
    px = (W - por.width) // 2 + 40
    canvas[0:ph, px:px + por.width] = pa
    # fade the photo's edges into black
    yy, xx = np.mgrid[0:H, 0:W]
    edge = np.clip((xx - px) / 90, 0, 1) * np.clip((px + por.width - xx) / 90, 0, 1) * np.clip((ph - yy) / 160, 0, 1)
    canvas *= edge
    # the globe: shaded sphere, graticule, city lights, rim light and halo
    cx, cy, R = W * 0.5, H * 0.80, 300.0
    dx, dy = (xx - cx) / R, (yy - cy) / R
    rr = dx * dx + dy * dy
    inside = rr < 1
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    L = np.array([-0.45, -0.55, 0.70]); L /= np.linalg.norm(L)
    lam = np.clip(dx * L[0] + dy * L[1] + nz * L[2], 0, 1)
    tilt = np.deg2rad(23)
    yr = dy * np.cos(tilt) - nz * np.sin(tilt)
    zr = dy * np.sin(tilt) + nz * np.cos(tilt)
    lat = np.arcsin(np.clip(-yr, -1, 1))
    lon = np.arctan2(dx, zr) + 0.6
    glat = np.abs(((np.rad2deg(lat) + 90) % 20) - 10)
    glon = np.abs(((np.rad2deg(lon) + 180) % 20) - 10)
    grid = np.clip(1 - np.minimum(glat, glon) / 0.9, 0, 1) * 0.35
    rng = np.random.RandomState(7)
    lights = np.zeros((H, W), np.float32)
    n = 1400
    lx = rng.uniform(-1, 1, n); ly = rng.uniform(-1, 1, n)
    keep = lx * lx + ly * ly < 0.92
    for a, b in zip(lx[keep], ly[keep]):
        x, y = int(cx + a * R), int(cy + b * R)
        if 0 <= x < W and 0 <= y < H:
            lights[y, x] = rng.uniform(0.5, 1.0)
    lights = np.asarray(Image.fromarray((lights * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),
                        np.float32) / 255 * 3
    sphere = (0.06 + 0.55 * lam ** 1.4 + grid * (0.4 + 0.6 * lam) + lights * (1 - lam) * 0.9)
    rim = np.clip(1 - np.abs(np.sqrt(rr) - 1) / 0.035, 0, 1) * 0.9
    halo = np.exp(-np.clip(np.sqrt(rr) - 1, 0, None) / 0.10) * 0.55 * (~inside)
    g = np.where(inside, sphere, 0) + rim + halo
    out_a = np.clip(np.where(inside, g, np.maximum(canvas, g)), 0, 1)
    Image.fromarray((out_a * 255).astype(np.uint8)).save(out, quality=92)
    return out


if __name__ == "__main__":
    force = "--force" in sys.argv
    make_ghost()
    for name, (key, t, frame) in FREEZES.items():
        if not force and os.path.exists(f"{IMG}/{name}_halo.png"):
            continue
        f = freeze(name, key, t, frame)
        c = cutout(name, f)
        glows(name, c)
        print(name, "done", flush=True)
