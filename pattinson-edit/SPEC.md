# SPEC — "The Post-Twilight Reinvention" (Robert Pattinson)

Style source: `../reference/sam-altman-reel-breakdown.md` (frame-by-frame study of the reference reel).
Script, VO and captions: the person's script and `robert patison video audio.mp3`, word for word.

GOAL:    The viewer ends convinced Pattinson's post-Twilight run is one of the great reinventions — and wants to rewatch it.
OUTPUT:  HyperFrames, 1440 x 1080 (4:3, horizontal, same frame as the reference), 24 fps.
TIME:    76.0 s x 24 = 1824 frames. No music (the person asked for SFX only). Clock = the VO.

## Timeline (T = output seconds)

| Block | T | Source |
|---|---|---|
| Cold open | 0.000–5.875 | `Starting frame.mp4` 0.00–5.85 — Venice fan shouts "Somebody get these beggars out of here!", cut to Antinous saying it in The Odyssey (voice stem only, music removed) |
| VO-1 | 5.875–30.795 | VO 0.000–24.920 ("Robert Pattinson…" → "…Twilight jokes,") |
| Receipt 1 | 30.795–33.195 | Twilight (2008) "You better hold on tight, spider monkey." (src 398.45–400.85, voice stem) |
| VO-2 | 33.195–38.675 | VO 24.920–30.400 ("he was quietly…" → "…he became Batman.") |
| Receipt 2 | 38.675–42.345 | Jimmy Kimmel Live: "Our first guest tonight is Batman, and the vampire" (src 0.00–3.67, original audio) |
| VO-3 | 42.345–60.195 | VO 30.400–48.250 ("The vampire kid…" → "…sting operations.") |
| Receipt 3 | 60.195–61.645 | Primetime trailer "I'm Chris Hansen." (`Pattison montage 2.mp4` 0.50–1.95, voice stem) |
| VO-4 | 61.645–73.111 | VO 48.250–59.716 ("And now he's closing…" → "…ever seen.") |
| Sting | 73.111–76.000 | Glow title card stepped at 12 fps, shrinks and fades |

VO is never re-cut inside a sentence; the three splits sit in measured silences (24.82–25.04, 30.20–30.72, 48.07–48.52).

## LOOK (numbers from the reference measurements)

- Ground: the footage. Black breath cards = #000 with a radial spotlight behind the words (centre 18% white → 0 at 55% radius).
- Every footage layer carries one `data-color-grading` base:
  adjust {contrast 0.28, blacks -0.35, highlights -0.05, saturation -0.10};
  details {vignette 0.5, vignetteFeather 0.6, grain 0.16, grainSize 0.3};
  effects {chromaticAberration 0.10, filmArtifacts 0.30 (old-film dust/wear build-up), bloom 0.35 r12}.
  Measured target: black point ≈ 5/255, edges ≈ 0.66 x centre, highlights blooming.
- Variants (the reference's colour logic): MONO (mono-clean + base) for archival/sets/directors;
  HALFTONE (halftone 0.9, size 0.30, + mono) for paparazzi/Twilight-era stills; VHS (vhs-playback) for the
  2008 internet-joke beat; RED (mono-screen, palette #000000/#e3121b) for danger flashes (Antinous, Batman);
  NEG (inverted colours) for Tenet's inversion; NEON (bloom 1.2) for Good Time.
- Display face: Instrument Serif Italic 76 px (connective words); Inter Tight 760 weight 62 px, tracking -0.045em
  (meaning words). White #FFFFFF; black #000000 on bright shots. Glow: text-shadow 0 0 2px 95%, 0 0 9px 55%,
  0 0 26px 32%, 0 0 64px 18% white. Caption line centre at 47% of frame height; flanks at 18% / 82% x when a
  centred object (Polaroid, poster) would be covered.
- Word slams: Instrument Serif Italic at 560 px, white, blur-glow 30 px, 2 frames.
- Film titles (Good Time … Mickey 17): 1.6x caption size, held for the whole title shot.

## MOTION

- Captions: each word enters on its spoken onset (snapped to the audio, ±1 frame) with an animated glow:
  opacity 0→1 and blur 10px→0 over 3 frames (expo.out), glow 2.4x→1x over 8 frames. Groups hard-clear at
  the end of their last word (tl.set). No slide, no scale.
- Cuts land on word onsets; in the hook (VO 0–5.9) on the ~0.30 s pulse of the VO cadence.
- Montages "on twos": 2 frames (0.0833 s) per image, caption held.
- Stills move: Ken Burns push 1.00→1.08 over the shot, power1.inOut. Punch-ins are hard 1.6–2x crops.
- Flashes: white 1–2 frames, exposure-blown; negative 1 frame. Whip: 3 frames.
- Pixel reveal (hook): pixelate 0.85→0 in 6 steps over 0.5 s.
- Strips: 5 vertical strips slide in from the right, 2 frames apart, expo.out 0.25 s.
- Grid "box": 3x3 tiles flip in one per frame in random-looking fixed order, then all flash white on "box."
- End sting: steps at 12 fps (every second frame), scale 1.6→1.0, hold, 1 s fade.

## SOUND (no music)

VO 1.0. Receipts at matched loudness. SFX at 0.30–0.55, each on a visible cause, two or three takes rotated:
whoosh/whoosh-short (whips, big cuts), impact-bass-1/2 (word slams: PATTINSON, TWILIGHT, BATMAN, ODYSSEY, DUNE),
glitch-1/2/3 (glitch, negative, red flashes), sparkle (Edward sparkle), riser (crests on "Batman."),
click (Polaroid shutter), whoosh-cinematic (into the sting). Peaks land one frame after the picture.
Mix target −14 LUFS, true peak ≤ −1 dBTP.

## SHOTS (VO-relative seconds; T = VO + offset of its block)

Hook VO 0–5.9: pixel-reveal portrait "Robert Pattinson" → slam PATTINSON → Polaroid (`photo frame` clip)
"is having a | generational" → "run," action pair → "and honestly" Venice crowd/red carpet → black card
"nobody saw it coming."
Edward VO 5.9–8.8: premiere fan frenzy → biology-class stare → sparkle skin "Edward Cullen." (sparkle SFX).
Roles VO 8.8–13.3: face montage across roles; "after Twilight" Twilight poster + slam; "one role." on twos.
Titles VO 13.3–18.4: Good Time (neon) / The Lighthouse (B&W, heavy film wear) / Tenet (negative) /
The Batman (red) / Mickey 17 (halftone yellow) — one title card each.
Swings VO 18.4–22.7: 5 role strips; "weird" on twos with glitch; "bold swing"; "nobody expected".
Internet VO 22.7–24.9: VHS 2008 frames, floating meme stills ("I DON'T SLEEP.", sparkle, tree-climb) →
Receipt 1 spider monkey (tree climb, original voice).
Directors VO 24.9–28.1: Bruce-Wayne set photos (mono halftone) "quietly working" → directors strips
(Nolan, Reeves, Bong Joon-ho, Villeneuve) → Nolan with the IMAX camera "alive,".
Batman VO 28.1–30.4: black "until one day" → Batman silhouette → mask → Batmobile fire "Batman." (riser crest,
slam BATMAN, impact) → Receipt 2 Kimmel.
Respect VO 30.4–35.5: young Twilight-era photo (halftone) → "laughed at" Twilight stills on twos → Venice
phones crowd → red-carpet portraits "Hollywood."
This year VO 35.5–36.5: black "And this | year?" → 2026 slate collage.
Odyssey VO 36.5–41.8: arch figure → Nolan + IMAX "Christopher Nolan's" → poster slam ODYSSEY → Antinous
(callback to the cold open) → red flash on "antagonists."
Primetime VO 41.8–48.25: PRIMETIME title → tan-suit journalist → 2006 TV board → camera crew → "wanna come over?"
chat + hidden camera → sting house → Receipt 3 "I'm Chris Hansen."
Dune VO 48.25–51.3: Scytale in the desert → white robe → DUNE poster slam.
Thesis VO 51.3–55.6: talk-show posters → roles on twos → 3x3 role grid "in one box." → white flash.
Close VO 55.6–59.7: Edward → Batman split "post-Twilight" → "reinvention" accelerating montage → Venice
boat → callback to the hook portrait "the best we've ever seen." (held ≥ 2 s) → sting.

## BANNED

Generic dark void with small floating text (black cards only as the reference's timed breath beats);
everything fading/sliding up; text drifting after it lands; logo docked in a corner; burned-in third-party
captions or watermarks visible (cropped, removed or avoided: freshcuppa, Gala, TOI, story-edit red words,
"I'M CHRIS HANSEN" subtitles); background music.

## QA frames

Every caption at its first frame (glow pulse visible, nothing clipped), each word slam, each film-title card,
the 3 receipts (voice audible, no music), the grid flash, the last line held ≥ 2 s, phone-width readability.
