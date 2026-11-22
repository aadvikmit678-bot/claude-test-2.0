# Reel DfhzVs8q9NH: "one guy was such a terrible boss" (3.17–5.47 s)

The user asked for this scene, exactly, for "the man who runs the most evil". It is built from:
- the user's red (`new red bg.jpg`, 254/0/0);
- the user's three Fink cut-outs: without horns, with horns, and horns only.

The renderer is `tools/prep_v6.py` (`r_evil`), and its output is `assets/clips/v6_evil.mp4`.

**How it was measured:** frame by frame at 29.97 fps, at full resolution. The head's top and width were tracked per frame, and the type's brightness was sampled per frame.

## The wide shot: the rise

**Background:** flat red, (254, 5, 8) in the reel. There is no texture on the red; the grain is on the man only.

**The rise:** the man rises from the bottom on a fast ease-out. His head's top, as a share of the frame height, by seconds after the cut-in:

| s | 0 | .033 | .067 | .100 | .133 | .167 | .200 | .234 | .267 | .300 | .334 | .5 | .667 | .834 | 1.0 | 1.168 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| top | .893 | .771 | .695 | .622 | .559 | .512 | .474 | .439 | .406 | .384 | .359 | .276 | .229 | .202 | .183 | .167 |

- **Softness:** he is soft throughout (a blur of about 2 px at 1080p). He carries vertical motion blur while he moves fast.
- **Head size:** the head is about 280 px wide, centred at about 0.42 of the width.
- **Grain:** light orange-black speckle on him, almost none at the start.

**The small words:**
- They sit in the middle, centred: Helvetica regular, about 54 px.
- The key word ("guy"; ours is "man") is bold italic, about 80 px, with a soft white glow spot behind it.
- "was such a" is laid out at x 0.13 / 0.50 / 0.87, each word on its own beat. Ours is "who runs the".
- Each word fades in over about 0.1 s, and the group clears at the next group.

**The horns:** they fade in over the last 0.1 s before the cut (from cut-out A to cut-out B).

## The cut: the close-up

**Framing:**
- The close-up is 1.69× closer: the head is about 480 px wide.
- The skull's top sits just inside the frame, with the horns' tips at the top edge.
- He is out of focus at the cut (a blur of about 10 px) and slightly less by the second word (about 6.5 px).

**Grain:** it builds from almost none to heavy by "boss" (on an exponential curve).

**The type:**
- **Face:** a Times-style serif (Liberation Serif here), cream white (255, 248, 240).
- **Bloom:** a heavy white bloom of about 14, 40 and 110 px, plus a 2–3 px colour fringe (red to the right, blue to the left).
- **Order:** the type sits behind him; he covers part of each word.
- **"terrible" (our "most"):** about 1400 px wide, baseline at 0.39 of the height. It fades in as opacity 1 − e^(−t/0.062).
- **"boss" (our "evil"):** about 1600 px wide, baseline at 0.89 of the height. It fades in as 1 − e^(−t/0.040), on its word.
- **Timing:** the cut lands two frames before the first big word.

## Our version

- The same curve, sizes, blur, grain, word layout and fade constants, on the user's red with the user's cut-outs.
- The cut-out stops at his waist, so the torso is continued downwards (mirrored and darkened) so the frame's bottom edge is always covered.
- The old Fink flipbook montage is not used. The red scene covers the whole beat, as the user allowed: "the red part only".
