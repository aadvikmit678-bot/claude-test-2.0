#!/usr/bin/env python3
"""v2 media prep: extracts every clip and still that tools/build2.py registers.

build2.py writes tools/media_v2.json ({"clips": {id: spec}, "stills": {id: spec}}). This script makes each missing
file (or every file with --force): clips into assets/clips2 (H.264, 30 fps, no audio), stills into assets/img2.

Run:  python3 -I tools/build2.py --specs && python3 -I tools/prep2.py [--force] [id ...]
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = "/home/user/claude-test-2.0"
SRC = f"{ROOT}/dimon-src"
PRJ = f"{ROOT}/jpm-dimon"
CLIPS, IMG = f"{PRJ}/assets/clips2", f"{PRJ}/assets/img2"
for d in (CLIPS, IMG):
    os.makedirs(d, exist_ok=True)

V = {
    "GAME": "_direct/name_of_the_game.mp4", "BANK": "_direct/we_bank.mp4", "MPB": "_direct/most_powerful_banker_doc.mp4",
    "UNT": "_direct/untold_career_story.mp4", "HOW": "_direct/how_jpm_became_largest.mp4",
    "STO": "_direct/stories_2008_recession.mp4", "CRASH": "_direct/crash_2008.mp4", "WOLF": "_direct/wolf_of_wall_street.mp4",
    "FIRED": "_direct/fired_push_scene.mp4", "COOL": "_direct/cool_cinematic.mp4", "CHAIR": "_direct/dimon_chairman_interview.mp4",
    "SPEAK": "_direct/dimon_speaking.mp4", "RIB": "_direct/ribbon_hq.mp4", "CIT": "_direct/citadel_trading.mp4",
    "WALLV": "_direct/wallst_ny_short.mp4", "NYSEV": "_direct/nyse_closing_bell.mp4", "JPMV": "_direct/jpm_building_aura.mp4",
    "P01": "_pin/p01_2008_8_crash_for_first_kind_.mp4", "P02": "_pin/p02_Explore_Modern_rustic_weddin.mp4",
    "P03": "_pin/p03_Gorgeous_wedding_hair_ideas_.mp4", "P04": "_pin/p04_Relaxed_shell_toned_style_id.mp4",
    "P06": "_pin/p06_Stylish_entryway_makeover_id.mp4", "P07": "_pin/p07_Try_these_11_Classy_side_hus.mp4",
    "P08": "_pin/p08_Well_that_is_Money_launderin.mp4", "P09": "_pin/p09_eye_mp4.mp4",
    "P10": "_pin/p10_money_can_be_used_in_differe.mp4", "P11": "_pin/p11_pint_videos_mp4.mp4",
}
# logo-safe framings: (cx, cy, zoom) of the crop window, relative to the frame
FRAMES = {"FULL": (0.5, 0.5, 1.0), "BBG": (0.47, 0.53, 1.07), "CNBC": (0.46, 0.54, 1.08), "UNTF": (0.45, 0.56, 1.12),
          "SIXTY": (0.56, 0.57, 1.17)}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(cmd)}\n{r.stderr[-1500:]}")
    return r


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of",
               "csv=p=0", path]).stdout.strip().split(",")
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


def make_clip(cid, spec):
    src = f"{SRC}/{V[spec['key']]}"
    W, H = probe(src)
    cx, cy, z = spec.get("frame_xyz") or FRAMES[spec.get("frame", "FULL")]
    Wt, Ht = spec.get("size", [1920, 1080])
    vf = crop_expr(W, H, Wt, Ht, cx, cy, z) + ",fps=30,format=yuv420p"
    out = f"{CLIPS}/{cid}.mp4"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{spec['t']:.3f}", "-i", src, "-t", f"{spec['dur']:.3f}",
         "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-g", "10", "-movflags", "+faststart", out])
    return cid


CUT_SRC = {  # subject cut-outs made with the local matting model (npx hyperframes remove-background)
    "dimon06": "Jamie_Dimon_Image_Pack/01_Jamie_Dimon/06_Jamie_Dimon_Global_Financial_Context_crop.jpg",
    "dimon09": "Jamie_Dimon_Image_Pack/01_Jamie_Dimon/09_Jamie_Dimon_Rachel_Reeves_portrait_crop.jpg",
    "bezos03": "Jamie_Dimon_Image_Pack/10_Supporting_Illustrative/03_ILLUSTRATIVE_Jeff_Bezos_laugh_portrait.jpg",
}


def ensure_cutout(path):
    name = os.path.basename(path)[:-4]
    if os.path.exists(path) or name not in CUT_SRC:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    run(["npx", "--yes", "hyperframes@0.9.2", "remove-background", f"{SRC}/{CUT_SRC[name]}", "-o", path, "--json"])


def make_still(sid, spec):
    out = f"{IMG}/{sid}.{spec.get('ext', 'jpg')}"
    if spec.get("key"):  # a frame from a video
        src = f"{SRC}/{V[spec['key']]}"
        W, H = probe(src)
        cx, cy, z = spec.get("frame_xyz") or FRAMES[spec.get("frame", "FULL")]
        Wt, Ht = spec.get("size", [1920, 1080])
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{spec['t']:.3f}", "-i", src, "-frames:v", "1",
             "-vf", crop_expr(W, H, Wt, Ht, cx, cy, z), "-q:v", "2", out])
    elif spec["path"].endswith(".svg"):  # vector logos are used as they are
        import shutil
        shutil.copy(spec["path"] if spec["path"].startswith("/") else f"{SRC}/{spec['path']}", out)
    else:  # a file: copy / resize (PNG keeps alpha)
        src = spec["path"] if spec["path"].startswith("/") else f"{SRC}/{spec['path']}"
        ensure_cutout(src)
        edge = spec.get("edge", 2000)
        vf = f"scale='if(gt(iw,ih),min({edge},iw),-2)':'if(gt(iw,ih),-2,min({edge},ih))':flags=lanczos"
        if spec.get("crop"):  # x, y, w, h as fractions of the source
            fx, fy, fw, fh = spec["crop"]
            vf = f"crop=iw*{fw}:ih*{fh}:iw*{fx}:ih*{fy}," + vf
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src, "-vf", vf] +
            (["-q:v", "2"] if out.endswith(".jpg") else []) + [out])
    return sid


if __name__ == "__main__":
    force = "--force" in sys.argv
    want = {a for a in sys.argv[1:] if not a.startswith("--")}
    spec = json.load(open(f"{PRJ}/tools/media_v2.json"))
    jobs = []
    for cid, s in spec["clips"].items():
        if (want and cid not in want) or (not force and not want and os.path.exists(f"{CLIPS}/{cid}.mp4")):
            continue
        jobs.append(("clip", cid, s))
    for sid, s in spec["stills"].items():
        if (want and sid not in want) or (not force and not want and os.path.exists(f"{IMG}/{sid}.{s.get('ext', 'jpg')}")):
            continue
        jobs.append(("still", sid, s))
    print(f"{len(jobs)} files to make", flush=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for done in ex.map(lambda j: (make_clip if j[0] == "clip" else make_still)(j[1], j[2]), jobs):
            pass
    print("done", flush=True)
