# Egypt Table 2 – ultra summary (2026-10-02)

Year 2030, carbon price $20/t, all % of CPAT 2030 baseline GHG (594.2 Mt). Full method: `EGYPT_Methodology_v1.0` (.md/.docx). Workbook: `AdHocRebuild/AdHocCalculations_Rebuild_v0.1.xlsx`.

## 1. Final results vs initial results (rebuilt / original)

| Metric | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Coverage, % GHG | 63 / 72 | 57 / 65 | 57 / 65 | 14 / 24 | 14 / 24 | 14 / 24 |
| Reduction, Mt | −31.6 / −41.6 | −27.7 / −38.9 | −29.3 / −41.0 | −18.0 / −21.5 | −12.8 / −18.1 | −22.4 / −24.5 |
| Reduction, % GHG | −5.3 / −8.5 | −4.7 / −8.0 | −4.9 / −8.4 | −3.0 / −4.4 | −2.1 / −3.7 | −3.8 / −5.0 |
| CBAM intensity, % | −6.6 / −7.6 | −2.2 / −5.5 | −2.2 / −5.5 | −6.6 / −7.6 | −6.6 / −7.6 | −12.7 / −13.1 |
| CBAM obligation/unit, % | −24.9 / −26.1 | −13.1 / −13.9 | −13.1 / −13.9 | −24.9 / −26.1 | −6.2 / −7.6 | −29.5 / −30.4 |
| Revenue, $bn | 6.81 / 5.77 | 6.23 / 5.18 | 6.19 / 5.18 | 1.51 / 2.38 | 0.33 / 0 | 0 / 0 |
| Deaths avoided | 1564 / 1656 | 1564 / 1564 | 1631 / 1631 | 546 / 546 | 412 / 345 | 633 / 621 |
| CBAM-sector output, % | −5.8 / −8.3 | −2.4 / −8.3 | −2.4 / −8.3 | −5.8 / −11.4 | 0 / −8.3 | −5.8 / −8.7 |

**Headline:** reductions fall 15–30% (economy-wide) and 10–30% (industry bundles); coverage falls 8–10 pp; revenue rises ~$1bn for economy-wide bundles and falls for 3A.

## 2. Why the numbers changed

1. **One denominator** (2030 baseline GHG); the original mixed years and three bases.
2. **IPPU double count removed:** CPAT's proportional IPPU scaling dropped; process emissions now come bottom-up from 8 CBAM products (base 61.2 Mt vs 53.6 Mt).
3. **Coverage computed, not typed;** EG3 industry run only prices 54% of industrial energy CO₂ (κ = 0.54).
4. **Scenario mapping fixed:** 1A on EG1 (was EG2); 3B from EG3 with explicit OBR correction (was hard-coded scaling).
5. **Output change per bundle** (original used 3B's −8.3% for all).
6. **Revenue** = CPAT fuel receipts + process revenue, net of rebates/fund; 3B now 0.33 $bn (only CBAM producers rebated).
7. **Deaths** from each bundle's own scenario, rescaled by energy CO₂ only.

## 3. Ad hoc rebuild vs main prototype kernel (v0.11)

`Mode = PROTOTYPE` reproduces the kernel exactly (<1e‑7). Differences in `REBUILD` mode:

| Item | Rebuild | Prototype |
|---|---|---|
| Fuel-intensity response | x_f = exp(b_f·(τ+σ)), b_f = −0.0025 | fixed |
| Process semi-elasticities | IPCC-based (Task D) → process ER ~4× larger | legacy E40:E47 |
| Fund (3C) | shadow price σ = $20/t on both intensity channels | inactive (3C = 3A) |
| National GHG, coverage, revenue, deaths | from CPAT | out of scope |
| CBAM obligation convention | NOPHASE default (FULL shown) | FULL |

Effect: intensity change (e.g. 1A −6.6% vs −1.1%) and CBAM-sector emissions change (−12.0% vs −6.8%) are larger; output change identical. Kernel v0.14 Table 2 (before T1/T3) gives K = −27.7/−25.7/−27.1/−9.7/−6.6/−17.3 Mt.

## 4. Methodology document

Complete: `EGYPT_Methodology_v1.0.md/.docx` (App. A emission factors, App. B process semi-elasticities). Rebuild-specific note: `AdHocRebuild/MethodologyNote_v0.1`.

## 5. Open flags

- Re-run EG3 with full industry coverage (κ → 1); will raise 3A–3C coverage/reductions.
- Apply new EFs (T5) and IPCC semi-elasticities (T1) in the kernel, then re-run Task M.
- 3B revenue sensitive to who is rebated (0.33 vs ≈0 $bn).
- β set and σ = $20/t are judgements.
