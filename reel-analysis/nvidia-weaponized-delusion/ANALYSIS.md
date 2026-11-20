# Reel analysis — "Nvidia: a 10-year exercise in weaponized delusion"

Source: https://www.instagram.com/reels/DdB8LATJ_1z/ — 960×720 (4:3), **24 fps**, 1357 frames, 56.66 s, stereo.
Measured frame by frame: every frame of the hook (0–6.5 s) read, a cut detector over all 1357 frames, word timings
(whisper small.en, cross-checked against the audio's dips), the sound's high-band onsets (hits, clicks) and its beat.
Frame numbers below are 0-based at 24 fps (frame n starts at n/24 s). Images: `img/`.

## Transcript (as the creator wrote it — the on-screen words settle two mishearings)

> Everyone thinks Nvidia is a chip company. It isn't. It is a 10-year exercise in **weaponized delusion**. In the
> mid-2000s, Jensen Huang intentionally sabotaged his own profit margins. He forced expensive, parallel computing
> software called CUDA into every single gaming chip his company made. *[Jensen, keynote: "One of the most interesting
> and most exciting architectural advantages that we're bringing to this generation. Okay."]* Wall Street analysts
> laughed at him. Shareholders demanded he stop. He was burning millions on an ecosystem for a scientific market that
> technically did not exist yet. He didn't just ignore them. He doubled down for almost a decade. Then in 2012, a
> neural network called AlexNet woke up. *[Jensen, podcast: "We saw AlexNet, this new algorithm that is completely
> different (from) computer vision algorithms (before it)…"]* It needed immense parallel processing to train. Nvidia
> was the only company on earth with the infrastructure already built. Jensen hadn't predicted the AI era. **He
> attracted it.** Most founders optimize for the next quarter. The dangerous ones build the infrastructure for a future
> nobody else can see yet. They don't react to markets. They force the market to react to them.

- The hook's word is **DELUSION** (red card, frames 119–134). Speech-to-text hears "illusion" because the *d* of
  "weaponized" runs into it; with the context given, the same model hears "delusion".
- 46.7 s reads **HE ATTRACTED** on screen (heard as "he had trapped it").

## 1. The hook, frame by frame (0 – 6.04 s = frames 0–144)

Structure: **myth → name → claim → denial → reframe → payoff → story**, one new visual idea per phrase, and between
them 1–2-frame "punctuation" frames (colour negatives, black, a white square, a blank card, cyan). The hook is cut to
the **words**; the body later cuts to the **beat**.

| Frames | Time (s) | Picture | Text on screen | Voice / sound |
|---|---|---|---|---|
| 0–1 | 0.00–0.08 | Jensen on stage at a Microsoft event (Windows logo top-left), live footage, camera panning (logo slides ~14 % of the width in 0.45 s) | — | sound starts (transient at 0.02) |
| **2** | 0.083 | **same, colour negative** (white jacket, cyan face) | `EVERYONE THINKS` appears | "Every-" starts here · hit |
| 3 | 0.125 | normal | same | |
| **4** | 0.167 | **colour negative** again | same | |
| 5–14 | 0.21–0.62 | normal, still panning | `EVERYONE THINKS` | "…one thinks" |
| **15** | 0.625 | **3×3 tile grid** (tiles 320×240 with thin dark gutters): pure white / black tiles, centre tile black with big `NVIDIA` | `NVIDIA` (big) | gap between words · hit |
| 16–18 | 0.67–0.75 | grid resolving: each tile shows white, black or the **new photo** | `NVIDIA` | "Nvidia" starts frame 16 |
| 19–33 | 0.79–1.38 | Jensen holding two gaming laptops on a black stage (live footage); the grid seams stay faintly visible | `NVIDIA` big, centre, over his chest | "…vidia" |
| 34 | 1.417 | same, no text | — | short gap |
| 35 | 1.458 | same | `IS A CHIP COMPANY.` (small) | "is a chip…" |
| **36** | 1.500 | **negative of the laptops shot** (caption inverted with it) | caption | "chip" |
| **37** | 1.542 | **negative of the next shot** with a **solid square over the chip** (a white square before inversion) | caption | |
| 38–49 | 1.58–2.04 | a hand holding a chip on black; a crisp **square "spotlight" box** (brighter, warmer) around the chip | `IS A CHIP COMPANY.` | "company" |
| **50**, **53** | 2.083, 2.208 | **black frames** (picture off, caption stays) — a two-blink strobe | caption | |
| 51–52, 54 | | chip shot | caption | |
| **55** | 2.292 | **negative** of the chip shot | — | |
| **56–57** | 2.33–2.38 | **solid cyan** (red's negative) | — | "It" |
| 58 | 2.417 | **solid red card** (#A00000 range, faint vertical streak texture) | `IT` — pops one frame bigger, already in its final place left of centre | **hit** (2.44) |
| 59–61 | 2.46–2.54 | red | `IT` | "isn't" |
| 62–72 | 2.58–3.00 | red, no movement | `IT ISN'T` — "ISN'T" joins on its syllable; held 10 frames into the pause | pause 2.9–3.05 |
| **73–109** | 3.04–4.54 | **GPU flipbook**: ~18 graphics-card board photos from product spec pages (labelled call-outs, smeared headlines "ENGINEERED FOR A BRIGHTER TOMORROW", "BUILT FOR WHAT'S NEXT"); **a new card every 2 frames (12 a second)**; mostly white pages with dark-page runs at 73–75, 84–86, 94–96, 104–106 | small lowercase words placed around the card: `it` `is` (75), `a` (78) on the top row; `ten` (83), `year` (89), `exercise` (96) on the bottom row; **difference blend** (black on white pages, white on dark); the word layer slowly zooms out | "It is a 10-year exercise in" · **a click every 2 frames** (12.2 Hz) · hit at 73 |
| 108–109 | 4.50–4.54 | last card, white page | all six words | |
| 110–117 | 4.58–4.88 | **red card with a wet-glass texture** (droplets, streaks) | `WEAPONIZED` — giant tall condensed caps (~65 % of the width) | "weaponized" starts frame 110 |
| **118** | 4.917 | red, **empty** | — | |
| 119–120 | 4.96–5.00 | red | `DELUSION` | "delusion" |
| **121** | 5.042 | red, **empty** | — | |
| 122–134 | 5.08–5.58 | red, no movement | `DELUSION` | |
| 135 → | 5.625 | **cut to the story**: young Jensen (beige jacket, purple set, live) | `IN THE MID 2000.` | the narrator says "In the mid-2000s" at 6.04 — **picture and caption 10 frames early** (a J-cut) |

### Timing rules (measured)
- **Text lands on the syllable**: the caption or keyword appears within −1…+1 frame of the spoken onset
  (EVERYONE 2/2, NVIDIA 15–17/16, IS A CHIP COMPANY 35/~36, IT 58/57, ISN'T 62/61, WEAPONIZED 110/~110).
  Flipbook micro-words: 0–4 frames after their syllable.
- **The picture changes 0–1 frame before the phrase** (the cut leads the voice).
- **One phrase = one visual idea**; inside a phrase only 1–2-frame punctuation (negative, black, blank, square).
- **Holds go into the pauses**: "IT ISN'T" holds 10 frames of near-silence; "DELUSION" holds 13 frames, then the
  story picture arrives 10 frames before the next sentence.
- Durations: 15 / 19 / 21 / 17 / 37 / 25 frames for the six beats; flipbook images 2 frames; punctuation 1–2 frames.

### Type (three scales + one layout)
1. **Caption chunks** — white, bold, tightly tracked grotesque in caps (Inter Display Bold / Helvetica Now Display
   class), ~46 px on 720 (≈ 6.4 % of the height), centred, ~83 % down; no box, no shadow. The whole chunk appears at once.
2. **Keyword over the picture** — the same grotesque, ~75 px caps, dead centre (`NVIDIA`).
3. **Red cards** — a tall condensed grotesque in caps (Bebas Neue / League Gothic class), white, ~125 px (`IT ISN'T`)
   to ~170 px (`WEAPONIZED`); words fill in place, left-to-right, the first one popping one frame bigger.
4. **Scattered micro-words** — regular-weight lowercase grotesque ~26 px, in difference blend, spaced across two rows
   around a central object (zig-zag reading), revealed word by word.

### Colour and texture
Dark real footage (the myth) → **red** for the truth, with **cyan** (red inverted) as the 2 bridge frames → bright
white/dark product pages for the list → red again for the payoff. Colour negatives are whole-frame (captions invert too).
Textures: vertical streaks on the first red, wet glass on the payoff red, smeared headlines on the product pages.

### Sound
A **hit on every scene change of the hook** (frames 2, 15, 58, 73, 110); **one click per flipbook image** (12 a second,
a shutter/slide click); a bass bed that swells through the hook (+11 dB from 0 to 4 s); the voice is close and dry.
The music runs at **83.3 BPM** (a beat every 0.72 s = 17.3 frames). See `img/hook_spectrogram.jpg`.

## 2. The body (6.04 – 56.6 s): 54 shots

**Cadence**: from the first story cut, **one shot per beat — 15–19 frames, median 17–18** (83.3 BPM). The first ten body
cuts sit within −76…+64 ms of the beat; later the cuts follow the phrases. **Captions** are 1–3-word chunks in the
style of scale 1 that change on the cut (so they ride the beat, up to ~0.3 s after the words). Picture logic: **real
footage of the person for every claim about him** (Jensen across 20 years), **industry demos for abstract nouns**
(each with a small source credit), **film stills for the crowd** (Wolf of Wall Street for "Wall Street analysts"),
**white type cards for turning points**.

| # | Frames (len) | Time | Picture | Caption |
|---|---|---|---|---|
| 1 | 146–160 (15) | 6.08 | young Jensen, purple set | IN THE MID 2000. |
| 2 | 161–179 (19) | 6.71 | Jensen in black polo, black background | JENSEN HUANG |
| 3 | 180–196 (17) | 7.50 | Jensen at a whiteboard | INTENTIONALLY |
| 4 | 197–214 (18) | 8.21 | Jensen interview, dark suit | SABOTAGED |
| 5 | 215–231 (17) | 8.96 | Jensen in a library | HIS OWN PROFIT |
| 6 | 232–248 (17) | 9.67 | Jensen, green jacket | MARGINS |
| 7 | 249–265 (17) | 10.38 | Jensen holding up a GPU on stage | HE FORCED EXPENSIVE |
| 8 | 266–282 (17) | 11.08 | hexagon fisheye render | PARALLEL |
| 9 | 283–301 (19) | 11.79 | car aerodynamics sim (Siemens / Mercedes-Benz) | COMPUTING SOFTWARE |
| 10 | 302–319 (18) | 12.58 | NVIDIA CUDA badge on white | — |
| 11–17 | 320–346 (3–5 each) | 13.33 | **GPU flipbook #2**: cards on "PERFORMANCE THAT GOES FURTHER" pages, dark/white alternating | — ("every single gaming chip his") |
| 18 | 347–364 (18) | 14.46 | NVIDIA Shield handheld | HIS COMPANY MADE |
| 19 | 365–494 (130) | 15.21 | **Jensen keynote clip with his own sound** | his words, e.g. AND MOST EXCITING |
| 20 | 495–516 (22) | 20.62 | Wolf of Wall Street still | WALL STREET |
| 21 | 517–532 (16) | 21.54 | DiCaprio laughing | LAUGHED AT |
| 22 | 533–566 (34) | 22.21 | collage of B&W boardroom photos over a blurred man (1-frame flash at 542) | SHAREHOLDERS |
| 23 | 567–584 (18) | 23.62 | ship in a shipyard (Siemens / HD Hyundai) | HE WAS |
| 24 | 585–601 (17) | 24.38 | jet airflow sim (Cadence / Boeing) | BURNING MILLIONS |
| 25 | 602–619 (18) | 25.08 | city aerial with green network lines | ON AN ECOSYSTEM |
| 26 | 620–636 (17) | 25.83 | 3D medical render (Ansys) | SCIENTIFIC MARKET |
| 27 | 637–647 (11) | 26.54 | lab instrument | SCIENTIFIC MARKET |
| 28 | 648–690 (43) | 27.00 | **white card**: `TECHNICALLY` big condensed, then `DID` `NOT` `EXIST` `YET` small, spread on one line, one by one | — |
| 29 | 691–705 (15) | 28.79 | Jensen on stage before a big screen | HE DIDN'T |
| 30 | 706–722 (17) | 29.42 | Jensen on a dark stage | JUST IGNORE THEM |
| 31 | 723–741 (19) | 30.12 | Jensen interview, yellow tie | HE DOUBLED DOWN |
| 32 | 742–754 (13) | 30.92 | young Jensen, cyan background | FOR ALMOST A DECADE. |
| 33 | 755–780 (26) | 31.46 | **white card**: `THEN` (smears in) → `IN` → `20` → `2012` (the year types on), heavy black grotesque | — |
| 34 | 781–798 (18) | 32.54 | robot arm and scientist | A NEURAL NETWORK |
| 35 | 799–826 (28) | 33.29 | glass beads macro | CALLED ALEXNET WOKE UP |
| 36 | 827–851 (25) | 34.46 | Jensen podcast (his own sound); his words stacked small at the right edge | WE / SAW |
| 37 | 852–921 (70) | 35.50 | AlexNet network diagram on black, under his voice | — |
| 38 | 922–943 (22) | 38.42 | podcast again | BEFORE IT |
| 39 | 944–962 (19) | 39.33 | galaxy grid (Argonne National Laboratory) | IT NEEDED IMMENSE |
| 40 | 963–983 (21) | 40.12 | scientist at a grid screen | PARALLEL PROCESSING |
| 41 | 984–998 (15) | 41.00 | scientists pointing at a network on screen | TO TRAIN. |
| 42 | 999–1020 (22) | 41.62 | NVIDIA logo on light grey | — |
| 43 | 1021–1039 (19) | 42.54 | Earth | THE ONLY COMPANY |
| 44 | 1040–1059 (20) | 43.33 | black, `WITH THE`, then a **3×3 photo wall builds from the bottom-right, a tile every 3 frames, each entering on a white tile** | INFRASTRUCTURE |
| 45 | 1060–1079 (20) | 44.17 | the full wall (factories, robots, wafers) | ALREADY BUILT. |
| 46 | 1080–1091 (12) | 45.00 | Jensen, green stage | JENSEN |
| 47 | 1092–1120 (29) | 45.50 | **white card**, a framed photo of Jensen, words at its corners one by one: `PREDICTED` `THE` / `AI` `ERA.` | — |
| 48 | 1121–1153 (33) | 46.71 | Jensen on stage with partner logos | HE ATTRACTED |
| 49 | 1154–1187 (34) | 48.08 | Lisa Su (AMD) on stage — "most founders" | OPTIMIZED |
| 50 | 1188–1206 (19) | 49.50 | young Jensen smiling | THE DANGEROUS ONES |
| 51 | 1207–1223 (17) | 50.29 | chip components macro | BUILD THE |
| 52 | 1224–1235 (12) | 51.00 | GPU board macro | INFRASTRUCTURE |
| 53 | 1236–1280 (45) | 51.50 | Jensen on stage with DGX machines | FOR A FUTURE |
| 54 | 1281–1356 (76) | 53.38 | **white end card**: small black caps build word by word (`THEY` → `THEY DON'T REACT` → `…TO MARKETS`, `THEY FORCE THE MARKET`), then `TO REACT TO THEM` big condensed | — |

## 3. Why it works
1. **The hook is a three-act argument in 6 s** (myth / denial / reframe), and each act has its own *visual register*
   (real footage → red card → product flipbook → red card). The eye always knows which act it is in.
2. **Punctuation frames instead of transitions**: 1–2-frame negatives, black blinks, a blank card, a square — all on
   hits — give the "fast" feeling without making any shot shorter than the words need.
3. **Every word lands on its syllable** (±1 frame) and the picture leads the voice by a frame, so the edit feels like
   it is *speaking* the script. The pauses are held on still type, which makes the next cut hit harder.
4. **The flipbook turns a number into an image**: "10-year" = a decade of GPU generations at 12 per second, clicking.
5. **Gear change into the body**: after the irregular, word-driven hook, a metronomic one-shot-per-beat rhythm
   (17 frames) carries 50 s of story, broken only by white type cards at the turning points and by Jensen's own voice.

## 4. Recipe: this opening for our next edit

Script shape (≈6 s): `Everyone thinks [SUBJECT] is [OBVIOUS THING]. It isn't. It is [a N-year …] in [TWO-WORD
PAYOFF].` Frames at 24 fps (× 1.25 for 30 fps, × 2.5 for 60 fps):

| Beat | Length | Picture | Type | Punctuation / sound |
|---|---|---|---|---|
| A. Myth | ~15 f | live footage of the subject in the *myth's* context | caption chunk, small, centred low | 1-frame colour negatives on frames 2 and 4 of the beat · hit |
| B. Name | ~20 f | 3×3 tile flip (4 frames: B/W tiles with the name in the centre tile → tiles turn into the 2nd photo) | the name huge, centre | grid seams stay faint · hit on the first tile frame |
| C. Obvious thing | ~20 f | object photo with a square spotlight box | caption chunk | in: negative of the old shot + negative of the new with a white square (1 f each); 2 black blinks |
| D. Denial | ~17 f | negative (1 f) → cyan (2 f) → solid red card | condensed caps, word by word in final place, first word pops 1 f bigger | hit on the red · hold into the pause |
| E. Reframe list | ~37 f | flipbook of ~18 photos of the thing over time, **2 frames each**, white pages with dark runs | micro-words around the object, difference blend, word layer slowly zooming out | **a click per image** · hit on the first |
| F. Payoff | ~25 f | red card with texture | one giant condensed word per beat; a 1-frame blank before the 2nd word and one inside it | — |
| G. Story | — | first story picture + caption **10 frames before** the narrator's next line | caption chunk | then cut on every beat of the music |

### Building it in HyperFrames (pieces we already have)
- **Colour-negative frames**: prep's `neg` grade (1-frame clips) or a frame-long invert layer, as in the GTA burst.
- **Square spotlight / white square**: the square-flash system in `GTA6-v3/tools/build4.py` (`build_fx`).
- **Difference-blend words**: reference 7's "took 13 years to make." (`r7_scene`, `.r7d`).
- **Blank-frame flicker**: the "Instinct." flicker on the giant words (`giant(..., flicker=...)`).
- **Tile grids / photo walls**: the GTA VI grid and the pin board (one picture per n frames).
- **New for this**: the 3×3 B/W tile flip (9 tiles, per-tile state per frame), the 12-fps flipbook with a click SFX per
  image (the user decides on SFX), and a condensed display face for the red cards (Bebas Neue, League Gothic or
  Anton, all OFL, into `assets/fonts/`). The reel is 4:3; ours are 16:9 — keep the type sizes as fractions of the
  height given above.
