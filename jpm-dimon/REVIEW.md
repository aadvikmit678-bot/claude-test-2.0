# Jamie Dimon / JPMorgan Chase: review (v12, the whole film)

v12 is built by `tools/build12.py`. Its media come from `tools/prep2.py --spec=media_v12.json` (clips) and `tools/prep10.py` (the Meet scene's stills), on top of the earlier rounds' media. `notes/v10`, `notes/v11` and `notes/v12` say what each round changed and why.

**Rendered:** `renders/jpm-dimon-v12.mp4`: 85.17 s, 1920x1080, 60 fps, 5,110 frames. `renders/jpm-dimon-v12-preview720.mp4` is a 720p, 30 fps preview.

**Sound:** voices only (the news open, the narration, Dimon's quote); no music and no effects. Integrated loudness -16.8 LUFS, true peak -1.5 dBTP.

## How it was rendered
1. The whole film in one pass (44.6 min, 2 workers).
2. The render was read end to end at 5 frames a second. Three defects were found and fixed in the builder (below).
3. Only the affected stretches were rendered again, from patch builds (`DIMON_ONLY=s12,s13` and so on) with `render --start/--end`: 47.5-51.8 s, 64.6-68.6 s and 77.9-78.3 s. The whole film's plan is over the renderer's 2 GB cap for `--start/--end`; a two-scene build is not.
4. The patches were spliced into the full render with ffmpeg (video re-encoded once at CRF 15, audio copied). The joins were checked frame against frame: the patch and the full render differ by about 1/255 at each edge.

## Checked
- **`check` at 25 times across the film:** ok, 0 errors. Lint has 0 errors and 25 warnings (timeline density and file size notices). The layout warnings are the shots' push-ins overflowing their clip boxes, by design.
- **The rendered file:** four contact sheets at 5 fps covering all 85 s, plus the patched moments and the six joins frame by frame.
- **Clips:** every new clip was checked for a hidden cut inside its used span. The user's two fast montages (`BR2`, `FINF`) were mapped shot by shot by exact seeking.

## Found in the render and fixed
| Found | Fix |
|---|---|
| Under "billions" the climbing-line chart ran into another firm's sign for 0.2 s. The chart shot in the user's B-roll montage is only 0.36 s long. | The chart plays at 0.6x, so the 0.54 s beat stays inside it. |
| "greatest", "JP Morgan" and "fell" held 3 frames into a white flash frame, where their scrim showed as a dark oval. | Those three end on the cut. |
| A negative rectangle crossed Bezos's face for 4 frames as he came in. | Removed; his face is clean from the first frame. |

## The narration's pauses
Three silences are cut out of the voice track, each inside the silence (below -55 dB):
- after "right now.": 0.26 s of 0.40 s;
- after "Street.": 0.40 s of 0.55 s;
- after "grudge,": 0.28 s of 0.37 s.

The later narration still has its sentence gaps of 0.3-0.57 s (after "fired", "job", "Amazon", "Wall Street", "profit", "2004", "fell"). They were not asked about and are untouched.

## Open
- **Bezos:** he is the film's one still photo, shown once with his whole face. The Drive has no footage of him.
- **Higgsfield:** the user offered one generated scene. The connected account is on the free plan with 0 credits and the request was refused. The prompt for the scene ("He took up boxing", a heavy bag) is in `notes/v12/notes.md`.
- **Pinboard words:** all three cards carry their words in the middle in the serif glow. The alternative the user mentioned first was "He built Citigroup" in black at the right of the first card.
- **The 1998 counter:** for about 4 frames its white digits cross the pale FIRED page while the page dissolves under it.
- **The tower film:** its burned-in captions were removed with a blur patch at the centre of the frame. Our own words sit over the patch in every shot that uses it.

---

## The v6 review (the first 30 s, an earlier round)

v6 is built by `tools/build6.py`, which is v5's builder plus your v6 notes. Its media come from:
- `tools/prep2.py --spec=media_v6.json`: clips and stills.
- `tools/prep6.py`: the fired photos, your cyber portrait and its B-roll plate, and the grudge slide's cut-out and backgrounds.
- The S06 interview matte, made with `remove-background`.
- v5's media for everything else.

`tools/rebuild/rebuild_media.sh` remakes all of it from the Drive folder.

**Rendered:** not yet. The project is open for your review; the 0–30 s render waits for your OK.

**Length:** 87.1 s (v5: 93.2 s). "You have to be big…" is cut, so everything from "Meet Jamie Dimon" on plays 6.083 s earlier and is otherwise exactly v5.

**Sound:** voices only, with no music bed and no sound effects. That means the news open, the narration, and Dimon's quote.

## Your v6 notes, one by one
| Note | v6 |
|---|---|
| "JPMorgan Chase" comes in at once, like Dario's DISAPPEAR, centred, not by syllable | One continuous type-on at DISAPPEAR's rate, starting on the reporter's "JP": a letter every 2 frames, the newest letter flaring for one frame. It holds 9 frames, then leaves through Dario's inverted sky-blue tiles. |
| "This is the most influential man in America right now": the Glitchy JPMorgan Chase Cyber Portrait | Your portrait, with Dimon cut out of it, pulling back from 1.75× at the Karp reel's zoom speed (exponential ease, tau 0.48 s). B-roll rolls fast behind him and through him at low opacity. Hemant's side cards keep their flashes, and the seal is there. The text is plain and aligned: no pop-up from the bottom and no continuous flash. |
| The 12 s Stanford shot: a direct cut, no pan | A straight cut. "CEO of Wall Street" is unchanged. |
| "A guy who got fired": many old photos, each zooming slightly, growing smoothly to the hero | Nine photos of young Dimon from your old-photos folder, youngest first, two frames each. Each pops in slightly and settles while the card grows smoothly. The black-and-white hero lands on "fired". |
| "by his own mentor": big, horizontal, one line at the bottom, not in the square, serif glow like Dario | One line at the bottom over the Sandy Weill montage, in Instrument Serif with Dario's bloom-in. Each word arrives blown out on the voice, then settles crisp with a soft glow. |
| "over a bonus and a family grudge": the opening of the reel you sent | "over a bonus" is your cartoon. "and a family grudge" is the reel's first second, frame for frame: Sandy and Joan Weill slide in from the left in 11 frames with motion blur, under a 3×3 grid whose cells light up one by one with white flashes. The background goes colour, then a white burn, then black-and-white, while the couple stays in colour with a thin white edge. |
| "the biggest bank" in Instrument Serif glow, like "capitalism" | Big centred serif glow: "now runs the" small above, "biggest bank" in the hero serif. |
| No background music or sound effects for these renders | The music bed is switched off (`MUSIC = False` in `build6.py`; one line puts it back). There were no other effects tracks. |
| The monologue starts directly at "We bank countries" | The quote starts 0.1 s before "We": "some of these companies in 30 countries" is gone. |
| Interview: the typography stays on the right. B-roll: centred serif glow, like Dario | On him: "We bank", "We bank the" and "we bank the" on the right with the quote marks, his globe picture behind him. On the B-roll, centred serif glow: "countries" over London from the air, "World Bank" centred on its building, "the IMF" over your money animation. |
| "IMF" over the money B-roll, then back to the interview | The money animation runs under "the IMF", then cuts back to him for "we bank the". |
| "the United States government": a completely clear B-roll, the building | The Capitol, ungraded and bright, with no overlay on the building. It "comes in" with the same pull-back as the cyber portrait (from 1.35× on its dome). "United States government" is one serif line along the lawn, like "by his own mentor", so nothing covers the building. |
| Remove "You have to be big…"; go straight to "Meet Jamie Dimon" | Done. "government." is followed by a 0.56 s pause, then the white frame and the name card ("Meet" at 29.17 s). |

## Measured
- **`check` over 0–30 s (12 samples):** ok, 0 errors. Contrast passes on every S06 caption after two fixes: "IMF" got a stronger scrim over the bright bills, and the government line went to the lawn.
- **`lint`:** 0 errors. The 32 warnings are the same density and size notices as v5, in the later scenes.
- **Later scenes:** from "Meet Jamie Dimon" on, each scene's file matches v5 except for clip file names, which round their 0.25 s padding differently after the shift. The roller cards keep v5's drift because they are seeded by v5's times.
- **Pauses in the voice track (measured, not listened to):**
  - "…in the world." to "We bank": 0.6 s.
  - Dimon's own pauses: 0.23 s and 0.35 s.
  - "government." to "Meet": 0.56 s.

## Open
- **Fired photos:** they flip at 2 frames each, so each photo's small zoom barely shows. At 3 frames each the faces read better, and the flip takes 0.3 s longer.
- **"Show Me MODS":** I took the mentor style to be the Dario serif glow this film already uses. Send a frame of the MODS caption if it should look different.
- **Music:** the bed was cut for 93.2 s. The film is now 87.1 s, so the bed needs a re-cut when music comes back.
- **Money animation:** the source is 736×414, so at full frame it is a little soft. The bills move, and the grain hides most of it.
- **Government line:** it sits on the lawn rather than the middle of the frame. Centred, it would sit on the white building and cover it. Say if you want it in the middle anyway.

---

## The v5 review (previous round)

v5 is built by `tools/build5.py`. Media comes from:
- `tools/prep2.py --spec=media_v5.json`
- `tools/prep4.py`: freezes, the globe picture
- `tools/prep5.py`: mattes and glow, smooth slow motion, Dario-aligned faces, young-Dimon squares
- `tools/make_music.py`: audio

**Rendered:** 0–31.7 s, `renders/jpm-dimon-v5-0-31.mp4`.

**References:** every one was watched again frame by frame at its own frame rate, at the moments you named; the measurements are in `REFERENCES.md`.

**Checked:** each note below against the snapshots (about 110 frames across 0–31.7 s) and, where it applies, side by side with the reference.

### Your notes on v4, one by one
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

#### BIGGER, frame for frame like Dario's SUDDENLY
- **Before the word:** a corner square, top left then bottom right, on the reporter shot.
- **Two glitch frames:** first the smeared band, then the crisp black word in a glowing bar.
- **Then:** the white word with its glow on near-black.
- **Echoes:**
  - Rows of repeated, blurred, faint "BIGGER" at the top and bottom rush in and slow down (expo ease-out), the top to the left and the bottom to the right.
  - Faint copies sit at the sides of the word and drift outward.
- **Gone:** the small copy.

#### JPMorgan Chase, like Dario's DISAPPEAR
- **Spelling and size:** "JPMorgan Chase" spelled properly, 420 px condensed to 0.7 like Dario's type, about 84 % of the width.
- **Typing:** in place from the left on the reporter's syllables; the newest letter flares.
- **Footage:** the flag, cutting to the JPMorgan tower mid-word.
- **Exit:** two tile-glitch frames (the word gone on the second), then the tower holds a moment.

#### "This is the most influential man in America right now", Hemant style
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

#### "We bank", the Fink Rogan screen
- **Edit pattern:**
  - Interview ("We bank some of these companies").
  - "in 30 countries": the JPMorgan Global China Summit, then Davos on the World Economic Forum stage.
  - Interview ("We bank"), then "countries": London from the air.
  - Interview ("We bank the"), then "World Bank": its building.
  - Interview ("the IMF, we bank the").
  - "United States": with Obama; "government": testifying to Congress.
- **Ghost:** your globe picture behind him (he is matted above it), slowly zooming and drifting. It pulls focus from soft to sharp each time we come back to him.
- **Quote marks:** they hug the words on screen.

### Measured
- **`check` (5 samples, contrast pass off):** ok, 0 errors.
- **Remaining warnings:**
  - The typed letters of "Chase" and the roller years are flagged as brief; the whole word holds, and the years flick by design.
  - WebGL performance notices.
  - Lint density warnings in later scenes, as in v4.
- **Not heard:** the levels were measured, not listened to.

### Open
- **"was fired" reference:** used for "a guy who got fired"; tell me if it was meant for "he was fired" at 48 s.
- **Faces in "by his own mentor":** some of Weill's photos are small. To fill the frame without a seam they are scaled up, so the biggest close-ups are soft. They are on screen for 2–3 frames each.
