#!/usr/bin/env python3
"""v6 media, made after tools/prep2.py has cut the registered clips and stills (modelled on tools/prep5.py).

1. Note 4, "a guy who got FIRED" (S04, film 15.065-16.200 s): yd6_01 .. yd6_10, square photos of young Dimon centred
   on his face (tools/faces.square, the call prep5.young() makes), youngest first; the last one is the black-and-white
   hero (the same crop as v5's yd5_3). The face fills a little more of each square, photo by photo (square side / face
   width 2.22 -> 1.67, the hero 1.45), so that the face on screen grows with the card. build6.sp_fired_flip shows the
   first nine for two frames each and lands the hero on "fired". Three come from the user's old photos
   (dimon-src/jamie-old-images); the others are documentary frames (KEY@seconds, the keys of tools/prep2.py). The
   user's other old photos show him grey-haired after 1998, as a half face, or too small in a group.

Like prep5.py, it skips files that already exist: delete a file (or change its id) to make it again. The stills are
not registered with ST(), so tools/media_v6.json does not list them.

Run:  cd jpm-dimon && CV4_DIR=/home/user/claude-test-2.0/dimon-work/cv4 python3 -I tools/prep6.py
      (faces.py needs OpenCV 4 from CV4_DIR, for its Haar face detector)
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prep2, faces  # noqa: E402

PRJ, CLIPS, IMG = prep2.PRJ, prep2.CLIPS, prep2.IMG
OLD = "jamie-old-images/jamie-old-images"   # the user's 12 old photos (dimon-src/jamie-old-images, from the Drive)

YOUNG6 = [  # id, source[#search region fx,fy,fw,fh], square side / face width, dx, dy (in face widths) -- youngest first
    ("yd6_01", f"{OLD}/jamie-old-image-03.jpg", 2.22, -0.15, 0.13),                 # at college, long hair (B&W)
    ("yd6_02", "MPB@700.0", 2.13, 0.0, 0.10),                                       # young banker, smiling over his shoulder (v5 yd5_2)
    ("yd6_03", f"{OLD}/jamie-old-image-01.jpg#0,0,0.55,0.6", 2.04, 0.0, 0.12),      # Commercial Credit, 1986, at the podium (B&W)
    ("yd6_04", f"{OLD}/jamie-old-image-05.jpg#0.45,0,0.55,0.65", 1.55, 0.0, 0.10),  # laughing, Weill beside him
    ("yd6_05", "MPB@871.0", 1.89, 0.0, 0.10),                                       # the Primerica/Travelers years (v5 yd5_1)
    ("yd6_06", "MPB@720.0#0.5,0,0.5,0.8", 1.85, 0.0, 0.12),                         # beside Weill (right half of the frame)
    ("yd6_07", "UNT@580.0#0.5,0.15,0.4,0.7", 1.79, 0.0, 0.10),                      # beside the man in glasses (Travelers)
    ("yd6_08", "UNT@619.0#0,0,0.5,0.8", 1.72, 0.0, 0.08),                           # beside Jessica Weill (left half)
    ("yd6_09", "MPB@930.0", 1.67, 0.0, 0.08),                                       # Citigroup, 1998, at the citi podium
    ("yd6_10", "UNT@543.0#0.2,0,0.6,1", 1.45, -0.12, 0.12),                         # the B&W hero (same crop as v5 yd5_3)
]


def young6():
    for yid, src, scale, dx, dy in YOUNG6:
        out = f"{IMG}/{yid}.jpg"
        if os.path.exists(out):
            continue
        s, reg = faces.split(src)
        im = faces.load(s)
        f = faces.face(im, reg)
        if not f:
            raise SystemExit(f"no face in {src}")
        faces.square(im, f, scale, dx, dy).save(out, quality=93)
        print("made", out, "face", f, flush=True)


if __name__ == "__main__":
    young6()
    print("done", flush=True)
