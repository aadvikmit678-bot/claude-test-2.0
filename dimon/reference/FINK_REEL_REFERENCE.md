# Reference: the Larry Fink reel, for the Jamie Dimon / JPMorgan Chase edit

The user's style reference for the next video. I measured it frame by frame: every second at 10 fps, and every animated beat at the full 30 fps.

- **Source:** Instagram reel `Dewt0XXoHtk`. The user's Drive copy is file id `1KijjBxmRkq5ICtjzSv0HCHBEPGcnlNjf`. Re-download it with:
  `https://drive.usercontent.google.com/download?id=1KijjBxmRkq5ICtjzSv0HCHBEPGcnlNjf&export=download&confirm=t`
- **Local copy:** `pattinson-work/refs/fink.mp4`. This folder is not committed.
- **Specs:** 1276×718, 30 fps, 85.0 s, H.264 plus AAC. It is already horizontal 16:9, like the Dimon edit, so its layout transfers 1:1. Multiply its pixel sizes by **1.504** for 1080p.
- **Files in this folder:**
  - `fink_words.json`: word-level VO timings as `[start, end, word]`.
  - `frames/`: contact sheets, both 10 fps overviews and 30 fps beat sheets. Each frame is labelled with its time.

---

## 1. Story: how the script is built

| # | Time | Beat | Device |
|---|---|---|---|
| 1 | 0.0–8.9 | "Donald Trump is not the President of America. This man is." Then a podcast clip: "Larry Fink, the guy running BlackRock, is really the President of the United States." Then "His name's Larry Fink." | A contradiction hook, backed up by an outside voice (a quoted clip), then the name reveal. |
| 2 | 9.0–15.1 | "And the thing that made him the most powerful person in America is the same thing that nearly ended his career." | A paradox that sets up the whole film. |
| 3 | 15.2–25.4 | 80s, mortgages "nobody cared about", invented the mortgage bond, "turned the whole of street into a money printing machine". | The rise. |
| 4 | 25.5–37.8 | One bet wrong, $100M lost in a quarter, First Boston "pinned every dollar on him", "threw him out", "acted as if he'd never existed". | The fall. |
| 5 | 37.9–48.3 | Takes the failure, builds Aladdin, walks it back to the same street; by 2007 every major firm runs on it. | The comeback, framed as revenge. |
| 6 | 48.4–62.9 | 2008 hits; the economy collapses because of the instrument he invented 20 years earlier. The government calls "the one person who understood the mess… the guy who built it". | Dramatic irony. |
| 7 | 63.0–77.8 | Three times the money, quietly bought the largest ETF business. Owns more NVIDIA than Jensen Huang and more Apple than Steve Jobs. | The payoff in hard numbers, compared against famous founders. |
| 8 | 77.9–82.4 | "You can vote out a president. You can't vote out the guy managing your retirement." | A kicker that calls back to the hook's word "president". |
| — | 82.4–85.0 | Light streaks converge into the creator's logo on black. | End sting. |

The VO is about 150 words per minute and conversational. Sentences are short, and every sentence ends on a concrete noun that gets its own picture.

---

## 2. Pace

- **Cuts:** 233 hard picture changes in 85 s, flash frames included.
- **Shot length:** real shots have a median of **0.45 s** and a mean of 0.58 s. The 25th–75th percentile is 0.29–0.63 s.
- **Holds:** only designed type beats hold longer: the 3.4 s quote panel, the 3 s typed and 3D card beat, and the 1.3–3 s donut charts. The longest single hold is 3.5 s.
- **Rule:** a new picture on almost every 1–3 words. Key nouns get a literal picture, sometimes three in a row. "invented" gets a blueprint, then gears, then a glowing burst, at 0.2–0.35 s each.
- **Camera:** almost every shot is static. Measured scale change over a shot is 1.00–1.02. The motion comes from cuts, type and flashes, not from pushes.

---

## 3. Typography: the core of the style

**One family throughout:** a tight bold grotesque, close to SF Pro Display or Inter Display Bold. In our kit that is **Inter Tight 700** for captions and **800** for heroes, with tracking about −0.02 to −0.035 em.

- **Case and punctuation:** mostly lowercase except names and sentence starts. **No commas or full stops** are shown.
- **Second face:** a condensed bold grotesque appears only on the 3D white card ("ended his career").
- **No serif anywhere** in this reference.

### 3.1 Line captions on footage (most of the film)

- **Look:** white, about **56 px at 1080p** (cap height about 41 px), weight 700, with a faint soft halo.
- **Position:** centred on the frame. The vertical centre is about **0.505 H** (y ≈ 545 at 1080p), so captions sit at the frame's centre, not low.
- **Length:** 1–4 words per line.
- **Layout:** the line is laid out once in its final centred position. Each word appears in place on the exact frame it is spoken.
- **Motion:** a hard cut. There is no fade, scale, slide or blur on these. Words never shift as the line fills. (Verified at 30 fps: "And" → "And the thing" → "And the thing that"; "whole" → "whole of" → "whole of street".)
- **Line change:** the next line replaces the old one on a cut. A line may span two picture cuts.
- **Exception:** in the NVIDIA and Apple chart beats, captions drop to **y ≈ 0.95 H** so the chart owns the centre.

### 3.2 Bar write-on (on black) — the signature

Seen at 25.53–27.6 ("But then / he got / one bet wrong").

- **Entry:** each word of the line first appears as a **solid white bar**, the word's width by its cap height, in the word's final position. Each bar **flips into its word in one frame** on the beat.
- **Exit:** a white bar **sweeps left to right over the line in 3–4 frames**, then the line is gone.
  - At 30 fps: 26.30 "he" becomes a bar again, 26.37 the bar covers "he g…", 26.43 one bar covers the whole line, 26.47 the next line's bars appear.
- **Variant in the quote panel (4.00):** the bars are frosted and translucent, and the words fade in over about 3 frames.

### 3.3 Hero lockups (one key word per sentence)

- **Hero word:** **125–230 px at 1080p**, bold, appearing instantly on its beat. It usually lands on the cut.
- **Context word:** a small companion at about 40–56 px, in the same family, tucked tight against the hero:
  - "the most / **powerful** / person"
  - "**money** / printing machine"
  - "starts / **collapsing**"
  - "**$100,000,000** / in a single quarter"
  - "called / **Aladdin**"
  - "**2008** / hits"
- **Colour:** white on footage; black on light grounds (Aladdin, mortgages, the name card).
- **Numbers grow in chunks on the words:** $100 → $100,000 → $100,000,000, left-aligned at x ≈ 0.1 W.
- **Years roll:** 2000 → 2005 → 2007 → 2008, with a chrome and cyan sheen on the digits.
- **Measured widths (1080p):**
  - "powerful": 551 px wide, about 125 px font.
  - "money": about 560 px, about 190 px font.
  - "$100,000,000": about 1550 px, about 230 px font.

### 3.4 Giant typed words on black ("is the same thing", "By 2007", "Today")

- **Look:** 300–600 px, white with a strong soft white glow (bloom).
- **Typing:** a new character every 1–2 frames. Each character arrives **dark grey and brightens to white over 2–3 frames**, roughly #666 → #aaa → #eee.
- **Camera:** the camera follows the cursor with **hard jump-reframes** about every 0.3 s, not a smooth pan. The text bleeds off the frame edges.
- **"By 2007":** "By" types small, then **jumps up and scales** as the year starts. "2007" fills the frame.
- **"is the same thing" continues into a 3D move:**
  - An overline draws over "thing" and fills down into a white box, so "thing" reads black on white.
  - The camera pulls back on a grey, grey, white flash.
  - The type plane tilts and rotates in 3D, so "the same thing" ends up running vertically.
  - The white box extends into a long white card reading "**ended his career**" in condensed black, which settles with a glow.
  - HUD wireframes flicker around it.

### 3.5 Stacked column (cold open)

- "Donald / Trump / is / not" stacks downward in a left column. Names are big (about 90 px at 1080p), and small words are small.
- A second column to the right of the seal: "the / president / of / **America**".

### 3.6 Name reveal

- On a white ground, "His name's" sits small and black above the card's top-left.
- "**Larry Fink**" **decodes letter by letter in random order**, each letter fading from pale to black, over about 8 frames. It is right-aligned under the card.
- At the same time, a **giant pale outline echo of the name** spans the whole frame behind it.

### 3.7 Quote panel (an outside voice)

- Big white “ ” quote marks frame small, left-aligned, stacked lines of the quoted speaker over the podcast clip.
- A dim, translucent ghost portrait-and-globe composite sits on the left.
- A four-point sparkle glints on the ghost's eye (4.27–4.43).

---

## 4. Pictures: how the B-roll matches the words

- **Literal noun-to-picture mapping.** Examples:
  - mortgages → house collage
  - mortgage bond → bond certificates
  - Wall St → street sign, Charging Bull, NYSE
  - money printing machine → cash piles and a cash box
  - $100M → bill close-ups
  - quarter → flip-calendar dates
  - First Boston → its sign and logo, so **no caption is needed when the picture says the word**
  - pinned → cartoon duck
  - threw him out → movie fight
  - never existed → the shot turned negative
  - Aladdin → a 3D lamp
  - walks → a walking pictogram
  - Then → hourglass
  - collapsing → dominoes
  - understood → chess clock
  - better than anyone → brain
  - ETF → iShares banner and BlackRock sign
  - on Earth → growth chart
  - vote → voting queue and a "Vote" card
  - president → Trump signing
- **Archival:**
  - 1970s–80s Wall Street street footage and trading floors.
  - NYSE facade with flag, the Charging Bull, the Wall St sign.
  - Bond certificates (Monmouth Title, Con Edison), dollar bills, counting machines.
  - 2008 floor panic.
- **The subject:**
  - Interviews from **many different stages** (Economic Club of Chicago, Power 100 Summit, Bloomberg, S&P Global, DealBook, BlackRock events), each 0.3–0.6 s. The variety itself signals power.
  - Portraits: a B&W young photo and a flag portrait.
  - With Trump, at the White House.
- **Graphic pictures:**
  - Pastel cut-out collage art on white (houses, hands, coins, clouds).
  - 3D renders: lamp, EMERGENCY buttons, brain, a gallery of floating screens.
  - Pictograms, blueprints, B&W macro (cells, gears), light bursts.
- **Pop culture:** The Wolf of Wall Street with purple face-detection boxes labelled "person", a cartoon, a movie fight.
- **Data:**
  - **Donut charts** in brand colours (NVIDIA green, Apple purple) fill around an extreme close-up of the subject's eye, with the logo reflected in his glasses. BlackRock's slice is blue and labelled.
  - A line chart with a moving cursor.

---

## 5. Transitions and textures (counted frame by frame)

| Device | How | Times |
|---|---|---|
| **Negative flash** (the signature cut) | 1–3 colour-inverted frames at a cut, sometimes alternating with normal frames | 2.93–3.07, 3.73–3.80, 5.93–6.00, 9.00, 12.07–12.13, 13.63, 15.20, 16.57, 20.20, 20.40, 22.03–22.10, 27.63, 31.33, 31.80, 33.53, 37.83–37.90, 40.00, 48.90, 63.13–63.20, 69.10, 70.00, 73.40–73.50, 74.83 (about 22 times, every 3–4 s) |
| White flash | 1 white frame | 2.77–2.83 (flare peak), 3.77, 12.10, 13.63, 22.07, 27.63, 33.53, 37.87, 63.17, 73.47 |
| Grey flash | 1–2 flat grey frames | 13.57–13.60, 25.50 |
| Light-ray burst | A four-point glint grows behind the seal, then rays fill the frame white | 1.87–2.83 |
| Particle dissolve | The photo disintegrates into white dust, the screen fills with particles, then they thin to a drifting starfield with bokeh | 0.93–2.6 |
| HUD wireframes | Thin white squares, lines and triangles plus tiny hex labels ("675.800.FFA"), flickering 1–2 frames | 0.0–0.5, 13.7–14.6 |
| Glitch | RGB-split slice displacement, then datamosh break-up | 38.93–39.20 |
| Halftone | Single halftone-dot frames inside a montage | 24.8, 41.7–41.8 |
| Style strobe | One motif in six looks, 2–3 frames each: white, halftone, orange on purple, grey, pixel red on blue, magenta outline | 41.4–42.67 (the walking man) |
| Thermal / pixel recolour | The same image cut to a posterised thermal look | 61.2–61.5 (brain) |
| Glass crack overlay | A shattered-glass texture over a sign | 68.3–68.5 |
| White wipe | A textured white panel sweeps across | 5.9 |
| Window zoom-out | The shot shrinks to a centred window on black, 100 % → 59 % in 0.55 s, ease-out | 33.6–34.15 |
| Card settle | A card on white shrinks from about 60 % to 35 % width, ease-out, about 0.35 s | 7.87–8.2 |
| 2×2 grid assembly | Four money clips fill their quadrants one by one | 27.67–28.5 |
| Logo sting | Diagonal light streaks converge to the centre and become the logo as the picture fades to black | 82.5–83.3 |

- **Grade:** dark and contrasty with heavy vignette, mostly desaturated or warm-amber or teal. Archival keeps its warm film look. Documents and macro shots are B&W.
- **Grain:** light.
- **Glow:** a soft bloom on all type, strong on the giant typed words.

---

## 6. Camera (measured with feature tracking)

- **Static:** most shots are static. Scale change over a shot is 1.00–1.02.
- **Hard punch-ins:** cuts to a 1.3–1.6× crop of the same image.
  - 3.33: Fink with the seal.
  - 39.23: the animated Fink.
  - 56.47: from the B&W group photo to young Fink.
- **Pushes:**
  - NYSE facade: +5 % in 0.55 s.
  - The eye during the NVIDIA donut: +19 % over 1.3 s.
- **Lateral pan:** across the bond stack, about 500 px/s at 1080p.
- **3D camera:** on the type plane, 13.4–15.0.

---

## 7. Sound

- **Music:** a continuous **dark, bass-heavy music bed** under the whole VO. Gaps between sentences sit at about −22 dB, never silent, and the bed carries on under the logo.
  - This differs from the Pattinson edit, which used SFX only. Ask the user whether the Dimon edit gets music.
- **SFX:** hits on flashes, glitches and big cuts. Level jumps land at 5.9, 9.1, 11.05, 31.1, 33.75, 38.6, 39.6, 45.9, 48.5, 53.25, 54.3, 57.25, 63.2 and 78.0.
- **Voices:** one narrator, plus a quoted podcast voice in the hook.

---

## 8. How Larry Fink is animated (each treatment)

1. **Cold-open reveal (2.87–3.70):**
   - Negative-flicker frames bring in a colour photo with the **presidential seal composited behind him**. It is the same seal that held Trump.
   - On "is", a **hard punch-in** of about 1.6× to his face.
   - A solarised flash frame, then a white frame.
2. **Name card (7.83–9.00):**
   - An inverted flash.
   - A **B&W cut-out on a red card** with 3D red ₿ logos, on white. The card settles from about 60 % to 35 % width.
   - The name decodes letter by letter, with a giant pale echo behind (see §3.6).
3. **Interview cutaways:** 0.3–0.6 s each, from many different events. Never the same stage twice in a row.
4. **The animated portrait (37.87–39.57), the key one:**
   - A one-frame white flash.
   - A dark, **top-lit photo of him seated at a long table**, hands on the table, warm amber, low key.
   - On "takes", the still comes alive (AI image-to-video): his neutral face turns into a **slow, knowing grin**, with slight head motion.
   - On "that", about 3 frames of **RGB-split slice glitch**. On "failure", about 5 frames of **datamosh break-up**.
   - It lands on a **1.3× punch-in** of the grin.
5. **Young Fink:**
   - A B&W 1980s group photo, then a hard punch-in to his face on "20 years earlier".
   - A young portrait with a slow push on "bought the".
6. **The eye (70.70–77.87):**
   - An extreme close-up of his eye with the NVIDIA logo reflected in his glasses.
   - A green donut ring fills around the eye, then the same beat repeats with the Apple logo and a purple ring.
   - The camera pushes +19 %.
   - Inverted flashes split the beats: 73.4 into Jensen Huang, 74.83 back to the eye.
7. **Close (81.50–83.30):** a close-up in front of the BlackRock backdrop. Diagonal light streaks converge on the caption and resolve into the end logo as the picture fades.

---

## 9. Shot-by-shot (times in s; type kinds refer to §3)

| Time | VO | Picture | Type | FX |
|---|---|---|---|---|
| 0.00–0.93 | Donald Trump | Black. Gold presidential-seal ring holding Trump photos that swap every 2–3 frames; scales up from 0.15 to 0.45 H; the photo becomes a tilted card behind the ring | Stacked column: "Donald" 0.03, "Trump" 0.40 | HUD wireframes |
| 0.93–1.40 | is not | The photo dissolves into dust, the screen fills with particles, then a starfield | "is" 0.73, "not" 0.97 | particle dissolve |
| 1.37–2.60 | the President of America | The ring now holds the real presidential seal; a glint grows behind it | Right column: "the president of **America**" | — |
| 2.60–2.83 | — | Rays from the seal fill the frame, then white | — | flare burst |
| 2.87–3.33 | This man | Negative flicker, then Fink (orange backdrop) with the seal behind him | "This / man", small, left | negative flicker |
| 3.33–3.70 | is | Hard punch-in to his face | "is" | punch-in |
| 3.80–7.77 | (podcast) "Larry Fink, the guy running BlackRock, is really the President of the United States" | Podcast host on the right; ghost portrait and globe on the left | Quote panel | white wipe 5.9 |
| 7.87–9.00 | His name's Larry Fink | The red name card on white | Name reveal | negative |
| 9.00–9.37 | And the thing | Fink at the Economic Club of Chicago | Line | negative |
| 9.37–9.63 | that | Fink portrait close-up | Line | — |
| 9.67–9.97 | made him | Power 100 Summit | Line | — |
| 9.97–10.47 | the most | A blurred zoom on him | Line | — |
| 10.50–10.97 | powerful | Hands together | Hero: "the most / powerful" | — |
| 11.00–11.37 | person | Gesturing, map backdrop | "person" small | — |
| 11.40–12.00 | in America | Close-up, blue backdrop | Line | — |
| 12.03–12.13 | — | Inverted frames, then white | — | negative + white |
| 12.13–13.53 | is the same thing | Black | Typed giant (§3.4) | — |
| 13.57–15.13 | that nearly ended his career | 3D type plane and the white card | Typed into 3D (§3.4) | grey, grey, white; HUD |
| 15.20–16.57 | Back in the 80s he looked at | 1980s NYC street, Wall St facade, crowd from behind | Line | negative |
| 16.60–17.40 | mortgages | Collage cards flip every 2 frames on white; zoom out to a collage wall | Hero, black, typed in from the right | — |
| 17.43–19.33 | stuff nobody on the street cared about | 1920s mortgage bonds, ticker board, 80s office, NYSE (+5 % push) | Line | — |
| 19.37–20.17 | and basically | Fink interview, then a close-up | Line | — |
| 20.20–21.07 | invented | Blueprint, gears, glowing burst | Line | negatives |
| 21.10–22.00 | the mortgage bond | Bond-certificate stack, panned | Line | — |
| 22.10–23.37 | turned the whole of street | Wall St sign, Charging Bull, trading floor | Line | negative + white |
| 23.40–24.03 | into a | The Wolf of Wall Street with face-detection boxes | Line | — |
| 24.03–25.47 | money printing machine | Cash montage | Hero: "money / printing machine" | halftone frame |
| 25.53–27.60 | But then he got one bet wrong | Black | Bar write-on (§3.2) | grey 25.50 |
| 27.67–29.17 | and lost $100… | A 2×2 money grid assembling | "lost a"; hero "$100" → "$100,000" → "$100,000,000" | white 27.63 |
| 29.20–30.87 | million in a single quarter | $100-bill close-ups, flip-calendar | "+ in a single quarter" | — |
| 30.90–31.77 | First Boston | Its sign, then its logo (slow push) | **none** | negatives |
| 31.80–33.47 | pinned every dollar on him | Cartoon duck, bill details, counting machine, a $50 sliding | Line | — |
| 33.57–34.17 | threw him out | A movie fight shrinking to a centred window | Line | white 33.53; zoom-out |
| 34.20–35.27 | and the rest of the street | 1980s trading split-panels | Line | — |
| 35.30–36.37 | basically acted | Wall St and the NYSE facade with Washington's statue | Line | — |
| 36.40–37.83 | as if he'd never existed | A young banker in an office, then **the same shot inverted** | Line | negative as meaning |
| 37.87–39.57 | So Fink takes that failure | The animated portrait (§8.4) | Line | white, glitch, punch-in |
| 39.60–40.77 | builds a system called | Rainbow light burst, B&W mechanism engraving | Line | negative |
| 40.80–41.37 | Aladdin | 3D lamp on grey | Hero (black): "called / Aladdin" | — |
| 41.40–42.67 | and walks it right back | Walking pictogram in 6 styles | Line | style strobe |
| 42.70–44.67 | to the same street that threw him out | "2 WALL STREET" engraving, then 1970s street people | Line | — |
| 44.70–45.77 | By 2007 | Black | Typed giant: "By", then "2007" | — |
| 45.80–48.37 | every major firm on the street is running on it | 80s office, terminal keys, 80s computer, "NOW is the Time for S&Ls" ad | Line | — |
| 48.40–48.87 | Then | B&W hourglass | Line | — |
| 48.90–50.07 | 2008 hits | 2008 floor panic | Year roll (hero) + "hits" | negative |
| 50.10–51.97 | The entire global economy starts | Five 2008 chaos shots | Line | — |
| 52.00–53.07 | collapsing | Dominoes | Hero: "starts / collapsing" | — |
| 53.10–54.87 | because of the exact instrument | Text characters dispersing, old deeds, a $500 bond with a green dot | Line | — |
| 54.90–55.70 | Fink invented | B&W macro: cells, metal, film strip | Line | — |
| 55.73–57.07 | 20 years earlier | B&W group photo, then a punch-in | Line | — |
| 57.10–59.17 | So the government calls the one person | With Trump, interview, dark office, flag portrait | Line | — |
| 59.20–61.57 | who understood the mess better than anyone | Chess clock, 3D screen gallery, EMERGENCY buttons, brain, thermal brain | Line | — |
| 61.60–63.10 | The guy who built it | Waving, walking with a map overlay, crowd | Line | negative + white |
| 63.20–64.97 | Fink came out of that crisis with | Bloomberg, S&P Global, TV set | Line | — |
| 65.00–66.17 | three times the money | Cash counting machine | Line | — |
| 66.20–67.47 | and quietly bought the | Stage, young portrait | Line | — |
| 67.50–69.97 | largest ETF business on Earth | iShares banner, BLACKROCK sign (+ glass crack), growth chart | Line | negative |
| 70.00–70.67 | Today | Black | Typed giant | — |
| 70.70–73.37 | he owns more of Nvidia than Jensen Huang | Eye close-up, NVIDIA donut | Bottom line | push |
| 73.50–74.77 | who built it from nothing | Jensen Huang on stage | Bottom line | negatives |
| 74.90–77.87 | And more of Apple than Steve Jobs ever did | Eye close-up, Apple donut | Bottom line | — |
| 77.90–79.37 | You can vote out a president | Voting queue, "Vote" card, Trump signing | Line | — |
| 79.40–82.40 | You can't vote out the guy managing your retirement | Three Fink interviews | Line | — |
| 82.40–85.00 | (music) | Streaks converge into the logo on black | — | logo sting |

---

## 10. Carrying it into the Jamie Dimon edit (16:9, 1920×1080, 30 fps)

### Structure template
1. A contradiction hook, backed by an outside voice.
2. The name reveal.
3. A paradox line.
4. Rise.
5. Fall. For Dimon: fired by Sandy Weill at Citigroup in 1998.
6. Comeback: Bank One, then JPMorgan.
7. Crisis irony: in 2008 the government calls him for Bear Stearns and WaMu.
8. Scale payoff in numbers: largest US bank, the new 270 Park Avenue HQ.
9. A kicker that calls back to the hook.

### Our toolkit, mapped to each device
- **Line captions:** a pre-laid-out centred line, with each word as a timed element that hard-cuts on.
- **Bar write-on:** white bar elements sized to each word that swap to the word on the beat. Exit is a bar sweeping left to right over the line in 3–4 frames.
- **Hero lockups:** an Inter Tight 800 hero plus a small 700 context word, set tight.
- **Typed giant words:** per-character spans stepping grey → white over 2–3 frames, with camera jump-reframes about every 0.3 s.
- **Negative flash:** the scene's `.neg` difference-blend element, 1–3 frames. This is the reel's main cut.
- **White flash:** `whiteflash`.
- **Window zoom-out:** an ease-out scale to about 0.6.
- **Card settle:** a card on white, scale 1.7 → 1.0 ease-out, about 0.35 s.
- **Name decode:** per-letter spans in a seeded random order, pale → black over about 8 frames, plus a giant pale outline echo.
- **Donut charts:** SVG arcs tweened by GSAP (deterministic), with brand colours.
- **HUD wireframes:** SVG lines and squares stepped on and off.
- **Glitch and halftone frames:** canonical grading only (`glitch` and `halftone` payloads), no CSS filters on footage.
- **Particle dissolve:** search the registry first, otherwise seeded canvas particles.

### Open items to ask about before building
- **The animated portrait:** the AI image-to-video grin needs a generated clip. Either the user supplies one, or I make one through `/media-use` (HeyGen or another provider, at a cost).
- **Music:** the reference has a music bed; the Pattinson edit used SFX only.

### What the Drive already holds
The Drive folder "Jamie Dimon" (id `1nC7mwKB1Baj2aL5CQehlxG5ztOkuh7WJ`) holds documentaries, Dimon speaking, the HQ ribbon cutting, 2008 crash and Wall Street footage, a Wolf of Wall Street clip, an image pack, halftone textures and money/Pinterest clips.

---

## 11. What makes it read as animation (learned the hard way on Dimon v1)

v1 matched the device list but still read as a documentary with captions. The reel reads as motion graphics because:

- **The opening is pure graphics, no footage.** 0–2.8 s is black, HUD wireframes, a seal ring rushing toward the camera
  (it grows about 5× in 0.9 s) with photos flipping inside it every 2–3 frames. The photo turns into a tilted card
  behind the ring, bursts into a dense cloud of specks that fills the screen, and the specks thin into a drifting
  starfield. The subject's face only arrives at 2.9 s, through negative flicker. Never open on a talking head.
- **Graphic B-roll carries the abstract words.** Chess clock, a gallery of floating screens, 3D "EMERGENCY" buttons,
  a 3D brain turned thermal, a 3D lamp, a walking pictogram, a rainbow light burst, engravings, collage art. These are
  stylised stock renders, not documentary footage. For Dimon they come from the Pinterest folder (3D chess,
  surreal engraving montage, fire with a silhouette) and the trading-screen clips.
- **Plain footage is short and treated.** Interview cutaways last 0.3–0.6 s. Shots get recoloured frames: teal
  negatives, a blue/red solarised frame before a new section, a thermal recolour, a map composited behind a walking
  subject.
- **Graphic compositions never hold still.** Rings grow, cards tilt, particles drift, the starfield moves, the globe
  turns. Only the footage shots are static.
