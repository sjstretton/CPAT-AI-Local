# Table 2 of EgyptResultsInitial.docx vs the rebuilt ad hoc calculations vs the merged prototype — what differs and why (2030)

**Sources.** (i) Table 2 and narrative of `EgyptResultsInitial.docx` (typed values; the 2030 cells of the underlying `AdHocCalculations.xlsb` are shown where they differ). (ii) Rebuild: `AdHocCalculations_Rebuild_v0.1.xlsx`, `Mode` = REBUILD, `Conv` = NOPHASE, `Yr` = 2030 (PolicyMatrix rows 7–12; `MethodologyNote_v0.1.md`). (iii) Merged prototype: `CPAT_Industry_Kernel_Egypt_v0.14.xlsx` (Task M), sheet `Table2_Industry` stored 2030 snapshot, `Manual inputs` at default (β = IPCC placeholder anchors, output response ON, `IppuOther` = NONE, CBAM convention FULL); NOPHASE values of O from the v0.13 run of the same block (v0.14 changes no prior sheet). All values 2030, carbon price 20 $/t in every bundle.

**Scope.** Table 2 and the rebuild are national (CPAT runs EG1 = 1A/2A, EG2 = 2B, EG3 = 3A–3C, with the CBAM block as an add-on). The prototype's national columns (J, K, P, Q) are a *composition*: CPAT deltas of the same runs with the industry/IPPU part replaced by the kernel's own response — and, for the industry-only bundles, only the four kernel sectors (iron & steel, cement, non-ferrous metals, chemicals; 16.4 Mt energy CO₂) are priced, not all industry (89 Mt in the CPAT run).

## 1. Side by side (2030)

**Carbon revenues raised, $bn (Table 2 col. 6; P)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | 5.8 | 5.2 | 5.2 | 1.1 | 0.0 | 0.0 |
| Original xlsb 2030 cell | 5.77 | 5.18 | 5.18 | 2.38 | 0 | 0 |
| Rebuild v0.1, net (gross) | 6.81 | 6.23 | 6.19 | 1.51 | 0.33 (1.55; rebate 1.22) | 0 (1.47 to fund; 0.19 spendable at σ = 20) |
| Prototype v0.14, net (gross) | 6.90 | 6.27 | 6.24 | 0.91 | 0.00 (0.97; rebate 0.97) | −0.37 (0.77; fund 1.14) |

**Total emissions reduction, MtCO₂e (col. 7; K)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (text) | −41.6 | −38.9 | −41.0 | −21.5 | −18.1 (13.6) | −24.5 |
| Rebuild v0.1 | −31.6 | −27.7 | −29.3 | −18.0 | −12.8 | −22.4 |
| Prototype v0.14 (composition) | −27.7 | −25.7 | −27.0 | −9.7 | −6.6 | −17.3 |
| Prototype block only (emrt) | −4.2 | −1.4 | −1.4 | −4.2 | −0.7 | −11.8 |

**CBAM coverage, % of CBAM-sector emissions (col. 8; M)** — identical in all three: 100 / 44.5 / 44.5 / 100 / 100 / 100 (fuel share of block emissions when only fuels are priced; export-weighted 54.7% in the prototype, `cbcovx`).

**Emission-intensity reduction, CBAM sectors, % (col. 9; N)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | −7.6 | −5.5 | −5.5 | −7.6 | −7.6 | −13.1 |
| Rebuild v0.1 | −6.6 | −2.2 | −2.2 | −6.6 | −6.6 | −12.7 |
| Prototype v0.14 | −1.1 | 0 | 0 | −1.1 | −1.1 | −14.3 |

**CBAM obligations reduced, % per unit exported (col. 10; O)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 (≈ NOPHASE) | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| Rebuild NOPHASE (FULL) | −24.9 (−44.9) | −13.1 (−24.1) | −13.1 (−24.1) | −24.9 (−44.9) | −6.2 (−6.2) | −29.5 (−48.2) |
| Prototype NOPHASE (FULL, Table2_Industry default) | −21.1 (−42.1) | −10.9 (−22.6) | −10.9 (−22.6) | −21.1 (−42.1) | −1.4 (−1.4) | −33.0 (−50.8) |

**Air-pollution deaths avoided per year (col. 11; Q)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 | 1,656 | 1,564 | 1,631 | 546 | 345 | 621 |
| Rebuild v0.1 | 1,564 | 1,564 | 1,631 | 546 | 412 | 633 |
| Prototype v0.14 | 1,441 | 1,441 | 1,497 | 278 | 241 | 397 |

**National GHG covered, % (col. 3 text; J)**

| Source | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Table 2 text | 72 | 65 | 65 | 20 | 20 | 20 |
| Original xlsb J | 72 | 65 | 65 | 24.3 | 24.3 | 24.3 |
| Rebuild v0.1 (κ = 1 memo) | 63.0 | 57.3 | 57.3 | 13.8 (20.7) | 13.8 (20.7) | 13.8 (20.7) |
| Prototype v0.14 | 63.0 | 57.3 | 57.3 | 8.5 | 8.5 | 8.5 |

Other PolicyMatrix columns (not in Table 2), rebuild / prototype: T block emissions −12.0/−6.8, −4.5/−2.4, −4.5/−2.4, −12.0/−6.8, −6.6/−1.1, −17.8/−19.3 %; U block output −5.8/−5.8, −2.4/−2.4, −2.4/−2.4, −5.8/−5.8, 0/0, −5.8/−5.8 %; AR Δnet revenue 10.43/11.10, 10.43/10.47, 10.62/10.67, 2.69/2.67, 1.47/1.76, 1.22/1.39 $bn (original 10.62 for 1A–2B, 2.69, 0, –).

## 2. Why K differs — decomposition, MtCO₂e

| Component | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| CPAT ΔGHG of the run (common start) | −38.88 | −38.88 | −41.00 | −21.54 | −21.54 | −21.54 |
| *Table 2 / original:* extra terms | −2.74 (1A built on EG2: −41.00 − 0.62 legacy process term) | 0 | 0 | 0 | K = −13.59·(2/3)/0.5 (untraceable) | −2.94 (untraceable) |
| *Rebuild:* remove CPAT's proportional IPPU scaling | +11.96 | +11.96 | +12.56 | +8.26 | +8.26 | +8.26 |
| *Rebuild:* block process intensity ER_p (IPCC β, 20 $/t; 3C: 40 $/t) | −2.55 | 0 | 0 | −2.55 | −2.73 | −4.89 |
| *Rebuild:* block process output channel | −2.17 | −0.81 | −0.81 | −2.17 | 0 | −2.17 |
| *Rebuild:* OBR correction D_obr / fund fuel F_fund | – | – | – | – | +3.24 | −2.10 |
| **Rebuild K** | **−31.64** | **−27.73** | **−29.25** | **−18.00** | **−12.76** | **−22.44** |
| *Prototype:* IPPU replacement (kernel ΔIPPU − CPAT ΔIPPU) | +9.04 (−2.92 + 11.96) | +11.03 | +11.64 | +5.34 | +7.59 | +0.60 (−7.66 + 8.26) |
| *Prototype:* industry-energy replacement (kernel composition − CPAT ΔInd) | +2.11 | +2.11 | +2.32 | +6.49 (−2.06 + 8.55) | +7.37 | +3.60 |
| **Prototype K** | **−27.73** | **−25.74** | **−27.05** | **−9.71** | **−6.59** | **−17.34** |

- **Table 2 → rebuild (10–12 Mt less for 1A–2B, 3.5 for 3A):** CPAT scales *all* IPPU (86 Mt) with industrial fuel CO₂ (−13.9% → −12 Mt), which a fuel price cannot do; the rebuild deletes that and adds the block's explicit process responses (ER_p via β, output channel). 1A also moves from the EG2 base to EG1 (#3). 3B: the untraceable K11 (−18.1; text 13.6) is replaced by EG3 with the OBR correction (+3.2: the output channel of the rebated 57% of industry is removed, 1 − s_int = 2/3 of the fuel response); 3C: σ = 20 $/t on both intensity channels instead of a −2.9 Mt constant.
- **Rebuild → prototype (−3.9 Mt for 1A, −8.3 for 3A, −6.2 for 3B, −5.1 for 3C):** (a) smaller kernel process response (ΔIPPU −2.9 vs −4.7 Mt: placeholder β anchors ≈ ¼ of the IPCC set); (b) industry energy: for *All sectors* the kernel's own 4-sector response (−2.06, −12.6%) replaces CPAT's (−13.9%) and non-kernel industry is scaled with the run — +0.2 Mt from the response, **+1.9 Mt from a data-vintage gap** (kernel industry CO₂ baseline 75.4 vs csv 89.0 Mt; the composition mixes the two totals through `nk1 = indx − ek1`); for *Industry only* everything outside the four sectors is unpriced, so CPAT EG3's −8.55 Mt of industrial fuel CO₂ shrinks to the kernel's −2.06 (3A), −1.18 (3B) or −4.95 (3C) — the single largest cause of the 3A–3C gap; (c) 3B: no D_obr-type correction is needed in the kernel (rebate per unit of output sets the output channel to 0 directly); 3C: the fund is solved as a shadow price s = 150 $/t spending the full 1.14 $bn (abatement 7.6 Mt: fuel 3.6, process 4.0) versus the rebuild's σ = 20 $/t.

## 3. Why the other columns differ

- **Revenue P.** Table 2's 5.8/5.2 cannot be reproduced from the 2030 CPAT outputs (six-fuel carbon-tax receipts 6.23 $bn EG1, 6.19 EG2); the rebuild and the prototype agree within 0.1 $bn (CPAT receipts + block process revenue 0.59–0.62 $bn; the prototype adds a +0.04 adjustment for its weaker industry response). 3A: 1.1 in the text = 20 $/t × 53.6 Mt (gross, typed; xlsb cell 2.38); rebuild 1.51 = 0.93 EG3 receipts (κ = 0.54 of industry priced) + 0.59 process; prototype 0.91 = 0.29 (four sectors' fuel) + 0.62 process. 3B: Table 2's 0 is a convention; prototype 0.00 by construction (output-based rebate 0.97 ≈ block payments 0.97); rebuild 0.33 because only CBAM producers are rebated (`ThetaOther` = 0) while the fuel levy on the rest of priced industry still yields revenue (gross 1.55; rebate 1.22 = v0.11 rule, uncapped — v0.13/14 cap it by sector shares 0.57–0.82). 3C: all three show nothing to the budget; the prototype is *negative* (−0.37) because the fund is fixed at pre-abatement revenue (1.14) and fully spent while post-abatement receipts fall to 0.77; the rebuild's fund (1.47) is 87% unspent at σ = 20 (outlay bound 0.19).
- **Coverage J.** Typed in the original (its own columns imply 59/53); rebuild and prototype compute the same 63.0/57.3 for 1A–2B (CPAT economy-wide energy CO₂ + priced block process 33.9 Mt over 594 Mt GHG). Industry bundles: Table 2's 20% ≈ all industry energy CO₂ + block process (20.7% at κ = 1), but the EG3 run prices only 54% of industrial fuel (rebuild 13.8%) and the kernel only its four sectors (8.5%).
- **CBAM coverage M.** Same definition everywhere; no difference.
- **Intensity N.** Table 2 from the legacy −0.549 %/$ block (#14). Rebuild: fuel-intensity channel exp(b_f τ) − 1 = −4.9% on the 44.5% fuel share (= −2.2%, the whole of 2A/2B) plus IPCC-β process response on the 55.5% process share → −6.6%. Prototype: block fuel intensity fixed and placeholder β → −1.1%; exactly 0 for 2A/2B (no process price, no fuel-intensity response). 3C: −13.1 / −12.7 / −14.3 agree only by coincidence (σ = 20 on both channels with large β vs s = 150 $/t with small β).
- **Obligations O.** O ≈ (1 + N)(1 − 20/100) − 1 in every source, so the gaps are N's: Table 2 −26.1 ↔ its −7.6; rebuild −24.9 ↔ −6.6; prototype −21.1 ↔ −1.1. The FULL convention (CBAM factor 0.485 in 2030) roughly doubles the percentage (prototype headline −42.1); Table 2 is on the NOPHASE basis. 3B: the rebate cancels the deductible price, so O ≈ N in all three (−7.6 / −6.2 / −1.4). 3C follows N (−30.4 / −29.5 / −33.0).
- **Deaths Q.** 1A: the original scaled EG2's 1,631 by K7/K9 → 1,656; 1A on EG1 gives 2A's 1,564 (the process charge has no air-quality effect). 3B: 345 typed/stale (#2); rebuild 412 = 546 × energy-CO₂ change after D_obr. 3C: 621 = 546 × K ratio incl. process; rebuild 633 rescales by energy CO₂ only. Prototype = CPAT deaths × (energy-CO₂ change with the kernel's industry response)/(CPAT's): ×0.92 for All sectors (1,441/1,497), ×0.51 for 3A (278) because only the four sectors' fuel responds; 241 (3B), 397 (3C).
- **AR.** Original 10.62 (EG2) for all of 1A–2B (#6); rebuild = CPAT Δnet revenue of the bundle's run less rebates/fund; prototype = CPAT Δnet revenue − CPAT receipts + its own P (so it adds the process revenue).

## 4. Internal inconsistencies in EgyptResultsInitial.docx

1. 3B reduction: table −18.1 Mt, text 13.6 Mt (range "13.6 to 41.6" and "3B … 13.6").
2. "5–17% of Egypt's annual CO₂ of about 249 Mt" uses a CO₂-only base, while the coverage shares (72/65/20%) use total GHG (594 Mt incl. LULUCF in 2030); on one base 1A is −7.0% (−41.6/594) and the rebuild's −5.3%.
3. Obligations: "about 8 to 30%" and "the 8% reduction (3B)" vs −7.6% in the table; intensity "nearly 8%" (1A/3A/3B) vs −7.6%, "nearly 6%" (2A/2B) vs −5.5%.
4. 3A revenue 1.1 $bn (= 20 × 53.6, gross block payments) vs 2.38 in the workbook cell and 0.93 of CPAT fuel receipts; the stated convention (value returned to firms not counted) is applied to 3B/3C but not to 3A's gross figure.
5. Coverage 72/65% typed; the workbook's own columns imply 59/53% and its 3A–3C coverage is 24.3%, not 20%.

## 5. Prototype caveats that matter for this comparison

- Industry-only bundles price the four kernel sectors only (about one fifth of industrial energy CO₂); Table 2 and the CPAT EG3 run intend all industry.
- Data-vintage mix in the K composition (+1.9 Mt in 1A/2A/2B); fund fixed at pre-abatement revenue (3C net revenue < 0); CBAM convention default FULL; placeholder β anchors and no fuel-intensity channel in the block (N, O, T understated relative to both other sources).
- The rebuild's `Mode` = PROTOTYPE reproduces the v0.11 block; v0.13/14 differ only for 3B (rebate capped by sector shares: 0.97 vs 1.22 $bn; block metrics unchanged) and 3C (fund active: N −14.3, O −33.0/−50.8, block −11.8 Mt; v0.11 had 3C ≡ 3A).

## 6. Bottom line

Table 2's national figures rest on the original workbook's defects (typed coverage, CPAT IPPU double-scaling, 1A on the wrong run, stale 3B deaths, three revenue concepts): the coherent rebuild gives 8–30% smaller K, ~1 $bn more revenue for the economy-wide bundles, 1A deaths = 2A. Block metrics (M, N, O) agree between Table 2 and the rebuild within ~1 pp because both carry a fuel-intensity response and a sizeable process response; the prototype's block is deliberately conservative (fixed fuel intensity, placeholder β), which is the main open modelling judgement (TASK-D β set, fuel-intensity channel), not an arithmetic discrepancy. The prototype's Task M national columns differ from the rebuild mainly through scope (four sectors vs all industry) and the data-vintage mix, both flagged above; where the scope is the same (1A–2B coverage, revenue) the two agree within 0.1 $bn / 0 pp.
