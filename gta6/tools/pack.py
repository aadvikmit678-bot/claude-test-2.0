"""Zip the GTA 6 HyperFrames project (everything needed to preview and re-render it).   python3 -I gta6/tools/pack.py OUT.zip"""
import os, sys, zipfile
ROOT = "/home/user/claude-test-2.0/gta6"
out = sys.argv[1]
keep = ["index.html", "package.json", "meta.json", "hyperframes.json", "CLAUDE.md", "AGENTS.md", "SPEC.md", "REVIEW.md",
        "compositions", "assets", "vendor", "tools", "notes"]
n = 0
with zipfile.ZipFile(out, "w") as z:
    for k in keep:
        p = f"{ROOT}/{k}"
        if os.path.isfile(p):
            z.write(p, f"gta6/{k}", compress_type=zipfile.ZIP_DEFLATED); n += 1
        elif os.path.isdir(p):
            for dp, _, fs in os.walk(p):
                for f in fs:
                    fp = f"{dp}/{f}"
                    if "/__pycache__" in fp:
                        continue
                    ct = zipfile.ZIP_STORED if f.endswith((".mp4", ".jpg", ".png", ".woff2", ".mp3")) else zipfile.ZIP_DEFLATED
                    z.write(fp, "gta6/" + os.path.relpath(fp, ROOT), compress_type=ct); n += 1
print(out, n, "files", round(os.path.getsize(out) / 1e6, 1), "MB")
