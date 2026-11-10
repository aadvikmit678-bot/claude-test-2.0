# v11: the user's twelve notes on 0-28 s, and the pinboard with more video

`tools/build11.py` (from build10, written by the scratch patches p1-p5 of 10-11 Nov) writes `tools/media_v11.json`. Render: `renders/jpm-dimon-v11-0-40.mp4`, 0-40.12 s at 60 fps (`DIMON_PREVIEW=board`).

| # | Note | What v11 does |
|---|---|---|
| 1 | "Wall Street" white, not yellow | (v10) `sx@300`. |
| 2 | "This is the most influential man in America right now": at the bottom, all Instrument Serif glow, Dario's animation | The lines run along the bottom in Dario's serif, each replacing the last: "This is the most", INFLUENTIAL, "man in" AMERICA, "right now". Normal words use `dn`, heroes `dh`, and the words leave in the order they came. There is no Helvetica in the line. |
| 3 | Reduce the pause "right now" -> "He's" | 0.26 s of the 0.40 s silence is cut (vo.wav 3.03-3.29). |
| 4 | "He's basically the CEO" in serif glow, the CEO highlighted | "He's basically" and "the" in `dn`. CEO in `dhl`: 2 frames black in a glowing white bar, then blown out, then a halo that stays. |
| 5 | "of Wall Street": Helvetica, gap closed, yellow, more difference, better animated | `sp_wolf_lockup11`. The word gap drops from 0.24 to 0.14 of the size. Each word rises into place out of a blur and a tall stretch (4 frames), and its own box goes negative for 2 frames. STREET's landing inverts the whole frame for 1 frame, and the lockup creeps in 4 %. The purple negative still ends it. |
| 6 | FIRED should animate with the square | FIRED sits in the card's own frame, so it grows, pops and settles with the square, ending at the same place and size as before. |
| 7 | "by his own mentor": Helvetica bold, centred, a different difference effect | `sp_diff_line`: Inter Tight 800, 150 px, centred, drawn in difference, so every letter is the negative of Weill's face under it. A blurred dark halo keeps it readable on mid-grey. Each word is first a difference block for 1 frame, then settles from 112 %. |
| 8 | "bonus" like "Dario Amodei" enters the Dario video | `sp_name_pop`: the word pops in whole with a white top-left square (1 frame) and a bottom-right square (2 frames). For 2 frames its row is a negative band with the word black, then it holds in the glow. |
| 9 | "Grudge" capital G | (v10) |
| 10 | Remove the pause after "Grudge" | 0.28 s of the 0.37 s silence is cut (vo.wav 11.53-11.81). |
| 11 | No money symbol over the IMF | (v10) |
| 12 | "United States government" typed like JPMorgan Chase, centred | `sp_type_word` (Dario's DISAPPEAR) at the centre of the Capitol. Each word types letter by letter across its own spoken span, with the newest letter flaring, over a soft dark band. Dario's tiles take it out on the frame before "Meet". |

Later message ("in the frames part, use videos more ... flashes and the glow effect"), done in `kboard11`, the pinboard:
- every card cuts between moving clips on the words: Dimon at the citi wall, then the two side by side (MPB 716), then the press scrum (MPB 852); Weill at the lectern, then the two of them (MPB 868);
- a white flash on every cut inside a card, and on each whip;
- a glow blooms behind each card as it lands;
- "Sandy Weill / for 16 years" is in the serif glow, blooming in.

## Timing

`VO_CUTS` lists the two cut spans in vo.wav time. `vo_gone()` retimes every narration word, and `RT()` retimes the hand-placed times written for v10. The first part of the narration plays as three audio pieces, each joint in silence. Everything after a cut comes that much sooner: the quote at 22.29 s, Meet Jamie Dimon at 27.57 s, the pinboard to 40.12 s, the film 85.56 s.

## The Dario reel's Instrument Serif (Copy of dario vidoe.mp4, 25 fps, read frame by frame)

**Normal words.** Examples: "The last time" 30.0, "world was warned" 30.5, "He built the" 34.6, "every AI tech bro wants to save humanity" 17.5-19.3.
- Small serif, cap about 62 px, on one line just below the frame's centre.
- Wide spacing; each word lands in its final place.
- A glowing white square marks the next word's place for 1-2 frames (the user's "glow square ... coming very fast").
- The word arrives stretched tall (about 1.4x) and settles in 1-2 frames.
- On light footage the words are black.
- Words leave in the order they came.
- White blocks also sweep over words as they are spoken ("The last time").

**Hero words.** Examples: "AI" 9.60, "Atomic" 35.08, "Bomb" 35.32.
- Big and condensed, with a strong glow.
- Blown out for one frame, then crisp.
- They clear the small words. Small serif words can flank a hero on its row ("cold AI war").

**Name entrance.** "Dario Amodei", 10.52-11.44:
1. A white glowing band wipes the last line.
2. Cut. "Dario" pops in whole with a white top-left square.
3. A bottom-right square for 2 frames.
4. 2 frames of a negative band across the name's row: the shot inverted (navy to cream, skin to cyan), the word black.
5. Both words hold, then leave in order.

**Glitch heroes.** "1945" 32.24 and "Oppenheimer" 33.44:
- Horizontal slices with an RGB split for about 5 frames, then crisp.
- Short glitches during the hold.
- A difference box near the exit.

**Typed word.** "DISAPPEAR" 36.6: a letter every 2 frames, the newest letter flaring (`sp_type_word`, since v5).
