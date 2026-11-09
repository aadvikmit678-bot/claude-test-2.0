# Jamie Dimon / JPMorgan Chase — spec (v2)

**GOAL:** the viewer ends on "$10 trillion every single day" feeling that Dimon's comeback was inevitable: fired, exiled,
back on top. It should play as a motion-graphics documentary, not a slideshow of clips with text on them.

**OUTPUT:** HyperFrames, 1920x1080 (16:9), 30 fps, 93.2 s (2796 frames).

**BUILD:**
- `tools/build2.py --specs` registers every shot in `tools/media_v2.json`.
- `tools/prep2.py` cuts the shots from the Drive sources into `assets/clips2` and `assets/img2`.
- `tools/build2.py` writes `index.html` and `compositions/`.
- v1 lives in `tools/build.py` and `tools/prep_media.py`.

## Audio clock (narrated: the voice is the clock)
Parakeet word times, snapped to the waveform.

| Film time | Source | What is said |
| --- | --- | --- |
| 0.00–8.81 | News open, `name_of_the_game.mp4`: src 1.12–2.68 + 5.05–12.30 | "The name of the game in / American financial capitalism, is being big, and no one is bigger on Wall Street than JPMorgan Chase." |
| 9.05–23.15 | VO 0.00–14.10 | "This is the most influential man in America right now … the biggest bank in the world." |
| 23.60–34.85 | Dimon, Bloomberg interview (`we_bank.mp4` src 273.05–284.30) | "We bank some of these companies in 30 countries … the United States government. You have to be big. You can't do those things and be small." |
| 34.97–91.57 | VO 18.40–75.00 | "Meet Jamie Dimon" lands at 35.25. |

No music has been supplied yet. No SFX, as the user prefers.

## References and what each gives
- **Larry Fink reel (Metro Media House):**
  - pace, with a new picture every 1–3 words and negative flashes on cuts;
  - the seal ring with portraits swapping inside it, plus glint and rays;
  - the "this man" punch-in in front of the seal;
  - the name card on paper with a decoding name and a pale outline echo;
  - the bar write-on;
  - typed giant words with grey-to-white letters and jump reframes;
  - chunk counters ($60 → $60,000 → $60,000,000), 2×2 grids;
  - the window zoom-out, face-detection boxes on the Wolf, the style strobe;
  - logos falling.
- **AMD reel:**
  - the red marker sweep over a real headline (the 1998 NYT "Heir Apparent" clipping);
  - the cream data page with a red line drawing on (Bank One net income 2000–2003).
- **RC Media, Dario reel:**
  - glow serif;
  - the SUDDENLY echo (inverted first frame, a giant blurred echo above and below), used for "BIGGER" and "COMEBACK";
  - the year roller with floating photo cards (1990→1998, 1982→1998, 2000→2004, 2004→2008);
  - the name glitch frames;
  - the photo wall ("the lead") for "the history of Wall Street".
- **RC Media, Hemant reel:**
  - the giant word behind a cut-out ("Amazon" behind Bezos);
  - a word mask over footage ("BIG", then a dive through the letter).
- **Pattinson edit:**
  - Instrument Serif with the white flicker box and the bloom-in;
  - sans words glowing in;
  - each line sliding to stay centred as its words arrive;
  - black words on lit paper.

## LOOK
- **Ground:** the footage itself. Dark set pieces use a near-black #070707 under the user's halftone print (screen, 10 %).
- **Textures:** every scene carries the halftone grunge (overlay 40 %) and halftone paper (soft-light 28 %).
- **Grades:**
  - documentary: contrast +0.16, saturation −0.2, warm +0.05, vignette 0.34, grain 0.12, faint scanlines;
  - CRT for TV news: curvature 0.2, scanlines 0.36;
  - gold bloom for the golden boy;
  - B&W for archival;
  - glitch for "broken";
  - halftone, two-ink, mono-screen and dither in the boxing strobe.
- **Ink and accent:** warm white #FBF8EC. Red #E5381B is reserved for the NYT marker and the data page.
- **Type:**
  - Satoshi Bold 84 / 60 for the small line;
  - Satoshi Black 160 for key nouns;
  - Instrument Serif 128 for line serif words (flicker box);
  - Instrument Serif 236–300 for hero words (blown-out bloom, then a crisp halo);
  - Instrument Serif 250 for names (with the Dario glitch frames);
  - Satoshi Black 330 for the year rollers;
  - Satoshi Black 420–520 for typed giants.

## MOTION
- **Sans word:** blur 16 → 0 and opacity 0 → 1 in 0.24 s (expo.out), with the bloom shadow settling to rest.
- **Serif line word:** a white box flashes for 2 frames where the word will land, then the word writes on, blur 8 → 3 → 0 over 3 frames.
- **Hero word:** a blown-out frame (blur 14, bloom), then 3 soft frames, then crisp.
- **Lines:** each line slides to re-centre as each word lands (0.04–0.2 s, power3.out).
- **Cuts:** hard cuts on the spoken word (−0.05 s), with negative flashes (1–2 frames) on cuts that change world.
- **White flash:** on "fired", "hit", "standing" and the boxing punch.
- **Cameras:** one slow push per shot (1.00 → 1.025), or a hard punch-in (a one-frame set, never eased).

## BANNED
- Pop, bounce or slide-up text.
- Tilts and slides between shots.
- Any SFX.
- The Larry Fink clip itself (it is a style reference only).
- Burned-in subtitles, channel bugs or YouTuber labels on screen (cropped out).
- A still with only a slow zoom and a caption standing in for a beat.

## QA frames
1.2, 4.05, 10.2, 11.3, 13.4, 16.9, 18.9, 26.0, 30.7, 35.6, 36.3, 40.0, 41.4, 46.5, 49.2, 50.0, 53.7, 56.5, 59.8, 61.2,
62.7, 64.0, 65.95, 66.95, 68.2, 73.2, 77.1, 78.6, 80.0, 82.8, 85.7, 87.8, 89.4, 91.2.
