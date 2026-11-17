# Type — the Sequoia and Tesla reels, measured frame by frame, and where each move went

The user asked for the type of two reels: **Sequoia** ("$1 billion bet", https://www.instagram.com/reel/DfRrJC9z5mi/)
and **Tesla Roadster** (https://www.instagram.com/reel/DezFTyktEUp/). They wanted our Inter kept but animated faster,
not the same entrance everywhere, Instrument Serif as the second face, the emphasis words big ("on the whole screen"),
some words behind people (cut-outs), and five named moves: the "Instinct" flicker, "Gmail" typed in a box, the giant
word behind Leo with glow and a little blur, "text a phone number", "Books flights". Then: **white type only** (the
user), except the black words on reference 7's light cards (the user's choice).

## What the reels do (Sequoia at 30 fps, sizes scaled x1.505 to 1080p)

| Move | Measured |
| --- | --- |
| Base words | Full brightness on the frame they land (no fade); line ~49 px of 718 tall (font ~79 px at 1080p), centred, wide gaps ~1.35 em; each word appears in place |
| "Instinct." | w 1118 px (58% of the width), cap ~233 px (font ~320 px); on f325-327, **off f328-332**, on f333-344, same place |
| "$1" | w 373, h 352 (font ~420 px); held 12 frames while the footage cuts under it |
| "billion" | w 1056, h 296 (font ~395 px), f53-59, then the small "$1 billion" summary at f60 (h 65) |
| "flights." | ~92% of the width (font ~430 px), behind the plane's wing; "It books" small above right (y ~25%); a 3-frame negative flash f215-217 |
| "G-mail" | letters typed at f393/395/398/403 (font ~400 px); a black full frame, then the box zooms out onto white (to scale ~0.62), its edges blurred early |
| "bet" | giant behind Leo, held 13 frames; 2 thermal glitch frames, then a box reveal |
| Serif lines | small words in directly; the big word ~2x, blurred for 2 frames ("founder," f653-654); out: a 3-frame smear to the right (f660-662) |
| "You text a / phone number." | bold sans line over a serif italic line, right of the subject, navy with a white halo, words in directly |
| "revoked access.", "got called useless." | behind the heads |

**Tesla**: a small regular sans, wide spacing, words pop; **single words replace each other** ("is / something / that /
you're"); "Last" in big for 2 frames then snapped small; "start" big; serif capitals "THE MONEY." framing a face; box
wipes; highlight boxes.

## Ours (`tools/build4.py`), after the user's notes on the first type render

- **Normal captions: v2's, as before the type change** (the user: "bring back that text font animation that we had
  throughout the video"): Inter variable 76 px, weight 540, v2's glow and v2's entrances (`pop`, `bloom`, `scale`,
  `streak`, `soft`), the same line breaks -- including reference 7's "GTA VI took 13 years to make." / "And yet, nobody
  seems to have moved on.", "It was about what it really gave you." and "cars and guns." (back as one line, no giant
  words). The faster entrances (`fcut`, `fpop`, `fbloom`, `fstreak`) stay only where the user liked them: "sitting in
  front of the family computer," and the single words.
- **Instrument Serif as in the Dario video** (the Dimon edit's recipe, `dario_js`): a glowing white square marks each
  small word's place for two frames, the word comes in dim and soft for a frame, then sits in its glow; the big word
  comes in blown out and settles crisp over four frames; the words leave in the order they came, a frame apart. White
  glow only, no dark shadow, and no commas or full stops on these lines (the user: "For a kid" and "started"):
  "For a **kid**", "it wasn't just a **game**", "It was a psychological ***escape***" (a soft dark oval behind it,
  the Dimon edit's scrim, because white on its white clouds can't read), "an alternate ***reality***", "And somewhere
  along the way" / "those kids ***grew up***", "Rockstar takes you back to" (centred, just under the Vice City logo,
  which fills the middle), "the city where it all **started**", "Drive ***slow***" (a gentler, longer entrance),
  "never really ***left***", and "Because **GTA**" (GTA alone in serif, blown out then crisp).
- **"But GTA lets you be"**: the Palmer Luckey reel's "John Wick" serif -- each word in blurred, sharp four frames
  later -- then BE THE PROBLEM behind the bad guys is the rest of the line (no caption repeats it).
- **Giant words** (Inter Display ExtraBold, white, wide glow), never repeated in a small line: "**billion dollars**" on
  one line; "**millions**" | "of adults"; "**Ah shit**" behind CJ (cut out, `assets/clips/cj_fg.webm`), then "here we
  go again." a size up; "**gunshots.**" behind Tommy and Lance with the Instinct flicker and the muzzle flash; "**bad
  guy**" behind Lucia; "**Today,**"; "**13 years**" behind the man in the suit.
- **Reference 7** (the Tesla Roadster reel): "GTA" | logo | "VI" already in place on the zoom, one dim frame, then
  "took 13 years to make." spread across the frame in difference blend (white over the light card reads dark), "moved
  on." heavy for two frames and then set, as the reel's "misunderstanding.".
- **Single words** (Tesla), each replacing the last, all in directly: "with / the / volume / turned / all / the / way /
  down". **The slow part** (the user): "don't / rush" each rise in softly (0.34 s, from a 6 px blur), "Take the long
  way" / "*home*" centred, each word rising in softly and "home" as the slow serif big word.
- **Typed box**: "**Los Santos**" (the "G-mail" move).
- **Gone** (the user): the giant "cars" and the giant "guns." behind the man with the shotgun ("cars and guns." is v2's
  line again); the "ASPIRINE and PANZER" caption under the notebook (the page shows the words); the commas after
  supercars / guns / planes.
- **The hook** (the user's final): "A video game / so popular / it could cost" as before, centred, now over the user's
  GTA VI montage, with the escape line's soft dark oval behind each line (lighter, 0.32) so the white reads on the beach.
- **White only**: the "19th" highlight is white on a dark card, and the date card's date is white (`datewhite` in
  `tools/prep.py`). The only dark type is on reference 7's light cards, as the user chose. Logos keep their colours.
