#!/usr/bin/env python3
"""Prepare every media asset the Jamie Dimon edit uses.

Trims, crops and scales source clips into assets/clips (H.264, 30 fps, no audio), resizes stills into
assets/img, makes the cut-outs, prepares the texture overlays from the user's halftone/TV textures, and
loudness-matches the voiceover and the opening soundbite.

Run:  python3 -I tools/prep.py [id ...]   (no ids = everything)
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
ROOT = "/home/user/claude-test-2.0"
SRC = f"{ROOT}/dimon-src"
PRJ = f"{ROOT}/dimon"
CLIPS, IMG, TEX, AUD = (f"{PRJ}/assets/{d}" for d in ("clips", "img", "tex", "audio"))
for d in (CLIPS, IMG, TEX, AUD):
    os.makedirs(d, exist_ok=True)

V = {
    "WB": "main/we_bank_the_countries.mp4",          # 1080p interview (the opening soundbite), small bug top right
    "NG": "main/name_of_the_game.mp4",               # 1080p Bloomberg-style doc, small bug top right
    "HJ": "main/how_jpmorgan_largest_bank.mp4",      # 1080p CNBC doc, peacock bug top right
    "UT": "main/untold_career_story_dimon.mp4",      # 1080p YouTube doc, age label top right
    "MP": "main/dimon_most_powerful_banker_doc.mp4", # 1080p doc, no bug
    "ST": "main/stories_2008_great_recession.mp4",   # 1080p 60 Minutes, bug top left
    "SM": "main/stock_market_crash_2008.mp4",        # 720p TV news montage
    "FP": "main/fired_push_scene_punch.mp4",         # 640x268 movie scene (the user's "fired" push)
    "WF": "main/wolf_of_wall_street_clip.mp4",       # 960x720
    "PK": "pinterest/klickpin_side_hustle.mp4",      # 1280x720 cash counter
    "PM": "pinterest/money_bg_blend.mp4",            # 736x414 falling money (background blend only)
    "CC": "main/cool_cinematic_clip.mp4",            # 720x360 surreal montage (engravings, clocks, eyes, nebula)
    "PV": "pinterest/pint_videos.mp4",               # 720x1280 3D chess: a glowing king among falling pieces
    "RD": "pinterest/klickpin_rustic_decor.mp4",     # 736x414 fire with a seated silhouette
    "CT": "main/citadel_high_speed_trading.mp4",     # 640x360 trading floor screens (bug bottom right, clock top right)
}
# zoom / centre that crop each source's burned-in bug or label out of frame
BUG = {"WB": (1.08, 0.48, 0.52), "NG": (1.08, 0.48, 0.52), "HJ": (1.09, 0.47, 0.53), "UT": (1.2, 0.45, 0.55),
       "ST": (1.10, 0.53, 0.54), "MP": (1.0, 0.5, 0.5), "SM": (1.0, 0.5, 0.5), "PK": (1.0, 0.5, 0.5),
       "PM": (1.0, 0.5, 0.5)}

# id: (source, in, duration, override (zoom, cx, cy) or None, W, H)
CLIP = {
    # the opening soundbite, in sync: the close shot, then the source's own two-shot for "You have to be big"
    "sb_cu": ("WB", 273.10, 3.00, None),
    "sb_two": ("WB", 281.05, 1.65, None),
    # hook
    "c_dimon_window": ("WB", 1222.0, 1.0, None),
    "c_wallst_sign": ("ST", 2082.0, 1.3, None),
    "c_nyse_jpm": ("NG", 244.0, 0.68, None),
    "c_nyse_flag": ("HJ", 69.6, 1.3, None),
    # fired setup
    "c_young_dimon": ("UT", 492.45, 1.2, (1.3, 0.44, 0.52)),
    "c_citigroup98": ("UT", 485.75, 0.9, None),
    "c_weill_old": ("MP", 466.2, 1.5, None),
    "c_dimon_weill_bw": ("MP", 516.4, 0.55, None),
    "c_cash": ("PK", 0.45, 1.3, None),
    "c_cash2": ("PK", 2.0, 1.9, None),
    "c_jessica": ("MP", 968.5, 0.8, None),
    "c_weill_daughter": ("MP", 1052.10, 1.6, None),
    # now runs a bank
    "c_jpm_gold": ("NG", 393.42, 0.95, None),
    "c_dc_aerial": ("NG", 381.9, 1.32, None),
    # golden boy
    "c_young_window": ("UT", 551.5, 0.95, None),
    "c_wolf_mic": ("WF", 0.2, 1.0, None),
    "c_wolf_money": ("WF", 35.7, 1.6, None),
    # heir apparent / Citigroup
    "c_cameras": ("NG", 121.0, 1.3, None),
    "c_heir": ("MP", 1097.0, 1.2, None),
    "c_citi_sign": ("MP", 848.0, 0.85, None),
    "c_citi_crowd": ("MP", 849.0, 1.3, None),
    "c_citi_aerial": ("MP", 855.64, 0.96, None),
    "c_weill_dimon_pair": ("MP", 359.0, 2.0, None),
    "c_weill_laugh": ("MP", 866.0, 0.8, None),
    # fired
    "c_strange": ("FP", 53.0, 1.7, None),
    "c_hallway": ("WB", 1201.45, 1.45, None),
    # wilderness
    "c_books": ("MP", 1494.0, 1.3, None),
    "c_bezos": ("NG", 256.2, 1.3, None),
    # comeback
    "c_dimon_dark": ("MP", 1183.0, 1.4, None),
    "c_old_wallst": ("HJ", 96.32, 1.28, None),
    # Bank One
    "c_bankone_podium": ("MP", 1450.5, 0.8, None),
    "c_bankone_night": ("MP", 1197.0, 0.8, None),
    "c_chicago": ("MP", 1214.5, 0.85, None),
    "c_bankone_stage": ("UT", 870.0, 1.15, (1.32, 0.40, 0.56)),
    "c_dimon_2000s": ("MP", 1329.4, 1.15, None),
    "c_trading_floor": ("HJ", 837.5, 1.4, None),
    "c_ticker_led": ("SM", 67.0, 1.6, None),
    "c_falling_chart": ("SM", 68.7, 0.6, None),
    # acquired
    "c_jpm_buys": ("UT", 1042.0, 0.65, None),
    "c_harrison_presser": ("UT", 1043.1, 0.75, None),
    "c_jpmco_sign": ("UT", 1048.0, 1.1, None),
    "c_harrison_backdrop": ("MP", 1571.0, 1.0, None),
    # 2008
    "c_stopwatch": ("ST", 4.0, 0.6, None),
    "c_nyse_floor": ("MP", 1770.0, 1.1, (1.22, 0.5, 0.40)),
    "c_plunge": ("SM", 86.5, 1.1, None),
    "c_bear_entrance": ("NG", 389.82, 0.83, None),
    "c_wamu": ("HJ", 827.0, 1.1, None),
    "c_bear_3d": ("MP", 1894.5, 1.4, None),
    "c_dimon_walk": ("MP", 1914.5, 0.85, None),
    "c_last_man": ("MP", 1915.5, 0.95, None),
    "c_fortress": ("UT", 1141.5, 1.0, None),
    "c_fire_sale": ("UT", 1160.0, 1.0, None),
    # payoff
    "c_jpm_night": ("HJ", 41.5, 1.1, None),
    "c_jpmco_sign2": ("HJ", 712.5, 1.2, None),
    "c_tickers": ("HJ", 1026.1, 1.2, None),
    "c_dimon_xcu": ("WB", 70.0, 1.3, None),
    "c_money_bg": ("PM", 0.0, 3.0, None),
    "c_citi_red": ("UT", 685.40, 0.50, None),
    "c_city_top": ("NG", 79.6, 1.3, None),
    # the wilderness year: alone at home under a lamp (the documentary's own picture of it)
    "c_alone": ("MP", 1133.0, 0.9, None),
    # the reference's graphic B-roll, from the Pinterest folder
    "c_surreal": ("CC", 0.2, 0.8, None),
    "c_chess": ("PV", 1.55, 0.9, None),
    "c_fire": ("RD", 2.0, 0.7, None),
    "c_screens": ("CT", 22.2, 0.7, (1.25, 0.45, 0.5)),
}

# single frames grabbed from the documentaries (with the source's crop): id -> (source, time)
GRAB = {
    "dimon_fists": ("UT", 824.6),   # the doc's "1998 (age 42)" photo: Dimon with both fists up
    "bear_door": ("NG", 390.3, "crop=1350:1030:285:25,scale=1920:-2"),   # the doc frames it in a TV mask
    "wamu_floor": ("HJ", 827.25),
}

# stills: id -> (source path, crop focus x, focus y) -- cover-cropped to 1920x1080
STILL = {
    "lead_japan1": ("imagepack/01_Jamie_Dimon/11_Jamie_Dimon_Japan_PM_courtesy_call_01.jpg", 0.5, 0.4),
    "lead_japan2": ("imagepack/01_Jamie_Dimon/12_Jamie_Dimon_Japan_PM_courtesy_call_02.jpg", 0.5, 0.4),
    "lead_japan3": ("imagepack/01_Jamie_Dimon/13_Jamie_Dimon_Japan_PM_courtesy_call_03.jpg", 0.5, 0.4),
    "lead_macri": ("imagepack/01_Jamie_Dimon/10_Jamie_Dimon_with_Mauricio_Macri.jpg", 0.5, 0.45),
    "lead_reeves1": ("imagepack/01_Jamie_Dimon/07_Jamie_Dimon_meets_Rachel_Reeves_01.jpg", 0.5, 0.35),
    "lead_reeves2": ("imagepack/01_Jamie_Dimon/08_Jamie_Dimon_meets_Rachel_Reeves_02.jpg", 0.5, 0.35),
    "dimon_reeves_portrait": ("imagepack/01_Jamie_Dimon/09_Jamie_Dimon_Rachel_Reeves_portrait_crop.jpg", 0.5, 0.3),
    "dimon_davos": ("imagepack/01_Jamie_Dimon/02_Jamie_Dimon_WEF_Davos_Becky_Quick_2016.jpg", 0.5, 0.4),
    "dimon_mcdermott": ("imagepack/01_Jamie_Dimon/04_Jamie_Dimon_with_Bill_McDermott_Becky_Quick.jpg", 0.5, 0.35),
    "wb_1": ("imagepack/08_World_Bank/01_World_Bank_Group_building_photo.jpg", 0.5, 0.5),
    "wb_2": ("imagepack/08_World_Bank/02_World_Bank_building_Washington.jpg", 0.5, 0.5),
    "wb_3": ("imagepack/08_World_Bank/03_World_Bank_building_alt.jpg", 0.5, 0.5),
    "gov_capitol": ("imagepack/07_US_Government_America/01_US_Capitol_west_front.jpg", 0.5, 0.5),
    "gov_wh1": ("imagepack/07_US_Government_America/02_White_House_north_facade.jpg", 0.5, 0.5),
    "gov_wh2": ("imagepack/07_US_Government_America/03_White_House_June_2024.jpg", 0.5, 0.5),
    "gov_treasury": ("imagepack/07_US_Government_America/04_US_Treasury_Building.jpg", 0.5, 0.5),
    "gov_gallatin": ("imagepack/07_US_Government_America/05_US_Treasury_Gallatin_statue.jpg", 0.5, 0.45),
    "gov_fed": ("imagepack/07_US_Government_America/06_Federal_Reserve_Eccles_Building.jpg", 0.5, 0.5),
    "gov_fed_old": ("imagepack/07_US_Government_America/07_Federal_Reserve_Eccles_1937_archival.jpg", 0.5, 0.5),
    "citi_center": ("imagepack/04_Citigroup/01_Citigroup_Center_53rd_Lex_day.jpg", 0.5, 0.4),
    "gloves": ("imagepack/10_Supporting_Illustrative/01_ILLUSTRATIVE_boxing_gloves_generic.jpg", 0.5, 0.5),
    "bezos_laugh": ("imagepack/10_Supporting_Illustrative/03_ILLUSTRATIVE_Jeff_Bezos_laugh_portrait.jpg", 0.5, 0.3),
    "bezos_amazon": ("imagepack/10_Supporting_Illustrative/04_ILLUSTRATIVE_Jeff_Bezos_Amazon_Seattle_2016.jpg", 0.5, 0.4),
    "chase_tower": ("imagepack/06_Bank_One_Chicago/01_Chase_Tower_Chicago_Bank_One_Plaza_ex.jpg", 0.5, 0.45),
    "nyse_old": ("imagepack/03_Wall_Street_NYSE/05_NYSE_exterior_historic_LOC.jpg", 0.5, 0.5),
    "lehman_nyc": ("imagepack/09_2008_Crisis/01_Lehman_Brothers_NYC_Sept_15_2008.jpg", 0.5, 0.45),
    "lehman_boxes": ("imagepack/09_2008_Crisis/02_Lehman_Brothers_employees_boxes_2008.jpg", 0.5, 0.4),
    "lehman_ts": ("imagepack/09_2008_Crisis/03_Lehman_Brothers_Times_Square.jpg", 0.5, 0.45),
    "bear_sign": ("imagepack/09_2008_Crisis/05_Bear_Stearns_signage.jpg", 0.5, 0.45),
    "wamu_center": ("imagepack/09_2008_Crisis/06_WaMu_Center_Seattle_1201_Third.jpg", 0.5, 0.45),
    "park270": ("imagepack/05_JPMorgan_Chase/03_270_Park_Avenue_summit_new_HQ.jpg", 0.5, 0.35),
    "dimon_gesture": ("imagepack/01_Jamie_Dimon/01_Jamie_Dimon_CEO_JPMorgan_Healthcare_2013.jpg", 0.5, 0.45),
    "ghost_bw": ("pinterest/jamie_black_and_white.jpg", 0.5, 0.4),
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


def crop_expr(W, H, Wt, Ht, cx, cy, zoom):
    A = Wt / Ht
    if W / H > A:
        h = H; w = H * A
    else:
        w = W; h = W / A
    w /= zoom; h /= zoom
    x = min(max(cx * W - w / 2, 0), W - w)
    y = min(max(cy * H - h / 2, 0), H - h)
    w, h, x, y = int(w) // 2 * 2, int(h) // 2 * 2, int(x), int(y)
    return f"crop={w}:{h}:{x}:{y},scale={Wt}:{Ht}:flags=lanczos,setsar=1"


def make_clip(cid):
    key, t, dur, over = CLIP[cid]
    src = f"{SRC}/{V[key]}"
    W, H = probe(src)
    if key == "PV":
        # vertical 3D render on black: keep it whole, full height, and place it on the black frame
        vf = "scale=-2:1080:flags=lanczos,setsar=1"
    elif key == "FP":
        # the movie scene keeps its own 2.39:1 letterbox picture: crop the black bars, scale to 1920 wide
        vf = "crop=640:268:0:0,scale=1920:804:flags=lanczos,setsar=1"
    else:
        zoom, cx, cy = over or BUG.get(key, (1.0, 0.5, 0.5))
        vf = crop_expr(W, H, 1920, 1080, cx, cy, zoom)
    vf += ",fps=30,format=yuv420p"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-t", f"{dur:.3f}",
         "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-g", "15",
         "-movflags", "+faststart", f"{CLIPS}/{cid}.mp4"])


def cuts(key, t0, t1, thr=0.22):
    """Picture cuts in a source between t0 and t1 (scene-change score), in source seconds."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i",
                        f"{SRC}/{V[key]}", "-an", "-vf", f"scale=480:-2,select='gt(scene,{thr})',showinfo", "-f", "null",
                        "-"], capture_output=True, text=True)
    return [round(t0 + float(x), 3) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def scan_all():
    """Report every clip or ramp whose source span crosses a picture cut (a stray frame of another shot)."""
    for cid, (key, t, dur, _) in CLIP.items():
        bad = [c for c in cuts(key, t, t + dur) if t + 0.02 < c < t + dur - 0.02]
        if bad:
            print(f"CUT  {cid}: {key} {t}..{t + dur:.2f} crosses {bad}")
    for rid, spec in RAMP.items():
        key, t = spec[0], spec[1]
        span = ramp_span(spec)
        bad = [c for c in cuts(key, t, t + span) if t + 0.02 < c < t + span - 0.02]
        print(f"{'CUT ' if bad else 'ok  '} {rid}: {key} {t}..{t + span:.2f} {bad or ''}")


# ---- speed ramps (time remapping) ------------------------------------------------------------------------------
# id: (source, in, [(output seconds, speed), ...], crop override or None, options)
# Speeds are joined smoothly (raised-cosine over `smooth` s), like a keyframed time-remap curve: fast parts are
# shutter-blended into motion blur, slow parts are optical-flow interpolated (minterpolate) so slow motion stays
# smooth. `hold` instead posterises time to that many frames per second for a deliberate low-frame-rate stutter.
RAMP = {
    # "fired": the push lands at normal speed, the astral body shoots out fast, then hangs in slow motion
    "r_strange": ("FP", 53.42, [(0.18, 1.0), (0.24, 4.2), (0.52, 0.42)], None, {}),
    # "into billions in profit": the money throw, fast into slow motion on "billions"
    "r_wolf_money": ("WF", 35.82, [(0.22, 2.2), (1.0, 0.42), (0.56, 1.0)], None, {}),
    # "and put $60 million": the counter races, then crawls on the number
    "r_cash2": ("PK", 1.2, [(0.45, 2.4), (0.75, 0.38), (0.42, 1.6)], None, {}),
    # "financial crisis hit"
    "r_plunge": ("SM", 86.68, [(0.25, 2.6), (0.6, 0.5), (0.37, 2.0)], None, {}),
    # "every single day": aerial over Manhattan, fast then floating
    "r_city_top": ("NG", 79.72, [(0.3, 2.4), (0.7, 0.55)], None, {}),
    # "2008": the floor, fast through the year roll, slow as it lands
    "r_nyse_floor": ("MP", 1770.1, [(0.3, 3.0), (0.55, 0.45)], (1.22, 0.5, 0.40), {}),
    # "That's JPMorgan": slow, whip fast, slow
    "r_jpm_night": ("HJ", 40.9, [(0.35, 0.5), (0.3, 3.0), (0.65, 0.6)], None, {}),
    # "into the stock": slow, then accelerating into the cut
    "r_trading_floor": ("HJ", 837.0, [(0.45, 0.6), (0.62, 2.0)], None, {}),
    # "turned a $500 million loss"
    "r_ticker_led": ("SM", 66.3, [(0.4, 2.5), (0.8, 0.45), (0.5, 1.8)], None, {}),
    # the closing face, in smooth slow motion
    "r_dimon_xcu": ("WB", 69.95, [(2.9, 0.38)], None, {}),
    # "standing"
    "r_last_man": ("MP", 1915.5, [(0.55, 0.5)], None, {}),
    # low frame rate on the crisis footage (12 fps stutter)
    "s_fire_sale": ("UT", 1160.0, [(1.05, 0.9)], None, {"hold": 12}),
    "s_falling_chart": ("SM", 68.82, [(0.62, 1.0)], None, {"hold": 12}),
    "s_bear_3d": ("MP", 1894.5, [(1.4, 1.0)], None, {"hold": 10}),
    "s_wamu": ("HJ", 827.0, [(0.35, 1.0)], None, {"hold": 12}),
    "s_bear_entrance": ("NG", 389.82, [(0.35, 1.0)], None, {"hold": 12}),
    "s_stopwatch": ("ST", 4.0, [(0.62, 1.0)], None, {"hold": 8}),
}


def _speed_curve(segs, smooth, fps=1000):
    """Source time as a function of output time, from speed segments joined by raised-cosine ramps."""
    total = sum(d for d, _ in segs)
    n = int(round(total * fps)) + 1
    t = np.arange(n) / fps
    sp = np.zeros(n)
    acc = 0.0
    for d, s in segs:
        sp[(t >= acc - 1e-9) & (t < acc + d + 1e-9)] = s
        acc += d
    if smooth > 0 and len(segs) > 1:
        w = int(smooth * fps)
        win = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(w) / (w - 1))
        win /= win.sum()
        pad = np.concatenate([np.full(w, sp[0]), sp, np.full(w, sp[-1])])
        sp = np.convolve(pad, win, mode="same")[w:-w]
    src = np.concatenate([[0.0], np.cumsum(sp[:-1]) / fps])
    return t, src, total


def ramp_span(spec):
    _, _, segs, _, opts = spec
    _, src, _ = _speed_curve(segs, opts.get("smooth", 0.12))
    return float(src[-1]) + 0.12


def make_ramp(rid):
    key, t_in, segs, over, opts = RAMP[rid]
    srcf = f"{SRC}/{V[key]}"
    W, H = probe(srcf)
    if key == "FP":
        vf, OW, OH = "crop=640:268:0:0,scale=1920:804:flags=lanczos,setsar=1", 1920, 804
    else:
        zoom, cx, cy = over or BUG.get(key, (1.0, 0.5, 0.5))
        vf, OW, OH = crop_expr(W, H, 1920, 1080, cx, cy, zoom), 1920, 1080
    hold = opts.get("hold")
    slow = min(s for _, s in segs) < 0.95 and not hold
    fin = 60.0 if slow else 30.0
    crop, rest = vf.split(",", 1)
    mi = "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
    vf = f"{crop},{mi},{rest}" if slow else f"{vf},fps=30"
    tg, src, total = _speed_curve(segs, opts.get("smooth", 0.12))
    span = float(src[-1]) + 0.12
    dec = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{t_in:.3f}", "-t", f"{span:.3f}",
                            "-i", srcf, "-an", "-vf", vf + ",format=rgb24", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{OW}x{OH}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf",
                            "16", "-g", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{CLIPS}/{rid}.mp4"],
                           stdin=subprocess.PIPE)
    fsize = OW * OH * 3
    buf, base = [], 0  # buf[k] is source frame base + k

    def frame(i):
        nonlocal base
        while i >= base + len(buf):
            b = dec.stdout.read(fsize)
            if len(b) < fsize:
                return buf[-1] if buf else np.zeros((OH, OW, 3), np.uint8)
            buf.append(np.frombuffer(b, np.uint8).reshape(OH, OW, 3))
        while base < i - 2 and len(buf) > 4:
            buf.pop(0); base += 1
        return buf[max(0, i - base)]

    def at(ts):
        p = ts * fin
        i = int(np.floor(p)); f = p - i
        a = frame(i).astype(np.float32)
        if f < 0.02:
            return a
        return a * (1 - f) + frame(i + 1).astype(np.float32) * f

    nout = int(round(total * 30))
    for k in range(nout):
        to = k / 30
        if hold:
            to = np.floor(to * hold + 1e-6) / hold
            img = at(float(np.interp(to, tg, src)))
        else:
            # 180-degree shutter: average sub-frames across half the frame interval (motion blur when fast)
            subs = [float(np.interp(min(total, max(0.0, to + d / 30)), tg, src)) for d in (-0.25, -0.125, 0, 0.125, 0.25)]
            spread = (subs[-1] - subs[0]) * fin
            if spread < 0.6:
                img = at(subs[2])
            else:
                img = sum(at(s_) for s_ in subs) / len(subs)
        enc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    dec.stdout.close(); dec.kill()
    return total, span


def make_grab(gid):
    key, t, *post = GRAB[gid]
    src = f"{SRC}/{V[key]}"
    W, H = probe(src)
    zoom, cx, cy = BUG.get(key, (1.0, 0.5, 0.5))
    vf = crop_expr(W, H, 1920, 1080, cx, cy, zoom) + ("," + post[0] if post else "")
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
         "-vf", vf, "-q:v", "2", f"{IMG}/{gid}.jpg"])


def cover(im, W, H, fx, fy):
    w, h = im.size
    s = max(W / w, H / h)
    im = im.resize((max(W, round(w * s)), max(H, round(h * s))), Image.LANCZOS)
    w, h = im.size
    x = int(min(max(fx * w - W / 2, 0), w - W)); y = int(min(max(fy * h - H / 2, 0), h - H))
    return im.crop((x, y, x + W, y + H))


def make_still(sid):
    path, fx, fy = STILL[sid]
    im = ImageOps.exif_transpose(Image.open(f"{SRC}/{path}")).convert("RGB")
    cover(im, 1920, 1080, fx, fy).save(f"{IMG}/{sid}.jpg", quality=92)


def make_cutouts():
    """Background removal on two portraits (the seal composite and the B&W name card)."""
    tmp = f"{SRC}/cutouts"
    os.makedirs(tmp, exist_ok=True)
    # 1) Dimon gesturing (seal composite): the full frame at 1920x1080 plus its cut-out
    run(["npx", "hyperframes@0.9.2", "remove-background", f"{IMG}/dimon_gesture.jpg", "-o", f"{IMG}/dimon_gesture-cut.png"])
    # 2) the smiling Davos portrait for the name card, cut out and made black and white
    src = Image.open(f"{SRC}/imagepack/01_Jamie_Dimon/03_Jamie_Dimon_portrait_crop_Davos_2016.jpg").convert("RGB")
    src.save(f"{tmp}/davos.jpg", quality=95)
    run(["npx", "hyperframes@0.9.2", "remove-background", f"{tmp}/davos.jpg", "-o", f"{tmp}/davos-cut.png"])
    cut = Image.open(f"{tmp}/davos-cut.png").convert("RGBA")
    r, g, b, a = cut.split()
    grey = ImageOps.autocontrast(Image.merge("RGB", (r, g, b)).convert("L"), cutoff=1)
    bw = Image.merge("RGBA", (grey, grey, grey, a))
    bbox = a.getbbox()
    bw = bw.crop(bbox)
    bw.thumbnail((900, 900), Image.LANCZOS)
    bw.save(f"{IMG}/dimon_card-cut.png")
    # the presidential seal (PNG with alpha), kept square
    seal = Image.open(f"{SRC}/pinterest/seal_president.png").convert("RGBA")
    seal.resize((1200, 1200), Image.LANCZOS).save(f"{IMG}/seal.png")


def make_textures():
    """The user's textures as overlay plates: halftone dots, the RGB phosphor (old TV screen), a print grain."""
    def plate(name, out, scale, mode="RGB"):
        im = Image.open(f"{SRC}/textures/{name}").convert(mode)
        w, h = im.size
        cw, ch = int(1920 * 1.12 * scale), int(1080 * 1.12 * scale)
        x, y = (w - cw) // 2, (h - ch) // 2
        im = im.crop((x, y, x + cw, y + ch)).resize((int(1920 * 1.12), int(1080 * 1.12)), Image.LANCZOS)
        im.save(f"{TEX}/{out}", quality=90)
    plate("halftone_3.jpg", "tx_dots.jpg", 2.0, "L")       # black print dots on white -> multiply
    plate("halftone_2.jpg", "tx_rgb.jpg", 1.0, "RGB")      # RGB phosphor triads -> overlay (old TV screen)
    plate("halftone_6.jpg", "tx_print.jpg", 1.6, "L")      # grey print grain with dots -> soft-light
    plate("halftone_7.png", "tx_dots_big.jpg", 1.4, "L")   # big black dots, for the halftone flash frames


def make_audio():
    # the voiceover (the user's "jamie dimon audio 2.0"), -16 LUFS
    vo = "/root/.claude/uploads/9d443a94-318c-570a-a605-cc849b61623f/6ff11667-jamie_dimon_audio_2.0.mp3"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", vo, "-af",
         "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", f"{AUD}/vo.wav"])
    # the opening soundbite from the interview, in sync with sb_cu / sb_two, matched to the voiceover
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", "273.10", "-t", "9.15", "-i", f"{SRC}/{V['WB']}",
         "-vn", "-af", "highpass=f=80,loudnorm=I=-16.5:TP=-1.5:LRA=9,afade=t=in:d=0.04,afade=t=out:st=8.85:d=0.30",
         "-ar", "48000", "-ac", "2", f"{AUD}/soundbite.wav"])


if __name__ == "__main__":
    only = set(sys.argv[1:])
    want = lambda k: not only or k in only
    if only <= {"scan", "ramps"} and only:
        want = lambda k: k in only
    for cid in CLIP:
        if want(cid):
            make_clip(cid); print("clip", cid)
    for sid in STILL:
        if want(sid):
            make_still(sid); print("still", sid)
    if want("cutouts"):
        make_cutouts(); print("cutouts")
    if want("textures"):
        make_textures(); print("textures")
    if want("audio"):
        make_audio(); print("audio")
    for gid in GRAB:
        if want(gid) or want("grabs"):
            make_grab(gid); print("grab", gid)
    for rid in RAMP:
        if want(rid) or want("ramps"):
            print("ramp", rid, make_ramp(rid), flush=True)
    if "scan" in only:
        scan_all()
