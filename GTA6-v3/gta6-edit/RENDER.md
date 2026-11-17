# GTA 6 edit (v4, new type) — HyperFrames project

The whole video, 1920x1080: the project renders 1:30.7 (5442 frames at 60 fps); the final drops 8 of them (below). Needs Node.js 22+, FFmpeg and Chrome, and an internet connection
(index.html loads GSAP from cdn.jsdelivr.net).

Highest quality, 60 fps (from this folder):

    npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 --output renders/gta6_v4_final_render.mp4

30 fps:

    npx --yes hyperframes@0.9.46 render --fps 30 --quality delivery --output renders/gta6_v4_final_30fps.mp4

Preview / edit in the browser:

    npx --yes hyperframes@0.9.46 preview

If Chrome is missing: `npx --yes hyperframes@0.9.46 browser ensure`.
Pinned to hyperframes 0.9.46, the version every render of this edit was made with.
Shots from 50/60 fps footage are cut at 60 fps, the rest at their own (<= 30 fps) rate.
The people in front of the giant words are VP9 WebMs with transparency (assets/clips/*_fg.webm); HyperFrames decodes
them with libvpx-vp9, which any standard FFmpeg build has.

The final (1:30.567, 5434 frames) has the user's own mix (their music and sound effects) as its sound and no pause
before "Ah shit": render as above, then ripple-delete frames 293-300 (CJ's silent lead-in) and put the mix on:

    ffmpeg -i renders/gta6_v4_final_render.mp4 -i final_mix/gta6_final_mix.m4a -filter_complex "[0:v]select='not(between(n\,293\,300))',setpts=N/60/TB[v]" -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 12 -pix_fmt yuv420p -c:a copy -movflags +faststart renders/gta6_v4_final_60fps.mp4

`final_mix/gta6_final_mix.m4a` is the user's "GTA6 final" sound with the money-counting effect taken out behind
"billion dollars" and the same 8 frames cut (at 4.87 s, in the silence before CJ), 90.567 s.
