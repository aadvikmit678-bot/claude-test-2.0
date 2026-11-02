#!/usr/bin/env python3
"""Remove the burned-in white captions from the cold-open clip (c_start.mp4).

The captions are static overlays while the footage moves, so for each caption state the
pixels that stay bright in (almost) every frame of that state are the text. Those pixels,
dilated to cover the drop shadow, are inpainted frame by frame (OpenCV Telea).
"""
import subprocess, sys
import numpy as np
import cv2

SRC = "/home/user/claude-test-2.0/pattinson/assets/clips/c_start.mp4"
OUT = "/home/user/claude-test-2.0/pattinson/assets/clips/c_start_clean.mp4"
W, H, FPS = 1920, 1080, 30
BAND = (470, 628, 330, 1590)  # y0, y1, x0, x1 search band for the captions

raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", SRC, "-f", "rawvideo",
                      "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()
n = len(frames)
y0, y1, x0, x1 = BAND

def white_mask(f):
    b = f[y0:y1, x0:x1].astype(np.int16)
    mn = b.min(axis=2); mx = b.max(axis=2)
    return (mn > 212) & ((mx - mn) < 40)

masks = [white_mask(f) for f in frames]
counts = np.array([m.sum() for m in masks])

# group frames into caption states: consecutive frames whose white masks overlap strongly
def iou(a, b):
    i = (a & b).sum(); u = (a | b).sum()
    return i / u if u else 0.0

groups = []
cur = [0]
for i in range(1, n):
    if counts[i] > 300 and counts[cur[-1]] > 300 and iou(masks[i], masks[cur[-1]]) > 0.72:
        cur.append(i)
    else:
        groups.append(cur); cur = [i]
groups.append(cur)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
# windows the automatic chaining misses (camera shake breaks the frame-to-frame overlap):
# Venice "BEGGARS" frames 31-39 and the wide-shot part of "OUT OF HERE" frames 40-45
MANUAL = [list(range(31, 40)), list(range(40, 46))]
covered = set(i for g in MANUAL for i in g)
groups = [g for g in groups if not (set(g) & covered)] + MANUAL
report = []
# manual windows: mask every frame on its own, limited to the caption rectangle
RECT = (488, 602, 640, 1290)  # y0, y1, x0, x1 in frame pixels
for g in MANUAL:
    for i in g:
        m = white_mask(frames[i])
        full = np.zeros((H, W), np.uint8)
        full[y0:y1, x0:x1] = m.astype(np.uint8) * 255
        lim = np.zeros_like(full); lim[RECT[0]:RECT[1], RECT[2]:RECT[3]] = 255
        full = np.minimum(full, lim)
        sh = np.zeros_like(full)
        for dx in range(0, 15, 3):
            for dy in range(0, 15, 3):
                sh = np.maximum(sh, np.roll(np.roll(full, dy, axis=0), dx, axis=1))
        full = cv2.dilate(np.maximum(full, sh), kernel, iterations=1)
        frames[i] = cv2.inpaint(frames[i], full, 6, cv2.INPAINT_TELEA)
    report.append((round(g[0] / FPS, 2), round((g[-1] + 1) / FPS, 2), RECT[2], RECT[3], RECT[0], RECT[1]))
for g in groups:
    manual = g in MANUAL
    if manual:
        continue
    if len(g) < 2 or (not manual and counts[g].mean() < 300):
        continue
    stack = np.stack([masks[i] for i in g])
    stable = stack.mean(axis=0) >= (0.75 if manual else 0.9)   # bright in most of the state's frames
    if stable.sum() < 200:
        continue
    ys0, xs0 = np.where(stable)
    cxs = (xs0.min() + xs0.max()) / 2 + x0
    if abs(cxs - 960) > 120:          # captions are centred; anything else is background
        continue
    full = np.zeros((H, W), np.uint8)
    full[y0:y1, x0:x1] = stable.astype(np.uint8) * 255
    # cover the soft dark drop shadow, offset down-right of the white fill
    sh = np.zeros_like(full)
    for dx in range(0, 15, 3):
        for dy in range(0, 15, 3):
            sh = np.maximum(sh, np.roll(np.roll(full, dy, axis=0), dx, axis=1))
    full = cv2.dilate(np.maximum(full, sh), kernel, iterations=1)
    for i in g:
        frames[i] = cv2.inpaint(frames[i], full, 6, cv2.INPAINT_TELEA)
    ys, xs = np.where(full > 0)
    report.append((round(g[0] / FPS, 2), round((g[-1] + 1) / FPS, 2), int(xs.min()), int(xs.max()),
                   int(ys.min()), int(ys.max())))

for r in report:
    print("state t=%.2f-%.2f  bbox x %d-%d  y %d-%d" % r)

p = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                      "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                      "-crf", "16", "-pix_fmt", "yuv420p", "-g", "15", "-movflags", "+faststart", OUT],
                     stdin=subprocess.PIPE)
p.stdin.write(frames.tobytes()); p.stdin.close(); p.wait()
print("wrote", OUT, n, "frames")
