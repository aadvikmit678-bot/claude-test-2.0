#!/usr/bin/env python3
"""Prepare every media asset the Pattinson edit uses.

Trims, crops and scales source clips into assets/clips (H.264, 30 fps, no audio), copies and
resizes stills into assets/img, builds the paper texture and white silhouettes, prepares the
dialogue stings from Demucs vocal stems, normalises the VO and copies SFX.

Run:  python3 -I prep_media.py [clip-id ...]   (no ids = everything)
"""
import json, os, re, shutil, subprocess, sys
import numpy as np

ROOT = "/home/user/claude-test-2.0"
SRC = f"{ROOT}/pattinson-src"
PRJ = f"{ROOT}/pattinson-v5"
WORK = f"{ROOT}/pattinson-work"
CLIPS = f"{PRJ}/assets/clips"
IMG = f"{PRJ}/assets/img"
TEX = f"{PRJ}/assets/tex"
AUD = f"{PRJ}/assets/audio"
SFXSRC = f"{ROOT}/.claude/skills/media-use/audio/assets/sfx"
for d in (CLIPS, IMG, TEX, AUD, f"{AUD}/sfx"):
    os.makedirs(d, exist_ok=True)

V = {
    "SF": "Starting frame.mp4",
    "MON": "Montage of pattison.mp4",
    "GEN": "General montage.mp4",
    "BAT": "Montage + batman clip at 25thsec.mp4",
    "FACE": "Pattison face montage from multiple films.mp4",
    "M2": "Pattison montage 2.mp4",
    "PT": "Primetime.mp4",
    "CL": "Robert Pattison all movie clips with names on top right.mp4",
    "TW": "Watch Edward & Bella Fall in Love in Twilight.mp4",
    "KIM": "Robert Pattinson on Telling People He’s a Pathological Liar & Working with Zendaya on Three Films.mp4",
    "STORY": "Pattison story twilight.mp4",
    "CARPET": "Pattison News carpet walk.mp4",
    "FRAME": "Pattison photo frame. In centre.mp4",
    "VENICE": "Pattison raw video.mp4",
    "CRAZY": "Robert Pattison crazy batman edit.mp4",
    "TEN": "patison clear video wo text.mp4",
    "RUNUSER": "user-clips/run_clip.mp4",  # the user's Batman cut for "run" (v5)
    "TWNEW": "user-clips/twilight_new.mp4",  # the user's 1080p Twilight footage (v5 segment 2)
}

# id: (source key, in, duration, W, H, cx, cy, zoom, content-box [x,y,w,h] relative or None)
# cx/cy: centre of the crop window, relative to the content box. zoom >= 1 tightens the crop.
CLIP_SPECS = {
    # cold open: centre crop keeps the burned captions at frame centre so ours can cover them
    "c_start": ("SF", 0.00, 5.80, 1920, 1080, 0.5, 0.5, 1.0, None),
    # thesis
    "c_run": ("MON", 31.20, 1.30, 1920, 1080, 0.5, 0.5, 1.0, None),
    "c_kimmel_laugh": ("KIM", 211.2, 1.0, 1920, 1080, 0.5, 0.45, 1.0, None),
    # edward
    "c_bio": ("TW", 24.0, 1.6, 1920, 1080, 0.62, 0.5, 1.0, "LB"),
    "c_edward_cu": ("FACE", 7.45, 1.35, 1920, 1080, 0.5, 0.40, 1.0, None),
    # turn
    "c_sparkle": ("TW", 205.6, 1.6, 1920, 1080, 0.40, 0.5, 1.0, "LB"),
    # film run panels (384 wide)
    "p_goodtime": ("FACE", 8.9, 2.85, 384, 1080, 0.47, 0.5, 1.0, None),
    "p_lighthouse": ("FACE", 13.7, 1.95, 384, 1080, 0.45, 0.5, 1.0, None),
    "p_tenet": ("FACE", 11.9, 1.65, 384, 1080, 0.47, 0.5, 1.0, None),
    "p_batman": ("BAT", 29.85, 1.10, 384, 1080, 0.36, 0.5, 1.0, "LB"),
    "p_mickey": ("FACE", 17.15, 1.05, 384, 1080, 0.30, 0.5, 1.0, None),
    # swing
    "c_soot": ("SF", 20.55, 1.0, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_connie": ("CL", 24.8, 1.2, 1920, 1080, 0.62, 0.62, 1.30, None),
    "c_king": ("MON", 17.0, 0.55, 1920, 1080, 0.5, 0.5, 1.0, None),
    # jokes
    "c_sparkle2": ("TW", 209.4, 1.4, 1920, 1080, 0.40, 0.45, 1.0, "LB"),
    "c_spider": ("TW", 398.2, 2.6, 1920, 1080, 0.42, 0.5, 1.0, "LB"),
    # batman
    "c_cowl": ("BAT", 29.82, 1.15, 1920, 1080, 0.5, 0.5, 1.0, "LB"),
    "c_backhead": ("BAT", 27.40, 2.30, 1920, 1080, 0.5, 0.5, 1.0, "LB"),
    "c_gotham": ("BAT", 31.05, 1.85, 1920, 1080, 0.5, 0.5, 1.0, "LB"),
    # respect
    "c_fans": ("STORY", 20.4, 1.9, 1080, 1180, 0.5, 0.30, 1.0, None),
    "c_carpet": ("FRAME", 0.2, 3.8, 1080, 1520, 0.5, 0.42, 1.0, None),
    # triptych panels (640 wide)
    "t_odyssey": ("GEN", 8.1, 4.0, 640, 1080, 0.50, 0.5, 1.0, None),
    "t_prime": ("M2", 6.25, 2.5, 640, 1080, 0.36, 0.5, 1.0, None),
    "t_dune": ("GEN", 12.35, 0.95, 640, 1080, 0.47, 0.5, 1.0, None),
    # odyssey
    "c_antinous_fire": ("GEN", 8.05, 4.2, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_antinous_feast": ("SF", 7.85, 1.95, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_antinous_arch": ("SF", 5.85, 0.95, 1920, 1080, 0.5, 0.42, 1.0, None),
    # primetime (VHS)
    "c_prime_title": ("PT", 30.75, 2.3, 1920, 1080, 0.5, 0.43, 1.0, None),
    "c_hansen": ("M2", 6.25, 2.5, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_schedule": ("M2", 12.0, 1.15, 1920, 1080, 0.5, 0.5, 1.0, None),
    "c_stinghouse": ("M2", 3.35, 2.8, 1920, 1080, 0.5, 0.5, 1.0, None),
    "c_chat": ("M2", 10.02, 0.66, 1920, 1080, 0.5, 0.5, 1.0, None),
    "c_hiddencam": ("M2", 13.92, 0.56, 1920, 1080, 0.5, 0.5, 1.0, None),
    "c_strobeface": ("M2", 17.6, 1.0, 1920, 1080, 0.5, 0.45, 1.0, None),
    # dune
    "c_scytale": ("GEN", 12.35, 4.2, 1920, 1080, 0.5, 0.42, 1.0, None),
    # payoff split halves (960 wide)
    "h_edward": ("FACE", 7.45, 1.35, 960, 1080, 0.5, 0.5, 1.0, None),
    "h_batman": ("BAT", 29.85, 1.10, 960, 1080, 0.40, 0.5, 1.0, "LB"),
    # ---- v2: full-frame footage instead of paper and stills ----
    # twilight (Montage of pattison crops stay above its bottom watermark)
    "c_tw_lab": ("MON", 26.74, 0.45, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_tw_wed": ("MON", 1.94, 0.42, 1920, 1080, 0.5, 0.40, 1.0, None),
    "c_fans_full": ("STORY", 20.40, 0.55, 1920, 1080, 0.5, 0.30, 1.0, None),
    "c_tw_stare": ("TW", 148.55, 0.50, 1920, 1080, 0.36, 0.5, 1.0, "LB"),
    "c_tw_van": ("MON", 33.22, 0.70, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_tw_battle": ("MON", 50.65, 0.55, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_tw_glitch": ("TW", 207.40, 0.55, 1920, 1080, 0.40, 0.5, 1.0, "LB"),
    "c_tw_party": ("MON", 43.60, 0.70, 1920, 1080, 0.5, 0.45, 1.0, None),
    # film run, one full-frame shot per title
    "c_goodtime": ("FACE", 9.00, 1.05, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_lighthouse": ("FACE", 13.75, 1.10, 1920, 1080, 0.5, 0.42, 1.0, None),
    "c_tenet_a": ("MON", 2.85, 0.40, 1920, 1080, 0.5, 0.42, 1.0, None),
    "c_tenet_b": ("MON", 28.20, 0.50, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_batroof": ("CRAZY", 16.12, 0.66, 1920, 1080, 0.5, 0.5, 1.0, None),
    "c_mickey": ("MON", 33.95, 3.00, 1920, 1080, 0.5, 0.42, 1.0, None),
    # directors
    "c_rover": ("CL", 52.30, 0.95, 1920, 1080, 0.62, 0.62, 1.30, None),
    "c_lh_work": ("CL", 43.60, 0.40, 1920, 1080, 0.60, 0.62, 1.30, None),
    "c_nolan_set": ("STORY", 66.10, 1.20, 1920, 1080, 0.5, 0.16, 1.0, None),
    # respect
    "c_fans2": ("STORY", 21.00, 0.40, 1920, 1080, 0.5, 0.30, 1.0, None),
    "c_venice": ("VENICE", 4.00, 0.65, 1920, 1080, 0.5, 0.39, 1.0, None),
    "c_frame_cu": ("FRAME", 4.20, 0.85, 1920, 1080, 0.5, 0.37, 1.0, None),
    # odyssey
    "c_antinous_glasses": ("SF", 6.86, 0.45, 1920, 1080, 0.5, 0.42, 1.0, None),
    # primetime: the real "have a seat right there" moment, cropped above its burned caption
    "c_hansen_cu": ("M2", 0.05, 0.92, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_pt_worried": ("PT", 12.35, 0.66, 1920, 1080, 0.5, 0.45, 1.0, None),
    "c_seat1": ("PT", 0.25, 1.50, 1920, 1080, 0.47, 0.23, 1.22, None),
    "c_seat2": ("PT", 1.75, 0.66, 1920, 1080, 0.5, 0.5, 1.0, None),
    # payoff role switch (King -> Mickey 17 -> Devil All the Time -> Good Time)
    "c_roles": ("MON", 0.22, 1.00, 1920, 1080, 0.5, 0.42, 1.0, None),
    # ---- v3 (user notes) ----
    # opening: three fast real-life clips behind the one-line name
    "c_open1": ("VENICE", 1.20, 0.40, 1920, 1080, 0.5, 0.40, 1.0, None),
    "c_open2": ("FRAME", 0.30, 0.40, 1920, 1080, 0.5, 0.30, 1.0, None),
    "c_open3": ("KIM", 72.00, 0.40, 1920, 1080, 0.5, 0.45, 1.0, None),
    # "having a generational run": Batman glider over Gotham under the sliding slate strips
    "c_glider": ("MON", 30.02, 1.18, 1920, 1080, 0.5, 0.42, 1.0, None),
    "c_genbg": ("MON", 1.10, 1.55, 1920, 1080, 0.5, 0.42, 1.0, None),
    # "honestly": the same Kimmel laugh, from where it moves most
    "c_kimmel_laugh2": ("KIM", 211.65, 0.85, 1920, 1080, 0.5, 0.45, 1.0, None),
    # "respected actors in Hollywood": Venice arrival behind the popping portraits
    "c_carpet_bg": ("FRAME", 1.00, 2.90, 1920, 1080, 0.5, 0.30, 1.0, None),
    # ---- v5 ----
    # the Kimmel laugh at its native 1280x720 (no enlargement), shown as a card
    "c_kimmel_card": ("KIM", 211.65, 0.85, 1280, 720, 0.5, 0.45, 1.0, None),
    # "run": the fast stretch of the user's clip (afterburner, speedometer, Batman driving, chase POV); a slight
    # zoom drops the small watermark at the bottom of the chase shots
    "c_run2": ("RUNUSER", 1.05, 1.0, 1920, 1080, 0.5, 0.44, 1.1, None),
    # ---- v5 segment 2 (10.85-23.41): "To some people ... the vampire kid." ----
    "c_twn_hall": ("TWNEW", 24.30, 0.95, 1920, 1080, 0.5, 0.5, 1.0, None),     # he'll always be: Edward turns
    "c_twn_warm": ("TWNEW", 96.80, 1.25, 1920, 1080, 0.5, 0.5, 1.0, None),     # Edward Cullen.: warm close-up
    "c_twn_eyes": ("TWNEW", 107.45, 0.70, 1920, 1080, 0.5, 0.5, 1.0, None),    # But everything: gold eyes
    "c_twn_walk": ("TWNEW", 137.30, 0.70, 1920, 1080, 0.5, 0.5, 1.0, None),    # he did after: the walk
    "c_twn_forest": ("TWNEW", 204.05, 0.55, 1920, 1080, 0.5, 0.45, 1.0, None), # more than just
    "c_ven_hair": ("VENICE", 2.55, 0.62, 1920, 1080, 0.5, 0.377, 1.0, None),   # making sure (below the Gala mark)
    "c_ven_crowd": ("VENICE", 14.00, 0.45, 1920, 1080, 0.9, 0.258, 1.35, None),  # the world (right of the mark)
    "p_carpet_a": ("CARPET", 1.85, 0.55, 640, 1080, 0.5, 0.42, 1.0, None),     # sees him: three premiere panels
    "p_carpet_b": ("CARPET", 3.10, 0.55, 640, 1080, 0.5, 0.42, 1.0, None),
    "p_carpet_c": ("CARPET", 9.95, 0.55, 640, 1080, 0.5, 0.42, 1.0, None),
}

# the 2026 slate cut into its four film strips (y0, y1 in the 1350x1688 still)
SLATE_STRIPS = {"slate_drama": (0, 416), "slate_odyssey": (416, 831), "slate_prime": (831, 1264),
                "slate_dune": (1264, 1688)}

# stills pulled from video (id: source, time, W, H, cx, cy, zoom, content-box)
FRAME_SPECS = {
    "f_belami": ("CL", 63.4, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_rover": ("CL", 53.0, 1920, 1080, 0.60, 0.62, 1.30, None),
    "f_queen": ("CL", 49.6, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_lostcity": ("CL", 76.0, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_damsel": ("CL", 41.6, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_king": ("CL", 15.0, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_devil": ("CL", 8.5, 1920, 1080, 0.60, 0.62, 1.30, None),
    "f_heron": ("CL", 30.0, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_dali": ("CL", 18.4, 1920, 1080, 0.55, 0.62, 1.30, None),
    "f_kimmel_scytale": ("KIM", 663.0, 1920, 1080, 0.5, 0.5, 1.0, None),
    "f_edward_cu": ("FACE", 8.1, 1920, 1080, 0.5, 0.40, 1.0, None),
    "f_cedric": ("FACE", 6.6, 1920, 1080, 0.5, 0.45, 1.0, None),
    "f_mickey_two": ("FACE", 17.7, 1920, 1080, 0.5, 0.45, 1.0, None),
    "f_scytale": ("FACE", 3.7, 1920, 1080, 0.5, 0.42, 1.0, None),
    "f_hansen": ("FACE", 5.2, 1920, 1080, 0.5, 0.42, 1.0, None),
    "f_bruce": ("FACE", 1.5, 1920, 1080, 0.5, 0.45, 1.0, None),
    "f_drama": ("FACE", 16.4, 1920, 1080, 0.5, 0.40, 1.0, None),
    "f_twn_vamp": ("TWNEW", 26.30, 1920, 1080, 0.5, 0.5, 1.0, None),  # the vampire kid plate (v5)
}

STILLS = {
    # id: source path relative to SRC, max side
    "hero": "solo-portraits/solo-portraits-90.jpg",
    "slate": "Instagram photo (eatmovies).jpg",
    "tw_cast": "twilight-edward-cullen/twilight-edward-cullen-01.jpg",
    "tw_poster": "twilight-edward-cullen/twilight-edward-cullen-10.jpg",
    "tw_trio": "twilight-edward-cullen/twilight-edward-cullen-13.jpg",
    "tw_tree1": "twilight-edward-cullen/twilight-edward-cullen-03.jpg",
    "tw_tree2": "twilight-edward-cullen/twilight-edward-cullen-08.jpg",
    "tw_kiss": "twilight-edward-cullen/twilight-edward-cullen-02.jpg",
    "tw_prom": "twilight-edward-cullen/twilight-edward-cullen-06.jpg",
    "tw_poster2": "twilight-edward-cullen/twilight-edward-cullen-12.jpg",
    "tw_newmoon": "twilight-edward-cullen/twilight-edward-cullen-16.jpg",
    "tw_car": "twilight-edward-cullen/twilight-edward-cullen-04.jpg",
    "bw1": "Pattison as Bruce wayne photo 1.jpg",
    "bw2": "Pattison as Bruce wayne photo 2.jpg",
    "bw3": "Pattison as Bruce wayne photo 3.jpg",
    "nolan": "the-odyssey-antinous/the-odyssey-antinous-47.jpg",
    "od_poster": "the-odyssey-antinous/the-odyssey-antinous-11.jpg",
    "od_poster2": "the-odyssey-antinous/the-odyssey-antinous-22.jpg",
    "pat5": "pat image 5.jpg",
    "pat4": "pat image 4.jpg",
    "pat1": "pat image 1.jpg",
    "solo01": "solo-portraits/solo-portraits-01.jpg",
    "solo04": "solo-portraits/solo-portraits-04.jpg",
    "solo06": "solo-portraits/solo-portraits-06.jpg",
    "solo02": "solo-portraits/solo-portraits-02.jpg",
    "solo03": "solo-portraits/solo-portraits-03.jpg",
    "solo05": "solo-portraits/solo-portraits-05.jpg",
    "solo07": "solo-portraits/solo-portraits-07.jpg",
    "solo08": "solo-portraits/solo-portraits-08.jpg",
    "pt_pink": "primetime/primetime-02.jpg",
    "pt_poster": "primetime/primetime-11.jpg",
    "dune_scy": "dune/dune-56.jpg",
    "dune_scy2": "dune/dune-52.jpg",
    "dune_poster": "dune/dune-11.jpg",
    "gt_neon": "good-time/good-time-01.jpg",
    "gt_blue": "good-time/good-time-03.jpg",
    "gt_red": "good-time/good-time-08.jpg",
    "gt_purple": "good-time/good-time-09.jpg",
    "lh_soot": "the-lighthouse/the-lighthouse-08.jpg",
    "lh_duo": "the-lighthouse/the-lighthouse-05.jpg",
    "lh_portrait": "the-lighthouse/the-lighthouse-04.jpg",
    "tn_desert": "tenet/tenet-07.jpg",
    "tn_red": "tenet/tenet-05.jpg",
    "tn_walk": "tenet/tenet-08.jpg",
    "bt_red": "the-batman/the-batman-01.jpg",
    "bt_fire": "the-batman/the-batman-02.jpg",
    "bt_cowl": "the-batman/the-batman-09.jpg",
    "bt_bruce": "the-batman/the-batman-07.jpg",
    "bt_signal": "the-batman/the-batman-11.jpg",
    "mk_helmet": "mickey-17/mickey-17-08.jpg",
    "mk_two": "mickey-17/mickey-17-07.jpg",
    "mk_naomi": "mickey-17/mickey-17-06.jpg",
    "mk_portal": "mickey-17/mickey-17-09.jpg",
    "pt_overhead": "primetime/primetime-03.jpg",
    "pt_blue": "primetime/primetime-01.jpg",
    "pt_smile": "primetime/primetime-06.jpg",
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-1500:]}")
    return r


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height", "-of", "csv=p=0", path]).stdout.strip().split(",")
    return int(out[0]), int(out[1])


def detect_letterbox(path, t, dur):
    """Return (x, y, w, h) of the picture area inside black bars."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-ss", str(t), "-t", str(max(dur, 0.6)), "-i", path,
                        "-vf", "cropdetect=limit=24:round=2:reset=0", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", r.stderr)
    if not m:
        W, H = probe(path)
        return 0, 0, W, H
    w, h, x, y = map(int, m[-1])
    return x, y, w, h


def crop_expr(W, H, box, Wt, Ht, cx, cy, zoom):
    bx, by, bw, bh = box
    A = Wt / Ht
    if bw / bh > A:
        h = bh; w = bh * A
    else:
        w = bw; h = bw / A
    w /= zoom; h /= zoom
    x = bx + cx * bw - w / 2
    y = by + cy * bh - h / 2
    x = min(max(x, bx), bx + bw - w)
    y = min(max(y, by), by + bh - h)
    w, h, x, y = int(w) // 2 * 2, int(h) // 2 * 2, int(x), int(y)
    return f"crop={w}:{h}:{x}:{y},scale={Wt}:{Ht}:flags=lanczos,setsar=1"


def make_clip(cid):
    key, t, dur, Wt, Ht, cx, cy, zoom, lb = CLIP_SPECS[cid]
    src = f"{SRC}/{V[key]}"
    W, H = probe(src)
    box = detect_letterbox(src, t, dur) if lb == "LB" else (0, 0, W, H)
    vf = crop_expr(W, H, box, Wt, Ht, cx, cy, zoom) + ",fps=30,format=yuv420p"
    out = f"{CLIPS}/{cid}.mp4"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-t", f"{dur:.3f}",
         "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-g", "15",
         "-movflags", "+faststart", out])
    return out


def make_frame(fid):
    key, t, Wt, Ht, cx, cy, zoom, lb = FRAME_SPECS[fid]
    src = f"{SRC}/{V[key]}"
    W, H = probe(src)
    box = detect_letterbox(src, t, 0.6) if lb == "LB" else (0, 0, W, H)
    vf = crop_expr(W, H, box, Wt, Ht, cx, cy, zoom)
    out = f"{IMG}/{fid}.jpg"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
         "-vf", vf, "-q:v", "2", out])
    return out


def make_still(sid):
    src = f"{SRC}/{STILLS[sid]}"
    out = f"{IMG}/{sid}.jpg"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src, "-vf",
         "scale='if(gt(iw,ih),min(2200,iw),-2)':'if(gt(iw,ih),-2,min(2200,ih))':flags=lanczos", "-q:v", "2", out])
    return out


def make_slate_strips():
    for sid, (y0, y1) in SLATE_STRIPS.items():
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{IMG}/slate.jpg", "-vf",
             f"crop=1350:{y1 - y0}:0:{y0}", "-q:v", "2", f"{IMG}/{sid}.jpg"])


def make_paper():
    W, H = 1920, 1080
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
    r = np.sqrt((nx / 1.05) ** 2 + (ny / 0.95) ** 2)
    t = np.clip((r - 0.35) / 0.85, 0, 1) ** 1.6
    c0 = np.array([238, 228, 224], np.float32)
    c1 = np.array([222, 213, 209], np.float32)
    img = c0[None, None, :] * (1 - t[..., None]) + c1[None, None, :] * t[..., None]
    rng = np.random.default_rng(7)
    fib = rng.normal(0, 1, (H, W)).astype(np.float32)
    # stretch noise horizontally into fibres
    k = np.ones(9, np.float32) / 9
    fib = np.apply_along_axis(lambda row: np.convolve(row, k, mode="same"), 1, fib)
    img += fib[..., None] * 3.2
    img = np.clip(img, 0, 255).astype(np.uint8)
    raw = f"{WORK}/paper.rgb"
    img.tofile(raw)
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-i", raw, f"{TEX}/paper.png"])
    os.remove(raw)


def make_silhouette(cut_png, out_png):
    """White silhouette from a cutout's alpha (for the 2-frame silhouette flash)."""
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", cut_png, "-vf",
         "format=rgba,geq=r=255:g=255:b=255:a='alpha(X,Y)'", out_png])


def make_audio():
    sep = f"{WORK}/sep/out/htdemucs"
    # VO, normalised to about -16 LUFS
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{SRC}/robert patison video audio.mp3",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", f"{AUD}/vo.wav"])
    # stings from Demucs vocal stems (music removed), gently levelled to the VO
    stings = {
        "sting-beggars": (f"{sep}/start/vocals.wav", 0.0, 5.55, 0.02, 0.18),
        "sting-spider": (f"{sep}/spider/vocals.wav", 0.0, 2.35, 0.02, 0.15),
        "sting-seat": (f"{sep}/prime/vocals.wav", 0.25, 2.15, 0.03, 0.20),
    }
    for name, (src, ss, dur, fi, fo) in stings.items():
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(ss), "-t", str(dur), "-i", src,
             "-af", f"highpass=f=70,afade=t=in:d={fi},afade=t=out:st={dur - fo}:d={fo},"
                    f"loudnorm=I=-17:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", f"{AUD}/{name}.wav"])


def make_vo2():
    """The v5 voiceover (pattinson_new_audio.mp3), normalised to about -16 LUFS."""
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{WORK}/vo2/new_vo.mp3",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", f"{AUD}/vo2.wav"])


def make_soft_glitch():
    """A short, band-limited TV blip from the bundled glitch-1: only the transient (0.5 s), static above
    4.5 kHz and rumble below 180 Hz removed, faded out. Replaces the long screeching glitch tails."""
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{SFXSRC}/glitch-1.mp3", "-t", "0.5",
         "-af", "highpass=f=180,lowpass=f=4500,afade=t=in:d=0.01,afade=t=out:st=0.3:d=0.2,volume=0.6",
         "-ar", "48000", "-ac", "2", f"{AUD}/sfx/tv-blip-soft.wav"])


def copy_sfx():
    for f in os.listdir(SFXSRC):
        if f.endswith(".mp3"):
            shutil.copy(f"{SFXSRC}/{f}", f"{AUD}/sfx/{f}")
    if os.path.exists(f"{SFXSRC}/CREDITS.md"):
        shutil.copy(f"{SFXSRC}/CREDITS.md", f"{AUD}/sfx/CREDITS.md")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    def want(k):
        return not only or k in only
    for cid in CLIP_SPECS:
        if want(cid):
            make_clip(cid); print("clip", cid)
    for fid in FRAME_SPECS:
        if want(fid):
            make_frame(fid); print("frame", fid)
    for sid in STILLS:
        if want(sid):
            make_still(sid); print("still", sid)
    if want("slate_strips"):
        make_slate_strips(); print("slate strips")
    if want("paper"):
        make_paper(); print("paper")
    if want("cutouts"):
        cut = f"{WORK}/rbtest/pat5-cut.png"
        shutil.copy(cut, f"{IMG}/pat5-cut.png")
        print("cutouts")
    if want("audio"):
        make_audio(); print("audio")
    if want("sfx"):
        copy_sfx(); print("sfx")
    if want("vo2"):
        make_vo2(); print("vo2")
    if want("sfx") or want("soft_glitch"):
        make_soft_glitch(); print("soft glitch")
