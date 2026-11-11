"""v15 media (the user's second batch of notes on the v13 render, 11 Nov), from their three uploads:

- `flow`: their Google Flow clip for "18 months of no job. He took up boxing, read biographies" (Drive
  1B3g51J1d9O5iixEFXsYkBKNg4pt1mH3G; 1920x1080, 24 fps, 83 frames, its own captions burned in). The Gemini sparkle in
  the bottom-right corner (x 1704-1775, y 864-935) is removed with ffmpeg delogo. Its three parts are a title (frames
  0-24), the boxer (25-48) and the reader (49-82). The boxer and the reader already run at the narration's pace; the
  title is 1.04 s and the narration's "18 months of no job." takes 2.21 s, so the title's bloom-in plays as it is
  (frames 0-8) and its settled part (frames 9-24, a faint shimmer) is stretched with blended frames. Output:
  dimon-src/_v15/flow_retimed.mp4 at 60 fps, no sound (prep2 key FLOW): 0-2.21 s the title, 2.21-4.653 s the rest.
- `bezos`: their Bezos photo (Drive 1pVdU57Veo973iMvZsSstrxIcBtZ4WG2N) cut out (hyperframes remove-background), cropped
  to him and enlarged 1.76x to the size the Dario reel gives its subject (a head about 410 px tall):
  assets/img2/r15_bezos_cut.png (1408x1126, drawn at left 268, top -24, which puts his head on the frame's centre line).
- `bg`: their warehouse picture (Drive 1iCKQu4CXIavOAgVG3yn0WSFFOs-GQY-E) as the Dario reel uses its background: full
  frame, dim and a little soft: assets/img2/r15_amazon_bg.jpg.

usage: python3 -I tools/prep15.py [flow] [bezos] [bg]     (DIMON_ROOT as for prep2)"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageEnhance, ImageFilter  # noqa: E402
import prep2  # noqa: E402

SRC, IMG = prep2.SRC, prep2.IMG
V15 = f"{SRC}/_v15"
TITLE_S, REST_S = 2.210, 2.443        # the film's spans: S11, and S12 up to the Bezos beat (tools/build15.py checks them)
BEZ_SCALE, BEZ_CROP = 1.76, (200, 100, 1000, 740)


def flow():
    """Three pieces, each cut to an exact number of 60 fps frames (its last frame cloned if it runs short), then joined."""
    a1, a2 = 9 / 24, 16 / 24                              # frames 0-8 as they are; frames 9-24 stretched
    n_title, n_rest = round(TITLE_S * 60), round(REST_S * 60)
    n1 = round(a1 * 60)
    k2 = ((n_title - n1) / 60) / a2
    k3 = REST_S / (58 / 24)
    logo, hold = "delogo=x=1688:y=848:w=104:h=104", "tpad=stop_mode=clone:stop=-1"
    parts = [(f"{logo},trim=end_frame=9,setpts=PTS-STARTPTS,fps=60,{hold}", n1),
             (f"{logo},trim=start_frame=9:end_frame=25,setpts=(PTS-STARTPTS)*{k2:.5f},minterpolate=fps=60:mi_mode=blend,"
              f"setpts=PTS-STARTPTS,{hold}", n_title - n1),
             (f"{logo},trim=start_frame=25,setpts=(PTS-STARTPTS)*{k3:.5f},fps=60,{hold}", n_rest)]
    names = []
    for k, (vf, n) in enumerate(parts):
        names.append(f"{V15}/_flow_p{k}.mp4")
        prep2.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{V15}/flow_ref.mp4", "-vf", vf, "-an", "-r", "60",
                   "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", names[-1]])
    out = f"{V15}/flow_retimed.mp4"
    prep2.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *sum((["-i", n_] for n_ in names), []), "-filter_complex",
               "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]", "-map", "[v]", "-an", "-r", "60", "-c:v", "libx264", "-crf", "13",
               "-preset", "medium", "-pix_fmt", "yuv420p", out])
    for n_ in names:
        os.remove(n_)
    print("flow", out, n_title, n_rest, flush=True)


def bezos():
    raw = f"{V15}/bezos_cut_raw.png"
    if not os.path.exists(raw):
        subprocess.run([("npx.cmd" if os.name == "nt" else "npx"), "--yes", "hyperframes@0.9.2", "remove-background",
                        f"{V15}/bezos_img.jpg", "-o", raw, "--json"], check=True, stdout=subprocess.DEVNULL)
    cut = Image.open(raw).convert("RGBA").crop(BEZ_CROP)
    a = cut.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))   # one pixel in, feathered
    cut.putalpha(a)
    w, h = round(cut.width * BEZ_SCALE), round(cut.height * BEZ_SCALE)
    big = cut.resize((w, h), Image.LANCZOS)
    rgb = big.convert("RGB").filter(ImageFilter.UnsharpMask(radius=2.4, percent=55, threshold=2))
    rgb.putalpha(big.getchannel("A"))
    rgb.save(f"{IMG}/r15_bezos_cut.png", optimize=True)
    print("bezos", rgb.size, flush=True)


def bg():
    im = Image.open(f"{V15}/bg_img.jpg").convert("RGB")
    k = max(1920 / im.width, 1080 / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = (im.width - 1920) // 2, (im.height - 1080) // 2
    im = im.crop((x, y, x + 1920, y + 1080)).filter(ImageFilter.GaussianBlur(2.6))
    im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.82)).enhance(0.58)
    im.save(f"{IMG}/r15_amazon_bg.jpg", quality=92)
    print("bg", im.size, flush=True)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["flow", "bezos", "bg"]):
        {"flow": flow, "bezos": bezos, "bg": bg}[step]()
