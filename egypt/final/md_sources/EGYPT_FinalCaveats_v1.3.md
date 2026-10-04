# Egypt carbon pricing and CBAM: key caveats on the final results (final v1.3)

**Applies to the final results:**

- `EGYPT_CarveOut_Table2_v1.3` (final Table 2);
- `EgyptResultsInitial_UpdatedResults_v1.3_tracked.docx` (results text);
- `EGYPT_Methodology_v1.3` (section 4.5); `EGYPT_CBAM_ObligationNote_v1.3`;
- background models: kernel `CPAT_Industry_Kernel_Egypt_v1.3.xlsx` (sheet `CarveOut_Table2` computes the final Table 2 line by line) and ad hoc rebuild `AdHocCalculations_Rebuild_v0.3.xlsx`.

All figures are for 2030 at a carbon price of USD 20/t. This list covers only the material caveats, most important first. The full log is `CAVEATS.md`.

**Final v1.3 (2026-10-07)**: all documents aligned to v1.3; methodology based on the author's edited version; CBAM obligations on intensity only. **Final v1.0 (2026-10-04)** = draft v1.2, proofread. Since draft v1.1, the final Table 2 is now the **CBAM carve-out**: original CPAT runs everywhere, with only the CBAM block (steel, cement, fertilisers, aluminium) replaced, counted once. CBAM obligations (O) are the change in embedded emissions per tonne of CBAM products exported to the EU (update 2026-10-06). Section F is new. Sections A–D describe the prototype and rebuild, which now feed only the block response.

## F. Caveats on the final results (carve-out)

F1. **3A–3C use CPAT run EG3 as it was run.** EG3 prices only 54% of industrial energy CO₂ (κ = 0.537), so coverage is 14% and the non-block industry cut is diluted. The 1/κ scaling in the prototype and rebuild is not used. **A true full-coverage EG3 CPAT run is still needed.**

F2. **CBAM-sector fuel intensity uses CPAT's own response.** Fuel per tonne falls by CPAT's efficiency share (1/3) of its industry fuel response (about −5%). This is an industry average, not product-specific. 3A–3C use the EG1 value because the block is fully priced at the same USD 20/t.

F3. **Output and process responses come from the kernel,** so caveats 5–7 (emission factors, process semi-elasticities, placeholders) apply to the block.

F4. **3B rebate and 3C fund are the kernel's values.** They are not re-solved for the slightly lower block fuel payments (under USD 0.05bn). The 3C fund follows the prototype convention (caveat 2).

F5. **CBAM obligations (O) reflect only the change in CBAM-product emission intensity** (export-weighted, fuel + process, CBAM products only). No credit for the Egyptian carbon price is taken, so the EU price and phase-in drop out: 1A −5.4, 2A −2.6, 2B −2.7, 3A −5.4, 3B −5.4, 3C −20.7%. With a full domestic-price deduction (Art. 9) the cuts would be larger (memo rows in `EGYPT_Table2_Final_CBAMcalc_v1.3.xlsx`). Kernel v1.3 sheet `CarveOut_Table2` stores these values (column M of the snapshot); its live O row is the deduction-based memo. The workbook governs.

F6. **Growth.** Block output is rescaled to CPAT 2024–2030 sector growth (steel ×0.976, cement ×1.001). Fertilisers (mining & chemicals) and aluminium (non-ferrous metals) have no CPAT energy for Egypt, so they follow total CPAT industry growth.

F7. **Deaths** are CPAT deaths scaled by the block fuel-CO₂ adjustment. The original 3B figure (345) cannot be traced.

## A. Background: prototype and rebuild caveats

1. **The industry-only scenarios (3A–3C) rest on a linear full-coverage approximation.**
   - The CPAT run behind them (EG3) prices only 54% of industrial fuel use (κ = 0.537).
   - Both models now divide EG3's industry energy-CO₂ change, receipts and deaths by κ. This gives:
     - coverage of 20.8% (rebuild) or 18.5% (prototype);
     - reductions of −25.1 / −19.6 / −30.6 Mt (rebuild) and −21.1 / −17.4 / −32.9 Mt (prototype);
     - deaths avoided of 850 / 714 / 997.
   - These replace the previous figures of −18.2 / −12.7 / −22.6 Mt, which were lower bounds.
   - The approximation assumes that the sectors left out of EG3 (mainly aluminium and other manufacturing) respond like the average priced industry.
   - **A true full-coverage EG3 CPAT run is still needed to confirm 3A–3C.**
2. **The 3C fund convention differs between the two models.**
   - The prototype's fund equals the CBAM block's own carbon payments after abatement (USD 0.93bn), solved as a fixed point. The other industrial carbon revenue (USD 0.73bn) stays with the budget.
   - The rebuild sends all industrial carbon revenue to the fund (net revenue 0) and abates at a fixed USD 20/t.
   - As a result, the prototype's 3C reduction (−32.9 Mt) exceeds the rebuild's (−30.6 Mt).
   - **Which convention is intended changes 3C revenue by about USD 0.7bn.**
3. **The prototype still mixes two CPAT data vintages.**
   - Industrial energy CO₂ is 75.4 Mt (stored CPAT) vs 89.0 Mt (new Egypt runs). The prototype combines only changes within each source.
   - The mix accounts for most of the prototype–rebuild gap: about 1.9 Mt in 1A–2B and about 3.5 Mt in 3A/3B after 1/κ.
   - It also lowers the prototype's industry-only coverage and revenue.
4. **Block fuel CO₂ is still above CPAT's sector energy CO₂** (cement 19.05 vs 10.91 Mt in 2030; chemicals and non-ferrous metals small).
   - The prototype now reallocates the excess out of non-kernel industry, so industry totals are unchanged.
   - The underlying mismatch between the product-level fuel use and CPAT's energy balance is not resolved. The Egypt clinker fuel factor (0.314) is part of it.

## B. Provisional parameters

5. **The Egypt emission factors (EF v0.1) are Tier C/D estimates and still need verifying.**
   - Open items:
     - ammonia energy per tonne;
     - the nitric-acid N₂O abatement share;
     - Egyptalum PFC rates;
     - the kiln fuel mix;
     - DRI gas use;
     - the EISCO blast-furnace closure.
   - Egyptian data portals could not be reached.
   - The EU default values were copied, not re-verified.
6. **The process responses to the carbon price (IPCC AR6 based) involve judgement.**
   - The price anchor is now deflated: USD 100 in 2019 dollars = USD 122 in 2024 dollars. This lowered the process responses by about 18%.
   - **Ammonium nitrate:** assumes 50% existing N₂O abatement.
   - **Aluminium:** applies the combined response (0.2164) to both of its process categories.
   - **Ammonia and urea:** no process response, because the CCS/feedstock route (fp routing) is not implemented. This understates the fertiliser response.
   - **Basis:** global IPCC cost data, not Egyptian abatement cost curves.
7. **Several inputs are still placeholders:**
   - the output elasticity ε_Q (−0.5);
   - the EU allowance price P_EU (USD 100);
   - the rebuild's fund shadow price σ (USD 20/t).

## C. Structural limitations

8. **Some response channels are missing.**
   - The prototype holds the block's fuel intensity fixed. Its CBAM intensity change for 2A/2B is therefore 0 (rebuild −2.2%), and its obligation cuts and deaths avoided are slightly smaller.
   - The output-based rebate (3B) is applied on two paths that are not reconciled.
9. **CBAM obligation convention.**
   - The final Table 2 uses the embedded-intensity change only (no domestic-price deduction). The prototype and kernel use FULL; the rebuild and the original Table 2 use NOPHASE (both with a deduction).
   - Deduction-based conventions give much larger cuts (1A about −24% NOPHASE, −44% FULL); quote the basis with every obligation figure.
10. **General limitations:**
    - long-run elasticities are applied within one year;
    - industrial output is inferred rather than modelled, so read it as an upper bound;
    - there is no trade or leakage model;
    - emission factors are fleet averages;
    - revenue is simple revenue, excluding interactions with existing taxes and subsidies;
    - the CPAT runs have no recycling outputs.

## D. Relation to the initial results

11. **The initial results (Table 2) overstated reductions for the economy-wide scenarios.**
    - The rebuild gives 8–29% smaller reductions for these scenarios and about USD 1bn more revenue.
    - The main causes:
      - CPAT scaled all industrial process emissions with fuel CO₂;
      - coverage was typed in by hand;
      - 1A was built on the wrong run;
      - the 3B figures were stale.
    - Under the full-coverage approximation, the industry-only scenarios are now *larger* than Table 2 (3A −25.1 vs −21.5 Mt).

    The initial document is also internally inconsistent. For 3B the table says −18.1 Mt and the text says 13.6 Mt, and the emission bases are mixed. See `ResultsComparison_Table2_v0.3`, section 4.
