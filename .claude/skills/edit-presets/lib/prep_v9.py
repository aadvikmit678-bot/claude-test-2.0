"""Trimmed from blackrock-open/tools/prep_v9.py for the edit-presets skill: only the code the presets use,
copied as it is (comments included). See SKILL.md for the paths this reads and writes."""

import json

import sys

from common import *  # noqa: F401,F403

import timing as TM

V9 = f"{DL}/v9"

D = os.path.abspath(f"{REPO}/dimon-src")

DOCS = f"{DL}/v6/docs"

SRCS = {
    "FIN": f"{DL}/fink_interview.mp4", "LFI": f"{DL}/lf_interview2.mp4", "FSP": f"{DL}/fink_speaking.mp4",
    "BRL": f"{DOCS}/br_largest.mp4", "BRE": f"{DOCS}/br_edit.mp4", "BR15": f"{DOCS}/br_15t_machine.mp4",
    "BRC": f"{DOCS}/br_conspiracies.mp4", "MBS": f"{DL}/m_blackrock_start.mp4", "PANEL": PANEL,
    "X": f"{DL}/v3/br_explainer.mp4", "FI": f"{D}/_direct/fired_push_scene.mp4", "TS": f"{DL}/v3/thinkschool.mp4",
    "HOW": f"{D}/_direct/how_jpm_became_largest.mp4", "GE": f"{DL}/good_edit_42s.mp4",
}

def nf(a, b):
    return round(b * FPS) - round(a * FPS)

def jumps(frames_, thr=38.0):
    """indices where the picture changes abruptly (a hidden cut inside a span)"""
    out = []
    for i in range(1, len(frames_)):
        a = cv2.resize(frames_[i - 1], (64, 36)).astype(np.float32)
        b = cv2.resize(frames_[i], (64, 36)).astype(np.float32)
        if np.abs(a - b).mean() > thr:
            out.append(i)
    return out

# ------------------------------------------------------------------ 3. "Larry Fink, the CEO of BlackRock."
# The Hemant video's name device (5.4-8.7 s, read every 0.1 s): a mosaic takes over the frame -- one big tile in the
# middle, three small ones down each side, every tile arriving as a white card for a frame or two and then playing a
# different clip of him; the name sits over the middle in the serif with a bloom (the whole frame washes out for two
# frames as it lands), then his title builds word by word in the grotesque while the tiles keep changing. Ours: Fink's
# clips, and on "BlackRock" every tile flips to BlackRock's own buildings. (The type is in the composition.)
SRCS.update({"MF": f"{DL}/m_finance.mp4", "BRS": f"{DL}/blackrock_short.mp4", "FK2": f"{DL}/m_fink2.mp4"})

MG = 6

MOSAIC_RECTS = {                     # tile -> (x, y, w, h)
    "C": (480, 0, 960, 1080),
    "L1": (0, 0, 480, 360), "L2": (0, 360, 480, 360), "L3": (0, 720, 480, 360),
    "R1": (1440, 0, 480, 360), "R2": (1440, 360, 480, 360), "R3": (1440, 720, 480, 360),
}

# tile -> its clips in turn: (first frame, source, start s, crop centre x, y, crop width)
MOSAIC_FINK = {
    "C": [(0, "FIN", 11.00, 1310, 540, 900), (49, "BRL", 422.00, 890, 592, 836)],
    "L1": [(4, "LFI", 9.20, 880, 380, 900)],
    "R3": [(8, "PANEL", 1187.30, 900, 400, 820)],
    "L3": [(12, "BRL", 22.40, 820, 425, 860)],
    "R1": [(16, "MBS", 10.45, 470, 315, 620), (62, "LFI", 12.00, 880, 380, 900)],
    "L2": [(20, "FSP", 11.00, 360, 235, 640)],
    "R2": [(24, "BRE", 247.60, 600, 420, 1000), (88, "FSP", 14.00, 360, 235, 640)],
}

MOSAIC_BR = {                        # from "BlackRock": (delay in frames, source, start s, cx, cy, crop width)
    "C": (0, "X", 174.70, 960, 540, 960),
    "L1": (2, "BRL", 122.50, 760, 590, 1300), "R1": (3, "BR15", 213.70, 900, 560, 1300),
    "L2": (4, "MF", 11.20, 958, 560, 1300), "R2": (5, "BRL", 588.50, 860, 560, 1300),
    "L3": (6, "BRS", 4.65, 512, 288, 760), "R3": (7, "BRS", 0.00, 512, 290, 760),
}

def crop_clip(key, t0, n, cx, cy, span, tw, th):
    src = SRCS[key]
    w, h, _ = probe(src)
    fr = grab(src, t0, n, fps=FPS)
    ch = span * th / tw
    x0 = int(min(max(cx - span / 2, 0), max(0, w - span)))
    y0 = int(min(max(cy - ch / 2, 0), max(0, h - ch)))
    out = [grade(cv2.resize(im[y0:int(y0 + ch), x0:int(x0 + span)], (tw, th), interpolation=cv2.INTER_AREA),
                 sat=0.92, contrast=1.08) for im in fr]
    j = jumps(fr)
    if j:
        print(f"   !! {key}@{t0}: picture jumps at frames {j} (of {len(fr)})")
    while len(out) < n:
        out.append(out[-1])
    return out

def r_mosaic():
    a0, a1 = TM.B["name"]
    n = nf(a0, a1)                                           # 150
    t0 = round(a0 * FPS)
    k_larry = round((TM.T["larry"] - 0.03) * FPS) - t0       # the name lands here: the frame washes out just before
    k_br = round((TM.T["blackrock"] - 0.03) * FPS) - t0      # every tile flips to BlackRock from here
    segs = {}
    for tile, lst in MOSAIC_FINK.items():
        x, y, w, h = MOSAIC_RECTS[tile]
        tw, th = w - MG, h - MG
        out = []
        for j, (f0, key, ts, cx, cy, span) in enumerate(lst):
            f1 = lst[j + 1][0] if j + 1 < len(lst) else k_br
            out.append((f0, f1, crop_clip(key, ts, f1 - f0, cx, cy, span, tw, th)))
        d, key, ts, cx, cy, span = MOSAIC_BR[tile]
        out.append((k_br + d, n, crop_clip(key, ts, n - k_br - d, cx, cy, span, tw, th)))
        segs[tile] = out
    wash = {k_larry - 2: 0.55, k_larry - 1: 0.85, k_larry: 0.35}          # the bloom as the name lands
    wr = Writer(f"{CLIPS}/v9_mosaic.mp4")
    for i in range(n):
        fr = np.full((H, W, 3), 10, np.float32)
        for tile, (x, y, w, h) in MOSAIC_RECTS.items():
            tw, th = w - MG, h - MG
            cur = None
            for f0, f1, clip in segs[tile]:
                if f0 <= i < f1:
                    cur = (f0, clip)
            if cur is None:
                # between its Fink clip and its BlackRock clip a tile holds its last frame
                prev = [sg for sg in segs[tile] if sg[1] <= i]
                if not prev:
                    continue
                img = prev[-1][2][-1]
            else:
                f0, clip = cur
                img = np.full((th, tw, 3), 246, np.float32) if i - f0 < 3 else clip[min(i - f0, len(clip) - 1)]
            fr[y + MG // 2:y + MG // 2 + th, x + MG // 2:x + MG // 2 + tw] = img
        k = wash.get(i, 0.0)
        if k:
            fr = fr * (1 - k) + 255 * k
        wr.write(fr)
    wr.close()
    print(f"   mosaic: {n} frames; the name at {k_larry}, BlackRock at {k_br}")

SRCS.update({"GATES": f"{DL}/v3/bill_gates.mp4", "JOBS": f"{DL}/v3/steve_jobs.mp4",
             "JENSEN": f"{V9}/jensen_reel.mp4"})
