#!/usr/bin/env python3
"""v5 media, made after tools/prep2.py has extracted the registered clips.

1. Mattes: every registered clip with "matte": true gets {cid}_cut.webm (npx hyperframes remove-background) and
   {cid}_halo.webm, a soft white glow of the subject's shape, pre-rendered from the matte's alpha (the cut-out glow).
2. The talking freeze (the first frame of S02's speaking clip, same crop): spk_f.jpg, spk_cut.png, spk_sil.png,
   spk_halo.png (tools/prep4.glows).
3. Smooth slow motion, so the player never repeats frames (v4's Wolf shot judderd at 0.72x playback):
   wolf_slow.mp4 and ceo_slow.mp4, motion-interpolated to 30 fps at the exact length the beat needs.
4. Dario's "every AI tech bro" stills for "by his own mentor": Sandy Weill's face centred at (960, 505) at close-up
   size, the edges of each photo zoom-blurred around a sharp circle (tools/faces.dario).
5. The was-fired page's three photos of young Dimon: squares centred on his face (tools/faces.square).

Run:  python3 -I tools/build5.py --specs && python3 -I tools/prep2.py --spec=media_v5.json && python3 tools/prep5.py
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep2, prep4, faces  # noqa: E402

PRJ, CLIPS, IMG = prep2.PRJ, prep2.CLIPS, prep2.IMG
SPEC = json.load(open(f"{PRJ}/tools/media_v5.json"))
SPEAK_XYZ = (0.592, 0.40, 1.15)          # Dimon centred like Hemant Taneja at 22 s: head top ~100 px, hands in frame
SPEAK_FREEZE_T = 12.65            # = the speaking clip's source time at film 9.05 (build5 SPK)

WEILL = [  # id, source[#search region], face width in the frame (Dario's faces are 390-830 px)
    ("wf0", "_weill/weill_1.jpg", 640),
    ("wf1", "MPB@772.0", 600),
    ("wf2", "MPB@861.0", 640),
    ("wf3", "_weill/weill_0.jpg", 560),
    ("wf4", "MPB@441.0", 700),
    ("wf5", "Jamie_Dimon_Image_Pack/02_Sandy_Weill/02_Sanford_Weill_portrait_Met_Opera_2009.jpg", 560),
    ("wf6", "MPB@714.0", 600),
    ("wf7", "MPB@889.0", 560),
]
YOUNG = [  # id, source, square scale (side / face width), dx, dy
    ("yd5_1", "MPB@871.0", 2.4, 0.0, 0.10),
    ("yd5_2", "MPB@700.0", 2.3, 0.0, 0.10),
    ("yd5_3", "UNT@543.0#0.2,0,0.6,1", 1.45, -0.12, 0.12),
]


def run(cmd):
    return prep2.run(cmd)


def matte(cid):
    src, cut, halo = f"{CLIPS}/{cid}.mp4", f"{CLIPS}/{cid}_cut.webm", f"{CLIPS}/{cid}_halo.webm"
    if not os.path.exists(cut):
        run(["npx", "--yes", "hyperframes@0.9.2", "remove-background", src, "-o", cut, "--quality", "best", "--json"])
    if not os.path.exists(halo):
        dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cut]).stdout)
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-c:v", "libvpx-vp9", "-i", cut, "-f", "lavfi", "-i",
             f"color=c=white:s=1920x1080:r=30:d={dur:.3f}", "-filter_complex",
             "[0:v]format=rgba,alphaextract,gblur=sigma=17,lutyuv=y='min(255,val*1.7)'[a];"
             "[1:v]format=rgba[w];[w][a]alphamerge,format=yuva420p",
             "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "34", "-auto-alt-ref", "0", "-row-mt", "1", halo])
    return cid


def speak_freeze():
    if os.path.exists(f"{IMG}/spk_halo.png"):
        return
    src = f"{prep2.SRC}/{prep2.V['SPEAK']}"
    W, H = prep2.probe(src)
    out = f"{IMG}/spk_f.jpg"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{SPEAK_FREEZE_T:.3f}", "-i", src, "-frames:v", "1",
         "-vf", prep2.crop_expr(W, H, 1920, 1080, *SPEAK_XYZ), "-q:v", "2", out])
    cut = prep4.cutout("spk", out)
    prep4.glows("spk", cut)


def slowmo(name, key, t, src_dur, out_dur, crop=None):
    """[t, t + src_dur) of a source, motion-interpolated to 30 fps and stretched to out_dur (+0.25 s padding)."""
    out = f"{CLIPS}/{name}.mp4"
    if os.path.exists(out):
        return
    src = f"{prep2.SRC}/{prep2.V[key]}"
    W, H = prep2.probe(src)
    vf = (crop or prep2.crop_expr(W, H, 1920, 1080, *prep2.FRAMES["FULL"])) + \
        f",setpts={out_dur / src_dur:.5f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,format=yuv420p"
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-t", f"{src_dur + 0.25 * src_dur / out_dur:.3f}",
         "-i", src, "-vf", vf, "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-g", "10", "-movflags", "+faststart",
         out])


def weill():
    for wid, src, fw in WEILL:
        out = f"{IMG}/{wid}.jpg"
        if os.path.exists(out):
            continue
        s, reg = faces.split(src)
        im = faces.load(s)
        f = faces.face(im, reg)
        if not f:
            raise SystemExit(f"no face in {src}")
        faces.dario(im, f, fw).save(out, quality=92)


def young():
    for yid, src, scale, dx, dy in YOUNG:
        out = f"{IMG}/{yid}.jpg"
        if os.path.exists(out):
            continue
        s, reg = faces.split(src)
        im = faces.load(s)
        f = faces.face(im, reg)
        if not f:
            raise SystemExit(f"no face in {src}")
        faces.square(im, f, scale, dx, dy).save(out, quality=93)


if __name__ == "__main__":
    mats = [cid for cid, c in SPEC["clips"].items() if c.get("matte")]
    print("mattes:", mats, flush=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        jobs = [ex.submit(matte, cid) for cid in mats]
        speak_freeze()
        # the Wolf: the dollar-bill shot (12.40-13.43 in the landscape copy), 960x540 window on Leo, 1.35 s on screen
        slowmo("wolf_slow", "WOLF", 12.40, 1.03, 1.35, crop="crop=960:540:0:40,scale=1920:1080:flags=lanczos,setsar=1")
        # "CEO": walking in with his detail (montage 16.945-17.425), 0.56 s on screen
        slowmo("ceo_slow", "MONT", 16.945, 0.48, 0.56,
               crop="crop=1280:720:0:43,scale=1920:1080:flags=lanczos,setsar=1")
        # JPMorgan Chase over the J.P.Morgan flag (12.40-13.00) and the JPMorgan tower at dusk (11.77-12.40)
        mont = "crop=1280:720:0:43,scale=1920:1080:flags=lanczos,setsar=1"
        slowmo("flag_slow", "MONT", 12.42, 0.54, 0.705, crop=mont)
        slowmo("tower_slow", "MONT", 11.80, 0.55, 1.13, crop=mont)
        weill()
        young()
        for j in jobs:
            print("matte done:", j.result(), flush=True)
    print("done", flush=True)
