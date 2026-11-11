# v17: the notes on the v16 render

`tools/build17.py` (from build16) writes `tools/media_v17.json`. The film is 85.16 s at 60 fps (28 frames shorter than v16: the hold after "Dimon" is gone).

Rebuild (after the v14-v16 prep steps in `notes/v16/notes.md`):

```bash
export DIMON_ROOT=<repo root> CV4_DIR=<repo root>/dimon-work/cv4
python3 -I tools/prep17.py meet                    # the blur-in frame and whip smears of h9_a04
python3 -I -X utf8 tools/build17.py --specs        # writes tools/media_v17.json
python3 -I tools/prep2.py --spec=media_v17.json    # cuts the clips
python3 -I -X utf8 tools/build17.py                # writes index.html and compositions/
npx --yes hyperframes@0.9.2 render --fps 60 --workers 2 -o renders/jpm-dimon-v17.mp4
```

## The notes and what v17 does

| Note | What v17 does |
|---|---|
| "Where is the animation that we do, like the Dario video, for influential and America? It's coming straight … that comes with a flash kind of thing." | "influential" and "America" are Dario's hero words again (condensed upright serif), with the flash entrance. |
| "You have removed animation from everywhere … Biggest Bank: where is the animation that was in v13 and v14 … world … countries … World Bank … the IMF is also the same case … it's coming like a plain." | The calm fade v14 gave every serif word is gone. Every serif word arrives as v13 had it: whole on its frame, blown out in a big white bloom and a little large, then crisp in its glow four frames later. |
| "The bonus word I want in normal Instrument Serif glow … straight. Grudge can be in italics." | "bonus" is upright and condensed again, with Dario's name entrance (the corner squares and the negative band). "Grudge" stays slanted. |
| "Broken Bank, both B capital." | "Broken Bank". |
| "$60 million can remain in Helvetica Bold, but it can come better with the flash effect." | The big bold Helvetica words and figures ($60 million, $10 trillion, dividend, loss, acquired, crisis and the rest) get the same flash, in the Helvetica's own glow. |
| "billions and profit can be the original Instrument Serif." | "billions" and "profit" are in the upright serif with the flash. |
| "Wherever the year comes, the same kind of animation as 1998 … the square flash that comes up with 1998 after 1998 has fully appeared." | 2000, 2004 and 2008 flash in; then, as 1998 does, the first two digits turn black in a white box: on, off, on, off (frames 6, 8, 10 and 11 after the year). The box fits the digits, so the small word above stays clear. |
| "Keep Jamie Dimon's pics till here [the portrait in a suit] … After this pic, the audio should come directly to 'the Golden Boy of Wall Street', switching directly to the cell picture … the colored pics are removed … We keep black-and-white pictures." | The name run is the four black-and-white portraits. The 28 frames v14 added after "Dimon" are gone, so the narration runs as recorded into "the Golden Boy". The reel's lift, blur-in and whip are on the last portrait now (`tools/prep17.py meet`). |
| "When we say 'the guy' there is one frame … I want to change this picture." | The frowning picture in front of the Capitol is out; the two front-on colour portraits from the name run take its place in "the guy" run. |
| "Bezos's picture is coming a bit off … his cutout can come in a bit lower, at a bit of a low frame rate, with a flash of him masked." | Read again off the Dario reel (frames 1184-1187): the head sits low, its collar's point on the frame's bottom edge, and the burst is inside the figure. Bezos's head comes up from the bottom edge in three steps at 12.5 fps; then the whole figure, the white flash masked to his shape for one reel frame and half as bright the next. The shot starts 0.12 s sooner, so the words keep their times. |

## Checks

`hyperframes lint`: 0 errors. `hyperframes check`: ok, 0 errors in lint, runtime, layout, contrast (14 of 14 samples pass) and audio. Every changed moment was looked at in stills before the render.
