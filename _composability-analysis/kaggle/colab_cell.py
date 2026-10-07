import gzip, base64, json
ANN = json.loads(gzip.decompress(base64.b64decode("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")))

import json, math, random, time, threading, collections
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
