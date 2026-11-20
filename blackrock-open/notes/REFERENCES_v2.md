# BlackRock opening — references re-watched (v2)

Every reference was run through the watch-video steps (hook sheets at 15 fps, body every 3.5 s, transcript), then the
parts that map to our beats were read frame by frame at full size, and their camera motion was measured per frame
(similarity transform between frames: zoom step, cumulative zoom, pan) with `scratchpad/motion.py`.

## 1. X / Hex creative reel (DelkyjLP4p_) — the NYSE floor photo (0–5.4 s, 24 fps)

**Camera — snap moves, then holds (not a slow continuous zoom, not a flicker):**

| t (s) | move (measured) |
|---|---|
| 0.00–0.33 | push-in 1.00→1.25, ease-out: +5.1 %, +1.8 %, +0.66 %, +0.15 % per 2 frames |
| 0.33–0.50 | hold |
| 0.50–0.75 | push-in 1.26→1.70 with a pan up-left (−147 px/frame at the peak, motion blur) |
| 0.75–1.00 | hold |
| 1.00–1.35 | whip right (+87 px/frame peak), settles |
| 1.45–1.75 | push-in 1.70→2.36 with a pan down (+277 px/frame peak) |
| 1.90–2.20 | whip left (−380 px/frame peak) |
| 2.33–2.60 | whip up-right |
| 2.75–3.00 | pull-out 2.33→1.08 (ease-out) |
| 3.00–3.30 | hold on the whole photo |
| 3.33–3.90 | pull-out continues and the photo becomes a **small print on white** (white border, soft shadow) |
| 3.9–4.3 | the print drifts and tilts slightly on white |
| 4.38 | cut back into the photo, then a whip smear to white, then live footage |

Every move is ~6–8 frames (0.25–0.33 s) with a strong exponential ease-out; holds are 0.25–0.5 s.

**The glow (what lights up):** the monitor screens — real object shapes, 30–200 px wide on a 1276 px frame — snap to
flat white (luma > 228, no colour) with a soft bloom. 3–9 are lit at once; each stays lit 1–4 frames (24 fps); the
set changes every 1–3 frames; a tall pillar lights now and then. Nothing lights during a whip. No round light blobs.

**Texture / grade:** faded film — blacks lifted (1st percentile luma 21, shadows RGB 39/31/35, warm-magenta),
highlights compressed (~196–240), low saturation (HSV S ≈ 31–45 of 255); centre-focused: the middle column is about
2× sharper than the edges (Laplacian 44 vs 15–23), sharpest band just above centre; light grain (0.4–0.9).

**Type:** small white serif with a glow, centred ("This", "in the 1980s,", "it's chaos,", "hundreds of men").
(For our film the captions stay in the Jensen reel's Helvetica, per the user.)

**For us:** the panel's own footage with the X-creative grade and focus, snap push-ins / whips with ease-out and
holds, and the **people's own silhouettes** lighting to flat white (as the screens do): 2–5 at a time, 2–6 frames each
at 60 fps, the set changing every 2–6 frames; never during a whip.

## 2. tfg intros reel (DNm1v08zsZM) — "each person's frame comes, the slow typography behind" (30 fps, 1280×400)

**Karp ("Cryptarch"), light page 0.00–2.07 s** (every 3rd frame read at full width):

| t (s) | what happens |
|---|---|
| 0.00–0.10 | warm cream page (RGB ≈ 240/226/218) with a faint paper grain, empty |
| 0.20 | the top of his head enters at the bottom centre; the small label starts: "C r y …" |
| 0.30–0.50 | the label types in letter by letter, left to right, widely letter-spaced, grey italic serif (≈ 6 % of the height), centred just above the middle |
| 0.30–0.60 | the giant word's letters appear far apart, faint pink, smeared sideways (horizontal motion blur) |
| 0.60–1.20 | the letters close up to their places and fill from faint to solid pink-red; the word is tall condensed Didone caps, **repeated** ("…TARCH CRYPTARCH CRYPT…") and running off both edges; letters ≈ 75 % of the height |
| 0.90–1.10 | the label goes darker and bolder; the rising head now covers part of it (the label is behind the person) |
| 1.20–2.07 | the giant word keeps growing slowly (≈ +25 % in 0.8 s) until the letters fill the height |
| 1.40 | a dark-red / black ink splatter bursts beside his head; he turns black and white over ~0.1 s |

**The rise (measured, head top in a 400 px frame):** 398 (0.10 s), 357, 322, 287, 256, 228, 200, 179, 157,
138 (1.00 s), 120, 105, 92, 79, 70 (1.50 s), 60, 53, 46, 40, 37 (2.00 s) — one slow ease-out of ≈ 2.1 s (close to a
quadratic ease-out), from fully below the frame to the head ≈ 9 % from the top; still creeping up at the end.
The person is a cut-out of his speaking video (he keeps gesturing), about half the frame tall at rest.

**Dark page 2.07–2.87 s:** hard cut. Charcoal (≈ 55/55/50); the same giant word in dark grey just above the
background; the person in black and white at the same place; a new word as the label (white italic serif).
Then 2.87–4.47: title cards ("Oligarchic", "Aporetic"): a big grey regular serif with a small bold mono word on it;
a soft-edged light page wipes in from the left over the dark one (3.07–3.27 s).

**Vance ("Exarch") from 4.50 s:** the same build, the giant word already up as the page appears, him rising
4.8–5.6 s, a black brush-stroke bar across his eyes at 5.7 s, dark B&W page from 6.07 s.

**For us:** the Dimon intro exactly like this: cream page; "JAMIE DIMON" tiled across the width in tall condensed
Didone caps, letters sliding together with a sideways blur and filling to pink, then slowly growing; Dimon's
speaking cut-out rising on a ~2 s quadratic ease-out (no fast pop); the splatter and the change to B&W by the head;
hard cut to the dark page. Captions stay the Jensen Helvetica at the bottom.

## 3. Bill Ackman — Metro Media House reel (25 fps) — "His name's Bill Ackman" (9.4–12.0 s, every frame)

| frame (t) | what happens |
|---|---|
| 236–247 (9.44–9.88) | the Wolf shot, caption "was all this legal?" (white sans, words added one by one, the newest grey for a frame) |
| **248 (9.92)** | **whole-frame negative** (the flash) |
| 249 (9.96) | positive again, punched in ~10 % (a jump, not a move) |
| 250 (10.00) | the negative blended with the next picture (his face showing through, washed) |
| **251 (10.04)** | **plain white frame** |
| 252–259 (10.08–10.36) | white page; a small rectangular photo card of him (≈ 255×408 px of 1276×718) in the centre, growing slowly (≈ +25 % in 0.3 s) and easing left; "His" fades in grey at the left, then "name's" in light grey |
| 260 (10.40) | the card is cut to big (fills the right two thirds, bleeding off the edges) |
| 260–267 (10.40–10.68) | hold with a slight drift; "His name's" black; "Bill" appears light grey (10.56) and goes black (10.64) |
| 268 (10.72) | one **pixelated** (mosaic) frame of the photo |
| 269 (10.76) | negative of the next picture with a sideways blur (the text inverted with it) |
| 270 (10.80) | the negative blended into the positive |
| 271–288 (10.84–11.52) | dark close-up of him (hand raised), slow push; "His name's" small white over "Bill Ackman." larger white, left of centre; a small warm orange light dot at the left that fades |
| 289–290 (11.56–11.60) | negative + a zoom jump (the text grows with the picture) |
| 291–292 | negative of the next shot, letterboxed on black |
| 293 → | next shot; small white words land one by one at fixed spots ("And", "the", "thing") |

**Type:** a clean grotesque (Helvetica/Inter class) — the small line (≈ 3.5 % of the height) over the name (≈ 6 %),
left-aligned at the left third; each word arrives light grey and settles to full colour in 1–2 frames.
**Transitions:** 1 negative frame → (blend) → 1 white frame; pixelation frame → blurred negative → blend; every
transition is 2–4 frames. **Motion:** slow pushes (≈ 3 %/s) on holds; the card's small push then a cut to big.

**For us (Dimon):** the panel close-up with a slow push (no fast zoom) → negative frame → blend → white frame →
the light page; words built one by one in the grotesque, grey → black; a pixelation + negative to leave it.

## 4. Larry Fink — Metro Media House reel (30 fps) — "His name's Larry Fink" (7.4–10.3 s, every 2nd frame)

| t (s) | what happens |
|---|---|
| 7.40–7.73 | previous shot (Bet-David) with a quote; a ghosted Fink photo double-exposed on the left |
| **7.80** | **whole-frame negative** |
| 7.87 | white page; a rectangular photo card (Fink in B&W, cut out, on a red BlackRock-logo background), big (≈ 58 % of the width) |
| 7.87–8.47 | the card **shrinks** with an ease-out (fast first, then slow) to ≈ 33 % of the width; "His" then "His name's" appear small, bold, black, above its top-left corner |
| 8.47–8.73 | "Larry Fink" assembles **letter by letter in random order** under the card's bottom-right corner, each letter light grey first, then black |
| 8.60–8.80 | at the same time a **huge, very light grey "Larry Fink"** (≈ 40 % of the height, same grotesque) fills in behind the card across the whole width, letters in random order, running off both edges |
| 8.80–9.07 | hold |
| 9.07 → | cut to dark footage; the next words land one by one, small white ("And", "And the thing", …) |

**For us:** the light-grey giant name behind (random letter order, grotesque) is this channel's "name at the back";
the intro reads in under 1.3 s; one negative frame in, a hard cut out.

## 5. VC roles reel (DdwXUrwtqJO) — the red box "probably wrong." (25 fps, 720×1280)

| frame (t) | what happens (box size measured per frame) |
|---|---|
| 86–91 (3.44–3.64) | light grey page (radial, lighter centre); a small photo card with "investing" left and "money" right (black grotesque), "own" in white over the photo |
| **92 (3.68)** | **hard cut**: the box is there at once over the same photo — see-through red (composite ≈ 232/109/111 on the light grey, so the red is ≈ 75 % opaque), thin dark outline, four black square handles at the corners, white serif "probably wrong." filling ≈ 85 % of its width; box 70.4 % of the frame width, aspect 3:1 |
| 92–99 (3.68–3.96) | it **settles bigger in steps held 2 frames each (12.5 fps)**: 70.4 → 75.0 → 77.8 → 79.0 → 79.4 % — an ease-out (remaining gap roughly halves each step); the red deepens as it settles (G 109 → 78, i.e. more opaque) |
| 99–110 (3.96–4.40) | hold, no movement |
| 110–124 (4.40–4.96) | the whole frame starts drifting left, accelerating, still in 2-frame steps, then a whip into the next page (the box leaves with the frame — it does not slide out on its own) |
| 127 → | grey page, a huge faint grey serif line behind ("…'s what actually…"), small serif words land one by one in front ("Here's" → "Here's what" …) |

**For us:** the box cuts in already on his face (no fade, no slide), settles from 88.5 % to 100 % in 2-frame steps over
~0.3 s, deepens a little, then stays still on his face until the shot cuts away — no exit animation. A square (the
user), lower opacity so his face shows (≈ 0.45–0.5), the words small inside it.

## Stepping (low frame rate) per reference — measured frame-to-frame differences

| reference | motion cadence |
|---|---|
| VC red box settle / exit | stepped: changes every 2nd frame (12.5 updates/s) |
| tfg rise (30 fps) | every frame: 14, 14, 13, 13, 12, 11, 11, 12, 12, 10, 10, 10, 9, 9, 10 … 2, 2, 1 px/frame — one smooth quadratic ease-out ≈ 1.95 s (400 px frame; ≈ 3.5 % of the height per frame at the start) |
| X creative moves (24 fps) | every frame (snap moves with motion blur) |
| Ackman MMH card / type (25 fps) | every frame; words switch on whole (grey → black in 1–2 frames) |
| Fink MMH card shrink (30 fps) | every frame for 0.45 s, then slow |

## 6. Hemant Taneja video (24 fps) — the flash on a person who is talking (0–2.0 s)

The talking head's **whole silhouette** becomes a flat, glowing cream-white shape with a soft halo (not a full-frame
flash). Measured per frame (S = silhouette, v = his normal video):
`SSSvSSSSSvvSSSSSSSSSSvSvSSSSSvvSSSSSSvvSvvvvvvvv` — for ~1.6 s the silhouette holds most frames, with 1–2-frame
glimpses of the real video at irregular spots; its brightness steps (183 → 192 → 163 → 158 → 231 → 220 → 213) every
3–6 frames; occasional white rectangular glitch blocks; then the normal talking video returns. The words build
around his head one by one and stay.
(The user: Hemant, Dario and the earlier analyses are already good; use them, don't over-transition.)

## 7. Solomon DJ video (the user's, 1080×1920, 30 fps, 27.2 s)

Usable for "a part-time DJ": him at the decks close (17 s), with the mic (23–24 s), hand up at the decks (6 s, 20 s),
the D-SOL screen with CO2 jets and crowd (4–5 s), stage jets (9–12 s, 21–22 s, 25–26 s). Crop to 16:9 from the
vertical frame.

## 8. Mafia / Attention Compounds (De9yb6rMm2s, the Sam Altman opening) and the Nvidia (Jensen Huang) reel

Frame-by-frame write-ups from earlier in this session: `reel-analysis/mafia-trae-stephens/ANALYSIS.md` and
`reel-analysis/nvidia-weaponized-delusion/ANALYSIS.md` (re-read for this rebuild). Key rules kept: the picture changes
0–1 frame before the phrase; one phrase = one visual idea; flipbooks 2 frames a picture; Nvidia captions are white
bold Helvetica caps appearing whole on the word; hold into the pauses.

## The user's rules for this rebuild (Nov 20)

1. Exactly the references' pacing and frame rate — no extra zoom in/out, bounce, pan, push or flash.
2. **Plain cuts** between shots by default; no transition flashes / glows / zoom transitions where a cut works.
3. **Videos, not photos**: BlackRock / Fink / JPMorgan clips for the montages; no static photos with zooms.
4. Captions (the storyline) in the Jensen reel's Helvetica caps; the special display type stays.
5. No SFX.
