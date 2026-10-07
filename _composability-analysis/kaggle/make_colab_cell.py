#!/usr/bin/env python3
"""Emit a single self-contained Colab cell (colab_cell.py): the type-specificity
composition search + embedded typed primitives, run as a 6h background thread
that checkpoints /content/results.json every 60s."""
import json

ann = json.load(open("../annotations.json", encoding="utf-8"))
compact = [{"n": a["name"], "d": a["domain"], "i": a["inputs"], "o": a["outputs"]} for a in ann]

BODY = '''import json, math, random, time, threading, collections
random.seed(13)

def build(rows):
    prim = {}
    for a in rows:
        p = prim.setdefault(a["n"], {"d": a["d"], "i": set(), "o": set()})
        p["i"] |= set(a["i"]); p["o"] |= set(a["o"])
    return prim

def spec(prim):
    n = len(prim)
    P = collections.Counter(t for p in prim.values() for t in p["o"])
    C = collections.Counter(t for p in prim.values() for t in p["i"])
    return {t: math.log((n*n)/(max(P.get(t,0),1)*max(C.get(t,0),1))) for t in set(P)|set(C)}

def adjacency(prim, sp):
    adj = {a: [] for a in prim}
    for a in prim:
        oa = prim[a]["o"]
        if not oa: continue
        for b in prim:
            if a == b: continue
            sh = oa & prim[b]["i"]
            if sh:
                t = max(sh, key=lambda x: sp[x]); adj[a].append((b, t, sp[t]))
    return adj

STATE = {"trials": 0, "top": [], "done": False, "started": time.time()}

def worker(prim, adj, budget, max_len=8, min_len=3):
    names = list(prim); found = {}; t0 = time.time(); last = 0
    while time.time() - t0 < budget:
        for _ in range(20000):
            STATE["trials"] += 1
            s = random.choice(names); path = [s]; doms = {prim[s]["d"]}; joints = []
            tgt = random.randint(min_len, max_len)
            while len(path) < tgt:
                nb = [(b, t, w) for (b, t, w) in adj[path[-1]] if b not in path]
                if not nb: break
                nb.sort(key=lambda e: e[2] + (1.5 if prim[e[0]]["d"] not in doms else 0), reverse=True)
                b, t, w = nb[random.randint(0, min(2, len(nb) - 1))]
                path.append(b); doms.add(prim[b]["d"]); joints.append((t, round(w, 3)))
            if len(path) >= min_len and joints:
                mw = sum(w for _, w in joints) / len(joints); key = tuple(sorted(path))
                cand = (round(mw, 4), len(doms), len(path), path, joints)
                if key not in found or cand > found[key]: found[key] = cand
        if len(found) > 6000:
            found = {tuple(sorted(c[3])): c for c in sorted(found.values(), reverse=True)[:3000]}
        if time.time() - last > 60:
            last = time.time()
            top = sorted(found.values(), reverse=True)[:250]
            STATE["top"] = top
            json.dump({"trials": STATE["trials"], "elapsed": round(time.time()-STATE["started"]),
                       "top": top}, open("/content/results.json", "w"))
    STATE["done"] = True
    json.dump({"trials": STATE["trials"], "elapsed": round(time.time()-STATE["started"]),
               "done": True, "top": sorted(found.values(), reverse=True)[:400]},
              open("/content/results.json", "w"))

prim = build(ANN); sp = spec(prim); adj = adjacency(prim, sp)
print("CLOUD RUN primitives=%d edges=%d" % (len(prim), sum(len(v) for v in adj.values())), flush=True)
th = threading.Thread(target=worker, args=(prim, adj, 21600), daemon=True); th.start()
print("background composition search started on Colab (budget 6h, checkpoints every 60s)", flush=True)
'''

import gzip, base64
blob = base64.b64encode(gzip.compress(json.dumps(compact, separators=(",", ":")).encode())).decode()

with open("colab_cell.py", "w", encoding="utf-8") as f:
    f.write("import gzip, base64, json\n")
    f.write('ANN = json.loads(gzip.decompress(base64.b64decode("' + blob + '")))\n\n')
    f.write(BODY)

print("wrote colab_cell.py: %d primitives, %d bytes (blob %d)"
      % (len(compact), len(open("colab_cell.py").read()), len(blob)))
