"""v3 builder: Pattinson-edit typography (small bold sans + big upright serif + bold numbers) with Tesla word
entrances, CRT frames, splits/strips/grids, curved wall, floating cards. No SFX.
usage: python -I -X utf8 build3.py   (from anywhere)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl3 as E
from edl import W, cut, N, VO_OFFSET, NEWS_DUR, NEWS_IN
TOTAL = E.TOTAL

P = E.PROJ
os.makedirs(os.path.join(P, "compositions"), exist_ok=True)
SH = {s["id"]: s for s in E.SHOTS}
r3 = lambda x: round(x, 3)

FONTS = """
@font-face{font-family:"InterV";src:url("assets/fonts/InterVar-latin.woff2") format("woff2");font-weight:100 900;font-style:normal;}
@font-face{font-family:"Instrument Serif";src:url("assets/fonts/InstrumentSerif-Regular.woff2") format("woff2");font-weight:400;font-style:normal;}
"""
SET = "0 0 22px rgba(255,255,255,0.40), 0 0 4px rgba(255,255,255,0.24), 0 2px 18px rgba(0,0,0,0.72)"
POP = "0 0 26px rgba(255,255,255,0.85), 0 0 7px rgba(255,255,255,0.85), 0 2px 18px rgba(0,0,0,0.30)"
BLOOM = "0 0 34px rgba(255,255,255,1), 0 0 10px rgba(255,255,255,1), 0 2px 18px rgba(0,0,0,0)"
SGLOW = "0 0 34px rgba(255,255,255,0.50), 0 0 8px rgba(255,255,255,0.32), 0 2px 22px rgba(0,0,0,0.65)"
FLASH = "0 0 80px rgba(255,255,255,1), 0 0 22px rgba(255,255,255,1), 0 2px 22px rgba(0,0,0,0)"
INK = "0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0), 0 0 0px rgba(0,0,0,0)"

CSS = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;}
.shot{position:absolute;inset:0;overflow:hidden;}
.shot video,.rc video,.fci video,.wp video{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;}
.shot video{width:1920px;height:1080px;}
.box{position:absolute;background:#fff;}
.crt{position:absolute;inset:0;background:#040404;overflow:hidden;}
.tube{position:absolute;left:64px;top:44px;width:1792px;height:992px;border-radius:150px / 110px;overflow:hidden;background:#000;
  box-shadow:0 0 0 2px rgba(255,255,255,0.06), 0 0 60px rgba(120,160,255,0.10);}
.tube video{position:absolute;left:-64px;top:-44px;width:1920px;height:1080px;object-fit:cover;}
.scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(0,0,0,0.26) 0px, rgba(0,0,0,0.26) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 4px);}
.glass{position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 35% 25%, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0) 55%),
  radial-gradient(ellipse 95% 95% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.62) 100%);}
.rc{position:absolute;overflow:hidden;}
.lab{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;pointer-events:none;}
.fc{position:absolute;opacity:0;}
.fci{position:absolute;inset:0;overflow:hidden;box-shadow:0 28px 70px rgba(0,0,0,0.65), 0 0 0 2px rgba(255,255,255,0.10);}
.dimov{position:absolute;inset:0;background:rgba(0,0,0,0.62);}
.wall{position:absolute;inset:0;perspective:1500px;background:#030303;}
.ring{position:absolute;left:960px;top:540px;width:0;height:0;transform-style:preserve-3d;}
.wp{position:absolute;width:600px;height:338px;left:-300px;top:-169px;overflow:hidden;opacity:0;}
.wp::after{content:"";position:absolute;inset:0;box-shadow:inset 0 0 0 2px rgba(0,0,0,0.6);}
.osd{position:absolute;left:190px;bottom:150px;font-family:"InterV",sans-serif;font-weight:800;color:#F2F2F0;letter-spacing:0.12em;
  text-shadow:0 0 16px rgba(255,255,255,0.85);opacity:0;}
.osd .bars{display:flex;gap:10px;margin-top:14px;}
.osd .bar{width:22px;height:46px;background:#F2F2F0;box-shadow:0 0 14px rgba(255,255,255,0.8);}
.band{position:absolute;left:0;right:0;top:445px;height:190px;background:#EEEDE9;transform-origin:50% 50%;}
.vhs{position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.05) 0px, rgba(255,255,255,0.05) 1px, rgba(0,0,0,0) 1px, rgba(0,0,0,0) 3px);}
.vband{position:absolute;left:0;right:0;height:120px;background:linear-gradient(180deg,rgba(255,255,255,0),rgba(255,255,255,0.30),rgba(255,255,255,0));}
.osdt{position:absolute;left:150px;top:110px;font-family:"InterV",sans-serif;font-weight:800;font-size:54px;color:#fff;letter-spacing:0.06em;text-shadow:3px 3px 0 #000;}
/* captions */
.cl{position:absolute;display:flex;flex-direction:column;align-items:center;pointer-events:none;}
.cl.c{left:0;right:0;} .cl.l{align-items:flex-start;} .cl.r{align-items:flex-end;}
.row{display:flex;align-items:baseline;white-space:nowrap;color:#F2F2F0;}
.row.wide{column-gap:46px;} .row.mix{column-gap:26px;}
.w{position:relative;display:inline-block;}
.gh{visibility:hidden;}
.ik{position:absolute;left:-60%;right:-60%;top:0;bottom:0;display:flex;justify-content:center;align-items:flex-start;z-index:1;}
.tx{display:inline-block;opacity:0;text-shadow:""" + SET + """;}
.st-s{font-family:"InterV",sans-serif;font-weight:600;font-size:54px;letter-spacing:-0.02em;line-height:1.15;}
.st-S{font-family:"Instrument Serif",serif;font-weight:400;font-size:136px;letter-spacing:-0.01em;line-height:1.0;}
.st-B{font-family:"Instrument Serif",serif;font-weight:400;font-size:196px;letter-spacing:-0.015em;line-height:1.0;}
.st-X{font-family:"Instrument Serif",serif;font-weight:400;font-size:250px;letter-spacing:-0.02em;line-height:1.0;}
.st-N,.st-Y{font-family:"InterV",sans-serif;font-weight:800;font-size:132px;letter-spacing:-0.045em;line-height:1.0;}
.st-k{font-family:"InterV",sans-serif;font-weight:700;font-size:32px;letter-spacing:0.45em;line-height:1.4;}
.st-T{font-family:"InterV",sans-serif;font-weight:800;font-size:120px;letter-spacing:0.06em;line-height:1.0;}
.st-i{font-family:"InterV",sans-serif;font-weight:600;font-size:66px;letter-spacing:-0.025em;line-height:1.15;color:#151515;}
.st-sel{font-family:"InterV",sans-serif;font-weight:600;font-size:54px;letter-spacing:-0.02em;line-height:1.15;}
.st-S .tx,.st-B .tx,.st-X .tx{text-shadow:""" + SGLOW + """;}
.st-i .tx{text-shadow:""" + INK + """;color:#151515;}
.selbox{position:absolute;left:-0.08em;right:-0.08em;top:0.12em;bottom:0.02em;background:rgba(48,96,255,0.88);z-index:0;transform-origin:0 50%;}
.yb{position:absolute;left:-0.03em;top:0.04em;width:1.12em;height:0.92em;background:#fff;mix-blend-mode:difference;opacity:0;}
.sub{position:absolute;left:0;right:0;top:100%;margin-top:14px;text-align:center;font-family:"InterV",sans-serif;font-weight:700;font-size:30px;letter-spacing:0.35em;color:#F2F2F0;opacity:0;text-shadow:0 0 14px rgba(255,255,255,0.6);}
"""


def comp(cid, dur, body, js, extra_css=""):
    return f"""<template>
<style>{CSS}{extra_css}</style>
<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{r3(dur)}">
{body}
</div>
<script>
(function(){{
  const tl = gsap.timeline({{ paused: true }});
{js}
  window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
"""


# ------------------------------------------------------------------ entrances
def ent(sel, kind, t):
    t = r3(t); a = r3(t + 0.034)
    if kind == "pop":
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.03,filter:"blur(0.6px) brightness(1.55)",textShadow:"{POP}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SET}",duration:0.13,ease:"expo.out"}},{a});\n')
    if kind == "bloom":
        return (f'  tl.set("{sel}",{{opacity:1,fontWeight:900,scale:1.05,filter:"blur(1.2px) brightness(1.9)",textShadow:"{BLOOM}"}},{t});\n'
                f'  tl.to("{sel}",{{fontWeight:600,scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SET}",duration:0.2,ease:"expo.out"}},{a});\n')
    if kind == "soft":
        return f'  tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:0.05,ease:"none"}},{t});\n'
    if kind == "flash":       # whole on its frame, blown out and a little large, crisp in its glow a few frames later
        return (f'  tl.set("{sel}",{{opacity:1,scale:1.1,filter:"blur(3px) brightness(2.8)",textShadow:"{FLASH}"}},{t});\n'
                f'  tl.to("{sel}",{{scale:1,filter:"blur(0px) brightness(1)",textShadow:"{SGLOW}",duration:0.22,ease:"power3.out"}},{r3(t + 0.05)});\n')
    if kind == "ink":
        return (f'  tl.set("{sel}",{{opacity:1,fontWeight:900,scale:1.04,filter:"blur(1.2px)"}},{t});\n'
                f'  tl.to("{sel}",{{fontWeight:600,scale:1,filter:"blur(0px)",duration:0.2,ease:"expo.out"}},{a});\n')
    raise ValueError(kind)


def year_flicker(sel, t):
    return "".join(f'  tl.set("{sel}",{{opacity:{1 if k % 2 == 0 else 0}}},{r3(t + f / 60)});\n' for k, f in enumerate((6, 8, 10, 11)))


SMALL = {"a", "an", "the", "to", "of", "in", "it", "on", "and", "so", "for", "at", "be", "is", "was", "if", "you", "it's",
         "he's", "that", "with", "are", "from", "but", "they", "what", "just", "how", "this", "your", "that's", "all"}

CJW = {"Ah": NEWS_DUR + 0.04, "shit,": NEWS_DUR + 0.56, "here": NEWS_DUR + 1.54, "we": NEWS_DUR + 1.66, "go": NEWS_DUR + 1.80, "again.": NEWS_DUR + 2.00}


def tok_time(ref):
    if ref.startswith("n"):
        return N(int(ref[1:]))
    if ref.startswith("cj:"):
        return CJW[ref[3:]]
    return W(int(ref))


class Line:
    def __init__(self, spec, y=540, align="c", x=0, end=None, start=None):
        self.rows = []
        for row in spec.split(" / "):
            toks = []
            for tok in row.split("  "):
                st, rest = tok.split(":", 1)
                text, ref = rest.rsplit("@", 1)
                toks.append((st, text, tok_time(ref)))
            self.rows.append(toks)
        self.y, self.align, self.x, self.end, self.start = y, align, x, end, start

    def first(self): return min(t for r in self.rows for _, _, t in r)
    def last(self): return max(t for r in self.rows for _, _, t in r)


def L(spec, **kw):
    return Line(spec, **kw)


# two spaces separate tokens; " / " separates stacked rows.  styles: s small sans, S serif, B big serif, X huge serif,
# N bold number, Y bold year (flicker), k kicker, T typed cheat code, i ink (on the white band), sel blue selection
LINES = [
    L("s:A@n0  s:video@n1  s:game@n2", end=N(3) - 0.04),
    L("s:so@n3  S:popular@n4", end=N(5) - 0.04),
    L("s:it@n5  s:could@n6  s:cost@n7", end=N(8) - 0.04),
    L("s:the@n8  sel:U.S.&nbsp;economy@n9", end=N(11) - 0.14),
    L("s:Ah@cj:Ah  s:shit,@cj:shit,", y=820, end=NEWS_DUR + 1.48),
    L("s:here@cj:here  s:we@cj:we  s:go@cj:go  S:again.@cj:again.", y=820, end=VO_OFFSET),
    L("s:That's@0  s:exactly@1  s:how@2"),
    L("B:millions@3 / s:of@4  s:adults@5", y=520),
    L("s:are@6  s:going@7  s:to@8  s:feel@9"),
    L("k:2026@11 / s:on@10  S:November@11  S:19th@12", y=520),
    L("s:when@13  s:they@14  s:play@15", end=cut(16) + 0.02),
    L("s:for@18  s:the@19  S:first@20  S:time.@21"),
    L("s:GTA@22  s:6@23  s:took@24", y=930),
    L("N:13@25  S:years@26"),
    L("s:and@27  B:$2@28  B:billion@29  s:dollars@30"),
    L("s:to@31  s:make.@32"),
    L("s:The@33  s:release@34  s:got@35  s:pushed@36  s:from@37", end=cut(38)),
    L("s:and@42  s:then@43  s:again@44  s:to@45", y=960, end=cut(46) + 0.05),
    L("s:And@47  s:yet,@48", y=540),
    L("B:nobody@49 / s:seems@50  s:to@51  s:have@52  s:moved@53  s:on.@54", y=520),
    L("s:But@55  B:why?@56"),
    L("s:Why@57  s:are@58  S:grown@59  S:adults@60"),
    L("s:waiting@61  N:13@62  S:years@63"),
    L("s:for@64  s:a@65  s:game@66  s:that's@67  s:supposedly@68"),
    L("s:just@69  s:about@70  S:stealing@71  S:cars?@72"),
    L("s:Because@73  s:GTA@74"),
    L("s:was@75  s:never@76  s:just@77  s:about@78", end=cut(79)),
    L("s:and@80", end=cut(82)),
    L("s:It@82  s:was@83  s:about@84  s:what@85"),
    L("s:it@86  s:really@87  s:gave@88  s:you.@89"),
    L("X:Freedom.@90", end=cut(91) + 0.12),
    L("N:10@94  S:years@95  S:old,@96"),
    L("s:sitting@97  s:in@98  s:front@99  s:of@100", y=905),
    L("s:the@101  s:family@102  S:computer,@103", y=905),
    L("s:playing@104  S:Vice@105  S:City@106"),
    L("s:with@107  s:the@108  s:volume@109  s:turned@110", y=905),
    L("s:all@111  s:the@112  s:way@113  S:down@114", y=905),
    L("s:so@115  s:nobody@116  s:could@117  s:hear@118"),
    L("s:the@119  S:gunshots.@120"),
    L("s:With@121  s:cheat@122  s:codes@123  s:like@124"),
    L("T:ASPIRINE@125", end=W(127) - 0.04),
    L("T:PANZER@127", end=cut(128)),
    L("s:scribbled@128  s:at@129  s:the@130  s:back@131"),
    L("s:of@132  s:your@133  S:notebook.@134"),
    L("s:For@135  s:a@136  S:kid,@137"),
    L("s:it@138  s:wasn't@139  s:just@140  s:a@141  S:game.@142"),
    L("s:It@143  s:was@144  s:a@145 / S:psychological@146  S:escape,@147", y=510),
    L("s:an@148  S:alternate@149  S:reality.@150"),
    L("s:It@151  s:was@152  S:everything@153"),
    L("s:you@154  s:imagined@155  S:adulthood@156  s:would@157  s:be.@158", end=cut(159)),
    L("s:and@165  s:owning@166  s:an@167  S:entire@168  S:city.@169"),
    L("s:And@170  s:while@171  s:every@172  s:other@173  s:game@174"),
    L("s:asks@175  s:you@176  s:to@177  s:be@178  s:the@179  S:hero,@180"),
    L("s:But@181  s:GTA@182  s:lets@183  s:you@184  s:be@185"),
    L("s:the@186  B:problem.@187"),
    L("s:It@188  s:lets@189  s:you@190  s:be@191  s:the@192  S:bad@193  S:guy@194"),
    L("s:in@195  s:a@196  s:world@197  s:that@198"),
    L("s:looks@199  s:just@200  s:like@201  S:yours.@202"),
    L("s:And@203  s:somewhere@204  s:along@205  s:the@206  s:way,@207", y=905),
    L("s:those@208  s:kids@209  S:grew@210  S:up.@211", y=905),
    L("B:Today,@212"),
    L("s:it's@213  s:the@214  s:exact@215  S:opposite.@216", end=cut(217)),
    L("s:It's@217  s:an@218  s:escape@219  s:from@220  S:adulthood,@221"),
    L("s:back@222  s:to@223  s:the@224  S:world@225"),
    L("s:they@226  s:once@227  S:dreamed@228  s:of@229  s:living@230  s:in.@231"),
    L("k:2026@234 / s:And@232  s:on@233  S:November@234  S:19th,@235", y=520),
    L("s:Rockstar@236  s:takes@237  s:you@238  s:back@239  s:to@240", y=920),
    L("S:Vice@241  S:City,@242", y=860),
    L("s:the@243  s:city@244  s:where@245  s:it@246  s:all@247  S:started.@248", y=930),
    L("s:So@249  s:if@250  s:you're@251  s:still@252  s:lost@253"),
    L("s:in@254  S:Los@255  S:Santos@256  s:this@257  s:week,@258"),
    L("s:don't@259  S:rush.@260"),
    L("s:Take@261  s:the@262  S:long@263  S:way@264  S:home.@265"),
    L("s:Drive@266  S:slow.@267"),
    L("s:Because@268  s:that@269  S:10-year-old@270"),
    L("s:playing@271  s:GTA@272  S:Vice@273  S:City@274"),
    L("s:never@275  s:really@276  S:left.@277"),
    L("s:He's@278  s:just@279  s:been@280  s:waiting@281"),
    L("N:13@282  S:years@283"),
    L("s:to@284  s:feel@285  s:that@286 / X:freedom@287 / s:again.@288", y=520, end=103.85),
]


def build_captions():
    body, js = [], []
    for li, Ln in enumerate(LINES):
        lid = f"cap{li:02d}"
        t0 = r3((Ln.start if Ln.start is not None else Ln.first()) - 0.03)
        nxt = LINES[li + 1].first() - 0.04 if li + 1 < len(LINES) else 103.85
        t1 = r3(min(Ln.end if Ln.end is not None else nxt, Ln.last() + 1.6))
        dur = r3(max(0.2, t1 - t0))
        rows_html, k = [], 0
        for ri, row in enumerate(Ln.rows):
            styles = {st for st, _, _ in row}
            mode = "mix" if styles & {"S", "B", "X", "N", "Y", "sel", "T"} else "wide"
            spans = []
            for wi, (st, txt, t) in enumerate(row):
                wid = f"{lid}r{ri}w{wi}"
                extra = ""
                bare = re.sub(r"[^a-z']", "", txt.lower())
                if st == "sel":
                    extra = f'<span class="selbox" id="{wid}b"></span>'
                    n = len(txt.replace("&nbsp;", " "))
                    js.append(f'  tl.set("#{wid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{r3(t)});\n'
                              f'  tl.to("#{wid}",{{clipPath:"inset(0% 0% 0% 0%)",duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(t)});\n'
                              f'  tl.fromTo("#{wid}b",{{scaleX:0}},{{scaleX:1,duration:{r3(n * 0.05)},ease:"steps({n})"}},{r3(t)});\n')
                elif st == "T":    # a cheat code typed on the TV, then the game's own confirmation
                    n = len(txt)
                    extra = f'<span class="sub" id="{wid}s">CHEAT ACTIVATED</span>'
                    js.append(f'  tl.set("#{wid}",{{opacity:1,clipPath:"inset(0% 100% 0% 0%)"}},{r3(t)});\n'
                              f'  tl.to("#{wid}",{{clipPath:"inset(0% 0% 0% 0%)",duration:{r3(n * 0.045)},ease:"steps({n})"}},{r3(t)});\n'
                              f'  tl.set("#{wid}s",{{opacity:1}},{r3(t + n * 0.045 + 0.05)});\n')
                elif st in ("S", "B", "X", "N", "Y"):
                    js.append(ent("#" + wid, "flash", t))
                    if st == "N" or st == "Y":
                        extra = f'<span class="yb" id="{wid}y"></span>'
                        js.append(year_flicker(f"#{wid}y", t))
                elif st == "k":
                    js.append(f'  tl.fromTo("#{wid}",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.25,ease:"power2.out"}},{r3(t + 0.2)});\n')
                elif st == "i":
                    js.append(ent("#" + wid, "ink", t))
                else:
                    kind = "soft" if bare in SMALL else ("bloom", "pop", "pop", "bloom", "pop")[(li + k) % 5]
                    k += 1
                    js.append(ent("#" + wid, kind, t))
                spans.append(f'<span class="w st-{st}">{extra}<span class="gh">{txt}</span><span class="ik"><span class="tx" id="{wid}">{txt}</span></span></span>')
            rows_html.append(f'<div class="row {mode}" id="{lid}r{ri}">{"".join(spans)}</div>')
        pos = "c" if Ln.align == "c" else Ln.align
        side = "" if pos == "c" else (f"left:{Ln.x}px;" if pos == "l" else f"right:{Ln.x}px;")
        body.append(f'<div id="{lid}" class="clip cl {pos}" data-start="{t0}" data-duration="{dur}" data-track-index="0" style="top:{Ln.y}px;{side}transform:translateY(-50%)">'
                    f'<div id="{lid}i">{"".join(rows_html)}</div></div>')
        js.append(f'  tl.fromTo("#{lid}i",{{x:22}},{{x:-14,duration:{dur},ease:"power2.out"}},{t0});\n')
        if dur > 0.5:
            js.append(f'  tl.to("#{lid}i",{{opacity:0,filter:"blur(8px)",duration:0.12,ease:"power2.in"}},{r3(t1 - 0.12)});\n')
    css = "#lines{position:absolute;inset:0;}\n"
    open(os.path.join(P, "compositions", "captions.html"), "w", encoding="utf-8").write(
        comp("captions", TOTAL, '<div id="lines">' + "\n".join(body) + "</div>", "".join(js), css))
    return len(LINES)


# ------------------------------------------------------------------ layers
def vtag(sid, t0, extra=""):
    s = SH[sid]
    return (f'<video id="v-{sid}" class="clip" src="assets/clips/{sid}.mp4" data-start="{r3(s["start"] - t0)}" '
            f'data-duration="{r3(s["end"] - s["start"])}" muted playsinline{extra}></video>')


def label_html(lid, text, cx, cy, style):
    parts = text.split("|")
    if len(parts) == 2:   # small word over a big one
        inner = (f'<span class="w st-s"><span class="gh">{parts[0]}</span><span class="ik"><span class="tx" id="{lid}a">{parts[0]}</span></span></span>'
                 f'<span class="w st-{style}"><span class="gh">{parts[1]}</span><span class="ik"><span class="tx" id="{lid}b">{parts[1]}</span></span>'
                 + (f'<span class="yb" id="{lid}y"></span>' if style in ("N", "Y") else "") + '</span>')
    else:
        inner = (f'<span class="w st-{style}"><span class="gh">{text}</span><span class="ik"><span class="tx" id="{lid}b">{text}</span></span>'
                 + (f'<span class="yb" id="{lid}y"></span>' if style in ("N", "Y") else "") + '</span>')
    return f'<div class="lab" style="left:{cx - 480}px;top:{cy - 200}px;width:960px;height:400px;z-index:60">{inner}</div>'


def layer_html(Ly, t0, z, idx):
    b, j = [], []
    k = Ly["kind"]
    if k == "full":
        s = SH[Ly["id"]]
        if Ly.get("crt"):
            b.append(f'<div class="crt" id="{Ly["id"]}-w" style="z-index:{z};opacity:0"><div class="tube">{vtag(Ly["id"], t0)}<div class="scan"></div><div class="glass"></div></div></div>')
            j.append(f'  tl.set("#{Ly["id"]}-w",{{opacity:1}},{r3(s["start"] - t0)});\n  tl.set("#{Ly["id"]}-w",{{opacity:0}},{r3(s["end"] - t0)});\n')
        else:
            b.append(f'<div class="shot" id="{Ly["id"]}-w" style="z-index:{z}">{vtag(Ly["id"], t0)}</div>')
        if Ly.get("push"):
            a, c = Ly["push"]
            j.append(f'  tl.fromTo("#{Ly["id"]}-w",{{scale:{a}}},{{scale:{c},duration:{r3(s["end"] - s["start"])},ease:"none"}},{r3(s["start"] - t0)});\n')
        if Ly.get("news"):
            zx, zy, kk = 1206, 980, 2.3
            tz = N(11) - 0.17
            b.append('<div class="box" id="nw-hl" style="left:604px;top:652px;width:652px;height:100px;mix-blend-mode:difference;transform-origin:0 50%;opacity:0;z-index:30"></div>')
            j.append(f'  tl.fromTo("#{Ly["id"]}-w",{{x:0,y:0,scale:1,transformOrigin:"0 0"}},{{x:{r3(960 - kk * zx)},y:{r3(700 - kk * zy)},scale:{kk},duration:0.42,ease:"power3.inOut"}},{r3(tz)});\n'
                     f'  tl.set("#nw-hl",{{opacity:1,scaleX:0}},{r3(N(12) + 0.02)});\n  tl.to("#nw-hl",{{scaleX:1,duration:0.3,ease:"power2.out"}},{r3(N(12) + 0.02)});\n')
        if Ly.get("rewind"):
            dur = r3(s["end"] - s["start"])
            st = r3(s["start"] - t0)
            b.append(f'<div class="clip" id="rw-o" data-start="{st}" data-duration="{dur}" style="position:absolute;inset:0;z-index:{z + 1}"><div class="vhs"></div>'
                     f'<div class="vband" id="rw-b" style="top:-140px"></div><div class="osdt">&#9664;&#9664; 2002</div></div>')
            j.append(f'  tl.fromTo("#rw-b",{{y:0}},{{y:1300,duration:{dur},ease:"none"}},{st});\n')
        if Ly.get("endcard"):
            st = r3(s["start"] - t0)
            b.append(f'<div class="lab" id="end-t" style="left:0;top:0;width:1920px;height:1080px;z-index:60">'
                     f'<div id="end-a" style="font-family:InterV,sans-serif;font-weight:800;font-size:76px;letter-spacing:0.08em;color:#F2F2F0;opacity:0;text-shadow:{SGLOW}">GRAND THEFT AUTO VI</div>'
                     f'<div id="end-l" style="width:520px;height:3px;background:#F2F2F0;margin:26px 0;transform-origin:50% 50%;opacity:0"></div>'
                     f'<div id="end-d" style="font-family:InterV,sans-serif;font-weight:600;font-size:36px;letter-spacing:0.42em;color:#F2F2F0;opacity:0">NOVEMBER 19, 2026</div></div>')
            j.append(ent("#end-a", "flash", st + 0.05) +
                     f'  tl.fromTo("#end-l",{{opacity:1,scaleX:0}},{{opacity:1,scaleX:1,duration:0.4,ease:"expo.out"}},{r3(st + 0.25)});\n'
                     f'  tl.fromTo("#end-d",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.3,ease:"power2.out"}},{r3(st + 0.45)});\n'
                     f'  tl.to("#{Ly["id"]}-w,#end-t",{{opacity:0,duration:0.45,ease:"power1.in"}},{r3(TOTAL - 0.45 - t0)});\n')
    elif k == "wall":
        g0, g1 = Ly["t0"], Ly["t1"]
        R, step = 1580, 21.6
        panels = []
        for i, sid in enumerate(Ly["ids"]):
            row, col = divmod(i, 6)
            ang = (col - 2.5) * step
            y = -172 if row == 0 else 172
            panels.append(f'<div class="wp" id="wp{i}" style="transform:rotateY({ang:.2f}deg) translateZ(-{R}px) translateY({y}px)">{vtag(sid, t0)}</div>')
            ti = r3(g0 - t0 + (abs(col - 2.5) // 1) * 0.034 + row * 0.017)
            j.append(f'  tl.set("#wp{i}",{{opacity:1}},{ti});\n')
        b.append(f'<div class="wall" id="wall" style="z-index:{z};opacity:0"><div class="ring" id="ring">{"".join(panels)}</div></div>')
        j.append(f'  tl.set("#wall",{{opacity:1}},{r3(g0 - t0)});\n  tl.set("#wall",{{opacity:0}},{r3(g1 - t0)});\n'
                 f'  tl.fromTo("#ring",{{rotationY:-6,z:{R - 80}}},{{rotationY:4,z:{R + 30},duration:{r3(g1 - g0)},ease:"power1.out"}},{r3(g0 - t0)});\n')
    elif k in ("split", "strips", "grid4"):
        g1 = Ly["t1"]
        for i, e in enumerate(Ly["els"]):
            rid = f"rc{idx}_{i}"
            b.append(f'<div class="rc" id="{rid}" style="left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px;z-index:{z};opacity:0">{vtag(e["id"], t0)}</div>'
                     f'<div class="box" id="{rid}f" style="left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px;z-index:{z + 1};opacity:0"></div>')
            ti = r3(e["t_in"] - t0)
            ta = r3(min(x["t_in"] for x in Ly["els"]) - t0 + i * 0.05)   # every panel builds in on the layout's first beat
            side = "inset(0% 0% 0% 100%)" if e["x"] > 0 else "inset(0% 100% 0% 0%)"
            if k == "grid4":
                side = "inset(100% 0% 0% 0%)" if e["y"] > 0 else "inset(0% 0% 100% 0%)"
            b.append(f'<div class="box" id="{rid}d" style="left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px;z-index:{z + 1};background:#000;opacity:0"></div>')
            j.append(f'  tl.set("#{rid}",{{opacity:1}},{ta});\n'
                     f'  tl.fromTo("#{rid}",{{clipPath:"{side}"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.28,ease:"expo.out"}},{ta});\n'
                     f'  tl.set("#{rid}f",{{opacity:0.85}},{ta});\n  tl.set("#{rid}f",{{opacity:0}},{r3(ta + 0.05)});\n')
            if ti > ta + 0.1:   # waits dimmed, then lights up with a flash on its own word
                j.append(f'  tl.set("#{rid}d",{{opacity:0.62}},{ta});\n  tl.set("#{rid}d",{{opacity:0}},{ti});\n'
                         f'  tl.set("#{rid}f",{{opacity:0.7}},{ti});\n  tl.set("#{rid}f",{{opacity:0}},{r3(ti + 0.05)});\n')
            j.append(f'  tl.set("#{rid},#{rid}f,#{rid}d",{{opacity:0}},{r3(g1 - t0)});\n')
            if i > 0:   # a hairline seam between panels
                b.append(f'<div class="box" id="{rid}s" style="left:{e["x"] - 2 if e["x"] else 0}px;top:{e["y"] - 2 if e["y"] else 0}px;'
                         f'width:{4 if e["x"] else e["w"]}px;height:{e["h"] if e["x"] else 4}px;background:#000;z-index:{z + 2};opacity:0"></div>')
                j.append(f'  tl.set("#{rid}s",{{opacity:1}},{ta});\n  tl.set("#{rid}s",{{opacity:0}},{r3(g1 - t0)});\n')
        for li, (text, ei, tt) in enumerate(Ly.get("labels", [])):
            e = Ly["els"][ei]
            lid = f"lb{idx}_{li}"
            style = "S" if Ly.get("serif") or (not text[0].isdigit() and "|" not in text and not Ly.get("small")) else "N"
            if "|" in text:
                style = "S" if not text.split("|")[1][0].isdigit() else "N"
            if Ly.get("small"):
                style = "s"
            cx, cy = e["x"] + e["w"] // 2, e["y"] + e["h"] // 2
            b.append(label_html(lid, text, cx, cy, style))
            off = (0.32 if k == "strips" else 0.44) if "|" in text else 0
            if "|" in text:
                j.append(ent(f"#{lid}a", "pop", tt - t0))
            j.append(ent(f"#{lid}b", "flash" if style != "s" else "pop", tt - t0 + off))
            if style == "N":
                j.append(year_flicker(f"#{lid}y", tt - t0))
            j.append(f'  tl.set("#{lid}a,#{lid}b",{{opacity:0}},{r3(g1 - t0)});\n' if "|" in text else f'  tl.set("#{lid}b",{{opacity:0}},{r3(g1 - t0)});\n')
    elif k == "cards":
        g1 = Ly["t1"]
        els = Ly["els"]
        c0 = els[0]
        b.append(f'<div class="shot" id="cbg{idx}" style="z-index:{z};opacity:0">{vtag(c0["id"], t0).replace(f'id="v-{c0["id"]}"', f'id="v-{c0["id"]}-bg"')}<div class="dimov"></div></div>')
        j.append(f'  tl.set("#cbg{idx}",{{opacity:1}},{r3(c0["t_in"] - t0)});\n  tl.set("#cbg{idx}",{{opacity:0}},{r3(g1 - t0)});\n')
        for i, e in enumerate(els):
            cid = f"fc{idx}_{i}"
            b.append(f'<div class="fc" id="{cid}" style="left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px;z-index:{z + 2 + i}">'
                     f'<div class="fci" style="transform:rotate({e["rot"]}deg)">{vtag(e["id"], t0)}</div></div>'
                     f'<div class="box" id="{cid}f" style="left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px;z-index:{z + 20};opacity:0;transform:rotate({e["rot"]}deg)"></div>')
            ti = r3(e["t_in"] - t0)
            dx = 14 if e["x"] < 900 else -14
            j.append(f'  tl.set("#{cid}f",{{opacity:0.9}},{ti});\n  tl.set("#{cid}f",{{opacity:0}},{r3(ti + 0.05)});\n'
                     f'  tl.set("#{cid}",{{opacity:1}},{r3(ti + 0.034)});\n'
                     f'  tl.fromTo("#{cid}",{{scale:1.08,x:0}},{{scale:1,x:{dx},duration:{r3(g1 - e["t_in"])},ease:"expo.out"}},{r3(ti + 0.034)});\n'
                     f'  tl.set("#{cid}",{{opacity:0}},{r3(g1 - t0)});\n')
    elif k == "osd_volume":
        a, c = Ly["steps"]
        bars = "".join(f'<div class="bar" id="vb{i}"></div>' for i in range(16))
        b.append(f'<div class="osd" id="osd" style="z-index:70"><div style="font-size:40px">VOLUME</div><div class="bars">{bars}</div>'
                 f'<div id="osd-m" style="font-size:56px;margin-top:14px;opacity:0">MUTE</div></div>')
        j.append(f'  tl.set("#osd",{{opacity:1}},{r3(Ly["t0"] - t0)});\n  tl.set("#osd",{{opacity:0}},{r3(Ly["t1"] - t0)});\n')
        for i in range(16):
            ti = a + (c - a) * (15 - i) / 16
            j.append(f'  tl.set("#vb{i}",{{opacity:0.12}},{r3(ti - t0)});\n')
        j.append(f'  tl.set("#osd-m",{{opacity:1}},{r3(c + 0.05 - t0)});\n')
    elif k == "band":
        b.append(f'<div class="band" id="band{idx}" style="z-index:65;opacity:0"></div>')
        j.append(f'  tl.set("#band{idx}",{{opacity:1}},{r3(Ly["t0"] - t0)});\n'
                 f'  tl.fromTo("#band{idx}",{{scaleY:0}},{{scaleY:1,duration:0.14,ease:"expo.out"}},{r3(Ly["t0"] - t0)});\n'
                 f'  tl.to("#band{idx}",{{scaleY:0.08,duration:0.12,ease:"power3.in"}},{r3(Ly["t1"] - t0 - 0.12)});\n'
                 f'  tl.set("#band{idx}",{{opacity:0}},{r3(Ly["t1"] - t0)});\n')
    return "\n".join(b), "".join(j)


SCENES = []


def build_scenes():
    for cid, t0, t1 in E.SECTIONS:
        body, js = [], []
        lys = [Ly for Ly in E.LAYERS if t0 - 1e-6 <= Ly["t0"] < t1 - 1e-6]
        for z, Ly in enumerate(lys, start=1):
            hb, hj = layer_html(Ly, t0, z * 3, f"{cid}{z}")
            body.append(hb); js.append(hj)
        SCENES.append((cid, t0, t1))
        open(os.path.join(P, "compositions", cid + ".html"), "w", encoding="utf-8").write(comp(cid, t1 - t0, "\n".join(body), "".join(js)))


def build_fx():
    flashes = [NEWS_DUR, cut(90), cut(212), cut(222), cut(241), W(287) - 0.04, 103.85]
    cuts = sorted({l["t0"] for l in E.LAYERS if l["kind"] == "full" and 1 < l["t0"] < TOTAL - 1})
    body, js = [], []
    for k, t in enumerate(flashes):
        fid = f"fl{k}"
        body.append(f'<div class="clip" id="{fid}" data-start="{r3(t - 0.1)}" data-duration="0.45" style="position:absolute;inset:0;z-index:50"><div class="fl" id="{fid}i"></div></div>')
        js.append(f'  tl.fromTo("#{fid}i",{{opacity:0}},{{opacity:0.85,duration:0.1,ease:"power2.in"}},{r3(t - 0.1)});\n'
                  f'  tl.set("#{fid}i",{{opacity:1}},{r3(t)});\n  tl.to("#{fid}i",{{opacity:0,duration:0.3,ease:"power2.out"}},{r3(t + 0.034)});\n')
    PAT = [[("inv", 520, 300, 980, 420)], [("glass", 430, 455, 1060, 170)], [("bar", 1090, 260, 70, 560)],
           [("inv", 0, 0, 1920, 380), ("inv", 1320, 640, 600, 440)], [("glass", 240, 120, 760, 520)], [("inv", 120, 620, 860, 300)]]
    STY = {"inv": "background:#fff;mix-blend-mode:difference;", "bar": "background:rgba(255,255,255,0.95);", "glass": "background:rgba(255,255,255,0.22);"}
    n = 0
    for i, t in enumerate(cuts):
        if any(abs(t - f) < 0.3 for f in flashes) or i % 4 != 0:
            continue
        boxes = "".join(f'<div class="gb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{STY[kd]}"></div>' for kd, x, y, w, h in PAT[n % len(PAT)])
        body.append(f'<div class="clip" id="sq{i:03d}" data-start="{r3(t - 0.034)}" data-duration="0.067" style="position:absolute;inset:0;z-index:49">{boxes}</div>')
        n += 1
    css = """
.fl{position:absolute;inset:0;background:#fff;opacity:0;}
.gb{position:absolute;}
.grain{position:absolute;left:-200px;top:-200px;width:2320px;height:1480px;background:url("assets/tex/grain.png");opacity:0.07;mix-blend-mode:overlay;}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.40) 100%);}
"""
    body.append('<div class="vig"></div><div class="grain" id="fx-grain"></div>')
    js.append(f'  tl.fromTo("#fx-grain",{{x:0,y:0}},{{x:-180,y:-140,duration:{TOTAL},ease:"steps({int(TOTAL * 15)})"}},0);\n')
    open(os.path.join(P, "compositions", "fx.html"), "w", encoding="utf-8").write(comp("fx", TOTAL, "\n".join(body), "".join(js), css))
    return n


def build_root():
    hosts = []
    for k, (cid, t0, t1) in enumerate(SCENES):
        hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{r3(t0)}" '
                     f'data-duration="{r3(t1 - t0)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:{k + 1}"></div>')
    hosts.append(f'      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:90;pointer-events:none"></div>')
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080" style="position:absolute;inset:0;z-index:80;pointer-events:none"></div>')
    aud = [f'      <audio id="a-news" src="assets/audio/news_line.wav" data-start="0" data-duration="{NEWS_DUR}" data-track-index="5" data-volume="1"></audio>',
           f'      <audio id="a-cj" src="assets/audio/cj_line.wav" data-start="{NEWS_DUR}" data-duration="{r3(VO_OFFSET - NEWS_DUR + 0.2)}" data-track-index="6" data-volume="1"></audio>',
           f'      <audio id="a-vo" src="assets/audio/vo.wav" data-start="{VO_OFFSET}" data-duration="96.44" data-track-index="7" data-volume="1"></audio>']
    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="bg" style="position:absolute;inset:0;background:#000"></div>
{chr(10).join(hosts)}
{chr(10).join(aud)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    open(os.path.join(P, "index.html"), "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    n = build_captions()
    build_scenes()
    sq = build_fx()
    build_root()
    keep = {c[0] for c in SCENES} | {"captions", "fx"}
    for f in os.listdir(os.path.join(P, "compositions")):
        if f.endswith(".html") and f[:-5] not in keep:
            os.remove(os.path.join(P, "compositions", f))
    print(f"v3: {n} caption lines | {len(SCENES)} scenes | {len(E.LAYERS)} layers | {sq} square flashes | no sfx")
