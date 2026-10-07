#!/usr/bin/env python3
"""Build a self-contained Kaggle kernel (run.py) for the FIXED composition
simulation: type-specificity-weighted composition search over the typed
primitive store. Embeds the annotations inline so no Kaggle dataset is needed.

Usage: python make_run.py <annotations.json> <time_budget_sec>
Writes ./run.py
"""
import json
import sys

anno_path = sys.argv[1] if len(sys.argv) > 1 else "../annotations.json"
budget = int(sys.argv[2]) if len(sys.argv) > 2 else 120

annotations = json.load(open(anno_path, encoding="utf-8"))

KERNEL = '''#!/usr/bin/env python3
# Auto-generated Kaggle kernel: type-specificity-weighted composition search.
import json, math, random, time, os
from collections import Counter, defaultdict

random.seed(13)

def build(rows):
    prim = {}
    for a in rows:
        p = prim.setdefault(a["name"], {"domain": a["domain"], "in": set(), "out": set()})
        p["in"] |= set(a["inputs"]); p["out"] |= set(a["outputs"])
    return prim

def specificity(prim):
    n = len(prim)
    prod = Counter(t for p in prim.values() for t in p["out"])
    cons = Counter(t for p in prim.values() for t in p["in"])
    spec = {t: math.log((n * n) / (max(prod.get(t, 0), 1) * max(cons.get(t, 0), 1)))
            for t in set(prod) | set(cons)}
    return spec, prod, cons

def adjacency(prim, spec):
    adj = defaultdict(list); names = list(prim)
    for a in names:
        oa = prim[a]["out"]
        if not oa: continue
        for b in names:
            if a == b: continue
            sh = oa & prim[b]["in"]
            if sh:
                t = max(sh, key=lambda x: spec[x]); adj[a].append((b, t, spec[t]))
    return adj

def search(prim, adj, budget, max_len=8, min_len=3):
    names = list(prim); found = {}; t0 = time.time(); trials = 0; last = t0
    while time.time() - t0 < budget:
        for _ in range(20000):
            trials += 1
            start = random.choice(names); path = [start]
            doms = {prim[start]["domain"]}; joints = []
            target = random.randint(min_len, max_len)
            while len(path) < target:
                nbrs = [(b, t, w) for (b, t, w) in adj.get(path[-1], ()) if b not in path]
                if not nbrs: break
                nbrs.sort(key=lambda e: e[2] + (1.5 if prim[e[0]]["domain"] not in doms else 0.0),
                          reverse=True)
                b, t, w = nbrs[random.randint(0, min(2, len(nbrs) - 1))]
                path.append(b); doms.add(prim[b]["domain"]); joints.append((t, round(w, 3)))
            if len(path) >= min_len and joints:
                mw = sum(w for _, w in joints) / len(joints)
                key = tuple(sorted(path))
                cand = (round(mw, 4), len(doms), len(path), path, joints)
                if key not in found or cand > found[key]:
                    found[key] = cand
        if len(found) > 6000:
            top = sorted(found.values(), reverse=True)[:3000]
            found = {tuple(sorted(c[3])): c for c in top}
        if time.time() - last > 300:  # periodic checkpoint
            last = time.time()
            _dump(prim, adj, sorted(found.values(), reverse=True), trials, partial=True)
    return sorted(found.values(), reverse=True), trials

def _dump(prim, adj, pipes, trials, partial=False):
    edges = sum(len(v) for v in adj.values())
    spec, _, _ = specificity(prim)
    out = {
        "partial": partial, "primitives": len(prim), "edges": edges,
        "edge_density": edges / (len(prim) * (len(prim) - 1)) if len(prim) > 1 else 0,
        "trials": trials,
        "type_specificity": {t: round(s, 3) for t, s in sorted(spec.items(), key=lambda kv: -kv[1])},
        "top_pipelines": [
            {"mean_joint": mw, "domains": nd, "len": ln, "path": path, "joints": joints}
            for (mw, nd, ln, path, joints) in pipes[:300]
        ],
    }
    base = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
    json.dump(out, open(os.path.join(base, "results.json"), "w"))
    return out

def main():
    prim = build(ANNOTATIONS)
    spec, prod, cons = specificity(prim)
    adj = adjacency(prim, spec)
    print("primitives=%d budget=%ds" % (len(prim), TIME_BUDGET_SEC), flush=True)
    pipes, trials = search(prim, adj, TIME_BUDGET_SEC)
    out = _dump(prim, adj, pipes, trials, partial=False)
    print("DONE primitives=%d edges=%d density=%.3f trials=%d pipelines=%d"
          % (out["primitives"], out["edges"], out["edge_density"], trials, len(pipes)), flush=True)
    for p in out["top_pipelines"][:15]:
        flow = p["path"][0]
        for nm, (t, w) in zip(p["path"][1:], p["joints"]):
            flow += " =[%s %.1f]=> %s" % (t, w, nm)
        print("[mean %.2f | %d steps | %d dom] %s"
              % (p["mean_joint"], p["len"], p["domains"], flow), flush=True)

main()
'''

with open("run.py", "w", encoding="utf-8") as f:
    f.write("ANNOTATIONS = " + json.dumps(annotations) + "\n")
    f.write("TIME_BUDGET_SEC = %d\n\n" % budget)
    f.write(KERNEL)

print("wrote run.py: %d primitives embedded, budget=%ds" % (len(annotations), budget))
