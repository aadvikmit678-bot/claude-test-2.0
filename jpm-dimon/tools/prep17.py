"""v17 media (the user's notes on the v16 render, 11 Nov).

- `meet`: the name run ("Meet Jamie Dimon") is black and white again and ends on h9_a04, the portrait in a suit (user:
  "keep Jamie Dimon's pics till here only ... then directly to the Golden Boy"). The reel's blur-in frame and the two
  whip smears are made from that portrait, as tools/prep14.py made them for the colour one it replaces:
  assets/img2/h9_a04b.jpg, h17_whip1.jpg, h17_whip2.jpg.

usage: python3 -I tools/prep17.py [meet]     (DIMON_ROOT as for prep2)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageEnhance, ImageOps  # noqa: E402
import prep2  # noqa: E402

IMG = prep2.IMG


def meet():
    import prep7
    last = Image.open(f"{IMG}/h9_a04.jpg").convert("RGB")
    prep7.blur_in(last, sigma=11, scale=0.92).save(f"{IMG}/h9_a04b.jpg", quality=90)
    prep7.vsmear(last, 160).save(f"{IMG}/h17_whip1.jpg", quality=90)
    prep7.vsmear(ImageEnhance.Brightness(ImageOps.grayscale(last).convert("RGB")).enhance(1.6), 720).save(
        f"{IMG}/h17_whip2.jpg", quality=90)
    print("meet", flush=True)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["meet"]):
        {"meet": meet}[step]()
