# Table 2 of EgyptResultsInitial.docx vs the rebuilt ad hoc calculations vs the final prototype — what differs and why (2030), v0.2

**Sources.** (i) Table 2 and narrative of `EgyptResultsInitial.docx` (typed values; 2030 cells of `AdHocCalculations.xlsb` where they differ). (ii) Rebuild v0.2: `AdHocCalculations_Rebuild_v0.2.xlsx`, `Mode` = REBUILD, `Conv` = NOPHASE, `EFSet` = EGY_EF_V01, `Yr` = 2030 (PolicyMatrix rows 7–12; `MethodologyNote_v0.2.md`). (iii) Final prototype: `CPAT_Industry_Kernel_Egypt_v0.15.xlsx`, sheet `Table2_Industry` (stored 2030 snapshot = live), `Manual inputs` at default (Egypt CBAM EF v0.1, Task D IPCC β, output response ON, `IppuOther` = NONE, CBAM convention FULL; NOPHASE values of O obtained by switching E76). All values 2030, carbon price 20 $/t in every bundle.

**What changed vs v0.1 of this note.** Both models now use the same emission factors (Egypt CBAM EF v0.1; block baseline 62.42 Mt in 2030) and the same IPCC process semi-elasticities (Task D). The prototype's placeholder β (≈ ¼ of the IPCC set) is gone, and a formula bug in its non-CO₂ process rows is fixed. The prototype–rebuild gap therefore no longer reflects β; it reflects scope (four kernel sectors vs all industry), the fixed block fuel intensity, the data-vintage mix and the fund design.

**Scope.** Table 2 and the rebuild are national (CPAT runs EG1 = 1A/2A, EG2 = 2B, EG3 = 3A–3C, plus the CBAM block). The prototype's national columns (J, K, P, Q) are a composition: CPAT deltas of the same runs with the industry/IPPU part replaced by the kernel's own response. For industry-only bundles only the four kernel sectors (16.4 Mt energy CO₂) are priced, not all industry (89 Mt in the CPAT run).

## 1. Side by side (2030)

**Carbon revenues raised, $bn (Table 2 col. 6; P)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | 5.8 | 5.2 | 5.2 | 1.1 | 0.0 | 0.0 |
| Original xlsb 2030 cell | 5.77 | 5.18 | 5.18 | 2.38 | 0 | 0 |
| Rebuild v0.2, net (gross) | 6.83 | 6.23 | 6.19 | 1.53 | 0.32 (1.57; rebate 1.25) | 0 (1.48 to fund) |
| Prototype v0.15, net | 6.87 | 6.27 | 6.24 | 0.89 | −0.02 | −0.47 |

**Total emissions reduction, MtCO₂e (col. 7; K)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (text) | −41.6 | −38.9 | −41.0 | −21.5 | −18.1 (13.6) | −24.5 |
| Rebuild v0.2 | −31.8 | −27.8 | −29.3 | −18.2 | −12.7 | −22.6 |
| Prototype v0.15 (composition) | −29.8 | −25.8 | −27.1 | −11.8 | −8.6 | −23.9 |
| Prototype block only (emrt) | −6.4 | −1.6 | −1.6 | −6.4 | −2.8 | −18.3 |
| *memo:* rebuild v0.1 / prototype v0.14 | −31.6 / −27.7 | −27.7 / −25.7 | −29.3 / −27.0 | −18.0 / −9.7 | −12.8 / −6.6 | −22.4 / −17.3 |

**CBAM coverage, % of CBAM-sector emissions (col. 8; M)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 / original | 100 | 44.5 | 44.5 | 100 | 100 | 100 |
| Rebuild v0.2 = prototype v0.15 | 100 | 44.2 | 44.2 | 100 | 100 | 100 |

(Fuel share of block emissions when only fuels are priced; moves from 44.5 to 44.2 with the Egypt EFs.)

**Emission-intensity reduction, CBAM sectors, % (col. 9; N)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | −7.6 | −5.5 | −5.5 | −7.6 | −7.6 | −13.1 |
| Rebuild v0.2 | −6.6 | −2.2 | −2.2 | −6.6 | −6.6 | −12.7 |
| Prototype v0.15 | −4.4 | 0 | 0 | −4.4 | −4.4 | −24.8 |

**CBAM obligations reduced, % per unit exported (col. 10; O)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (≈ NOPHASE) | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| Rebuild NOPHASE (FULL) | −24.8 (−44.8) | −12.5 (−23.1) | −12.5 (−23.1) | −24.8 (−44.8) | −6.0 (−6.0) | −29.3 (−48.1) |
| Prototype NOPHASE (FULL, default) | −22.8 (−43.3) | −10.5 (−21.6) | −10.5 (−21.6) | −22.8 (−43.3) | −3.5 (−3.5) | −36.9 (−53.6) |

**Air-pollution deaths avoided per year (col. 11; Q)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | 1,656 | 1,564 | 1,631 | 546 | 345 | 621 |
| Rebuild v0.2 | 1,564 | 1,564 | 1,631 | 546 | 410 | 633 |
| Prototype v0.15 | 1,441 | 1,441 | 1,497 | 278 | 239 | 366 |

**National GHG covered, % (col. 3 text; J)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 text | 72 | 65 | 65 | 20 | 20 | 20 |
| Original xlsb J | 72 | 65 | 65 | 24.3 | 24.3 | 24.3 |
| Rebuild v0.2 | 63.2 | 57.3 | 57.3 | 13.9 | 13.9 | 13.9 |
| Prototype v0.15 | 63.2 | 57.3 | 57.3 | 8.6 | 8.6 | 8.6 |

Other PolicyMatrix columns (not in Table 2), rebuild / prototype: T block emissions −12.3/−10.2, −4.7/−2.6, −4.7/−2.6, −12.3/−10.2, −6.6/−4.4, −18.0/−29.4 %; U block output −6.1/−6.1, −2.6/−2.6, −2.6/−2.6, −6.1/−6.1, 0/0, −6.1/−6.1 %; AR Δnet revenue 10.43/11.07, 10.43/10.47, 10.62/10.67, 2.69/2.65, 1.44/1.74, 1.21/1.29 $bn (original 10.62 for 1A–2B, 2.69, 0, –).

## 2. Why K differs — decomposition, MtCO₂e

| Component | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| CPAT ΔGHG of the run (common start) | −38.88 | −38.88 | −41.00 | −21.54 | −21.54 | −21.54 |
| *Table 2 / original:* extra terms | −2.74 (1A built on EG2 −41.00 − 0.62 legacy process term) | 0 | 0 | 0 | K = −13.59·(2/3)/0.5 (untraceable) | −2.94 (untraceable) |
| *Rebuild:* remove CPAT's proportional IPPU scaling | +11.96 | +11.96 | +12.56 | +8.26 | +8.26 | +8.26 |
| *Rebuild:* block process intensity ER_p (IPCC β, 20 $/t; 3C: 40 $/t) | −2.57 | 0 | 0 | −2.57 | −2.76 | −4.94 |
| *Rebuild:* block process output channel | −2.30 | −0.90 | −0.90 | −2.30 | 0 | −2.30 |
| *Rebuild:* OBR correction D_obr / fund fuel F_fund | – | – | – | – | +3.29 | −2.10 |
| **Rebuild K** | **−31.79** | **−27.82** | **−29.34** | **−18.15** | **−12.74** | **−22.62** |
| *Prototype:* IPPU replacement (kernel ΔIPPU − CPAT ΔIPPU) | +6.98 (−4.98 + 11.96) | +10.95 | +11.56 | +3.29 (−4.98 + 8.26) | +5.51 | −6.68 (−14.94 + 8.26) |
| *Prototype:* industry-energy replacement (kernel composition − CPAT ΔInd) | +2.11 | +2.11 | +2.32 | +6.49 (−2.06 + 8.55) | +7.42 | +4.35 |
| **Prototype K** | **−29.79** | **−25.82** | **−27.12** | **−11.77** | **−8.62** | **−23.87** |

- **Table 2 → rebuild (10–12 Mt less for 1A–2B, 3.4 for 3A):** CPAT scales *all* IPPU (86 Mt) with industrial fuel CO₂ (−13.9 % → −12 Mt), which a fuel price cannot do; the rebuild deletes that and adds the block's explicit process responses (ER_p via IPCC β, output channel). 1A also moves from the EG2 base to EG1. 3B: the untraceable −18.1 (text 13.6) is replaced by EG3 with the OBR correction (+3.3); 3C: σ = 20 $/t on both intensity channels instead of a −2.9 Mt constant.
- **Rebuild → prototype (now −2.0 Mt for 1A–2B, −6.4 for 3A, −4.1 for 3B, +1.2 for 3C):** with the same EFs and β, the process side is now close: kernel ΔIPPU −4.98 vs rebuild −4.87 (1A/3A). The remaining gap is (a) industry energy — for *All sectors*, +0.2 Mt from the kernel's own 4-sector response and **+1.9 Mt from the data-vintage mix** (kernel industry CO₂ 75.4 vs csv 89.0 Mt via `nk1 = indx − ek1`); for *Industry only*, everything outside the four sectors is unpriced, so CPAT EG3's −8.55 Mt shrinks to −2.06 (3A), −1.13 (3B), −4.20 (3C), which is the largest cause of the 3A/3B gap; (b) 3B: no D_obr-type correction is needed in the kernel (the rebate per unit of output sets the output channel to 0 directly); (c) 3C: the kernel's fund is solved as a shadow price that spends the whole fund on block abatement (block −18.3 Mt; ΔIPPU −14.9), versus the rebuild's σ = 20 $/t. With IPCC β this now *exceeds* the rebuild's K.

## 3. Why the other columns differ

- **Revenue P.** Table 2's 5.8/5.2 cannot be reproduced from 2030 CPAT outputs (six-fuel receipts 6.23 $bn EG1, 6.19 EG2). Rebuild and prototype agree within 0.05 $bn for 1A–2B (CPAT receipts + block process revenue ≈ 0.6 $bn). 3A: 1.1 in the text = gross block payments (xlsb cell 2.38); rebuild 1.53 = EG3 receipts (κ = 0.54 of industry priced) + process; prototype 0.89 = four sectors' fuel + process. 3B: Table 2's 0 is a convention; prototype ≈ 0 (−0.02) because the rebate ≈ block payments; rebuild 0.32 because only CBAM producers are rebated (`ThetaOther` = 0). 3C: nothing to the budget in all three; the prototype is *negative* (−0.47) because the fund is fixed at pre-abatement revenue and fully spent while post-abatement receipts fall further with the larger IPCC β.
- **Coverage J.** Typed in the original (its columns imply 59/53). Rebuild and prototype give the same 63.2/57.3 for 1A–2B. Industry bundles: Table 2's 20 % ≈ all industry energy CO₂ + block process; the EG3 run prices only 54 % of industrial fuel (rebuild 13.9 %), the kernel only its four sectors (8.6 %).
- **CBAM coverage M.** Same definition everywhere; 44.2 vs 44.5 is the Egypt EF fuel/process split.
- **Intensity N.** Table 2 from the legacy −0.549 %/$ block. Rebuild: fuel-intensity channel (−4.9 % on the fuel share = −2.2 %, the whole of 2A/2B) plus IPCC-β process response → −6.6 %. Prototype: same IPCC β on the process share (−4.4 %) but block fuel intensity is fixed (0 for 2A/2B; the missing ≈ −2.2 pp is the fuel-intensity channel). 3C: the prototype's fund buys much more process abatement (−24.8 % vs −12.7 %).
- **Obligations O.** O ≈ (1 + N)(1 − 20/100) − 1 in every source, so gaps follow N: Table 2 −26.1 ↔ −7.6; rebuild −24.8 ↔ −6.6; prototype −22.8 ↔ −4.4. FULL (CBAM factor 0.485 in 2030) roughly doubles the percentage; Table 2 is on the NOPHASE basis. 3B: the rebate cancels the deductible price, so O ≈ N (−7.6 / −6.0 / −3.5).
- **Deaths Q.** 1A: the original scaled EG2's 1,631 by K7/K9 → 1,656; on EG1 it equals 2A (1,564). 3B: 345 typed/stale; rebuild 410 after D_obr. Prototype = CPAT deaths × kernel/CPAT energy-CO₂ change: ×0.92 for All sectors, ×0.51 for 3A (only four sectors' fuel responds), 239 (3B), 366 (3C).
- **AR.** Original 10.62 (EG2) for all of 1A–2B; rebuild = CPAT Δnet revenue of the run less rebates/fund; prototype = CPAT Δnet revenue − CPAT receipts + its own P.

## 4. Internal inconsistencies in EgyptResultsInitial.docx (unchanged)

1. 3B reduction: table −18.1 Mt, text 13.6 Mt.
2. "5–17 % of Egypt's annual CO₂ of about 249 Mt" uses a CO₂-only base, while coverage shares (72/65/20 %) use total GHG (594 Mt incl. LULUCF in 2030); on one base 1A is −7.0 % (−41.6/594), rebuild −5.3 %.
3. Obligations "about 8 to 30 %" and "the 8 % reduction (3B)" vs −7.6 % in the table; intensity "nearly 8 %" vs −7.6 %, "nearly 6 %" vs −5.5 %.
4. 3A revenue 1.1 $bn (gross block payments) vs 2.38 in the workbook cell; the "value returned to firms not counted" convention is applied to 3B/3C but not 3A.
5. Coverage 72/65 % typed; the workbook's own columns imply 59/53 % and 24.3 % (not 20 %) for 3A–3C.

The updated text (`EgyptResultsInitial_UpdatedResults_v0.2_tracked.docx`) uses the rebuild v0.2 values.

## 5. Prototype caveats that matter for this comparison

- Industry-only bundles price the four kernel sectors only (about one fifth of industrial energy CO₂); Table 2 and CPAT EG3 intend all industry (re-run EG3 with full coverage pending).
- Data-vintage mix in the K composition (+1.9 Mt in 1A/2A/2B); fund fixed at pre-abatement revenue (3C net revenue < 0); CBAM convention default FULL; no fuel-intensity channel in the block (N, O, T understated for fuel-priced bundles).
- Egypt EF v0.1 VERIFY list open; AN 50 % abatement blend, aluminium combined β, ammonia/urea β = 0 (see `CAVEATS.md` 2026-10-02 T1 + T5).

## 6. Bottom line

Table 2's national figures rest on the original workbook's defects (typed coverage, CPAT IPPU double-scaling, 1A on the wrong run, stale 3B deaths, mixed revenue concepts): the coherent rebuild gives 8–30 % smaller K and about 1 $bn more revenue for the economy-wide bundles. With common EFs and β, the final prototype now agrees with the rebuild within about 2 Mt for 1A–2B and on the process response; the remaining differences are scope (3A/3B), the fixed block fuel intensity (N, O) and the fund design (3C), all flagged above.

