# Jamie Dimon / JPMorgan Chase edit: handoff

Written on Mon 9 Nov 2026 for two readers: the user, who made this film with a Claude session whose account has since expired, and the next Claude session that continues the edit. It gathers what that session left behind (the notes files and commit history in git, the build scripts and the committed film) and checks it against the user's Drive folder. Nothing in git was changed to write it.

**How to read it**
- Paths are relative to the repository root, `/home/user/claude-test-2.0/`, unless they start with `/`.
- Times of day are UTC, taken from `git log` and from Drive.
- "Film" times are seconds in the 93.2 s v5 film. "Ref" times are seconds in a reference video. One film frame is 0.033 s (30 fps).
- "Inter" is short for Inter Tight. "Serif" means Instrument Serif Regular.
- Words in quotes that are attributed to the user are copied exactly from the notes files. Those files mostly record the user's notes in the previous session's condensed wording; the user's own full wording is not in git.
- "Not recorded" or "unknown" means that no file in git says it.

**Contents:** 1 What this is · 2 Where everything is · 3 The film as it stands (v5) · 4 Version history and every note · 5 References and watch-video breakdowns · 6 Style rules and the user's standing preferences · 7 How it is built, edited and rendered · 8 Open questions and next steps

---

## 1. What this is

This is a 93.2-second motion-graphics documentary short about Jamie Dimon and JPMorgan Chase (16:9, 1920×1080, 30 fps, 2,796 frames), built as a HyperFrames project in `jpm-dimon/`. It opens on a Bloomberg reporter's line ("The name of the game in American capitalism, is being big…"), runs on the user's own narration (`jamie dimon audi.mp3`), lets Dimon speak for himself from his Bloomberg interview ("We bank some of these companies in 30 countries…"), and covers it all with documentary footage, photographs and the user's own assets, edited in the style of the user's reference reels, above all the Larry Fink reel by Metro Media House. Its goal, from `SPEC.md`: "the viewer ends on "$10 trillion every single day" feeling that Dimon's comeback was inevitable: fired, exiled, back on top. It should play as a motion-graphics documentary, not a slideshow of clips with text on them." The previous session built it in five rounds of the user's notes on 5–6 Nov 2026, and the current version is v5 (commit `292806f`). v4 and v5 rebuilt only the first 31.7 s (the open through "…the United States government"), and only that stretch was rendered; the user's copy of that render is `jpm-dimon-v5-0-31-share.mp4`. From 31.7 s to the end the film is still v3's cut, with v4's fonts and v5's lighter textures: no notes on it are recorded after v3, and no full-length render of any version is recorded. A first full-length render of v5 was running in this session when this was written (§2).

---

## 2. Where everything is

### The video

| What | Where | Notes |
|---|---|---|
| v5, film 0–31.7 s (the user's "jpm-dimon-v5-0-31-share") | `jpm-dimon/renders/jpm-dimon-v5-0-31-share.mp4`. In the Drive folder its id is `1lMc957Cg69_7NMju71amKNro3LdIChDO`. | 1920×1080, 30 fps, H.264 with AAC sound, 31.70 s. Downloaded from the Drive folder into this checkout on 9 Nov. A Drive title search did not find it; listing the folder does. How it differs from the original render is not recorded. |
| v5 original render, 0–31.7 s | `jpm-dimon/renders/jpm-dimon-v5-0-31.mp4` | Made by the old session. `renders/` is not in git, so it is not in this checkout. |
| v4 render, 0–31.7 s | `jpm-dimon/renders/jpm-dimon-v4-0-31.mp4` | The same: not in this checkout. It ends on "…the United States government." |
| The whole film, 0–93.2 s | `jpm-dimon/renders/jpm-dimon-v5-full.mp4` (master, 250.6 MB) and `jpm-dimon/renders/jpm-dimon-v5-full-share.mp4` (123 MB, re-encoded at the share file's 10 Mbps) | Rendered on 9 Nov with `npx hyperframes@0.9.2 render` from the unchanged v5 project and the media rebuilt by `tools/rebuild/` (54 min, 2,796 frames). The old session never made a full-length render of any version that the files record. **Checked against the user's v5 share render:** `hyperframes diff` over 0–31.7 s gives mean SSIM 0.977 (p05 0.963), all 47 cuts matched, sound 0 ms off. The residue is grain, scanlines and the share file's lighter encode, not different pictures. `renders/` is not in git. |

### Project, branch and old sessions
- **Project:** `jpm-dimon/`, a HyperFrames project. `jpm-dimon/meta.json` records it as created 2026-11-05T19:22:16Z.
- **Branch:** `claude/jpm-dimon-edit`, also on GitHub as `origin/claude/jpm-dimon-edit`. This session works on it.
  - On 9 Nov it gained commits on top of v5 (`292806f`, Fri 6 Nov 19:54) that do not touch the edit: `fb7351b`, `dce1c64` and `008d820` update the HyperFrames skills; `ff85051` adds `jpm-dimon/tools/rebuild/` (the media rebuild kit, §7.3); later commits add this file. `index.html`, `compositions/`, `tools/build*.py`, the prep scripts and the notes files are exactly as v5 left them.
  - Earlier on 9 Nov the branch was merged into `claude/fervent-bohr-532e8t` as `2eadf4b` ("Merge the Jamie Dimon v5 edit (claude/jpm-dimon-edit) to continue it here", 16:24). The session then moved onto `claude/jpm-dimon-edit` itself and copied the three skill commits onto it.
  - Every round's commit is listed in §4.
- **Old sessions** (from the `Claude-Session` lines in the commits):
  - v1 to v5: `session_01Vq7i2awP4rpyPzMUUr5GRk`. The chat link the user pasted (`claude.ai/code/cshk_01Vq7i2awP4rpyPzMUUr5GRk…`) contains the same ID.
  - The Fink reference pass (`18142fc`): `session_014cWME7tHAiVCvUYTf8oFGz`. That session then made a separate, earlier build of the same film in `dimon/` (branch `origin/claude/stoic-mccarthy-hijqav`: `36daffd` Fri 6 Nov 04:01, `0b01d42` 05:49, `18bf89d` 05:51). That build is context only; `jpm-dimon/` is the one being continued.

### Notes files, and which one is current

| File | What it holds | Current? |
|---|---|---|
| `jpm-dimon/REVIEW.md` | The v5 review: the user's notes on v4 one by one, what v5 did about each, the checks and the open items. Rewritten every round. | Yes, for 0–31.7 s |
| `jpm-dimon/REFERENCES.md` | Frame-by-frame breakdowns of the reference reels (§5). Written in v4; v5 added two passes. | Yes for the two v5 passes, except the S03 and S06 effects they list that were never built (§8.3). The first half ("Lifted into v4", "Your assets used in v4") describes v4 and is superseded where v5 changed a beat (§6.4): the five S02 cards and the S01 glow pop-up, BIGGER's echoes "just above and below", "JPMORGAN CHASE" in capitals, the Wolf "slowed to 0.72×", S06 with no B-roll, the globe "at 0.5 opacity" (v5: 0.45). |
| `jpm-dimon/SPEC.md` | The goal, what each reference gives, look, motion, the banned list and the QA frames | In part. It was last changed in v2 (`a9e958c`) and still describes v2 in places: Satoshi, sliding caption lines, "No music has been supplied yet", textures at 40 % / 28 %, the v2 build steps, the v2 open, its list of what each reference gives and its camera rule (1.00 → 1.025) (§6.4). |
| `git show 1ca18f3:jpm-dimon/REVIEW.md` | The v3 review | The latest record for 31.7–93.2 s, with v4's type and v5's lighter textures applied on top. For s07, s08, s10, s12, s15, s17 and s20 it at most lists their set pieces as "Kept from v2"; they were last described in `git show a9e958c:jpm-dimon/REVIEW.md` (neither review mentions s20). |
| `dimon/reference/FINK_REEL_REFERENCE.md`, `fink_words.json`, `frames/` | The Larry Fink reel breakdown, its word timings and its frames (`18142fc`) | Yes (§5.1) |
| `jpm-dimon/HANDOFF.md` | This file | — |

Any older version of a notes file: `git show <commit>:jpm-dimon/REVIEW.md` (or `SPEC.md`, `REFERENCES.md`).

### Code
`jpm-dimon/tools/build5.py` holds the whole edit, and the prep scripts in `jpm-dimon/tools/` make the media it asks for. See §7.

### Media and work files (not in git)
- `.gitignore` keeps out `dimon-src/`, `dimon-work/`, `jpm-dimon/assets/{clips,clips2,img,img2,audio,tex}/`, `jpm-dimon/renders/` and `jpm-dimon/assets/fonts/Satoshi-*`. A fresh checkout starts without them and has to make them again (§7).
- In this container, when this was written:
  - `dimon-src/` holds the Drive download (its layout is in §7.1).
  - `jpm-dimon/assets/` holds `clips2/` (122 files), `img2/` (135), `tex/` (4) and `audio/` (5). They were made again in this session on 9 Nov between 16:30 and 17:00 (file times). `clips/` and `img/`, the v1 media, are empty.
  - `dimon-work/` holds `cut/` (3 photo cut-outs), `music/` (the Bloomberg open split into voice and music), `tx/` and `vo/` (the transcripts and the audio they are matched to) and `cv4/` (OpenCV 4 for `faces.py`). With them, `build5.py` runs and regenerates `index.html`, all compositions and `tools/media_v5.json` byte for byte (checked on 9 Nov).
- **To make all of this again on a fresh session:** `bash jpm-dimon/tools/rebuild/rebuild_media.sh` (about 4 GB of Drive downloads, about 30 min). It downloads the Drive folder by file id, makes the links the scripts read, puts the verified transcripts in `dimon-work/`, runs the prep scripts in order, makes the two by-hand files (the S06 matte and `paper_light.png`) and checks the result. Run on 9 Nov with everything present, every file it re-made was byte-identical to the ones in the full render.

### The Drive folder
"Jamie Dimon": https://drive.google.com/drive/folders/1nC7mwKB1Baj2aL5CQehlxG5ztOkuh7WJ (id `1nC7mwKB1Baj2aL5CQehlxG5ztOkuh7WJ`). It holds the source footage, the reference reels, the user's own assets and the share render. What each file is and where the film uses it: §5.9 and §5.10. The AMD reel and the Pattinson film are not in it.

Reference videos:

| File | Id |
|---|---|
| `larry fink metro media house.mp4` | `1KijjBxmRkq5ICtjzSv0HCHBEPGcnlNjf` |
| `Copy of dario vidoe.mp4` | `1Fnuc3yMBC-RDUN3wwY1mLhunSDw1XZEQ` |
| `Copy of hemant taneja vid.mp4` | `1d7GFmviqHaqcKIZt0DwV9cJpLa8aLkEW` |
| `bill ackman metro medi ref.mp4` | `1TBj5O2GetgQQWolM1-IRHl705Vx-LWcb` |
| `was fired part ref.mp4` | `17it0dLnGR7bgSmcC83b-IY3tQ2gGLsgp` |
| `we bank countries part.mp4` | `1gC51b42vOPI6KgQPbHnYJcUzMA4jU32h` |

The user's assets:

| File | Id |
|---|---|
| `jamie ghost image.webp` | `1sVhI6acIPZy5GkSRjXzj3eAxblSn2nl0` |
| `jp morgan montage.mp4` | `1tR33xzJt3CocPBCZEQS9LDrkcpsL_uyH` |
| `wolf of wwall street vid.mp4` | `1t6phONwSESqe1tLZsJORX5L5M5_FYspR` |
| `wolf of wall street clip to be used when he says wolf of wall street.mp4` | `1gTSe35P06lYmR_bo9RO-5PhSvlCBEUJi` |
| `over a bonus.mp4` | `1jxbPPYeXOiXnzCRGBYhfrfkCY91Hgz6j` |
| `money asset.mp4` | `1PSoq5vawwq3z7N2lbTyyK_FyrdmHX0un` |
| `fiered him push scene punch one. that takes soul out.mp4` | `1h-AhK1rsDURRtkLdeOuIvdDne0f6Mr7h` |

Source footage, and the render:

| File | Id |
|---|---|
| `name of the game.mp4` | `1ARBy0wSIzJLAB-WKTnwt0r7PoJ7IZvii` |
| `we bank the countries, we bank the world bank.mp4` | `1Wllh7CTiF_6nzMO_zrlAZALoDcLedj_A` |
| `Jamie Dimon - The Most Powerful Banker in America   Full Documentary.mp4` | `1OscnlKRqGPkSFuWZ1eGC10ph5cFF34-2` |
| `The Untold Career Story of Jamie Dimon (CEO of JPMorgan).mp4` | `1Vz6hCp5ZzE0dy3kK5CIT0lA66LPAOOE8` |
| `How JP Morgan Chase Became The Largest Bank In The US.mp4` | `1lnXqwCZDXBgnx_hfqIzbiYpO8mbflhDm` |
| `Stories from 2008's Great Recession …` | `1PUD23TiA82yrk4bDG4e9eQl5PEXKDJPT` |
| `Stock Market Crash of 2008.mp4` | `10mOSgJ0gqEBrXldt0y4iS0X0CKNxCwCy` |
| `Jamie Dimon, Chairman, President, and CEO of JPMorgan Chase.mp4` | `1gRz856BM80dCq2-nVCem9TMemOms3Thc` |
| `jamie dimon speaking video.mp4` | `15ratys4h5MljeGNQWpv-2BJOikDelHkk` |
| `jamie dimon audi.mp3` | `1T16cZxLIesMIPeXvv_-RfaKIbR6ExpBK` |
| `J P Morgan The Man Who Bought America   Full Documentary.mp4` | `1ezwAFToKynVr-1sCTvMmtBymyqGj7hyE` |
| `Dimon Cuts Ribbon on JPMorgan's New Manhattan HQ.mp4` | `1LXu49_Vm-i1Wp3Dcaz3QPSSkI6YkeBuy` |
| `JPMorgan building aura farming!! #shorts #aura.mp4` | `12NcnNnOFRh8ZMAzJ3tMAvh5N8RbFgj7_` |
| `NEW YORK STOCK EXCHANGE Closing Bell Ceremony 🇺🇸.mp4` | `1WT260qedOOnd96GNCnejqxyKLLxx0MC_` |
| `💰Wall Street New York … shorts.mp4` | `1N57Mmin5Y-Qb6Vp-PhPhIFq2nU2Rlac4` |
| `watch-citadel-s-high-speed-trading-in-action-ytmp4.savetube.vip.mp4` | `101hb_I5QYxgkFSJ1UuYg25u2AMwScmqm` |
| `cool cinematic clip.mp4` | `1G3Y8jPgq_olTtaKbc9nEVl3pUglOjMQT` |
| `jpm-dimon-v5-0-31-share.mp4` (the v5 render, not a source) | `1lMc957Cg69_7NMju71amKNro3LdIChDO` |

Subfolders:

| Folder | Id |
|---|---|
| `Jamie_Dimon_Image_Pack` | `1YxTGH5jWuwIy91_BjX1PbBEb-1g4Y-a-` |
| `money/pinterest videos` | `1HjNSU0BtRvH1vLDeyE4RiW36u95p5wKR` |
| `halftone textures` | `1HvD_N_JP1P35gnKiuPdXNsdQ9dwJao3C` |
| `sandie weil images` | `1Fk4z_-0Bogwi6MIpwXD7S1f9ofduK6I7` |

---

## 3. The film as it stands (v5)

`jpm-dimon/` plays at 1920×1080, 30 fps, and runs 93.200 s (2,796 frames).

- **Structure:** the root, `index.html`, holds 23 scene compositions (`compositions/s01.html` … `s23.html`, all on track 1), one captions composition (`captions.html`, track 3, z 100), one grain composition (`grain.html`, track 4, z 150) and 5 audio clips. `tools/build5.py` generates all of it (§7).
- **Counts:** `npx hyperframes@0.9.2 compositions` lists 26 compositions. `npx hyperframes@0.9.2 timeline` lists 120 video elements, 477 graphics, 1 captions host and 5 audio clips.

**How to read the tables below**
- Picture cuts land 0.05 s before the word they illustrate (`LEAD`, `CUT(t) = t − 0.05`).
- Word onsets come from the generated compositions, so they are the times the edit actually uses. `build5.py` takes them from Parakeet transcripts snapped to the waveform. Those transcripts (`dimon-work/tx/`) are not in the repo, so a word that no animation keys on has no recorded onset; it is marked "onset not recorded".
- Asset ids are `KEY_<source s×100>_<length s×100>[v][_x<crop>]`. The length includes 0.25 s of padding: `HOW_32320_56` is CNBC source 323.20 s, a 0.56 s file of which 0.31 s is on screen (0.630–0.940). The crop numbers are truncated, not rounded, so some ids do not spell the real crop: `GAME_8150_70_x56_53_114` is cut with xyz (0.57, 0.53, 1.15) and `BANK_120_57_x55_57_120` with (0.55, 0.58, 1.2). Read the `xyz` in `build5.py`. The full naming rule is in §7.3.
- What a shot shows comes from the build-script comments and the `tools/prep_media.py` labels. Shots marked † were not described in the files; each was checked with one frame grab from the Drive source in `dimon-src/_drive` (read-only).
- Grade names (`doc`, `bw`, `crt`, `night`, `hcrt` and the rest) are explained in §7.5.

**Source keys** (`V` in `tools/prep2.py`). The labels for GAME, BANK, MPB, HOW, UNT, STO, CRASH, FIRED, P02, P06, P07, P10 and P11 are the comments on `V` in `tools/prep_media.py` (REVIEW v2 calls MPB "the career documentary"). `prep_media.py` has no entry for CHAIR, SPEAK, MONT, BONUS, MONEY or P01 and no comment on WOLF, so those labels come from elsewhere: MONT, BONUS and MONEY from v4's comment on `V` in `prep2.py`; CHAIR's "Stanford" from the `build5.py` comment on its moment at 1265.2 s; "his talking video" from `build5.py`; WOLF's "the dollar-bill shot" from a `prep5.py` comment; P01's "chess hand" from the `build5.py` S13 comment. File specs and what each source is used for: §5.10.

| Key | Drive file | Label in the files |
|---|---|---|
| GAME | name of the game.mp4 | Bloomberg Originals: the news open + B-roll |
| BANK | we bank the countries, we bank the world bank.mp4 | Bloomberg (Emily Chang) Dimon interview + archival |
| MPB | Jamie Dimon - The Most Powerful Banker in America Full Documentary.mp4 | "Most Powerful Banker in America" documentary |
| HOW | How JP Morgan Chase Became The Largest Bank In The US.mp4 | CNBC |
| UNT | The Untold Career Story of Jamie Dimon (CEO of JPMorgan).mp4 | archival inserts |
| STO | Stories from 2008's Great Recession … .mp4 | 60 Minutes 2008 stories |
| CRASH | Stock Market Crash of 2008.mp4 | 2008 news broadcasts |
| CHAIR | Jamie Dimon, Chairman, President, and CEO of JPMorgan Chase.mp4 | the Stanford talk |
| SPEAK | jamie dimon speaking video.mp4 | his talking video: standing at a window over Manhattan† |
| WOLF | wolf of wall street clip to be used when he says wolf of wall street.mp4 | the dollar-bill shot |
| FIRED | fiered him push scene punch one. that takes soul out.mp4 | the user's "fired" push scene (Doctor Strange) |
| MONT | jp morgan montage.mp4 | the user's montage (4:3, burned subtitles, cropped above them) |
| BONUS / MONEY | over a bonus.mp4 / money asset.mp4 | the user's assets |
| P01–P11 | `_pin/pNN_…` (Pinterest clips; git does not record which Drive files they are, but in this container `_pin/` links into `money_pinterest videos/`, §7.1) | P01 chess hand · P02 man in a burning room · P06 helicopter lifting pallets of money off the Fed · P07 money counting machine · P10 falling money · P11 chess: the king stands, the rest fall |

### 3.1 Scenes at a glance

| Scene | Film time (s) | Spoken | On screen | Text / graphics | Reference imitated | Last rebuilt |
|---|---|---|---|---|---|---|
| s01 | 0.000–9.050 | Reporter (Bloomberg open, re-cut): "The name of the game in American capitalism, is being big, and no one is bigger [0.5 s held] on Wall Street than JPMorgan Chase." | 1–3-word B-roll montage, BIG word mask, reporter in sync, BIGGER set piece, street sign, J.P.Morgan flag → tower (slow motion), Dimon's matted talking video steps up from the bottom | Inter Tight lines; Instrument Serif heroes "capitalism", "Wall Street"; BIG knock-out; BIGGER echoes; typed "JPMorgan Chase" | Fink pace; Hemant word mask (no dive, per user); Dario SUDDENLY; Dario DISAPPEAR | v5 (montage, BIG, "on Wall Street" from v4) |
| s02 | 9.050–12.365 | VO: "This is the most influential man in America right now." | His talking video: grey → cream silhouette with live frames; white silhouette flash; him matted on a defocused copy, with 6 photo cards and the presidential seal; white sweep out | Serif "This is the **most**" left, "**influential**" right; "man in **America**", "right **now**" | Hemant Taneja reel, 0–1.67 s and 21.4–25.1 s | v5 |
| s03 | 12.365–15.065 | VO: "He's basically the CEO of Wall Street," | 270 Park podium; Stanford (arrives moving); walking in → window with 4 cards; inverted frame; Wolf dollar-bill shot (interpolated slow motion) with detection boxes; punch-in; purple negative; white frame | Spread "He's" "basically"; serif "the CEO"; "OF WALL STREET" bold caps | Ackman reel; Pattinson "generational run"; Fink detection boxes | v5 |
| s04 | 15.065–20.855 | VO: "a guy who got fired in 1998 by his own mentor over a bonus and a family grudge," | Paper page with 3 young-Dimon squares; 1990→1998 roller over the Citigroup launch; 8 Weill faces; 2×2 money grid; "over a bonus" cartoon; Weill with his daughter (reframe) | Black Helvetica words + FIRED; roller; small serif "by his own mentor"; "over a" / "bonus" / "and a family" / "grudge" | was-fired (Jan Koum) reel; Dario roller; Dario "every AI tech bro"; Fink 2×2 | v5 (roller, grid, cartoon, grudge from v4) |
| s05 | 20.855–23.600 | VO: "now runs the biggest bank in the world." | Ribbon at 270 Park, on stage, tower from below, JPMORGAN CHASE & CO. on the glass, London, Manhattan from above; white flash out | "now runs the / biggest bank"; "in the / world" | Fink pace | v3 picture, v4 type, v5 textures |
| s06 | 23.600–34.850 | Dimon (Bloomberg interview): "We bank some of these companies in 30 countries. We bank countries. We bank the World Bank, the IMF, we bank the United States government. You have to be big. You can't do those things and be small." | Interview close-up, matted over the globe ghost, alternating with B-roll; then the wide two-shot, towers, the two-shot shrinking into a window | Left-aligned we-bank lockups with hugging quote marks; "You have to be / big"; "You can't do those things / and be small" | "We bank countries" reel; Fink Rogan screen; Fink window zoom-out | v5 to 31.550; v3/v4 after |
| s07 | 34.850–38.430 | VO: "Meet Jamie Dimon, the golden boy of Wall Street," | Name card on paper; young Dimon laughing (gold); young Dimon and Weill (gold); WALL ST. sign (B&W) | "Meet" + decoding "Jamie Dimon"; gold serif "golden boy"; "of / Wall Street" | Fink name card | v2 |
| s08 | 38.430–42.845 | VO: "the guy everyone said was next in line to run the biggest financial company in the world." | Citigroup-launch press flashes; press around him; the 1998 NYT clipping with red marker sweeps | "the guy everyone"; "said was / next in line"; "to run the biggest financial company / in the world" | AMD red marker sweep | v2 |
| s09 | 42.845–47.760 | VO: "He built Citigroup side by side with his mentor Sandy Weill for 16 years." | Commercial Credit; Smith Barney; Citigroup launch; split screen Dimon / Weill; Weill (warm); 1982→1998 roller with 7 cards | "He built / Citigroup"; "side by side with his mentor"; name "Sandy Weill"; "16 years" | Dario roller with floating cards | v3 |
| s10 | 47.760–50.810 | VO: "But then, at 42, he was fired." | Bar write-on; B&W portrait with punch-in; bar write-on; the palm-strike push scene, letterboxed | Bars "But then", "he was"; "at / 42"; "fired" | Fink bar write-on and punch-in | v2 |
| s11 | 50.810–53.020 | VO: "18 months of no job." | Flip calendar NOV 1998 → MAR 2000 | "18 months / of no job" | Fink flip calendar | v3 |
| s12 | 53.020–57.760 | VO: "He took up boxing, read biographies, even met Bezos for a job at Amazon." | Stanford talk; boxing-gloves strobe; reading room; book covers; Bezos; Bezos cut-out with "Amazon" behind | "He took up / boxing"; "read / biographies"; "even met / Bezos"; "for a job at" | Fink style strobe; Hemant word behind a cut-out | v2 (plus the `74e6c6b` Bezos fix) |
| s13 | 57.760–62.080 | VO: "But it was all a premise for the greatest comeback in the history of Wall Street." | Dimon thinking; chess hand on paper; on stage, arm raised; COMEBACK echo; he walks back in; 24-tile archival wall | "premise" black on paper; "in the history of / Wall Street" | Dario SUDDENLY (v2 echo); Dario "the lead" wall | v3 |
| s14 | 62.080–65.320 | VO: "In 2000, he takes over a broken bank in Chicago," | Typed "In 2000"; Dimon at Bank One; broken bank (glitch); Chicago from the air; Chase Tower Chicago | Typed giant words; "he takes over a / broken bank"; "in / Chicago" | Fink typed giant words | v3 |
| s15 | 65.320–67.140 | VO: "cuts the dividend, cleaned it up," | Diagonal slice; dirty copy wiped clean | "cuts the / dividend"; "cleaned it / up" | none named | v2 |
| s16 | 67.140–70.730 | VO: "and puts $60 million of his own money into the stock." | Falling money + counter; $100 note with punch-in; trading screen; ticker board | $60 → $60,000 → $60,000,000; "of his / own money"; "into the / stock" | Fink chunk counter | v3 |
| s17 | 70.730–74.500 | VO: "Turn a $500 million loss into billions in profit." | Cream data page | "Bank One / net income, 2000 - 2003"; red line; −$500M / +$3.5B | AMD data page | v2 |
| s18 | 74.500–77.670 | VO: "That bank got acquired by JP Morgan in 2004." | Fox report (CRT); logo cards merge on paper; 2000→2004 roller with 5 cards | "That bank got / acquired"; "by / JP Morgan" | Dario roller; logo cards | v3 |
| s19 | 77.670–80.190 | VO: "Then, 2008 financial crisis hit," | Hourglass; 2004→2008 roller with 6 cards; Fox "Dow falls 733"; Lehman; room on fire | "Then"; "financial / crisis hit" | Dario roller | v3 |
| s20 | 80.190–82.040 | VO: "and when every other bank was dying," | 10-picture flash montage of the failures; trader, head in hands | "and when every other bank was / dying" | Fink pace, negative flashes | v2 |
| s21 | 82.040–83.495 | VO: "he was the only one standing" | Chess king stands (vertical panel); "Last Man Standing" book + flash | "he was the / only one"; "standing" | none named | v3 |
| s22 | 83.495–86.110 | VO: "with enough money to buy the ones that fell." | Fed cash pallets; "Fire Sale"; Bear Stearns; Washington Mutual; cards drop off the paper | "with enough / money"; "to buy the ones"; "that / fell" on paper | Fink logos falling | v3 |
| s23 | 86.110–93.200 | VO: "That's JP Morgan and Chase, the name that moves $10 trillion every single day today." | Stone sign; glass door; blue signs; wordmark sweep; NYSE board; screens; screen wall + counter; counting machine; Chase building; floor; typed "Today"; Dimon close-up; fade | "That's / JP Morgan"; counter $10 → $10,000,000,000,000; "every single day" (one line); "Today" | Fink chunk counter and typed words | v3 |
| captions | 0–93.200 (66 groups) | | | Pattinson engine (§3.3) | Pattinson edit | v4 engine, v5 blinks |
| grain | 0–93.200 | | Registry grain overlay | | Pattinson film (REVIEW.md) | v5 |
| textures | each scene, full length | | `ht_grunge.jpg` overlay 0.10 + `ht_paper.jpg` soft-light 0.04 (s02 and s06: 0.05 / 0) | | the user's halftone prints | v5 |

### 3.2 Beat by beat

**s01 · 0.000–9.050**

| Time | Spoken (onset s) | Picture | Text / graphics |
|---|---|---|---|
| 0.000–0.630 | The 0.58 | `GAME_0_82` Lower Manhattan, at 0.9× | "The name of the game", Inter Tight 700 84 px, centred (0.513–1.290). Sans words glow in. |
| 0.630–0.940 | name 0.68 · of 0.80 · the 0.90 | `HOW_32320_56` the Wall St sign, 1920s · bw | ↑ |
| 0.940–1.550 | game 0.99 · in 1.36 | `HOW_79260_86` the NYSE trading floor | "in American" small (Inter 84) above "capitalism" (Instrument Serif 236, hero burst) (1.293–3.020) |
| 1.550–2.010 | American 1.60 | `BANK_75060_71` the board and the flag | ↑ |
| 2.010–2.460 | capitalism 2.06 | `P07_100_70` the counting machine; build5 comment "(user: very good)" | "capitalism" lands 2.06 |
| 2.460–3.000 | — | `GAME_32960_79` the vault door | ↑ |
| 3.000–3.450 | is 3.05 · being 3.16 | `GAME_7020_70` towers from below | "is being" (2.983–3.450) |
| 3.450–4.030 | big 3.50 | `GAME_600_83` towers from below†, seen only through "BIG" (Inter 800, 1000 px knock-out, multiply). No push; 2-frame negative at 3.450. | (the word is the matte) |
| 4.030–4.480 | and 4.08 · no 4.28 | `GAME_8150_70_x56_53_114` Wall Street at rush hour, cropped at xyz (0.57, 0.53, 1.15). Reframed in v4 so that a dark building column at its left edge no longer reads as a black bar (REVIEW v4); keep the crop. | "and no one is", y 900, on a dark scrim 0.45 (4.013–5.060) |
| 4.480–5.060 | one 4.60 · is 4.76 | `GAME_840_83` the reporter on camera, in lip-sync. White corner squares 4.960 (top-left, 2 frames) and 5.027 (bottom-right, 1 frame). | |
| 5.060–6.160 | bigger 5.11; held silence 5.70–6.20 | BIGGER on #020202, in three steps. 5.060: glitch frame with the word smeared through a pale band. 5.093: crisp black word in a glowing white bar. From 5.126: the white word with glow (Instrument Serif 340, blur 8 → 0 by 5.227). Rows of three blurred "BIGGER" (520 px; top row 30 % white, bottom 24 %) rush in (expo.out 0.85 s) and creep on, top row left, bottom row right. Faint side copies drift outward. No small copy. Hard cut at 6.160. | Dario SUDDENLY |
| 6.160–7.230 | on 6.21 · Wall 6.29 · Street 6.50 · than 6.78 | `GAME_342_132` the street sign, push 1.00 → 1.04 | "on" (serif 112) + "Wall Street" (serif 340), landing in place (6.143–6.730); "than" (Inter 84, 6.713–7.230) |
| 7.230–7.920 | JP 7.28 · Morgan 7.61 | `flag_slow.mp4` the J.P.Morgan flag (MONT 12.42 s, motion-interpolated slow motion) · night | "JPMorgan Chase" typed into its final centred layout: Instrument Serif 420 px squeezed to 0.70 width. Letters at 7.280 7.420 7.610 7.672 7.734 7.796 7.858 7.920 · 7.970 8.036 8.102 8.168 8.234; the newest letter flares. Dario DISAPPEAR. |
| 7.920–9.050 | Chase 7.97 | `tower_slow.mp4` the JPMorgan tower at dusk (MONT 11.80 s, slowed) · night, push 1.00 → 1.04; the cut lands mid-word | 8.433: light-blue inverted tiles over the word. 8.467: pink and blue blocks, and the word is gone. The tower holds 8.467–8.600. |
| 8.600–9.050 | (reporter ends 8.88) | Dimon's talking video, matted with a glow (`SPEAK_1220_70_x59_40_114` cut + halo). It steps up from the bottom at 10 fps: y 1080 / 560 / 230 / 60 / 0 at 8.60 / 8.70 / 8.80 / 8.90 / 9.00, landing where the s02 silhouette stands. | user note |

**s02 · 9.050–12.365** (reference: Hemant Taneja)

| Time | Spoken | Picture | Text / graphics |
|---|---|---|---|
| 9.050–10.700 | This 9.085 · is 9.45 · the 9.61 · most 9.77 · influential 10.01 | Dimon's talking video (`SPEAK_1265_190_x59_40_114`, dim) under its freeze (`spk_f.jpg`, dark) and silhouette (`spk_sil.png`). The silhouette is grey and see-through (0.86) from 9.050 to 9.730 and opaque cream from 9.763. (`build5.py` passes `grey_until=9.55`, but it is tested against each silhouette segment's start, so the segment that starts at 9.477 stays grey until 9.730.) Live picture shows through at 9.150–9.217, 9.410–9.477, 9.730–9.763, 10.000–10.067, 10.280–10.313 and 10.520–10.620. Live strip across him at 9.400 (1 frame). White glitch blocks at 9.433, 9.467, 9.500 and 10.010. | "This is the" (Instrument Serif 80) + "most" (180), left at x 114; "influential" (180), right-aligned to x 1820, one baseline (y ≈ 380; the lockup is centred on y 330). 10.500–10.567: a cream band through "influential", the word dark and offset inside it, while the white word blinks out. |
| 10.700–10.767 | — | Blazing white silhouette, 2 frames (Hemant 21.375) | |
| 10.767–12.365 | man 10.73 · in 10.97 · America 11.13 · right 11.61 · now 11.85 | The same take (`SPEAK_1437_185_x59_40_114`) as a heavily defocused backdrop (hbg, 1.34 → 1.37), with Dimon matted on top (cut + halo, hcrt CRT lines). Cards from the user's montage land one frame after a soft glowing box: `cd_fortune` top-left 10.86, `cd_congress` bottom-right 11.00, `cd_whitehouse` top-right 11.20, `cd_press` bottom-left 11.40. Red boxes swap in `cd_cash` 11.63 and `cd_park` 11.697. The presidential seal fades in behind his head at 11.13 (to 0.62). Push on his face 1.00 → 1.08, 10.97–11.61. White band sweeps in from the left, 12.265–12.365. | "man in" (Inter 600 60) + "America" (serif 126), y 650 (10.663–11.560); "right" + "now" (serif 126) (11.543–12.265) |

**s03 · 12.365–15.065**

| Time | Spoken | Picture | Text / graphics |
|---|---|---|---|
| 12.365–12.830 | He's 12.415 · basically 12.57 | `GAME_6155_71` the 270 Park podium, push 1.00 → 1.03 | "He's", "basically" spread small on the left (Inter 700 62). Ackman spread words. |
| 12.830–13.160 | the 13.05 | `CHAIR_126520_58` Stanford, arriving still moving (x +220 → 0, scale 1.26 → 1.03 in 0.34 s) | "the" (serif 80) + "CEO" (serif 180), centred at the bottom (12.983–13.720) |
| 13.160–13.720 | CEO 13.21 | `ceo_slow.mp4` walking in with his detail (MONT 16.945 s, interpolated). From 13.24 it eases back into a centred window (0.64, power4.out 0.42 s). Cards pop out behind it in 2-frame steps, each after a soft white box: `dp0` (Healthcare 2013) 13.32, `dp1` (Davos 2016) 13.38, `ld3` (WEF with Becky Quick) 13.44, `pin_mic` (the user's Pinterest photo) 13.50. Inverted frame 13.687. | Pattinson 5.40–6.17 |
| 13.720–15.065 | of 13.77 · Wall 13.93 · Street 14.33 | `wolf_slow.mp4` the Wolf of Wall Street dollar-bill shot: WOLF 12.40–13.43 stretched to 1.35 s by interpolation (REVIEW.md: 0.77×) · warm. It arrives moving and drifts, then punches in 1.05 → 1.12 at 14.895. Purple detection boxes "person 0.97" (13.787) and "currency 0.94" (13.887). Purple inverted frame 14.998; white frame 15.032. | "OF WALL STREET", Inter 800 165 px white caps at the bottom, each word blurring in place over 3 frames (13.77 / 13.93 / 14.33); it turns pink on the purple frame. Ackman 4.2–7.3 s. |

**s04 · 15.065–20.855**

| Time | Spoken | Picture | Text / graphics |
|---|---|---|---|
| 15.065–16.200 | A 15.115 · guy 15.175 · who 15.37 · got 15.53 · fired 15.69 · in (onset not recorded) | Window-lit paper. Square young-Dimon photos replace each other, larger each time: `yd5_1` 230 px (MPB 871 s) 15.065, `yd5_2` 290 px (MPB 700 s) 15.32, `yd5_3` 400 px (UNT 543 s; the B&W portrait is the hero per REVIEW.md; 2-frame zoom blur) 15.64. Four black dots off the corners. The page pushes 1.0 → 1.3 in 0.3 s at 15.69, then drifts to 1.34. | "A / guy / who / got" stacked black Inter 700 56 px; "FIRED" Inter 800 112 px black at 15.69. was-fired (Jan Koum) reel 0–1.95 s. |
| 16.200–17.015 | 1998 16.25 | Year roller 1990 → 1998 (Inter 800 330, glow) over `MPB_85000_107`, the Citigroup launch press conference† (teal), under 62 % black. Lands 1998 at 16.42; "19" flicks inverted 16.620–16.787. Build5 comment "(user: fine with Citigroup behind)". | Dario roller |
| 17.015–18.405 | by 17.065 · his 17.29 · own 17.465 · mentor 17.77 | Eight Sandy Weill faces `wf0`–`wf7`, face centre aligned at (960, 505), zoom-blurred edges, changing every 3 then 2 frames (17 slots), each creeping in 3 %. Four fixed thin white lines frame the face. | "by his own mentor" in small white Instrument Serif 56 at nose height, word by word. Dario 17.40–18.40. |
| 18.405–18.740 | over 18.455 · a 18.65 | One frame 70 % dark, then a 2×2 grid on black, cells every 2 frames, each with a white flash: `P07_120_58` counting machine (TL) · `MONEY_100_52` the user's money asset (TR) · `MPB_178400_45` a $20 bill† (BL) · `HOW_78150_38` a hand with a stack of bills† (BR) | "over a" (Inter 84) |
| 18.740–19.620 | bonus 18.81 · and 19.29 · a 19.405 | `BONUS_590_113_x50_46_109` the user's "over a bonus" cartoon (Daffy fanning cash, watermark cropped), no grade | "bonus" (serif 240, y 880); "and a family" centred from 19.223 |
| 19.620–20.855 | family 19.69 · grudge 20.09 | `MPB_105660_148` Weill with his daughter (v4: "his daughter comes into it"; v1 named this moment `v_jessica`). Reframes from 1.22× / x +170 to 1.05× / x −70. 1-frame negative 19.62. | "grudge" (serif 236, centred) |

**s05 · 20.855–23.600** (straight cuts)
- 20.855: `GAME_9360_55`, the ribbon at 270 Park. "now" 20.905.
- 21.160: `GAME_9920_68`, on stage over the hard hats. "runs" 21.21, "the" 21.405.
- 21.595: `GAME_11420_63`, the tower from below, with a 1-frame negative. "biggest" 21.645.
- 21.975: `GAME_10820_63`, JPMORGAN CHASE & CO. on the glass. "bank" 22.025.
- 22.360: `BANK_120_57_x55_57_120`, London. "in" 22.41, "the" 22.57.
- 22.680: `GAME_8020_117`, Manhattan from straight above. "world" 22.73.
- **Flash:** a white flash builds from 23.530 (0.85 at 23.580) and is cut off by the scene end at 23.600.
- **Captions:**
  - "now runs the" (Inter 84) over "biggest bank" (Inter 800 160), 20.838–22.360.
  - "in the / world" ("world" serif 236), 22.343–23.550, fading from 23.430.

**s06 · 23.600–34.850** (Dimon's own audio)

| Time | Spoken (Dimon) | Picture |
|---|---|---|
| 23.600–25.080 | We 23.725 · bank 23.85 · some 24.285 · of 24.49 · these 24.57 · companies 24.73 · in 25.13 | `BANK_27305_820_x63_50_135`: the interview close-up, one continuous take of source 273.05–281.00, Dimon left of centre, push 1.00 → 1.03. Dimon is re-laid on his own matte (`…_cut.webm`) above `globe_ghost.jpg` (x 800–2020, difference blend, opacity 0 → 0.45). The ghost zooms 1.00 → 1.12 and drifts (−110, −36) over 23.600–31.550. It pulls focus (blur 13 → 1 px, 0.85 s) at 23.600, 26.445, 27.745 and 28.795. |
| 25.080–25.640 | 30 25.255 | B-roll `BANK_5262_81_x50_42_120`, the JPMorgan Global China Summit |
| 25.640–26.445 | countries 25.69 | `BANK_4030_105`, Davos, World Economic Forum stage |
| 26.445–26.885 | We 26.495 · bank 26.57 | interview |
| 26.885–27.745 | countries 26.935 | `BANK_30_111_x55_55_114`, London from the air |
| 27.745–28.200 | We 27.795 · bank 27.855 · the 28.165 | interview |
| 28.200–28.795 | World 28.25 · Bank 28.49 | `worldbank.jpg`, the World Bank building, Washington (image pack) |
| 28.795–30.280 | the 28.845 · IMF 29.05 · we 29.935 · bank 29.995 · the 30.25 | interview |
| 30.280–30.795 | United 30.33 · States 30.595 | `BANK_7745_77`, with Obama |
| 30.795–31.550 | government 30.845 | `BANK_2835_100`, testifying to Congress |
| 31.550–32.160 | You 31.705 · have 31.81 · to 31.97 · be 32.05 | `BANK_28100_86`, the interview continues on the wide two-shot with the interviewer† |
| 32.160–32.875 | big 32.21 | `GAME_7060_97`, the towers (1.15 → 1.00) |
| 32.875–34.850 | You 32.925 · can't 33.05 · do 33.45 · those 33.61 · things 33.85 · and 34.17 · be 34.33 · small 34.49 | `BANK_28232_223`, the wide two-shot†. It shrinks into a window (scale 0.16, 34.440–34.820, power3.out): Fink window zoom-out. |

Captions in s06:
- **Style:** left-aligned at x 1110, centred on y 520, each group leaving with a blur.
  - "We bank" (23.658–24.235).
  - "some of these / **companies** / in **30** *countries*" (24.218–26.445).
  - "We bank / *Countries*" (26.428–27.745).
  - "We bank the / **World Bank**" (27.728–28.795).
  - "the / *IMF*" (28.778–29.885).
  - "we bank the / **United States** / *government*" (29.868–31.550).
  - Bold = Inter 800 100–118; italics here mark Instrument Serif 150–230.
- **Quote marks:** Inter 800 210 px, 0.92 white. They hug the lines only while the interview is up: 23.600–24.235, 24.235–25.080, 26.445–26.885, 27.745–28.200, 28.795–29.885, 29.885–30.280.
- **Centred groups:**
  - "You have to be / **big**" (Inter 800 200, 31.638–32.875).
  - "You can't do those things / and be small" (y 820; "small" in the small 62 px size, 32.858–34.800, fading from 34.680).

**s07 · 34.850–38.430**
- **34.850:** white frame, 1 frame.
- **34.883–36.760, the Fink name card on paper:**
  - `cut_dimon09` (image pack, Rachel Reeves portrait crop, matted, B&W) on a navy gradient card 560×700 that settles from 1.65× in 0.36 s.
  - "Meet" (Inter 700 48, black) at 35.25.
  - "Jamie Dimon" (Inter 800 118) decodes letter by letter, pale → grey → black, in shuffled order, 35.525–36.04.
  - A giant pale outline "JAMIE DIMON" (Inter 800 330) sits behind.
  - Spoken: Meet 35.25 · Jamie 35.525 · Dimon (onset not recorded).
- **36.760:** `MPB_29480_73_x68_45_150`, young Dimon laughing · gold, with a gold gleam sweep (36.810–37.260). Spoken: the 36.81 · golden 36.895.
- **37.245:** `MPB_35620_49`, young Dimon and Weill laughing† · gold, gleam 37.275–37.485. Spoken: boy 37.295.
- **37.485–38.430:** `HOW_32360_120`, the WALL ST. sign† · bw. Spoken: of 37.535 · Wall 37.615 · Street 37.935.
- **Captions:** "the / golden boy" (Instrument Serif 236, gold halo); "of / Wall Street" (serif 236).

**s08 · 38.430–42.845**
- **38.430:** `MPB_85060_59`, press flashes at the Citigroup launch. Spoken: the 38.48 · guy 38.54.
- **38.765:** `BANK_3460_65`, the press around him. Spoken: everyone 38.815.
- **39.165–42.845, the real 1998 NYT clipping** (`nyt_1093.jpg`, MPB frame at 1093 s, bw):
  - Negatives at 39.165 and 40.285.
  - 1.25 → 1.32 on the headline.
  - A red multiply marker sweeps under "Heir Apparent" (39.695–40.395) with a red cursor riding it, then blinking.
  - At 40.285 a hard jump-reframe goes down to the body text (1.85 → 1.95).
  - Marker under "the world's largest financial" (40.870–41.500), then "services company," (41.500–42.015).
  - Reference: AMD.
- **Spoken:** said 39.215 · was 39.455 · next 39.695 · in 39.96 · line 40.095 · to 40.335 · run 40.495 · the 40.735 · biggest 40.87 · financial 41.215 · company 41.62 · in 42.015 · the 42.175 · world 42.335.
- **Captions:**
  - "the guy everyone".
  - "said was / next in line" (serif 236, y 760).
  - "to run the biggest financial company / in the world" (Inter 600 62 + serif "world", y 770).

**s09 · 42.845–47.760**
- **42.845:** `MPB_73460_58`, Commercial Credit, where they started. He 42.895.
- **43.170:** `MPB_101860_41`, Smith Barney. built 43.22.
- **43.325:** `MPB_84040_105`, the Citigroup launch, with a negative. Citigroup 43.375.
- **44.125–45.325, split screen on black:**
  - Left `BANK_45580_145`, a photo portrait of Dimon†.
  - Right `MPB_43860_105` from 44.525 with a white frame. v1 labels MPB 438 s "Weill".
  - Spoken: side 44.175 · by 44.415 · side 44.575 · with 44.815 · his 44.895 · mentor 44.975. Caption at y 930.
- **45.325:** `MPB_86040_108`, Sandy Weill · warm. Sandy 45.375 · Weill 45.775. Name style, serif 250.
- **46.160–47.760, year roller 1982 → 1998:**
  - Seven white-bordered drifting cards (`c16_0`–`c16_6`).
  - Lands 1998 at 47.105; "16 years" (Inter 700 60) at 47.055.
  - Spoken: for 46.21 · 16 (onset not recorded) · years 47.055.

**s10 · 47.760–50.810**
- **47.760–48.420, bar write-on:** "But" 47.81 and "then" 47.94 (Inter 700 110) flip out of white bars; a bar sweeps them away 48.287–48.387.
- **48.420–49.500:** `UNT_54380_133` · bw, the same source moment as the B&W portrait. Negative at 48.420; hard punch-in to 1.45 at 48.650. Spoken: at 48.47 · 42 48.53. Caption "at / 42" (serif 300).
- **49.500–49.907:** bars "he" 49.55 and "was" 49.615; sweep 49.807.
- **49.840–50.810:** `FIRED_9693_161` at 1.4×, letterboxed 1920×804 on black, push to 1.08. This is the user's push scene (Doctor Strange palm strike). White flash peaks at 49.89; 2-frame negative 49.957. Spoken: fired 49.89. Caption "fired" (serif 300).

**s11 · 50.810–53.020**
- **Calendar:** cream pages with a red month band, on black, at x 620. NOV 1998 holds until 51.175. Then a page every 2 frames to MAR 2000 at 52.175, with a white flash (0.45). Push 1.00 → 1.06.
- **Spoken:** 18 50.86 · months 51.375 · of 51.73 · no 51.935 · job 52.175.
- **Caption (right, x 1330):** "18" (Inter 800 160) "months" / "of no" (serif 128) "job" (serif 236).

**s12 · 53.020–57.760**
- **53.020:** `CHAIR_287500_67`, Dimon in an armchair at the Stanford talk†. He 53.07 · took 53.13 · up 53.295.
- **53.440–54.045, style strobe on `gloves.jpg`:**
  - Looks change every 2–3 frames: doc, halftone, two-ink, mono, dither, print, doc, halftone.
  - Punch to 1.35 at 53.54; flash at 53.49.
  - Spoken: boxing 53.49.
- **54.045:** `MPB_118000_38`, the reading room · warm. read 54.095.
- **54.180–55.460:** book covers flip: MPB 616.0, then MPB 1496.0, then MPB 1273.0 (from 54.380). biographies 54.23.
- **55.460:** `GAME_25660_114`, even met Bezos, with a negative. even 55.51 · met 55.57 · Bezos 55.775.
- **56.350–57.760:** the Bezos cut-out (`cut_bezos03`, warm) on a brown ground. A giant "Amazon" (Instrument Serif 470) slides behind him; 2-frame negative. Spoken: for 56.40 · a 56.575 · job 56.655 · at 56.815 · Amazon (onset not recorded).
- **Captions:** "for a job at" sits at the top (y 180).

**s13 · 57.760–62.080**
- **57.760:** `BANK_3660_94`, Dimon thinking. But 57.81 · it 57.87 · was 58.015 · all 58.20 · a 58.335.
- **58.445–58.890:** `P01_640_70v`, the chess hand · bw, in a 520×780 panel on paper (1.55 → 1.0). "premise" 58.495, in black Instrument Serif 250 on the paper, right.
- **58.890:** `GAME_6140_92`, on stage, arm raised. for 58.94 · the 59.135 · greatest 59.295.
- **59.565–59.865, COMEBACK:**
  - One inverted frame: black word on a cream panel.
  - Then a white "COMEBACK" between drifting giant blurred echoes on #060606.
  - comeback 59.615.
- **59.865:** `MPB_146840_51`, he walks back in, with a 4-frame light streak.
- **60.125–62.080, photo wall:**
  - 24 B&W archival tiles (6×4) assemble in 0.55 s; centre darkens from 60.455; push to 1.1.
  - Spoken: in 60.175 · the 60.335 · history 60.415 · of 60.735 · Wall 60.895 · Street 61.36.
  - Caption "in the history of / Wall Street" (serif 300, blur exit 61.90).

**s14 · 62.080–65.320**
- **62.080–62.910:** typed "In" (150 px) 62.13 and "2000" (520 px) 62.19, Inter 800, grey → white over 3 frames. Jump-reframes 1.5 → 1.15 (62.31) → 1.0 (62.55).
- **62.910:** `MPB_144620_99`, Dimon at Bank One, with a negative. he 62.96 · takes 63.135 · over 63.375 · a 63.535.
- **63.645:** `MPB_119220_89`, a broken bank, with glitch-grade overlays 63.675–63.828 and 63.995–64.062. broken 63.695 · bank 64.095.
- **64.285:** `MPB_124800_41`, Chicago from the air, with a negative. in 64.335.
- **64.445:** `chi_tower.jpg`, Chase Tower Chicago (push to 1.07). Chicago 64.495.
- **Captions:** "Chicago" in Inter 800 160.

**s15 · 65.320–67.140**
- **65.320:** `MPB_144600_134`, the same Bank One shot. At 65.675 a white cut-line flashes and the two diagonal halves shear apart. Spoken: cuts 65.37 · the 65.535 · dividend 65.615.
- **66.410:** `MPB_132300_98`, younger Dimon in a leather chair†. A "dirty" copy is wiped off left to right by a glowing line (66.755–67.075). Spoken: cleaned 66.46 · it 66.735 · up 66.815.

**s16 · 67.140–70.730**
- **67.140:** `P10_150_180`, falling money · warm, under 55 % black. Chunk counter at left: $60 67.615 → $60,000 67.755 → $60,000,000 67.85. Spoken: and 67.19 · puts 67.295.
- **68.685:** `bill100.jpg`, a classic $100 note, with a hard punch to 1.4 at 69.295. Spoken: of 68.735 · his 68.895 · own 69.08 · money 69.295. The caption sits on a scrim.
- **69.565:** `HOW_102320_57`, a finger on a trading screen†, with a negative. into 69.615 · the 69.855.
- **69.885:** `BANK_75790_109`, a stock-ticker board†. stock 69.935.

**s17 · 70.730–74.500**
- **Page:** white frame, then the AMD cream page. "Bank One" (serif 92) / "net income, 2000 - 2003"; dashed zero line; years 2000–2003. The page scales 1.0 → 1.22 toward 2003.
- **Animation:** first red dot 71.087; "−$500M loss" 72.142; red line draws 72.61–73.22; "+$3.5B profit" 73.20. No captions.
- **Spoken:** Turn 70.78 · $500 71.12 · loss 72.175 · into 72.61 · billions 73.00. "a", "million", "in" and "profit" have no recorded onset.

**s18 · 74.500–77.670**
- **74.500:** `HOW_69700_117`, the Fox report · crt. That 74.55 · bank 74.665 · got 74.905 · acquired 75.065 (Inter 800 160).
- **75.415–76.410:** on paper, the Bank One and J.P. Morgan logo cards slide together and become the JPMorgan Chase (2008) card at 76.025, with a white flash. by 75.465 · JP 75.625 · Morgan 76.025 (name serif 250, y 880).
- **76.410:** roller 2000 → 2004 over `HOW_69260_151`, the JPMorgan Chase building with flags† · teal, with 5 cards. Lands 2004 at 76.585. Spoken: in 76.46 · 2004 76.585.

**s19 · 77.670–80.190**
- **77.670:** `HOW_69800_82_x36_27_300`, the hourglass · bw. Then 77.72.
- **78.240:** roller 2004 → 2008 over `HOW_79300_89`, the NYSE floor from above† · teal, with 6 cards. Lands 2008 at 78.42. Spoken: 2008 78.29.
- **78.880:** `CRASH_7250_69`, Fox "Dow falls 733" · crt, with a 2-frame negative. financial 78.93.
- **79.320:** `STO_143860_67`, Lehman. crisis 79.37.
- **79.735:** `P02_120_70`, the room on fire · warm, with a white flash peaking at 79.785. hit 79.785.

**s20 · 80.190–82.040**
- **Flash montage:** ten pictures, 0.1225 s each, alternating doc and B&W, with negatives at 80.313, 80.680 and 81.048.
  - `cr_lehman_boxes`.
  - `MPB_189120_37` (Bear Stearns per v1).
  - `cr_wamu`.
  - `HOW_101060_37`.
  - `GAME_40960_37`.
  - `STO_34620_37` (near v1's "bank run").
  - `STO_3040_37` (near v1's FDIC).
  - `cr_lehman_ts`.
  - `STO_172300_37` (60 Minutes "A BANK RESCUE"†).
  - `cr_lehman_nyc`.
- **81.415:** `STO_229460_88`, a trader with his head in his hands.
- **Spoken:** and 80.24 · when 80.345 · every 80.53 · other 80.825 · bank 80.985 · was 81.305 · dying 81.465.

**s21 · 82.040–83.495**
- **82.040:** `P11_90_130v_x50_50_100`, the chess king stands while the rest fall, in an 800×1080 panel on black. he 82.09 · was 82.265 · the 82.425 · only 82.60 · one 82.825.
- **83.095:** `MPB_191660_65`, the "Last Man Standing" book†, with a white flash at 83.145. standing 83.145 (serif 300).

**s22 · 83.495–86.110**
- **83.495:** `P06_100_105`, pallets of cash lifted off the Fed. with 83.545 · enough 83.785 · money 84.025.
- **84.295:** `UNT_115760_65`, "Fire Sale" · crt, with a negative. to 84.345 · buy 84.505.
- **84.695:** `MPB_189040_41`, Bear Stearns. the 84.745.
- **84.855:** `HOW_101080_50`, Washington Mutual. ones 84.905.
- **85.110:** on paper, the Lehman logo card, the WaMu logo card and a Bear Stearns signage photo land (85.11 / 85.21 / 85.31) and drop out of frame (85.37 / 85.43 / 85.49). Spoken: that 85.16 · fell 85.37. Caption in black at the top.

**s23 · 86.110–93.200**
- **86.110:** `MPB_151760_83`, the stone sign. That's 86.16 · JP 86.265.
- **86.695:** `GAME_10960_65`, the glass door. Morgan 86.745.
- **87.095:** `GAME_20280_41`, the blue signs. and 87.145.
- **87.255–87.850:** the JPMorganChase 2024 wordmark, white, revealed by a 0.32 s light sweep on black, plus a streak. Chase 87.305.
- **87.850:** `BANK_75080_54`, the NYSE board. the 87.90 · name 87.96 · that 88.185.
- **88.135:** `BANK_75660_68`, screens of stock charts†. moves 88.345.
- **88.570–89.990, screen wall:**
  - A 3×3 wall of trading-screen clips, plus `P10_320_167` falling money in screen blend at 0.55, under 42 % black.
  - Centred counter $10 88.62 → $10,000,000 88.80 → $10,000,000,000,000 89.065.
  - Spoken: $10 88.62 · trillion 89.065.
- **89.990:** `P07_200_48`, the counting machine. every 90.04.
- **90.215:** `BANK_74460_57`, a CHASE building on a street†. single 90.265.
- **90.535:** `GAME_12890_57`, the floor at work. day 90.585. Caption "every single day" (one line), y 860.
- **90.855–91.815:** typed "Today" (Inter 800 420) on black from 90.905. today 90.905; the VO ends 91.575.
- **91.815–93.200:** `BANK_103140_164`, Dimon in close-up against a red-and-white background† (v1 called this `m_end`). Push to 1.08, 2-frame negative at 91.815, fade to black 92.450–93.070.

### 3.3 Layers over the whole film
- **captions.html:** 66 groups (`cg000`–`cg065`), each word in its final place (no slide since v4). Most lines keep one font family, but six mix Inter Tight and Instrument Serif: "man in America" and "right now" (s02), "in 30 countries" (s06), "in the world" (s08), "crisis hit" (s19) and "every single day" (s23). The Pattinson caption engine has four word types: sans words (Inter 84 / 62 / 160) glow in; serif line words land after a white flicker box; hero, name and gold words (serif 236 / 250 / 300) burst in blown out and settle crisp with a halo; "paper" words ("premise", "that fell") are black on paper. Frame by frame: §7.5.
- **grain.html:** the registry `grain-overlay` noise at 6 %, overlay blend, re-positioned 12 times a second, 0–93.2.
- **Per-scene textures:** grunge overlay 0.10 + paper soft-light 0.04 (s02 and s06: 0.05 / 0). Black grounds carry grunge in screen at 0.05.

### 3.4 Audio
In `index.html`. Every clip is at volume 1; the voices are on track 10 and the music on 11.

| Clip | File (made by) | Content | Film | Media in | Level | Fades |
|---|---|---|---|---|---|---|
| news | `assets/audio/news_voice.wav` (`tools/make_music.py`) | The reporter's voice alone (Demucs vocal stem of name_of_the_game.mp4). Source 1.12–4.05 + 6.85–9.62 + 0.5 s silence (film 5.70–6.20) + 9.62–12.30; the soft "than" (src 10.18–10.44) is put back from the music stem. | 0.000–8.880 | 0 | −16 LUFS | out 0.02 |
| music | `assets/audio/music_bed.wav` (`make_music.py`) | The Bloomberg open's own music: the Demucs no-vocals stem, opening cue, 120 BPM. Film 0–42.915 = cue 2.17–45.085, then one bar-aligned jump (80 ms equal-power crossfade). Film 42.915–93.2 = cue 3.215–53.5, so the cue's own ending lands on the last frame. A 0.6 s fade is baked in from 92.6. | 0.000–93.200 | 0 | −30 LUFS (≈14 dB under the voice) | out 0.05 |
| vo-a | `assets/audio/vo.wav` (`tools/prep_media.py`, v1: the user's "jamie dimon audi.mp3") | VO 0.00–14.10 | 9.050–23.150 | 0.000 | −16 LUFS | out 0.06 |
| dimon | `assets/audio/dimon_quote.wav` (`prep_media.py`: we_bank.mp4 src 272.5–285.0) | Dimon, src 273.05–284.30 | 23.600–34.850 | 0.550 | −16 LUFS | in 0.02, out 0.06 |
| vo-b | `assets/audio/vo.wav` | VO 18.40–75.00; "Meet" lands at 35.25 | 34.975–91.575 | 18.400 | −16 LUFS | out 0.08 |

- **Music only:** 8.880–9.050, 23.150–23.600, 34.850–34.975 and 91.575–93.200.
- **Unused VO:** vo.wav 14.10–18.40 is never placed. SPEC v1 calls it "the narrator's paraphrase at VO 14.24-18.48", replaced by Dimon's own words. Its words are not in the repo.
- **No SFX:** the user's standing preference (§6.1).
- **Not heard:** REVIEW.md says the levels "were measured, not listened to."

### 3.5 What v5 rebuilt and what it carried over

| Film range | Scenes | Status |
|---|---|---|
| 0.000–9.050 | s01 | **v5.** BIGGER redone as Dario's SUDDENLY, frame for frame. "JPMorgan Chase" typed like DISAPPEAR over slow-motion flag and tower, ending in the tile exit. Dimon's matted slide-up. "in American" small again. The montage, BIG, "on Wall Street" and the re-cut news line are v4's. |
| 9.050–12.365 | s02 | **v5:** Hemant opening and stage on his talking video |
| 12.365–15.065 | s03 | **v5:** Pattinson transitions, the continuous interpolated Wolf, the Ackman words blurring in place, punch-in, purple and white frames |
| 15.065–20.855 | s04 | **v5:** young-Dimon squares, the page push, Weill faces, the dark frame, centred "and a family" / "grudge". Roller, faster four-square, cartoon and grudge reframe are v4's. |
| 20.855–23.600 | s05 | **Carried:** v3 code unchanged ("now runs the biggest bank in the world": no change). Only fonts (v4) and lighter textures (v5) differ. |
| 23.600–31.550 | s06, part 1 | **v5:** B-roll interleaved, the ghost moving and pulling focus, quote marks per group. The base interview, the matte and the we-bank captions are v4's. |
| 31.550–34.850 | s06 tail ("You have to be big…") | **Carried:** v3 picture; v4 made "big" Inter 800 200. Untouched in v5 (an open item in the v4 review, §8.2). |
| 34.850–93.200 | s07–s23 | **Carried:** v3's edit (commit `1ca18f3`); the S07–S23 code is identical in build4.py and build5.py. v4 changed type (Satoshi and italics → Inter Tight + Instrument Serif, no slide) and removed the box-shadow from the s13 "premise" chess-hand panel (the same untimed-wrapper bug as the S01 "square"; REVIEW v4). v5 changed only the global look: textures 0.40 / 0.28 → 0.10 / 0.04, ground texture 0.10 → 0.05, grade grain 0.12 → 0.07, plus the grain overlay. s07, s08, s10, s12, s15, s17 and s20 have not changed since v2, apart from v4's type and v5's textures: v3 did not touch their scene files (s12 also has the `74e6c6b` fix). **The v4 and v5 renders stop at 31.7 s**, so no render of 31.7–93.2 is recorded since v3. |

The notes behind each round, word for word, are in §4.

---

## 4. Version history and every note

The film was built in rounds on `claude/jpm-dimon-edit`. Each round rewrote REVIEW.md, so a round's notes are read with `git show <commit>:jpm-dimon/REVIEW.md`. Media, work files and renders were never committed.

| Round | Commit | When (UTC) | Generator scripts | Notes files changed | Render recorded |
|---|---|---|---|---|---|
| Reference | `18142fc` | Thu 5 Nov 19:21 | none | `dimon/reference/FINK_REEL_REFERENCE.md` (new) | none |
| v1 | `2bb2905` | Thu 5 Nov 20:32 | `tools/prep_media.py`, `tools/build.py` | `SPEC.md`, `REVIEW.md` (new) | none named |
| v2 | `a9e958c` | Fri 6 Nov 00:01 | `tools/build2.py`, `tools/prep2.py` (`media_v2.json`) | `SPEC.md`, `REVIEW.md` rewritten | none named |
| v2 fixes | `74e6c6b` | Fri 6 Nov 00:16 | `tools/build2.py` | none | none |
| v3 | `1ca18f3` | Fri 6 Nov 04:46 | `build3.py`, `make_music.py`, `check_shots.py` (`media_v3.json`) | `REVIEW.md` rewritten | none named |
| v4 | `127f4c1` | Fri 6 Nov 17:49 | `build4.py`, `prep4.py` (`media_v4.json`); changed: `make_music.py` (the open re-cut) and `prep2.py` (the MONT, BONUS, MONEY and WOLF2 keys) | `REVIEW.md` rewritten, `REFERENCES.md` (new) | `renders/jpm-dimon-v4-0-31.mp4`, 0–31.7 s |
| v5 | `292806f` | Fri 6 Nov 19:54 | `build5.py`, `prep5.py`, `faces.py` (`media_v5.json`) | `REVIEW.md` rewritten, `REFERENCES.md` extended | `renders/jpm-dimon-v5-0-31.mp4`, 0–31.7 s |

### Reference pass: `18142fc` "Jamie Dimon edit: frame-by-frame reference from the Larry Fink reel" (Thu 5 Nov 19:21)

**What was done.** The Larry Fink reel (Metro Media House) was measured "frame by frame: every second at 10 fps, and every animated beat at the full 30 fps", and its voiceover was transcribed to word timings. The doc calls it "The user's style reference for the next video".
- Source: Instagram reel `Dewt0XXoHtk`.
- The user's Drive copy is `larry fink metro media house.mp4` (id `1KijjBxmRkq5ICtjzSv0HCHBEPGcnlNjf`). Drive shows it added to the folder at 19:07 that evening.
- Format: 1276×718, 30 fps, 85.0 s.

**Where it lives.**
- `dimon/reference/FINK_REEL_REFERENCE.md` (347 lines at this commit); `dimon/reference/fink_words.json`, with word timings as `[start, end, word]`; `dimon/reference/frames/`, 27 contact sheets and beat frames.
- These are in `dimon/`, not `jpm-dimon/`, and no jpm-dimon file cites them by path.
- The local video copy, `pattinson-work/refs/fink.mp4`, was never committed.
- The `dimon/` build later added a §11, "What makes it read as animation (learned the hard way on Dimon v1)" (`0b01d42`). That section is only on `origin/claude/stoic-mccarthy-hijqav`, not in this checkout; read it with `git show 0b01d42:dimon/reference/FINK_REEL_REFERENCE.md` (367 lines). The checked-out copy is the `18142fc` version (§1–§10, 347 lines).

**What it records** (measurements in §5.1).
- **Story:** 8 numbered beats plus an end sting: a contradiction hook backed by an outside voice, then the name reveal (together, beat 1), a paradox, rise, fall, comeback, crisis irony, a payoff in numbers, and a kicker. Its §10 splits the hook and the name reveal into a 9-beat template for Dimon.
- **Pace:** 233 cuts in 85 s, median shot 0.45 s, "a new picture on almost every 1–3 words". The camera is almost static (scale change 1.00–1.02).
- **Type:** one bold grotesque, mapped to Inter Tight 700/800 ("No serif anywhere in this reference"); centred line captions of about 56 px that hard-cut on word by word; the bar write-on, hero lockups and chunk counters; giant typed words that go from grey to white; a name decode with a giant outline echo; a quote panel with a ghost portrait and globe.
- **Transitions:** a negative flash about every 3–4 s (the signature cut), white and grey flashes, a ray burst, a particle dissolve, HUD wireframes, a style strobe, a window zoom-out (100 % to 59 % in 0.55 s), a 2×2 grid and a logo sting.
- **Sound:** "a continuous dark, bass-heavy music bed" plus SFX hits. The doc adds: "This differs from the Pattinson edit, which used SFX only. Ask the user whether the Dimon edit gets music."
- **The rest:** how each Fink beat is treated, a shot-by-shot table, and a §10 plan for Dimon. The plan left two open items: music, and an AI-animated portrait, which would need a generated clip.

### v1: `2bb2905` "Jamie Dimon / JPMorgan Chase edit v1 (16:9, HyperFrames)" (Thu 5 Nov 20:32)

**What the user asked for, as recorded:**
- **Format:** "16:9, user switched from vertical" (SPEC) and "the user switched from 9:16" (REVIEW).
- **Sound:** "Music bed: none supplied yet (asked); no SFX (user's standing preference)" (SPEC).
- **The Larry Fink clip** was excluded: "the user said it is for someone else" (REVIEW).
- **Material:** the user's Drive folder, their voiceover (`jamie dimon audi.mp3`) and their halftone scans. Drive shows the sources added to the folder on 5 Nov, between about 10:05 and 19:07.
- **Instructions in the user's own Drive file names:**
  - "wolf of wall street clip to be used when he says wolf of wall street";
  - "fiered him push scene punch one. that takes soul out" (`prep_media.py` calls it "the user's "fired" push scene (Doctor Strange)");
  - "Stories from 2008's Great Recession  (a lot of material on stock market bank clips wwall street traders persons)";
  - in the Pinterest folder, "money can be used in difference effect in bg less opacity. bklend" (P10; `prep_media.py`: "falling money (the user's bg blend clip)"). Not followed as written in v5: P10 is darkened under the counter in S16 and in screen blend at 0.55 in S23, never in a difference blend (§5.9);
  - in the Pinterest folder, "2008 8 crash for first kind chess part." (P01, first keyed in `prep2.py`, v2). What it asks for is not recorded (§8.6). The film uses the clip for "premise" (S13); v2 and v3 also used it on "game".

**What was built.** A 93.2 s narrated short, 1920×1080 at 30 fps, in 8 scenes. Cuts are timed to the voice, using Parakeet word times. The goal (SPEC): "the viewer ends on "$10 trillion every single day" feeling Dimon's comeback was inevitable: fired, exiled, back on top."
- **The open:** the Bloomberg news line, cut to "The name of the game in American financial capitalism, is being big and no one is bigger on Wall Street than JPMorgan Chase." (source 1.12–2.68 s plus 5.05–12.53 s).
- **Dimon's own words:** at 23.60–34.85 his Bloomberg answer ("We bank some of these companies in 30 countries … You can't do those things and be small.") replaces the narrator's paraphrase.
- **Captions:** "the Dimon-reel system": Satoshi plus Instrument Serif Italic in warm white with a bloom. One word lands on each spoken onset, with a 3-frame horizontal motion-blur entrance and a cascading exit.
- **Look:** literal B-roll on each spoken noun; halftone print textures on every scene (overlay 42 %, soft light 30 %), and a CRT look on the news inserts; the Doctor Strange palm strike lands on "fired"; a cream Bank One data page, credited in the files to "the AMD reference".

**Rendered:** not recorded.

**Checked:** `check` passed with 0 errors, and more than 90 snapshot frames were looked at. Each audio piece was measured at −16 LUFS, but the mix was "not heard".

**Open after v1:**
- **Music:** none. "Nothing in the Drive is a usable music track, and the HeyGen catalog needs a sign-in."
- **Weakest shot:** "But it was all a premise" over the stock "cool cinematic" collage.

### v2: `a9e958c` "motion-graphics rebuild" (Fri 6 Nov 00:01) and `74e6c6b` "check fixes" (00:16)

**What the user asked for.** REVIEW v2 records only a paraphrase: "The user's verdict on v1: pictures held for 2–3 s with a slow zoom and text in front; no motion graphics and no real animation." SPEC v2 turned this into:
- a goal: "It should play as a motion-graphics documentary, not a slideshow of clips with text on them";
- a ban: "A still with only a slow zoom and a caption standing in for a beat."

**What changed.** The film was rebuilt from scratch in 23 scenes (`s01`–`s23`).
- **Footage:** 134 shots and 73 stills from every source, with a new picture every 1–3 words and negative flashes on the cuts.
- **What each reference gave (SPEC v2):**
  - **Larry Fink reel:** the seal ring with swapping portraits, the punch-in, a name card with a decoding name, the bar write-on, typed giant words, chunk counters, a 2×2 grid, the window zoom-out, face boxes on the Wolf, and falling logos.
  - **AMD reel:** a red marker sweep on the real 1998 NYT "Heir Apparent" clipping, and the cream data page.
  - **RC Media Dario reel:** glow serif, the SUDDENLY echo for "BIGGER" and "COMEBACK", year rollers with floating cards, name glitch frames, and a photo wall.
  - **RC Media Hemant reel:** "Amazon" behind a Bezos cut-out, and a "BIG" word mask with a dive through the letter.
  - **Pattinson edit** (the user's own film, `pattinson-v5/`): Instrument Serif glow with a white flicker box and a bloom, and lines that slide to stay centred.
- **Cleanup:** burned-in subtitles, channel bugs and YouTuber labels were cropped out. The audio did not change.
- **`74e6c6b`:** marked the Bezos cut-out as a deliberate overlap, and added a soft scrim behind "and no one is" over the bright reporter shot.

**Rendered:** not recorded.

**Checked:** `check` was run, and about 150 frames were looked at.

**Open after v2:**
- **Music:** still none.
- **Weakest beats:** "We bank countries" (photo cards of his real meetings) and the stock tunnel shot for "18 months".

### v3: `1ca18f3` "Bloomberg music bed, rebuilt to the references" (Fri 6 Nov 04:46)

**What the user asked for**, verbatim from REVIEW v3 ("The user's notes on v2"):
- "keep the background music of the first Bloomberg clip, continuing for the whole video"
- "sloppy changes"
- "better footage, more photos"
- "edit it exactly like the reference"
- "rebuild it"

**What changed:**
- **Music** (`tools/make_music.py`):
  - Demucs (htdemucs, two stems) separates the Bloomberg open's own music cue (120 BPM, about 53 s).
  - One jump on a downbeat (cue 45.085 to 3.215 s, 80 ms crossfade) makes the cue's own ending land on 93.2 s.
  - The open keeps only the reporter's voice stem.
  - Levels: voice −16 LUFS, music bed −30 LUFS.
- **Cleaner cutting:** no more blurred-fill strips around vertical clips; `tools/check_shots.py` checks that every clip stays inside one source shot, and 13 clips were fixed.
- **More literal footage:** the 270 Park podium, his office, the ribbon cutting, the hard hats, JPMORGAN CHASE & CO. on the glass, Manhattan from straight above, and on "than / JP / Morgan" "the blue CHASE signs, the stone lettering, the etched glass door" (REVIEW v3).
- **More photographs:** an 18-portrait seal ring; "30 Countries" as his real meetings flipping, then a 12-card wall; the World Bank logo on a card; the Bank One / Chase Tower, and his hundreds.
- **New set pieces:** a flip calendar from NOV 1998 to MAR 2000 for "18 months"; the BANK ONE and J.P.Morgan cards merging into JPMORGAN CHASE & CO.; the fallen banks dropping off the page; new cards for the 2004 year roller.
- **Kept:** v2's other set pieces and the Pattinson caption engine.

**Rendered:** not recorded.

**Checked:** `check` passed with 5 samples and the contrast pass off (the full 9-sample run stalls, §7.4). About 60 frames were looked at. Levels were measured but "not listened to".

**Open after v3:** "We bank countries" is still the weakest beat ("a talking shot under the line").

### v4: `127f4c1` "the first 30 s rebuilt to the notes" (Fri 6 Nov 17:49)

**What the user asked for.** REVIEW v4 records the notes mostly through its answers ("Every note from today was checked against the frames"). These fragments are attributed to the user in the files.
- **In the `build4.py` comments:**
  - "game": "a trading picture".
  - "capitalism" (the counting machine): "very good".
  - BIG: "simply there".
  - The flash on BIG: "fine".
  - "in 1998": "fine with Citigroup behind".
  - "mentor": "a montage, no zooming photo".
  - "bigger": "bigger word, echoes much closer, the word simply there".
  - S02, one full sentence (the `sp_freeze_pop` docstring, line 1297): "An interview plays, you pause that picture, and then the picture comes up at the centre with that glow". The docstring names no speaker, but the sentence is addressed to the editor and REVIEW v4 answers it ("Freeze: the interview plays, pauses, and he comes forward with a white glow"), so it reads as the user's S02 note, word for word. v5 replaced that beat with the Hemant stage.
- **The Wolf lockup** (REFERENCES v4): "OF WALL STREET" "in big bold white caps (not yellow, per your note)". `build5.py` keeps it as "(user: not yellow)".
- **S05** ("now runs the biggest bank in the world"): "Unchanged, as asked."
- **S06** ("We bank…"):
  - The interview is the base for the user's lines ("Lines: exactly yours"), captioned as in the we-bank reel.
  - The Fink reel's Rogan screen, "from your screenshot", with the user's globe picture behind Dimon.
  - Dimon is matted out of the interview. REFERENCES v4: "at your note he is matted out of the interview frame by frame (the local matting model) and sits on his own layer above the picture. It only touches the curtain behind him, never him."
- **Also answered in REVIEW v4:** drop "especially American financial capitalism" from the open, and hold "bigger"; remove v3's "square" (a shadow on an untimed wrapper) and the same shadow on the s13 "premise" card; reframe the "and no" crowd shot ("a dark building column at its left edge had read as a black bar"; `build5.py` keeps that crop, but its comment no longer gives the reason, §3.2); put captions beside the subject; use real video only in S03, and use the user's new assets. Whether the user raised the crowd shot is not recorded.
- **Assets the user added to the Drive folder that afternoon** (Drive creation times, 16:25–17:23): `jp morgan montage.mp4`, `bill ackman metro medi ref.mp4`, `was fired part ref.mp4`, `wolf of wwall street vid.mp4`, `over a bonus.mp4`, `money asset.mp4`, `we bank countries part.mp4`, `J P Morgan The Man Who Bought America   Full Documentary.mp4`, `jamie ghost image.webp`.

**What changed (0–31.7 s only).** After 31.7 s the film is "v3's edit with v4's fonts and no slide".
- **The open, re-cut** (in `tools/make_music.py`, which v4 changed: src 1.12–4.05 + 6.85–9.62 + 0.5 s silence + 9.62–12.30): "The name of the game in American capitalism, is being big, and no one is bigger [0.5 s held] on Wall Street than JPMorgan Chase."
  - The reporter's soft "than" had ended up in the music stem; it was taken back.
  - Word times were re-measured on the new track (in v3 the first words came about 0.5 s early).
- **Type:** across the whole film, only Inter Tight (in the Helvetica role) and Instrument Serif regular with glow; no Satoshi and no italics; words land in their final place, and lines no longer slide. One font family per line applied to 0–31 s only, with exceptions (REVIEW v4: "the Helvetica-over-serif stack is gone from 0–31 s, except where the we-bank reel itself mixes them ("in 30 countries", "We bank / Countries")"). The committed v5 film has six lines that mix the two: s02's "man in America" and "right now" (v5, copying Hemant's "small sans words plus one big serif word"), s06's "in 30 countries" (the we-bank exception), and, after 31.7 s, "in the world" (s08), "crisis hit" (s19) and "every single day" (s23).
- **S01:**
  - The NYSE trading floor on "game", and "in American capitalism" as one serif lockup.
  - BIG simply there, with the negative flash.
  - "bigger" as Dario's SUDDENLY: 340 px with glow, close echoes, corner squares, one glitch frame and a tiny copy.
  - "on Wall Street" lands word by word in big serif.
  - JPMORGAN CHASE is typed like Dario's DISAPPEAR over the J.P.Morgan flag and tower: "over JPMorgan pictures only (the J.P.Morgan flag, the JPMorgan tower). There is no Chase sign." (REVIEW v4). This replaced v3's blue CHASE signs on "than / JP / Morgan"; `build4.py` and `build5.py` both still say "over JPMorgan pictures only".
  - Dimon pops up "from the centre" as the Pattinson glow cut-out.
- **S02:** Hemant Taneja's opening: a grey-then-cream glowing silhouette with live frames flashing through, "This is the most" on the left and "influential" on the right. The interview freezes and he comes forward with a glow. The presidential seal rises behind his head, and five photo cards land, each after a white box.
- **S03:** real video only: the podium, Stanford, and him walking in (from the user's montage). The Ackman lockup "OF WALL STREET", with a motion blur on each word, over the user's Wolf dollar-bill shot (slowed to 0.72× by the player). Face boxes and a purple inverted exit frame.
- **S04:** the was-fired reference's paper page with three young-Dimon photos; Sandy Weill wide on "by his own", then a three-shot montage for "mentor"; a faster four-square with the user's money asset; the user's "over a bonus" cartoon, with its watermark cropped; the grudge photo pans until his daughter is in it.
- **S06 (23.6–31.6 s):** one continuous interview take (REVIEW v4: "it is 1080p, not 4K"), captioned in the user's chunks. The globe picture sits in a difference blend at 0.5 opacity on the right, with quote marks. Dimon is matted above it.
- **New `REFERENCES.md`:** frame-by-frame breakdowns of each reference, from dense contact sheets and Parakeet transcripts: Hemant (0–1.7 s, 22–25.5 s); Dario (SUDDENLY 16.6–17.6 s, DISAPPEAR 36.6–37.4 s); Ackman (4.3–7.0 s); the "was fired" reel, a Jan Koum / WhatsApp reel (0–1.9 s); the we-bank reel; and Fink at 4–5 s. Plus a table of the user's assets and where each is used.

**Rendered:** `renders/jpm-dimon-v4-0-31.mp4`, 0–31.7 s, ending on "…the United States government."

**Checked:** `check` passed (5 samples, contrast off), and about 110 frames across 0–31.7 s were looked at.

**Open after v4:**
- **"You have to be big…" (31.7–34.85 s):** "it still follows your lines". Dropping it would shorten the film by about 3 s, and the music bed, timed to end on the last frame, would need re-cutting.
- **The "was fired" reference** is used for "a guy who got fired". Was it meant for "he was fired" at 48 s instead?

### v5: `292806f` "every note on v4, matched to the references frame by frame" (Fri 6 Nov 19:54), the latest

**The user's notes on v4, and what v5 did.** The notes column is REVIEW v5's condensed wording; the user's full wording is not in git.

| Note on v4 (as REVIEW.md records it) | v5 |
|---|---|
| "in American" written small | "Back as it was": "in American" small above, "capitalism" in big serif below. |
| "bigger" not animated like Dario; darker; echoes moving; no small copy; more echoes at the sides | Dario's SUDDENLY, frame for frame. A corner square top left, then bottom right, and two glitch frames. The word with its glow on near-black. Rows of faint, blurred echoes rush in and slow down (top row to the left, bottom row to the right), and faint side copies drift outward. No small copy. |
| JPMorgan Chase not like DISAPPEAR; spelling | "JPMorgan Chase" in mixed case, 420 px, condensed to 0.7, about 84 % of the frame width. It is typed in place on the reporter's syllables, and the newest letter flares. The flag cuts to the tower mid-word, and two tile-glitch frames take the word out. |
| Dimon came in from the side, zooming | His talking video, matted, with the glow, slides up from the bottom in 10 fps steps until he stands where the next scene's silhouette stands. No zoom. |
| "most influential man in America": a video of him, mask glow, pops up, photos at his sides like Hemant; subtle zoom on his face on "in America"; fonts misaligned | Hemant's opening: a see-through grey silhouette, the live strip, white bars, the band through "influential", and two text sizes on one baseline. Then Hemant's 22–25 s layout on Dimon's talking video: a defocused copy of his own shot behind him, and borderless cards landing behind him after soft white boxes (red boxes swap two). A slow push on his face from "in America", the seal behind his head, and a white sweep out. |
| Textures too heavy; use CRT lines and noise, lighter | Across the whole film, the grunge and paper overlays drop from 0.40 / 0.28 to 0.10 / 0.04 (0.05 / 0 on the interview scenes). Noise comes from the registry grain overlay at 6 % (`compositions/grain.html`), "as in the Pattinson film". CRT lines come from the grades, "a bit lighter than Hemant's". |
| "He's basically the CEO of Wall Street": Pattinson-style smooth transitions, and the move from "CEO" to "of Wall Street" | "the" (Stanford) arrives still moving. "CEO" eases back into a window with photo cards popping out behind it. An inverted frame, then the Wolf arrives moving. The words blur in place, a punch-in, then a purple frame and a white frame. (REFERENCES.md and the `build5.py` header also list Ackman's block glitch into the Wolf; the committed `s03.html` does not have it, §8.3.) |
| The Wolf shot looked cut | One continuous shot, "cut after the house frame" (REVIEW v5): it starts at source 12.40 s of the landscape copy (`prep5.py`), so keep that in-point if the Wolf is retimed. It is slowed to 0.77× by motion interpolation (`wolf_slow.mp4`). In v4 the player did the slowing, which repeated frames unevenly and read as a jump at 14.37. |
| The fired photos cut his face; wrong pictures | Three 1990s documentary photos of young Dimon, cropped square on his face by face detection. The black-and-white portrait is the hero. The page pushes in 1.3× after FIRED. |
| "By his own mentor" like Dario's "every AI tech bro" | Eight photos of Sandy Weill, each aligned so his face sits within 15 px of the same point, with zoom-blurred edges. A new photo every 2–3 frames, behind four fixed white lines, with the words building at nose height. Then the four-square comes in dark for one frame. |
| "and a family" / "grudge" at the bottom | Both centred. |
| "now runs the biggest bank in the world": no change | Unchanged (only the lighter texture). |
| "We bank": textures, quote marks closer, B-roll mixed in, the ghost behind him moving like Fink's | Interview and B-roll alternate: the JPMorgan Global China Summit and Davos, London from the air, the World Bank building, Obama, and Congress. The globe ghost slowly zooms and drifts, and pulls focus each time we cut back to him. The quote marks hug the words. (REFERENCES.md and the `build5.py` header also list Fink's glitch boxes, a glint and a white-block wipe before "the IMF"; the committed `s06.html` has none of them, §8.3.) |

**The same notes in fuller form,** from the comments in `build5.py`:
- `sp_suddenly` ("bigger"): "User: much darker; more echoes, fainter, blurred, moving, also at the sides; no small copy; the word keeps its glow."
- `sp_type_word` ("JPMorgan Chase"): "User: "JPMorgan Chase", spelt properly, not in capitals."
- `sp_slide_pop`: "User: Dimon slides in from the bottom at a low frame rate with the cut-out glow -- his talking video, matted -- until he stands exactly where the next scene's silhouette stands (hands in frame); no zoom, no side entry."
- `sp_hemant_stage`: "User: a subtle push on his face on "in America" while everything else holds; the presidential seal behind his head."
- The Hemant CRT grade: "CRT lines over the frame (a little lighter than the reference, per the user)".
- S01: `"in American" as before (user)`. S04, "and a family": `user: in the centre`.
- The S06 scene: "User: the interview as the base for "We bank some of these companies in 30 countries. We bank countries, we bank the World Bank, the IMF, ... the United States government", cutting to B-roll and back (interview, B-roll, interview, B-roll ...); the captions as in the we-bank reel; the Fink reel's Rogan screen: his globe picture behind him (he is matted above it), low opacity, slowly moving and pulling focus; the quote marks close to the text."

**References re-watched** "at the moments you named". Two frame-by-frame passes were added to `REFERENCES.md`, each at the reference's own frame rate:
- **Hemant:** 0–1.9 s and 20.0–25.6 s.
- **Dario:** SUDDENLY (16.45–17.75 s), DISAPPEAR (36.3–37.9 s), and "every AI tech bro" (17.40–18.40 s).
- **Ackman:** 4.2–7.3 s.
- **The was-fired reel:** 0–1.95 s.
- **Fink:** 3.0–6.8 s, with the ghost picture's movement measured by feature tracking.
- **The user's own Pattinson film:** 5.30–9.10 s (the "generational run" transitions).

**Assets added to Drive between v4 and v5:** `Copy of hemant taneja vid.mp4` and `Copy of dario vidoe.mp4` (18:20), and the folder `sandie weil images` (18:36).

**New tools:** `tools/prep5.py` (mattes and glows, smooth slow motion, face-aligned Weill photos, young-Dimon squares) and `tools/faces.py` (OpenCV face detection). The registry `grain-overlay` component was installed.

**Rendered:** `renders/jpm-dimon-v5-0-31.mp4`, 0–31.7 s.

**Checked:** `check` passed with 0 errors (5 samples, contrast off). About 110 frames were looked at, side by side with the references where that applies. Levels were measured but "not heard".

**Open after v5:** see §8.

---

## 5. References and watch-video breakdowns

This section draws on `jpm-dimon/REFERENCES.md` (v5, `292806f`) and its v4 version (`git show 127f4c1:jpm-dimon/REFERENCES.md`); the Fink breakdown (`git show 18142fc:dimon/reference/FINK_REEL_REFERENCE.md`); `SPEC.md` and every `REVIEW.md` in git; `jpm-dimon/tools/build5.py` and the prep scripts; the committed `compositions/*.html`, which give the film times; and a read-only check of the Drive folder and the downloaded files on 9 Nov 2026 (file specs measured with ffprobe on the downloads).

### Where the breakdowns are kept
- **`jpm-dimon/REFERENCES.md`:** breakdowns of Hemant, Dario, Ackman, "was fired", "we bank" and Fink at 4–5 s, then "Frame-by-frame pass (v5)" and "Second frame-by-frame pass (v5)"; the second pass also measures our own Pattinson film. The file was first written in v4, and v5 added the two passes.
- **Larry Fink reel:** `git show 18142fc:dimon/reference/FINK_REEL_REFERENCE.md` (347 lines, shot by shot), `dimon/reference/fink_words.json` (word timings) and `dimon/reference/frames/` (27 contact sheets and stills). It was written for the separate `dimon/` build, and both builds use it. That build later added a §11, "What makes it read as animation", on `claude/stoic-mccarthy-hijqav` (`0b01d42`).
- **What each reference gives, as one list:** the Quick map below and the "Reference imitated" column of §3.1. SPEC.md's "References and what each gives" (written in v2, `a9e958c`, unchanged since) is the v2 list and out of date (§6.4).
- **The code for each device:** `jpm-dimon/tools/build5.py`, in functions named after the reference (named in each section below); `tools/faces.py` for face alignment; `tools/prep5.py` for mattes, halos and smooth slow motion; `tools/prep4.py` for the ghost picture.

### How they were watched
- **Fink:** every second at 10 fps and every animated beat at 30 fps. Camera moves were measured with feature tracking.
- **v4:** dense contact sheets (the first 15 s at 15 fps, key beats at full resolution, the rest every 2–3.5 s) and a local Parakeet transcript of each reel.
- **v5:** every frame at each reference's own rate, at the moments the user named. A second pass then measured the full-resolution frames.

### Caveats
- **Only Fink's material is in git.** Only the Fink frames and word timings were committed. The contact sheets and transcripts behind the other breakdowns were not; re-extract them from the Drive files.
- **The measurements only cover 0–31.7 s.** The v4 and v5 passes measured beats in film 0–31.7 s, the part those rounds rebuilt. The set pieces after 31.7 s date from v2/v3, and apart from the Fink document no measurements were written down for them.
- **Four frame-rate labels are wrong.** In REFERENCES.md's first v5 pass, titled "every frame at each reference's own rate", both Dario headings say "24 fps" (the file is 25 fps), the Fink heading says "25 fps" (the file is 30 fps), and the "Hemant, 21.8–25.6 s" heading says "12 fps" (the file is 23.976 fps). Use the times in seconds.
- **The references are for style only.** SPEC.md bans "The Larry Fink clip itself (it is a style reference only)". The v1 review records "the Larry Fink clip (the user said it is for someone else)".
- **Only Fink has an original link.** The Fink reel is Instagram reel `Dewt0XXoHtk`. For every other reference the Drive copy is the only source.
- **The user's general notes on following the references** ("edit it exactly like the reference", and the rest) are in §4; the standing rules are in §6.

### Quick map

| Reference | Drive file | File specs | Where it is in the v5 film |
|---|---|---|---|
| Larry Fink reel (Metro Media House) | `larry fink metro media house.mp4` | 1276×718, 30 fps, 85.1 s (85.0 s in the breakdown) | Pace and negative flashes throughout; S02 seal 11.13; S03 face boxes 13.79; S04 2×2 grid 18.41; S06 "Rogan screen" 23.60–31.55, window zoom-out 34.44; S07 name card 34.85; S10 bar write-on 47.76 / 49.50, punch-in 48.65; S11 flip calendar 50.81; S12 style strobe 53.44; S14 / S23 typed words 62.08 / 90.86; S16 / S23 chunk counters 67.61 / 88.62; S18 logo cards 75.42; S22 falling cards 85.11 |
| Dario Amodei reel ("RC Media 11.3") | `Copy of dario vidoe.mp4` | 1920×1080, 25 fps, 83.9 s | S01 BIGGER 4.96–6.16; S01 "JPMorgan Chase" 7.23–8.50; S04 "by his own mentor" 17.02–18.41; year rollers 16.20, 46.16, 76.41, 78.24; S13 "comeback" 59.56 and the archival wall 60.12–62.08 |
| Hemant Taneja reel ("RC Media 10.4") | `Copy of hemant taneja vid.mp4` | 1920×1080, 23.976 fps, 65.7 s | S02 9.05–12.37; S01 BIG word mask 3.45 and slide-up glow 8.60; S12 "Amazon" behind Bezos 56.35; the CRT lines |
| Bill Ackman reel (Metro Media House) | `bill ackman metro medi ref.mp4` | 1276×718, 25 fps, 95.0 s | S03 12.37–15.07 |
| "Was fired" reference (Jan Koum / WhatsApp reel) | `was fired part ref.mp4` | 1276×718, 25 fps, 86.9 s | S04 15.07–16.20 |
| "We bank countries" reel | `we bank countries part.mp4` | 720×1280 (vertical), 29.97 fps, 57.7 s | S06 captions 23.60–31.55, and the v1 caption system |
| AMD reel | not in the Drive folder; source unknown | — | S08 headline sweep 39.16–42.84; S17 data page 70.73–74.50 |
| Our own Pattinson film | not in the Drive folder; it is `pattinson-v5/` in this repo | — | S03 transitions 12.83–13.72; the caption glow; the 6 % grain |

### 5.1 Larry Fink reel (Metro Media House): the main style reference

**What it is.** A Metro Media House reel about Larry Fink. It opens: "Donald Trump is not the President of America. This man is." Its parts are a hook backed by an outside voice, the name reveal, a paradox, rise, fall, comeback, crisis irony, a payoff in hard numbers, and a closing line that calls back to the hook. The breakdown also proposed a nine-beat template for Dimon (its §10), but the film follows the user's own voiceover.

**Measured** (FINK_REEL_REFERENCE.md; to convert its pixel sizes to 1080p, multiply by 1.504):
- **Pace:**
  - 233 hard picture changes in 85 s.
  - Real shots: median 0.45 s, mean 0.58 s, middle half 0.29–0.63 s.
  - Only designed type beats hold: the quote panel 3.4 s, the longest 3.5 s.
  - A new picture on almost every 1–3 words, with a literal picture for each key noun.
  - Voiceover about 150 words a minute.
- **Camera:**
  - Almost static: a shot changes scale by only 1.00–1.02.
  - Hard punch-ins to a 1.3–1.6× crop at 3.33, 39.23 and 56.47.
  - Pushes: +5 % in 0.55 s on the NYSE, +19 % over 1.3 s on the eye.
  - One sideways pan at about 500 px/s.
- **Type:**
  - One tight bold grotesque, close to Inter Tight 700 for captions and 800 for heroes, tracking −0.02 to −0.035 em. No serif, no commas or full stops.
  - Line captions about 56 px at 1080p, centred at 0.505 of the frame height, 1–4 words.
  - Each line is laid out once in its final place, and each word cuts on in place on the frame it is spoken.
- **Bar write-on (ref 25.53–27.6):**
  - Each word first shows as a solid white bar (the word's width by its cap height) and flips into the word in one frame.
  - A white bar then sweeps the line away, left to right, in 3–4 frames.
- **Hero lockups:**
  - A 125–230 px hero word with a 40–56 px context word.
  - Numbers grow in chunks ($100 → $100,000 → $100,000,000), left-aligned at 10 % of the width.
  - Years roll 2000 → 2005 → 2007 → 2008.
- **Typed giant words (300–600 px, strong glow):**
  - A character every 1–2 frames, each going dark grey to white over 2–3 frames (#666 → #aaa → #eee).
  - The camera jumps to a new framing about every 0.3 s.
- **Name reveal:**
  - "Larry Fink" decodes letter by letter in random order, pale to black over about 8 frames, under a giant pale outline of the name.
  - The card shrinks from about 60 % to 35 % of the width in about 0.35 s.
- **Transitions:**
  - Negative (colour-inverted) flashes of 1–3 frames at cuts, about 22 times, every 3–4 s.
  - One-frame white flashes.
  - A window zoom-out, 100 % → 59 % in 0.55 s, easing out (33.6–34.15).
  - A 2×2 grid filling one cell at a time (27.67–28.5).
  - A style strobe: one picture in six looks, 2–3 frames each (41.4–42.67).
  - HUD wireframes.
  - Purple face-detection boxes labelled "person" on The Wolf of Wall Street.
- **Sound:** a continuous dark, bass-heavy music bed (about −22 dB between sentences) plus SFX hits.
- **The "Rogan screen" (ref 3.80–7.77):** the user sent a screenshot of this moment. A podcast host sits on one side; a dim black-and-white ghost of Fink holding a glowing globe sits on the other, with big quote marks around a stacked caption.
  - First v5 pass:
    - 3.72: an inverted frame; 3.76: a white frame.
    - 3.80: the screen appears, with the quote marks there from the first frame.
    - 4.00–4.08: small white glitch boxes by the top quote mark.
    - 4.28–4.40: a 4-frame star glint on the glasses in the picture.
    - 4.24–5.20: the words fade in.
    - 5.92–6.00: a white inverted-block wipe across the frame (left, middle, right).
  - Second pass: the ghost zooms in 10 % over 2.3 s, drifts left and up, and pulls focus from soft to sharp (sharpness 17 → 228 by 6.0 s).

**In the film (v5)**
- **S06 23.60–31.55, the Rogan screen** (`sp_ghost`, `sp_quotes`; the beat-by-beat is in §3.2):
  - The base is Dimon's Bloomberg interview, one take (source 273.05–281.0).
  - Behind him on the right is the user's globe picture, turned into `assets/img2/globe_ghost.jpg` by `prep4.py` (grayscale, box x 800–2020). In this session the picture is `jamie ghost image.webp`; the old session's files do not name it (§8.6).
  - It sits in a difference blend at 0.45 opacity (0.3 s fade-in) and zooms 1.0 → 1.12 while drifting (−110, −36) px over the whole stretch. That is slower than the reference's 10 % in 2.3 s.
  - It pulls focus (blur 13 → 1 px in 0.85 s, power2.out) at 23.60, 26.45, 27.75 and 28.80, each time the edit cuts back to him.
  - Dimon is matted (`BANK_27305_820_x63_50_135_cut.webm`) and sits above the ghost.
  - Quote marks (Inter Tight 800, 210 px, opacity 0.92) hug each caption block while the interview is on screen.
  - The reference's glitch boxes, glint and white-block wipe are not in the committed film (§8.3).
- **S06 34.44, window zoom-out on "small"** (`sp_window`): to 16 % in 0.38 s, power3.out.
- **S02 11.13, the seal:** the presidential seal (PNG from the Pinterest folder) rises behind his head, opacity to 0.62 and scale 0.94 → 1 in 0.24 s. Built from the user's note "the presidential seal behind his head".
- **S03 13.79 / 13.89, face boxes on the Wolf:** purple boxes "person 0.97" and "currency 0.94" (3 px #B455FF), each with a one-frame flicker.
- **S04 18.41–18.74, the 2×2 grid** (`sp_grid4`): a cell every 2 frames, each with a one-frame white flash. v4 made it faster (REVIEW v4: "faster (cells every 2 frames), with your money asset in the top-right cell in place of the money falling on black").
- **S07 34.85–36.76, the name card** (`sp_name_card`):
  - A white frame, then a black-and-white cut-out of Dimon on a blue card that settles from 1.65× to 1.0 in 0.36 s (power3.out). The reference card is red.
  - "Meet" (48 px) appears at 35.25.
  - "Jamie Dimon" (Inter Tight 800, 118 px) decodes in a fixed random order, a letter every 0.035 s. Each letter goes pale, then grey (+3 frames), then black (+6 frames), under a 330 px outline of the name.
- **S10, bar write-on and punch-in** (`sp_bars`):
  - "But then" at 47.76–48.42 and "he was" at 49.50–49.91, in Inter Tight 700 at 110 px. The exit sweep takes 3 frames.
  - At 48.65, a hard punch-in to 1.45× on the young Dimon at "42".
- **S11 50.81–53.02, flip calendar** (`sp_calendar`): NOV 1998 → MAR 2000, a page every 2 frames, landing at 52.18.
- **S12 53.44–54.07, style strobe** (`sp_strobe`): the boxing gloves in six looks (documentary, halftone, two-ink, mono-screen, dither, print), alternating 3 and 2 frames, with a punch to 1.35× at 53.54.
- **Typed giant words** (`sp_typed`): "In 2000" in S14 (62.08–62.91) and "Today" in S23 (90.86–91.81).
  - A character every 0.055 s, going #5c5c5c → #a8a8a8 → white over 2 frames.
  - In S14 the camera jumps 1.5× → 1.15× (+0.23 s) → 1.0 (+0.47 s).
- **Chunk counters** (`sp_counter`):
  - S16 67.61–68.69: $60 → $60,000 → $60,000,000.
  - S23 88.62–89.99: $10 → $10,000,000 → $10,000,000,000,000, over the screen wall.
- **Logo cards:**
  - S18 75.42–76.41: the Bank One and J.P. Morgan cards merge into JPMorgan Chase & Co.
  - S22 85.11–86.11: the fallen banks' cards drop off the page. v2 listed this as "logos falling".
- **Negative flashes** (1–2 frames, on cuts that change world): 3.45 (BIG; "the flash (user: fine)"), 13.69, 19.62, 21.60, 39.16, 40.28, 43.32, 48.42, 49.96, 55.46, 56.35, 62.91, 64.28, 69.56, 78.88, 80.31, 80.68, 81.05, 84.30, 91.81.
- **White flashes and frames:**
  - Flashes on "fired" (49.84), the boxing punch (53.44), "hit" (79.73) and "standing" (83.10).
  - One-frame white frames at 15.03, 34.85, 44.52 and 70.73.
- **No longer in the film:** the seal-ring opening (portraits swapping inside the ring, a glint, rays, HUD) and the seal punch-in, both used for "the most influential man" in v2/v3. v4 replaced them with the Hemant opening. The "mortgages" photo flip collage is also gone. Their functions are still in `build5.py` but are not called.
- **Never built:** the animated AI image-to-video portrait (an open item in the Fink document) and the donut charts around the eye.
- **Music:** the film uses the Bloomberg open's own music, at the user's request, not anything from this reel.

### 5.2 Dario Amodei reel ("RC Media 11.3")

**What it is.** An RC Media reel about Dario Amodei. Three moments are used: SUDDENLY (ref 16.56–17.40), "every AI tech bro" (17.40–18.40) and DISAPPEAR (36.60–37.64). In v2 it also supplied a glowing serif, a year counter ("Dario's 2023"), name glitch frames and a photo wall ("the lead").

**Measured** (REFERENCES.md: v4 and both v5 passes)
- **SUDDENLY:**
  - 16.60–16.64: a white square (about 215 px) in the top-left corner of the outgoing shot; 16.68: one in the bottom-right.
  - 16.72: a glitch frame, with the word smeared vertically through a pale band and the echoes already rushing.
  - 16.76: a glowing white bar with the crisp black word.
  - From 16.80: near-black ground (brightness 4/255); the white uppercase serif word at 55 % of the frame width; giant blurred echoes cropped at the top and bottom (brightness about 84 and 66, roughly 30 % white).
  - Echo motion: the top row moves left and the bottom row right. About 240 px a frame through the glitch frames, then 30–34 px a frame slowing to 2 px a frame by 17.30.
  - A hard cut at 17.40.
  - The v4 pass also notes a tiny copy under the right end, and that the word "is simply there, with no fly-in".
- **"Every AI tech bro":**
  - A different face every 2–3 frames (3, 2, 3, 2 …): five people, cycled twice.
  - Faces centred within 15 px of (960, 505), 390–830 px tall (36–77 % of the frame height). Each photo creeps in 2–3 %.
  - A sharp circle of about 250–300 px around the face, zoom-blurred outside it.
  - Four thin white lines stay fixed on screen: top and bottom at x 770–1230 (y 194 and 730), sides at x 714 and 1280 (y 270–640).
  - The text is small white serif (about 56 px) at nose height, left edge at x 674, centre y 572, building word by word.
  - Out: the next scene comes in dark for one frame (18.40 → 18.44).
- **DISAPPEAR:**
  - A letter about every 2 frames on the spoken word (v4: about 0.055 s a letter), typed into its final centred layout from the left, so the word never re-centres.
  - The newest letter flares for 1–2 frames; earlier letters stay crisp white with a soft dark shadow.
  - Cap height 384 px (36 % of the frame); the word spans 78 % of the width; letters are about 0.7 as wide as Instrument Serif's.
  - The footage cuts mid-word (36.88). The word holds about 0.35 s and leaves through two frames of tile glitch.

**In the film (v5)**
- **S01 4.96–6.16, "bigger" as SUDDENLY** (`sp_suddenly`):
  - Squares at 4.96 (top-left, 216×208 px, 2 frames) and 5.03 (bottom-right, 1 frame).
  - Glitch frames at 5.06 (smeared word in a pale band) and 5.09 (black word in a glowing bar).
  - "BIGGER" (Instrument Serif 340 px caps, glowing) blooms at 5.13 and is crisp by 5.23, on #020202.
  - Rows of three "BIGGER" at 520 px (opacity 0.30 / 0.24, blur 9 / 11 px) rush from ±460 to ±40 px in 0.85 s (expo.out) and keep drifting: top row left, bottom row right.
  - Faint side copies (0.17, blur 7 px) drift outward. There is no small copy.
  - The word holds 1.1 s over the held voice.
- **S01 7.23–8.50, "JPMorgan Chase" as DISAPPEAR** (`sp_type_word`):
  - Instrument Serif 420 px, squeezed to 0.70 of its width (about 84 % of the frame).
  - Letters land at 7.28 and 7.42 (J, P), then every 0.062 s from 7.61 ("Morgan") and every 0.066 s from 7.97 ("Chase"). Each newest letter blooms, going blur 9 → 3 → 0 px over 2 frames.
  - The picture is the J.P.Morgan flag, cutting mid-word at 7.92 to the JPMorgan tower at dusk. Both come from the user's montage, in smooth slow motion. JPMorgan pictures only, with no Chase sign (v4, replacing v3's CHASE signs).
  - Tile exit: at 8.43 light-blue tiles invert parts of the word; at 8.47 tinted blocks cover the frame and the word is gone. The tower holds until Dimon slides up at 8.60.
- **S04 17.02–18.41, "by his own mentor" as "every AI tech bro"** (`sp_dario_faces`, `faces.dario`):
  - Eight photos of Sandy Weill: two from the user's `sandie weil images`, five frames from the Most Powerful Banker documentary (772, 861, 441, 714, 889 s) and one portrait from the image pack.
  - Face detection places each face at (960, 505), 560–700 px wide, with the edges zoom-blurred around a sharp circle.
  - A new photo every 3 / 2 frames (17 changes cycling the eight photos), each creeping in 3 %.
  - The four lines sit at exactly the measured positions.
  - "by" 17.07, "his" 17.29, "own" 17.47, "mentor" 17.77, in 56 px serif at x 674, y 572.
  - Then the four-square comes in dark for one frame (18.41).
  - This replaced v4's three-shot montage ("mentor": "a montage, no zooming photo"). Some Weill photos are small, so the biggest close-ups are soft (§8.1).
- **Year rollers** ("Dario's 2023", `sp_roller`):
  - Glowing Inter Tight 800 digits at 330 px. The steps slow down as they approach the landing year. The first two digits of that year invert on frames 6, 8, 10 and 11. Photo cards drift in the dark.
  - S04 16.20–17.02: 1990 → 1998 over Citigroup footage (v4 note: "fine with Citigroup behind").
  - S09 46.16–47.76: 1982 → 1998, plus "16 years".
  - S18 76.41–77.67: 2000 → 2004.
  - S19 78.24–78.88: 2004 → 2008.
- **S13 59.56–59.86, "comeback"** (`sp_echo`): the v2 version of SUDDENLY. One inverted frame, then the word between drifting blurred echoes.
- **S13 60.12–62.08, "the history of Wall Street"** (`sp_wall`, Dario's "the lead"):
  - 24 black-and-white archival tiles (6 × 4) land in random order over 0.55 s, with a one-frame white flash on every third tile.
  - The wall pushes in 1.0 → 1.1, with a dark centre behind the words.

### 5.3 Hemant Taneja reel ("RC Media 10.4")

**What it is.** An RC Media reel about Hemant Taneja (General Catalyst), opening "This man is the modern day…". Two parts are used: its opening (ref 0–1.67) and his stage layout (ref 20.0–25.6). In v2 it also supplied a giant word behind a cut-out ("EUDIA") and a word cut out of the footage.

**Measured**
- **Opening (24 fps):**
  - He is a flat silhouette with a soft glow over his darkened stage. It is light grey and see-through at first (about 85 %; his face and hands show faintly), then opaque cream from 0.67.
  - His live picture shows through at 0.125 (1 frame), 0.375–0.42 (2), 0.875 (1), 0.958 (1), 1.21–1.29 (3) and 1.54–1.58 (2).
  - Glitches: 0.33, a strip of the live frame crosses the silhouette at mid-height; 0.375–0.42, white blocks; 0.46–0.54, a white vertical bar and a dash beside "is the".
  - Words: "This" 0.125, "man" 0.25, "is the" 0.50, "modern" 0.92 (blurring in), "day" 1.21.
  - Two sizes only, about 90 and 200 px. "This **man** / is the" sits left (baseline about y 370) and "**modern** / day" right, both clear of the head.
  - 1.46–1.50: a white band through "modern day", with the word dark and offset inside it.
  - 1.67: a hard cut to black, where photo cards pop around the centre name. A white box marks each card's spot 1–2 frames before it lands.
- **Stage (every frame, 24 fps):**
  - 21.375–21.417: two frames of his blazing white silhouette. 21.458: a cut to him talking.
  - He is matted and sharp, head top about 110 px, centred, over a heavily blurred light-grey copy of the stage. Subtle CRT lines run over everything (about 10 px apart).
  - Four borderless photo cards sit behind him: two at head height (top-left about 356–890 × 240–536, top-right about 1156–1590 × 260–504) and two at the waist.
  - Each card lands one frame after a soft glowing box at its spot (21.88, 22.05, 22.30).
  - Red boxes swap two cards at 23.88 and 24.92 (the first pass says 24.88).
  - One line runs across his chest (centre y about 616): small sans words plus one big serif word.
  - Out at 25.08: a white band sweeps in from the left. The first pass instead says the frame defocuses at 25.05.

**In the film (v5)**
- **S02 9.05–10.70, the opening** (`sp_hemant_open`), on Dimon's talking video (`jamie dimon speaking video.mp4`):
  - A freeze at source 12.65 is matted into a cream silhouette with a glow.
  - It is grey and see-through (0.86) until 9.730 and opaque from 9.763 (the code's `grey_until=9.55`; see §3.2).
  - Live frames at 9.15 (2 frames), 9.41 (2), 9.73 (1), 10.00 (2), 10.28 (1) and 10.52 (3).
  - The live strip at 9.40; white blocks at 9.43, 9.47, 9.50 and 10.01.
  - "This is the **most**" sits left (80 / 180 px serif) and "**influential**" right (180 px), on one baseline (y ≈ 380; the lockup is centred on y 330).
  - 10.50: the band through "influential" (2 frames), with the word dark and offset inside it while the white word blinks out.
- **10.70–10.77:** the blazing silhouette, for two frames (`sp_sil_flash`).
- **10.77–12.37, the stage** (`sp_hemant_stage`):
  - His talking video, matted with a halo and CRT lines, over its own heavily defocused copy.
  - Cards from the user's montage land after soft glowing boxes, at exactly the measured spots: the Fortune cover at 10.86 (top-left, 534×296), Congress at 11.00, the White House at 11.20 (top-right, 434×244) and the press scrum at 11.40.
  - Red boxes swap two of the cards at 11.63 / 11.70.
  - The seal appears behind his head at 11.13.
  - A push on his face from 1.0 to 1.08 runs 10.97–11.61 ("in America") while everything else holds.
  - "man in **America**", then "right **now**", run across his chest (60 px sans + 126 px serif, y 650).
  - The white sweep out at 12.27 (3 frames, `sp_white_wipe`).
- **S01 8.60–9.05, the slide-up** (`sp_slide_pop`): the same matte-and-halo look, moving in steps every 3 frames: y 1080 → 560 → 230 → 60 → 0. v4 used the glow cut-out pop from this reel here; v5 changed it at the user's note.
- **S01 3.45–4.03, BIG** (`sp_big_static`): the skyscrapers seen through a giant "BIG" (Inter Tight 800, 1000 px), with a 2-frame negative flash. v2 also dived through the letter; that dive was removed at the user's note ("big: simply there (user)").
- **S12 56.35–57.76, "Amazon" behind a Bezos cut-out** (`sp_text_behind`, "Hemant's EUDIA"): Instrument Serif 470 px with a glow. It comes out of a blur in 0.25 s, then drifts slowly behind him. A 2-frame negative flash on the cut.

### 5.4 Bill Ackman reel (Metro Media House)

**What it is.** The transcript as recorded in REFERENCES.md:
- 0.1: "This is the investor every CEO in America is afraid of."
- 4.2: "And he's basically the real Wolf of Wall Street."
- 7.0: "The real question is this, was all this legal?"

The "real Wolf of Wall Street" lockup is the part used.

**Measured** (ref 4.2–7.3, every frame at 25 fps)
- 4.28–4.60: white boxes wipe the background from Apple Park to a glass wall, while "And he's basically" sits small and spread across the frame at mid-height over his cut-out with devil horns.
- 4.92: the cut-out drops away.
- 5.24–5.36: a 4-frame block glitch (inverted, pink-tinted panels) into the clean Wolf shot (Leo, arms spread).
- 5.52–6.24: "THE", "REAL", "WOLF" / "OF", "WALL", "STREET" each come out of a blur in place over about 3 frames, in big bold condensed caps, with line 2 smaller.
- Hold: a slow push, then a punch-in at 6.92.
- Exit: 6.96 a purple inverted frame, 7.00 one white frame, 7.04 the next shot.

**In the film (v5), S03 12.37–15.07** ("He's basically the CEO of Wall Street"; `sp_wolf_lockup`, `spread`)
- "He's" and "basically" sit small (62 px sans) and spread on the left of the 270 Park podium shot.
- **13.72–15.07, "of Wall Street":**
  - The user's Wolf of Wall Street dollar-bill shot plays as one continuous shot: source 12.40–13.43 of the landscape copy, motion-interpolated to 1.35 s (about 0.77×) so no frame repeats.
  - "OF" 13.77, "WALL" 13.93, "STREET" 14.33. Each word comes from a 14 px blur, 36 px to the left and 1.08× wide, to sharp in 3 frames (power2.out). Inter Tight 800, 165 px, white, at the bottom (y ≈ 1000).
  - The face/currency boxes (from the Fink reel) are on top.
  - A punch-in at 14.90 (1.05 → 1.12 in 0.1 s).
  - 15.00: the purple inverted frame, with the words turning pink. 15.03: one white frame, then the fired page.
- Only "OF WALL STREET" is used, because the line is "the CEO of Wall Street".
- The reference's block glitch into the Wolf is not in the committed film; the Wolf enters after an inverted frame at 13.69 (§8.3).

### 5.5 "Was fired" reference (Jan Koum / WhatsApp reel)

**What it is.** A reel that opens "This guy was rejected by Facebook". Its creator is not recorded. It is used for "a guy who got FIRED"; whether it was meant for "he was fired" at 48 s instead is still open (§8.1).

**Measured** (ref 0–1.95, every frame at 25 fps)
- **Page:** window-lit off-white paper with a small square photo; four black dots sit just off its corners.
- **Photos:** each new photo replaces the last at a larger size, at 0.00, 0.20 and 0.44. The hero photo lands bigger with a motion blur, with REJECTED, at 0.68.
- **Words:** "this" 0.00, "guy" 0.28, "was" 0.48, "by" 1.00, stacked in black Helvetica on the photo's left, the block's edge following the photo. REJECTED sits in bold black caps on the right.
- **Push:** 0.68–0.96, the page pushes in hard (about 1.35×), then drifts.
- **Seen in the file:** computer icons (keyboard, cursor, floppy, camera) surround the hero photo. The Dimon version leaves them out ("no side assets").

**In the film (v5), S04 15.07–16.20** (`sp_fired_paper`, `faces.square`)
- **Page:** paper with window light.
- **Photos:** three young-Dimon squares, centred on his face by face detection: the Most Powerful Banker documentary at 871 s, from 15.07 (230 px); the same documentary at 700 s, from 15.32 (290 px); the black-and-white portrait from the Untold documentary (543 s) as the hero, from 15.64 (400 px, with a 2-frame zoom blur 0.84 → 1.0).
- **Dots:** four 13 px dots, 28 px off the photo's corners.
- **Words:** "A" 15.12, "guy" 15.18, "who" 15.37, "got" 15.53, in black Inter Tight 700 at 56 px, each sharpening in 2 frames, stacked left of the photo.
- **"FIRED":** Inter Tight 800, 112 px, on the right at 15.69. The page then pushes from 1.0 to 1.3 in 0.3 s (power3.out) and drifts to 1.34.

### 5.6 "We bank countries" reel

**What it is.** The user's own reference: a vertical reel of Dimon's Bloomberg interview. In the file, the interview sits in a rounded card on black with a small logo under it.

Transcript: "If you want to do what JP Morgan does, we move $10 trillion of money around the world every day, we bank some of these companies in 30 countries, we bank countries, we bank the World Bank, the IMF, we bank the United States government."

v1 calls it "the Dimon reel" or "the reference reel". The lockups v1 lists ("We bank / IMF", "30 / Countries") are on screen in this file.

**Measured (v4)**
- One or two words at a time over his chest, with a soft dark scrim.
- Helvetica-style words, with serif emphasis on "trillion" and "countries".
- Two-line lockups: "JP Morgan / does", "some of the / companies", "30 countries", "We bank / Countries".
- Words fade in from a blur and dissolve out.

**In the film (v5), S06 23.60–31.55** (the shots, caption blocks and times are in §3.2)
- **Base:** the same Bloomberg interview (`we bank the countries, we bank the world bank.mp4`, one take, source 273.05–281.0), cut to the user's lines, with B-roll between the interview stretches.
- **Captions:** the user's chunks, left-aligned at x 1110; each block leaves through a blur. "countries", "Countries", "IMF" and "government" are Instrument Serif at 150–230 px; "companies", "30", "World Bank" and "United States" are Inter Tight 800 at 100–118 px.
- **After the captions:** "You have to be big. You can't do those things and be small." runs to 34.85.
- **v1's caption system came from this reel:** Satoshi with Instrument Serif Italic, two-tier lockups and a 3-frame horizontal motion-blur entrance. v4 moved all type to Inter Tight and upright Instrument Serif, with no Satoshi and no italics.

### 5.7 AMD reel

**What it is.** Nothing is recorded beyond its name. There is no file in the Drive folder (checked, including the subfolders), no link, and no breakdown or frames in git. SPEC.md credits two devices to it: "the red marker sweep over a real headline" and "the cream data page with a red line drawing on". v1 calls the red #E5381B "AMD reference red".

**In the film (v5)**
- **S08 39.16–42.84, the headline sweep** (`sp_nyt`):
  - The real 1998 New York Times clipping, a black-and-white still from the Most Powerful Banker documentary at 1093 s.
  - On "next in line", a red marker sweeps under "Heir Apparent", tilted 1.1°, with a red cursor riding its front edge and then blinking.
  - At 40.28 the camera jumps down to the body text. A second sweep runs under "the world's largest financial services company" on "the biggest financial company".
  - Negative flashes at 39.16 and 40.28.
- **S17 70.73–74.50, the cream data page:**
  - Background #F2E8D6 with a halftone texture; heading "Bank One / net income, 2000 - 2003".
  - A red line draws on from "−$500M loss" to "+$3.5B profit", and the page pushes in 1.0 → 1.22.
  - v1 calls these real figures: −$511M in 2000 to +$3.5B in 2003.
- SPEC.md reserves the red for these two beats.

### 5.8 Our own Pattinson film

**What it is.** The Robert Pattinson montage film built earlier in this repo (`pattinson/`, `pattinson-v5/`). It is not in the Dimon Drive folder. The Dimon notes cite it for three things: the caption engine, the grain, and (in v5) its "generational run" transitions.

The Pattinson film was itself styled on two other references, which the Dimon notes never cite directly: the Metro Media House F1/Horner reel (`reference/f1-horner-reel-breakdown.md`, `c235220`) and, for the serif glow, the user's "AI cold war" reference (per `pattinson-v5/tools/build_v5.py`).

**Measured** (REFERENCES.md, Pattinson 5.30–9.10, every frame)
- 5.40–5.90: the shot eases back from full frame into a centred window (fast ease-out). Photo cards pop out from behind it in two- and three-frame steps, each after a white box.
- 6.17: an inverted frame.
- 6.63: a cut to the run, which arrives still moving sideways and slows into place (x 220 → 0, scale 1.26 → 1.03 over 0.34 s).
- Then straight cuts every 0.2–0.3 s.

**In the film (v5)**
- **S03 transitions** (`pan_arrive`, `sp_window_ease`):
  - 12.83: "the" (the Stanford shot) arrives still moving (x 220 → 0, scale 1.26 → 1.03 in 0.34 s, power2.out), then drifts.
  - 13.16–13.72: "CEO" (walking in with his security detail, from the user's montage) eases back into a window, to 0.64 in 0.42 s (power4.out).
  - Four photo cards pop out behind it at 13.32, 13.38, 13.44 and 13.50. Each follows a 2-frame soft white box and grows in 2-frame steps (0.62 → 0.86 → 1.0).
  - 13.69: an inverted frame. 13.72: the Wolf arrives moving the same way.
- **Captions everywhere** (the "Pattinson engine", §7.5): the glow values are copied from `pattinson-v5/tools/build_v5.py`. Black words on lit paper appear in S13 ("premise") and S22 ("that fell"). v2's sliding lines were removed in v4.
- **Noise:** the registry grain overlay at 6 % ("as in the Pattinson film"), jittered 12 times a second.

### 5.9 The user's own assets

| Drive file | What it is | Where (v5) |
|---|---|---|
| `jp morgan montage.mp4` | The user's montage. 1280×960 (4:3) with burned-in subtitles at the bottom, 30 fps, 28.5 s; the shots are cut from a 16:9 band above the subtitles. | S01 the J.P.Morgan flag (source 12.42–12.96, stretched to 0.705 s by `slowmo()`) and the tower at dusk (11.80–12.35, stretched to 1.13 s); S02 photo cards (stills at 25.55, 26.05, 16.55, 28.05, 11.65, 18.85); S03 "CEO" walking in (16.95–17.43) |
| `wolf of wwall street vid.mp4` | The user's Wolf cut, 720×900, 30 fps, 24.6 s | Picks the dollar-bill shot; the landscape copy is used instead, for width |
| `wolf of wall street clip to be used when he says wolf of wall street.mp4` | The Wolf of Wall Street, 960×720, 23.976 fps, 52.7 s | S03 13.72–15.07 (`wolf_slow.mp4`) |
| `over a bonus.mp4` | Daffy Duck fanning cash, 736×416, 30 fps, 27.8 s | S04 18.74–19.62 (from source 5.90; watermark cropped) |
| `money asset.mp4` | Money clip, 736×414, 24 fps, 8.0 s | S04 four-square, top-right cell (18.47–18.74) |
| `jamie ghost image.webp` | Black-and-white Dimon holding a glowing globe, 1536×1024 | The S06 ghost in this session. `tools/prep4.py` reads the first image in `dimon-src/_globe/` and draws a stand-in globe if the folder is empty. Which picture the old session used is not recorded (§8.6). |
| `fiered him push scene punch one. that takes soul out.mp4` | Doctor Strange palm strike, 640×268, 4:14 | S10 "fired" 49.84–50.81 (source from 96.93 s, i.e. 96.35 + 0.58 (`STRIKE_MS`), so that source 97.0 lands on "fired"; 1.4× speed, letterboxed to 1920×804, white flash and negatives) |
| `money/pinterest videos/` (17 files) | The user's Pinterest clips and stills | Details below this table |
| `halftone textures/` | The user's halftone scans | Every scene: Halftone Grunge as an overlay, Halftone 6 as paper. v5 strengths are 0.10 / 0.04 (0.05 / 0 on the interview scenes); Halftone 1 is on the data page |
| `sandie weil images/` | Photos of Sandy Weill, plus `Jamie_Dimon_Image_Pack_More.zip` | Two of them are among the eight S04 Weill faces (`dimon-src/_weill/weill_0.jpg`, `weill_1.jpg`). Which two the old session used is not recorded in git; this session links `images.jpg` and `images (1).jpg`. |
| `Jamie_Dimon_Image_Pack/` | 90 images in 10 folders, plus `Sources.csv` | Photo cards, SVG logos, the World Bank building, boxing gloves, the Bezos cut-out, the $100 note, Chicago's Bank One tower, 2008 crisis photos, the name-card cut-out. Its README says: "Not all commercially cleared. Source-specific licences apply (Sources.csv)." |

How v5 uses `money/pinterest videos/`:
- **Counting machine** (P07): S01 "capitalism", the S04 grid, S23.
- **Falling money** (P10): darkened under the $60M counter in S16, and in screen blend at 0.55 over the screen wall in S23. The filename reads "money can be used in difference effect in bg less opacity. bklend"; v5 does not use a difference blend.
- **Chess hand** (P01): S13 "premise".
- **Burning room** (P02): S19 "hit".
- **Pallets of cash lifted off the Fed** (P06): S22.
- **The chess king left standing** (P11): S21.
- **The presidential seal PNG:** S02.
- **Dimon pictures:** only one of the three is on screen: `jamie image.jpg` (`pin_mic`), a photo card in S03 at 13.50. `jamie black and white image.jpg` (`pin_bw`) and `jamie dimon pic.jpg` (`pin_green`) are registered but not on screen in v5: they only feed the uncalled seal ring, and `prep4.py` uses the black-and-white one for its stand-in globe when `_globe/` is empty.

### 5.10 Drive source footage (documentaries, interviews)

| Drive file | Local alias (key) | Specs | What it is | Used for in v5 |
|---|---|---|---|---|
| `name of the game.mp4` | `_direct/name_of_the_game.mp4` (GAME) | 1920×1080, 23.976 fps, 9:26 | Bloomberg Originals: the news open and B-roll | See notes below the table |
| `we bank the countries, we bank the world bank.mp4` | `_direct/we_bank.mp4` (BANK) | 1920×1080, 23.976 fps, 22:31 | Bloomberg interview (Emily Chang) plus archival (REVIEW v4: "it is 1080p, not 4K") | S06 Dimon's own words (audio source 272.5–285.0; picture 273.05–281.0, matted) and its B-roll; NYSE board and screens (S01, S23); side by side (S09); the last shot (S23) |
| `Jamie Dimon - The Most Powerful Banker in America   Full Documentary.mp4` | `_direct/most_powerful_banker_doc.mp4` (MPB) | 1920×1080, 24 fps, 34:31 | Documentary | See notes below the table |
| `The Untold Career Story of Jamie Dimon (CEO of JPMorgan).mp4` | `_direct/untold_career_story.mp4` (UNT) | 1920×1080, 30 fps, 20:24 | Documentary, used only for archival inserts (its "year (age)" label is cropped out) | The black-and-white young Dimon (S04 hero photo, S10 "at 42"); "Fire Sale" (S22); a 2004 card |
| `How JP Morgan Chase Became The Largest Bank In The US.mp4` | `_direct/how_jpm_became_largest.mp4` (HOW) | 1920×1080, 25 fps, 19:02 | CNBC | Wall St sign, 1920s (S01, S07); NYSE floor on "game" (S01); the Fox "JP Morgan buys Bank One" report (S18); hourglass and 2008 floor (S19); WaMu (S22); wall tiles (S13); screen wall (S23) |
| `Stories from 2008's Great Recession  (a lot of material on stock market bank clips wwall street traders persons).mp4` | `_direct/stories_2008_recession.mp4` (STO) | 1920×1080, 29.97 fps, 51:36 | 60 Minutes stories from 2008 | Lehman (S19 "crisis"); bank run, FDIC "Your bank has failed", head in hands on "dying" (S20) |
| `Stock Market Crash of 2008.mp4` | `_direct/crash_2008.mp4` (CRASH) | 1280×720, 29.97 fps, 3:12 | 2008 news broadcasts | Fox "Dow falls 733" on "financial" (S19, CRT look); a screen-wall cell (S23) |
| `Jamie Dimon, Chairman, President, and CEO of JPMorgan Chase.mp4` | `_direct/dimon_chairman_interview.mp4` (CHAIR) | 1920×1080, 29.97 fps, 57:19 | Long interview; the build labels the moment at 1265.2 s "Stanford" | S03 "the" (arrives moving); S12 "He took up" |
| `jamie dimon speaking video.mp4` | `_direct/dimon_speaking.mp4` (SPEAK) | 1920×1080, 23.976 fps, 1:13 | Dimon talking | S01 slide-up and S02 Hemant opening and stage, matted with a glow |
| `jamie dimon audi.mp3` | `dimon-src/jamie dimon audi.mp3` | 75.0 s | The narration | See notes below the table |

`name of the game.mp4` provides:
- **The opening voice:** the reporter alone (a Demucs vocal stem), re-cut to "The name of the game in American capitalism, is being big, and no one is bigger [0.5 s held] on Wall Street than JPMorgan Chase."
- **The music bed under the whole film:** its opening cue (120 BPM), with one jump on a bar line, at −30 LUFS.
- **B-roll:** S01: Lower Manhattan, the towers, the vault door, rush hour, the reporter in sync, the Wall St sign. S03: the 270 Park podium. S05: the ribbon, the hard hats, the tower, the glass. S12: Bezos. S23: signs and the trading floor.

`Most Powerful Banker` is the most-used source (30 clips, 16 stills): S04 (the young-Dimon photos, the Weill faces, and Weill with his daughter); S07 (the golden boy); S08 (the 1998 NYT clipping); S09 (Commercial Credit, Smith Barney and the Citigroup launch); S14 (Bank One and Chicago); S15 (the dividend and the clean-up); S20–S22 (Bear Stearns and the last man standing); S23 (the stone sign).

`jamie dimon audi.mp3` is laid in two pieces: voiceover 0–14.10 s starts at film 9.05, and voiceover 18.40–75.00 s starts at film 34.97. The narrator's paraphrase in between is replaced by Dimon's interview (§3.4).

**Not used in v5:**
- `Dimon Cuts Ribbon on JPMorgan's New Manhattan HQ.mp4` (RIB, vertical). The ribbon shot comes from GAME instead.
- `JPMorgan building aura farming!! #shorts #aura.mp4`.
- `NEW YORK STOCK EXCHANGE Closing Bell Ceremony 🇺🇸.mp4`.
- `💰Wall Street New York 🇺🇸 … shorts.mp4`.
- `watch-citadel-s-high-speed-trading-in-action-ytmp4.savetube.vip.mp4`.
- `cool cinematic clip.mp4` (v1's "premise" shot, which v1 called its weakest).
- `J P Morgan The Man Who Bought America   Full Documentary.mp4` (34:17). It was downloaded in v4 "For B-roll later in the film" but no script uses it yet.

`jpm-dimon-v5-0-31-share.mp4` in the folder is the v5 render of 0–31.7 s, not a source (§2).

---

## 6. Style rules and the user's standing preferences

### 6.1 The user's standing preferences (recurring across rounds)

| Preference | Where it is recorded | Status |
|---|---|---|
| No sound effects at all | SPEC v1: "no SFX (user's standing preference)"; REVIEW v1; SPEC v2 bans "Any SFX" and says "No SFX, as the user prefers" | In force; no version has SFX. `18142fc` says the Pattinson edit "used SFX only"; the jpm-dimon files treat no SFX as the user's wish for this film. |
| Music: the Bloomberg open's own cue under the whole film | v3 note: "keep the background music of the first Bloomberg clip, continuing for the whole video" | In force since v3. The bed is cut to end on the last frame, so any change in length means re-cutting it with `tools/make_music.py`. |
| 16:9, 1920×1080, 30 fps (switched from vertical) | v1 | In force |
| Dimon's own words for "We bank…", using exactly the user's lines | v1 build; v4: "Lines: exactly yours" | In force |
| Motion graphics, not "a slow zoom and text in front" | v1 verdict; SPEC v2 | In force |
| Real, literal footage and more photographs; real video only in S03 (v4) | v3: "better footage, more photos"; v4: S03 in real video only (S04 still uses photos in v5, changed at the note "The fired photos cut his face; wrong pictures") | In force |
| Copy the references exactly, frame by frame, at the moments the user names | v3: "edit it exactly like the reference"; v4–v5 working method | In force. Each beat's reference is in the "Reference imitated" column of §3.1; the measurements are in §5. |
| Type: Inter Tight plus Instrument Serif regular with glow; no italics, no Satoshi; words land in place; captions beside the subject; two consistent sizes per lockup; "JPMorgan Chase" spelt properly, not in capitals (v5 note on S01; the S07 name card still has a capitalised outline, "JAMIE DIMON"); the Wolf lockup in white, "not yellow" | v4–v5 | In force |
| Light textures: CRT lines and noise, lighter than the references | v5 | In force; replaces the heavy halftone of v1–v4 |
| The Larry Fink clip is a style reference, not footage | v1: "for someone else"; v2: "a style reference only" | In force |
| Use the user's own assets wherever given: the Wolf dollar-bill shot, the "over a bonus" cartoon, the money asset, the JP Morgan montage, the globe picture, the Sandy Weill photos | v4–v5 | In force |
| Keep the beats the user approved: the "capitalism" counting machine ("very good"), the flash on BIG ("fine"), the 1998 year roller ("fine with Citigroup behind"), and S05 unchanged | v4–v5 | In force |

### 6.2 Rules from SPEC.md that still apply
- **Ground:** the footage itself. Dark set pieces use near-black #070707 (SPEC: under the user's halftone print in screen at 10 %; v5 uses 5 %).
- **Ink and accent:** warm white #FBF8EC. Red #E5381B is reserved for the NYT marker and the data page (v1 calls it "AMD reference red").
- **Cuts:** hard cuts on the spoken word (−0.05 s), with negative flashes (1–2 frames) on cuts that change world.
- **White flash:** on "fired", "hit", "standing" and the boxing punch.
- **Cameras:** one slow push per shot, or a hard punch-in (a one-frame set, never eased). SPEC says 1.00 → 1.025; in the v5 code the push is set per shot with `push=` (the montage default is 1.025). Of the 101 pushes in the compositions, 72 end at 1.02–1.04, 18 at 1.05 and 9 at 1.06–1.08 (FIRED and the last shot reach 1.08); one pulls back 1.15 → 1.00 (the towers on "big"), the S02 backdrop goes 1.34 → 1.37, and some shots have no push.
- **Caption motion:** the sans, serif-line and hero word entrances in §7.5. SPEC's line slide is superseded (§6.4).
- **QA frames:** §7.4.

### 6.3 The banned list and the house rules

SPEC.md's BANNED list, word for word, with whose rule each is:

| Banned (SPEC.md) | Whose rule |
|---|---|
| Pop, bounce or slide-up text. | A house rule of the previous sessions, not attributed to the user |
| Tilts and slides between shots. | House rule |
| Any SFX. | The user's standing preference |
| The Larry Fink clip itself (it is a style reference only). | The user: "for someone else" (v1) |
| Burned-in subtitles, channel bugs or YouTuber labels on screen (cropped out). | House rule |
| A still with only a slow zoom and a caption standing in for a beat. | From the user's verdict on v1 |

Where the user's later notes conflict with this list, the notes won. Two examples:
- The comment on `sp_slide_pop` records the user asking for Dimon's matted video to slide up from the bottom in S01.
- The notes on v4 asked for "Pattinson-style smooth transitions" in S03, which is where `pan_arrive` comes from.

Other house rules set by the previous sessions (not attributed to the user), with where each is recorded:
- no glowing orbs, mesh gradients, logo in a corner, or three cards in a row: only in the v1 SPEC's BANNED line (`git show 2bb2905:jpm-dimon/SPEC.md`); the current SPEC.md (v2) dropped them;
- no made-up headlines ("any fabricated headline (only real headlines from the footage)"): also only in the v1 SPEC;
- every clip stays inside one source shot: REVIEW v3 and `tools/check_shots.py`;
- no styles on untimed wrappers: the `build4.py` / `build5.py` header ("No visual styles on untimed wrappers") and REVIEW v4 (v3's "square").

### 6.4 Superseded notes and decisions

| Earlier | Round | Replaced by | Round |
|---|---|---|---|
| Satoshi plus Instrument Serif Italic captions with a motion-blur entrance ("the Dimon-reel system") | v1 | The Pattinson caption engine: glow, flicker box, lines that re-centre as words arrive | v2 |
| The Pattinson engine: Satoshi, sliding lines, sans-over-serif stacks (SPEC.md still describes it) | v2–v3 | Inter Tight plus Instrument Serif only, words landing in place | v4 |
| Dario's glitch frames on the second word of a name (SPEC.md: "Instrument Serif 250 for names (with the Dario glitch frames)") | v2–v3 | Removed: `build4.py` and `build5.py` no longer have them; no review records the change | v4 |
| A slow push on every shot; stills held 2–3 s | v1 | Motion-graphics set pieces, a new picture every 1–3 words | v2 |
| No music ("none supplied yet"; SPEC.md still says "No music has been supplied yet") | v1–v2 | The Bloomberg open's cue under the whole film | v3 |
| Open: "…in American financial capitalism, is being big…" (SPEC.md: 0.00–8.81) | v1–v3 | "…in American capitalism, is being big … bigger [held] on Wall Street than JPMorgan Chase", 0–8.88 s | v4 |
| SPEC.md's build steps (`build2.py`, `prep2.py`, `media_v2.json`) | v2 | `build5.py` and `media_v5.json` (§7) | v5 |
| "game" on a paper card | v2–v3 | The NYSE trading floor | v4 |
| BIG as a word mask with a dive through the letter | v2–v3 | BIG "simply there" | v4 |
| The Fink seal ring and the seal punch-in for "the most influential man" | v2–v3 | Hemant's opening (v4), then Hemant's opening and stage on his talking video (v5) | v4–v5 |
| "in American capitalism" as one serif lockup | v4 | "in American" small above "capitalism" big | v5 |
| "bigger" as a 150 px word between two giant blurred echoes, one above and one below (v2–v3), then 340 px with close echoes and a tiny copy (v4) | v2–v4 | Dario's SUDDENLY frame for frame: darker, moving echo rows, no small copy | v5 |
| JPMORGAN CHASE typed in capitals | v4 | "JPMorgan Chase", condensed | v5 |
| Dimon popping up as a glow cut-out | v4 | His matted talking video sliding up from the bottom, no zoom | v5 |
| S02: an interview freeze, then photo cards | v4 | Hemant's 22–25 s layout on Dimon's talking video | v5 |
| Photo cards in S03 | v3 | Real video only | v4 |
| The Wolf shot slowed by the player (0.72×) | v4 | One continuous shot, slowed to 0.77× by motion interpolation | v5 |
| v4's young-Dimon photos | v4 | 1990s documentary photos cropped on his face | v5 |
| "mentor" as a three-shot montage | v4 | Dario's "every AI tech bro", with Sandy Weill | v5 |
| "and a family" / "grudge" at the bottom | v4 | Centred | v5 |
| "We bank countries" as photo cards (v2), then a photo wall (v3) | v2–v3 | The interview as the base (v4), then interview and B-roll alternating with a moving ghost picture (v5) | v4–v5 |
| Heavy halftone textures (grunge 40–42 %, paper 28–30 %; SPEC.md: 40 % / 28 %), documentary-grade grain 0.12, black grounds' texture at 10 % | v1–v4 | 0.10 / 0.04 (0.05 / 0 on the interview scenes), grade grain 0.07, black grounds at 5 %, plus the 6 % grain layer | v5 |
| The v3 "square" (a shadow on an untimed wrapper), and the same box-shadow on the s13 "premise" chess-hand panel | v3 | Removed | v4 |

What still holds in SPEC.md: the goal, the output spec, the colours (with the red reserved for two beats), the cut, negative-flash and white-flash rules, the sans and hero word entrances, and the banned list. Its "References and what each gives" is the v2 list: it still lists devices v4 and v5 removed (the seal ring with glint and rays, the "this man" punch-in, BIG's dive, the v2 SUDDENLY echo for "BIGGER", the sliding lines, the name glitch frames) and none of the references added since (Ackman, "was fired", the we-bank reel, Hemant's opening and stage, DISAPPEAR, "every AI tech bro", the Fink Rogan screen, the Pattinson window and arrive moves). Its camera rule (1.00 → 1.025) and its 2-frame flicker box differ from the code (§6.2, §7.5). The current list is the §5 Quick map and the "Reference imitated" column of §3.1.

---

## 7. How it is built, edited and rendered

This describes the code as of v5 (`292806f`).

**In short:** the film is generated by code. `tools/build5.py` is one Python file of about 2,400 lines, and it holds the whole edit: every shot, word time, effect and caption. Running it rewrites `index.html` and everything in `compositions/`. The prep scripts cut the media it asks for out of the raw Drive download into asset folders that are not in git.
- **Edit the Python, not the HTML.** You fix a note by changing `build5.py` (or a prep script) and rebuilding. Hand edits to the HTML, and edits saved from Studio, are overwritten on the next build. Every commit that changed `compositions/` also changed that round's builder, so nothing was ever edited by hand.
- **One builder per round.** Each round got its own builder and media list (`build.py` for v1, `build2.py` to `build5.py`, `media_v2.json` to `media_v5.json`). The older ones are kept for reference only.
- **The committed HTML plays as it is.** It plays once the media assets exist, and you need `build5.py` only to change the edit.
- **Skills.** `CLAUDE.md` asks for the `/hyperframes` skill to be loaded before compositions are changed, and for a check and a snapshot after every change.

### 7.1 Where things live

| Path | What it is | In git? |
|---|---|---|
| `jpm-dimon/tools/build5.py` | The edit. Writes `tools/media_v5.json`, `index.html` and `compositions/*.html`. | yes |
| `jpm-dimon/tools/media_v5.json` | List of every clip and still `build5.py` registers (113 clips, 111 stills); 110 clips and 71 stills are on screen. `ST()` registers stills where they are defined, used or not (unused: `ring0`–`ring11`, `gov_*`, `lead_*`, `ld0`–`ld2` and `ld4`–`ld9`, `dp2`–`dp5`, `pin_bw`, `pin_green`, `cut_dimon06`, `lg_citi`, `lg_chase`, `lg_wb`). The unused clips are the three books from the module-level `BOOKS` (`MPB_61600_75`, `MPB_149600_75`, `MPB_127300_75`); S12 cuts them again at other lengths. Generated; do not edit it by hand. | yes |
| `jpm-dimon/tools/prep_media.py`, `prep2.py`, `prep4.py`, `prep5.py`, `faces.py`, `make_music.py`, `check_shots.py` | Media preparation and checks (§7.3). | yes |
| `jpm-dimon/tools/base_grade.json` | The neutral colour-grade settings every grade starts from. `gradings.json` is left over from v1. | yes |
| `jpm-dimon/index.html`, `compositions/s01.html` to `s23.html`, `captions.html`, `grain.html` | Generated output. | yes |
| `jpm-dimon/compositions/components/grain-overlay.html` | Film-grain component from the HyperFrames library, listed in `hyperframes.json`. Not regenerated. | yes |
| `jpm-dimon/assets/fonts/` | Used: Inter Tight 600/700/800 and Instrument Serif Regular. Unused: Instrument Serif Italic (from v1). Satoshi (v1 to v3) is kept out of git and unused since v4. | yes |
| `jpm-dimon/assets/clips2`, `img2`, `tex`, `audio` | The media the film plays. Rebuilt by the prep scripts. | no |
| `jpm-dimon/assets/clips`, `img` | v1 media made by `prep_media.py`. Not used by v5. | no |
| `jpm-dimon/renders/` | Rendered videos. | no |
| `jpm-dimon/vendor/gsap.min.js` | The GSAP animation library, loaded from the project. | yes |
| `jpm-dimon/SPEC.md`, `REVIEW.md`, `REFERENCES.md` | The notes (§2). | yes |
| `/home/user/claude-test-2.0/dimon-src/` | The raw Drive download. | no |
| `/home/user/claude-test-2.0/dimon-work/` | Working files: `tx/` and `vo/` (transcripts and the WAV files their word times are matched to), `cut/` (photo cut-outs), `music/` (the voice and music separated from the Bloomberg open). | no |
| `/home/user/claude-test-2.0/pattinson-v5/tools/build_v5.py` | The user's Pattinson film. v5's text-glow values were taken from it. | yes |
| `/home/user/claude-test-2.0/dimon/reference/FINK_REEL_REFERENCE.md` | Frame-by-frame breakdown of the Larry Fink reel (`18142fc`, §1–§10). In this checkout `dimon/` holds only `reference/` (29 tracked files). The earlier separate build of the same film, and the §11 it added to this file, are only on `origin/claude/stoic-mccarthy-hijqav` (`36daffd`, `0b01d42`, `18bf89d`); that build is not used here. | yes |

**How `dimon-src` is laid out.** The scripts use short file names, not the Drive's names.
- **Short-name folders:** `_direct/` (for example `name_of_the_game.mp4`, `we_bank.mp4`, `most_powerful_banker_doc.mp4`); `_pin/p01` to `p11` (the "money_pinterest videos"); `_bonus/` and `_money/`; `_globe/` (the user's globe picture); `_weill/` (Sandy Weill photos).
- **Folders and files under their own names:** `Jamie_Dimon_Image_Pack/`, `money_pinterest videos/`, `halftone textures/` and `jamie dimon audi.mp3` (the narration).
- **Where each short name points:** the table of short names is `V` in `tools/prep2.py`, and the comments on `V` in `prep_media.py` say what each source is.
- **The links themselves** are not in git. In this container they are symbolic links. `_direct/`, `_bonus/`, `_money/`, `_globe/` and `jamie dimon audi.mp3` link into `dimon-src/_drive/`, which holds the Drive files under their Drive names. `_pin/` links into `dimon-src/money_pinterest videos/` (each `pNN_…` name is made from part of the target's file name), and `_weill/` into `dimon-src/sandie weil images/`.

**Paths are fixed.** Every script hard-codes `ROOT = "/home/user/claude-test-2.0"`.

### 7.2 How build5.py writes the film

```bash
cd /home/user/claude-test-2.0/jpm-dimon
python3 -I tools/build5.py --specs   # rewrites tools/media_v5.json only, prints the clip and still counts
python3 -I tools/build5.py           # rewrites media_v5.json, index.html and all of compositions/
```

The "Run:" line at the top of `build5.py` still names `build4.py`. It is out of date.

A full run does these steps in order:
1. Writes `media_v5.json`.
2. Deletes every `.html` file directly in `compositions/` (not in `components/`).
3. Writes `s01.html` to `s23.html`, one per scene.
4. Builds `captions.html`.
5. Writes `grain.html` from the grain component.
6. Writes `index.html`.

The build's only randomness has a fixed seed, so the same inputs give the same output.

| Lines in build5.py | Part |
|---|---|
| 52–128 | **The clock.** Word times for the news open (`NEWS`, typed in by hand), the narration (`VOW`) and Dimon's interview quote (`QUOTE`). `NT(i)`, `VT(i)` and `QT(i)` turn word number *i* into a time in the film. `CUT(t)` is t − 0.05 s, so picture cuts land 50 ms before the word. |
| 131–224 | **Media list.** `CL()` registers a clip and `ST()` a still. `VERT` lists the vertical sources, `FRAME_OF` gives the crop that removes channel logos for each source, and there are photo lists (`DIMON_PHOTOS`, `LEADERS`, `RING`, `WALL`, `CARDS_*`, `LOGO` and others). |
| 226–271 and 1172–1183 | **Colour grades** (`GR`). |
| 273–315 | **Type:** font loading, `INK` (the text colour), the glow shadows, and `textw()`, which measures text widths from the font files. |
| 323–500 | **`Scene`**, with the building blocks every scene uses: `v()` (a video shot), `vfile()`, `vert()`, `img()`, `black()`, `paper()`, `raw()`, `neg()`, `flash()`, `whiteframe()`, `streak()`, `punch()` and `write()`. |
| 522–1165 | Effects from v2 and v3 (the `sp_*` functions). |
| 1171–1566 | Effects from v4 and v5, matched to the reference reels. |
| 1569–1752 | **Captions:** `STY`, `cap()`, `spread()` and `build_captions()`. |
| 1754–2286 | **The edit itself.** One block per scene, `S01` to `S23`. The film-wide list of negative flashes is at line 2282. |
| 2291–2372 | `write_aux()` writes the grain; `write_root()` writes `index.html` and places the audio. |

**How a scene is built.** A scene is `Scene(sid, start, end, ground="#070707", tex=(0.10, 0.04))`.
- **Timing:** every element inside it is `class="clip"` with `data-start` and `data-duration` counted from the start of the scene.
- **Animation:** each scene registers one paused GSAP timeline as `window.__timelines["sNN"]`.
- **Shots:** a shot is a muted `<video src="assets/clips2/<clip id>.mp4" data-media-start="0">`. The file is already cut to the shot. It sits inside a `.cam` box that carries the slow push-in, and its colour grade is set with `data-color-grading`.
- **Texture:** each scene also gets two full-frame texture layers.

**`index.html`** holds the 23 scenes (`data-composition-src="compositions/sNN.html"`, stacked at z 10 to 32); `captions` (z 100) and `grain` (z 150), both running the full 93.2 s; and the five audio clips in §3.4. The film is 1920×1080. The root sets no frame rate, so it uses the default of 30 fps.

**The clock.**
- **The open:** `NEWS` (line 106) holds word start times measured by hand on `news_voice.wav`.
- **The narration:** `VOW` is the Parakeet transcript `dimon-work/tx/pk_vo/transcript.json`. Each start is snapped to the sound in `dimon-work/vo/vo16k.wav`. Narration 0–14.10 plays from 9.05 s. The rest is shifted so that word 55 ("Meet") lands at 35.25 s.
- **The quote:** `QUOTE` is `dimon-work/tx/pk_bank/transcript.json`, snapped to `dimon-work/tx/bank_quote.wav`. Time 0 there is 272.5 s into `we_bank.mp4`. Parakeet dropped the word "You", so the code puts it back at position 25.
- **How the edit refers to words:** captions and cuts point at words by their number. `W_(i, style)`, `N_` and `Q_` give (text, time, style), and shots start at `CUT(VT(i))`.

**Scene map** (with the line in `build5.py` where each block starts). Only 0–31.7 s, from S01 to "…the United States government" in S06, was rebuilt in v4 and v5.

| Scene | Film time (s) | Line | What happens and the main effects |
|---|---|---|---|
| S01 | 0.00–9.05 | 1775 | Bloomberg open. "BIG" (`sp_big_static`); "bigger" (`sp_suddenly`, Dario's SUDDENLY); "JPMorgan Chase" (`sp_type_word`, Dario's DISAPPEAR) over `flag_slow`/`tower_slow`; Dimon slides up (`sp_slide_pop`) |
| S02 | 9.05–12.36 | 1812 | "This is the most influential man in America right now." Hemant reel effects: `sp_hemant_open`, `sp_sil_flash`, `sp_hemant_stage`, `sp_white_wipe` |
| S03 | 12.36–15.07 | 1850 | "He's basically the CEO of Wall Street." Pattinson moves `pan_arrive` and `sp_window_ease`; `wolf_slow` with face boxes; Ackman lockup `sp_wolf_lockup`; purple negative frame, then a white frame |
| S04 | 15.07–20.86 | 1889 | `sp_fired_paper` (the "was fired" reference); `sp_roller` to 1998; `sp_dario_faces` (Sandy Weill); `sp_grid4`; the bonus cartoon; the grudge pan |
| S05 | 20.86–23.60 | 1911 | Straight cuts |
| S06 | 23.60–34.85 | 1925 | Interview alternating with B-roll; `sp_ghost` and `sp_quotes` (Fink's Rogan screen); Dimon matted above the globe picture; `sp_window` |
| S07 | 34.85–38.43 | 2000 | `sp_name_card`, `sp_gleam` |
| S08 | 38.43–42.85 | 2014 | `sp_nyt` (red marker on the NYT clipping) |
| S09 | 42.85–47.76 | 2029 | Split screen; `sp_roller` "16 years" |
| S10 | 47.76–50.81 | 2047 | `sp_bars`; punch-in on "42"; palm strike on "fired" |
| S11 | 50.81–53.02 | 2063 | `sp_calendar` |
| S12 | 53.02–57.76 | 2068 | `sp_strobe` (boxing); book covers; `sp_text_behind` ("Amazon" behind Bezos) |
| S13 | 57.76–62.08 | 2087 | Paper card for "premise"; `sp_echo` ("comeback"); `sp_wall` |
| S14 | 62.08–65.32 | 2104 | `sp_typed` "In 2000"; glitch on "broken" |
| S15 | 65.32–67.14 | 2122 | `sp_slice`, `sp_wipe` |
| S16 | 67.14–70.73 | 2129 | `sp_counter` to $60 million; the $100 bill with a punch-in |
| S17 | 70.73–74.50 | 2144 | Bank One data page (written directly in the scene block) |
| S18 | 74.50–77.67 | 2179 | `sp_merge`; `sp_roller` to 2004 |
| S19 | 77.67–80.19 | 2188 | `sp_roller` to 2008; crash shots |
| S20 | 80.19–82.04 | 2203 | Fast flicker of crisis pictures |
| S21 | 82.04–83.50 | 2222 | Chess panel; "standing" |
| S22 | 83.50–86.11 | 2232 | `sp_cards_fall` |
| S23 | 86.11–93.20 | 2246 | `sp_logo_wipe`, `sp_screens`, `sp_counter` to $10 trillion, `sp_typed` "Today", fade to black |

### 7.3 Media: the list and the prep scripts

**How clips and stills are registered.**
- **Clips:** `CL(key, t, dur, frame, size, xyz, matte)` registers a clip: source `key`, start `t` and length `dur`, with 0.25 s added at the end.
  - The clip's name spells out its settings: `KEY_<t×100>_<dur×100>[v][_frame][_x<cx>_<cy>_<zoom>]`, where `dur` includes the 0.25 s. For example, `BANK_27305_820_x63_50_135` is `we_bank.mp4` from 273.05 s, an 8.20 s file for 7.95 s on screen, cropped around the point (0.63, 0.50) at 1.35× zoom.
  - The crop numbers in the name are truncated (`int(v * 100)`), so some are one off: `GAME_8150_70_x56_53_114` is really (0.57, 0.53, 1.15), and the SPEAK clips' `x59_40_114` is (0.592, 0.40, 1.15). Read the `xyz` in `build5.py`, not the name.
  - So changing a shot's start, length or crop gives it a new file name, and the next `prep2.py` run cuts that new file.
  - `frame` picks a named crop that removes channel logos, the YouTuber's label or the montage's burned-in subtitles (`BBG`, `CNBC`, `UNTF`, `SIXTY`, `MONT`, `FULL`).
  - `xyz` sets a custom crop.
  - `matte=True` asks `prep5.py` to cut the person out of the background.
- **Stills:** `ST(sid, ...)` registers a still.
  - `path=` means a file under `dimon-src`, or an absolute path. `edge` sets the longest side and `crop` trims it.
  - `key=` and `t=` mean a frame grabbed from a source video, with the same crop as the clips.
  - SVG logos are copied unchanged.

**What each script makes:**

| Script | Makes | Notes |
|---|---|---|
| `build5.py --specs` | `tools/media_v5.json` | Needs `dimon-work/tx`, `dimon-work/vo` and `brotli`. It loads the transcripts as soon as it starts, and the scene code measures text with fontTools (which needs `brotli` for the `.woff2` fonts) before `--specs` exits. |
| `prep2.py --spec=media_v5.json [--force] [id …]` | Clips in `assets/clips2/<id>.mp4` (H.264, 30 fps, no sound, cropped to the registered size: 1920×1080, or 608×1080 for vertical sources). Stills in `assets/img2/`. Cut-outs in `dimon-work/cut/*.png`, made with `npx hyperframes@0.9.2 remove-background`. | Its default list is still `media_v4.json`, so always pass `--spec=media_v5.json`. It makes only missing files; any ids you name on the command line are remade. |
| `prep4.py [--force]` | `img2/globe_ghost.jpg`: the first image in `dimon-src/_globe/`, in black and white, cropped to 1220×1080. If the folder is empty it draws a stand-in. Also the v4 freeze frames `stage_*` and `intv_*`, which v5 does not use. | |
| `prep5.py` | Cut-outs of clips flagged `matte` (`<id>_cut.webm` from `remove-background --quality best`, plus a `<id>_halo.webm` glow). The S02 silhouette images (`img2/spk_f.jpg`, `spk_cut.png`, `spk_sil.png`, `spk_halo.png`). Smooth slow-motion clips (`wolf_slow`, `ceo_slow`, `flag_slow`, `tower_slow`). Sandy Weill's faces (`img2/wf0.jpg` to `wf7.jpg`, from `faces.dario`). Square photos of young Dimon (`img2/yd5_1.jpg` to `yd5_3.jpg`, from `faces.square`). | The file name `media_v5.json` is written into the script. It has no `--force`: anything that already exists is skipped. It loads `faces.py`. |
| `faces.py` | Face-finding functions used by `prep5.py`. Also a command: `sheet` (a contact sheet showing the detected faces, for choosing photos), `square` and `align`. | Needs OpenCV 4, because it uses `cv2.CascadeClassifier`, and it builds its detectors as soon as it is imported, so without OpenCV 4 all of `prep5.py` fails. It looks for OpenCV in the folder named by `$CV4_DIR`; the default is a scratchpad folder from the old session, which no longer exists. `tools/rebuild/rebuild_media.sh` installs it into `dimon-work/cv4` and sets `CV4_DIR` (§8.4). |
| `make_music.py` | `audio/news_voice.wav` (the reporter alone, re-cut, at −16 LUFS) and `audio/music_bed.wav` (at −30 LUFS). The separated voice and music go in `dimon-work/music/`. | Uses Demucs to separate voice from music, and needs `torch`, `torchaudio`, `demucs` and `soundfile`. It answers the v3 note about the Bloomberg music. The music is cut to end exactly at 93.2 s. |
| `prep_media.py [id …]` | The textures `tex/ht_grunge.jpg`, `ht_paper.jpg` and `ht_warm.jpg` (the user's halftone scans, filtered into neutral overlay maps). Also `audio/vo.wav` (the narration), `audio/dimon_quote.wav` (`we_bank.mp4` from 272.5 s) and `audio/news_open.wav` (not used in v5). | This is the v1 script. Run with no ids, it also re-cuts all the v1 clips into `assets/clips` and downloads Satoshi. For v5, run it only with `ht_grunge ht_paper ht_warm audio`. |
| `check_shots.py media_v5.json` | A report | Lists clips that cross a cut in their source video; such a clip would flash one frame of the wrong shot. Its default list is `media_v3.json`. |

**Rebuilding everything from scratch, in order.** The order is the one REVIEW.md gives. The `prep_media.py` step dates from v1 but is still the only one that makes the textures and the narration and quote audio. On a fresh checkout the commands fail unless step 0 is done first, and they leave two files missing (the last step).

Step 0, by hand (no script does any of it):
1. Download the Drive folder: the top-level files into `dimon-src/_drive/`, and `Jamie_Dimon_Image_Pack/`, `money_pinterest videos/`, `halftone textures/` and `sandie weil images/` into `dimon-src/` (§7.1).
2. Make the short-name links that `V` in `prep2.py` expects (`_direct/`, `_pin/`, `_bonus/`, `_money/`, and `jamie dimon audi.mp3` at the top of `dimon-src/`), using §3's table of keys and Drive files.
3. Put `jamie ghost image.webp` in `_globe/` (if the folder is empty, `prep4.py` silently draws a stand-in globe) and two Sandy Weill photos in `_weill/` as `weill_0.jpg` and `weill_1.jpg` (this session used `images.jpg` and `images (1).jpg`).
4. Make `dimon-work/tx/` and `dimon-work/vo/` again ("Files no script makes", below).
5. Install `brotli` and OpenCV 4 (§8.4).

```bash
cd /home/user/claude-test-2.0/jpm-dimon
python3 -I tools/build5.py --specs
python3 -I tools/prep2.py --spec=media_v5.json
python3 -I tools/prep4.py
CV4_DIR=/path/to/opencv4 python3 tools/prep5.py   # a folder with OpenCV 4; all of prep5.py needs it, as it imports faces.py (§8.4)
python3 -I tools/make_music.py
python3 -I tools/prep_media.py ht_grunge ht_paper ht_warm audio
python3 -I tools/check_shots.py media_v5.json
python3 -I tools/build5.py
```

Last step, by hand: make the S06 cut-out with `npx --yes hyperframes@0.9.2 remove-background assets/clips2/BANK_27305_820_x63_50_135.mp4 -o assets/clips2/BANK_27305_820_x63_50_135_cut.webm --quality best` (the call `prep5.py`'s `matte()` makes; or add `matte=True` at line 1937 before running `prep5.py`), and supply `assets/tex/paper_light.png`, which no script makes (both below).

**What has to be installed:** Python 3 with fontTools plus `brotli` (needed to read the `.woff2` fonts); numpy and Pillow; OpenCV 4 with its Haar face detector; torch, torchaudio, demucs and soundfile; ffmpeg and ffprobe with `libx264`, `libvpx-vp9` and `minterpolate`; Node, for `npx hyperframes@0.9.2`.

**Files no script makes.** The old session made these by hand, and the commands it used are not recorded. Since 9 Nov, `tools/rebuild/rebuild_media.sh` supplies all three, as below and in §8.4.
- **The transcripts and their audio.** `dimon-work/tx/pk_vo/transcript.json` and `dimon-work/tx/pk_bank/transcript.json` are Parakeet word lists: JSON arrays of `{text, start, end}`. `dimon-work/tx/bank_quote.wav` and `dimon-work/vo/vo16k.wav` are 16-bit PCM WAV files.
  - `build5.py` cannot run at all, not even `--specs`, without them. The kit makes the two WAVs with ffmpeg and copies the two transcripts from `tools/rebuild/clock/`. With them, `build5.py` reproduces the committed v5 files byte for byte (checked 9 Nov).
  - The pinned CLI has `transcribe --engine parakeet`, but whether the old session used it is not recorded. The kit's transcripts were made with it (parakeet-tdt-0.6b-v3) and passed the byte-for-byte check above.
  - If a new transcript splits the words differently, every hard-coded word number shifts. Print the word list and check the fixed points before trusting a build: word 55 must be "Meet", word 101 "fired" and word 223 "today".
  - The code always puts "You" back at position 25 of the quote, so a transcript that already includes it would show it twice.
  - The best check is to rebuild before changing anything: `git diff --stat` should then show no changes.
- **The S06 cut-out of Dimon.** `assets/clips2/BANK_27305_820_x63_50_135_cut.webm` is Dimon cut out of the interview, so the globe picture sits behind him. The edit uses it, but the clip is not flagged `matte`, so `prep5.py` skips it. Either add `matte=True` to the `IV_CID = CL(...)` call (line 1937), or run the same `remove-background` command by hand, as the kit's step 8 does (with the CLI's default quality; v4's flag is not recorded). The 9 Nov rebuild made it this way, and S06 then matched the share render at 23.6–31.7 s.
- **The paper texture.** `assets/tex/paper_light.png` is the window-lit paper used in S04, S07, S13, S18 and S22; REFERENCES.md says S04 uses "your paper and window light". It is the Pattinson v5 edit's window-light paper (`make_paper_light()` on `claude/pattinson-v5-notes5`). `tools/rebuild/paper_light.py` is the same generator and reproduces that committed file byte for byte.

### 7.4 Checking, looking at frames, and rendering

**Checking.**
- `npm run check` runs `npx --yes hyperframes@0.9.2 check` with the default 9 samples and the contrast check.
- REVIEW.md records each passing run from v3 to v5 as "`check` (5 samples, contrast pass off)". In the pinned CLI that is `npx --yes hyperframes@0.9.2 check --samples=5 --no-contrast`.
- The reason, from v3: "The full 9-sample run stalls in the checker's overlap pass on a film this dense." Adding `--range=0,31.7` limits the timed samples to that stretch.
- Before building, run `python3 -I tools/check_shots.py media_v5.json`.

**Warnings left on purpose.**
- In v5: the typed letters of "Chase" and the roller years are flagged as too brief (REVIEW.md: "the whole word holds, and the years flick by design"); WebGL performance notices; layout-density warnings in the later scenes.
- In v3: `line_unread` on the roller years, calendar pages and counter steps; `text_below_floor` on the "person 0.97" face-box labels.
- In v1: `composition_file_too_large` and `timeline_track_too_dense` on `captions.html`.

**QA frames** (seconds, from SPEC.md, word for word): 1.2, 4.05, 10.2, 11.3, 13.4, 16.9, 18.9, 26.0, 30.7, 35.6, 36.3, 40.0, 41.4, 46.5, 49.2, 50.0, 53.7, 56.5, 59.8, 61.2, 62.7, 64.0, 65.95, 66.95, 68.2, 73.2, 77.1, 78.6, 80.0, 82.8, 85.7, 87.8, 89.4, 91.2. These date from v2. The 0–31.7 s part was retimed in v4 and v5, so check those times against the current beats. They can be passed straight to `snapshot --at`.

**Looking at frames.**
- Use `npx --yes hyperframes@0.9.2 snapshot --at <times>`, or `--range A,B`, or `--review`.
- v5 was checked on about 110 frames across 0–31.7 s, and side by side with the reference reels. The result for each note is in REVIEW.md.
- The sound levels were measured, not listened to.

**Rendering.**
- `npm run render` renders the whole film to `renders/<project>_<date>_<time>.mp4`.
- v4 and v5 were rendered only for 0–31.7 s, as `renders/jpm-dimon-v4-0-31.mp4` and `renders/jpm-dimon-v5-0-31.mp4`. The pattern is the round, then the range in whole seconds.
- The exact render command is not recorded. In the pinned CLI the equivalent is `npx --yes hyperframes@0.9.2 render --end 31.7 -o renders/jpm-dimon-v5-0-31.mp4`; use `--start` for a later stretch.
- `renders/` is not in git. What is in it now: §2.

**Live preview:** for an agent, `npx hyperframes preview --background` (check it with `--status`, stop it with `--stop`); for a person, `npm run dev`.

### 7.5 Look, type and motion (as the v5 code has them)

**Colours:** background #070707; text in warm white #FBF8EC; red #E5381B used only for the NYT marker and the data page.

**Colour grades** (`GR` in `build5.py`, chosen per shot with `grade=` and written as HyperFrames `data-color-grading`; every grade starts from `base_grade.json`):
- **`doc`, the default documentary base:** contrast +0.16, highlights −0.16, saturation −0.2, temperature +0.05, vignette 0.34, grain 0.07, scanlines 0.08, colour fringing 0.03.
- **From v1 to v3:** `warm` and `teal`; `bw` (archive footage); `crt` (TV news: screen curvature 0.2, scanlines 0.36); `gold` (bloom, for "the golden boy"); `glitch` ("broken"); `dirty` (the shot before the clean wipe); `blurbg`; and the boxing-strobe looks `halftone`, `twoink`, `mono`, `dither` and `print`.
- **Added in v5:**
  - `dim`, `night` and `dark`: exposure −0.55, −0.32 and −0.95 (`night` is on the flag and the tower);
  - `clean`: a light grade for stills (photos on paper, and the Weill faces);
  - `ghost`;
  - `hcrt`, `hbg` and `hcard`: the Hemant stage, with CRT lines (scanlines 0.2 at count 0.5); `hbg` adds a 0.9 blur for the defocused background.
- **A rule from the code:** a picture laid over others with a blend mode is blurred with CSS, not graded, because "a grading pass would drop its blend mode".

**Textures and grain** (v5, from the note "Textures too heavy; use CRT lines and noise, lighter"):
- **Per scene:** `ht_grunge` as an overlay at 0.10 and `ht_paper` as soft light at 0.04, set with `Scene(tex=...)`. S02 and S06 use 0.05 and 0.
- **On black backgrounds:** `ht_grunge` in screen mode at 0.05.
- **On the S17 data page:** `ht_warm` in multiply mode at 0.42.
- **Grain:** `grain.html` is written by `write_aux()` from the grain component. It is that component's noise at 6 % in overlay mode over the whole film (z 150). Every 1/12 s it jumps between ten positions using GSAP `tl.set`, which can be scrubbed to any frame, in place of the component's CSS animation.
- **CRT lines:** they come from the grades' scanlines, not from a separate layer.

**Type.** Since v4 there are two families only: Inter Tight (in the role of Helvetica) and Instrument Serif Regular with a glow. No italics and no Satoshi. Mostly one family per line: REVIEW v4 set that rule for 0–31 s only, with exceptions, and the code does not enforce it (the `build5.py` header's "A caption line keeps one family" overstates it). Six lines mix the two families: "man in America", "right now", "in 30 countries", "in the world", "crisis hit" and "every single day" (§3.3). Lines do not slide; each word lands where it ends up. The section comment in `build5.py` that says lines slide is out of date.

Styles are set in `STY`. You use them by code in `cap()`, and `@N` overrides the size (for example `sh@180`).

| Code | Font | Size (px) | Kind |
|---|---|---|---|
| `s` / `sm` / `b` | Inter Tight 700 / 600 / 800 | 84 / 62 / 160 | sans |
| `ss` / `sl` | Instrument Serif | 92 / 128 | serif |
| `sh` / `sx` | Instrument Serif | 236 / 300 | hero |
| `nm` | Instrument Serif | 250 | name |
| `gold` | Instrument Serif | 236 | gold glow |
| `ink` / `inkb` | Inter Tight 700 / 800 | 64 / 120 | black on paper |
| `p` / `pb` / `ps` | Inter Tight 800 / 800 / Instrument Serif | 96 / 150 / 250 | paper |

**How caption words arrive** (`build_captions()`):
- **sans:** fades in and sharpens from 16 px blur in 0.24 s (expo.out) while its glow settles from a bloom to rest.
- **serif:** a glowing white box sits on the word's spot from 4 frames to 1 frame before it (SPEC.md calls it a 2-frame flicker box), then the word lands with blur 8, then 3, then 0 px over 3 frames.
- **hero, name and gold:** one blown-out frame (blur 14 px, bloom, 104 % size), then soft frames, crisp with a halo by frame 4.
- **ink:** sharpens from 6 px blur in 2 frames.
- **paper:** rises 44 px in 4 steps over 0.28 s.

**How caption groups behave:**
- A group appears 2 frames before its first word.
- It leaves at `end=` when one is given. Otherwise it stays until 2 frames before the next group's first word, unless that would keep it up more than 1.4 s after its own last word; then it leaves 1 s after that word.
- Exits are a cut (the default), `blur` (0.18 s) or `fade` (0.12 s).
- `scrim=` puts a soft dark patch behind the group, and `blinks=` hides it for a few frames.
- Commas and full stops are removed from caption words, except in "$10", "$60" and "$500".

**The captions file.** Every caption in the film is in one file, `compositions/captions.html`. It sits at z 100, above the scenes and below the grain. Groups are named `cg000` onward, in order of their first word, and each word is placed from the font's measured widths. The big words that are part of an effect are not in this file: BIGGER, JPMorgan Chase, the Wolf lockup, "by his own mentor", the fired page, the rollers, the counters, the typed words and the data page all live in the scene files, inside their `sp_*` functions.

**Cuts, flashes and camera moves.**
- **Cuts:** they land 0.05 s before the word (`CUT`). One frame is `F1` = 1/30 s.
- **Flashes:** `neg()` gives one or two negative frames on cuts that change place or time; `flash()` is a white flash, and `whiteframe()` is one solid white frame; `blk()` draws the glitch boxes from the references; `streak()` is a bright horizontal streak.
- **Camera moves:** a shot gets at most one steady push (`ease: "none"`), set per shot with `push=`: most go from 1.00 to 1.02–1.04 (the montage default is 1.025), some to 1.05–1.08, one pulls back 1.15 → 1.00, and some shots have none (`push=None`); the counts are in §6.2. `punch()` is a hard punch-in set on a single frame, never eased; `pan_arrive()` makes a shot arrive still moving and settle in 0.34 s.
- **Slow motion:** a recommendation, not a rule the code follows. Prefer a smooth slow-motion file made with `slowmo()` in `prep5.py` and played with `s.vfile()`, as v5 does for the Wolf, the CEO walk, the flag and the tower, and do not add new `rate=` slow-downs. REVIEW v5: "v4 had the player slow it, which repeated frames unevenly and read as a jump at 14.37." v5 still has two player-rate shots: s01's opening Lower Manhattan shot (`GAME_0_82`) slowed to 0.9× (`{"rate": 0.9}`, line 1779), a candidate for `slowmo()`, and the S10 palm strike (`FIRED_9693_161`) sped up to 1.4× (`rate=1.4`, line 2056).

### 7.6 To change X, edit Y

| The note | What to edit in `tools/build5.py` (unless another file is named) | Then run |
|---|---|---|
| Swap a shot | In the scene's block, change the shot entry `(film_t0, KEY, src_t, {opts})` or the call `s.v(KEY, src_t, t0, t1, ...)`. `KEY` is a source from `V` in `prep2.py`, and `src_t` is the number of seconds into that source. For framing use `xyz=(cx, cy, zoom)` or `frame=`; for colour use `grade=`. To use a new source file, put it in `dimon-src`, give it a key in `V` in `prep2.py`, and add it to `VERT` or `FRAME_OF` in `build5.py` if it is vertical or has a channel logo. | A |
| Swap a photo | Edit its `ST(...)` entry or the list it is in (lines 157–224, and `CARD` at line 1758). Some photos are made by prep scripts: the Weill faces from `WEILL` in `prep5.py` (source file or `KEY@seconds`, face width), the young-Dimon squares from `YOUNG` in `prep5.py`, cut-outs from `CUT_SRC` in `prep2.py`, and the globe from the image in `dimon-src/_globe/`. `faces.py sheet` helps you choose. A photo whose settings change but whose name stays the same is not remade: rename it, delete the old file, or name it on the `prep2.py` command line. | A (plus `prep4.py` or `prep5.py` if they make it) |
| Move a cut, or make a shot longer or shorter | Change the shot's `t0` and `t1` in its scene block. They are tied to words (`CUT(VT(i))`), so add or subtract seconds, or point at a different word. The clip's name changes with its length, so the clip must be cut again. | A |
| Retime a caption word | In its `cap()` call, replace `W_(i, "s")` with a fixed tuple such as `("word", 12.34, "s")`, or point it at a different word. The open's word times are in the `NEWS` table (line 106). | B |
| Move a whole block of voice | Change `VO1_AT` (line 99, narration part 1), the 35.25 anchor in `VO2_OFF` (line 101, narration part 2) or `QUOTE_AT` (line 102, Dimon's quote). The audio and everything keyed to words (`VT`, `QT`, `CUT`: most cuts and the word-keyed captions) move with them, but many v4/v5 beats are typed-in film seconds that stay put, so picture and sound drift apart unless you shift these by hand: S01 `POP0 = 8.60` (line 1763; the slide-up runs from it to `VO1_AT`); S02 `OPEN_END = 10.70`, the live frames 9.15–10.52 and `grey_until=9.55`, the blocks at 9.433, 9.467, 9.50 and 10.01, the band and the blink at 10.50, and the cards at 10.86, 11.00, 11.20 and 11.40 (lines 1814–1846); S03 12.83 and the cards at 13.32–13.50 (lines 1852–1860); S04 `BON = 18.74` and 19.62 (lines 1898–1905); S06's end, its last shot's end and S07's start at 34.85, and the caption end 34.80 (lines 1930, 1994–2003). Recompute the `dimon` clip's 11.25 s duration in `write_root()` (line 2337). S01's other times (7.92, 8.50, `JPMC_T`) follow the news voice, which these anchors do not move. A shot that runs between a time that moves and a time that does not changes length, so it gets a new clip id and needs a new file: the S02 live clip and both matted SPEAK clips, S05's last shot, S06's last shot and S23's last shot among them. Check `git diff tools/media_v5.json` for new ids. A `prep5.py` slow-motion file whose shot changes length (`tower_slow.mp4` ends at `VO1_AT`) must be deleted and made again, because `prep5.py` skips files that exist. If the film's total length (`DUR`, 93.2 s) changes, the music bed in `make_music.py` must be re-cut. | A, plus `prep5.py` for the SPEAK mattes |
| Change which words appear together | The `cap()` groups: each line is a list of words, and each `cap()` call is a separate group. | B |
| Change how a caption looks or where it sits | For one group: `cap(..., x=, y=, align=, exit=, scrim=, end=, lh=)`. For one word: its style code. For everything: `STY`, `INK`, the glow settings (`GLOW_*`, `SERIF_*`, `GOLD_REST`) and the entrances in `build_captions()`. For the big words in effects: the `sp_*` call's settings (for example `size=`, or the letter times in `JPMC_T`) or the function itself. | B |
| Texture, grain or scanline strength | Per scene: `Scene(..., tex=(grunge, paper))`; the default `(0.10, 0.04)` is set in `Scene.__init__`. Grain: `opacity: 0.06` in `write_aux()`. Grain, scanlines and vignette inside the grades: `DOC_D`, `DOC_E`, `HCRT` and the `GR` entries. Black backgrounds: the `.bktex` opacity in `Scene.write()`. Different texture images: `TEXTURES` in `prep_media.py`. | B (and `prep_media.py` for new images) |
| Colour of a shot | `grade=` on the shot; add or change a grade in `GR`. | B |
| Slow a shot down | Add a `slowmo()` line in `prep5.py` and play the file with `s.vfile("name.mp4", t0, t1)`. | `prep5.py`, then B |
| Music or voice volume | The loudness targets in `make_music.py` (music −30, voice −16) or `prep_media.py` (narration and quote, −16). Or set a `data-volume` per audio clip in `write_root()`; every clip is at 1 now. | That script, then B if the HTML changed |
| Add an effect from a reference reel | 1. Measure the reference frame by frame at its own frame rate; REFERENCES.md shows the method (times, sizes, positions, eases). The reels in `dimon-src/_drive` are `larry fink metro media house.mp4`, `Copy of dario vidoe.mp4`, `Copy of hemant taneja vid.mp4`, `bill ackman metro medi ref.mp4`, `was fired part ref.mp4` and `we bank countries part.mp4`; the Pattinson film is in `pattinson-v5`. 2. Look for a ready-made block in the HyperFrames library first (the grain came from there). 3. Write a new `sp_<name>(sc, t0, t1, ...)` next to the v5 effects. Build it from `sc.raw(html, js)`, give every timed element `class="clip"` and `sc.timed()`, use `sc.at()` for timeline positions, `F1` for frame-exact steps (`tl.set` for choppy low-frame-rate motion) and `blk()` for glitch boxes. 4. Call it from the scene block at word times. 5. Write the measurements in REFERENCES.md and the note and its result in REVIEW.md. | A if it needs new media, otherwise B |
| Flashes and negative frames | The `s.neg()`, `s.flash()` and `s.whiteframe()` calls in the scene; the film-wide list is at line 2282. | B |

**A** = `build5.py --specs`, then `prep2.py --spec=media_v5.json` (plus `prep4.py` or `prep5.py` if their outputs change), then `check_shots.py media_v5.json`, then B.

**B** = `build5.py`, then `check --samples=5 --no-contrast`, then `snapshot --at` the moments you changed (side by side with the reference for a reference effect), then render that stretch.

**Starting a new round.** Earlier rounds copied the builder (for example `build5.py` to `build6.py`) and wrote a new media list. If you do that, also change the file name in the new builder's `json.dump`, the name you pass to `prep2.py` with `--spec=`, and the `media_v5.json` written into `prep5.py`.

**Prep scripts skip files that already exist.** If a run was interrupted and left a broken or empty file, delete it before running again.

---

## 8. Open questions and next steps

### 8.1 Open, from REVIEW.md (v5), word for word
- **"was fired" reference:** used for "a guy who got fired"; tell me if it was meant for "he was fired" at 48 s.
  - For context: `build4.py` marks the S04 page `a guy who got FIRED: the was-fired reference's opening (user)`, but REVIEW v4 and v5 both still ask the question, and no answer is recorded.
- **Faces in "by his own mentor":** some of Weill's photos are small. To fill the frame without a seam they are scaled up, so the biggest close-ups are soft. They are on screen for 2–3 frames each.

### 8.2 Still unanswered from earlier rounds
- **"You have to be big…" (31.7–34.85 s).** REVIEW v4: "it still follows your lines". Dropping it would shorten the film by about 3 s, and the music bed, timed to end on the last frame, would need re-cutting. v5 does not mention it, so the answer is unknown. The stretch is untouched since v4 (v3 picture; v4 made "big" Inter 800 200).
- **31.7–93.2 s (s07–s23).** No notes on this part are recorded after v3's general notes. It is still v3's cut, in v4's type with v5's lighter textures, and no render of it is recorded since v3. s07, s08, s10, s12, s15, s17 and s20 have not changed since v2, apart from v4's type and v5's textures (REVIEW v3 at most lists their set pieces as "Kept from v2"; they were last described in `git show a9e958c:jpm-dimon/REVIEW.md`, and neither review mentions s20).

### 8.3 Where the committed film differs from the notes
Nothing was changed; these are differences found while mapping the film.
- **S06 is missing three Fink effects.** REFERENCES.md (v5: "the glitch boxes, the glint on the picture, and the 3-frame wipe before "the IMF"") and the `build5.py` header ("the Fink screen's glitch boxes, glint and white-block wipe in S06") say v5 added them. The committed `compositions/s06.html` has none of them: only the ghost, the matte, the quote marks and the B-roll. REVIEW.md's S06 section does not list them.
- **S03 has no block glitch into the Wolf.** REFERENCES.md (v5: "the block glitch in") and the `build5.py` header ("a block glitch into the Wolf") list Ackman's block glitch. The committed S03 enters the Wolf with an inverted frame (13.687) and an arrival in motion; its only blocks are the four soft white boxes before the photo cards and the purple inverted frame at 14.998.
- **The caption "Chase" never appears.** Group `cg063` ("and / Chase") runs 87.078–87.255, but "Chase" is spoken at 87.305, after the group has ended, where the JPMorganChase wordmark sweep starts (87.255).
- **The two Hemant passes disagree.** The first pass gives the second red box at 24.88 and the exit at 25.05 (the frame defocuses). The second pass gives 24.92 and 25.08 (a white band). v5 follows the second pass.
- **SPEC.md is still the v2 spec** in its build steps, open, music, type, textures, reference list and camera rule (§6.4).

### 8.4 What a rebuild needs (all handled by `tools/rebuild/rebuild_media.sh` since 9 Nov)
The old session left these out of git; the kit supplies each one.
- **`dimon-work/tx/` and `dimon-work/vo/`** (the transcripts and their audio), without which `build5.py` cannot run. The kit makes the two 16 kHz WAVs with ffmpeg (output seeking for the interview: input seeking moves "Bank," by 80 ms) and copies the verified Parakeet transcripts from `tools/rebuild/clock/` (md5 `7f0a1a9e…` and `f4d962f8…`). Re-running Parakeet is not needed, and on another machine it might not give identical word times.
- **`brotli`:** fontTools needs it to read the `.woff2` fonts, and `build5.py` measures text while it loads, so without it even `build5.py --specs` fails. The kit installs it.
- **OpenCV 4 for `faces.py`:** OpenCV 5 has no `cv2.CascadeClassifier`, and `prep5.py` imports `faces.py` at the top. The kit installs opencv-python-headless 4.14.0.94 into `dimon-work/cv4` and passes it as `CV4_DIR`.
- **The S06 matte** (`BANK_27305_820_x63_50_135_cut.webm`) is made by no committed script (v4 ran `npx hyperframes@0.9.2 remove-background` by hand). The kit's step 8 runs the same call; its quality flag in v4 is unknown (the kit uses the CLI default).
- **`assets/tex/paper_light.png`** comes from the Pattinson v5 edit (`make_paper_light()` in `pattinson-v5/tools/prep_media.py` on `claude/pattinson-v5-notes5`, committed there as blob `e38093a8`). The kit's `paper_light.py` is the same generator and reproduces that file byte for byte (md5 `63a1d9e9949ef55d94a8598a73c4c33a`).
- **Local folder links** (`tools/rebuild/links.tsv`): `_weill/weill_1.jpg` = `sandie weil images/images (1).jpg` and `_weill/weill_0.jpg` = `images.jpg`. Both were matched against the v5 share render: wf0 at film 17.015 s and wf3 at 17.282 s, and all eight wf slots at r = 0.97–0.99. `_globe/` = `jamie ghost image.webp`, which the render supports over the drawn stand-in. `_wolf2/wolf_first_part.mp4` (prep2's WOLF2 key) is unused in v5 and not linked.

### 8.5 Coded but unused; never built
- **Still in `build5.py` but not called** (seven functions): `sp_mask_word` (v2's BIG word mask with the dive through the letter), `sp_seal_ring` (the Fink seal ring), `sp_seal_portrait` (the seal punch-in), `sp_face_boxes` (S03 now builds its face boxes inline), `sp_cards` (photo cards landing one after another on a dark ground), `sp_drop` (the logo drop) and `sp_flip_collage` (the mortgages collage).
- **Never built:** the animated AI image-to-video portrait (an open item in the Fink document) and the donut charts around the eye.

### 8.6 Not recorded in the files (unknown)
- **v1–v3 reviews:** how the user saw these versions; no render is named for them.
- **Note wording:** the user's exact words for the v1, v2, v4 and v5 notes. Only the paraphrases and fragments quoted in §4 survive, plus one v4 sentence word for word: the S02 note quoted in `build4.py`'s `sp_freeze_pop` docstring ("An interview plays, you pause that picture, and then the picture comes up at the centre with that glow"), which names no speaker but reads as the user's (§4 v4).
- **4K:** REVIEW v4 says the interview "is 1080p, not 4K"; whether the user asked for 4K is not recorded.
- **The P01 file name:** what the user's Pinterest file name "2008 8 crash for first kind chess part." asks for (§4 v1) is not recorded, including whether it was meant for the 2008 crash beat.
- **Where some references came from:** the AMD reel, "the Dimon reference reel" behind v1's captions, and the Dario and Hemant reels before their Drive copies appeared on 6 Nov at 18:20. v1's lockups ("30 / Countries", "We bank / IMF") resemble the we-bank reel described in `REFERENCES.md`, but that reel's Drive copy (`we bank countries part.mp4`) only arrived on 6 Nov.
- **The globe picture:** the old files do not name the file behind "your globe picture" (`prep4.py` reads it from `dimon-src/_globe/`). `jamie ghost image.webp` (added to Drive at 17:23 on 6 Nov, before v4) is the one the share render supports, and the rebuild uses it.
- **Full-length render:** whether the old session ever made a full 0–93.2 s render of v4 or v5. This session made the first recorded one on 9 Nov (§2).
- **The share render:** how `jpm-dimon-v5-0-31-share.mp4` differs from the original `jpm-dimon-v5-0-31.mp4`. It is a 10.4 Mbps encode, lighter than a default HyperFrames render.

### 8.7 Next steps
1. **Watch what exists.** `jpm-dimon/renders/jpm-dimon-v5-0-31-share.mp4` (the old session's 0–31.7 s) and `jpm-dimon/renders/jpm-dimon-v5-full-share.mp4` (the whole film, rendered 9 Nov). On a fresh session, run `tools/rebuild/rebuild_media.sh` first (§2).
2. **Answer the open questions** in 8.1 and 8.2: where the "was fired" reference belongs, whether to keep "You have to be big…", whether the soft Weill close-ups need other photos, and notes on 31.7–93.2 s, which has had none since v3.
3. **Decide on the differences in 8.3:** whether the missing S03 and S06 effects should be added, and whether the "Chase" caption should show.
4. **Before the first change** on a fresh session, run `bash jpm-dimon/tools/rebuild/rebuild_media.sh`. It ends by running `build5.py` and confirming that `git diff` shows no changes to the composition (§8.4).
5. **For each note,** edit `build5.py` as in §7.6, rebuild, run `check --samples=5 --no-contrast`, snapshot the changed moments (side by side with the reference where there is one), and render the changed stretch. Record the note and its result in `REVIEW.md` and any new measurements in `REFERENCES.md`.
