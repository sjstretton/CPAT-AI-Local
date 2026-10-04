# Table 2 of EgyptResultsInitial.docx, the final Table 2, the rebuilt ad hoc calculations and the prototype: what differs and why (2030), v0.5

**Sources.**

- (i) Table 2 and the narrative of `EgyptResultsInitial.docx`.
- (ii) The final Table 2: CBAM carve-out (`EGYPT_CarveOut_Table2_v1.6`; kernel sheets `CarveOut_Table2`, `Table2_Final`).
- (iii) Rebuild v0.5: `AdHocCalculations_Rebuild_v0.5.xlsx`, `Mode` = REBUILD, `Conv` = FULL, `ThetaOther` = 1, `KappaMode` = SCALE (see `MethodologyNote_v0.5.md`).
- (iv) Prototype: kernel `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`, sheet `Table2_Industry` (stored 2030 snapshot, kernel composition).

All values are for 2030 at USD 20/t. The rebuild and the prototype scale EG3 to full industrial coverage (a linear approximation); the final Table 2 uses EG3 as run. All three models use output elasticities by product (cement −0.10, steel and fertilisers −0.40, aluminium −0.50; the rebuild's PROTOTYPE mode keeps −0.5).

## 1. Side by side (2030)

**Total emissions reduction, MtCO₂e (K)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (initial) | −41.6 | −38.9 | −41.0 | −21.5 | −18.1 | −24.5 |
| Final Table 2 | −34.7 | −31.9 | −33.7 | −20.0 | −12.0 | −30.8 |
| Rebuild v0.5 | −29.7 | −27.1 | −28.6 | −23.4 | −12.3 | −29.0 |
| Prototype | −27.3 | −24.7 | −26.0 | −19.4 | −17.4 | −31.6 |

**Carbon revenue, $bn (P)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (initial) | 5.8 | 5.2 | 5.2 | 1.1 | 0.0 | 0.0 |
| Final Table 2 | 6.9 | 6.3 | 6.2 | 1.6 | 0.3 | 0.4 |
| Rebuild v0.5 | 6.9 | 6.2 | 6.2 | 2.4 | 0.2 | 0.0 |
| Prototype | 6.9 | 6.3 | 6.2 | 1.9 | 1.0 | 0.7 |

**Air-pollution deaths avoided per year (Q)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (initial) | 1,656 | 1,564 | 1,631 | 546 | 345 | 621 |
| Final Table 2 | 1,440 | 1,431 | 1,492 | 509 | 330 | 606 |
| Rebuild v0.5 | 1,564 | 1,564 | 1,631 | 850 | 412 | 997 |
| Prototype | 1,420 | 1,420 | 1,472 | 816 | 746 | 984 |

**CBAM-sector emission intensity change, % (N)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (initial) | −7.6 | −5.5 | −5.5 | −7.6 | −7.6 | −13.1 |
| Final Table 2 | −5.8 | −2.1 | −2.3 | −5.8 | −5.8 | −23.1 |
| Rebuild v0.5 | −5.8 | −2.1 | −2.1 | −5.8 | −5.8 | −11.2 |
| Prototype | −3.6 | 0.0 | 0.0 | −3.6 | −3.6 | −21.1 |

**National GHG covered, % (J)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (initial) | 72 | 65 | 65 | 20 | 20 | 20 |
| Final Table 2 | 63 | 57 | 57 | 14 | 14 | 14 |
| Rebuild v0.5 | 63.2 | 57.3 | 57.3 | 20.8 | 20.8 | 20.8 |
| Prototype | 63.2 | 57.3 | 57.3 | 18.5 | 18.5 | 18.5 |

**CBAM obligations, % per unit exported (O).** The final Table 2 reports the intensity-only measure (−5.4 / −2.6 / −2.7 / −5.4 / −5.4 / −20.7). The rebuild and the prototype report the deduction-based obligation; it is not comparable with the final row O.

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (initial, ≈ NOPHASE) | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| Rebuild FULL (NOPHASE) | −44.4 (−24.3) | −23.1 (−12.5) | −23.1 (−12.5) | −44.4 (−24.3) | −5.4 (−5.4) | −47.4 (−28.4) |
| Prototype FULL | −42.9 | −21.6 | −21.6 | −42.9 | −2.9 | −51.9 |

**Other PolicyMatrix columns** (rebuild; not in Table 2): T block emissions, % 1A −7.2, 2A −2.8, 2B −2.8, 3A −7.2, 3B −5.8, 3C −12.6. U block output, % 1A −1.5, 2A −0.7, 2B −0.7, 3A −1.5, 3B 0.0, 3C −1.5. AR change in net revenue, $bn 1A 10.43, 2A 10.43, 2B 10.62, 3A 2.69, 3B 0.51, 3C 0.36.

## 2. Why the models differ

- **Scope of the national response.** The final Table 2 keeps CPAT's own response everywhere except the CBAM block and uses EG3 as run, so 3A–3C are lower bounds (coverage 14%). The rebuild and the prototype scale EG3's industry response by 1/κ (κ = 0.537), which raises coverage to 18.5–20.8% and the 3A–3C reductions.
- **IPPU.** The final Table 2 keeps CPAT's proportional IPPU response for non-CBAM IPPU. The rebuild removes CPAT's IPPU scaling altogether (`IppuOther` = NONE); the prototype replaces it by the kernel's IPPU. This is the main reason the rebuild's 1A–2B cuts (−27 to −30 Mt) are smaller than the final Table 2's.
- **3B rebate scope.** The rebuild and the final Table 2 rebate all covered industry; the prototype rebates the CBAM block only, so its 3B cut is larger and its revenue higher.
- **3C fund.** The rebuild sends all industrial carbon revenue to the fund at a fixed USD 20/t shadow price (net revenue 0). The prototype's fund equals the block's own payments after abatement, solved as a fixed point, and the final Table 2 takes the prototype's fund.
- **Data vintage.** The prototype combines changes from two CPAT data vintages (industry energy CO₂ 75.4 Mt stored against 89.0 Mt in the new Egypt runs); this lowers its coverage and revenue for 3A–3C.
- **Fixed block fuel intensity in the prototype.** Its CBAM intensity change for 2A/2B is 0 (rebuild and final Table 2 about −2%).
- **Obligations.** The rebuild and the prototype compute a deduction-based obligation (FULL: 2030 phase-in, CBAM factor 0.485; NOPHASE: factor 1). The final Table 2 reports the CBAM-product intensity change only.

## 3. Internal inconsistencies in EgyptResultsInitial.docx

1. **3B reduction:** the table gives −18.1 Mt, the text 13.6 Mt.
2. **Mixed bases.** "5–17% of Egypt's annual CO₂ of about 249 Mt" uses a CO₂-only base, while the coverage shares use total GHG (594 Mt).
3. **Obligations and intensity:** the text says "about 8 to 30%" for obligations and "nearly 8%" for intensity, while the table gives −7.6%.
4. **3A revenue:** 1.1 $bn (gross block payments) against 2.38 in the workbook cell.
5. **Coverage:** 72/65% is typed in; the workbook's own columns imply 59/53% and 24.3%.

## 4. Caveats that matter for this comparison

- The 1/κ scaling is linear; a full-coverage EG3 CPAT run would differ (fuel mix of aluminium and other manufacturing, general-equilibrium effects).
- The 3C fund convention and the 3B rebate scope differ between the models (section 2).
- Block fuel intensity is fixed in the prototype; process β is not routed to fp.
- Provisional parameters: the Egypt EF v0.1 VERIFY list is open; AN 50% abatement blend; aluminium combined β; ammonia/urea β = 0; output elasticities are judgements (Low–Medium confidence). See `EGYPT_FinalCaveats_v1.6`.
