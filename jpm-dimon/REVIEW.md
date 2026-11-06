# Jamie Dimon / JPMorgan Chase: review (v4, the first 30 s)

v4 is `tools/build4.py`, with media from `tools/prep2.py --spec=media_v4.json` and `tools/prep4.py` (freezes, cut-outs, glows, the globe picture and the matte), and audio from `tools/make_music.py`.

**Rendered:** 0–31.7 s, `renders/jpm-dimon-v4-0-31.mp4`. It ends on "…the United States government."

**Rest of the film:** after 31.7 s it is v3's edit with v4's fonts and no slide.

Every note from today was checked against the frames, and each line below was verified by snapshot.

## The open (S01, 0–9.05 s)
- **Line re-cut:** "especially American financial capitalism" is gone. The voice runs "The name of the game in American capitalism, is being big, and no one is bigger … on Wall Street than JPMorgan Chase." The cuts are made in the voice stem's silences.
- **Restored word:** the source's soft "than" had been put in the music stem by the separator. It is taken back, so the line no longer skips it.
- **"bigger":** 0.5 s longer (a held silence after the word).
- **Word times:** read off the new voice track. In v3 the first words came up about 0.5 s early.
- **"game":** the NYSE trading floor. The picture-left/word-right paper card is gone.
- **"capitalism":** kept as it was (counting machine, vault, the serif word). The line is now one serif lockup, "in American capitalism", with no Helvetica stacked on top.
- **BIG:** simply there, with the negative flash on the cut. No scale-in, no zoom-out, no dive.
- **"bigger":** Dario's SUDDENLY with glow. The word is 340 px (it was 150), the echoes sit just above and below it, there are corner squares and one glitch frame, and the texture is kept.
- **"on Wall Street":** "on", then "Wall", then "Street", big serif words landing in place with no slide, over the Wall St/Broadway sign. "than" follows in small Helvetica.
- **JPMORGAN CHASE:** typed at the centre (about 85% of the width) like Dario's DISAPPEAR, over JPMorgan pictures only (the J.P.Morgan flag, the JPMorgan tower). There is no Chase sign. It leaves through glitch blocks and the tower holds for 0.17 s.
- **Dimon pop:** he pops up from the centre as the Pattinson glow cut-out (white silhouette, then him with a halo).
- **The square:** gone. It was a shadow on an untimed wrapper, the same bug as on the s13 "premise" card, which is also fixed.
- **Shot fix:** the crowd shot is reframed (a dark building column at its left edge had read as a black bar).

## "This is the most influential man in America right now" (S02)
- **Hemant open:** the glowing silhouette (pale grey, then bright cream) over the darkened stage, the live clip showing through at six moments. "This is the most" sits left and "influential" right, with white bars and the white band.
- **Freeze:** the interview plays, pauses, and he comes forward with a white glow. The presidential seal rises behind his head.
- **Cards:** five pictures of him land left, right and top, each after a white box; one lands in front of him. They are the Fortune cover, the White House, the press scrum, Congress, and the young Dimon with cash.

## "He's basically the CEO of Wall Street" (S03)
- **Real video only:** the podium (3× longer than in v3), Stanford (longer), and a third video (walking in with his detail, from your montage) in place of the photos.
- **Caption placement:** captions sit on the side away from him. "He's" and "basically" are spread on the left of the podium shot; "the CEO" is on the right while he walks on the left.
- **Wolf beat:**
  - **Footage:** your Wolf of Wall Street dollar-bill shot.
  - **Lockup:** the face/currency boxes, and the Ackman lockup "OF WALL STREET" in big bold white caps at the bottom, each word with a motion blur.
  - **Exit:** the purple inverted exit frame.

## "a guy who got fired in 1998 by his own mentor over a bonus and a family grudge" (S04)
- **"a guy who got FIRED":** the was-fired reference's opening, on window-lit paper with the four dots and black Helvetica. Three young-Dimon photos step up with no side assets, at the reference's speed.
- **"in 1998":** the roller with Citigroup behind, kept.
- **"by his own":** the Sandy Weill picture now fills the frame horizontally.
- **"mentor":** a three-shot montage (Weill & Dimon, Weill at his desk, Weill's face) with no zooming photo.
- **"over a bonus":**
  - **Four-square:** faster (cells every 2 frames), with your money asset in the top-right cell in place of the money falling on black.
  - **Cartoon:** then your "over a bonus" cartoon (Daffy fanning cash, its watermark cropped) through "bonus, and a".
- **"family grudge":** the Weill photo starts off-centre on him and pans until his daughter is fully in the picture.

## "now runs the biggest bank in the world" (S05)
- Unchanged, as asked. Only the fonts changed, globally.

## "We bank…" (S06, 23.6–31.6 s)
- **Base:** the Bloomberg interview, one continuous take (it is 1080p, not 4K).
- **Lines:** exactly yours, "We bank / some of these companies in 30 countries / We bank / countries / We bank the World Bank, the IMF, … the United States government", captioned in the we-bank reel's style.
- **Globe picture:** in a difference blend at low opacity on the right, with big quote marks (the Fink Rogan screen). It sits behind him: he is matted out of the interview and laid above it, so it never crosses him.

## Type, everywhere
- **Families:** only Inter Tight (the Helvetica role) and Instrument Serif (regular, with glow). Satoshi and the italics are gone from the whole film.
- **One family per line:** the Helvetica-over-serif stack is gone from 0–31 s, except where the we-bank reel itself mixes them ("in 30 countries", "We bank / Countries").
- **No slide:** words land in their final place.

## Measured
- **`check` (5 samples, contrast pass off):** ok.
- **Remaining warnings:**
  - Typed single letters and roller years flagged as brief. The whole word holds; the years flick by design.
  - WebGL performance notices.
  - Lint density warnings in later scenes, as in v3.
- **Looked at:** about 110 frames across 0–31.7 s.

## Open
- **"You have to be big…" (31.7–34.85 s):** it still follows your lines. Dropping it would shorten the film by about 3 s, and the music bed (timed to end on the last frame) would need re-cutting.
- **The "was fired" reference:** used for "a guy who got fired". Tell me if it was meant for "he was fired" at 48 s instead.
