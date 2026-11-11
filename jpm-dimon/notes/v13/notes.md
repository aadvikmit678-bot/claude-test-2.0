# v13: the back half re-edited; three fixes in the first half

`tools/build13.py` (from build12) writes `tools/media_v13.json`. The film is 85.16 s at 60 fps, 21 scenes.

Rebuild:

```bash
export DIMON_ROOT=<repo root> CV4_DIR=<repo root>/dimon-work/cv4
python3 -I tools/prep13.py pics bezos              # the paintings, the cleaned Bezos clip (once)
python3 -I -X utf8 tools/build13.py --specs        # writes tools/media_v13.json
python3 -I tools/prep2.py --spec=media_v13.json    # cuts the clips
python3 -I tools/prep13.py mattes                  # the cut-out of Dimon for "standing"
python3 -I -X utf8 tools/build13.py                # writes index.html and compositions/
npx --yes hyperframes@0.9.2 render --fps 60 --workers 2 -o renders/jpm-dimon-v13.mp4
```

Everything is HyperFrames: HTML and GSAP written by the builder, rendered by the `hyperframes` CLI. ffmpeg only cuts the source clips; `hyperframes remove-background` makes the one cut-out.

## The notes of 11 Nov and what v13 does

| Note | What v13 does |
|---|---|
| "After this [A guy who got FIRED] the fade transition is very bad. Change it." | No fade. Two frames after the hero photo lands, the whole page dives through the photo (the square fills the frame in a fifth of a second), one white frame, and the Citigroup shot arrives still moving under the year counter. `sp_fired_flip(through=)`, `sp_roller(arrive=)`. |
| "This 'in the world' pic with panning is very bad. Change it to this video of the world, from 2 min 1 sec." | Their film of the planet from 121.0 s (the sun coming over its edge), letterbox cropped away, on a slow push. The map and its pan are gone. Prep2 key `WORLD`. |
| "The frame part with 3 frames: the panning is very fast … sloppy. Maybe a low frame rate and a smoother animation, keyframes that ramp up." | The pinboard's camera is keyed by hand at 15 fps (posterized time). Each move starts slowly, ramps up and settles long, about a second each; between moves it keeps creeping. The cards carry a blur that follows the speed of each step. The white flashes on the moves are gone, and the cards sit closer so there is always a card in view. `kboard11(moves=, fps=)`; `fps=60` gives a smooth camera again. |
| "Make it a video playing of Jamie Dimon … why are you just sticking to documentaries" (0:34) | The pinboard's full-frame shot and first card are their own video of him talking in the office (`SPEAK` 12.2). The other two cards are moving footage too (the Citigroup launch, Weill at the lectern). |
| "Pics should come like motion graphics … not simply there for 2-3 seconds with a zoom effect" | No still is shown with a zoom. A picture is only ever a designed move: `kpaint` (a card on the lit paper that grows in steps as its view widens, then a zoom-blur to the full frame; whip-pans and glides between details). `tools/motion_audit.py` found the documentary stills that v12 had played as footage; all are replaced with moving shots. |
| "After 18 months … he took up boxing, read biographies, to cut to Bezos: something like this video from the 53rd second" + the Renaissance pictures + the Bezos clip | S11-S12, below. |
| The Dimon montage "from 22 second" and the fire clip for "the greatest comeback"; "history of Wall Street is fine" | S13, below. The strips stay; the one still among them is replaced. |
| "Mixture of Helvetica Bold plus Instrument Serif"; "why is it bouncing pop and then coming" | Small words in Helvetica Bold (Inter Tight 700), hero words in Instrument Serif, everywhere from S10 on and again in S01, S04, S05, S06. The serif heroes arrive in the film's normal bloom; the glitch entrance and the blown-out pop are gone. Numbers that count are bold Helvetica. No italic, no yellow. |
| "Golden Boy: the skeleton is coming for a bit more time" | The X-ray shows for three short flickers (4, 4 and 2 frames of 60) instead of holding. |
| "The moving-out-of-perspective … like Hemant Taneja's" | The hand-over from Bezos into S13: his shot eases back into a card, turns away in perspective and leaves to the left while the next shot arrives still moving. |

## The back half, scene by scene

- **S10 "But then, at 42, he was fired."** Pictures unchanged (the user: keep the soul-out push). Words in the mixture.
- **S11 "18 months of no job."** The lit paper. Matejko's jester is a card on the right growing in three steps; a month counter in black Helvetica runs to 18, "months" in the serif under it. On "no job" a zoom-blur throws the card to the full frame.
- **S12 "He took up boxing, read biographies, even met Bezos for a job at Amazon."** The boxing picture as a tiny card growing on the paper, thrown to the full frame on "boxing". A whip-pan to the readers at their table; the camera glides from the old reader to the men at their book. A glitch cut to Bezos in 1999 (their clip, the two corner graphics blurred out, his whole face in frame), the words beside him: his name in bold Helvetica, Amazon in the serif.
- **S13 "But it was all a premise for the greatest comeback in the history of Wall Street."** The Hemant hand-over; their Dimon montage (a finger to his lips); on "premise" four more of its shots pop out as cards, each after a white box; "greatest" on his face, close; "comeback" on their man before the fire, the word burning behind his chair (`mix-blend-mode: color-dodge`, so the dark silhouette cuts it out); then the strips.
- **S14 "In 2000, he takes over a broken bank in Chicago,"** the towers from the air, the year rolling to 2000; him at Bank One; the bank's door; Chicago.
- **S15 "cuts the dividend, cleaned it up,"** him, hands cutting the air; a light streak wipes to the floor at work.
- **S16 "and puts $60 million of his own money into the stock."** The figure counts up to $60 beside "million"; the coins picture as a card thrown to the full frame on "money"; the exchange floor.
- **S17 "Turn a $500 million loss into billions in profit."** The Chicago pit, the figure counting to $500; the floor on "loss"; the counting machine; him striding in.
- **S18 "That bank got acquired by JP Morgan in 2004."** The handshake; the name on the glass; the flag with the year rolling to 2004.
- **S19 "Then, 2008 financial crisis hit,"** a run of the crash, ten frames a shot, the year rolling to 2008; the anchor; Lehman's sign.
- **S20 "and when every other bank was dying, he was the only one standing"** (one scene). The bankers before Congress; then the Hemant roll-up: a curved 3D band of moving cards with Dimon in the middle and the banks of 2008 either side. On "dying" they go grey and drop out. His card comes forward and fills the frame; "standing" is a giant word behind him.
- **S22 "with enough money to buy the ones that fell."** The treasury picture as a card thrown into its chests of coin; the anchor under FIRE SALE; Bear Stearns and Washington Mutual as two cards that drop on "fell".
- **S23 "That's JP Morgan and Chase, the name that moves $10 trillion every single day today."** A mosaic of nine moving cells, the name typed across it letter by letter as at the film's opening; the tower at sunset and dusk with the figure counting to $10 beside "trillion"; "every single day" one word a shot; the tower at night with "Today" typed across it; out to black.

## New in the builder

`kpaint`, `pregion` (a painting as motion graphics), `kpop` (a card after a white box), `kmosaic`, `kcarousel` (the 3D band; its wrappers are untimed, each card's edge is on its video), `kbehind` and `kword` (a word in the scene, behind a subject or blended with the picture), `kcount` (a counter on whole frames), `kstreak`, `kglitch`, `kfall`. `CL` adds the clip's width to its id when it is not the standard one.

## Sources added (dimon-src, not in git)

- `_v13/ren/`: the seven Renaissance pictures and the Bezos clip from the Drive folder; `_v13/bezos_clean.mp4`.
- `_v13/dl/dimon_montage2.mp4`, `_v13/dl/comeback2.mp4`: the Dimon montage and the man before the fire.
- `_v13/world/world_src.mp4`: the film of the planet.

## Checks

`hyperframes lint`: 0 errors. `hyperframes check`: 0 errors in lint, runtime, layout, contrast (15 of 15 samples pass), audio. Every new clip was scanned for a cut inside its shown span; four were moved.

## Known limits

- The boxing picture is 550 px wide at source; it is soft at the full frame.
- The Dimon montage is 720 px wide and the planet film 1280 px letterboxed, so both are enlarged.
- Higgsfield could not be used (the account is on the free plan with no credits), so nothing in the film is generated.
- The Karp reel would not download again on 11 Nov; the earlier frame notes on it were used.
