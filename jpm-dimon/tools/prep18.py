"""v18 media (the user's notes on the v17 render, 12 Nov).

- `fired`: the photo run of "a guy who got FIRED" again (user: "I want more photos in that place, so the photos keep on
  happening, and the frame keeps on getting bigger ... some photos are where there's negative space and his face is at
  the side ... at the 7th or 8th photo another person is also coming in ... in the second-last photo there's a wall").
  Nine squares of young Dimon, youngest first, every one alone in the frame and centred on his face at the same size
  (the face box half the square, its centre a little above the middle; the hero a little tighter), the last the
  black-and-white hero:
  assets/img2/yd18_01.jpg .. yd18_09.jpg. Sources: two of the user's old photos and frames of two documentaries
  (KEY@seconds, the keys of tools/prep2.py), found by scanning them for a single large face near the centre.

usage: CV4_DIR=... python3 -I tools/prep18.py [fired]     (DIMON_ROOT as for prep2; faces.py needs OpenCV 4)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep2, faces  # noqa: E402

IMG = prep2.IMG
OLD = "jamie-old-images/jamie-old-images"
SCALE, DY = 2.05, 0.12     # the square's side / the face box's width; the crop centre this far below the face centre
FIRED18 = [  # id, source[#search region fx,fy,fw,fh], square side / face width -- youngest first, each alone in frame
    ("yd18_01", f"{OLD}/jamie-old-image-03.jpg", SCALE),             # at college, long hair (B&W)
    ("yd18_02", "UNT@435.0", SCALE),                                 # the young banker smiling, 1986 (B&W)
    ("yd18_03", "MPB@1169.5", SCALE),                                # in shirtsleeves
    ("yd18_04", "MPB@721.5#0.5,0,0.5,0.8", SCALE),                   # against the dark (the right half: Weill is left)
    ("yd18_05", "MPB@871.5", SCALE),                                 # the Primerica / Travelers years
    ("yd18_06", "MPB@1256.5", SCALE),                                # smiling
    ("yd18_07", "HOW@726.0", SCALE),                                 # the skyline behind him
    ("yd18_08", "UNT@702.0", SCALE),                                 # arms crossed, the sky behind
    ("yd18_09", "UNT@543.0#0.2,0,0.6,1", 1.5),                      # the black-and-white hero (tighter: the film's
]                                                                    # "1985 - 1998" tag sits above the square)


def fired():
    for yid, src, sc in FIRED18:
        out = f"{IMG}/{yid}.jpg"
        s, reg = faces.split(src)
        im = faces.load(s)
        f = faces.face(im, reg)
        if not f:
            raise SystemExit(f"no face in {src}")
        faces.square(im, f, sc, 0.0, DY).save(out, quality=93)
        print("made", out, "face", f, im.size, flush=True)


if __name__ == "__main__":
    for step in (sys.argv[1:] or ["fired"]):
        {"fired": fired}[step]()
