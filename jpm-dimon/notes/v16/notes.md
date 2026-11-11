# v16: the third batch of notes on the v13 render

`tools/build16.py` (from build15) writes `tools/media_v16.json`. The film is 85.62 s at 60 fps, 22 scenes. v14 and v15 were built but never rendered; v16 contains them.

Rebuild:

```bash
export DIMON_ROOT=<repo root> CV4_DIR=<repo root>/dimon-work/cv4
python3 -I tools/prep14.py                         # v14: the grudge cut-out, the Bold face, the name run's last portrait
python3 -I tools/prep15.py                         # v15: the first Flow clip, the Bezos cut-out, the warehouse
python3 -I tools/prep16.py fonts flow2 strip       # v16: the Bold Italic face, the second Flow clip, the card's red edge
python3 -I -X utf8 tools/build16.py --specs        # writes tools/media_v16.json
python3 -I tools/prep2.py --spec=media_v16.json    # cuts the clips
python3 -I tools/prep16.py mattes                  # the cut-out of Dimon for "standing"
python3 -I -X utf8 tools/build16.py                # writes index.html and compositions/
npx --yes hyperframes@0.9.2 render --fps 60 --workers 2 -o renders/jpm-dimon-v16.mp4
```

## The notes and what v16 does

| Note | What v16 does |
|---|---|
| "I don't want italics everywhere, only where there is emphasis, like JPMorgan, by JP Morgan, or in 2004." Then, on the stills: "why are you changing everything that was in Instrument Serif glow, the original one … we can have a mix", with a list of the lines to put back; and "only the ones I have told right now; if you have turned some other fonts into italic, keep it like that." | The type is a mix, word by word (table below). |
| "$60 million: why are 60 and million looking very different?" / "$500 million is also written very badly." | Each figure is one style: `$60 million`, `$10 trillion` in bold Helvetica 200. ($500 million is now inside the user's own clip.) |
| "2004 is coming in a bouncing way." | 2000, 2004 and 2008 no longer roll or pop. A small word over a big bold year; they appear as the other words do. |
| "From the 2008 crash there is all of a sudden panning and zooming of the videos. I want just direct fast cuts." | From S13 to the end no shot is pushed, slid or dropped. The 2008 run is seven shots of ten frames, cut straight. |
| "Every other bank": "not exactly like [the Hemant reel] … close up, not far … very smoothly, flowing very softly"; then, on the first build: "the whole roll is coming as a slant … on the right there is some gap … this black text should have soft edges … slowly and smoothly both. Use fewer frames." | `krollup`, below. |
| "At 1:14, dying, and then you suddenly switch. I just want it directly cut there. No falling of the images." | A hard cut from the band to Dimon at the lectern. No cards go grey, drop or zoom. |
| "Why is the standing text sliding from right to left? Standing can come normally just behind Jamie Dimon, exactly like comeback." | The word stands still behind him (a cut-out of the same shot over it) and arrives as "comeback" does: soft, then sharp, in place. |
| "That 'fell' at the last is also very bad … that falling of those pictures is very absurd." | Two plain cuts: the Bear Stearns sign, the Washington Mutual branch. Nothing falls. |
| "For 'with enough money' I want this exact same style … Sean Desmond's video at 'powers lending and banking operations', the 16th and 17th seconds, with the same typography." | `kcardref`, below. |
| "Here's the video you can use: of his own money into the stock, turn the 500 million. The video cuts at that, and then the money video into billions of profit with Jamie Dimon." | Their second Flow clip plays from "of" to "million" with its own captions; then plain cuts: the exchange floor on "loss", their money film on "into", banded cash on "billions", Dimon coming down the stairs with his arms open on "in profit". The coins picture and its moves are gone. |

## The type, word by word

Small words are Helvetica Bold (TeX Gyre Heros Bold) throughout. The big words:

| Treatment | Words |
|---|---|
| Upright Instrument Serif with its glow, as v13 had them (the user's list) | capitalism, BIGGER, Wall Street (the opening), JPMorgan Chase, "This is the most influential man in America right now", "He's basically the CEO", Biggest Bank, world, countries, World Bank, IMF, United States government, the pinboard ("He built Citigroup", "side by side with his mentor", "Sandy Weill", "for 16 years"), 42, fired, greatest, comeback, Wall Street (in "the history of"), broken bank, Chicago, Today |
| Slanted Instrument Serif (kept from v14 and v15) | bonus, Grudge, the Bezos frame (even met / Bezos / for a job at / Amazon), JP Morgan, standing |
| Bold Helvetica | guy, premise, dividend, loss, billions, profit, acquired, crisis, hit, only one, fell, every single day; the figures ($60 million, $10 trillion); the years (2000, 2004, 2008) |
| Their own design | FIRED, 1998, "by his own mentor" (difference), Golden Boy (gold), WORLD (difference), the picture card's words (upright serif, as the reference), the band's title (bold slanted Helvetica, as the reference) |

In the builder the serif is upright by default (`SERIF_ITALIC = False`); the slanted places say so themselves (the `si` caption style, `NAME_ITALIC`, `italic=True`). Every word arrives calmly, out of a soft blur, with no pop (v14). What the user asked for since v13 stays: both capitals in "Biggest Bank", "influential" in its line, no dark backing behind "United States government" or on the pinboard.

## The picture card (`kcardref`, S22)

Measured on every frame of the reference's 15.93-18.0 s (30 fps, frames 478-539):

- a hard cut to a flat off-white page (250, 250, 248);
- one 16:9 card, 1204 x 678, centred, an 18 px crimson edge down its right side, a soft warm shadow under it;
- it comes in 10.8 % large and settles: the excess shrinks by x0.895 a frame, which is GSAP's `expo.out` over 2.08 s. Nothing else moves;
- the words are Instrument Serif Regular, upright, 108 px, white, no tracking (the reference's "and banking operations" is 873 px wide: the same face at 107.6 px), on one centred line. A phrase is laid out whole and each word shows in its place on the voice; the next phrase replaces it at once. A word arrives blown out and is crisp three frames later; the key word arrives under a streak of light.

Here the picture is the same painting (it is the user's own treasury picture), the phrases are "with enough money" and "to buy the ones", and the streak is on "money". The card holds 1.6 s.

## The band (`krollup`, S20)

Read off the Hemant reel's frames 364-416 (24 fps) and a strip of the band's middle row against time: lit paper, a blurred grid of teal cards behind, scan lines over the frame; a band of 16:9 video cards on a cylinder seen from outside, close (the card at the bulge about 850 x 480); a bold slanted black title about 195 px standing on the band's top edge and bent round it; the band's speed falls evenly to nothing at the cut.

After the user's second note the band is:

- level and centred (no tilt), on a cylinder wide enough to run off both sides of the frame (20 slots, radius 2600, camera 1070 px away);
- bent inside each card (two half-planes a card), cards touching;
- slow: it is there from the first frame and glides 30 degrees to rest on a quadratic ease, 1475 px a second at first and nothing at the cut (the reel's soft phase runs 1150 to 480 px a second);
- keyed at 24 fps on a 3:2 cadence, with a faint sideways blur while it is quickest;
- titled "Every other bank" in TeX Gyre Heros Bold Italic 205 px with soft edges (0.9 px), "was dying" under the band, "and when" small on the paper above it.

The reel's small words are black on the band; these cards are dark, so "and when" stands on the paper instead.

## The second Flow clip (`tools/prep16.py flow2`)

Drive `1hclK-tOU74shZPHlevekEbGRXr6HmoRM`: 83 frames at 24 fps, three painted shots, its own captions burned in. The Gemini sparkle is painted out (OpenCV inpaint over the sparkle's own shape). The clip is retimed so each caption comes up on the narration's word: a smooth time map through seven anchors; the third shot runs at half pace with cross-faded frames. Its own sound is not used.

The voice says: of 61.16, his 61.32, own 61.50, money 61.72, into 62.04, the 62.28, stock 62.36, Turn 63.20, a 63.32, $500 63.54, million 64.04. On a sheet of the retimed clip (every third frame) each caption comes up within about a tenth of a second of its word, never after it by more than that.

## Also changed

- The Lehman sign now starts after the documentary's dissolve (it was half a face for its first frames).
- The 2008 film and the crash film are framed a little tighter in this section: a corner of a caption and the black side edges are out.
- Three caption groups that follow a light page (after the Flow clip, the band and the card) start on the cut, so their dark backing never shows on the page.

## Sources added (dimon-src, not in git)

- `_v16/flow2_ref.mp4`: the second Flow clip; `_v16/flow2_retimed.mp4` is made from it.
- `_drive/Sean Desmond - NAC Trailer v2.mp4`: the reference for the picture card.

## Checks

`hyperframes lint`: 0 errors, 29 warnings (23 on track density, the rest on file size, overlay count and the two narration tracks that meet at a join; none new in kind). `hyperframes check` on the final build: ok, 0 errors in lint, runtime, layout, contrast (11 of 11 samples pass) and audio. Every changed moment was looked at in stills before the render.

## Known limits

- Helvetica Neue is a commercial face; TeX Gyre Heros Bold and Bold Italic stand in. A licensed file can be swapped in through `SANS_FILE`.
- The band's cards are flat halves, not truly curved; at this size the bend reads as a curve.
- The money film is 736 px wide and is enlarged.
