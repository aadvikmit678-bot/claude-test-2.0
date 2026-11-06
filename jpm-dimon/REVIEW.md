# Jamie Dimon / JPMorgan Chase — review (v3)

The user's notes on v2:
- "keep the background music of the first Bloomberg clip, continuing for the whole video";
- "sloppy changes";
- "better footage, more photos";
- "edit it exactly like the reference";
- "rebuild it".

v3 is `tools/build3.py`, with media from `tools/prep2.py --spec=media_v3.json` and audio from `tools/make_music.py`.

## Sound
- **Music:** the Bloomberg open's own music is lifted out with Demucs (htdemucs, two stems).
  - It is the opening cue: 120 BPM, about 53 s, ending on a held hit.
  - The bed plays the cue from 2.17 s with one jump on a downbeat (cue 45.085 → 3.215, 80 ms equal-power crossfade),
    so the cue's own ending lands on the last frame (93.2 s).
  - The jump was picked by comparing the spectra of the bars on both sides of every downbeat pair. No click was
    measured at the junction (largest sample step 0.0027, against 0.0117 typical).
- **News open:** the reporter's voice alone (the vocal stem), spliced like the picture, so the music is not doubled.
- **Levels:** voice −16 LUFS, bed −30 LUFS (about 14 dB under the voice, as in the Bloomberg mix).
- **Not heard:** the levels were measured, not listened to.

## Picture changes from v2
- **No blurred-fill vertical strips:** the vertical clips (biggest tower, chess, money porthole) are either replaced or
  framed as a panel on black.
- **Every clip sits inside one source shot.** `tools/check_shots.py` scans each clip's source range for scene cuts, so
  no clip flashes a frame of the wrong shot (13 fixed).
- **Stronger, more literal footage:**
  - "He's": the 270 Park podium, arm raised.
  - "CEO": in his office.
  - "of": under the press lights.
  - "now": the ribbon.
  - "runs": on stage over the hard hats.
  - "bank": JPMORGAN CHASE & CO. on the glass.
  - "world": Manhattan from straight above.
  - "than / JP / Morgan": the blue CHASE signs, the stone lettering, the etched glass door.
  - "the floor at work" on "day".
- **More photographs:**
  - The seal ring now cycles 18 portraits (image pack, Pinterest, interview stills).
  - "30 Countries" is his real meetings (Reeves, Kishida with Blair, Macri, Davos), flipping on paper, then a pull-back
    to a scattered wall of 12 photo cards.
  - "Bank": the World Bank logo printed on a card.
  - "Chicago": the Bank One / Chase Tower.
  - "own money": his hundreds, with a punch-in.
- **New set pieces:**
  - "18 months of no job": a flip calendar from NOV 1998 to MAR 2000, beside the line.
  - "acquired by JP Morgan": the BANK ONE and J.P.Morgan cards slide together into the JPMORGAN CHASE & CO. card on
    "Morgan".
  - "the ones that fell": the Lehman and WaMu cards and a 2008 photo land on paper, then drop off the page.
  - The 2004 roller has its own cards (the merger handshake, the Fox report).
- **Kept from v2:**
  - BIG word mask, seal ring and punch-in, Wolf face boxes, name card, NYT marker sweep, the side-by-side split.
  - Bar write-on, the palm strike, boxing strobe, Amazon behind Bezos, the archival wall.
  - Typed 2000 and Today, glitch on "broken", slice on "dividend", the clean wipe, the counters.
  - The AMD data page, year rollers, the screen wall, the JPMorganChase light sweep, the Pattinson caption engine.

## Measured
- `check` (5 samples, contrast pass off): **ok**. The full 9-sample run stalls in the checker's overlap pass on a film
  this dense.
- **Warnings kept on purpose:**
  - `line_unread` on roller years, calendar pages and counter steps. They flick past by design, as in the
    references.
  - `text_below_floor` on the decorative "person 0.97" HUD tags.
- **Looked at:** every changed beat, plus about 60 frames.

## Open
- Weakest beat: "We bank countries" (a talking shot under the line).
