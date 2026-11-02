# SPEC — "The Post-Twilight Reinvention" (Robert Pattinson)

Style source: `../reference/f1-horner-reel-breakdown.md` (Metro Media House F1 reel). Same grammar,
new subject. Where this file and the reference disagree, the person's own request wins
(Instrument Serif, glow captions, halftone / VHS / old-film textures, no music, SFX only).

```text
GOAL:    the viewer laughs at the "beggars" cold open, then finishes convinced Pattinson's
         post-Twilight run is one of the great reinventions — the 2026 slate lands as a 1-2-3 list.
OUTPUT:  HyperFrames, 1920 x 1080 (horizontal only), 30 fps.
TIME:    74.00 s x 30 = 2220 frames. No music bed (person's request). The voice is the clock.
```

## Audio map (global seconds)

| Global | Source | Notes |
|---|---|---|
| 0.00–5.40 | `assets/audio/sting-beggars.wav` | Demucs vocal stem of `Starting frame.mp4` 0–5.4 (fan line, then Antinous' line, laugh). Source music removed. |
| 5.40–30.30 | VO 0.00–24.90 (seg A) | "Robert Pattinson … Twilight jokes," |
| 30.30–32.60 | `sting-spider.wav` | "You better hold on tight, spider monkey." (Twilight, vocal stem) |
| 32.60–38.00 | VO 24.90–30.30 (seg B) | "he was quietly … became Batman." |
| 38.00–38.90 | — | 0.9 s held impact for the Batman reveal |
| 38.90–44.85 | VO 30.30–36.25 (seg C) | "The vampire kid … And this year?" |
| 44.85–45.85 | — | 1.0 s breath: the 1-2-3 triptych builds |
| 45.85–57.80 | VO 36.25–48.20 (seg D) | Odyssey + Primetime chapters |
| 57.80–59.90 | `sting-seat.wav` | "…don't you have a seat right there?" (Primetime trailer, vocal stem) |
| 59.90–71.42 | VO 48.20–59.72 (seg E) | Dune + payoff |
| 71.42–74.00 | — | End card hold, final hit |

Word clock: `global = vo_start + offset` with offsets A +5.40, B +7.70, C +8.60, D +9.60, E +11.70
(`../pattinson-work/words_global.json`). VO normalised to about -16 LUFS. SFX sit 6–10 dB under
the voice (volume 0.25–0.45); every effect has a cause on screen; whooshes rotate 3 takes.

## LOOK (numbers, from the reference)

- **Footage grade**: milky matte. Blacks lifted to about 20/255, highlights rolled off to about
  221, saturation about 0.26. Applied with `media-treatment` (`adjust.contrast -0.12`,
  `saturation -0.12`, `details.grain 0.10`), never CSS filters.
- **Paper**: `#EEE4E0` centre → `#E0D7D4` edges, soft oval vignette, 1.5 % fibre noise
  (`assets/tex/paper.png`). Used as the full-screen breath and as a desk for photo cards.
- **Photo cards**: 45–70 % of the frame, 6 px off-white border `#F4EFEB`, shadow `0 18px 40px
  rgba(0,0,0,.28)`, card rotation ±0–2°, slow push 1.00 → 1.04 per 2 s.
- **Ink, white captions**: `#F7F4F7`, Inter Tight 700, tracking -4 %. The glow (person's
  request) is `text-shadow: 0 0 12px rgba(255,255,255,.55), 0 0 34px rgba(255,255,255,.22),
  0 3px 10px rgba(0,0,0,.40)`.
- **Ink, hero words**: Instrument Serif (400 and Italic), tracking -2 %, with the same glow plus
  a bloom of 0 0 60px rgba(255,255,255,.18) while it lands.
- **Ink, paper**: `#0B0B0B` Inter Tight 700, punch words in Instrument Serif Italic black.
- **One-off accent**: electric blue `#1C59F7` on the "SPIDER MONKEY" shout only, in Archivo
  Black. This mirrors the reference's single blue radio shout.
- **Textures** (person's request):
  - Halftone (`editorial-halftone` treatment) on Twilight-era tabloid moments.
  - VHS (`vhs-playback`) plus scanlines on Primetime, the 2006 TV world.
  - Old film (`home-movie-8mm`: dust, scratches, weave) on the Twilight memory beats.
  - Film burn shader at "post-Twilight".
  - Organic light leaks at 2 motivated handoffs.
  - Global grain at 6 %.
- **Sizes (1080 tall)**: function words 40 px cap, normal words 64–80 px, hero words 150–230 px,
  counters 260 px, chapter numerals 520 px with a bottom alpha fade.

## Caption system (the reference's grammar)

- One word or one short lockup on screen at a time. A group changes on every spoken word. Words
  arrive 2 frames before they are spoken.
- **White entrance ("glow coming in")**: opacity 0 → 1, `blur(16px)` → 0, scale 1.12 → 1.00,
  bloom text-shadow 60 px → resting, over 7 frames, ease `expo.out`. A second word in a lockup
  blurs in on its own word time, left to right.
- **Paper entrance**: hard cut in at scale 1.14 → 1.00 over 12 frames, ease `expo.out`, no blur.
- **Lockups**:
  - small-over-big: "is having a / *generational*", "the / *fastest*".
  - big-over-small: "*Batman.*", chapter "1 / The Odyssey".
  - two-line names: "Robert / Pattinson", "Edward / Cullen".
  - Placement moves into negative space when a face fills the centre.
- **Exit**: hard cut to the next group. A blur-out of 6 frames is used only on "luck"-style
  closers ("coming.", "role.", "seen.").
- **Radio / sting lines**: small sentence case, Inter Tight 600 at 34 px, top-centre, the whole
  line at once.

## MOTION

- Arrive `expo.out` (7–12 frames); camera pushes `sine.inOut`; zoom-through `power3.in`.
  Exits are 40 % shorter.
- Stills always push 1.00 → 1.05 across their life (Ken Burns), never static.
- Hard cuts on the word (2 frames early). About 1 visual change per second; strobes are 5 frames.

## Transition kit (the reference's devices, 6 kinds)

1. **Negative flash**: white `mix-blend-mode:difference` layer over the footage only, 2–6
   frames, on about 1 in 5 cuts (12 total).
2. **Pixel-mosaic resolve**: animated `pixelate` treatment 1 → 0 over 15 frames. Used at 5.40.
3. **Paper card drop / scale-to-card / zoom-through blowout**: white exposure flash.
4. **Whip / zoom blur** on "swing", "run".
5. **Triptych / 5-panel builds** that expand to full frame. Also the tile-grid multiplication.
6. **Film burn** (shader, once) and **organic light leak** (twice). The glitch / VHS tear only
   in Primetime.

## SHOTS (global seconds; ↘ = transition in)

| # | t | Picture (source) | Captions | Sound / transition |
|---|---|---|---|---|
| 1 | 0.00–1.50 | Venice autograph (Starting frame 0.00–1.50), 4:3 → 16:9 crop | cover captions: somebody / get these / **beggars** / out of here? | fan line; camera shutters at 0.35 and 1.10 |
| 2 | 1.50–3.10 | laughing close-up in shades (Starting frame 1.50–3.10) | "out of here?" until 2.00, then clean | laugh |
| 3 | 3.10–5.40 | THE ODYSSEY, Antinous at the feast (Starting frame 3.10–5.40) | somebody get these / ***beggars*** / out of here! | ↘ negative flash (3 frames) + whoosh; Antinous' line |
| 4 | 5.40–6.52 | hero portrait solo-03, pixel-mosaic resolve | Robert / Pattinson (two-line serif, left) | ↘ pixel resolve; impact-bass |
| 5 | 6.52–7.96 | portrait shrinks to a paper card; 2026 slate card (eatmovies) | is having a / ***generational*** | paper slide |
| 6 | 7.96–8.52 | Batmobile through fire (montage 31.2–32.5) | run, | ↘ white blowout zoom-through; whoosh |
| 7 | 8.52–8.66 | black frame | and | — |
| 8 | 8.66–9.56 | Kimmel laughing (interview 3:28) | honestly, (right) | ↘ white silhouette flash (2 frames) |
| 9 | 9.56–11.00 | PAPER | nobody / saw / it / ***coming.*** | paper tick |
| 10 | 11.00–12.12 | Twilight cards drop on paper, halftone (cast 01, poster 10, 13) | to / some / people, | card thuds ×3 |
| 11 | 12.12–13.00 | Edward in biology class (Twilight 0:24) | he'll / always be (right) | — |
| 12 | 13.00–14.20 | Edward pale close-up (face montage 7.4–8.8), 8mm film | Edward / Cullen (two-line serif) | sparkle shimmer |
| 13 | 14.20–15.48 | sparkle-skin reveal (Twilight 3:25.5–3:29) | but / ***everything*** / he did after | ↘ negative flash |
| 14 | 15.48–16.20 | Twilight poster card on paper, halftone | ***Twilight*** | ↘ film-burn shader out at 16.10 |
| 15 | 16.20–17.88 | year counter 2012 → 2026 over a 5-frame strobe of 11 roles | proved / he was never / stuck (small, under counter) | key ticks per year |
| 16 | 17.88–18.60 | PAPER | with one / ***role.*** | — |
| 17 | 18.60–23.72 | 5-panel build: Good Time · The Lighthouse · Tenet · The Batman · Mickey 17 | film titles in serif per panel + years | panel whooshes ×5 |
| 18 | 23.72–25.00 | tile wall 2×2 → 4×4 of roles | every one / of them / was a | tile clacks |
| 19 | 25.00–25.40 | The Lighthouse soot face (Starting frame 20.5–22.0) | ***weird,*** | ↘ negative flash |
| 20 | 25.40–25.88 | Good Time blond Connie (clips 24.6–28.3) | ***bold*** | — |
| 21 | 25.88–26.44 | The King battle (montage 17.0–17.9) | swing | ↘ whip |
| 22 | 26.44–27.96 | PAPER | nobody / ***expected*** / from him. | — |
| 23 | 27.96–29.32 | Twilight stills drop as halftone tabloid cards (03, 08) | and while / the internet / kept making | card thuds |
| 24 | 29.32–30.30 | sparkle close (Twilight 3:29.5) halftone | Twilight / ***jokes,*** | — |
| 25 | 30.30–32.60 | STING: Edward + Bella tree climb (Twilight 6:38.4–6:40.7) | "you better hold on tight," + **SPIDER MONKEY** (blue shout) | sting audio |
| 26 | 32.60–33.86 | Pattinson on The Batman set as Bruce (BW photo 2) card | he was / quietly / working | — |
| 27 | 33.86–34.98 | Nolan with the IMAX camera (odyssey-47 left) card | with the best / ***directors*** | — |
| 28 | 34.98–35.62 | 4-frame strobe of director/film pairs | ***alive,*** | key ticks |
| 29 | 35.62–36.74 | Bruce Wayne on set, police car (BW photo 1) | until / one day, | — |
| 30 | 36.74–37.30 | cowl close-up (Batman clip 28.3–31.0) push | he became | impact-bass-2 swell |
| 31 | 37.30–38.90 | Gotham sunrise silhouette (Batman clip 31.0–32.9) | ***Batman.*** (huge serif, glow) | ↘ negative flash + bass impact |
| 32 | 38.90–40.28 | young Pattinson (pat image 5), "vampire" behind his head | the / ***vampire*** / kid | text behind subject (cutout) |
| 33 | 40.28–41.24 | Twilight-era fan frenzy, halftone (story 20.3–22.4, top crop) | everyone / ***laughed*** at | — |
| 34 | 41.24–42.68 | The Drama red carpet (carpet walk) as a vertical card | is now one of the most / ***respected*** | camera flashes |
| 35 | 42.68–44.04 | portrait cards drop (solo 01, 04, 06) | actors in / ***Hollywood.*** | card thuds |
| 36 | 44.04–44.85 | PAPER | and / ***this year?*** | — |
| 37 | 44.85–45.85 | triptych build: Odyssey · Primetime · Dune, numerals 1 2 3 | — | 3 whooshes |
| 38 | 45.85–47.60 | panel 1 expands; Antinous firelit (general montage 8.0–12.3) | 1 / The Odyssey (chapter), then he walked into / Christopher / ***Nolan's*** | — |
| 39 | 47.60–48.32 | The Odyssey poster (fire horse) | ***The Odyssey*** | — |
| 40 | 48.32–49.20 | Antinous at the feast (Starting frame 7.83–9.80) | as / ***Antinous,*** | — |
| 41 | 49.20–51.36 | Antinous in the arch (Starting frame 5.83–6.80) → | one of the story's / central / ***antagonists.*** | negative flash at 50.9 |
| 42 | 51.36–52.64 | panel 2 expands → PRIMETIME title card (VHS) | 2 / Primetime (chapter), then came / ***Primetime,*** | VHS glitch |
| 43 | 52.64–54.32 | Pattinson as Chris Hansen (montage-2 6.2–8.8), VHS | with Pattinson / playing a / television | — |
| 44 | 54.32–55.04 | 2006 TV schedule board (montage-2 12.0–13.2), VHS | ***journalist*** | — |
| 45 | 55.04–56.16 | sting house (montage-2 3.3–6.2), VHS | at the center of / controversial | — |
| 46 | 56.16–56.72 | chat screen "wanna come over?" (montage-2 10.0–10.7) | ***predator*** | glitch hit |
| 47 | 56.72–57.20 | hidden camera (montage-2 13.9–14.5) | sting | — |
| 48 | 57.20–57.80 | strobing face close-up (montage-2 15.2–19.1) | ***operations.*** | — |
| 49 | 57.80–59.90 | STING: Hansen in the pink room (primetime-02 still), VHS | "…don't you have a seat right there?" | sting audio |
| 50 | 59.90–61.86 | panel 3 expands; Scytale (general montage 12.3–16.6) | 3 / Dune (chapter), then and now he's / closing out / the year | — |
| 51 | 61.86–62.90 | Scytale still (dune-56) | with / ***Dune.*** | bass impact |
| 52 | 62.90–64.58 | 5-frame photo strobe of 10 roles | Pattinson keeps / choosing / ***roles*** | key ticks |
| 53 | 64.58–66.58 | tile wall 4×4 → 2×2 → one tile that becomes a box | that stop anyone / from putting him / in ***one box,*** | tile clacks, thud |
| 54 | 66.58–67.86 | Edward card (Twilight), 8mm | and that / post | — |
| 55 | 67.86–68.50 | film burn through Edward → | ***Twilight*** | burn whoosh |
| 56 | 68.50–69.22 | split: Edward (left) / The Batman (right) | ***reinvention*** | — |
| 57 | 69.22–71.42 | PAPER | might be / one of the / ***best*** / we've ever / ***seen.*** | — |
| 58 | 71.42–74.00 | PAPER end card | Robert / Pattinson (black serif), "2008 → 2026" small | final soft impact |

## BANNED (this film)

- Music beds or music bleed from source clips (vocal stems only).
- Burned-in source captions showing beside ours: cover them exactly or avoid them.
- Watermarks ("freshcuppa", "Gala", film-title cards): crop them out.
- A dark void with small floating text; everything centred; the same entrance on every element.
- Text that drifts after it lands; titles sliding up; generic fades between worlds.
- Glows on the paper ink, which stays flat black.
- Any frame where a caption sits on a face.

## QA frames

0.5 (cover captions hide the burned ones), 3.9 ("beggars" over Antinous), 5.7 (pixel resolve),
7.3 (paper card lockup), 13.5 (Edward / Cullen), 16.9 (counter), 21.8 (5 panels), 24.6 (tile
wall), 31.5 (spider monkey shout), 37.8 (Batman), 39.6 (text behind subject), 45.5 (triptych),
52.0 (Primetime VHS), 56.4 (chat screen), 62.4 (Dune), 65.8 (one box), 68.8 (split),
70.9 (paper seen.), 73.0 (end card).
