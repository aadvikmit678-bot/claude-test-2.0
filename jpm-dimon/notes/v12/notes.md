# v12: the whole film; the last 45 s rebuilt

`tools/build12.py` (from build11) writes `tools/media_v12.json`. The film is 85.16 s at 60 fps. The cleaned tower film is `dimon-src/_v12/jphoriz_clean.mp4` (prep2 key `JPH2`).

Rebuild: `python3 -I -X utf8 tools/build12.py --specs`, `python3 -I tools/prep2.py --spec=media_v12.json`, `python3 -I -X utf8 tools/build12.py`, then `npx --yes hyperframes@0.9.2 render --fps 60 --workers 2`. To re-render a short stretch, build with `DIMON_ONLY=<scene ids>` and use `render --start/--end`; `REVIEW.md` says how the patches were spliced in.

## The user's notes on the v11 render (11 Nov)

| Note | What v12 does |
|---|---|
| "Why is the text bouncing?" | The small serif words (`dn`) no longer arrive stretched. They come in dim and soft for one frame, then full. |
| The pause after "the CEO of Wall Street" (14-15 s) | A third cut in the narration: 0.40 s of the 0.55 s silence after "Street." (vo.wav 5.60-6.00). |
| The pause after FIRED; "it should be a transition" | The photos keep changing through the word "fired" (three frames a photo, the hero landing 0.3 s after the word). The page keeps pushing in after the hero lands and runs on for 0.3 s under the 1998 counter, whose ground fades in over it. |
| The skeleton is missing on "Golden Boy" | The X-ray flickers in once, then holds under "Golden Boy" for about 0.35 s (it was 2 frames). |
| "guy" in a cursive font | Upright Instrument Serif. The film uses two families only, with no italic. |
| The small NEW YORK pop-up | Removed. |
| Pinboard: "Citigroup" comes late; words in the middle in serif glow on the other two frames too | Each card carries its words in its middle in the serif glow, on the voice: "He built Citigroup", "side by side" then "with his mentor", "Sandy Weill" then "for 16 years". The black stack is gone. |
| "at 42": no newspaper panning | Video: him on the news screen (MPB 1047.2). |
| "billions in profit": change the B-roll | "into": cash thrown off the yacht (the user's Wolf of Wall Street edit). "billions": the line climbing (their new B-roll). "in profit": him with his thumb up at the new headquarters. No money rain anywhere. |
| "he was fired": keep the soul-out push | Unchanged (FIRED from its 55th second, the flash and the negative). |
| "in the history of Wall Street": the vertical rectangles with the glow | `kstrips`, from the Hemant reel's 25.10-26.95 s; see below. |

## The last 45 s (S10-S23)

Rebuilt from the three references the user named:
- **Madoff:** full-frame moving footage under small glowing words; hero type moments.
- **Karp:** one clip a phrase, cut on the word, the clip showing what the words say. Plain cuts between B-rolls.
- **Heath:** a ten-frames-a-shot run for "financial crisis", single black frames, the click cam.

Gone:
- the frames on a vignette, the 3x3 grids with inverted cells and the tilted cards;
- the black beats under speech and the split-frame "cuts";
- the yellow type, the logo cards and the "cut cut" panels.

Typography: the Dario format everywhere, through `dz`.
- A row of small serif words, then the hero in their place.
- Words spoken within 0.3 s of the hero share its row.
- The hero holds 3 frames past the cut, so the type carries into the next shot.
- Years glitch in like Dario's "1945" (`dg`).
- Helvetica stays in the designed moments: BIG, OF WALL STREET, the FIRED page, "by his own mentor", "and a family", the Meet scene.

| Line | Picture |
|---|---|
| But then, at 42, he was fired | Him years later; him on the news screen; the push scene. |
| 18 months of no job | One room at night: he sits by the lamp, then lies down. No black. |
| He took up boxing | His fists, with two jabs of the click cam. |
| read biographies | The Snowball; Buffett reading (the user's new B-roll); The House of Morgan. |
| even met Bezos for a job at Amazon | Him telling it at the Economic Club. Bezos appears once, his whole face, the word under it: the Drive has no Bezos footage. |
| a premise for the greatest comeback | Him in the dark; under the lights; back at the lectern ("comeback" highlighted). |
| in the history of Wall Street | Seven vertical strips of archive footage. Each arrives in a white glow, left to right, with the line across the middle. They leave strip by strip over Bank One's columns, the next scene's first shot. |
| In 2000 ... a broken bank in Chicago | Bank One's columns; its door, with two negative frames on "broken"; the city from the air. |
| cuts the dividend, cleaned it up | His hands cutting the air (click cam, one black frame); the floor at work. |
| $60 million of his own money into the stock | Him; hands counting dollars; him; the floor. |
| a $500 million loss into billions in profit | The traders; the falling line; cash thrown off the yacht; the line climbing; his thumb up. |
| acquired by JP Morgan in 2004 | The announcement; the flag; the sign; the facade. |
| Then, 2008 financial crisis hit | The exchange's sign; the board at -605; a five-shot run; "Worst not over?". |
| every other bank was dying | A bank's sign coming down; Lehman; Bear Stearns; "Bank owned". |
| the only one standing | Him; then a man standing at the window over the city. |
| enough money to buy the ones that fell | Bills through the counter; the fire-sale bulletin; Bear Stearns' door; Lehman's tower dropping in. |
| That's JP Morgan and Chase ... $10 trillion every single day today | The board with the name; the tower's crown from above; its silhouette at sunset with four rectangle cutouts popping in (the flag, the board, the tower by day, the sign); the skyline at dusk; six black-and-white shots at about nine frames each; the lit tower at night, pushing in; fade out. |

## The four files the user added on 11 Nov

| File | Use |
|---|---|
| Wolf of Wall Street edit (Drive 1wOgl-sJhpxgPCDGcQMdC6oTYkcg8YTKl, prep2 key `WOLFE`) | One shot: cash thrown off the yacht, under "into" (6.83 s). |
| Finance B-roll montage (Drive 1-JyhS9eqBswYLP5R0ryLMbYBqW7oWbOw, `BR2`) | Buffett reading (10.83 s) under "biographies"; the climbing line (14.6 s) under "billions". |
| New York building montage (Drive 1JNNG-IImrD6nIxIABlkw0wCDjreGb9i3) | Its device from the 15th second, rectangle cutouts popping over a skyline, is rebuilt with JPMorgan pictures over the tower at sunset. Its own shots are not used: they carry burned-in titles of other buildings. |
| Black-and-white fast finance edit (Drive 1dabjjUbyQzl4UGFD4us7rL9AVa2JLDSt, `FINF`, vertical) | "every single day": six shots at about nine frames each (the Wall St sign, the pit, the bull, the boards, the round floor, the chart). Its cars, jet and the exchange-floor shot with a garbled sign are left out. |

Both montage files are cut every 0.2-0.3 s. Shot starts were read by exact seeking (contact sheets made with the `fps` filter mislabel them by up to 0.17 s).

## Higgsfield

The user offered one generated scene. The connected account is on the free plan with 0 credits, and the request was refused ("Requires plus plan or higher"; a 5 s clip is 35 credits). Nothing was generated. The scene prepared for it is the heavy bag for "He took up boxing":

```
Cinematic 35mm film shot inside a dim old boxing gym at night. One hard shaft of warm light cuts through dust in the air. A middle-aged businessman in a white dress shirt with rolled sleeves and white hand wraps, seen from behind and slightly to the side so his face is never visible, throws fast heavy punches at a worn leather heavy bag. The bag swings and chalk dust bursts on every hit. Handheld camera close to his shoulder, shallow depth of field, high contrast, desaturated teal and amber grade, natural motion blur. No text, no logos, no boxing gloves.
```

## Sources checked and left out

- `jp morgan edit use clips in the last fast paced.mp4`: its clips sit in a 405-line band of a vertical frame, with captions.
- The vertical videos (tower "aura", ribbon cutting, NYSE bell, Wall Street short): they cannot fill a 16:9 frame.
- `p01` in the pinterest folder: named "2008 crash", it is a fashion edit.
