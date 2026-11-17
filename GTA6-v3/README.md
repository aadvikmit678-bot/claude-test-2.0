# GTA 6 edit — v4 (the whole video, 0:00–1:30.7)

v4 is v2 (the desktop session's cut, picked to continue from) with the user's notes, built part by part and now
rendered whole: the FOX 2 cold open, CJ, the voiceover on the user's cut-down script, and v2's ending (the GTA VI logo,
then the date card with the date only):

> That's exactly how millions of adults are going to feel on November 19th when they play GTA 6 for the first time. GTA 6 took 13 years to make. And yet, nobody seems to have moved on. But why are grown adults waiting 13 years for a game that's supposedly just about stealing cars? Because GTA was never just about cars and guns. It was about what it really gave you: freedom. Back to being 10 years old, sitting in front of the family computer, playing Vice City with the volume turned all the way down so nobody could hear the gunshots. With cheat codes like aspirin and panzer scribbled at the back of your notebook. For a kid, it wasn't just a game. It was a psychological escape, an alternate reality. It was everything you imagined adulthood would be. Driving supercars, firing guns, flying planes, and owning an entire city. And while every other game asks you to be the hero, But GTA lets you be the problem. It lets you be the bad guy in a world that looks just like yours. And somewhere along the way, those kids grew up. Today, it's the exact opposite. It's an escape from adulthood, back to the world they once dreamed of living in. And on November 19th, Rockstar takes you back to Vice City, the city where it all started. So if you're still lost in Los Santos this week, don't rush. Take the long way home. Drive slow. Because that 10-year-old playing GTA Vice City never really left. He's just been waiting 13 years to feel that freedom again.

v2 is in git history (commit 193a7c7; `tools/edl.py` + `tools/build.py` still build it); v3 is at 93a94ec.
The `gta6/` folder on this branch is a different session's edit.

## What v4 does (the user's notes)

- **Type** (`TYPE.md`): v2's captions and v2's entrances everywhere, as before the type change (the user), with the
  new moves only where the user wanted them: giant words ("billion", "millions", "Ah shit," behind CJ, "gunshots." with
  the "Instinct" flicker, "bad guy", "Today,", "13 years"), Tesla-style single words, "Los Santos" typed in the "G-mail"
  box, "Take the long way / home.", and Instrument Serif lines in the Dario video's style with a white glow. **White
  type only**, except the black words on reference 7's light cards (the user's choice). Captions do not slide. No
  textures (v2's grain and vignette only). No sound effects.
- **Voiceover** (`tools/vo4.py` → `assets/audio/vo4.wav`, `words4.json`): "and 2 billion dollars", the release line
  and the first "why?" cut ("But" ends on its own dip, before any of that "why"); every silence over 0.3 s cut to 0.2 s.
- **Cold open**: the frame zooms onto the "U.S. economy" highlight (corner blur), then cuts to the money clip on
  "a billion dollars"; CJ "Ah shit,"; on "here we go again" the user's beat-drop clip (from its 0.43 s drop) until "millions".
- **"millions of adults"** grid with GTA VI cells; the 2013 fan's face on "are going to feel"; the GTA VI logo
  (Pre-Load, 2x) landing on "GTA 6".
- **Reference 7** for "GTA 6 took 13 years to make. And yet, nobody seems to have moved on.": tiles in from the top
  left on the grey card, "GTA VI" splitting around the logo, "took 13 years to make." as a caption on top; the white
  card with the black bars closing right after "And yet", "moved on." in the band; square flashes.
- **"But why are grown adults waiting 13 years"**: the GTA V handover (its burned-in "2013" painted out) and the GTA V
  crew; the split frame replaced. **"guns"**: the shotgun from lenojoga.
- **"It was about what it really gave you"**: a fast burst mixing the user's Pinterest cinematic clips with GTA shots,
  posterised and black-and-white flash frames; **"freedom"** big, white, glowing.
- **"Back to being"**: the Vice City car. **"10 years old, sitting in front of the family computer,"**: the user's
  green-screen kid with Vice City gameplay on the TV (`tools/tv4.py`), full screen, then reference 1 / 2's move — a
  bright frame, two negative frames, a white square growing into a card, the picture in the card and the words in glow
  either side. **"playing Vice City"**: the VICE letters (beat-drop clip) for a moment, then v2's Vice City shots.
- **"With cheat codes like"**: the user's notebook clip — the desk, the polaroids lighting up, the notebook opening
  (sped up 1.9x; its zoom into the page left out). **"aspirin and" / "panzer"**: straight cut to the page, cut out of
  its black background and see-through (paper 0.55, the writing and the glow solid) over v2's footage for those words
  (the dentist, Tommy with the gun; Tommy climbing into the Rhino), the clip's own highlight on ASPIRINE / PANZER drawn
  ~2.5x faster (`tools/nb4.py`); the caption below the writing, at v2's low line.
- **"scribbled at the back of your notebook."**: the tank (v2's) through "notebook.". **"For a kid, it wasn't just a game.
  It was a psychological escape,"**: v2.
- **"an alternate reality."**: the user's chasing-dreams clip from its start, half see-through, over the "gta city"
  aerial (stored sideways, turned upright) of the Vice City skyline zooming out. **"It was everything you imagined
  adulthood would be."**: the madebyajit clip from 12 s (the kiss, its car, the embrace), then Tommy & Lance with the
  guns on "would be.".
- **"Driving supercars, firing guns, flying planes, and owning an entire city."**: the screen in four, each phrase's
  clip coming in on its first word with a white flash; the four joined edge to edge, no gap, no glow, floating on black.
- **"And while every other game asks you to be"**: reference 3's curved wall of GTA clips (`tools/gp4.py`), starting
  on the first zoom; the camera as measured on the reference frame by frame -- pans 10 frames apart, most of the way
  in one smeared frame, then easing out over ~7 frames as the blur fades -- right, down-left, up-right.
- **"the hero, But GTA lets you be the problem."**: reference 3's Palmer Luckey part
  (`tools/hero4.py`): the user's Lucia & Jason art with BE THE HERO behind them (`tools/text4.cjs`), the glowing
  jagged outline and glitch strips, then on "the problem." inverted squares, blur and a ghost into the user's bad-guys
  art, both through a soft-edged, colour-fringed lens. **"It lets you be the bad guy"**: v2's B-roll (the store
  robbery, Lucia aiming).
- **"in a world that looks just like yours." ... "It's an escape from adulthood,"**: v2 (the "2013" painted out).
- **"back to the world they once dreamed of living in."**: the Ackman reel's pin board, frame for frame (`tools/pb4.py`
  grabs the pictures): two white frames, the board seen close on the window photo (Vice City at sunset) zooming out to
  the whole board (x2.0 -> x1.0 in 1.35 s, as measured on the reel), 22 GTA pictures one a frame in runs (different
  sizes, taped, some landing on the one before, the bare window between runs), then tilted prints on "they",
  "dreamed", "living"; the words in black on the page.
- **"And on November 19th,"**: v2. **"Rockstar takes you back to Vice City,"**: the Vice City Definitive Edition intro
  (Rockstar Games presents, the logo forming on "Vice"). Then v2 to "Drive slow."
- **"Because that 10-year-old, playing GTA"**: the user's "real people waiting for GTA 5" (the people showing GTA V)
  full screen, then the same card move as "10 years old" with "playing" | "GTA" either side. **"Vice"**: the VICE
  letters (madebyajit). **"never really left."**: the two of them at sunset (bykeipker ~17 s). **"He's just been
  waiting 13 years"**: the user's clip, the guys talking to the kid. **"freedom"**: the big title again over the
  freedom B-roll. The date card ends on the date only ("PRE-ORDER NOW" and the legal line removed).
- Where the shortened pauses would move v2's cut points, the beat pins v2's cut words (`at=` in `edl4.py`).
- Square flashes (white / grey / white rectangles on consecutive frames, as in reference 7) before most cuts.

## The notes on the type renders (latest)

- Normal captions are v2's again; the new moves only where asked: "billion dollars" big on one line, "Ah shit" big
  behind CJ, "millions", "gunshots." (Instinct flicker), "bad guy", "Today,", "13 years", the single words, "Los Santos"
  typed, "Take the long way / home." (centred, slow). Instrument Serif as in the Dario video (white glow, no
  punctuation): kid, game, escape, reality, "And somewhere along the way / those kids grew up", "Rockstar takes you
  back to" (centred under the Vice City logo), started, slow, left; "Because GTA" with GTA in serif; "But GTA lets you
  be" in the Palmer Luckey reel's "John Wick" serif.
- Reference 7 (the Tesla Roadster reel) frame for frame: the zoom with "GTA | logo | VI" already in place, one dim frame,
  "took 13 years to make." spread across the frame in difference blend, the bars a touch faster and curved like the
  reel's (panoramic pinch), "moved on." bold for two frames, faint TV grain on the card.
- The hero -> the problem as the reel's John Wick match cut: the user's Franklin & Trevor art (Drive) with BE THE
  PROBLEM behind them (cut out with `hyperframes remove-background`), the cyan squares, four soft frames, blurred sides.
- B-roll: no goggles face (the GTA V kid runs on), no TV room on "waiting", the burst rebuilt as scoopedfriday cuts
  (five shots, one-frame textures), the kid at the TV from "Back to", "playing Vice City" slowed through "with the
  volume" (no ship), the clip wall's third stop a new tile (a triangle), the GTA city full screen on "city.", one shot
  each for "Take the long way home" and "Drive slow", Tommy through the door on "Vice City", a fourth pin-board print
  on "in"; faint CRT scanlines on the news (HyperFrames' scanlines treatment).

## The user's final (their "GTA6 final" export, with their own music and SFX)

The user mixed their own music and sound effects onto the type3 render (picture unchanged: every frame matches it) and
asked for three last changes, nothing else:
- **The hook** -- "A video game so popular it could cost" -- over other GTA footage: their `_beneg_` clip (Drive
  1ecRRkJs_-dhJJ3C9U1xkv1WJWaWdj0x9, stored sideways, turned upright), its GTA VI montage from 6.25 s as its creator cut
  it (palms, the beach crowd, the speedboat, two characters, the lowriders, the city at night), the captions centred as
  before with a light scrim behind them (the escape line's oval) so the white reads on the beach; then a straight cut to
  the FOX 2 news on "the U.S. economy", which plays as before. In the project this is the only change (`news.html`).
- **No pause between "billion dollars" and "Ah shit"**: the 8 frames of CJ's silent lead-in (frames 293-300,
  4.883-5.0 s at 60 fps) ripple-deleted from picture and sound together, so every other frame and every sound stays
  exactly where the user had it: 90.567 s, 5434 frames. The project keeps the approved timeline (`GAP_FRAMES` in
  `edl4.py`); the cut is made on the render (`gta6-edit/RENDER.md`).
- **The money-counting sound** behind "billion dollars" (in the user's mix, 3.05-4.85 s) taken out; the bass rise
  under it, which runs on into the drop, kept.

The delivered MP4: this project's render up to frame 292 (the new hook, then the news and the money as before), then
the user's own final from frame 301 on; its sound is the user's final mix with the money sound taken out (their added
layer above ~180 Hz, 3.00-4.87 s) and the same 8 frames cut at 4.87 s (10 ms crossfade, in the silence), encoded from
float so their peaks are kept as they were (`final_mix/gta6_final_mix.m4a`).

## Open / render

```bash
cd GTA6-v3/gta6-edit
npx hyperframes@0.9.46 preview      # Studio
npx hyperframes@0.9.46 render --fps 30 --quality delivery --output renders/gta6_v4_full.mp4
npx hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 --output renders/gta6_v4_final_render.mp4   # highest quality, 60 fps
```

## Rebuild

```bash
python -I GTA6-v3/tools/link_sources.py        # once per machine: links the source downloads under their Drive names
cd GTA6-v3
python -I tools/vo4.py                          # the cut voiceover and its word times
python -I tools/logo4.py                        # the GTA VI logo cut-out
python -I tools/tv4.py                          # the green-screen kid with Vice City on the TV
EDL=edl4 python -I tools/prep.py                # cuts only the shots whose spec changed (assets/clips/_spec.json)
python -I tools/nb4.py 0.55                     # the see-through notebook page over its footage (after prep)
python -I tools/gp4.py                          # the tile wall
python -I tools/pb4.py                          # the pin-board pictures
python -I tools/mask4.py && node tools/text4.cjs && python -I tools/hero4.py   # the cut-out, BE THE HERO, the hero / bad guy clip
cd gta6-edit && for id in cj sj2c sm10b sq3a; do   # the people in front of the giant words (VP9 alpha WebM, after prep)
  npx hyperframes@0.9.46 remove-background assets/clips/$id.mp4 -o assets/clips/${id}_fg.webm --quality best; done; cd ..
python -I -X utf8 tools/build4.py               # writes index.html and compositions/
```

Shots from 50/60 fps sources are cut at 60 fps (`HFR` in `edl4.py`) and the tile wall is drawn at 60 fps, so a 60 fps
render keeps their motion; everything else is <= 30 fps footage. prep writes clips with `-fps_mode passthrough`, so ffmpeg 6 (cloud) cuts the same frames with the same timestamps as
the desktop session's ffmpeg 8. The user's reference and B-roll files (beat drop, green-screen kid, Pinterest clips,
the cheat-code notebook, chasing dreams, the hero art, the talking-to-the-kid clip) are downloaded to `gta6-src/` (not
committed) and linked by `link_sources.py`; `hero4.py` reads the hero art and its cut-out mask from there.

`tools/`: `edl4.py` / `build4.py` are v4; `edl.py` / `build.py` v2; `edl3.py` / `build3.py` v3; `edl_v1.py` / `build_v1.py` v1.
