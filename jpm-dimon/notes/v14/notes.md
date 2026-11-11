# v14: the notes on the v13 render (0-36 s) and the new type

`tools/build14.py` (from build13) writes `tools/media_v14.json`. The film is 85.62 s (0.47 s longer: the hold after "Meet Jamie Dimon"). **Not rendered yet**: the user is sending more changes first.

Rebuild: as v13, with `python3 -I tools/prep14.py` first (the grudge cut-out, the font, the new portrait stills) and `build14.py` in place of `build13.py`.

## Type

- **Sans:** the user asked for Helvetica Neue Bold. It is a commercial face and is not on this machine, so the film uses TeX Gyre Heros Bold, the open-licence Helvetica Bold (their sample's sans matches it letter for letter). One weight, Bold, everywhere. To use a licensed Helvetica Neue Bold: put the file in `assets/fonts` and name it in `SANS_FILE`.
- **Emphasis:** the font in their sample is Instrument Serif Italic, set tight. Emphasis words inside a Helvetica line are now in it (`SERIF_ITALIC = True`; `False` gives the upright again).
- **One entrance:** every emphasis word arrives the way the Helvetica words do, out of a soft blur into its glow. No scale, no pop.
- The three typed title words ("JPMorgan Chase", "United States government", "Today") stay upright, as approved.

## The notes

| Note | What v14 does |
|---|---|
| "influential" comes in pop-pop style | Two rows along the bottom, Helvetica Bold with "influential" and "America" in the slanted serif; every word arrives the same way. |
| No zoom transition after FIRED; cut directly to 1998 | The hero photo lands with the word FIRED, on "fired"; the page holds still for the word and the film cuts straight to the 1998 shot on "in 1998". The narration runs "fired in 1998" without a breath, so nothing was cut from it. |
| "By his own mentor" below | The line sits under the faces (y 898), not across them. |
| The mask in "and a family grudge" | The cut-out is made again (`prep14.py grudge`): one outline traced along Weill's own head and shoulder instead of four rough polygons, the hedge keyed out of his hair's edge, no white outline (a faint glow only). |
| "Biggest Bank", both capitals | Done. |
| No black shadow behind "United States government" | The dark band is gone; the letters carry a white glow only. Where the line crosses the white dome it is fainter. |
| Two more colour, current portraits after the 0:28 one, then the jail photo; "Meet Jamie Dimon" a split second longer | 28 frames of 60 are added to the narration's own silence after "Dimon," (`MEET_HOLD`). The name run is seven portraits; the two new ones are `h9_a08` (his office) and `h9_a17` (against the dark). The reel's blur-in and whip moved to the new last one. |
| "Golden Boy" in glowing gold, entering like "Joker" | Gold with a gold glow. The entrance was already the reel's (the word flies in from the left as a blur and resolves). |
| The second Wall Street picture zooms at 0:30 | Still now. |
| WORLD in the difference effect | WORLD is drawn in difference, as "by his own mentor" is. The planet film is graded darker and harder so the word stays bright. |
| Black shadows on "He built Citigroup" | No dark backing anywhere on the pinboard. The first frame and card are now the Stanford interview (a dark picture), so the white words read with their glow alone; v13's bright window shot needed the backing. Card words are Helvetica Bold with the emphasis word in the serif. |

## Checks

`lint`: 0 errors. `check`: ok, 0 errors (contrast 12 of 12). About 50 stills looked at across every changed moment. No render.

## Open

- The exact Helvetica Neue Bold needs the user's licensed font file.
- "United States government" is harder to read over the dome without the band.
- Google Flow MCP cannot be connected to a cloud session (it drives a Chrome window on the user's own computer).
