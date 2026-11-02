# Reference breakdown — "The scariest thing about Sam Altman" (Instagram reel `DeW5zohMQWC`)

Frame-by-frame study of the reference edit, written as a style bible for re-creating the look
(next target: a Robert Pattinson edit in the same style).

**Source file:** 960×720 (4:3), 23.976 fps, 2,071 frames, 86.47 s, H.264 + AAC stereo 44.1 kHz.
**Method:** every frame of 0–15 s at 15 fps, the rest at 8 fps, key transitions at the full 24 fps,
full-resolution crops for typography, per-frame difference map (held frames), scene-cut detection,
word-level transcription (whisper.cpp), and voice/music stem separation (Demucs) for the audio analysis.

---

## 0. The style in 15 lines (TL;DR recipe)

1. **Documentary-essay VO** (one narrator, ~3 words/sec) carried by **word-by-word captions** in the centre of frame.
2. **Two-font captions:** connective words in a **thin high-contrast italic serif**; the meaning-word in a **heavy, tightly-tracked grotesk**. White, with a soft white **glow**. On bright shots they flip to **black text with a white halo**.
3. Captions **hard-pop on** at each word start (no fade/slide/scale), stack up to ~3–4 words, then **hard-clear** at the phrase end. First frame of each word has a brighter glow pulse.
4. **Hook = 3 shots per second.** Average shot 0.36 s for the first 15 s; cuts land **~1 frame before the music beat** (≈100 BPM pulse).
5. **Every abstract word gets a picture:** "control" → statues, "humanity" → atom/Vitruvian Man/Moon/black hole/clock, "kill switch" → a light switch, "biggest mistake" → nuclear fire, "four days" → warp tunnel, "five people" → five faces.
6. **Metaphor montages run "on twos":** each image holds exactly **2–3 frames** (~10–12 images/sec) while the caption stays fixed.
7. **Receipts:** real TV news with chyrons, article screenshots, hearing footage — and two **news clips play with their original audio** as proof.
8. **Black "breath" cards** with a radial glow behind a single phrase ("For context,", "their lives.", "GONE." ×2, "it happened", "comes").
9. **Word slams:** the key word blown up 4–5× frame width, white, bloomed out, for **1–2 frames** as the transition ("SCARIEST", "COMPANY", "hu…", "proj…").
10. **Flash vocabulary:** 1–2-frame white flashes, a 1-frame colour-inverted frame, whip smears, grid-tile flashes, glitch smears, red duotone flashes.
11. **Lens look on every frame:** strong vignette (edges ≈ 66 % of centre brightness), rainbow chromatic fringing + blur in the corners, highlight bloom, crushed blacks.
12. **Colour logic:** mostly natural-punchy footage; **B&W** for archival/statues/power imagery; **red** as the danger accent (red tie, red duotone, logo turning red on "safe"); purple/blue/green tints for "tech" moods.
13. **Pacing arc:** fast hook → montage-heavy setup → slows to ~1.5 s shots for the news "receipts" → punctuated aftermath → B&W political escalation → thesis line → logo sting.
14. **Music:** quiet ~100 BPM tension pulse under the first half with **sub-bass booms on key words**; a steady groove (snare every 1.23 s, ≈97.6 BPM) enters at ~42 s; **no ducking**; 4 s music-only outro.
15. **End:** callback shot of the subject under the same blue light used earlier, then a **glowing logo sting animated at 12 fps** that shrinks and fades to black.

---

## 1. Transcript (corrected against the on-screen captions)

`[VO]` = narrator. `[NEWS]` = original audio from a news/stage clip.

| Time (s) | Line |
|---|---|
| 0.0–3.6 | [VO] The scariest thing about Sam Altman isn't how powerful he is. |
| 3.6–6.9 | [VO] It's what happens to anyone who tries to take his power away. |
| 6.9–13.9 | [VO] For context, Sam designed OpenAI to be the one company on Earth that no single person could ever control. |
| 13.9–17.9 | [VO] A nonprofit whose board didn't answer to money but to humanity. |
| 17.9–20.8 | [VO] A kill switch to fire even the CEO. |
| 20.8–25.4 | [VO] There was even a cap on profit, so past a point, the profit went back to the world. |
| 25.4–28.4 | [VO] It was the safest structure anyone ever built. |
| 28.4–33.0 | [VO] And then, on a Friday, four board members actually pressed the button. |
| 33.0–36.5 | [NEWS] Well, the company that gave us ChatGPT fired its CEO. |
| 36.5–39.1 | [NEWS] They just made the biggest mistake of their lives. |
| 39.1–43.2 | [VO] Within hours, 700 of his people threatened to walk out the door with him. |
| 43.2–45.2 | [VO] And within four days, he was back. |
| 45.2–51.2 | [NEWS] Sam Altman is apparently back as OpenAI CEO — this, just days after getting fired. |
| 51.2–55.2 | [VO] The two who challenged him? Gone. The humanity cap on profits? Gone. |
| 55.2–63.2 | [VO] As a result, the company worth $86B the day they fired him is now worth $852B. |
| 63.2–65.0 | [VO] And last week, it happened again. |
| 65.0–71.1 | [VO] The most powerful people in AI walked into the White House and signed a promise to keep this technology safe. |
| 71.1–72.7 | [VO] But who is watching them? |
| 72.7–75.5 | [VO] The most powerful technology in human history. |
| 75.5–78.6 | [VO] And it all comes down to the mood of about five people. |
| 78.6–82.2 | [VO] That's not a plan. That's just hoping the king stays kind. |
| 82.2–86.5 | (music only — logo sting) |

Whisper misheard "ChatGPT" as "chatG from T" and "this" as "That's"; the captions were used to correct them.
Words spoken ≈ 245 in 82 s → **~180 words per minute**.

---

## 2. Structure and pacing

Shot counts use detected cuts (scene score ≥ 0.45; flashes and 1-frame inserts count as shots).

| Act | Time | Job | Shots | Mean shot | Median shot |
|---|---|---|---|---|---|
| 1. Hook | 0.0–7.2 | Contradiction + threat ("isn't how powerful… it's what happens to anyone…") | ~22 | 0.33 s | ~0.27 s |
| 2. "For context," | 7.2–8.4 | Black breath card | 1 | 1.0 s | — |
| 3. The safe design | 8.4–28.4 | Explain the structure; 3 metaphor montages | ~58 | 0.36–0.47 s | 0.27–0.33 s |
| 4. The firing | 28.4–36.6 | "And then, on a Friday…" + first news receipt | ~14 | ~0.6 s | — |
| 5. The comeback | 36.6–51.0 | Mistake → walk-out → back in 4 days; second news receipt (5.9 s hold) | 12 | **1.51 s** | 0.79 s |
| 6. Aftermath | 51.0–63.2 | "Gone." refrain ×2, $86B → $852B | 11 | 1.10 s | 0.71 s |
| 7. Escalation + thesis | 63.2–82.2 | "It happened again" → White House → "five people" → "the king stays kind" | 22 | 0.91 s | 0.69 s |
| 8. Sting | 82.2–86.5 | Logo, music only | 1 | 4.2 s | — |

Whole video: **126 shots, mean 0.69 s, median 0.40 s; 27 shots are 3 frames or shorter.**
The rhythm deliberately **slows down when the proof arrives** (news clips) and **speeds up for metaphor**.

---

## 3. Shot-by-shot breakdown

Times are seconds. **Bold** caption words = heavy grotesk; *italic* = serif italic. "f" = frames at 23.976 fps (1 f = 41.7 ms).

### Act 1 — Hook (0.00–7.22)

| Time | Picture | Caption on screen | Transition / effect | Sound |
|---|---|---|---|---|
| 0.00–0.54 | Flash-lit photo of Sam with another man at an event | *the* → **SCARIEST** (small, centre) | **Pixel-mosaic reveal**: faces start as big pixel blocks; tiles un-pixelate one by one (some tiles flash white) over ~13 f; slow push-in | VO starts at 0.01 |
| 0.54–0.62 | — | **Word slam**: "SCARIEST" at ~4–5× frame width, heavy serif, blown-out white bloom | 2 f; the slam carries across the cut into the next shot | high-band hit 0.67 |
| 0.63–1.21 | Same photo as a **Polaroid print** (white border, ~35 % frame width, slight tilt) on black with a soft radial glow; slow push-in | *thing* (left of the print) … *about* (right) | Caption **breaks out of centre** so it doesn't cover the photo | |
| 1.21–1.50 | Sam on a TV-interview set | *Sam* | hard cut, ~1 f before the beat | pulse ≈ every 0.30 s |
| 1.50–1.84 | Sam in a dark suit on a panel | *Sam* **Altman** | hard cut | whoosh/tick 1.58 |
| 1.84–2.38 | Sam in a navy puffer vest, pink-cream backdrop | *Sam* **Altman** *isn't* | hard cut | |
| 2.38–2.67 | Sam lit blue on stage | *how* → *how* **powerful** | hard cut | |
| 2.67–3.00 | Sam in a red armchair, dark purple stage | *how* **powerful** | hard cut | |
| 3.00–3.30 | Sam in a white armchair, US flags (wide) | *how* **powerful** | hard cut | |
| 3.30–3.59 | Same scene **punched in** ~2× | *he* → *he is.* | punch-in cut | |
| 3.59–4.25 | A TV screen filmed at an angle: news graphic **"'BAD THINGS'?"** with a B&W tuxedo photo of Sam | *what* | hard cut | |
| 4.25–4.59 | Sam on webcam, news chyron "NEW: OPENAI CEO SAM ALTMAN SAYS PEOPLE NEED TO ACCEPT SOME 'BAD THINGS' FOR THE BENEFITS…" | *what* **happens** | hard cut | |
| 4.59–4.80 | Purple bokeh field of blurred faces | *to* | hard cut | |
| 4.80–4.96 | **White grid panels** flash on one by one → full white-out with Sam's silhouette | *to* **anyone** | grid-flash build, 4 f | |
| 4.97 | Colour-**inverted** (negative) frame | — | 1 f flash | |
| 5.01–5.30 | **B&W high-contrast cutout of Sam** gesturing, over the purple bokeh; the white panels turn into **floating UI cards** (article/tweet screenshots) that pop in around him | *who* → *who* **tries** | cards pop in one per 1–2 f | |
| 5.30–5.38 | Blown-out white flash with motion smear | *…tries* | 2 f white flash | |
| 5.38–6.00 | Collage continues; another white flash on "take" | *to* → *to* **take** | 1–2 f flash | **sub-bass impact 5.79** |
| 6.00–6.50 | The grid behind Sam now holds **photos of two women** (one with a "HELEN TONER" lower third) | *to take his* → *power* | grid tiles swap images | |
| 6.50–6.59 | White motion-smear flash | — | 2 f | high hit 6.06 |
| 6.59–7.17 | Sam at a Senate hearing (nameplate "Mr. Samuel Altman") | *power* **away.** | hard cut | |
| 7.17–7.22 | Whip smear + **1-frame white flash** into black | *For* | whip, 2 f | |

### Act 2 — Breath card (7.23–8.39)

| Time | Picture | Caption | Effect | Sound |
|---|---|---|---|---|
| 7.23–8.18 | Pure black with a **radial glow** behind the text | *For* → *For* **context,** | Words pop on; the first frame of "For" has a brighter glow (bloom pulse) | VO only |
| 8.23–8.35 | Pure black | — | **4 frames of nothing** (the breath) | |

### Act 3 — The safe design (8.39–28.4)

| Time | Picture | Caption | Effect | Sound |
|---|---|---|---|---|
| 8.39 | A small colour-inverted square over Sam's face | *Sam* | 1-f glitch | high hit 8.44 |
| 8.43–8.93 | Desaturated photo of young Sam smiling among people, heavy vignette | *Sam* (left) … **designed** (right) | words flank the face | |
| 8.93–9.67 | **OpenAI logo** on a browser screen (macro, angled, cool B&W-ish) | *to* | slow push | |
| 9.67–10.33 | Senate-hearing Sam again | *to be the one* (all italic, word by word) | | |
| 10.33–10.47 | Whip + **word slam "COMPANY"** (blurred giant letters) + light flare | **company** | 3 f | whoosh 10.39 |
| 10.47–12.00 | **Earth at night from orbit**, sunrise flare on the horizon | **company** *on earth* → *that* → *that no* | slow drift | |
| 12.00–13.27 | Crossfade into a **pixel-mosaic B&W group photo** with selective red kept (a red top/tie) | *single* **person** → *could* → *could ever* | crossfade (rare), mosaic | |
| 13.27–13.40 | White ghost smear | *could ever* | 3 f | |
| 13.40–14.40 | **STATUE MONTAGE**, B&W, crushed blacks, 2 f per image: helmeted warrior with a glowing ring, angel, warrior bust, warrior with shield (high-key), winged figure, robed poet statue with a moon, lovers sculpture, hands, ornate sword, figure in a garden | *could ever* → **control.** | images "on twos" (~12/sec); then **"control." alone on black for 1 f** | |
| 14.40–14.60 | OpenAI stage ("Sam Altman, Chief Executive Officer" on screen) 2 f → SoftBank stage, a man bowing 2 f → a woman in black at an interview 2 f | **control.** → *A* | 2-f cuts | |
| 14.60–15.00 | Sam in a green sweater (two angles: warm, then blue backdrop) | *A* **nonprofit** | | |
| 15.00–15.13 | Sam on a panel stage with another man, plants in the foreground | *A* **nonprofit** → *whose* | | |
| 15.13–15.75 | Sam on stage with another tech figure at a Vanity Fair event (giant "VANITY" letters) | *whose board* → *didn't answer* | | |
| 15.75–16.75 | Early group photo of Sam with three colleagues | *didn't answer* → *to money.* → *but* | | |
| 16.75–16.85 | Whip smear → white rectangle flash | — | 2 f | **music swells +9 dB from 16.5 s** |
| 16.85–17.05 | Vertical light beam; **word slam "hu…"** (giant italic serif) for 1 f | *but to* | | sub-bass boom 16.92 |
| 17.05–17.25 | Light beam with **HUD constellation lines and bounding boxes** | *but to* **humanity.** | | boom 17.25 |
| 17.25–18.00 | **HUMANITY MONTAGE**, 2–3 f each: glowing head silhouette outline → atom → Vitruvian Man (parchment with scanlines) → the Moon → Fibonacci circles → radial dot pattern → black hole (red-orange disk) → clock face → red glow blob | *but to* **humanity.** (held, centred) | images on twos/threes | booms 17.64, 18.07 |
| 18.00–19.05 | **A wall light switch** (black plate) on a light-grey radial gradient; **huge grey italic serif "Switch"** behind it, its last letters **dissolving into smoke particles**; the switch rotates/flips in 3D; light rays | *a* (left) … *kill* (right) → giant *Switch* | particle dissolve | booms 18.55, 18.92; click-like hit 17.97 |
| 19.05–19.90 | Black | *fire* *even* *the* in an **upright serif**, **each word bigger than the last**, each blurring in | blur-in + growing scale | boom 19.24; hit 19.05 |
| 19.90–20.00 | Black | — | 2-3 f breath | |
| 20.00–21.20 | **B&W halftone portrait of Sam** in front of a giant stylised "$" emblem; slow push-in | *the* **CEO.** → *There* → *There was* | Ken Burns push | hit 20.39 |
| 21.25 | White ink/smoke wipe | *There was even* | wipe | |
| 21.40–21.60 | News: Sam walking in a crowd; chyron "OPENAI CEO ALTMAN: EXPECT TO END THIS YEAR … BILLION IN ANNUALIZED REVENUE RUN RATE" | *There was even* → *a* | | |
| 21.60–22.00 | News: man in a suit with a skyline; chyron "…EXPECTS $70 BILLION IN REV. THIS YEAR" | *a cap on* → *a cap on* **profit.** | | |
| 22.00–22.10 | Stock-quote board with an anchor | *a cap on* **profit.** | | |
| 22.10–22.25 | White whip smear | — | | |
| 22.25–22.90 | CNN two-shot "WHEN WILL OPENAI TURN A PROFIT?" | **profit.** → *So* → *So past* | | |
| 22.90–23.40 | Whip → angled green/red **candlestick chart** on dark | *So past a point,* | whip | whoosh 22.73 / 23.05 |
| 23.40–23.60 | A TV in a room showing a war news broadcast | *So past a point,* | | |
| 23.60–23.90 | Stock-exchange floor traders | *So past a point,* | | |
| 23.90–24.10 | Sam presenting on black with terminal text ("what about the radio?", "radio_on") | *the* | | |
| 24.10–24.40 | Meta-branded news set, two people standing | *the* **profit** | | |
| 24.40–24.75 | Anchor; chyron "HOW A.I. DATA CENTERS ARE DRIVING UP ENERGY BILLS" | *the* **profit** *went* | | |
| 24.75–25.10 | Live financial-TV guest | **back** → *to* | | |
| 25.10–25.40 | Anchor with "Q2 NET INCOME YEAR-OVER-YEAR GROWTH" graphic | *to the* | | |
| 25.40–25.60 | Blue-vs-orange **bar chart** ("…went up nearly eightfold") | *to the* **world.** | | |
| 25.60–26.00 | Sam on a keynote stage with a big serif "06" / "Higher rate limits" slide | *It* → *It was* → *It was the* | | |
| 26.00–26.75 | Sam isolated on a black stage | *safest* → *safest* **structure** | | |
| 26.75–28.10 | **CNBC article screenshot** "OpenAI wraps $7 billion share sale ahead of potential IPO" with Sam's photo; slow push | **anyone** → *ever* → *ever* **built.** in **BLACK** (bright page) | colour flip to black captions | |
| 28.10–29.00 | Sam in an interview at home (dark jacket, bookshelf) | *ever* **built.** (white again) → *And* → *And* **then** | ends in a **horizontal slice smear** (28.9–29.0) | |

### Act 4 — The firing (29.0–36.6)

| Time | Picture | Caption | Effect | Sound |
|---|---|---|---|---|
| 29.02 | **Word slam** "proj…" (giant italic serif) | — | 1 f | |
| 29.06–29.15 | Black; a small glowing hexagon (logo glint) shrinking away | — | | |
| 29.20 | Full white | — | **1-f white flash** | |
| 29.25–29.35 | Horizontal **anamorphic light streak**, then three glints | *on* | | |
| 29.35–29.75 | **"ON A FRIDAY" MONTAGE**, 2 f each: spine X-ray (inverted) → skull X-ray → red liquid overlay → aerial fisheye of a stadium/city → radio tuner dial → Creation-of-Adam hands (B&W fresco) | *on a* → *on a* **Friday,** | on twos | |
| 29.80–30.40 | Dark UI screens with code and product copy ("Same model. 3X faster. 3X cheaper.") | *on a* **Friday,** | | |
| 30.40–31.60 | **B&W cutout collage of four portraits** (the board members), high-contrast halftone, red shapes behind; they slide in one by one | *four* → *four* **board** → **members** | staggered slide-ins | |
| 31.60–31.90 | Business reporter in front of stock-exchange screens | **members** *actually* | | |
| 31.90–33.00 | News: "EX-OPENAI BOARD MEMBER SPEAKS", lower third "HELEN TONER — OpenAI Former Board Member" | *pressed* → *the* → *the button.* | | |
| 33.00–34.60 | **NEWS CLIP with its own audio**: anchor; "TECH WATCH — ARTIFICIAL INTELLIGENCE SHAKE-UP: OPENAI FIRES CO-FOUNDER & CEO SAM ALTMAN IN SURPRISE DECISION" | **BLACK** captions: *Well* → *the company* → *that gave us* → **ChatGPT** | | news audio |
| 34.60–36.20 | Same anchor **punched in** (chyron cropped out) | *fired* → *its* | punch-in | music bump 35–37 s |
| 36.20–36.40 | Sam at the hearing (warm) | *its* **CEO.** (black) | | |
| 36.40–36.60 | Sam in an interview, red backdrop | *its* **CEO.** | | |
| 36.60–36.75 | Whip smear | — | | |

### Act 5 — The comeback (36.75–51.0)

| Time | Picture | Caption | Effect | Sound |
|---|---|---|---|---|
| 36.75–37.20 | A speaker on stage (patterned T-shirt, gold hexagon wall) | **They** *just made* | | news audio |
| 37.20–37.60 | A woman speaking on a dark stage | *the* → *the* **biggest** | | |
| 37.60–37.75 | Whip | — | | |
| 37.75–38.40 | **Firestorm / nuclear blast** rolling over a city | **mistake** *of* | | |
| 38.40–38.90 | Black card | *their* → *their* **lives.** | held frames (static) | |
| 38.90–39.40 | Desaturated fire field | *their* **lives.** → *Within* | | |
| 39.40–39.60 | Black space with a bright star flare | *Within* | | |
| 39.60–39.75 | Nebula | *Within* **hours,** | | **impact 39.76** |
| 39.75–40.25 | **Burning ring of embers** around a white light | *Within* **hours,** | | |
| 40.25–40.70 | **3×3 grid transition**: thin grid lines split the frame; tiles flip one at a time (white flash per tile) into news clips | *(no caption — "700 of his people" is spoken uncaptioned)* | tile-by-tile build, ~0.8 s | |
| 40.70–42.40 | **News video wall**, 9 tiles of coverage (chyrons: "OPENAI EMPLOYEES THREATEN TO QUIT, DEMAND BOARD RESIGN", "MICROSOFT HIRES SAM ALTMAN…", "SAM ALTMAN RETURNS AS OPENAI CEO…") | **threatened** *to* → **walk** *out* | | **music groove starts ~42 s** |
| 42.40–42.75 | Young Sam in a company T-shirt, candid camcorder interview, as an **inset over the blurred wall** | *(uncaptioned: "the door with him")* | nested picture-in-picture | |
| 42.75–43.60 | Sam in the puffer vest **pops in as a smaller inset** on top; then swaps to Sam in a suit on a talk-show chair | *and* → *and within* | 3-level frame-in-frame stack | |
| 43.75–44.60 | **Hyperspace warp tunnel** → green/teal nebula vortex | *four* **days,** → *he* | | |
| 44.60–44.75 | Teal flash | *he* | | |
| 44.75–45.10 | Candid: Sam walking down a cobblestone street | *he was* **back.** | | |
| 45.10–51.00 | **NEWS CLIP with its own audio**: anchor in a red turtleneck, dark studio; **punch-in at ~46.4** | *Sam Altman is apparently back as* **OpenAI CEO** → *this just days after getting fired.* | the longest shot (5.9 s) | news audio |
| 51.00–51.10 | Whip/blur | — | | |

### Act 6 — Aftermath (51.1–63.2)

| Time | Picture | Caption | Effect | Sound |
|---|---|---|---|---|
| 51.10–51.60 | **Split screen**: woman on a news set (left) + woman in a black dress on a green set (right) | *The two* → *who* | | |
| 51.60–52.25 | Sam seated in a dark studio, blue light streaks | *who challenged* → *him?* | | |
| 52.25–52.75 | Black | **GONE.** (all caps, glow) | held | sub-bass impact 52.99 |
| 52.75–52.90 | Dim warm light flicker | *The* | | |
| 52.90–53.50 | **Silhouette of a man falling backward** against blinding white light | *The* **humanity** → *cap* | | impact 53.78 |
| 53.50–54.40 | Bokeh → blurred stock chart → candlesticks "230.00" → stack of $100 bills → red line chart on black | *cap on profits* | 2–4 f each | impacts 54.13, 54.43 |
| 54.40–55.10 | Black | **GONE.** (the same card again — a refrain) | held | |
| 55.10–55.60 | Sam under blue stage light (**this shot returns at the end**) | *As a* **result,** | | |
| 55.60–55.75 | Young Sam, teal T-shirt, red acoustic-foam wall | *As a* **result,** | | |
| 55.75–56.40 | Young Sam with a mic at a startup event (plants, crowd foreground) | *the company* → *worth* | | |
| 56.40–59.90 | NBC-style anchor; over-the-shoulder graphic "A.I. REVOLUTION > OUSTED CEO'S SURPRISE MOVE" with Sam | *worth* **$86B** (bigger) → *the day* → *they fired* → *him.* | | snare grid every 1.23 s |
| 59.90–63.20 | Bloomberg anchor ("TIM STENOVEC, Bloomberg News"); chyron "OPENAI VALUED AT $852B IN LATEST FUNDING"; lower third animates in | *him is now* → *worth* ***$852B*** (huge italic serif, ~70 % opacity) | | |
| 63.20 | Background drops to **black** while "worth $852B" stays | | caption persists over black | |
| 63.25 | **B&W glitch / datamosh smear** | — | 1 f | |

### Act 7 — Escalation and thesis (63.3–82.2)

| Time | Picture | Caption | Effect | Sound |
|---|---|---|---|---|
| 63.30–63.45 | Black, with a **1-frame dark flash** of an Oval Office address | *And* | | |
| 63.45–63.90 | **B&W Oval Office address** (a man at the Resolute-style desk) | *And last* → *And last week,* | | |
| 63.90–64.05 | Same shot in a **red duotone** | *And last week,* | 4 f red flash | |
| 64.05–64.40 | B&W Oval Office address by a different man | *it* → *it happened* | edge scanline glitch | |
| 64.40–64.75 | Black | *it happened* | | |
| 64.75–65.10 | B&W **venetian-blind / bar shadows** with birds | **again.** | | |
| 65.10–65.50 | B&W archival of a man in a classroom with a chalkboard | **again.** → *The most* | | |
| 65.50–65.90 | B&W high-contrast still of a figure | *powerful* | | |
| 65.90–66.25 | Man on a dark background | *powerful* → *people in* | | |
| 66.25–66.50 | Man in glasses in a decorated room | *people in* | | |
| 66.50–66.90 | Man in a blue sweater | *AI* **walked** | | impact 66.87 |
| 66.90–67.40 | News: executives walking outside the Capitol; chyron "…TAKES CENTER STAGE IN WASHINGTON" | *into* | | |
| 67.40–68.10 | Executives and officials walking; chyron "SENATE OVERSIGHT HEARING…" | *into the* **White House** → *and* | | |
| 68.10–69.90 | State dining room full of tech leaders; chyron "PRESIDENT TRUMP MEETS WITH TECH LEADERS" | *and signed* → *a promise* → *to keep this* | | |
| 69.90–71.25 | Black with faint code; a **3D extruded OpenAI logo** (white, glowing) swings in and rotates; it **turns red on "safe."** | *technology* → *technology* **safe.** | 3D logo, colour switch | |
| 71.25–71.40 | Red logo blur | | | |
| 71.40–71.90 | Overhead **silhouettes of a crowd**, blue high-key | **But** *who is* (**black** text) | | |
| 71.90–72.10 | Red-tinted silhouettes | **watching** | red duotone | |
| 72.10–72.25 | Crowd again | **watch…** | | |
| 72.25–72.75 | B&W archival film of a man reaching up / shielding himself | **watching** *them?* | | |
| 72.75–73.10 | Dark red blur | *The* → *The most* | | |
| 73.10–73.40 | Code/manifest text ("base=ELEMENT", "Saturn_Ring", "collective_unconscious", "chronos") over a particle network | **POWERFUL** (all caps) | | |
| 73.40–74.10 | **Periodic-table card "C — carbon — 6 — 12.011"** with a graphene hexagon lattice; then a red version | *technology* → *technology in* | | |
| 74.10–74.60 | Code overlay on dark red | **human** → **human** *history.* | | |
| 74.60–75.60 | **Glowing white line-art of a robed figure with arms outstretched** (a painting rendered as light), red then dark | **human** *history.* → *And it all* | | |
| 75.60–75.90 | Black | *comes* | breath | |
| 75.90–76.90 | **Green night-vision surveillance footage** with tracking boxes (a hand, then a station crowd) | *down to the mood of* | HUD boxes | |
| 76.90–77.40 | Crowd continues | *about* | | |
| 77.40–77.75 | **Five vertical portrait strips slide in from the right**, one every 1–3 frames, until five faces fill the frame | *about* → **five** | staggered strip slide-in | |
| 77.75–78.75 | Strips hold | **five** *people.* | | |
| 78.75–79.50 | Scientist in a dark blue lab | *That's not* → *a plan.* | | |
| 79.50–81.00 | Dark room, warm desk lamp, someone writing | *That's just* → *hoping* → *hoping the* **king** | | |
| 81.00–81.90 | **Callback:** Sam under the same blue stage light as 55.1 s | *stays* → *stays* **kind.** | | VO ends 82.24 |

### Act 8 — Sting (81.9–86.5)

| Time | Picture | Effect | Sound |
|---|---|---|---|
| 81.90–83.00 | Glowing white **diamond + play-triangle logo**, starts huge and over-exposed | scales down to centre | music only |
| 83.00–85.30 | Logo held small, centre, soft glow on near-black | **animated on twos (12 fps)** — the only deliberately low-frame-rate motion in the film | |
| 85.30–86.30 | Logo fades to black | 1 s fade | music fades out |

---

## 4. Typography system

### Fonts (closest matches — estimates from 960×720 frames)

| Role | What it looks like | Closest free match | Paid alternatives |
|---|---|---|---|
| Connective words | Thin, high-contrast editorial **serif italic**, single-storey italic "a", ball/teardrop terminals | **Instrument Serif Italic** | PP Editorial New Italic, Canela Light Italic |
| Meaning-word | **Heavy neo-grotesk**, round "o"/"e", very **tight tracking** (letters nearly touching) | **Inter Display Bold/ExtraBold** at −5 % tracking | Helvetica Now Display Bold, Neue Haas Grotesk Display Bold, SF Pro Display Bold |
| "fire even the" card | Upright, slightly condensed text serif | **Instrument Serif Regular** | Times New Roman |
| Word slams | Heavy serif / italic serif, blown out | Instrument Serif (Italic) at 400–600 % | Editorial New Ultrabold |
| "Switch" | Large **grey bold italic serif**, ~50 % opacity, behind the object | Instrument Serif Italic + faux-bold | — |

### Size and position

- Centred horizontally. Vertical centre at **~47 % of frame height** (just above the middle).
- "For context," measured: text block **284 px wide × 51 px tall on a 960×720 frame** → font size ≈ **50 px at 720p** ≈ **7 % of frame height** ≈ **5.2 % of frame width**.
  - 1440×1080 (4:3 HD): ~75 px. 1080×1920 (9:16) at the same width ratio: ~56 px (go 64–72 px for phone readability).
- Italic and bold words share one baseline; the bold word reads slightly larger because of its weight.
- **Breaks out of centre** when the middle is occupied: "thing … about" flanking the Polaroid, "Sam … designed" flanking a face, "a … kill" flanking the switch.
- Numbers get **size**, not weight: "$86B" bold and ~1.3× larger; "$852B" italic serif at ~1.6× and ~70 % opacity.

### Colour and glow (measured on the black card at 7.6 s)

- Fill **pure white #FFFFFF**. Profile outward from the glyph edge: 255 → **101 at +4 px** (tight glow ~40 %) → **58 at +8 px** → slow decay **55 → 29 over the next ~70 px** (wide halo ~20 % → 11 %).
- That is two layers: a tight glow (blur ~3 px, ~45 %) + a wide soft halo (blur ~30–40 px at 720p, ~18 %).
- On black cards a **radial spotlight** sits behind the phrase (~40–55/255 near the text, 0 at the corners).
- **Bloom pulse:** the first frame a word appears its halo is ~2–3× brighter (84 vs ~30), then settles.
- **Bright shots** (white article page, light news sets, high-key crowd): text switches to **black #000 with a white halo**. It is per-shot, not a blend mode.
- Close up, the heavy words carry a **faint speckle texture** (tiny dark dots inside the strokes), like a printed/grain texture on the text layer.

### Which words go bold (the rule)

The bold grotesk takes the **semantic payload**: names, the noun or verb that carries the sentence, numbers and verdicts.
Examples: **Altman, powerful, happens, anyone, away, context, designed, company, person, control, nonprofit, humanity, profit, world, structure, built, then, Friday, board, members, ChatGPT, CEO, biggest, mistake, lives, hours, days, back, OpenAI CEO, result, $86B, GONE., again., walked, White House, safe., But, watching, POWERFUL, human, five, king, kind.**
Everything else (articles, pronouns, prepositions, auxiliaries, connective verbs) is serif italic: *the, about, how, he is, what, to, who, to take his, For, to be the one, on earth, that no, could ever, A, whose, didn't answer, but to, There was even, a cap on, So past a point, It was the, ever, And, on a, pressed the, They just made the, of their, Within, four, he was, The two who challenged him?, cap on profits, As a, the day they fired him, is now worth, And last week, it happened, The most, people in, into, and signed a promise to keep this, is, them?, technology in, history., And it all comes down to the mood of about, people., That's not a plan., That's just hoping the, stays.*
**All caps** is rare and reserved for the hook ("SCARIEST") and the verdicts ("GONE." ×2, "POWERFUL").

---

## 5. Caption timing mechanics

- One caption **group per phrase** (2–5 words). Words are **added one at a time on the spoken word start (±1 frame)**; the group **clears instantly at the end of the last word**, often followed by a few frames of an empty or black frame.
- **No entrance animation** on standard captions: no fade, slide or scale; the bounding box is pixel-identical from frame to frame (measured 7.31–8.18 s). The only "animation" is the 1-frame glow pulse.
- A caption **can persist across cuts** within a phrase (most phrases span 2–6 shots), and **can persist while the picture drops to black** (63.2 s "worth $852B").
- **Deliberately uncaptioned moments:** while the 3×3 video wall builds ("700 of his people", 39.9–41.1 s) and during the nested picture-in-picture ("the door with him", 42.4–43.2 s). The picture carries the line there.
- News clips with original audio are captioned in the same system (black-on-bright when the set is light).

---

## 6. Motion graphics and effects inventory

| Effect | Where | Exact behaviour |
|---|---|---|
| Pixel-mosaic reveal | 0.0–0.54; 12.0–13.3 | Large-block pixelation; tiles resolve individually in a random order over ~13 f; some tiles flash white as they resolve |
| Word slam | 0.54 ("SCARIEST"), 10.33 ("COMPANY"), 16.9 ("hu…"), 29.02 ("proj…") | Keyword at 400–500 % width, heavy bloom; 1–2 f; bridges the cut |
| Polaroid print | 0.63–1.21 | Photo inside a white border (wider at the bottom), ~3° tilt, on black with a radial glow, slow push-in; caption flanks it |
| White flash frame | 4.80, 5.30, 5.93, 6.50, 7.18, 16.8, 21.25, 22.1, 29.2 … | 1–2 f full-frame white with bloom/smear; on emphasis words and section turns |
| Inverted (negative) frame | 4.97; 8.39 (a square region) | 1 f colour inversion |
| Grid flash build | 4.80–4.96 | White rectangles in a 3×3 grid pop on one by one → white-out |
| B&W subject cutout + floating cards | 5.0–6.6 | Background-removed subject, high-contrast B&W, over a coloured bokeh plate; screenshot cards pop in around him one per 1–2 f; grid tiles swap to the antagonists' photos |
| Whip / motion-smear | 7.17, 10.33, 16.75, 22.1, 22.9, 36.6, 37.6, 51.0 | 2–4 f directional blur between shots |
| Metaphor montage on twos | 13.4–14.4, 17.25–18.0, 29.35–29.75, 53.5–54.4 | 2–3 f per image, caption held centre, B&W or mono-tint |
| Particle / smoke dissolve | 18.3–19.0 ("Switch") | Big serif word dissolves into smoke from its right edge |
| Growing-word card | 19.05–19.9 ("fire even the") | Each word blurs in larger than the previous (roughly 1.0× → 1.3× → 1.7×) |
| Halftone B&W portrait | 20.0–21.2; 30.4–31.6 | Newsprint dot texture, crushed blacks, big emblem or red shapes behind |
| Ink / smoke wipe | 21.25 | White organic wipe |
| Horizontal slice smear | 28.9–29.0 | Bands of the frame displace sideways |
| Anamorphic streak / flares | 29.25–29.35; 39.4; 10.4 | Horizontal light streak, glints, star flare |
| Board-member collage | 30.4–31.6 | Four B&W cutout portraits slide in one by one, red graphic shapes behind |
| Punch-in zoom | 3.30, 34.6, 46.4 | Hard cut to a ~1.5–2× crop of the same clip |
| 3×3 video-wall build | 40.25–40.7 | Grid lines, then each tile flips to a news clip with its own small white flash, random order |
| Nested picture-in-picture | 42.4–43.6 | Each new clip pops in as a smaller framed inset on top of the last (3 levels) |
| Split screen | 51.1–51.6 | Two clips side by side with a hard vertical seam |
| Background drop to black | 7.2, 63.2 | Picture cuts to black, caption stays |
| Glitch / datamosh smear | 63.25; 64.4 edge scanlines | 1 f B&W pixel smear; horizontal scanline tear at the frame edge |
| Red duotone flash | 63.9–64.05; 71.9 | 4 f of the shot mapped to red/black |
| 3D logo | 69.9–71.25 | Extruded white logo swings in, rotates, turns red on "safe." |
| HUD / tracking boxes | 17.05; 75.9–77.4 | Thin rectangles and constellation lines; green night-vision with tracking boxes |
| Vertical strip slide-in | 77.4–77.75 | Five portrait strips enter from the right, each 1–3 f after the last |
| Logo sting at 12 fps | 81.9–86.3 | Scale-down from huge, hold, 1 s fade; motion on twos |

**Low frame rate — exactly where.** The footage itself plays at the full 23.976 fps. The "choppy" feel comes from three places only:
(1) the montages that hold each image for 2–3 frames, (2) the end-logo animation stepping on twos (12 fps, 82–86 s), and
(3) static black cards and stills that hold (7.2–8.4, 38.4–38.9, 52.2–52.8, 54.4–55.1).
No speed ramps or frame-blending were found.

---

## 7. Global look and grade

- **Vignette:** strong; edge brightness ≈ **0.66×** the centre.
- **Lens edges:** rainbow **chromatic fringing and blur in the corners only** (prism-like), clean centre. The outer border carries a faint **magenta** tint (mean RGB ≈ 61/46/58).
- **Contrast:** blacks crushed (5th-percentile luma ≈ **5/255**), whites near clip (99.5th percentile ≈ **253**). Highlights **bloom** (white shirts and lamps glow).
- **Saturation:** slightly under normal TV levels (median 0.31); **~9 % of frames are B&W**.
- **Colour logic:** natural-punchy for interviews and news; **B&W** for statues, archival, power and political imagery; **red** as the warning accent; **purple/blue** for "tech/collage" plates; **green night-vision** for surveillance; warm amber for fire and lamps.
- **No added film grain:** black cards are clean (noise σ ≈ 0.1); texture only comes from the source images (halftone, scanlines on the Vitruvian Man).
- **Aspect ratio:** 4:3 at 960×720. Cards and graphics are built for 4:3, not 9:16.

---

## 8. Asset inventory

1. **Subject photos:** event photo with another man (hook, also as the Polaroid); young Sam smiling among people; early group photo with three colleagues; a B&W halftone portrait in front of a "$" emblem; a candid photo walking on a cobblestone street.
2. **Subject video:** TV interviews (Bloomberg set, green sweater, home interview, red backdrop, webcam), keynote stages (blue light, red armchair, white armchair with flags, "06" slide, black stage), Senate hearing (nameplate), panels (Vanity Fair, plants), young-founder footage (camcorder interview, red foam wall, startup mic).
3. **TV news as receipts (chyrons kept):** "'BAD THINGS'?", "PEOPLE NEED TO ACCEPT SOME 'BAD THINGS'", "WHEN WILL OPENAI TURN A PROFIT?", "AI DATA CENTERS… ENERGY BILLS", "Q2 NET INCOME", "EX-OPENAI BOARD MEMBER SPEAKS / HELEN TONER", "ARTIFICIAL INTELLIGENCE SHAKE-UP", "OPENAI EMPLOYEES THREATEN TO QUIT", "SAM ALTMAN RETURNS AS OPENAI CEO", "OUSTED CEO'S SURPRISE MOVE", "OPENAI VALUED AT $852B", "…TAKES CENTER STAGE IN WASHINGTON", "PRESIDENT TRUMP MEETS WITH TECH LEADERS".
4. **Screenshots:** CNBC article page; browser with the OpenAI logo; tweet/article cards; bar chart; product UI copy.
5. **Stock footage:** Earth at night from orbit, nebulae/star flares, hyperspace warp, burning ember ring, firestorm/nuclear blast, stock tickers/candlesticks/traders, $100 bills, crowd silhouettes, night-vision surveillance crowds, scientist in a lab, desk lamp scene.
6. **Symbol / metaphor stills:** classical statues (warriors, angels, poet, lovers), ornate sword, atom, Vitruvian Man, the Moon, Fibonacci circles, black hole, clock, light switch, spine and skull X-rays, radio dial, Creation-of-Adam hands, periodic-table carbon card, code/manifest text, a robed figure as glowing line-art, venetian-blind shadows.
7. **Archival:** B&W Oval Office addresses, a classroom with a chalkboard, an old film clip of a man shielding himself.
8. **Made graphics:** Polaroid frame, word slams, black glow cards, grid/tile panels, floating cards, HUD lines/boxes, 3D extruded logo, five-strip face layout, the creator's diamond-and-triangle logo.

---

## 9. Sound design and music (from separated stems)

- **Voice:** one narrator, ~180 wpm, sitting ~2–4 dB above the music in the second half and ~8–10 dB above it in the first.
- **Music, part A (0–42 s):** sparse tension bed (−27 to −31 dBFS) with a **~100 BPM pulse (hits every ~0.30 s)**. It swells **+9 dB at 16.5 s** for the "humanity / kill switch / fire even the CEO" run, with **sub-bass booms every ~0.35–0.4 s** (16.92, 17.25, 17.64, 18.07, 18.55, 18.92, 19.24), then drops back. A bump at 35–37 s sits under "fired its CEO / biggest mistake".
- **Music, part B (≈42–82 s):** a steady groove at a **constant −21 dBFS**, with a **snare/clap every 1.23 s (≈97.6 BPM backbeat)**: 42.8, 44.1, …, 51.5, 52.7, 53.9, 55.2, 57.6, 58.8, 60.1, 62.5, 63.8, 65.0, 66.2, 67.5, …, 79.8.
- **No ducking:** the music level is the same whether the voice is speaking or not (−20.5 vs −20.6 dB).
- **Key:** roughly G/G♯ major (low confidence).
- **Sound-effect hits:** sub-bass impacts at 5.79 ("take"), 39.76 ("hours"), 52.99 / 53.78 / 54.13 / 54.43 ("Gone." run), 66.87 ("walked"); high whoosh/click hits at 0.67, 1.58, 3.92, 8.44 (into "Sam designed"), 10.39 (into Earth), 17.97 (switch), 19.05 ("fire"), 22.73 / 23.05 (whip into the chart).
- **Outro:** about 4 s of music only after the last word (82.2 → 86.3), fading with the logo.

**How the cuts sit on the sound:**
- **Hook (0–15 s): cut on the beat, one frame early.** 41–42 % of cuts land within ±1 frame of a beat (random would be 26–28 %), and **68–73 % of cuts come before the beat** (median −37 ms ≈ 1 frame). The new image is already up when the hit lands.
- **After 15 s the edit stops following the music** (alignment drops to chance) and **follows the words**: shots change on the meaning-words of the narration, and the sound-effect hits are placed on the visual events (flashes, slams, switch, impacts), not the other way round.

---

## 10. Why it works

1. **A contradiction hook in 3.6 s.** "The scariest thing isn't how powerful he is" opens a curiosity gap. It is delivered over 10 shots, a pixel reveal and a word slam, so the eye never settles.
2. **Literal visual rhyme.** Every abstract word gets a concrete picture ("control" → statues, "kill switch" → a switch, "biggest mistake" → nuclear fire, "five people" → five faces). The viewer *sees* the argument, and the 2-frame montages feel like a thought racing.
3. **Proof as pacing.** The edit slows to 1.5 s shots for real news audio and chyrons. Credibility comes from the receipts, and the slower section lets the viewer breathe before the next acceleration.
4. **Refrains and callbacks.** "GONE." twice on identical black cards; the blue-light Sam shot used at "As a result" returns for the final "stays kind"; black breath cards bracket each act.
5. **Typography as the narrator's voice.** Reading word by word at speech speed, with the meaning-word in heavy type, makes the captions a second audio track. The serif/sans pairing reads as premium editorial journalism.

---

## 11. Steal the structure → Robert Pattinson

Keep the skeleton, swap the content.

| Act | Reference beat | Pattinson version (example) | Technique to reuse |
|---|---|---|---|
| Hook 0–7 s | "The scariest thing about X isn't Y. It's Z." | "The strangest thing about Robert Pattinson isn't that he escaped *Twilight*. It's how he did it." | Pixel reveal on an early photo → word slam on the key word → Polaroid with flanking words → ~10 shots cut 1 frame before the beat |
| Breath | "For context," on black | "For context," | Black glow card, 4 empty frames after |
| Setup 8–28 s | How the system was built | The machine that made him: the *Twilight* fan frenzy, paparazzi, magazine covers | Metaphor montages on twos for abstract words (fame, cage, hunger…), article screenshots in black captions |
| Turn 28–37 s | "And then, on a Friday…" + news clip | "And then he did something no teen idol does…" + a real interview clip saying it | "On a Friday"-style 2-frame montage; let a real clip play with its own audio |
| Consequence 37–51 s | Mistake → walk-out → back in 4 days | Indie run (*Good Time*, *The Lighthouse*) → the Batman casting backlash | 3×3 headline video wall (uncaptioned), warp transition, nested picture-in-picture |
| Aftermath 51–63 s | "Gone." refrain, $86B → $852B | "The critics? Gone. The petition? Gone." → box office / reviews numbers | Identical black verdict cards ×2; numbers sized up |
| Escalation 63–82 s | B&W archival, faces in strips, thesis line | B&W film stills, five-strip faces, a final line on reinvention | Red duotone flashes, strip slide-in, callback to a hook shot |
| Sting 82–86 s | Logo at 12 fps | Your own mark (or a "RP" monogram) | Scale-down, 12 fps, 1 s fade |

**What a matching edit needs from you:** the VO (your recording, or a local Kokoro TTS voice), a music bed (~100 BPM, sparse first half, groove from the middle), the footage/photos (interviews, red carpets, film stills, news chyrons, headlines), and the aspect ratio (4:3 like the reference, or 9:16 for Reels).

---

## 12. HyperFrames rebuild map

The effect, and the catalog item or technique to build it with. Check each against `/hyperframes-registry` when building.

| Effect | Build with |
|---|---|
| Two-font glow captions, word by word | `caption-editorial-emphasis` as a base, or hand-built spans with Instrument Serif Italic + Inter Display Bold, `text-shadow` stack (tight + wide), shown with GSAP `set` at whisper word times |
| Black captions on bright shots | Per-shot class swap (the reference does it per shot); `caption-blend-difference` is the automatic alternative |
| White flash frames | `flash-through-white`, `editorial-flash-overlay`, `transitions-light`, or a white div shown for 1–2 frames |
| Whip smears | `whip-pan-cut` / `whip-pan`, `motion-blur` |
| Word slam | `caption-kinetic-slam` / `headline-slam`, scaled to 400–500 % with a blur glow, 1–2 frames |
| Pixel-mosaic reveal | `grid-pixelate-wipe` (reversed) or a canvas pixelate with per-tile resolve |
| Grid builds / video wall | `transitions-grid`, `mk-placeholder-grid` (3×3) with per-tile flash |
| Glitch / datamosh | `glitch`, `rgb-glitch-text` |
| Corner chromatic fringe + vignette | `chromatic-radial-split` (as an overlay idea), `vignette`, `yt-screen-warp` |
| Light streaks / flares / leaks | `vfx-anamorphic-flare`, `lens-flare`, `light-leak`, `organic-light-leak-overlay` |
| "Switch" smoke dissolve | `particle-text-dissolve` |
| "fire even the" growing words | `blur-in` / `focus-blur-resolve` with a per-word scale step |
| Halftone portraits | `halftone-field` / `halftone-dissolve` styling, or pre-processed images |
| HUD / tracking boxes | `telemetry-hud` |
| Montage on twos | Image clips of exactly 2/23.976 s (0.0834 s) each |
| 12 fps logo | GSAP with time snapped to 1/12 s steps |
| Polaroid, strips, nested PIP | Plain HTML/CSS (borders, `clip-path`, staggered `translateX`, scale-in insets) |

---

## 13. Confidence notes

- **Font names are visual matches**, not identified files; the reference is 960×720 and compressed.
- **People are named only where the narration or an on-screen chyron names them**; others are described, not identified.
- **Music key is a low-confidence estimate.** Tempo/beat findings come from the separated music stem and are solid for 42–82 s (regular snare grid); the 0–42 s pulse is softer.
- **Word timings come from whisper.cpp (base.en)** and are ±1–2 frames.
