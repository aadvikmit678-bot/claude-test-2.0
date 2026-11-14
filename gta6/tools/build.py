"""Build gta6/index.html and gta6/compositions/*.html from gta6/tools/edit.py.   python3 -I gta6/tools/build.py"""
import os, sys, html, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edit

PROJ = f"{edit.ROOT}/gta6"
COMP = f"{PROJ}/compositions"
F1 = 1 / edit.FPS
END = edit.END
INK, DARK = "#FBF8EC", "#0E0E0E"
# the Dimon / Pattinson glow (jpm-dimon/tools/build18.py)
SERIF_REST = ("0 0 14px rgba(255,255,255,0.62), 0 0 42px rgba(255,255,255,0.30), 0 0 90px rgba(255,255,255,0.12), "
              "0 3px 10px rgba(0,0,0,0.35)")
SERIF_BLOOM = ("0 0 22px rgba(255,255,255,1), 0 0 60px rgba(255,255,255,0.95), 0 0 130px rgba(255,255,255,0.7), "
               "0 3px 10px rgba(0,0,0,0)")
SERIF_SOFT = ("0 0 18px rgba(255,255,255,0.85), 0 0 50px rgba(255,255,255,0.45), 0 0 100px rgba(255,255,255,0.18), "
              "0 3px 10px rgba(0,0,0,0.2)")
HERO_BLOWN = ("0 0 26px rgba(255,255,255,1), 0 0 70px rgba(255,255,255,1), 0 0 150px rgba(255,255,255,0.85), "
              "0 0 240px rgba(255,255,255,0.5)")
HERO_HALO = ("0 0 16px rgba(255,255,255,0.80), 0 0 46px rgba(255,255,255,0.46), 0 0 110px rgba(255,255,255,0.24), "
             "0 3px 10px rgba(0,0,0,0.40)")
D_REST = "0 0 0 rgba(0,0,0,0)"
D_BLOOM = "0 0 16px rgba(0,0,0,0.55), 0 0 40px rgba(0,0,0,0.30)"
D_SOFT = "0 0 8px rgba(0,0,0,0.35)"
FONTS = """
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Regular.woff2') format('woff2'); font-weight: 400; font-style: normal; }
  @font-face { font-family: 'Instrument Serif'; src: url('assets/fonts/InstrumentSerif-Italic.woff2') format('woff2'); font-weight: 400; font-style: italic; }
  @font-face { font-family: 'Hand'; src: url('assets/fonts/NothingYouCouldDo-Regular.ttf') format('truetype'); }
  @font-face { font-family: 'Pixel'; src: url('assets/fonts/Silkscreen-Regular.ttf') format('truetype'); }
"""


def r3(x):
    return f"{x:.3f}"


def fr(x):           # snap to the film's frame grid
    return round(round(x * edit.FPS) / edit.FPS, 3)


def esc(s):
    return html.escape(s, quote=True)


def all_cuts():
    """Every cut in film time: beat starts and the hard cuts inside multi-segment beats (frame-snapped)."""
    c = set()
    for b in edit.S:
        c.add(fr(b["a"]))
        a = b["a"]
        for seg in b.get("segs") or []:
            if seg[2] is not None:
                c.add(fr(seg[2]))
    return sorted(c)


CUTS = all_cuts()


def cut_in(lo, hi):
    """The first cut c with lo < c <= hi, or None."""
    for c in CUTS:
        if lo < c <= hi + 1e-9:
            return c
    return None


def last_cut_at_or_before(t):
    best = 0.0
    for c in CUTS:
        if c <= t + 1e-9:
            best = c
    return best


_FONT_TTF = {False: "/mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSerif-Regular.ttf",
             True: "/mnt/skills/examples/canvas-design/canvas-fonts/InstrumentSerif-Italic.ttf"}
_FONTS = {}


def text_w(txt, size, italic=False):
    """Advance width of a word in Instrument Serif at `size` px (PIL with the TTF; an estimate without it)."""
    try:
        from PIL import ImageFont
        key = (italic, int(round(size)))
        if key not in _FONTS:
            _FONTS[key] = ImageFont.truetype(_FONT_TTF[italic], key[1])
        return _FONTS[key].getlength(txt) * (0.98 if italic else 0.99)   # the -0.01/-0.02 em tracking
    except Exception:
        return len(txt) * size * 0.40


HALO = ", 0 0 3px rgba(0,0,0,0.32), 0 0 18px rgba(0,0,0,0.42)"   # v2: a dark halo under the glow on scrimmed groups


def beat_at(t):
    for b in edit.S:
        if b["a"] - 1e-6 <= t < b["b"] - 1e-6:
            return b
    return edit.S[-1]


def comp_file(cid, css, body, js, dur):
    open(f"{COMP}/{cid}.html", "w").write(f"""<template>
  <style>{FONTS}
  #root {{ position: absolute; inset: 0; overflow: hidden; }}
  #root .box {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: hidden; }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to({{}}, {{ duration: {r3(dur)} }}, 0);
{chr(10).join('    ' + j for j in js)}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""")


# ------------------------------------------------------------------ captions
def build_captions():
    els, js = [], []
    css = f"""  #root {{ pointer-events: none; }}
  #root .cg {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }}
  #root .anchor {{ position: absolute; transform: translate(-50%, -50%); }}
  #root .drift {{ position: relative; }}
  #root .ln {{ position: relative; white-space: nowrap; line-height: 1.0; font-family: 'Instrument Serif'; font-weight: 400; letter-spacing: -0.01em; }}
  #root .w {{ display: inline-block; position: relative; }}
  #root .wt {{ display: inline-block; position: relative; opacity: 0; -webkit-text-stroke: var(--sw, 0px) currentColor; paint-order: stroke fill; }}
  #root .it {{ font-style: italic; letter-spacing: -0.02em; }}
  #root .fl {{ position: absolute; left: -0.03em; right: -0.03em; top: 0.22em; bottom: 0.10em; opacity: 0;
    background: #ffffff; box-shadow: 0 0 16px rgba(255,255,255,0.9), 0 0 44px rgba(255,255,255,0.45); }}
  #root .dk .fl {{ background: #141414; box-shadow: 0 0 14px rgba(0,0,0,0.5); }}
  #root .fl.bar {{ top: 0.06em; bottom: 0.12em; left: -0.08em; right: -0.08em; }}
  #root .sk {{ position: absolute; left: 0; right: 0; top: -0.30em; bottom: -0.30em; opacity: 0;
    background: repeating-linear-gradient(90deg, rgba(255,255,255,0.95) 0 3px, rgba(255,255,255,0) 3px 10px); }}
  #root .yi {{ display: inline-block; line-height: 0.8; }}
  #root .scrim {{ position: absolute; pointer-events: none; }}
  #root .cnv {{ position: absolute; left: 0; top: 0; transform: translate(-50%, -50%); white-space: nowrap; line-height: 1;
    font-family: 'Instrument Serif'; letter-spacing: -0.01em; color: {INK}; }}
  #root .cnt {{ display: inline-block; opacity: 0; text-shadow: {SERIF_REST}; }}
"""
    prev, spans_t = [], []
    for g in edit.C:
        gid = g["id"]
        dark = g["ink"] == "dark"
        INKc = DARK if dark else INK
        REST, BLOOM, SOFT = (D_REST, D_BLOOM, D_SOFT) if dark else (SERIF_REST, SERIF_BLOOM, SERIF_SOFT)
        halo = bool(g.get("scrim")) and not dark
        if halo:
            REST, SOFT = REST + HALO, SOFT + HALO
        HHALO = HERO_HALO + (HALO if halo else "")
        lines, cur = [], []
        toks = g["text"].split()
        wi = 0
        for tok in toks:
            if tok == "|":
                lines.append(cur); cur = []
                continue
            cur.append((tok, g["words"][wi])); wi += 1
        lines.append(cur)
        t_sp = g["words"][0][1]
        a_first = fr(max(0.0, t_sp - F1))
        c = cut_in(a_first - 1e-6, fr(t_sp + F1))
        if c is not None:              # v2: the first word is spoken on a cut: the group starts on the cut, no square
            a_first = t0 = c
        else:
            t0 = fr(max(a_first - 4 * F1, last_cut_at_or_before(a_first), 0.0))
        for pend, py, px, pid in prev:  # a group still showing that ends during this one's lead-in: this one waits
            if t0 < pend - 1e-6:
                if pend <= a_first + 3 * F1 + 1e-6:
                    t0 = fr(pend); a_first = fr(max(a_first, t0))
                elif abs(py - g["pos"][1]) < 260 and abs(px - g["pos"][0]) < 700:
                    print(f"WARNING: {gid} overlaps {pid} by {pend - t0:.2f}s in the same place")
        prev.append((fr(g["end"]), g["pos"][1], g["pos"][0], gid))
        spans_t.append((gid, t0, fr(g["end"]), g["pos"][1]))
        t1 = fr(g["end"])
        assert t1 > t0, (gid, t0, t1)
        x, y = g["pos"]
        lines_html, line_ws = [], []
        for li, line in enumerate(lines):
            size = g["size"] if li == 0 or not g.get("l2") else g["l2"]
            style = f"font-size:{size}px;"
            if g["layout"] == "stack" and li > 0:
                style += f"margin-left:{g['indent']:.2f}em;margin-top:-0.14em;"
            spans = []
            for k, (tok, (spoken, t)) in enumerate(line):
                marks = ""
                while tok and tok[0] in "*!^#~=%":
                    marks += tok[0]; tok = tok[1:]
                word, _, sz = tok.partition("@")
                kind = ("hero" if "!" in marks else "yr" if "^" in marks else "dhl" if "#" in marks else
                        "streak" if "~" in marks else "dnorm" if "=" in marks else "weight" if "%" in marks else "serif")
                sid = f"{gid}-w{li}{k}"
                wsty = f"font-size:{sz}px;" if sz else ""
                cls = "w" + (" it" if "*" in marks else "")
                inner = esc(word)
                if kind == "yr" and len(word) >= 2:
                    inner = f'<span id="{sid}-y" class="yi">{esc(word[:2])}</span>{esc(word[2:])}'
                extra = f'<span id="{sid}-s" class="sk"></span>' if kind == "streak" else ""
                flc = "fl bar" if kind == "dhl" else "fl"
                spans.append(f'<span id="{sid}" class="{cls}" style="{wsty}"><span id="{sid}-f" class="{flc}"></span>{extra}'
                             f'<span id="{sid}-t" class="wt" style="color:{INKc};text-shadow:{REST}">{inner}</span></span>')
                a = fr(max(t0, t - F1))
                c = cut_in(a - 1e-6, fr(t + F1))
                if c is not None:          # v2: a word spoken on a cut appears on the cut, not a frame before it
                    a = c
                a = fr(max(a, t0))
                T = f"#{sid}-t"
                if kind == "serif":
                    b0 = fr(max(t0, a - 4 * F1))
                    cb = cut_in(b0, a - 1e-6)
                    if cb is not None:     # v2: the square stays inside the word's own shot
                        b0 = cb
                    if a - b0 >= 2 * F1 - 1e-6:
                        js += [f'tl.set("#{sid}-f", {{ opacity: 1, filter: "blur(3px)" }}, {r3(b0)});',
                               f'tl.set("#{sid}-f", {{ filter: "blur(0px)" }}, {r3(b0 + F1)});',
                               f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(max(b0 + 2 * F1, a - F1))});']
                    js += [f'tl.set("{T}", {{ opacity: 1, filter: "blur(8px)", textShadow: "{BLOOM}" }}, {r3(a)});',
                           f'tl.set("{T}", {{ filter: "blur(3px)", textShadow: "{SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("{T}", {{ filter: "blur(0px)", textShadow: "{REST}" }}, {r3(a + 3 * F1)});']
                elif kind in ("hero", "yr"):
                    js += [f'tl.set("{T}", {{ opacity: 1, scale: 1.04, filter: "blur(14px)", textShadow: "{BLOOM}" }}, {r3(a)});',
                           f'tl.set("{T}", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SOFT}" }}, {r3(a + F1)});',
                           f'tl.set("{T}", {{ scale: 1.005, filter: "blur(2.5px)" }}, {r3(a + 3 * F1)});',
                           f'tl.set("{T}", {{ scale: 1, filter: "blur(0px)", textShadow: "{REST if dark else HHALO if kind == "hero" and size >= 118 else REST}" }}, {r3(a + 4 * F1)});']
                    if kind == "yr" and len(word) >= 2:
                        for f_, on in ((6, 1), (8, 0), (10, 1), (11, 0)):
                            if a + f_ * F1 < t1 - 1e-6:
                                js.append(f'tl.set("#{sid}-y", {{ backgroundColor: "{INKc if on else "rgba(0,0,0,0)"}", '
                                          f'color: "{(INK if dark else "#0a0a0a") if on else INKc}", textShadow: "{"none" if on else REST}" }}, {r3(a + f_ * F1)});')
                elif kind == "dhl":
                    js += [f'tl.set("#{sid}-f", {{ opacity: 1 }}, {r3(a)});',
                           f'tl.set("{T}", {{ opacity: 1, color: "{INK if dark else "#0b0b0b"}", textShadow: "none" }}, {r3(a)});',
                           f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(a + 2 * F1)});',
                           f'tl.set("{T}", {{ color: "{INKc}", filter: "blur(7px)", textShadow: "{BLOOM if dark else HERO_BLOWN}" }}, {r3(a + 2 * F1)});',
                           f'tl.set("{T}", {{ filter: "blur(0px)", textShadow: "{REST if dark else HHALO}" }}, {r3(a + 3 * F1)});']
                elif kind == "streak":
                    js += [f'tl.set("#{sid}-s", {{ opacity: 1, scaleY: 1.8 }}, {r3(a)});',
                           f'tl.set("#{sid}-s", {{ opacity: 0.8, scaleY: 1.3 }}, {r3(a + F1)});',
                           f'tl.set("#{sid}-s", {{ opacity: 0 }}, {r3(a + 2 * F1)});',
                           f'tl.set("{T}", {{ opacity: 1, filter: "blur(6px)", textShadow: "{BLOOM}" }}, {r3(a + 2 * F1)});',
                           f'tl.set("{T}", {{ filter: "blur(2px)", textShadow: "{SOFT}" }}, {r3(a + 3 * F1)});',
                           f'tl.set("{T}", {{ filter: "blur(0px)", textShadow: "{REST}" }}, {r3(a + 5 * F1)});']
                elif kind == "dnorm":
                    b0 = fr(max(t0, a - 2 * F1))
                    cb = cut_in(b0, a - 1e-6)
                    if cb is not None:
                        b0 = cb
                    if a - b0 > 0.02:
                        js += [f'tl.set("#{sid}-f", {{ opacity: 1 }}, {r3(b0)});', f'tl.set("#{sid}-f", {{ opacity: 0 }}, {r3(a)});']
                    js += [f'tl.set("{T}", {{ opacity: 0.5, filter: "blur(1.5px)", textShadow: "{SOFT}" }}, {r3(a)});',
                           f'tl.set("{T}", {{ opacity: 1, filter: "blur(0px)", textShadow: "{REST}" }}, {r3(a + F1)});']
                else:   # weight: the Tesla reel's heavy frame, smeared, then the regular cut
                    js += [f'tl.set("{T}", {{ opacity: 1, "--sw": "0.045em", filter: "blur(1.4px)", textShadow: "{BLOOM if dark else HERO_BLOWN}" }}, {r3(a)});',
                           f'tl.set("{T}", {{ "--sw": "0.035em", scaleX: 1.04, filter: "blur(3px)" }}, {r3(a + F1)});',
                           f'tl.set("{T}", {{ "--sw": "0px", scaleX: 1, filter: "blur(0.6px)", textShadow: "{SOFT}" }}, {r3(a + 2 * F1)});',
                           f'tl.set("{T}", {{ filter: "blur(0px)", textShadow: "{REST}" }}, {r3(a + 3 * F1)});']
                spans.append(" ")
            lines_html.append(f'<div class="ln" style="{style}">{"".join(spans).rstrip()}</div>')
            lw = 0.0
            for k, (tok, _) in enumerate(line):
                wtxt = tok.lstrip("*!^#~=%")
                wword, _, wsz = wtxt.partition("@")
                wsize = float(wsz) if wsz else size
                lw += text_w(wword, wsize, "*" in tok[:3]) + (0.25 * size if k else 0)
            if g["layout"] == "stack" and li > 0:
                lw += g["indent"] * size
            line_ws.append((lw, max([size] + [float(t.partition("@")[2]) for t, _ in line if "@" in t])))
        scrim = ""
        bw = max(w for w, _ in line_ws)
        bh = sum(h for _, h in line_ws) * 0.92
        mx = max(h for _, h in line_ws)
        if bw / 2 > 960 - 96 or (g["layout"] != "stack" and abs(x - 960) + bw / 2 > 960 - 96):
            print(f"WARNING: {gid} is {bw:.0f}px wide; it leaves the 90% safe area")
        if g.get("scrim"):               # v2: a tight soft shadow behind the words, moving with them
            s_ = g["scrim"] * 0.85
            W_, H_ = int(bw + 2.4 * mx), int(bh + 1.9 * mx)
            scrim = (f'<div class="scrim" style="left:50%;top:50%;margin-left:{-W_ // 2}px;margin-top:{-H_ // 2}px;width:{W_}px;'
                     f'height:{H_}px;background:radial-gradient(closest-side, rgba(6,5,4,{s_:.2f}) 0%, rgba(6,5,4,{s_ * 0.72:.2f}) 38%, '
                     f'rgba(6,5,4,{s_ * 0.3:.2f}) 68%, rgba(6,5,4,0) 100%)"></div>')
        align = "left" if g["layout"] == "stack" else "center"
        els.append(f'<div id="{gid}" class="clip cg{" dk" if dark else ""}" data-start="{r3(t0)}" data-duration="{r3(t1 - t0)}" '
                   f'data-track-index="1" data-layout-allow-overflow data-layout-allow-overlap>'
                   f'<div class="anchor" style="left:{x}px;top:{y}px;text-align:{align}"><div id="{gid}-d" class="drift">{scrim}'
                   f'{"".join(lines_html)}</div></div></div>')
        if g["drift"]:
            d = t1 - t0
            js.append(f'tl.fromTo("#{gid}-d", {{ x: 0 }}, {{ x: {-g["drift"] * d:.1f}, duration: {r3(d)}, ease: "none", '
                      f'immediateRender: false }}, {r3(t0)});')
    ok_pairs = {("c1", "c2"), ("b1", "b2"), ("n3", "n3b"), ("b3", "b3b")}
    for i, (ga, a0, a1, ay) in enumerate(spans_t):
        for gb, b0_, b1_, by in spans_t[i + 1:]:
            ov = min(a1, b1_) - max(a0, b0_)
            if ov > 1.5 * F1 and (ga, gb) not in ok_pairs:
                print(f"NOTE: {ga} and {gb} are both on screen for {ov:.2f}s")
    # counters: a number rolling in place, fast then slowing, the last value landing with the hero bloom
    for cid, start, land, values, x, y, size, end in edit.COUNTERS:
        start, land, end = fr(start), fr(land), fr(end)
        n = len(values)
        times = []
        for i in range(n):
            u = i / (n - 1)
            times.append(fr(start + (land - start) * u * u))
        for i in range(1, n):
            if times[i] <= times[i - 1]:
                times[i] = fr(times[i - 1] + F1)
        spans = []
        for i, v in enumerate(values):
            inner = (f'<span id="{cid}-y" class="yi">{esc(v[:2])}</span>{esc(v[2:])}' if cid == "cn3" and i == n - 1 else esc(v))
            spans.append(f'<div class="cnv" style="left:{x}px;top:{y}px;font-size:{size}px"><span id="{cid}-{i}" class="cnt">{inner}</span></div>')
            js.append(f'tl.set("#{cid}-{i}", {{ opacity: 1 }}, {r3(times[i])});')
            if i < n - 1:
                js.append(f'tl.set("#{cid}-{i}", {{ opacity: 0 }}, {r3(times[i + 1])});')
        L = f"#{cid}-{n - 1}"
        js += [f'tl.set("{L}", {{ scale: 1.04, filter: "blur(14px)", textShadow: "{SERIF_BLOOM}" }}, {r3(times[-1])});',
               f'tl.set("{L}", {{ scale: 1.015, filter: "blur(5px)", textShadow: "{SERIF_SOFT}" }}, {r3(times[-1] + F1)});',
               f'tl.set("{L}", {{ scale: 1, filter: "blur(0px)", textShadow: "{HERO_HALO}" }}, {r3(times[-1] + 4 * F1)});']
        if cid == "cn3":
            for f_, on in ((6, 1), (8, 0), (10, 1), (11, 0)):
                if times[-1] + f_ * F1 < end:
                    js.append(f'tl.set("#{cid}-y", {{ backgroundColor: "{INK if on else "rgba(0,0,0,0)"}", color: "{"#0a0a0a" if on else INK}", '
                              f'textShadow: "{"none" if on else SERIF_REST}" }}, {r3(times[-1] + f_ * F1)});')
        els.append(f'<div id="{cid}" class="clip cg" data-start="{r3(start)}" data-duration="{r3(end - start)}" data-track-index="2" '
                   f'data-layout-allow-overflow data-layout-allow-overlap>{"".join(spans)}</div>')
    comp_file("captions", css, "\n".join("    " + e for e in els), js, END)
    return len(els)


# ------------------------------------------------------------------ fx: flashes, negatives, wipes, static, strikes, the volume bar
def build_fx():
    els, js, n = [], [], [0]

    def uid(p):
        n[0] += 1
        return f"{p}{n[0]}"

    css = """  #root { pointer-events: none; }
  #root .full { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; }
  #root .wf { background: #FFFDF6; opacity: 0; }
  #root .neg { background: #ffffff; mix-blend-mode: difference; opacity: 0; }
  #root .over { background: #ffffff; mix-blend-mode: screen; opacity: 0; }
  #root .leak { background: radial-gradient(ellipse at 30% 60%, rgba(255,120,170,0.95) 0%, rgba(255,150,90,0.7) 35%, rgba(255,200,140,0.0) 75%);
    mix-blend-mode: screen; opacity: 0; }
  #root .wipe { position: absolute; top: 0; left: 0; width: 560px; height: 1080px;
    background: linear-gradient(90deg, rgba(255,253,246,0) 0%, rgba(255,253,246,0.96) 38%, rgba(255,253,246,0.96) 62%, rgba(255,253,246,0) 100%); }
  #root .vsm { background: repeating-linear-gradient(90deg, rgba(255,255,255,0) 0px, rgba(255,255,255,0.55) 3px, rgba(255,255,255,0) 9px);
    opacity: 0; }
  #root .strike { position: absolute; height: 8px; background: #FBF8EC; transform-origin: 0% 50%; transform: none;
    box-shadow: 0 0 12px rgba(255,255,255,0.95), 0 0 32px rgba(255,255,255,0.5); }
  #root .black { background: #000; opacity: 0; }
  #root .osd { position: absolute; left: 120px; top: 110px; font-family: 'Pixel'; color: #4BFF6B; font-size: 40px; letter-spacing: 0.08em;
    text-shadow: 0 0 10px rgba(75,255,107,0.75), 0 0 26px rgba(75,255,107,0.35); white-space: nowrap; }
  #root .bar { display: inline-block; width: 20px; height: 44px; margin-right: 8px; background: #4BFF6B; vertical-align: middle;
    box-shadow: 0 0 10px rgba(75,255,107,0.7); }
  #root .stat { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; }
"""

    def timed(i, a, b, cls, style="", inner="", tag="div", attrs=""):
        els.append(f'<{tag} id="{i}" class="clip {cls}" data-start="{r3(a)}" data-duration="{r3(b - a)}" data-track-index="1" '
                   f'{attrs} style="{style}">{inner}</{tag}>')

    for fx in edit.FX:
        kind, t = fx[0], fr(fx[1])
        if kind == "flash":
            k = fx[2]
            i = uid("wf")
            timed(i, t, t + (k + 2) * F1, "", "", f'<div id="{i}-c" class="full wf"></div>')
            seq = [0.95, 0.55, 0.0] if k == 1 else [1.0, 0.9, 0.45, 0.0]
            for j, o in enumerate(seq):
                js.append(f'tl.set("#{i}-c", {{ opacity: {o} }}, {r3(t + j * F1)});')
        elif kind == "neg":
            k = fx[2]
            i = uid("ng")
            timed(i, t, t + k * F1, "", "", f'<div id="{i}-c" class="full neg" style="opacity:1"></div>')
        elif kind == "wipe":
            i = uid("wp")
            timed(i, t - 4 * F1, t + 5 * F1, "", "", f'<div id="{i}-c" class="wipe"></div>')
            js.append(f'tl.fromTo("#{i}-c", {{ x: 1920 }}, {{ x: -560, duration: {r3(8 * F1)}, ease: "none", immediateRender: false }}, {r3(t - 4 * F1)});')
        elif kind == "bloomcut":
            i = uid("bc")
            timed(i, t - 2 * F1, t + 3 * F1, "", "",
                  f'<div id="{i}-o" class="full over"></div><div id="{i}-n" class="full neg"></div><div id="{i}-l" class="full leak"></div>')
            js += [f'tl.set("#{i}-o", {{ opacity: 0.45 }}, {r3(t - 2 * F1)});', f'tl.set("#{i}-o", {{ opacity: 0.85 }}, {r3(t - F1)});',
                   f'tl.set("#{i}-o", {{ opacity: 0 }}, {r3(t)});', f'tl.set("#{i}-n", {{ opacity: 1 }}, {r3(t)});',
                   f'tl.set("#{i}-n", {{ opacity: 0 }}, {r3(t + F1)});', f'tl.set("#{i}-l", {{ opacity: 0.9 }}, {r3(t + F1)});',
                   f'tl.set("#{i}-l", {{ opacity: 0.4 }}, {r3(t + 2 * F1)});']
        elif kind == "whip":
            i = uid("wh")
            timed(i, t - F1, t + 2 * F1, "", "", f'<div id="{i}-v" class="full vsm"></div><div id="{i}-w" class="full wf"></div>')
            js += [f'tl.set("#{i}-v", {{ opacity: 0.9 }}, {r3(t - F1)});', f'tl.set("#{i}-w", {{ opacity: 0.55 }}, {r3(t)});',
                   f'tl.set("#{i}-v", {{ opacity: 0.5 }}, {r3(t + F1)});', f'tl.set("#{i}-w", {{ opacity: 0 }}, {r3(t + F1)});']
        elif kind == "double":
            i = uid("db")
            timed(i, t - F1, t + 3 * F1, "", "", f'<div id="{i}-c" class="full wf"></div>')
            for j, o in enumerate([0.35, 0.5, 0.25, 0.0]):
                js.append(f'tl.set("#{i}-c", {{ opacity: {o} }}, {r3(t - F1 + j * F1)});')
        elif kind == "static":
            k = fx[2]
            i = uid("st")
            timed(i, t, t + k * F1, "stat", "", "", tag="video",
                  attrs='src="assets/clips/s02.mp4" muted playsinline data-media-start="0" data-hf-media-start-basis="local"')
        elif kind == "strike":
            x0, x1, y = fx[2], fx[3], fx[4]
            i = uid("sk")
            bend = beat_at(t)["b"]
            timed(i, t, bend, "", "", f'<div id="{i}-c" class="strike" style="left:{x0}px;top:{y - 4}px;width:{x1 - x0}px"></div>')
            js.append(f'tl.fromTo("#{i}-c", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {r3(5 * F1)}, ease: "power2.out", immediateRender: false }}, {r3(t)});')
        elif kind == "fadeout":
            i = uid("fo")
            timed(i, t, fx[2], "", "", f'<div id="{i}-c" class="full black"></div>')
            js.append(f'tl.fromTo("#{i}-c", {{ opacity: 0 }}, {{ opacity: 1, duration: {r3(fx[2] - t)}, ease: "power1.in", immediateRender: false }}, {r3(t)});')
    # the TV volume bar on "with the volume turned all the way down"
    v0, v1, vend = fr(edit.F(36.73)), fr(edit.F(37.90)), fr(edit.F(38.16))
    bars = "".join(f'<span id="ob{k}" class="bar"></span>' for k in range(16))
    nums = "".join(f'<span id="on{k}" style="position:absolute;left:0;top:0;opacity:{1 if k == 16 else 0}">{k}</span>' for k in range(17))
    timed("osd", v0, vend, "", "", f'<div class="osd">VOLUME&nbsp;&nbsp;{bars}<span style="position:relative;display:inline-block;width:70px;height:40px;vertical-align:middle">{nums}</span></div>')
    for k in range(16):
        tk = fr(v0 + (v1 - v0) * (k + 1) / 16)
        js += [f'tl.set("#ob{15 - k}", {{ opacity: 0.12 }}, {r3(tk)});', f'tl.set("#on{16 - k}", {{ opacity: 0 }}, {r3(tk)});',
               f'tl.set("#on{15 - k}", {{ opacity: 1 }}, {r3(tk)});']
    comp_file("fx", css, "\n".join("    " + e for e in els), js, END)


# ------------------------------------------------------------------ built scenes
def scene_logogrid(b):
    d = b["b"] - b["a"]
    la = fr(b["logo_at"] - b["a"])
    tiles, js = [], []
    k = 0
    for row in range(6):
        for col in range(6):
            imgs = "".join(f'<div id="lg{k}-{j}" class="ti" style="background-image:url(assets/img/g{(k * 5 + j * 7) % 24:02d}.jpg)"></div>' for j in range(3))
            tiles.append(f'<div class="tile" style="left:{col * 320}px;top:{row * 180}px">{imgs}</div>')
            steps = int(d / (3 * F1)) + 1
            for s in range(steps):
                t = fr(s * 3 * F1)
                j = (s + k) % 3
                js.append(f'tl.set("#lg{k}-{j}", {{ opacity: 1 }}, {r3(t)});')
                js.append(f'tl.set("#lg{k}-{(j + 2) % 3}", {{ opacity: 0 }}, {r3(t)});')
            k += 1
    css = """  #root { background: #000; }
  #root .tile { position: absolute; width: 320px; height: 180px; overflow: hidden; }
  #root .tile .ti { position: absolute; left: 0; top: 0; width: 320px; height: 180px; background-size: cover; background-position: center; opacity: 0; }
  #root .dim { position: absolute; inset: 0; background: rgba(0,0,0,0.38); }
  #root .card { position: absolute; left: 500px; top: 270px; width: 920px; height: 518px; background: #05060c; overflow: hidden;
    border: 2px solid rgba(255,255,255,0.92); opacity: 0;
    box-shadow: 0 0 18px rgba(255,255,255,0.75), 0 0 60px rgba(255,255,255,0.35), 0 30px 80px rgba(0,0,0,0.7); }
  #root .card img { position: absolute; left: 0; top: 0; width: 920px; height: 518px; object-fit: cover; }
  #root .sq { position: absolute; left: 500px; top: 270px; width: 920px; height: 518px; background: #fff; opacity: 0;
    box-shadow: 0 0 30px rgba(255,255,255,0.95), 0 0 90px rgba(255,255,255,0.55); }
"""
    body = ('    <div id="lgbox" class="box">'
            + "".join(tiles) + '<div class="dim"></div><div id="lgsq" class="sq"></div>'
            '<div id="lgcard" class="card"><img src="assets/img/vilogo.jpg"></div></div>')
    js += [f'tl.set("#lgsq", {{ opacity: 1 }}, {r3(la - 2 * F1)});', f'tl.set("#lgsq", {{ opacity: 0 }}, {r3(la)});',
           f'tl.set("#lgcard", {{ opacity: 1 }}, {r3(la)});']
    comp_file(f"sc_{b['id']}", css, body, js, d)


def scene_white(b):
    d = b["b"] - b["a"]
    css = """  #root { background: #F3F0E9; }
  #root .tex { position: absolute; inset: 0; width: 1920px; height: 1080px; object-fit: cover; opacity: 0.35; mix-blend-mode: multiply; }
"""
    body = f'    <div id="wbox" class="box"><img class="tex" src="assets/tex/paper_light.png"></div>'
    comp_file(f"sc_{b['id']}", css, body, [], d)


def scene_wall(b):
    d = b["b"] - b["a"]
    tiles = []
    k = 0
    for row in range(5):
        for col in range(8):
            i = (row * 8 + col * 3) % 24
            tiles.append(f'<div class="wt" style="left:{col * 318 - 160 + (row % 2) * 60}px;top:{row * 184 - 20}px">'
                         f'<div class="wi" style="background-image:url(assets/img/w{i:02d}.jpg)"></div></div>')
            k += 1
    css = """  #root { background: #000; }
  #root .persp { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; perspective: 1400px; }
  #root .tilt { position: absolute; left: -200px; top: -40px; width: 2400px; height: 1160px; transform: rotateY(-16deg) rotateX(5deg) scale(1.05); transform-origin: 30% 50%; }
  #root .wall { position: absolute; left: 0; top: 0; width: 2400px; height: 1160px; }
  #root .wt { position: absolute; width: 306px; height: 172px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
  #root .wt .wi { width: 306px; height: 172px; background-size: cover; background-position: center; }
  #root .vig { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 60%, rgba(0,0,0,0.92) 100%); }
"""
    body = (f'    <div id="wlbox" class="box"><div class="persp"><div class="tilt">'
            f'<div id="wall" class="wall">{"".join(tiles)}</div></div></div><div class="vig"></div></div>')
    js = [f'tl.fromTo("#wall", {{ x: 0 }}, {{ x: -120, duration: {r3(d)}, ease: "none" }}, 0);']
    comp_file(f"sc_{b['id']}", css, body, js, d)


def scene_crt(b):
    d = b["b"] - b["a"]
    jc = fr(edit.F(34.81) - b["a"])            # jump cut in on "family"
    css = """  #root { background: radial-gradient(ellipse at 50% 38%, #2a2018 0%, #120d09 55%, #050403 100%); }
  #root .desk { position: absolute; left: 0; top: 720px; width: 1920px; height: 360px; background: linear-gradient(180deg, #3a2a1c 0%, #1c140d 45%, #0d0906 100%); }
  #root .cam { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 50% 36%; }
  #root .crt { position: absolute; left: 512px; top: 50px; width: 896px; height: 688px; border-radius: 32px;
    background: linear-gradient(160deg, #e3dccb 0%, #cfc6b1 55%, #b3a990 100%);
    box-shadow: 0 40px 90px rgba(0,0,0,0.7), inset 0 -10px 30px rgba(0,0,0,0.25), inset 0 6px 14px rgba(255,255,255,0.5); }
  #root .bez { position: absolute; left: 48px; top: 40px; width: 800px; height: 608px; border-radius: 24px; background: #1d1c1a;
    box-shadow: inset 0 0 30px rgba(0,0,0,0.9); }
  #root .scr { position: absolute; left: 16px; top: 16px; width: 768px; height: 576px; border-radius: 20px; overflow: hidden; background: #000; }
  #root .scr video { position: absolute; left: 0; top: 0; width: 768px; height: 576px; object-fit: cover; }
  #root .lines { position: absolute; inset: 0; background: repeating-linear-gradient(180deg, rgba(0,0,0,0.22) 0px, rgba(0,0,0,0.22) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 4px); }
  #root .glare { position: absolute; inset: 0; background: radial-gradient(ellipse at 30% 25%, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0) 45%),
    radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.55) 100%); }
  #root .led { position: absolute; left: 792px; top: 661px; width: 12px; height: 12px; border-radius: 6px; background: #5dff7a; box-shadow: 0 0 10px #5dff7a; }
"""
    body = (f'    <div id="crtbox" class="box">'
            f'<div class="desk"></div><div id="crtcam" class="cam"><div class="crt"><div class="bez"><div class="scr">'
            f'<video id="crtv" class="clip" src="assets/clips/l_crt.mp4" muted playsinline data-start="0" data-duration="{r3(d)}" '
            f'data-track-index="2" data-media-start="0" data-hf-media-start-basis="local"></video><div class="lines"></div><div class="glare"></div></div></div>'
            f'<div class="led"></div></div></div></div>')
    js = [f'tl.set("#crtcam", {{ scale: 1.32 }}, {r3(jc)});']
    comp_file(f"sc_{b['id']}", css, body, js, d)


def scene_notebook(b):
    d = b["b"] - b["a"]
    L = lambda v: fr(edit.F(v) - b["a"])
    asp, pz, close_in, close_out, photo = L(41.44), L(42.00), L(41.83), L(42.80), L(42.35)
    faint = [("THUGSTOOLS", 330, 300, -4), ("LEAVEMEALONE", 1300, 300, 3), ("GETTHEREFAST", 380, 800, 2),
             ("BIGBANG", 1130, 820, -3), ("SEAWAYS", 1560, 640, 5), ("PRECIOUSPROTECTION", 280, 560, -2)]
    fh = "".join(f'<div class="hand faint" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">{w}</div>' for w, x, y, r in faint)
    css = """  #root { background: #EDE6D6; }
  #root .cam { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 50% 50%; }
  #root .page { position: absolute; left: -80px; top: -60px; width: 2080px; height: 1200px; transform: rotate(-2.2deg);
    background-color: #F4EEDF; background-image: repeating-linear-gradient(180deg, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 61px, rgba(70,110,190,0.38) 61px, rgba(70,110,190,0.38) 63px); }
  #root .tex { position: absolute; inset: 0; width: 2080px; height: 1200px; object-fit: cover; opacity: 0.5; mix-blend-mode: multiply; }
  #root .margin { position: absolute; left: 300px; top: 0; width: 3px; height: 1200px; background: rgba(210,70,70,0.55); }
  #root .hand { position: absolute; font-family: 'Hand'; color: #34343c; white-space: nowrap; line-height: 1; }
  #root .faint { font-size: 54px; opacity: 0.42; }
  #root .big { font-size: 150px; letter-spacing: 0.02em; }
  #root .ul { position: absolute; height: 6px; background: #34343c; border-radius: 3px; transform-origin: 0% 50%; opacity: 0.8; }
  #root .photo { position: absolute; left: 1290px; top: 470px; width: 470px; padding: 18px 18px 64px 18px; background: #FAFAF6;
    box-shadow: 0 18px 40px rgba(0,0,0,0.45); transform: rotate(6deg); }
  #root .photo img { display: block; width: 434px; height: 326px; object-fit: cover; }
  #root .pin { position: absolute; left: 1290px; top: 470px; width: 470px; height: 410px; background: #fff; transform: rotate(6deg); opacity: 0;
    box-shadow: 0 0 30px rgba(255,255,255,0.95); }
  #root .vig { position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(40,30,15,0.45) 100%); }
"""
    body = (f'    <div id="nbbox" class="box"><div id="nbcam" class="cam">'
            f'<div class="page"><img class="tex" src="assets/tex/paper_light.png"><div class="margin"></div>{fh}'
            f'<div id="nbasp" class="hand big" style="left:560px;top:330px;clip-path:inset(0% 100% 0% 0%)">ASPIRINE</div>'
            f'<div id="nbpz" class="hand big" style="left:640px;top:560px;clip-path:inset(0% 100% 0% 0%)">PANZER</div>'
            f'<div id="nbul" class="ul" style="left:630px;top:720px;width:560px;transform:scaleX(0) rotate(-1deg)"></div>'
            f'</div><div id="nbphoto" class="photo" style="opacity:0"><img src="assets/img/tank.jpg"></div><div id="nbpin" class="pin"></div>'
            f'</div><div class="vig"></div></div>')
    js = [f'tl.fromTo("#nbasp", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.36, ease: "none", immediateRender: false }}, {r3(asp)});',
          f'tl.set("#nbcam", {{ scale: 1.65, x: -60, y: -300 }}, {r3(close_in)});',
          f'tl.fromTo("#nbpz", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.30, ease: "none", immediateRender: false }}, {r3(pz)});',
          f'tl.fromTo("#nbul", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.16, ease: "none", immediateRender: false }}, {r3(pz + 0.30)});',
          f'tl.set("#nbcam", {{ scale: 1, x: 0, y: 0 }}, {r3(close_out)});',
          f'tl.set("#nbpin", {{ opacity: 1 }}, {r3(close_out)});', f'tl.set("#nbpin", {{ opacity: 0 }}, {r3(close_out + 2 * F1)});',
          f'tl.set("#nbphoto", {{ opacity: 1 }}, {r3(close_out + 2 * F1)});']
    comp_file(f"sc_{b['id']}", css, body, js, d)


def scene_grid4(b):
    d = b["b"] - b["a"]
    times = [fr(edit.F(v) - b["a"]) for v in (50.32, 50.62, 51.43, 51.92)]
    ids = ["l_g1", "l_g2", "l_g3", "l_g4"]
    pos = [(0, 0), (960, 0), (0, 540), (960, 540)]
    tiles, js = [], []
    for k, (cid, (x, y), t) in enumerate(zip(ids, pos, times)):
        tiles.append(f'<div class="cell" style="left:{x}px;top:{y}px"><video id="g4v{k}" class="clip" src="assets/clips/{cid}.mp4" muted playsinline '
                     f'data-start="{r3(t)}" data-duration="{r3(d - t)}" data-track-index="{k + 2}" data-media-start="{r3(t)}" data-hf-media-start-basis="local"></video>'
                     f'<div id="g4f{k}" class="cf"></div></div>')
        js += [f'tl.set("#g4f{k}", {{ opacity: 1 }}, {r3(t)});', f'tl.set("#g4f{k}", {{ opacity: 0.5 }}, {r3(t + F1)});',
               f'tl.set("#g4f{k}", {{ opacity: 0 }}, {r3(t + 2 * F1)});']
    css = """  #root { background: #000; }
  #root .cell { position: absolute; width: 960px; height: 540px; overflow: hidden; }
  #root .cell video { position: absolute; left: 0; top: 0; width: 960px; height: 540px; object-fit: cover; }
  #root .cf { position: absolute; inset: 0; background: #FFFDF6; opacity: 0; }
  #root .seam { position: absolute; background: #000; }
"""
    body = (f'    <div id="g4box" class="box">{"".join(tiles)}'
            f'<div class="seam" style="left:957px;top:0;width:6px;height:1080px"></div><div class="seam" style="left:0;top:537px;width:1920px;height:6px"></div></div>')
    comp_file(f"sc_{b['id']}", css, body, js, d)


def scene_split(b):
    d = b["b"] - b["a"]
    css = """  #root { background: #000; }
  #root .half { position: absolute; top: 0; width: 960px; height: 1080px; overflow: hidden; }
  #root .half video { position: absolute; left: 0; top: 0; width: 960px; height: 1080px; object-fit: cover; }
  #root .seam { position: absolute; left: 957px; top: 0; width: 6px; height: 1080px; background: #FBF8EC;
    box-shadow: 0 0 14px rgba(255,255,255,0.9), 0 0 40px rgba(255,255,255,0.4); }
  #root .lab { position: absolute; top: 915px; font-family: 'Instrument Serif'; font-style: italic; font-size: 52px; color: #FBF8EC;
    text-shadow: 0 0 14px rgba(255,255,255,0.62), 0 0 42px rgba(255,255,255,0.30), 0 0 4px rgba(0,0,0,0.4), 0 0 22px rgba(0,0,0,0.55); white-space: nowrap; }
"""
    body = (f'    <div id="spbox" class="box">'
            f'<div class="half" style="left:0"><video id="spl" class="clip" src="assets/clips/l_spl.mp4" muted playsinline data-start="0" data-duration="{r3(d)}" data-track-index="2" data-media-start="0" data-hf-media-start-basis="local"></video></div>'
            f'<div class="half" style="left:960px"><video id="spr" class="clip" src="assets/clips/l_spr.mp4" muted playsinline data-start="0" data-duration="{r3(d)}" data-track-index="3" data-media-start="0" data-hf-media-start-basis="local"></video></div>'
            f'<div class="seam"></div><div class="lab" style="left:120px">Miami</div><div class="lab" style="left:1080px">Vice City</div></div>')
    comp_file(f"sc_{b['id']}", css, body, [], d)


SCENES = {"logogrid": scene_logogrid, "white": scene_white, "wall": scene_wall, "crt": scene_crt, "notebook": scene_notebook,
          "grid4": scene_grid4, "split": scene_split}


def build_grain():
    js = []
    seq = [(-5, -5), (-10, 5), (5, -10), (-5, 15), (-10, 5), (15, 0), (0, 10), (-15, 0), (10, 5), (0, 0)]
    t, i = 0.0, 0
    while t < END:
        x, y = seq[i % len(seq)]
        js.append(f'tl.set("#grain-tex", {{ xPercent: {x}, yPercent: {y} }}, {r3(t)});')
        t += 0.1; i += 1
    css = """  #root { pointer-events: none; }
  #grain-tex { position: absolute; left: -50%; top: -50%; width: 200%; height: 200%; opacity: 0.07;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"); mix-blend-mode: overlay; }
"""
    body = f'    <div id="grain-box" class="clip" data-start="0" data-duration="{r3(END)}" data-track-index="1" data-layout-ignore style="position:absolute;left:0;top:0;width:1920px;height:1080px"><div id="grain-tex"></div></div>'
    comp_file("grain", css, body, js, END)


def sfx_len(name):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          f"{PROJ}/assets/sfx/{name}.mp3"], capture_output=True, text=True).stdout
    return float(out)


def build_root():
    els = ['<div id="bg"></div>']
    for b in edit.S:
        a, d = fr(b["a"]), fr(b["b"]) - fr(b["a"])
        if b.get("segs") or b.get("scene") == "static":
            src = f"assets/clips/{b['id']}.mp4" if b.get("segs") else "assets/clips/s02.mp4"
            els.append(f'<video id="v_{b["id"]}" class="clip v" src="{src}" muted playsinline data-start="{r3(a)}" '
                       f'data-duration="{r3(d)}" data-media-start="0" data-track-index="1"></video>')
        else:
            SCENES[b["scene"]](b)
            els.append(f'<div id="h_{b["id"]}" class="clip" data-composition-id="sc_{b["id"]}" data-composition-src="compositions/sc_{b["id"]}.html" '
                       f'data-start="{r3(a)}" data-duration="{r3(d)}" data-track-index="2" data-track-kind="graphics" '
                       f'data-width="1920" data-height="1080" style="z-index:5"></div>')
    els.append(f'<div id="fx" class="clip" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" '
               f'data-duration="{r3(END)}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:30"></div>')
    els.append(f'<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
               f'data-duration="{r3(END)}" data-track-index="4" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:40"></div>')
    els.append(f'<div id="grain" class="clip" data-composition-id="grain" data-composition-src="compositions/grain.html" data-start="0" '
               f'data-duration="{r3(END)}" data-track-index="5" data-width="1920" data-height="1080" style="z-index:50"></div>')
    els.append(f'<audio id="a_news" class="clip" src="assets/audio/news_n.wav" data-start="0.000" data-duration="6.700" data-media-start="0" data-volume="1" data-track-index="10"></audio>')
    els.append(f'<audio id="a_cj" class="clip" src="assets/audio/cj_n.wav" data-start="{r3(edit.CJ0)}" data-duration="2.450" data-media-start="0" data-volume="1" data-track-index="11"></audio>')
    els.append(f'<audio id="a_vo" class="clip" src="assets/audio/vo_n.wav" data-start="{r3(edit.V0)}" data-duration="96.440" data-media-start="0" data-volume="1" data-track-index="12"></audio>')
    for k, (name, t, _) in enumerate(edit.SFX):
        vol = edit.SFX_GAIN[name]
        ln = min(sfx_len(name), END - t)
        els.append(f'<audio id="a_sfx{k}" class="clip" src="assets/sfx/{name}.mp3" data-start="{r3(t)}" data-duration="{r3(ln)}" '
                   f'data-media-start="0" data-volume="{vol}" data-track-index="{13 + k % 3}"></audio>')
    open(f"{PROJ}/index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #050505; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; background: #050505; }}
      .v {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{r3(END)}" data-width="1920" data-height="1080">
{chr(10).join('      ' + e for e in els)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.to({{}}, {{ duration: {r3(END)} }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")


if __name__ == "__main__":
    os.makedirs(COMP, exist_ok=True)
    for f in os.listdir(COMP):
        if f.endswith(".html"):
            os.remove(f"{COMP}/{f}")
    n = build_captions()
    build_fx()
    build_grain()
    build_root()
    print("built:", n, "caption groups;", len(os.listdir(COMP)), "compositions")
