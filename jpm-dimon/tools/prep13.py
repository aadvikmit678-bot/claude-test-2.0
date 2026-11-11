"""v13 media, from the user's uploads of 11 Nov (the Drive folder with the Renaissance pictures and the Bezos clip):
- the seven paintings, enlarged with Lanczos (the boxing picture is 550 px wide) and lightly sharpened, as
  assets/img2/r13_<name>.jpg;
- the 1999 Bezos interview with its two corner graphics (the date, the CNBC logo) blurred out, as
  dimon-src/_v13/bezos_clean.mp4 (prep2 key BEZ). His head reaches the top of the frame, so cropping them would cut it;
- `mattes`: every clip in tools/media_v13.json flagged "matte" gets its subject cut out (hyperframes
  remove-background) as assets/clips2/<id>_cut.webm.

usage: python3 -I tools/prep13.py [pics] [bezos] [mattes]     (no argument: all three; DIMON_ROOT as for prep2)"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageFilter  # noqa: E402
import prep2  # noqa: E402

SRC, IMG, CLIPS = prep2.SRC, prep2.IMG, prep2.CLIPS
PRJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REN = f"{SRC}/_v13/ren"
PICS = {  # name: (file, the long edge to enlarge to)
    "boxing": ("ren_3933.jpg", 2400), "readers": ("ren_8cfa.jpg", 2800), "coins": ("ren_banking.jpg", 2400),
    "jester": ("ren_d68c.jpg", 2600), "treasury": ("ren_new1.jpg", 2600), "altar": ("ren_new2.jpg", 2400),
    "allegory": ("ren_paintings.jpg", 2800),
}


def pics():
    for name, (fn, edge) in PICS.items():
        im = Image.open(f"{REN}/{fn}").convert("RGB")
        k = edge / max(im.size)
        big = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        big = big.filter(ImageFilter.UnsharpMask(radius=2.2, percent=60, threshold=2))
        big.save(f"{IMG}/r13_{name}.jpg", quality=92)
        print(name, im.size, "->", big.size, flush=True)


def bezos():
    out = f"{SRC}/_v13/bezos_clean.mp4"
    prep2.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{REN}/bezoz.mp4", "-vf",
               "delogo=x=8:y=6:w=176:h=50,delogo=x=876:y=4:w=78:h=62", "-an", "-c:v", "libx264", "-crf", "14", "-preset",
               "medium", "-pix_fmt", "yuv420p", out])
    print("bezos", out, flush=True)


def mattes():
    m = json.load(open(f"{PRJ}/tools/media_v13.json"))
    for cid, sp in m["clips"].items():
        if not sp.get("matte"):
            continue
        src, out = f"{CLIPS}/{cid}.mp4", f"{CLIPS}/{cid}_cut.webm"
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
            continue
        subprocess.run([("npx.cmd" if os.name == "nt" else "npx"), "--yes", "hyperframes@0.9.2", "remove-background", src,
                        "-o", out, "--json"], check=True, stdout=subprocess.DEVNULL)
        print("matte", cid, flush=True)


if __name__ == "__main__":
    todo = sys.argv[1:] or ["pics", "bezos", "mattes"]
    for step in todo:
        {"pics": pics, "bezos": bezos, "mattes": mattes}[step]()
