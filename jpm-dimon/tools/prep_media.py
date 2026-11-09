#!/usr/bin/env python3
"""Prepare every media asset the Jamie Dimon / JPMorgan edit uses (16:9, 1920x1080, 30 fps).

Trims, crops and scales source shots into assets/clips (H.264, 30 fps, no audio), copies and
resizes stills into assets/img, builds the halftone print textures into assets/tex and cuts the
three dialogue/voice pieces into assets/audio (loudness-matched).

Run:  python3 -I tools/prep_media.py [id ...]   (no ids = everything)
"""
import os, re, subprocess, sys

ROOT = "/home/user/claude-test-2.0"
SRC = f"{ROOT}/dimon-src"
PRJ = f"{ROOT}/jpm-dimon"
CLIPS, IMG, TEX, AUD = (f"{PRJ}/assets/{d}" for d in ("clips", "img", "tex", "audio"))
for d in (CLIPS, IMG, TEX, AUD):
    os.makedirs(d, exist_ok=True)

V = {
    "GAME": "_direct/name_of_the_game.mp4",          # Bloomberg Originals: the news open + B-roll
    "BANK": "_direct/we_bank.mp4",                   # Bloomberg (Emily Chang) Dimon interview + archival
    "MPB": "_direct/most_powerful_banker_doc.mp4",   # "Most Powerful Banker in America" documentary
    "UNT": "_direct/untold_career_story.mp4",        # "Untold Career Story" (archival inserts only)
    "HOW": "_direct/how_jpm_became_largest.mp4",     # CNBC "How JP Morgan Chase became the largest bank"
    "STO": "_direct/stories_2008_recession.mp4",     # 60 Minutes 2008 stories
    "CRASH": "_direct/crash_2008.mp4",               # 2008 news broadcasts
    "WOLF": "_direct/wolf_of_wall_street.mp4",
    "FIRED": "_direct/fired_push_scene.mp4",         # the user's "fired" push scene (Doctor Strange)
    "COOL": "_direct/cool_cinematic.mp4",
    "P02": "_pin/p02_Explore_Modern_rustic_weddin.mp4",   # man in a burning room
    "P07": "_pin/p07_Try_these_11_Classy_side_hus.mp4",   # money counting machine
    "P08": "_pin/p08_Well_that_is_Money_launderin.mp4",   # money porthole (vertical)
    "P10": "_pin/p10_money_can_be_used_in_differe.mp4",   # falling money (the user's bg blend clip)
    "P11": "_pin/p11_pint_videos_mp4.mp4",                # chess: the king stands, the rest fall (vertical)
    "P06": "_pin/p06_Stylish_entryway_makeover_id.mp4",   # helicopter lifting pallets of money off the Fed
}

# Logo-safe framings. (cx, cy, zoom): centre of the crop window relative to the frame, zoom >= 1 tightens.
BBG = (0.47, 0.53, 1.07)   # Bloomberg bug, top right
CNBC = (0.46, 0.54, 1.08)  # CNBC peacock, top right
UNTF = (0.45, 0.56, 1.12)  # the YouTuber's "year (age)" label, top right
SIXTY = (0.56, 0.57, 1.17)  # 60 Minutes logo, top left
FULL = (0.5, 0.5, 1.0)

# id: (source, in, duration, framing, W, H, letterbox(bool))
CLIP_SPECS = {
    # ---- open: the news piece (picture kept close to its own cut; the reporter stays in sync) ----
    "o_aerial": ("GAME", 0.00, 1.80, BBG, 1920, 1080, False),
    "o_wallst": ("GAME", 3.55, 1.30, BBG, 1920, 1080, False),
    "o_up": ("GAME", 5.60, 2.90, BBG, 1920, 1080, False),
    "o_reporter": ("GAME", 8.40, 3.10, BBG, 1920, 1080, False),
    "o_jpmsign": ("GAME", 522.05, 2.40, BBG, 1920, 1080, False),
    # ---- VO part 1 ----
    "v_dimon_up": ("BANK", 69.00, 1.80, BBG, 1920, 1080, False),
    "v_flag": ("BANK", 38.00, 1.60, (0.64, 0.5, 1.30), 1920, 1080, False),
    "v_walk": ("GAME", 261.00, 2.10, BBG, 1920, 1080, False),
    "v_wolf": ("WOLF", 1.20, 1.60, (0.5, 0.42, 1.0), 1920, 1080, False),
    "v_dimon_int": ("MPB", 1081.00, 1.20, (0.55, 0.5, 1.06), 1920, 1080, False),
    "v_heir": ("MPB", 1094.30, 1.90, FULL, 1920, 1080, False),
    "v_weill": ("MPB", 438.00, 1.70, FULL, 1920, 1080, False),
    "v_money": ("P07", 1.00, 1.30, FULL, 1920, 1080, False),
    "v_jessica": ("MPB", 1053.50, 2.00, FULL, 1920, 1080, False),
    "v_tsq": ("MPB", 1042.00, 1.20, FULL, 1920, 1080, False),
    "v_jpmsign2": ("HOW", 39.20, 1.20, CNBC, 1920, 1080, False),
    "v_aerial2": ("BANK", 219.00, 1.40, BBG, 1920, 1080, False),
    # ---- Dimon himself (Bloomberg interview, sync) ----
    "d_dimon": ("BANK", 273.05, 4.95, BBG, 1920, 1080, False),
    "d_dimon2": ("BANK", 278.30, 1.40, BBG, 1920, 1080, False),
    "d_capitol": ("GAME", 182.00, 1.90, BBG, 1920, 1080, False),
    "d_two": ("BANK", 281.00, 3.50, BBG, 1920, 1080, False),
    "d_big": ("MPB", 1483.00, 1.00, FULL, 1920, 1080, False),
    # ---- VO part 2 ----
    "m_name": ("MPB", 1295.00, 2.30, FULL, 1920, 1080, False),
    "m_golden": ("MPB", 369.50, 2.10, FULL, 1920, 1080, False),
    "m_press": ("MPB", 849.50, 1.70, FULL, 1920, 1080, False),
    "m_nextline": ("MPB", 291.00, 1.00, FULL, 1920, 1080, False),
    "m_citicenter": ("MPB", 856.00, 3.00, FULL, 1920, 1080, False),
    "m_citigroup": ("MPB", 840.00, 1.70, FULL, 1920, 1080, False),
    "m_sidebyside": ("BANK", 458.20, 1.60, BBG, 1920, 1080, False),
    "m_weill": ("MPB", 860.00, 1.50, FULL, 1920, 1080, False),
    "m_16a": ("MPB", 291.80, 0.80, FULL, 1920, 1080, False),
    "m_16b": ("MPB", 277.00, 0.80, FULL, 1920, 1080, False),
    "m_16c": ("UNT", 561.00, 0.80, UNTF, 1920, 1080, False),
    "m_42": ("UNT", 543.00, 1.80, UNTF, 1920, 1080, False),
    "m_strange": ("FIRED", 96.35, 2.00, FULL, 1920, 804, False),
    "m_fall": ("FIRED", 99.70, 1.30, FULL, 1920, 804, False),
    "m_bed": ("MPB", 1133.50, 1.60, FULL, 1920, 1080, False),
    "m_snowball": ("MPB", 614.00, 1.70, FULL, 1920, 1080, False),
    "m_bezos": ("GAME", 256.55, 1.50, BBG, 1920, 1080, False),
    "m_premise": ("COOL", 0.00, 1.70, FULL, 1920, 1080, False),
    "m_walkback": ("MPB", 1468.00, 1.60, FULL, 1920, 1080, False),
    "m_wallst_hist": ("HOW", 323.00, 1.10, CNBC, 1920, 1080, False),
    "m_nyse_hist": ("HOW", 306.00, 1.40, CNBC, 1920, 1080, False),
    "m_bankone": ("MPB", 1192.00, 1.90, FULL, 1920, 1080, False),
    "m_chicago": ("MPB", 1248.00, 1.10, FULL, 1920, 1080, False),
    "m_dividend": ("MPB", 1446.00, 1.40, FULL, 1920, 1080, False),
    "m_cleaned": ("MPB", 1323.00, 1.30, FULL, 1920, 1080, False),
    "m_money": ("MPB", 1783.50, 2.00, FULL, 1920, 1080, False),
    "m_ownmoney": ("P08", 4.00, 1.30, FULL, 608, 1080, False),
    "m_stock": ("HOW", 1022.50, 1.30, CNBC, 1920, 1080, False),
    "m_fox": ("HOW", 697.00, 1.60, CNBC, 1920, 1080, False),
    "m_harrison": ("UNT", 1055.50, 1.30, UNTF, 1920, 1080, False),
    "m_flags": ("HOW", 692.50, 1.40, CNBC, 1920, 1080, False),
    "m_2008": ("HOW", 792.60, 1.60, CNBC, 1920, 1080, False),
    "m_dow": ("CRASH", 72.00, 1.20, FULL, 1920, 1080, False),
    "m_fire": ("P02", 1.00, 0.80, FULL, 1920, 1080, False),
    "m_lehman": ("STO", 1438.50, 0.80, SIXTY, 1920, 1080, False),
    "m_bankrun": ("STO", 345.00, 0.80, SIXTY, 1920, 1080, False),
    "m_fdic": ("STO", 30.00, 0.80, SIXTY, 1920, 1080, False),
    "m_head": ("STO", 2294.60, 1.00, SIXTY, 1920, 1080, False),
    "m_chess": ("P11", 0.90, 1.10, FULL, 608, 1080, False),
    "m_lastman": ("MPB", 1916.50, 1.10, FULL, 1920, 1080, False),
    "m_heli": ("P06", 1.40, 1.30, FULL, 1920, 1080, False),
    "m_firesale": ("UNT", 1157.50, 1.20, UNTF, 1920, 1080, False),
    "m_bear": ("MPB", 1891.00, 1.00, FULL, 1920, 1080, False),
    "m_jpmstone": ("MPB", 1517.00, 1.70, FULL, 1920, 1080, False),
    "m_chase": ("HOW", 1019.20, 1.00, CNBC, 1920, 1080, False),
    "m_nyseboard": ("BANK", 750.20, 1.20, BBG, 1920, 1080, False),
    "m_screens": ("BANK", 756.00, 1.70, BBG, 1920, 1080, False),
    "m_moneyfall": ("P10", 2.00, 1.30, FULL, 1920, 1080, False),
    "m_end": ("BANK", 1031.00, 2.80, BBG, 1920, 1080, False),
}

STILLS = {  # id: (path under dimon-src, max long edge)
    "worldbank": ("Jamie_Dimon_Image_Pack/08_World_Bank/02_World_Bank_building_Washington.jpg", 2400),
    "boxing": ("Jamie_Dimon_Image_Pack/10_Supporting_Illustrative/01_ILLUSTRATIVE_boxing_gloves_generic.jpg", 2400),
    "bezos_amazon": ("Jamie_Dimon_Image_Pack/10_Supporting_Illustrative/04_ILLUSTRATIVE_Jeff_Bezos_Amazon_Seattle_2016.jpg", 2400),
}

TEXTURES = {  # id: halftone source (the user's print textures) -> neutral overlay maps
    "ht_grunge": "halftone textures/Copy of Halftone Grunge.jpg",
    "ht_paper": "halftone textures/Copy of Halftone 6.jpg",
    "ht_warm": "halftone textures/Copy of Halftone 1.jpg",
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
    x = cx * W - w / 2
    y = cy * H - h / 2
    x = min(max(x, 0), W - w)
    y = min(max(y, 0), H - h)
    w, h, x, y = int(w) // 2 * 2, int(h) // 2 * 2, int(x), int(y)
    return f"crop={w}:{h}:{x}:{y},scale={Wt}:{Ht}:flags=lanczos,setsar=1"


def make_clip(cid):
    key, t, dur, (cx, cy, zoom), Wt, Ht, _ = CLIP_SPECS[cid]
    src = f"{SRC}/{V[key]}"
    W, H = probe(src)
    vf = crop_expr(W, H, Wt, Ht, cx, cy, zoom) + ",fps=30,format=yuv420p"
    out = f"{CLIPS}/{cid}.mp4"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", src, "-t", f"{dur:.3f}",
         "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-g", "15",
         "-movflags", "+faststart", out])
    return out


def make_still(sid):
    rel, edge = STILLS[sid]
    out = f"{IMG}/{sid}.jpg"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{SRC}/{rel}", "-vf",
         f"scale='if(gt(iw,ih),min({edge},iw),-2)':'if(gt(iw,ih),-2,min({edge},ih))':flags=lanczos",
         "-q:v", "2", out])
    return out


def make_texture(tid):
    """High-pass the user's halftone scan into a neutral-grey overlay map (128 = no change), 1920x1080."""
    src = f"{SRC}/{TEXTURES[tid]}"
    out = f"{TEX}/{tid}.jpg"
    # big blur removes the paper's tone and vignette; what is left is the dot screen, fibres and specks
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src, "-filter_complex",
         "[0:v]scale=2400:-2:flags=area,format=gray,split[a][b];[b]gblur=sigma=40[bl];"
         "[a][bl]blend=all_expr='clip(128+(A-B)*1.6,0,255)',crop=1920:1080:(iw-1920)/2:(ih-1080)/2",
         "-q:v", "3", out])
    return out


def loudnorm(inp, out, ss=None, t=None, target=-16.0):
    pre = (["-ss", f"{ss:.3f}"] if ss is not None else []) + ["-i", inp] + (["-t", f"{t:.3f}"] if t is not None else [])
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", *pre, "-af",
                        f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    import json
    j = json.loads(m.group(0))
    af = (f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *pre, "-af", af, "-ar", "48000", "-ac", "2",
         "-c:a", "pcm_s16le", out])
    return out


def make_audio():
    # the news open: source 0-14 s (the build places two pieces of it, joined in natural pauses)
    loudnorm(f"{SRC}/{V['GAME']}", f"{AUD}/news_open.wav", ss=0.0, t=14.0)
    # Dimon, Bloomberg interview: source 272.5-285.0 s
    loudnorm(f"{SRC}/{V['BANK']}", f"{AUD}/dimon_quote.wav", ss=272.5, t=12.5)
    # the narration as delivered
    loudnorm(f"{SRC}/jamie dimon audi.mp3", f"{AUD}/vo.wav")


def get_satoshi():
    """Satoshi is free to use (ITF Free Font License) but may not be redistributed, so it is fetched from Fontshare."""
    import io, urllib.request, zipfile
    fonts = f"{PRJ}/assets/fonts"
    need = [f"Satoshi-{w}.woff2" for w in ("Regular", "Medium", "Bold", "Black", "Variable")]
    if all(os.path.exists(f"{fonts}/{n}") for n in need):
        return
    data = urllib.request.urlopen("https://api.fontshare.com/v2/fonts/download/satoshi").read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            name = os.path.basename(info.filename)
            if "/WEB/fonts/" in info.filename and name in need:
                open(f"{fonts}/{name}", "wb").write(z.read(info))


if __name__ == "__main__":
    want = set(sys.argv[1:])
    if not want or "fonts" in want:
        get_satoshi(); print("fonts", flush=True)
    def ok(k):
        return not want or k in want
    for cid in CLIP_SPECS:
        if ok(cid):
            make_clip(cid); print("clip", cid, flush=True)
    for sid in STILLS:
        if ok(sid):
            make_still(sid); print("still", sid, flush=True)
    for tid in TEXTURES:
        if ok(tid):
            make_texture(tid); print("tex", tid, flush=True)
    if ok("audio"):
        make_audio(); print("audio", flush=True)
