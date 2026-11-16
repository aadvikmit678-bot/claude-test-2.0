"""Cut every shot of edl.SHOTS into gta6-edit/assets/clips/<id>.mp4 (silent, 30 fps CFR, keyframe every 15).
usage: python -I prep.py [id ...]      (no ids: every shot whose spec changed)"""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
edl = importlib.import_module(os.environ.get('EDL', 'edl'))

OUT = os.path.join(edl.PROJ, "assets", "clips")
os.makedirs(OUT, exist_ok=True)
CACHE = os.path.join(OUT, "_spec.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
HANDLE = 0.2

GRADE = {
    "none": "eq=contrast=1.04:saturation=1.03",
    "bw": "hue=s=0,eq=contrast=1.18:brightness=-0.02,curves=all='0/0 0.25/0.18 0.75/0.82 1/1'",
    "dim": "eq=contrast=1.05:brightness=-0.10:saturation=0.85",
    "warm": "eq=contrast=1.05:saturation=1.08,colorbalance=rs=0.04:bs=-0.04",
    "cool": "eq=contrast=1.05,colorbalance=bs=0.05:rs=-0.03",
    # v4
    "blur": "gblur=sigma=16,eq=contrast=1.04:saturation=1.03",
    "nolabel": "delogo=x=884:y=512:w=152:h=62,eq=contrast=1.04:saturation=1.03",      # gta5bye's "2013"
    "bwhi": "hue=s=0,eq=contrast=1.35:brightness=-0.02",
    "nopreorder": "delogo=x=650:y=548:w=622:h=60,delogo=x=204:y=933:w=1510:h=48,eq=contrast=1.04:saturation=1.03",   # the date card: the date only
    # the date card with its date in white (the user: white type only): every pixel in the date's box is unmixed into
    # the card (22,26,34), the white letters and their magenta drop shadow (215,5,221) from G and (R+B)/2; the shadow's
    # part is taken out, so the letters stay white with clean edges and the card is untouched
    "datewhite": "delogo=x=650:y=548:w=622:h=60,delogo=x=204:y=933:w=1510:h=48,eq=contrast=1.04:saturation=1.03,format=gbrp,"
                 "geq=r='st(0,clip(((r(X,Y)+b(X,Y))/2-g(X,Y)-4)/209,0,1));st(1,clip((g(X,Y)-28+21*ld(0))/229,0,1));st(2,between(X,460,1462)*between(Y,466,556));clip(r(X,Y)-ld(2)*(193*ld(0)+10*ld(1)),0,255)':"
                 "g='st(0,clip(((r(X,Y)+b(X,Y))/2-g(X,Y)-4)/209,0,1));st(1,clip((g(X,Y)-28+21*ld(0))/229,0,1));st(2,between(X,460,1462)*between(Y,466,556));clip(g(X,Y)-ld(2)*(10*ld(1)-21*ld(0)),0,255)':"
                 "b='st(0,clip(((r(X,Y)+b(X,Y))/2-g(X,Y)-4)/209,0,1));st(1,clip((g(X,Y)-28+21*ld(0))/229,0,1));st(2,between(X,460,1462)*between(Y,466,556));clip(b(X,Y)-ld(2)*(187*ld(0)+10*ld(1)),0,255)'",
    # the burst's one-frame textures (the scoopedfriday reel): a horizontal whip smear, a negative
    "whip": "avgblur=sizeX=64:sizeY=1,eq=contrast=1.05:brightness=0.02:saturation=1.05",
    "neg": "negate,eq=contrast=1.15:saturation=1.1",
    "poster": "format=gray,eq=contrast=1.5,format=rgb24,lutrgb=r='if(lt(val,85),205,255)':g='if(lt(val,85),18,if(lt(val,175),214,244))':b='if(lt(val,85),12,if(lt(val,175),0,190))'",
}


def build(s):
    src = os.path.normpath(os.path.join(edl.ROOT, edl.SRC[s["src"]]))
    if not os.path.exists(src):
        print(f"  !! {s['id']}: missing source {src}")
        return False
    dur = s["end"] - s["start"] + HANDLE
    sdur = dur * s["speed"]
    pre = []
    if s.get("rot"):                                    # v4: a source stored sideways
        pre.append({"ccw": "transpose=2", "cw": "transpose=1"}[s["rot"]])
    if s["crop"]:
        x, y, w, h = s["crop"]
        pre.append(f"crop={w}:{h}:{x}:{y}")
    grade = GRADE[s["grade"]]
    if s["reverse"]:
        pre.append("reverse")
    if s["speed"] != 1.0:
        pre.append(f"setpts=PTS/{s['speed']}")
    rate = (f"minterpolate=fps={s.get('fps', edl.FPS)}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"   # smooth slow motion
            if s.get("interp") else f"fps={s.get('fps', edl.FPS)}")
    if s["fit"] == "cover":
        vf = ",".join(pre + ["scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos", "crop=1920:1080",
                             grade, rate, "format=yuv420p"])
        cmd = ["-vf", vf]
    elif s["fit"] == "card":
        cw, ch = s["card"]
        vf = ",".join(pre + [f"scale={cw}:{ch}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={cw}:{ch}",
                             grade, f"fps={s.get('fps', edl.FPS)}", "format=yuv420p"])
        cmd = ["-vf", vf]
    elif s["fit"] == "blurfill":   # vertical/square source: sharp copy fit to height over a blurred, darkened cover copy
        base = ",".join(pre) + "," if pre else ""
        fc = (f"[0:v]{base}split=2[a][b];"
              f"[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=40:2,eq=brightness=-0.28:saturation=0.8[bg];"
              f"[b]scale=-2:1080:flags=lanczos,{grade}[fg];"
              f"[bg][fg]overlay=(W-w)/2:0,fps={s.get('fps', edl.FPS)},format=yuv420p[v]")
        cmd = ["-filter_complex", fc, "-map", "[v]"]
    else:
        raise ValueError(s["fit"])
    out = os.path.join(OUT, s["id"] + ".mp4")
    args = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s['sin']:.3f}", "-t", f"{sdur:.3f}", "-i", src] + cmd + [
        "-an", "-fps_mode", "passthrough", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "15", "-keyint_min", "15",
        "-sc_threshold", "0", "-movflags", "+faststart", out]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  !! {s['id']}: {r.stderr[-400:]}")
        return False
    return True


only = set(sys.argv[1:])
done = 0
for s in edl.SHOTS:
    key = hashlib.md5(json.dumps([s, edl.SRC.get(s["src"]), edl.FPS, HANDLE], sort_keys=True).encode()).hexdigest()
    out = os.path.join(OUT, s["id"] + ".mp4")
    if only and s["id"] not in only:
        continue
    if not only and cache.get(s["id"]) == key and os.path.exists(out):
        continue
    ok = build(s)
    if ok:
        cache[s["id"]] = key
        done += 1
        print(f"  {s['id']:6s} {s['src']:9s} {s['sin']:8.2f}  {s['end']-s['start']:.2f}s  {s['fit']}", flush=True)
    json.dump(cache, open(CACHE, "w"), indent=0)
print(f"prepared {done} clips")
