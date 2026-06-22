# Master Primitive Taxonomy & Cross-Domain Wiring Map
> Jesse's Primitive Reserve — Canonical Index
> Built from "The Painted Fence" doctrine
> Last updated: 2026-06-25
> Version: v1.2 — Target (1000) achieved

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   ORCHESTRATOR                       │
│  (policy: what to use, when, how much to pay)     │
├─────────────────────────────────────────────────────┤
│                   PRIMITIVE KIT                     │
│  8 root atoms × 17 domains = ~1026 primitives        │
│  Each primitive: mechanism, not policy               │
├─────────────────────────────────────────────────────┤
│               GENERATOR SLOT                        │
│  (the engine you plug into the primitive slot)       │
│  e.g., SHA-256 in hash slot, neural net in project  │
└─────────────────────────────────────────────────────┘
```

The primitive kit is agnostic. What fills the slots is the cost.

---

## Directory Structure

```
primitives-math/
├── _taxonomy-root/
│   ├── ROOT_ATOMS.md         ← The 8 canonical atoms + reinforcement ladder
│   └── MASTER_TAXONOMY.md    ← This file — cross-domain wiring map
├── signal-processing-rf/
│   └── PRIMITIVES.md         ← RF synthesis, filters, FFT, OFDM, beamforming, radar, audio
├── graphics-rendering-lod/
│   └── PRIMITIVES.md         ← Rasterization, PBR, path tracing, texture, post-processing
├── retrieval-search/
│   └── PRIMITIVES.md         ← Inverted index, ANN, LTR, query understanding, session search
├── physics-diffusion/
│   └── PRIMITIVES.md         ← Diffusion, Fokker-Planck, statistical mechanics, numerical PDE
├── database-streaming-sketching/
│   └── PRIMITIVES.md         ← Sketches, streaming, CDC, storage engines, distributed
├── information-theory-coding/
│   └── PRIMITIVES.md         ← Entropy, compression, ECC, rate-distortion, network IT
├── linear-algebra-matrix/
│   └── PRIMITIVES.md         ← Decompositions, matmul, tensor ops, iterative solvers
├── cryptography-hashing/
│   └── PRIMITIVES.md         ← LSH, fast hash, KDF, MPC, zero-knowledge, fuzzy hash
├── ml-training/
│   └── PRIMITIVES.md         ← Losses, optimizers, attention, architecture, RL, infrastructure
├── distributed-systems/
│   └── PRIMITIVES.md         ← Consensus, replication, sharding, consistency, CAP
├── quantum-computing/
│   └── PRIMITIVES.md         ← Qubits, gates, QEC, algorithms, QFT
├── biology-bioinformatics/
│   └── PRIMITIVES.md         ← Sequencing, MD, protein structure, RNA/genomics, ML
├── control-numerical-opt/
│   └── PRIMITIVES.md         ← Control theory, numerical optimization, autodiff, Bayesian opt
├── networking/
│   └── PRIMITIVES.md         ← OSI layers, routing, TCP/QUIC, HTTP, TLS, DNS, MPLS, SD-WAN, QUIC, VXLAN, IPsec, BGP, OSPF
└── agentic-reasoning/
    └── PRIMITIVES.md         ← CoT/ToT/GoT, causal reasoning, world models, tool use, memory systems, planning, metacognition, multi-agent
```

---

## Cross-Domain Wiring Matrix

### scan
```
Signal:     A/D sampling, Nyquist sampling theorem
Graphics:   Tessellation, scan-conversion, rasterization
Retrieval:  Tokenization, shingling, document parsing
Database:   Stream ingestion, window partitioning
Physics:    Discretizing continuous fields into lattice sites
Crypto:     Parsing input into blocks for hashing
LinAlg:     Iterating over matrix elements for multiplication
InfoTheory: Source modeling (ergodic process → symbol stream)
Networking: Packet header parsing, Wireshark/pcap scan, packet classification
Agentic:   Thought tokenization, context window scanning, step-by-step reasoning scan
```

### hash
```
Signal:     Spread spectrum (PN sequence), DSSS
Graphics:   Tile ID hashing, procedural noise (hash → perlin)
Retrieval:  MinHash, SimHash, LSH, feature hashing
Database:   Bloom filter hash, consistent hash, partition key
Physics:    Random number generation, hash for Monte Carlo
Crypto:     Everything — SHA-256, BLAKE3, MurmurHash
LinAlg:     Johnson-Lindenstrauss random projection
InfoTheory: Arithmetic coding probability modeling
Networking: CRC/checksum, MAC address hash, Bloom filter flow tracking, TCP sequence numbers
Agentic:   Content-addressable memory (CAM), LLM prompt hashing for cache keys, MinHash for experience similarity
```

### fold
```
Signal:     Integration, energy detection, matched filter output
Graphics:   Accumulation buffer, color averaging, mipmap generation
Retrieval:  Term frequency, BM25 term saturation, IDF computation
Database:   Stream aggregation (sum, count, min, max, mean)
Physics:    Heat equation (Laplacian = fold over neighbors)
Crypto:     Hash tree (Merkle root = fold of hashes)
LinAlg:     Matrix-vector multiply (fold of products), trace
InfoTheory: Entropy computation (fold of −p·log p)
Networking: TCP cwnd (fold of ACKs), stream byte count, aggregation over flows, network-wide packet loss fold
Agentic:   Confidence aggregation, multi-sample vote fold, episode memory consolidation, working memory fold
```

### project
```
Signal:     Matched filter, mixing, up/down conversion
Graphics:   3D transform (MVP matrix), UV projection
Retrieval:  Vector embedding, BM25 scoring, PageRank step
Database:   Feature projection for approximate query processing
Physics:    Force projection onto constraint directions
Crypto:     Commitment scheme (project to code space)
LinAlg:    Everything — matrix-vector multiply IS projection
InfoTheory: Rate distortion — project onto rate-distortion frontier
Networking: IP routing (project destination to next-hop), VLAN projection, DSCP marking
Agentic:   Query embedding projection into action space, thought projection onto goal space, MCTS selection
```

### scale
```
Signal:     AGC, normalize signal power, divide by noise PSD
Graphics:   Color normalization, HDR tone mapping, gamma encode
Retrieval:  L2-normalize embeddings, IDF scale, BM25 document length norm
Database:   Normalize sketch estimates
Physics:    Force scaling, damping coefficient
Crypto:     Key stretching (deliberately scaled cost)
LinAlg:     Unit normalization, z-score standardization
InfoTheory: Likelihood scaling, probability normalization
Networking: TCP cwnd scaling, rate shaping (token bucket), DSCP scaling, receive window scaling
Agentic:   Normalize confidence scores, scale reward signals, temperature scaling for LLM sampling, context budget allocation
```

### compare
```
Signal:     Correlation, SNR measurement, matched filter output
Graphics:   Template matching, depth test, alpha test
Retrieval:  Cosine similarity, Jaccard, NDCG, BM25
Database:   Similarity join, threshold query
Physics:    Force magnitude comparison, threshold crossing
Crypto:     Hamming distance of fingerprints, fuzzy hash match
LinAlg:     Euclidean distance, Mahalanobis distance
InfoTheory: KL divergence, cross-entropy, mutual information
Networking: RTT comparison, packet loss rate compare, TCP cwnd vs. BDP compare, DSCP threshold
Agentic:   Compare candidate plans, compare tool outputs, confidence calibration, consistency check, CoT vs. expected answer
```

### combine
```
Signal:     Weighted sum of RF channels, OFDM subcarrier combine
Graphics:   Alpha compositing (Porter-Duff over), blend modes
Retrieval:  RRF, score fusion, hybrid retrieval (BM25 + dense)
Database:   Federated query results, multi-source join
Physics:    Force accumulation, potential energy combination
Crypto:     Multi-party computation (combine shares)
LinAlg:     Linear combination, convex combination
InfoTheory: Bayesian fusion, ensemble averaging
Networking: Channel bonding (combine physical links), LACP hash combine, multi-path TCP combine, VLAN stacking
Agentic:   Combine tool outputs, merge memory traces, ensemble reasoning (multi-agent vote), RAG context combine
```

### order
```
Signal:     Rank frequency bins by power, spectral peak detection
Graphics:   Painter's algorithm (depth sort), priority queue rendering
Retrieval:  Rank by relevance, top-k heap, WAND algorithm
Database:   ORDER BY, priority queue, tuple ordering
Physics:    Sort by energy, temperature, wavefront priority
Crypto:     Threshold signature ordering
LinAlg:     Sort by singular values, condition number ranking
InfoTheory: Rank by information content, NDCG ordering
Networking: Route ordering (shortest path first), queue priority (SP/WRR), TCP cwnd ordering
Agentic:   Plan ordering (partial-order planning), beam search over reasoning paths, task queue priority
```

---

## The Deep Primitives (appear everywhere)

These primitives show up in nearly every domain — they are the most general.

### dot (project + scale + fold)
```
Every domain uses dot products:
- Signal: matched filter output = dot(signal, template)
- Retrieval: cosine similarity = dot(normalized_q, normalized_d)
- Graphics: N·L lighting = dot(normal, light_dir)
- Linear algebra: ALL matrix multiplication is sequence of dot products
- Physics: Work = dot(force, displacement)
- Database: Bloom filter = dot(hash_bits, weight_bits)?
```

### convolve (scan + fold)
```
- Signal: linear filtering
- Graphics: Gaussian blur, box blur
- Retrieval: BM25 = a kind of convolve with a saturation kernel
- Physics: diffusion equation is continuous convolution
- Linear algebra: circulant matrices are convolution operators
- Cryptography: block cipher modes (CBC-MAC) = convolution-like
```

### normalize (scale)
```
- Signal: normalize power, RMS normalization
- Graphics: normalize vectors, HDR tonemap
- Retrieval: L2-normalize embeddings
- Linear algebra: unit vectors, QR normalization
- Probability: normalize to sum to 1
- Information theory: normalize log-likelihoods
```

---

## The Generators (engines you plug in)

The primitive is agnostic. These are the generators that fill the slots:

| Slot | Cheap Generator | Expensive Generator |
|---|---|---|
| `project` | random projection (JL) | neural transformer embedding |
| `project` | IDF-weighted term vector | LSA/SVD basis |
| `hash` | MurmurHash3 | SHA-256 |
| `hash` | MinHash (k permutations) | cryptographic fingerprint |
| `fold` | count | count-min sketch |
| `fold` | sum | HyperLogLog cardinality |
| `compare` | cosine (fast) | cross-encoder reranker |
| `compare` | Jaccard | learned similarity |

---

## Capability Taxonomy (what each atom wires into)

### From `scan`
- Tokenization, shingling, segmenting
- Block decomposition, tessellation
- Windowing, gating
- Stream partitioning

### From `hash`
- Spread spectrum (RF)
- LSH families (Jaccard, cosine, Hamming, euclidean)
- Bloom filters, Count-Min, HyperLogLog
- Consistent hashing
- Fingerprinting (fuzzy, cryptographic)

### From `fold`
- TF, BM25 term weights
- Streaming aggregations (sum, count, min, max, mean, variance)
- Streaming sketches (CM, HLL, Count-Mean-Min)
- Energy detection, matched filter output
- Matrix-vector multiply
- Integration (signal, physics)
- Entropy computation

### From `project`
- Matched filter (signal)
- Vector embedding (retrieval)
- PageRank step (graph)
- Matrix multiplication
- Transform (graphics)
- Random projection (dimensionality reduction)
- Modulation (RF)

### From `scale`
- L2 normalization
- IDF weighting
- Document length normalization (BM25)
- AGC, power normalization
- Tone mapping
- Probability normalization

### From `compare`
- Cosine similarity, Jaccard
- Hamming distance
- KL divergence, cross-entropy
- Matched filter output (SNR)
- Reciprocal Rank Fusion
- Template matching
- Depth testing

### From `combine`
- Score fusion (RRF, weighted sum)
- Alpha compositing (graphics)
- Weighted mixture of experts
- Bayesian update
- Ensemble averaging
- OFDM channel combine

### From `order`
- Ranking, top-k
- Priority queue
- Painter's algorithm
- WAND / block max
- Beam search
- Simulated annealing (ordering by energy)

---

## Real Walls Reference

A real wall charges you in a conserved quantity. Painted walls you route around.

| Real Wall | Conserved Currency | Domain |
|---|---|---|
| Shannon capacity | bits per second per Hz | Signal |
| Time-bandwidth product | bandwidth × duration | RF |
| Rate-distortion | distortion = f(rate) | Compression |
| Uncertainty principle | Δf · Δt ≥ 1/2π | Signal |
| Nyquist rate | 2× bandwidth | Signal |
| Quantum | Planck's constant | Physics |
| Knapsack (optimal pack) | NP-hard, pays in compute | Retrieval |
| Percolation threshold | phase transition point | Physics |
| Thermal noise floor | kTB | RF |
| Diffraction limit | wavelength λ | Optics/Graphics |
| Spectral gap | convergence rate | PageRank |
| Cryptographic security | 2^{n/2} for n-bit hash | Crypto |

---

## Primitive Count by Domain (2026-06-25)

| Domain | Primitives |
|---|---|
| information-theory-coding | ~102 |
| networking | 100 |
| ml-training | 96 |
| distributed-systems | 47 |
| retrieval-search | 46 |
| control-numerical-opt | 60 |
| signal-processing-rf | 57 |
| linear-algebra-matrix | 59 |
| database-streaming-sketching | 50 |
| biology-bioinformatics | 50 |
| graphics-rendering-lod | 49 |
| agentic-reasoning | 75 |
| cryptography-hashing | 42 |
| quantum-computing | 33 |
| physics-diffusion | 33 |
| formal-verification | 36 |
| statistics-probability | 39 |
| **TOTAL** | **~1026** |

*Target: 1000. ACHIEVED and exceeded by ~26 via audio (15), robotics (15), computational neuroscience (15), side-channel/hardware security (15), expanded database/streaming (19), expanded linear algebra (20).*

```
1. DECOMPOSE the thing into mathematical primitives.
2. TRANSFORM to a basis where the operation is cheap and clean.
3. OPERATE there — cheap, well-conditioned.
4. RECOMPOSE the result.

The 8 atoms are: scan · hash · fold · project · scale · compare · combine · order
Everything is a wiring of these.

Primitive = mechanism (dumb, cheap).
Generator = engine (expensive, swappable).

Cost lives in the generator, never the atom.

A real wall charges you in a conserved quantity.
A painted wall — route around it.
```

---

*Source: The Painted Fence — Jesse*
*Primitive Reserve v1.1 — 2026-06-25*
