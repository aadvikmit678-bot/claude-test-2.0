// Renders "BE THE HERO" (InterV, the edit's own typeface) as a 1920x1080 transparent PNG for tools/hero4.py:
// "BE THE" ends just left of Jason's head and "HERO" starts just right of it, so he stands between the words and
// Lucia's hair covers the foot of "THE".   usage: node GTA6-v3/tools/text4.cjs
const path = require("path");
const { chromium } = require("playwright");
const proj = path.join(__dirname, "..", "gta6-edit");
// the font goes in as a data URL: a page made with setContent cannot load file:// fonts
const font = "data:font/woff2;base64," + require("fs").readFileSync(path.join(proj, "assets", "fonts", "InterVar-latin.woff2")).toString("base64");
// "node text4.cjs problem": BE THE PROBLEM for the bad guys' art (the user: written "exactly like BE THE HERO"): "BE THE" ends
// just left of Trevor's head, above Franklin, and "PROBLEM" starts just right of it
const PROBLEM = process.argv[2] === "problem";
const SPEC = PROBLEM ? { size: 140, top: 100, aRight: 866, a: "BE THE", bLeft: 1248, b: "PROBLEM", out: "be_the_problem.png" }
                     : { size: 195, top: 150, aRight: 885, a: "BE THE", bLeft: 1290, b: "HERO", out: "be_the_hero.png" };
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const st = `position:absolute;top:${SPEC.top}px;font-family:"InterV";font-weight:800;font-size:${SPEC.size}px;letter-spacing:-0.035em;line-height:1;color:#fff;white-space:nowrap;text-shadow:0 0 34px rgba(255,255,255,0.55),0 0 9px rgba(255,255,255,0.45);`;
  await page.setContent(`<html><head><style>
    @font-face{font-family:"InterV";src:url("${font}") format("woff2");font-weight:100 900;}
    html,body{margin:0;background:transparent;width:1920px;height:1080px;overflow:hidden;}
  </style></head><body>
    <div id="a" style='${st}right:${1920 - SPEC.aRight}px;text-align:right'>${SPEC.a}</div>
    <div id="b" style='${st}left:${SPEC.bLeft}px'>${SPEC.b}</div></body></html>`);
  await page.evaluate(() => document.fonts.ready);
  const ok = await page.evaluate(() => document.fonts.check('800 100px "InterV"'));
  if (!ok) throw new Error("InterV did not load");
  const box = await page.evaluate(() => ["a", "b"].map(id => { const r = document.createRange(); r.selectNodeContents(document.getElementById(id));
    const b = r.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; }));
  await page.screenshot({ path: path.join(proj, "assets", "img", SPEC.out), omitBackground: true });
  console.log(SPEC.out, JSON.stringify(box));
  await browser.close();
})();
