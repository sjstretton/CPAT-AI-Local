# Egypt Table 2 (2030): CPAT results with a CBAM carve-out, v0.1

**What this is.** The original CPAT runs give every result, except the CBAM block (steel, cement, fertilisers, aluminium). For the block, CPAT's implied change is taken out and kernel v0.16's product-level change is put in. 3A–3C use CPAT run EG3 exactly as run (no scaling to full industry coverage). Carbon price USD 20/t in 2030 in every bundle.

## Table 2 columns

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Coverage, % of GHG (J) | 63 | 57 | 57 | 14 | 14 | 14 |
| Revenue, $bn (P) | 6.9 | 6.3 | 6.3 | 1.6 | 0.7 | 0.4 |
| Emission cut, MtCO₂e (K) | −36.1 | −31.7 | −33.4 | −21.5 | −17.8 | −31.9 |
| Cut, % of GHG | −6.1 | −5.3 | −5.6 | −3.6 | −3.0 | −5.4 |
| CBAM coverage, % (M) | 100 | 44 | 44 | 100 | 100 | 100 |
| CBAM intensity, % (N) | −3.6 | 0.0 | 0.0 | −3.6 | −3.6 | −21.1 |
| CBAM obligations per unit, % (O, NOPHASE) | −22.3 | −10.5 | −10.5 | −22.3 | −2.9 | −34.6 |
| Deaths avoided (Q) | 1,425 | 1,378 | 1,436 | 498 | 434 | 597 |

## Comparison

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Emission cut, Mt: original Table 2 | −41.6 | −38.9 | −41.0 | −21.5 | −18.1 | −24.5 |
| Emission cut, Mt: **carve-out** | −36.1 | −31.7 | −33.4 | −21.5 | −17.8 | −31.9 |
| Emission cut, Mt: prototype v0.16 | −29.0 | −25.5 | −26.7 | −21.1 | −17.4 | −32.9 |
| Revenue, $bn: original Table 2 | 5.8 | 5.2 | 5.2 | 1.1 | 0.0 | 0.0 |
| Revenue, $bn: **carve-out** | 6.9 | 6.3 | 6.3 | 1.6 | 0.7 | 0.4 |
| Revenue, $bn: prototype v0.16 | 6.9 | 6.3 | 6.2 | 1.9 | 1.0 | 0.7 |
| Deaths avoided: original Table 2 | 1,656 | 1,564 | 1,631 | 546 | 345 | 621 |
| Deaths avoided: **carve-out** | 1,425 | 1,378 | 1,436 | 498 | 434 | 597 |
| Deaths avoided: prototype v0.16 | 1,421 | 1,421 | 1,473 | 816 | 746 | 985 |

## How K is built, MtCO₂e

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| CPAT ΔGHG of the run | −38.9 | −38.9 | −41.0 | −21.5 | −21.5 | −21.5 |
| CPAT industry change, % (applied to block) | −13.9 | −13.9 | −14.6 | −9.6 | −9.6 | −9.6 |
| Block emissions, baseline (fuel + process) | 63.1 | 63.1 | 63.1 | 63.1 | 63.1 | 63.1 |
| less: CPAT's implied block change | 8.8 | 8.8 | 9.2 | 6.1 | 6.1 | 6.1 |
| plus: kernel block change | −6.0 | −1.6 | −1.6 | −6.0 | −2.3 | −16.4 |
| **K** | −36.1 | −31.7 | −33.4 | −21.5 | −17.8 | −31.9 |

## Method notes

- **Runs.** 1A and 2A = EG1, 2B = EG2, 3A–3C = EG3 (CPAT csv, 2030).
- **IPPU.** CPAT scales all IPPU with industrial energy CO₂. The carve-out keeps that for non-CBAM IPPU (about 50 Mt, mainly F-gases and other process emissions) and replaces it only for the block. Prototype v0.16 held non-CBAM IPPU fixed, which is most of why its 1A cut was lower.
- **Growth.** Block output is rescaled so 2024–2030 growth matches CPAT sector energy CO₂: steel (irn) x0.976, cement (cem) x1.001. CPAT has no energy in mining & chemicals (mch) or non-ferrous metals (nfm) for Egypt, so fertilisers (mch) x1.157 and aluminium (nfm) x0.956 follow total CPAT industry growth.
- **Sectors.** irn = iron and steel; cem = cement (non-metallic minerals); mch = mining and chemicals (ammonia, urea, ammonium nitrate); nfm = non-ferrous metals (aluminium).
- **Revenue P.** CPAT carbon-tax receipts of the run, plus the block fuel-revenue adjustment, plus block process fees; less the 3B output-based rebate and the 3C abatement fund (kernel v0.16).
- **Deaths Q.** CPAT deaths of the run, scaled by (CPAT Δenergy CO₂ + block fuel adjustment) / CPAT Δenergy CO₂.
- **Coverage J.** 1A: all energy CO₂ plus block process; 2A/2B: energy CO₂; 3A–3C: EG3's priced industry energy (κ = 0.537 of 89.0 Mt) plus block process.
- **M, N, O** are kernel v0.16 values. The growth rescaling only reweights sectors, so they are not recomputed.
- **Why 3A–3C are low.** EG3 prices only about 54 % of industrial energy CO₂, as CPAT ran it.
