#!/usr/bin/env python3
"""
Null-model + composability audit of the primitive-combination simulator's score.

Question 1 (null model): does a high recipe_score actually beat a RANDOM recipe,
once you normalize away recipe size (score = sum over C(n,2) pairs)?

Question 2 (composability): are "recipes" real compositions (A's output/definition
actually references B) or just affinity clusters (A and B resemble each other)?

Parses the real primitive store (C:\\Projects\\primitves math\\*/PRIMITIVES.md),
reproduces the user's 6-signal compatibility score, then runs both tests.
Std-lib only.
"""
from __future__ import annotations
import glob
import os
import random
import re
import statistics
from collections import Counter

random.seed(41)
ROOT = r"C:\Projects\primitves math"

# 8 canonical root atoms + keyword proxies (the store doesn't tag atoms per
# primitive, so infer from the definition the same way for every primitive --
# the inference bias cancels in a top-vs-random comparison).
ATOM_KW = {
    "scan": ["scan", "stream", "sampl", "tokeniz", "iterat", "travers", "enumerat", "window"],
    "hash": ["hash", "fingerprint", "sketch", "minhash", "simhash", "bloom", "lsh", "random projection"],
    "fold": ["fold", "sum", "accumulat", "aggregat", "reduce", "count", "integrat", "mean", "average", "tally"],
    "project": ["project", "embed", "dot product", "matrix-vector", "transform", "mixing", "gemm", "convolv"],
    "scale": ["normaliz", "rescale", "scale", "clip", "whiten", "standardiz"],
    "compare": ["compar", "similar", "distance", "cosine", "correlat", "match", "diverg", "metric", "d-separation"],
    "combine": ["combine", "fuse", "fusion", "merge", "weighted sum", "superpos", "concat", "mix "],
    "order": ["order", "sort", "rank", "top-k", "priority", "heap", "median", "select"],
}

# coarse super-categories for the +2 "same category" signal
SUPERCAT = {
    "combinatorial-optimization": "optimization", "control-numerical-opt": "optimization",
    "linear-algebra-matrix": "optimization",
    "causal-inference": "causal", "statistics-probability": "causal",
    "agentic-reasoning": "reasoning", "logic-reasoning": "reasoning",
    "decision-logic": "reasoning", "cognitive-primitives": "reasoning",
    "formal-verification": "verification", "type-theory-programming-languages": "verification",
    "cryptography-advanced": "crypto", "cryptography-hashing": "crypto",
    "networking": "systems", "distributed-systems": "systems", "operating-systems": "systems",
    "database-streaming-sketching": "systems", "queueing-theory-stochastic-processes": "systems",
    "information-theory-coding": "info", "signal-processing-rf": "info", "ml-training": "info",
    "retrieval-search": "info",
    "computational-geometry": "geometry", "graphics-rendering-lod": "geometry",
    "physics-diffusion": "physics", "condensed-matter": "physics", "astrophysics-cosmology": "physics",
    "electromagnetics-antennas": "physics", "photonics-optics": "physics",
    "quantum-computing": "physics", "biology-bioinformatics": "physics",
}


def kebab(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.strip().lower()).strip("-")


def infer_atoms(text: str) -> set[str]:
    t = text.lower()
    return {atom for atom, kws in ATOM_KW.items() if any(kw in t for kw in kws)}


def field(body: str, label: str) -> str:
    # handles **Label:** , **Label**: , ** Label ** : (colon inside or outside bold)
    m = re.search(r"\*\*\s*" + label + r"\s*:?\s*\*\*\s*:?\s*(.*)", body, re.I)
    return m.group(1).strip() if m else ""


def parse_file(path: str, domain: str) -> list[dict]:
    text = "\n" + open(path, encoding="utf-8").read()
    prims = []
    for block in re.split(r"\n### ", text)[1:]:
        lines = block.splitlines()
        header = lines[0].strip()
        alias_hdr = re.search(r"cross-domain alias:\s*(.*?)\)", header, re.I)
        h = re.sub(r"^\[PRIM-\d+\]\s*", "", header)
        h = re.sub(r"^[A-Za-z]{1,4}\.\d+:\s*", "", h)
        h = re.sub(r"\(cross-domain alias:.*", "", h)
        name = kebab(h)
        if not name:
            continue
        body = "\n".join(lines[1:])
        ac = field(body, "Atom/Composite") or field(body, "Atom or composite")
        definition = field(body, "Definition")
        if not definition and not ac:  # section header, not a primitive
            continue
        aliases_raw = (
            field(body, "Cross-Domain Aliases")
            + " " + field(body, "Cross-domain wiring")
            + " " + field(body, "Cross-domain aliases")
            + " " + (alias_hdr.group(1) if alias_hdr else "")
        )
        alias_names = {kebab(t) for t in re.findall(r"[a-zA-Z][a-zA-Z0-9_\-]{2,}", aliases_raw)}
        alias_names.discard("")
        prims.append({
            "name": name,
            "domain": domain,
            "cat": SUPERCAT.get(domain, domain),
            "is_composite": "composite" in ac.lower(),
            "definition": definition.lower(),
            "aliases": alias_names,
            "atoms": infer_atoms(name.replace("-", " ") + " " + definition),
        })
    return prims


def load() -> list[dict]:
    prims, seen = [], set()
    for path in glob.glob(os.path.join(ROOT, "*", "PRIMITIVES.md")):
        domain = os.path.basename(os.path.dirname(path))
        for p in parse_file(path, domain):
            if p["name"] not in seen:
                seen.add(p["name"])
                prims.append(p)
    return prims


def uses(a: dict, b: dict) -> bool:
    """Directed composition signal: composite A actually references mechanism B.
    Only counts the full kebab name or a COMPOUND (hyphenated, >=6 char) alias,
    so generic single tokens (svd, nee, sample, rank) don't create phantom edges."""
    if not a["is_composite"]:
        return False
    d = a["definition"]
    if len(b["name"]) >= 6 and re.search(r"\b" + re.escape(b["name"]) + r"\b", d):
        return True
    return any("-" in al and len(al) >= 6 and re.search(r"\b" + re.escape(al) + r"\b", d)
               for al in b["aliases"])


def compat_breakdown(a: dict, b: dict) -> dict:
    sa = len(a["atoms"] & b["atoms"])
    ao = len(a["aliases"] & b["aliases"])
    nia = 1 if (a["name"] in b["aliases"] or b["name"] in a["aliases"]) else 0
    sc = 1 if a["cat"] == b["cat"] else 0
    cm = 1 if (uses(a, b) or uses(b, a)) else 0
    sd = 1 if a["domain"] == b["domain"] else 0
    return {
        "shared_atoms": sa * 15, "alias_overlap": ao * 8, "name_in_alias": nia * 20,
        "same_category": sc * 2, "compose_mechanism": cm * 25, "same_domain": sd * 1,
    }


def compat(a: dict, b: dict) -> int:
    shared_atoms = len(a["atoms"] & b["atoms"])
    alias_overlap = len(a["aliases"] & b["aliases"])
    name_in_alias = 1 if (a["name"] in b["aliases"] or b["name"] in a["aliases"]) else 0
    same_cat = 1 if a["cat"] == b["cat"] else 0
    comp_mech = 1 if (uses(a, b) or uses(b, a)) else 0
    same_dom = 1 if a["domain"] == b["domain"] else 0
    return (shared_atoms * 15 + alias_overlap * 8 + name_in_alias * 20
            + same_cat * 2 + comp_mech * 25 + same_dom * 1)


def recipe_score(recipe: list[dict]) -> int:
    n = len(recipe)
    return sum(compat(recipe[i], recipe[j]) for i in range(n) for j in range(i + 1, n))


def comp_edges(recipe: list[dict]) -> int:
    return sum(1 for i in range(len(recipe)) for j in range(len(recipe))
               if i != j and uses(recipe[i], recipe[j]))


def greedy_best(prims: list[dict], k: int, restarts: int = 40) -> list[dict]:
    best, best_s = None, -1
    # seed from the highest-degree primitives (most total compatibility) + randoms
    for r in range(restarts):
        start = prims[r] if r < len(prims) else random.choice(prims)
        chosen = [start]
        pool = random.sample(prims, min(400, len(prims)))  # candidate pool for speed
        while len(chosen) < k:
            cand = max(pool, key=lambda p: 0 if p in chosen else sum(compat(p, c) for c in chosen))
            if cand in chosen:
                cand = random.choice([p for p in prims if p not in chosen])
            chosen.append(cand)
        s = recipe_score(chosen)
        if s > best_s:
            best, best_s = chosen, s
    return best


def pct(v, p):
    return statistics.quantiles(v, n=100)[p - 1] if len(v) > 1 else v[0]


def main():
    prims = load()
    print(f"Parsed {len(prims)} unique primitives across "
          f"{len({p['domain'] for p in prims})} domains.")
    print(f"Composite (orchestrator) primitives: {sum(p['is_composite'] for p in prims)}")
    print()

    # --- TEST 1: does raw score just track recipe size (pair count)? ---
    print("=" * 70)
    print("TEST 1  raw score vs size  (recipe_score = sum over C(n,2) pairs)")
    print("=" * 70)
    print(f"{'size':>4} {'pairs':>6} {'rand_raw_mean':>14} {'per_pair':>9}")
    for k in (3, 4, 5, 6):
        pairs = k * (k - 1) // 2
        raws = [recipe_score(random.sample(prims, k)) for _ in range(3000)]
        m = statistics.mean(raws)
        print(f"{k:>4} {pairs:>6} {m:>14.1f} {m / pairs:>9.2f}")
    print("If per_pair is flat, the cross-version score growth was just more pairs.")
    print()

    # --- TEST 2: null model at k=6 (per-pair normalized) ---
    print("=" * 70)
    print("TEST 2  null model at 6 primitives  (per-pair = score / 15)")
    print("=" * 70)
    null6 = [recipe_score(random.sample(prims, 6)) / 15 for _ in range(10000)]
    top = greedy_best(prims, 6)
    top_pp = recipe_score(top) / 15
    rmean, rsd = statistics.mean(null6), statistics.pstdev(null6)
    z = (top_pp - rmean) / rsd if rsd else 0
    print(f"random per-pair:  mean={rmean:.2f}  sd={rsd:.2f}  "
          f"p50={pct(null6,50):.2f}  p95={pct(null6,95):.2f}  max={max(null6):.2f}")
    print(f"greedy-top per-pair: {top_pp:.2f}   (z = {z:.1f} sd above random)")
    print(f"greedy-top recipe: {[p['name'] for p in top]}")
    print()

    # --- TEST 3: composability — do high-compat recipes actually compose? ---
    print("=" * 70)
    print("TEST 3  composability: real A-uses-B edges vs affinity")
    print("=" * 70)
    total_pairs = 0
    compat_pos = 0       # pairs with compat > 0
    real_edges = 0       # ordered pairs with a real composition edge
    sample = random.sample(prims, min(600, len(prims)))
    for i in range(len(sample)):
        for j in range(i + 1, len(sample)):
            total_pairs += 1
            if compat(sample[i], sample[j]) > 0:
                compat_pos += 1
            if uses(sample[i], sample[j]):
                real_edges += 1
            if uses(sample[j], sample[i]):
                real_edges += 1
    print(f"sampled pairs: {total_pairs}")
    print(f"  with compatibility > 0:   {compat_pos} ({100*compat_pos/total_pairs:.0f}%)")
    print(f"  with a REAL compose edge: {real_edges} ({100*real_edges/total_pairs:.2f}%)")
    edges_in_top = comp_edges(top)
    print(f"greedy-top recipe (6 prims): {edges_in_top} real compose edges "
          f"of 30 ordered pairs (a real 6-chain needs >=5)")
    print()

    # --- TEST 4: what DRIVES the top score? similarity vs composition ---
    print("=" * 70)
    print("TEST 4  decompose the greedy-top score by signal (sum over 15 pairs)")
    print("=" * 70)
    totals = Counter()
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            for k, v in compat_breakdown(top[i], top[j]).items():
                totals[k] += v
    grand = sum(totals.values()) or 1
    for k, v in sorted(totals.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<20} {v:>6}  ({100*v/grand:.0f}% of score)")
    print(f"  {'TOTAL':<20} {grand:>6}")
    print()
    sim = totals["shared_atoms"] + totals["same_category"] + totals["same_domain"]
    comp = totals["compose_mechanism"]
    print(f"similarity signals (atoms+category+domain): {100*sim/grand:.0f}%   "
          f"composition signal (compose_mechanism): {100*comp/grand:.0f}%")
    print("If similarity dominates, the score finds resemblance clusters (real, but not")
    print("compositions). If compose_mechanism carries it, the bridges are real pipelines.")


if __name__ == "__main__":
    main()
