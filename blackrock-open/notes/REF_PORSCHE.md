# Reel DdazhmWsDem ("Porsche … the intelligence behind it, increasingly Indian")

The user wants this reel's look for the rest of the BlackRock film, from "Back in the 1980s" to the end:
- its captions (the font, and how smoothly the words come in);
- how its clips are framed and cut;
- its texture.

**The file:** 1916×1078 at 60 fps, 58.7 s. The footage underneath runs at 15–40 distinct frames per second.

**How it was measured:**
- every frame of "And here's crazy part." (27.3–28.8 s), word by word: brightness, sharpness and centroid;
- 20 fps strips of "crazy part.", "4,500 people", "€1.25B." and "On August 24th,";
- full-resolution crops of ten captions;
- the voice aligned word by word with wav2vec2 (`tools/align.py`).

## The small captions

**Font:** Instrument Serif *Italic*, white, sentence case. The full stop, comma and "?" stay on screen.

**Size:**

| Kind of line | Size (1080p) | Example |
|---|---|---|
| Most lines | 92–108 px; x-height about 48 px, cap height about 75 px | "And here's crazy part.", "Porsche can't win the" |
| Long lines | about 70 px | "The intelligence behind it?" |
| A single key word | about 170 px | "called" |

**Spacing:** words are set far apart, about 0.6 em from word to word (normal is about 0.25 em). A 3–4-word line spans 45–60 % of the frame width.

**Position:**
- The line sits centred, a little above or on the middle (y 0.45–0.52).
- When a subject fills the middle (the MRI head), the phrase splits into two tight groups, one left and one right of it ("So they" … "sold their", "for" … "€320M,").

**Glow:**
- A soft white halo: a tight one of about 6 px plus a wide faint one of 30–40 px.
- Over black, a dim grey radial pool sits behind the line, like the light of the words.
- Over bright pictures the same halo still reads, because the white words are lifted by a faint dark shadow.

**Layout:** the whole phrase is laid out, centred, before it starts. Each word then fades in *in its own place*; nothing re-centres or slides.

**Entrance (measured):** each word goes from 0 to full white in 0.25–0.33 s.
- It starts soft, with a blur of about 4–6 px at 1080p, and is sharp by the end. Its sharpness rises with its brightness: 27 → 81 → 96 → 99.
- There is no movement or scale: the centroid stays within 1–2 px.
- In this reel the caption layer updates at about 12 fps (5-frame steps). We keep it at 60 fps, which is smoother.

**Timing:**
- A word starts on its spoken onset, from up to 0.15 s before to 0 s.
- On fast phrases the last word can lead its sound by up to 0.4 s: "part." is on screen at 28.00 and said at 28.45.
- Unspoken filler is dropped ("And here's crazy part." skips "the").

**Clearing:** a phrase stays until the cut, then the next shot starts clean. Phrases of 2–5 words, one phrase per shot.

**Numbers:** "4,500 people" is revealed left to right, letter by letter, with a soft edge. That is about 85 ms a letter, 1.0 s for the 12 letters. It reads like a fading typewriter.

## Big words

**"€1.25B."** (46.0 s):
- Instrument Serif Italic about 800 px tall; it spans 88 % of the width.
- Pure white, with a heavy white bloom of about 20 px plus about 80 px.
- It hard-cuts in from the small "for €1.25B.". Frame 1 is blurred and blooming at scale 1.04; it is sharp at frame 4. Then it holds, nearly still.
- This is the same entrance as our Dario "dhero".

**"On August 24th,"** (21.5 s):
- One blank white frame.
- Then the phrase whips in from the right with heavy horizontal motion blur and settles in about 0.3 s. It then keeps drifting slowly.
- The font is Instrument Serif Italic about 330 px, in dark grey on lined white paper (faint horizontal rules).
- The frame's edges are softened by a lens blur; the centre stays sharp.

**On black:** "called", "but it just", "And here's crazy part.", "A 5-year deal", "Why?" and "The intelligence behind it?" are small captions alone on black, with the radial pool of light behind them. They are the breaths between the picture shots.

## Clips: framing, cuts, texture

**Framing:**
- Full-bleed 16:9.
- One subject in the middle with a shallow depth of field: the car's flank, the building, the document, the screen.
- Mostly still or a slow push.
- Documents get a slow push-in, and a yellow marker sweeps across the key figure.

**Cuts:**
- On phrase boundaries, every 1.2–2.5 s.
- A phrase may run across two or three quick shots of the same subject (the crowds: B&W → colour → overhead).

**Transitions:**
- straight cuts;
- a white or overexposed flash frame into a new idea (21.5, 48.5 s);
- black frames for the "breath" lines.

**Texture:**
- Soft, slightly lifted blacks.
- Light grain.
- The dark frames carry a vignette pool.
- The paper frames have faint ruled lines.
