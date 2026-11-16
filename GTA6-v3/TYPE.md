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

## Ours (`tools/build4.py`)

- **Base line**: Inter variable 76 px, weight 540, v2's glow; every word lands in 1-3 frames. Small words ("a", "the",
  "it", ...) come in directly (`cut`: one over-bright frame); the others rotate `pop` (0.05 s), `bloom` (0.08 s),
  `cut`, `streak` (0.06 s), so no two neighbours move the same way.
- **Serif lines** (Instrument Serif, 86 px): small words in directly, the big word 2.05x blurred-in over 0.07 s, the
  line smeared out to the right over its last 0.1 s -- "For a **kid,**", "it wasn't just a **game.**", "It was a
  psychological ***escape,***", "an alternate ***reality.***", "the city where it all **started.**", "Drive ***slow.***",
  "never really ***left.***".
- **Giant words** (Inter Display ExtraBold, fitted to the width, white with a wide glow): land blurred and over-bright,
  sharp 2-3 frames later -- "**billion**" (then the small "a billion dollars"), "**millions**" (then "millions of
  adults"), "**cars**", "**Today,**".
- **Behind people** (the subject cut out with `hyperframes remove-background`, `assets/clips/<id>_fg.webm`, laid over
  the giant word): "**guns.**" behind the man with the shotgun, "**gunshots.**" behind Tommy and Lance -- with the
  Instinct flicker (gone frames 3-7) and a white muzzle flash in the gap --, "**bad guy**" behind Lucia, "**13
  years**" behind the man in the suit.
- **Single words** (Tesla): "with / the / volume / turned / all / the / way / **down**", each replacing the last on its
  own syllable; "down" and "rush." in big for 2 frames, then snapped down (Tesla's "Last"); "don't".
- **Typed box** ("G-mail"): "**Los Santos**" typed letter by letter in a black box that is the whole frame for two
  frames, then zooms out (blurred at first) to a card on white.
- **Two-line block** ("You text a / phone number."): "Take the long way" bold over "*home.*" in serif italic, set in the
  shot's open sky -- white with our glow (the reel's is navy; the user wants white type only).
- **White only**: the "19th" highlight is white on a dark card (was black on a white card), and the date card's pink
  date is white (`datewhite` in `tools/prep.py` unmixes its magenta drop shadow out). The only dark type left is on
  reference 7's light cards ("GTA VI", "took 13 years to make.", "And yet, nobody seems to have", "moved on."), as the
  user chose. Logos (GTA VI, Vice City) keep their colours.
