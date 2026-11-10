# v10: the Meet Jamie Dimon scene (S07) and the pinboard (S09)

Built by the user's other session (10 Nov, night) and rebuilt here from its pasted code, applied to `tools/build9.py` in the same order:
- patch A (S07);
- the three quick notes and the map shade;
- the `meet` preview cut;
- patch B (S09) and its three tweaks.

Builder: `tools/build10.py` writes `tools/media_v10.json`. The new stills come from `tools/prep10.py`.

The rebuild matches the other session's render (`jpm-dimon-v10-0-40.mp4`, Drive 1rl-apsyGihPkC4tNvlfPiLcZNTbccufD). Sampled frames differ by 1-3/255 on average, plus one-frame offsets at word boundaries and on the whips.

Rebuild:
```
cd jpm-dimon && export DIMON_ROOT=<repo> CV4_DIR=<repo>/dimon-work/cv4
python3 -I tools/prep10.py                     # needs dimon-src/_heath/h18-h22_front*.png, h_xray2.png, h_map_usa.png, h_desk.png
python3 -I -X utf8 tools/build10.py --specs && python3 -I tools/prep2.py --spec=media_v10.json
DIMON_PREVIEW=board python3 -I -X utf8 tools/build10.py   # 0-40.65 s; without the variable, the whole film
```

## Round 1: S07 with the Heath reel's own typography (28.10-35.73 s, 60 fps frames from 28.10)

| Frames | Voice | Picture | Words |
|---|---|---|---|
| 0-71 | Meet Jamie Dimon | Five front portraits, youngest to today; the second is the user's new front-on college photo (h9_a22). | The name flanks the face on the centre row: "Jamie" ends at x 473, "Dimon" starts at x 1401. "Dimon" is a white bar, then sits in a white box for 2 frames. |
| 71-75 | | The vertical whip. | The words smear with it. |
| 75-130 | the golden boy | The cell picture; black, the top negative box, black; the X-ray is the user's "jamie skeleton 2.0"; the silhouette. | "Golden Boy" in the reel's red (its "Joker"). |
| 130-196 | of Wall Street | The Wall St sign, the focus window, the street. | A white bar under the sign becomes "of Wall Street"; black inside the window; the line leaves as one bar. |
| 196-217 | the guy | Three new front portraits. | "the", and "guy" in serif italic under it. |
| 217-322 | everyone said was next in line to run | The user's Wall Street montage ("wall street videos montge edits"), its 3.0-4.75 s. | "everyone ... said ... was" along one row; "next in line", "to run" centred under the figure. |
| 322-402 | the biggest financial company | The user's desk picture ("montage jamie", h10_desk*): a gold line drawing (4 frames), the picture on a slow push, a defocus, black-and-white. | "the / biggest" left, "financial / company" right. |
| 402-409 | | Black, six grey box flashes, black. | |
| 410-452 | in the world | The user's map of America as the reel's map pan. | "in the WORLD" centred, a "NEW YORK" label over "WORLD"; the line becomes one bar. |
| 452-458 | | Strobe: white, white, black, black, white, white. | |

Also in round 1:
- "Wall Street" white at "bigger on Wall Street";
- capital-G "Grudge";
- no money over the IMF.

## Round 2: S09 as the Karp reel's pinboard (35.74-40.65 s)

"He built Citigroup side-by-side with his mentor Sandy Weill for 16 years.", on the Karp reel's pinboard from its 15th second (instagram Dfc3GMjxrP5), with video in every card and the user's blue grid as the board (drawn in CSS).

| Moment | What happens |
|---|---|
| "He built" | Weill and Dimon under the citi sign (MPB 1001.6), full frame. |
| "Citigroup" | The shot blows out white (posterize) and shrinks into a white-edged card. |
| First whip | The camera whips right (expo out, blurred while fast) to a tilted card under a red pushpin: Dimon at the citi wall (MPB 927.0). Bold black words stack beside it. |
| Second whip | The camera whips down to Weill at the lectern (MPB 727.3). "Sandy Weill", then "for 16 years", appear on the card. |
| Out | One negative frame, then black. |

Partial renders: `render --end` fails on this project (PLAN_TOO_LARGE: 2.6 GB of media against a 2 GB cap), so build a preview cut. `DIMON_PREVIEW=meet` ends the film after S07, and `DIMON_PREVIEW=board` ends it after S09.
