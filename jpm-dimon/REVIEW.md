# Jamie Dimon / JPMorgan Chase: review (v5, the first 30 s)

v5 is built by `tools/build5.py`. Media comes from:
- `tools/prep2.py --spec=media_v5.json`
- `tools/prep4.py`: freezes, the globe picture
- `tools/prep5.py`: mattes and glow, smooth slow motion, Dario-aligned faces, young-Dimon squares
- `tools/make_music.py`: audio

**Rendered:** 0–31.7 s, `renders/jpm-dimon-v5-0-31.mp4`.

**References:** every one was watched again frame by frame at its own frame rate, at the moments you named; the measurements are in `REFERENCES.md`.

**Checked:** each note below against the snapshots (about 110 frames across 0–31.7 s) and, where it applies, side by side with the reference.

## Your notes on v4, one by one
| Note | v5 |
|---|---|
| "in American" written small | Back as it was: "in American" above, "capitalism" in big serif below. |
| "bigger" not animated like Dario; darker; echoes moving; no small copy; more echoes at the sides | Dario's SUDDENLY, frame for frame (details below). |
| JPMorgan Chase not like DISAPPEAR; spelling | Dario's DISAPPEAR (details below). |
| Dimon came in from the side, zooming | His talking video, matted, slides up from the bottom in 10 fps steps with the glow, and lands where the next scene's silhouette stands, hands in frame. No zoom. |
| "most influential man in America": a video of him, mask glow, pops up, photos at his sides like Hemant; subtle zoom on his face on "in America"; fonts misaligned | Hemant's opening and his 22–25 s layout on Dimon's talking video (details below). |
| Textures too heavy; use CRT lines and noise, lighter | The grunge and paper overlays are down from 0.40 / 0.28 to 0.10 / 0.04 (0.05 / 0 on the interview scenes). Noise comes from the registry grain overlay at 6 %, as in the Pattinson film. CRT lines come from the grades, a bit lighter than Hemant's. |
| "He's basically the CEO of Wall Street": Pattinson-style smooth transitions, and the move from "CEO" to "of Wall Street" | "the" (Stanford) arrives still moving and slows into place, as the run does in the Pattinson film. "CEO" eases back into a window with photo cards popping out behind it. Then an inverted frame, and the Wolf arrives moving. |
| The Wolf shot looked cut | It is one continuous shot (12.40–13.43 s of the film), cut after the house frame. It is slowed to 0.77× by motion interpolation (`wolf_slow.mp4`), so no frames repeat. v4 had the player slow it, which repeated frames unevenly and read as a jump at 14.37. |
| The fired photos cut his face; wrong pictures | Three photos of the young Dimon from the documentaries (1990s), cropped square on his face by face detection, head and face whole. The black-and-white portrait is the hero. |
| "By his own mentor" like Dario's "every AI tech bro" | Eight photos of Sandy Weill (yours and documentary frames). Each is aligned by face detection so his face sits at Dario's spot (within 15 px of the same point in every photo), with edges zoom-blurred around a sharp circle. A new photo every 2–3 frames, each creeping in about 3 %, behind four fixed white lines, with "by his own mentor" building at nose height. Then the four-square comes in dark for one frame (Dario's flicker). |
| "and a family" / "grudge" at the bottom | Both centred. |
| "now runs the biggest bank in the world": no change | Unchanged (only the lighter texture). |
| "We bank": textures, quote marks closer, B-roll mixed in, the ghost behind him moving like Fink's | Interview, then B-roll, interview, B-roll (details below). |

### BIGGER, frame for frame like Dario's SUDDENLY
- **Before the word:** a corner square, top left then bottom right, on the reporter shot.
- **Two glitch frames:** first the smeared band, then the crisp black word in a glowing bar.
- **Then:** the white word with its glow on near-black.
- **Echoes:**
  - Rows of repeated, blurred, faint "BIGGER" at the top and bottom rush in and slow down (expo ease-out), the top to the left and the bottom to the right.
  - Faint copies sit at the sides of the word and drift outward.
- **Gone:** the small copy.

### JPMorgan Chase, like Dario's DISAPPEAR
- **Spelling and size:** "JPMorgan Chase" spelled properly, 420 px condensed to 0.7 like Dario's type, about 84 % of the width.
- **Typing:** in place from the left on the reporter's syllables; the newest letter flares.
- **Footage:** the flag, cutting to the JPMorgan tower mid-word.
- **Exit:** two tile-glitch frames (the word gone on the second), then the tower holds a moment.

### "This is the most influential man in America right now", Hemant style
- **Opening:**
  - The grey see-through silhouette turns cream.
  - Live frames flicker through, plus the live strip and the white bars.
  - "This is the **most**" sits left and "**influential**" right, in two sizes on one baseline, kept clear of his head.
  - The white band runs through "influential".
- **Transition:** the blazing white silhouette.
- **Stage:**
  - He talks (matted, with the glow) over a defocused copy of his own shot.
  - Cards land behind him at head and waist height after soft white boxes; red boxes swap two.
  - "man in **America**" then "right **now**" run across his chest.
  - A slow push on his face from "in America" while everything else holds.
  - The seal sits behind his head; a white sweep takes it out.

### "We bank", the Fink Rogan screen
- **Edit pattern:**
  - Interview ("We bank some of these companies").
  - "in 30 countries": the JPMorgan Global China Summit, then Davos on the World Economic Forum stage.
  - Interview ("We bank"), then "countries": London from the air.
  - Interview ("We bank the"), then "World Bank": its building.
  - Interview ("the IMF, we bank the").
  - "United States": with Obama; "government": testifying to Congress.
- **Ghost:** your globe picture behind him (he is matted above it), slowly zooming and drifting. It pulls focus from soft to sharp each time we come back to him.
- **Quote marks:** they hug the words on screen.

## Measured
- **`check` (5 samples, contrast pass off):** ok, 0 errors.
- **Remaining warnings:**
  - The typed letters of "Chase" and the roller years are flagged as brief; the whole word holds, and the years flick by design.
  - WebGL performance notices.
  - Lint density warnings in later scenes, as in v4.
- **Not heard:** the levels were measured, not listened to.

## Open
- **"was fired" reference:** used for "a guy who got fired"; tell me if it was meant for "he was fired" at 48 s.
- **Faces in "by his own mentor":** some of Weill's photos are small. To fill the frame without a seam they are scaled up, so the biggest close-ups are soft. They are on screen for 2–3 frames each.
