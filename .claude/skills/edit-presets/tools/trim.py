"""Copy out of blackrock-open/tools only the code the presets use: start from each preset's entry functions, follow
every name they reference (same module, star imports, module aliases, function-level imports) and write trimmed
copies of the modules, statements in their original order with the comments directly above them.

Run from the skill folder: python3 -I tools/trim.py lib
(it rewrites lib/*.py and copies the word timings to lib/words)
"""
import ast
import builtins
import json
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
TOOLS = os.path.join(REPO, "blackrock-open", "tools")
PROJECT = {os.path.splitext(f)[0] for f in os.listdir(TOOLS) if f.endswith(".py")}

ENTRIES = {
    "powerful-man-rise": [("prep_v10", "fink_cut2"), ("prep_v10", "fink_plates3"), ("prep_v10", "r_wall5"),
                          ("prep_v16", "r_open"), ("prep_v17", "r_bgs"), ("build", "s_first")],
    "name-mosaic": [("prep_v9", "r_mosaic"), ("build", "s_name")],
    "built-red-word": [("prep_v10", "r_company2"), ("prep_v10", "r_built"), ("build", "s_hook")],
    "founder-squares": [("prep_v10", "r_founders2")],
    "counter-roll": [("prep_v17", "r_count3")],
    "crisis-date-grid": [("prep_v17", "r_date2"), ("prep_v17", "r_grid2"), ("prep_v16", "r_gov"), ("build", "s_crisis")],
    "money-handoff": [("prep_v17", "r_money2"), ("build", "s_money")],
}
# always kept: the scene writer and the helpers every scene file needs
ALWAYS = [("build", "Scene"), ("build", "FONTS"), ("timing", "F"), ("common", "Writer")]


def is_main(st):
    return (isinstance(st, ast.If) and isinstance(st.test, ast.Compare) and isinstance(st.test.left, ast.Name)
            and st.test.left.id == "__name__")


def target_names(t):
    """(defined names, mutated base names) of an assignment target"""
    if isinstance(t, ast.Name):
        return [t.id], []
    if isinstance(t, (ast.Tuple, ast.List)):
        d, m = [], []
        for e in t.elts:
            a, b = target_names(e)
            d += a
            m += b
        return d, m
    base = t
    while isinstance(base, (ast.Subscript, ast.Attribute)):
        base = base.value
    return [], ([base.id] if isinstance(base, ast.Name) else [])


class Mod:
    def __init__(self, name):
        self.name = name
        self.src = open(f"{TOOLS}/{name}.py").read()
        self.lines = self.src.splitlines()
        self.tree = ast.parse(self.src)
        self.defs, self.attach, self.aliases, self.star, self.fromnames = {}, {}, {}, [], {}
        self.imports = []
        for k, st in enumerate(self.tree.body):
            if k == 0 and isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant):
                continue                                            # the module docstring
            if is_main(st):
                continue
            if isinstance(st, ast.Import):
                self.imports.append(k)
                for a in st.names:
                    if a.name in PROJECT:
                        self.aliases[a.asname or a.name] = a.name
            elif isinstance(st, ast.ImportFrom):
                self.imports.append(k)
                if st.module in PROJECT:
                    for a in st.names:
                        if a.name == "*":
                            self.star.append(st.module)
                        else:
                            self.fromnames[a.asname or a.name] = (st.module, a.name)
            elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.defs.setdefault(st.name, []).append(k)
            elif isinstance(st, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                tg = st.targets if isinstance(st, ast.Assign) else [st.target]
                for t in tg:
                    d, m = target_names(t)
                    for n in d:
                        (self.attach if isinstance(st, ast.AugAssign) else self.defs).setdefault(n, []).append(k)
                    for n in m:
                        self.attach.setdefault(n, []).append(k)
            elif isinstance(st, ast.Expr):
                base = st.value
                while isinstance(base, (ast.Call, ast.Attribute, ast.Subscript)):
                    base = base.func if isinstance(base, ast.Call) else base.value
                if isinstance(base, ast.Name):
                    self.attach.setdefault(base.id, []).append(k)
            else:                                                   # for / if / try / with at module level
                for n in ast.walk(st):
                    if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                        self.defs.setdefault(n.id, []).append(k)


MODS = {}


def mod(name):
    if name not in MODS:
        MODS[name] = Mod(name)
    return MODS[name]


def resolve(mname, name, seen=None):
    """-> (module, [stmt indices]) defining `name` as seen from module `mname`, or None"""
    m = mod(mname)
    if name in m.defs:
        return mname, sorted(set(m.defs[name] + m.attach.get(name, [])))
    if name in m.fromnames:
        return resolve(*m.fromnames[name])
    for s in m.star:
        r = resolve(s, name)
        if r:
            return r
    return None


NEED = {}                  # module -> set of stmt indices
USED_ALIAS = {}            # module -> set of alias names used
UNRESOLVED = {}
BUILTIN = set(dir(builtins))


def need(mname, idxs):
    s = NEED.setdefault(mname, set())
    new = [i for i in idxs if i not in s]
    s.update(new)
    for i in new:
        scan(mname, mod(mname).tree.body[i])


def scan(mname, st):
    m = mod(mname)
    local_alias = {}
    for n in ast.walk(st):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name in PROJECT:
                    local_alias[a.asname or a.name] = a.name
                    mod(a.name)
        elif isinstance(n, ast.ImportFrom) and n.module in PROJECT and n is not st:
            for a in n.names:
                r = resolve(n.module, a.name)
                if r:
                    need(*r)
    params = set()
    for n in ast.walk(st):
        if isinstance(n, ast.arg):
            params.add(n.arg)
    for n in ast.walk(st):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name):
            a = n.value.id
            tgt = local_alias.get(a) or m.aliases.get(a)
            if tgt:
                USED_ALIAS.setdefault(mname, set()).add(a)
                r = resolve(tgt, n.attr)
                if r:
                    need(*r)
                else:
                    UNRESOLVED.setdefault(tgt, set()).add(n.attr)
        if isinstance(n, ast.Name):
            if n.id in m.aliases:
                USED_ALIAS.setdefault(mname, set()).add(n.id)
                continue
            if n.id in local_alias:
                continue
            r = resolve(mname, n.id)
            if r:
                need(*r)
            elif isinstance(n.ctx, ast.Load) and n.id not in BUILTIN and n.id not in params:
                UNRESOLVED.setdefault(mname, set()).add(n.id)


def start_line(st):
    ln = st.lineno
    for d in getattr(st, "decorator_list", []):
        ln = min(ln, d.lineno)
    return ln


ROOT_LINE = 'ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))'
ENV = """# edit-presets: where the code reads and writes. Default: this repo's BlackRock project. For a new edit set
# PRESET_ROOT (the HyperFrames project: assets/clips, assets/img, assets/fonts, compositions), PRESET_SRC (its
# source media, the old blackrock-src) and PRESET_REPO (the repo, for dimon-src).
REPO = os.environ.get("PRESET_REPO") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
ROOT = os.environ.get("PRESET_ROOT") or os.path.join(REPO, "blackrock-open")"""


def fix_paths(mname, text):
    if mname in ("common", "build"):
        assert text.count(ROOT_LINE) == 1, mname
        text = text.replace(ROOT_LINE, ENV)
    if mname == "common":
        a = 'SRC = os.path.abspath(os.path.join(ROOT, "..", "blackrock-src"))'
        assert text.count(a) == 1
        text = text.replace(a, 'SRC = os.environ.get("PRESET_SRC") or os.path.join(REPO, "blackrock-src")')
    text = text.replace("{ROOT}/../", "{REPO}/")
    assert "/../" not in text.replace("../..", ""), mname
    return text


def emit(mname, out_dir):
    m = mod(mname)
    keep = NEED.get(mname, set())
    used = USED_ALIAS.get(mname, set())
    chunks = [f'"""Trimmed from blackrock-open/tools/{mname}.py for the edit-presets skill: only the code the presets use,\n'
              f'copied as it is (comments included). See SKILL.md for the paths this reads and writes."""']
    order = sorted(set(keep) | set(m.imports))
    for i in order:
        st = m.tree.body[i]
        if i in m.imports and i not in keep:
            mods = [a.name for a in st.names] if isinstance(st, ast.Import) else [st.module]
            if isinstance(st, ast.Import):
                ok = all(a.name not in PROJECT or (a.asname or a.name) in used for a in st.names)
            else:
                ok = st.module not in PROJECT or any(a.name == "*" for a in st.names) or st.module in [x for x in mods]
                if st.module in PROJECT and not any(a.name == "*" for a in st.names):
                    ok = any((a.asname or a.name) in used or resolve(mname, a.asname or a.name) for a in st.names)
            if not ok:
                continue
        a, b = start_line(st) - 1, st.end_lineno
        while a > 0 and m.lines[a - 1].lstrip().startswith("#"):
            a -= 1
        chunks.append("\n".join(m.lines[a:b]))
    text = "\n\n".join(chunks) + "\n"
    text = fix_paths(mname, text)
    open(f"{out_dir}/{mname}.py", "w").write(text)
    return len(keep), text.count("\n")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for mn, nm in ALWAYS:
        r = resolve(mn, nm)
        need(*r)
    per = {}
    for preset, ents in ENTRIES.items():
        for mn, nm in ents:
            r = resolve(mn, nm)
            assert r, (mn, nm)
            need(*r)
    # star-imported modules and aliased modules must exist even when nothing of theirs is used
    for mn in list(NEED):
        for s in mod(mn).star:
            NEED.setdefault(s, set())
    import shutil
    os.makedirs(f"{out}/words", exist_ok=True)
    for w in ("open", "open2", "rest", "rogan", "pace"):
        shutil.copy(f"{TOOLS}/words/{w}.json", f"{out}/words/{w}.json")
    for mn in sorted(NEED):
        k, n = emit(mn, out)
        print(f"{mn:10s} {k:4d} statements  {n:5d} lines")
    print("unresolved (expected: locals, comprehension vars):")
    for k, v in UNRESOLVED.items():
        print(" ", k, sorted(v)[:60])
