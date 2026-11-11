"""Zip the project with only the media its HTML refers to (the full assets folder holds every earlier round's media).

usage: python3 -I tools/pack_project.py v16        -> renders/jpm-dimon-v16-project.zip
The zip unpacks to jpm-dimon/ and previews with `npx --yes hyperframes@0.9.2 preview`."""
import os, re, sys, zipfile

PRJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver = sys.argv[1] if len(sys.argv) > 1 else "vX"
n = ver.lstrip("v")
keep = ["index.html", "package.json", "meta.json", "hyperframes.json", "CLAUDE.md", "vendor/gsap.min.js",
        f"notes/{ver}/notes.md", f"tools/build{n}.py", "tools/prep2.py", f"tools/media_{ver}.json"]
keep += [f"tools/{f}" for f in sorted(os.listdir(f"{PRJ}/tools")) if re.fullmatch(r"prep1[3-9]\.py|pack_project\.py", f)]
html = ["index.html"]
for root, _, files in os.walk(f"{PRJ}/compositions"):
    for f in sorted(files):
        if f.endswith(".html"):
            html.append(os.path.relpath(os.path.join(root, f), PRJ))
used = set()
for h in html:
    used.update(re.findall(r"assets/[A-Za-z0-9_./@-]+\.[A-Za-z0-9]+", open(f"{PRJ}/{h}", encoding="utf-8").read()))
fonts = [f"assets/fonts/{f}" for f in sorted(os.listdir(f"{PRJ}/assets/fonts")) if f.endswith(".txt")]   # the licences
missing = sorted(u for u in used if not os.path.exists(f"{PRJ}/{u}"))
if missing:
    raise SystemExit(f"referenced but not on disk: {missing[:8]}")
out = f"{PRJ}/renders/jpm-dimon-{ver}-project.zip"
names = sorted(set(keep + html + sorted(used) + fonts))
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in names:
        if os.path.exists(f"{PRJ}/{name}"):
            z.write(f"{PRJ}/{name}", f"jpm-dimon/{name}")
print(out, len(names), "files", round(os.path.getsize(out) / 1e6, 1), "MB")
