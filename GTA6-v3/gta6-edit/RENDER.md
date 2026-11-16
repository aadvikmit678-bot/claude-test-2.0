# GTA 6 edit (v4, new type) — HyperFrames project

The whole video, 1920x1080, 1:30.7. Needs Node.js 22+, FFmpeg and Chrome, and an internet connection
(index.html loads GSAP from cdn.jsdelivr.net).

Highest quality, 60 fps (from this folder):

    npx --yes hyperframes@0.9.46 render --fps 60 --quality delivery --crf 12 --output renders/gta6_v4_type_60fps.mp4

30 fps:

    npx --yes hyperframes@0.9.46 render --fps 30 --quality delivery --output renders/gta6_v4_type.mp4

Preview / edit in the browser:

    npx --yes hyperframes@0.9.46 preview

If Chrome is missing: `npx --yes hyperframes@0.9.46 browser ensure`.
Pinned to hyperframes 0.9.46, the version every render of this edit was made with.
Shots from 50/60 fps footage are cut at 60 fps, the rest at their own (<= 30 fps) rate.
The people in front of the giant words are VP9 WebMs with transparency (assets/clips/*_fg.webm); HyperFrames decodes
them with libvpx-vp9, which any standard FFmpeg build has.
