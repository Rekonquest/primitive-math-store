#!/usr/bin/env python3
"""
Type-driven composition finder + null model.

Consumes annotations.json (produced by the I/O-type annotation workflow):
  [{name, domain, inputs:[type], outputs:[type]}, ...]

Builds the REAL composition graph: edge A->B iff A's output type feeds B's input
type. Then:
  - reports composition-edge density (vs the 0.01% the text-based detector found),
  - self-checks whether a few "hub" types make everything trivially compose,
  - finds long, cross-domain composition PIPELINES (real A->B->C chains),
  - runs a null model: do random recipes form composition chains, or only the
    deliberately-found pipelines?

Std-lib only.
"""
from __future__ import annotations
import json
import os
import random
import statistics
from collections import Counter, defaultdict

random.seed(7)
HERE = os.path.dirname(os.path.abspath(__file__))
ANNO = os.path.join(HERE, "annotations.json")


def load():
    raw = json.load(open(ANNO, encoding="utf-8"))
    prim = {}
    for a in raw:
        n = a["name"]
        if n not in prim:
            prim[n] = {"domain": a["domain"], "in": set(a["inputs"]), "out": set(a["outputs"])}
        else:
            prim[n]["in"] |= set(a["inputs"])
            prim[n]["out"] |= set(a["outputs"])
    return prim


def build_edges(prim):
    adj = defaultdict(list)
    edges = xdom = 0
    names = list(prim)
    for a in names:
        oa = prim[a]["out"]
        if not oa:
            continue
        for b in names:
            if a == b:
                continue
            shared = oa & prim[b]["in"]
            if shared:
                adj[a].append((b, sorted(shared)[0]))
                edges += 1
                if prim[a]["domain"] != prim[b]["domain"]:
                    xdom += 1
    return adj, edges, xdom


def longest_chain_in_subset(nodes, adj):
    """Longest simple type-compatible path using only `nodes` (<=6 -> brute DFS)."""
    nodeset = set(nodes)
    best = 1
    succ = {n: [b for (b, _t) in adj.get(n, []) if b in nodeset] for n in nodes}

    def dfs(n, seen):
        nonlocal best
        best = max(best, len(seen))
        for b in succ[n]:
            if b not in seen:
                dfs(b, seen | {b})

    for n in nodes:
        dfs(n, {n})
    return best


def find_pipelines(prim, adj, trials=40000, max_len=6):
    """Random-restart greedy: extend preferring neighbors that add a NEW domain."""
    names = list(prim)
    found = {}
    for _ in range(trials):
        start = random.choice(names)
        path = [start]
        doms = {prim[start]["domain"]}
        types = []
        while len(path) < max_len:
            nbrs = [(b, t) for (b, t) in adj.get(path[-1], []) if b not in path]
            if not nbrs:
                break
            fresh = [(b, t) for (b, t) in nbrs if prim[b]["domain"] not in doms]
            b, t = random.choice(fresh) if fresh else random.choice(nbrs)
            path.append(b)
            doms.add(prim[b]["domain"])
            types.append(t)
        if len(path) >= 4:
            key = tuple(sorted(path))
            score = (len(doms), len(path))
            if key not in found or score > found[key][0]:
                found[key] = (score, path, types, len(doms))
    ranked = sorted(found.values(), key=lambda x: x[0], reverse=True)
    return ranked


def main():
    prim = load()
    N = len(prim)
    doms = Counter(p["domain"] for p in prim.values())
    print(f"Annotated primitives: {N} across {len(doms)} domains")
    print(f"  per domain: {dict(doms)}")
    adj, edges, xdom = build_edges(prim)
    pairs = N * (N - 1)
    print()
    print("=" * 70)
    print("COMPOSITION GRAPH  (edge A->B iff A.output type feeds B.input type)")
    print("=" * 70)
    print(f"directed type-compatible edges: {edges} of {pairs} ordered pairs "
          f"({100*edges/pairs:.1f}%)")
    print(f"  cross-domain edges: {xdom} ({100*xdom/max(edges,1):.0f}% of edges)")
    print(f"  vs text-based detector earlier: 0.01% -> composition is now FINDABLE.")
    print()

    # self-check: do a few hub types make everything compose?
    in_hub = Counter(t for p in prim.values() for t in p["in"])
    out_hub = Counter(t for p in prim.values() for t in p["out"])
    print("type hub-check (if 1-2 types dominate, the vocabulary is too coarse):")
    print(f"  most common INPUT types:  {in_hub.most_common(5)}")
    print(f"  most common OUTPUT types: {out_hub.most_common(5)}")
    print()

    # null model: random 6-recipes -- do they chain?
    print("=" * 70)
    print("NULL MODEL  longest composition chain inside a recipe")
    print("=" * 70)
    rnd = [longest_chain_in_subset(random.sample(list(prim), 6), adj) for _ in range(5000)]
    print(f"random 6-primitive recipe: mean longest chain = {statistics.mean(rnd):.2f}, "
          f"max = {max(rnd)}  (chain of 1 = nothing composes)")
    dist = Counter(rnd)
    print(f"  chain-length distribution: {dict(sorted(dist.items()))}")
    print()

    # the real pipelines
    print("=" * 70)
    print("TOP CROSS-DOMAIN COMPOSITION PIPELINES (type-flow, not resemblance)")
    print("=" * 70)
    pipes = find_pipelines(prim, adj)
    shown = 0
    for score, path, types, ndoms in pipes:
        if shown >= 10:
            break
        if ndoms < 3:
            continue
        flow = path[0]
        for nm, t in zip(path[1:], types):
            flow += f" --[{t}]--> {nm}"
        chips = " | ".join(f"{nm}({prim[nm]['domain'][:4]})" for nm in path)
        print(f"\n[{len(path)} steps, {ndoms} domains]")
        print(f"  {flow}")
        print(f"  domains: {chips}")
        shown += 1
    if shown == 0:
        print("No >=3-domain pipelines found (graph too sparse or too clustered).")


if __name__ == "__main__":
    main()
