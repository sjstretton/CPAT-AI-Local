# Table 2 of EgyptResultsInitial.docx vs the rebuilt ad hoc calculations vs the final prototype — what differs and why (2030), v0.4

**Sources.**

- (i) Table 2 and the narrative of `EgyptResultsInitial.docx`.
- (ii) Rebuild v0.4: `AdHocCalculations_Rebuild_v0.4.xlsx`, `Mode` = REBUILD, `Conv` = FULL, `ThetaOther` = 1, `EFSet` = EGY_EF_V01, `KappaMode` = SCALE, `Yr` = 2030 (see `MethodologyNote_v0.4.md`).
- (iii) Prototype kernel: `CPAT_Industry_Kernel_Egypt_v1.5.xlsx`, sheet `Table2_Industry` (stored 2030 snapshot, kernel composition), with `Manual inputs` at default and the CBAM convention FULL. NOPHASE values of O are obtained by switching `Manual inputs` E76.

This note compares the rebuild with the prototype's own composition. It is not the final Table 2: the final Table 2 is the CBAM carve-out (`EGYPT_CarveOut_Table2_v1.5`), whose row O is the intensity-only measure (EGYPT_Methodology section 4.5).

All values are for 2030, at a carbon price of USD 20/t in every bundle.

**Settings common to both models.**

1. **P\* = USD 122 (2024 dollars).** The process response is anchored at USD 100 in 2019 dollars.
2. **EG3 scaled to full industrial coverage by 1/κ (κ = 0.537).** For 3A–3C, CPAT's industry energy CO₂ change, receipts and deaths are scaled to what a run covering all industry would give. **This is a linear approximation, not a CPAT re-run.**
3. **3C fund** (kernel): capped at revenue after abatement, solved as a fixed point; the fund equals what the block actually pays after it abates.
4. **Block fuel CO₂ above the sector total** (kernel): where the block's fuel CO₂ exceeds CPAT's sector energy CO₂ (cement 19.05 vs 10.91 Mt, chemicals 1.88 vs 0, non-ferrous metals 0.05 vs 0 in 2030), the excess comes out of non-kernel industry. Total industry CO₂ is unchanged: kernel sectors 26.5 Mt, non-kernel 48.9 Mt.

**Where the models differ by design.** The rebuild rebates all covered industry in 3B (`ThetaOther` = 1) and uses σ = 20 $/t for the 3C fund; the kernel rebates the CBAM block only (rebate capped by sector shares) and solves the 3C fund from the block's own post-abatement payments.

## 1. Side by side (2030)

**Carbon revenues raised, $bn (Table 2 col. 6; P)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | 5.8 | 5.2 | 5.2 | 1.1 | 0.0 | 0.0 |
| Rebuild v0.4, net (gross) | 6.84 | 6.23 | 6.19 | 2.34 | 0.20 (2.38; rebate 2.18) | 0 (2.30 to fund) |
| Prototype, net | 6.89 | 6.28 | 6.24 | 1.88 | 0.98 | 0.73 (gross 1.65; fund 0.93) |

**Total emissions reduction, MtCO₂e (col. 7; K)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (text) | −41.6 | −38.9 | −41.0 | −21.5 | −18.1 (13.6) | −24.5 |
| Rebuild v0.4 | −31.4 | −27.8 | −29.3 | −25.1 | −12.3 | −30.6 |
| Prototype (composition) | −29.0 | −25.5 | −26.7 | −21.1 | −17.4 | −32.9 |
| Prototype block only (emrt) | −5.9 | −1.6 | −1.6 | −5.9 | −2.3 | −16.2 |

**CBAM coverage, % (col. 8; M).** Table 2 and the original give 100 / 44.5 / 44.5 / 100 / 100 / 100. Both the rebuild and the prototype give 100 / 44.2 / 44.2 / 100 / 100 / 100.

**Emission-intensity reduction, CBAM sectors, % (col. 9; N)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | −7.6 | −5.5 | −5.5 | −7.6 | −7.6 | −13.1 |
| Rebuild v0.4 | −5.8 | −2.2 | −2.2 | −5.8 | −5.8 | −11.2 |
| Prototype | −3.6 | 0 | 0 | −3.6 | −3.6 | −21.1 |

**CBAM obligations reduced, % per unit exported (col. 10; O)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (≈ NOPHASE) | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| Rebuild FULL (NOPHASE) | −44.4 (−24.3) | −23.1 (−12.5) | −23.1 (−12.5) | −44.4 (−24.3) | −5.4 (−5.4) | −47.4 (−28.4) |
| Prototype FULL (NOPHASE) | −42.9 (−22.3) | −21.6 (−10.5) | −21.6 (−10.5) | −42.9 (−22.3) | −2.9 (−2.9) | −51.9 (−34.6) |

These are deduction-based obligations. Row O of the final Table 2 is the intensity-only measure (−5.4 / −2.6 / −2.7 / −5.4 / −5.4 / −20.7), which is not comparable with the rows above.

**Air-pollution deaths avoided per year (col. 11; Q)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | 1,656 | 1,564 | 1,631 | 546 | 345 | 621 |
| Rebuild v0.4 | 1,564 | 1,564 | 1,631 | 850 | 412 | 997 |
| Prototype | 1,421 | 1,421 | 1,473 | 816 | 746 | 985 |

**National GHG covered, % (col. 3 text; J)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 text (original xlsb) | 72 | 65 | 65 | 20 (24.3) | 20 (24.3) | 20 (24.3) |
| Rebuild v0.4 | 63.2 | 57.3 | 57.3 | 20.8 | 20.8 | 20.8 |
| Prototype | 63.2 | 57.3 | 57.3 | 18.5 | 18.5 | 18.5 |

**Other PolicyMatrix columns, 2030** (not in Table 2; rebuild / prototype):

- **T, block emissions, %:** 1A −11.6 / −9.5; 2A −4.7 / −2.6; 2B −4.7 / −2.6; 3A −11.6 / −9.5; 3B −5.8 / −3.6; 3C −16.7 / −25.9.
- **U, block output, %:** −6.1 / −6.1 for 1A and 3A; −2.6 / −2.6 for 2A and 2B; 0 / 0 for 3B; −6.1 / −6.1 for 3C.
- **AR, Δ net revenue, $bn:** 1A 10.43 / 11.09; 2A 10.43 / 10.48; 2B 10.62 / 10.67; 3A 2.69 / 2.84; 3B 0.51 / 1.94; 3C 0.39 / 1.69.

## 2. Why K differs — decomposition, MtCO₂e

| Component | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| CPAT ΔGHG of the run (EG3 unscaled) | −38.88 | −38.88 | −41.00 | −21.54 | −21.54 | −21.54 |
| *Rebuild:* ΔGHG scaled by 1/κ, less CPAT ΔIPPU scaling | −26.92 | −26.92 | −28.44 | −20.65 | −20.65 | −20.65 |
| *Rebuild:* block process intensity ER_p (3C: σ added) | −2.13 | 0 | 0 | −2.13 | −2.28 | −4.11 |
| *Rebuild:* block process output channel | −2.30 | −0.90 | −0.90 | −2.30 | 0 | −2.30 |
| *Rebuild:* D_obr / F_fund | – | – | – | – | +10.61 | −3.56 |
| **Rebuild K** | **−31.35** | **−27.82** | **−29.34** | **−25.07** | **−12.31** | **−30.60** |
| *Prototype:* IPPU replacement (kernel ΔIPPU − CPAT ΔIPPU) | +7.43 (−4.53 + 11.96) | +10.95 | +11.56 | +3.73 (−4.53 + 8.26) | +5.99 | −4.61 (−12.87 + 8.26) |
| *Prototype:* industry-energy replacement (kernel composition − CPAT ΔInd) | +2.45 | +2.45 | +2.74 | −3.32 (−11.87 + 8.55) | −1.89 | −6.73 |
| **Prototype K** | **−29.00** | **−25.47** | **−26.71** | **−21.13** | **−17.45** | **−32.88** |

**Notes on the decomposition:**

- **For EG3 the two models present the 1/κ scaling differently.**
  - The rebuild scales CPAT's ΔGHG and ΔIPPU.
  - The prototype keeps the unscaled CPAT ΔGHG and puts the scaling in its industry replacement. Non-kernel industry falls at CPAT's full-coverage rate: dnk = −8.75 Mt instead of −4.70.
  - Both give the same economic quantity.
- **Rebuild → prototype gap:**
  - 1A–2B: about −2.4 Mt.
  - 3A: −3.9 Mt; 3B: +5.1 Mt, so the prototype is larger (the rebuild's D_obr removes the output channel for all covered industry).
  - 3C: +2.3 Mt, so the prototype is larger.
- **Sources of the gap:**
  - **(a) Process response.** It is now common to both models (kernel ΔIPPU −4.53 vs rebuild −4.43 in 1A/3A).
  - **(b) Data-vintage mix, the largest remaining cause.** The prototype's non-kernel industry is the stored CPAT industry energy CO₂ (75.4 Mt) less the kernel sectors (26.5), not the csv's 89.0. This is about 1.9 Mt at κ = 1 and about 3.5 Mt for EG3 after 1/κ.
  - **(c) Kernel-sector fuel response.** The kernel sectors respond slightly less than CPAT's industry average (−11.8 % vs −13.9 %), because the block's fuel intensity is fixed.
  - **(d) 3C fund design.** The prototype's fund equals the block's revenue after abatement and buys block process abatement at the solved shadow price, giving block −16.2 Mt and ΔIPPU −12.9. The rebuild uses σ = 20 $/t.
  - **(e) 3B rebate scope.** The rebuild rebates all covered industry (D_obr +10.6 Mt); the kernel rebates the CBAM block only, so no D_obr-type term is needed.

## 3. Why the other columns differ

- **Revenue P.**
  - **1A–2B:** the two models agree within 0.05 $bn.
  - **3A:** the rebuild gives EG3 receipts/κ + process revenue (2.34). The prototype gives price × full-coverage industry CO₂ on the stored vintage + process revenue (1.88); the gap is the vintage mix.
  - **3B:** the rebuild rebates all covered industry (2.18 $bn), so net revenue is 0.20 $bn. The prototype rebates the CBAM block only (rebate equal to block payments) and gives 0.98.
  - **3C:** the rebuild sends all industrial carbon revenue to the fund (net 0). The prototype's fund is capped at the block's own post-abatement payments (0.93 $bn), so the non-block industry revenue (0.73 $bn) stays with the budget. **This is a difference in convention.** If the 3C fund is meant to absorb all industrial carbon revenue, the prototype's P would be 0 and its fund larger.
- **Coverage J.**
  - **1A–2B:** both models give 63.2 / 57.3.
  - **3A–3C after 1/κ:** coverage is all industrial energy CO₂ plus block process emissions. The rebuild uses CPAT's 89.0 Mt (20.8 %); the prototype uses the stored 75.4 Mt (18.5 %). Table 2's 20 % is close to both.
- **Intensity N and obligations O.**
  - P\* deflation lowers the process response, so N for 1A/3A goes from −6.6 to −5.8 % (rebuild) and from −4.4 to −3.6 % (prototype).
  - The prototype is still smaller, because the block's fuel intensity is fixed: about −2.2 pp, which is all of 2A/2B.
  - O ≈ (1 + N)(1 − 20/100) − 1 under NOPHASE. FULL roughly doubles the percentage.
  - 3C in the prototype: the fund buys more process abatement (−21.1 %) than the rebuild's σ = 20 (−11.2 %).
- **Deaths Q.**
  - **EG3:** deaths are scaled by 1/κ in both models.
  - **Rebuild:** CPAT deaths/κ × the bundle's energy-CO₂ ratio.
  - **Prototype:** CPAT deaths/κ × (kernel ΔEnergy CO₂ / CPAT ΔEnergy CO₂ at full coverage).
  - 1A–2B are about 9 % lower in the prototype (the vintage mix plus the fixed block fuel intensity).
- **AR.**
  - **Rebuild:** CPAT Δnet revenue less rebates/fund, with P scaled.
  - **Prototype:** CPAT ΔRev − CPAT receipts/κ + its own P.
  - The 3C difference follows the fund convention above.

## 4. Internal inconsistencies in EgyptResultsInitial.docx (unchanged)

1. **3B reduction:** the table gives −18.1 Mt, the text 13.6 Mt.
2. **Mixed bases.** "5–17 % of Egypt's annual CO₂ of about 249 Mt" uses a CO₂-only base, while the coverage shares use total GHG (594 Mt).
3. **Obligations and intensity:** the text says "about 8 to 30 %" for obligations and "nearly 8 %" for intensity, while the table gives −7.6 %.
4. **3A revenue:** 1.1 $bn (gross block payments) vs 2.38 in the workbook cell.
5. **Coverage:** 72/65 % is typed in; the workbook's own columns imply 59/53 % and 24.3 %.

The final Table 2 and the tracked results text use the CBAM carve-out (`EGYPT_CarveOut_Table2_v1.5`): original CPAT runs, with only the CBAM block replaced.

## 5. Remaining caveats that matter for this comparison

- **EG3 1/κ scaling is linear.** A true full-coverage EG3 CPAT run would differ, for example through the fuel mix of aluminium and other manufacturing, and general-equilibrium effects. 3A–3C are best estimates, not lower bounds.
- **Data-vintage mix in the prototype composition:** about 1.9 Mt (κ = 1) and about 3.5 Mt (EG3).
- **3C fund convention:** block-only (prototype) vs all industry (rebuild).
- **CBAM convention default:** FULL in both models.
- **3B rebate scope:** rebuild = all covered industry; kernel and carve-out = CBAM block only.
- **Block fuel intensity is fixed** (N, O and T understated for fuel-priced bundles). Process β is not routed to fp.
- **Provisional parameters.** The Egypt EF v0.1 VERIFY list is open, and some β values are judgement calls: AN 50 % abatement blend, aluminium combined β, ammonia/urea β = 0. See `EGYPT_FinalCaveats_v1.1`.

## 6. Bottom line

Table 2's national figures rest on defects in the original workbook. The coherent rebuild gives 8–29 % smaller K for the economy-wide bundles and about 1 $bn more revenue. With full-coverage scaling, the industry-only bundles are no longer small: 3A −25 Mt, 3C −31 Mt, close to the economy-wide levies, although with far smaller revenue and health gains. The prototype agrees with the rebuild within about 2.4 Mt for 1A–2B and 4 Mt for 3A, and differs by 2.3 Mt (3C) and 5.1 Mt (3B), the latter because of the rebate scope. The remaining gaps are explained by the data-vintage mix, the fixed block fuel intensity and the fund convention.
