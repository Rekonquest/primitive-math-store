#!/usr/bin/env python3
"""
Type-specificity-weighted composition finder (the refinement).

Problem in compose_check.py: pipelines ranked by domain-count routed through
weak hub types (scalar, decision) that match almost anything. Fix: weight every
type by specificity (IDF-style -- rare handoff types carry real structure, common
ones are glue), score an edge by its STRONGEST shared type, and rank pipelines by
MEAN joint strength (not length, not domain count -- avoids the size trap).

Reads annotations.json. Std-lib only. Deterministic (seeded).
"""
from __future__ import annotations
import json
import math
import os
import random
from collections import Counter, defaultdict

random.seed(13)
HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    raw = json.load(open(os.path.join(HERE, "annotations.json"), encoding="utf-8"))
    prim = {}
    for a in raw:
        n = a["name"]
        p = prim.setdefault(n, {"domain": a["domain"], "in": set(), "out": set()})
        p["in"] |= set(a["inputs"])
        p["out"] |= set(a["outputs"])
    return prim


def type_specificity(prim):
    """IDF-style: a type that many primitives both produce AND consume is a weak
    hub; a type few touch is specific. spec = log(N^2 / (producers*consumers))."""
    n = len(prim)
    producers = Counter(t for p in prim.values() for t in p["out"])
    consumers = Counter(t for p in prim.values() for t in p["in"])
    spec = {}
    for t in set(producers) | set(consumers):
        pc = max(producers.get(t, 0), 1) * max(consumers.get(t, 0), 1)
        spec[t] = math.log((n * n) / pc)
    return spec, producers, consumers


def build_weighted(prim, spec):
    """Edge A->B weighted by the strongest (most specific) shared handoff type."""
    adj = defaultdict(list)
    names = list(prim)
    for a in names:
        oa = prim[a]["out"]
        if not oa:
            continue
        for b in names:
            if a == b:
                continue
            shared = oa & prim[b]["in"]
            if not shared:
                continue
            t = max(shared, key=lambda x: spec[x])
            adj[a].append((b, t, spec[t]))
    return adj


def best_pipelines(prim, adj, trials=120000, max_len=6, min_len=3):
    """Random-restart greedy preferring HIGH-SPECIFICITY next joints. Rank by mean
    joint strength so a few strong joints beat many weak ones (no length bias)."""
    names = list(prim)
    found = {}
    for _ in range(trials):
        start = random.choice(names)
        path, doms, joints = [start], {prim[start]["domain"]}, []
        target = random.randint(min_len, max_len)
        while len(path) < target:
            nbrs = [(b, t, w) for (b, t, w) in adj.get(path[-1], []) if b not in path]
            if not nbrs:
                break
            # weighted pick favouring strong, domain-fresh joints
            def keyf(e):
                b, t, w = e
                return w + (1.5 if prim[b]["domain"] not in doms else 0.0)
            nbrs.sort(key=keyf, reverse=True)
            b, t, w = nbrs[random.randint(0, min(2, len(nbrs) - 1))]
            path.append(b); doms.add(prim[b]["domain"]); joints.append((t, w))
        if len(path) >= min_len and joints:
            mean_w = sum(w for _, w in joints) / len(joints)
            key = tuple(sorted(path))
            cand = (round(mean_w, 4), len(doms), len(path), path, joints)
            if key not in found or cand > found[key]:
                found[key] = cand
    return sorted(found.values(), reverse=True)


def main():
    prim = load()
    spec, producers, consumers = type_specificity(prim)
    print(f"Loaded {len(prim)} typed primitives.")
    print()
    print("Type specificity (high = meaningful handoff, low = weak glue):")
    for t, s in sorted(spec.items(), key=lambda kv: kv[1], reverse=True):
        tag = "STRONG" if s > 4.0 else ("weak-glue" if s < 2.5 else "")
        print(f"  {t:<13} spec={s:5.2f}  (produced x consumed = {producers.get(t,0)}x{consumers.get(t,0)})  {tag}")
    print()

    adj = build_weighted(prim, spec)
    pipes = best_pipelines(prim, adj)

    print("=" * 74)
    print("TOP PIPELINES BY JOINT STRENGTH (strong-typed, not hub-glued)")
    print("=" * 74)
    shown = 0
    for mean_w, ndoms, length, path, joints in pipes:
        if shown >= 8 or ndoms < 3 or length < 4:
            continue
        flow = path[0]
        for nm, (t, w) in zip(path[1:], joints):
            flow += f" =[{t} {w:.1f}]=> {nm}"
        print(f"\n[mean joint {mean_w:.2f} | {length} steps | {ndoms} domains]")
        print(f"  {flow}")
        shown += 1
    print()

    # contrast: weakest "impressive-looking" chains the OLD ranking would surface
    print("=" * 74)
    print("CONTRAST  strongest single bridges (most specific handoffs in the store)")
    print("=" * 74)
    edges = [(w, a, b, t) for a in adj for (b, t, w) in adj[a]
             if prim[a]["domain"] != prim[b]["domain"]]
    edges.sort(reverse=True)
    seen = set()
    for w, a, b, t in edges:
        k = (prim[a]["domain"], prim[b]["domain"], t)
        if k in seen:
            continue
        seen.add(k)
        print(f"  [{t} {w:.1f}] {a} ({prim[a]['domain']}) -> {b} ({prim[b]['domain']})")
        if len(seen) >= 10:
            break


if __name__ == "__main__":
    main()
