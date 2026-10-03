# Egypt carbon pricing and CBAM: key caveats on the final results (v1.0)

**Applies to:** the final prototype `CPAT_Industry_Kernel_Egypt_v0.15.xlsx`, the ad hoc rebuild `AdHocCalculations_Rebuild_v0.2.xlsx`, `ResultsComparison_Table2_v0.2`, `EgyptResultsInitial_UpdatedResults_v0.2_tracked.docx` and `EGYPT_Methodology_v1.1`. All figures are for 2030 at a carbon price of USD 20/t. This list covers only the material caveats, most important first. The full log is `CAVEATS.md`.

## A. Caveats that move the headline numbers

1. **Industry-only bundles (3A–3C) are understated and uncertain.**
   - The CPAT run behind them (EG3) prices only 54 % of industrial fuel use (κ = 0.54), so rebuild coverage is 13.9 % of GHG. The initial results gave 20 %.
   - The prototype prices only its four modelled sectors: 16.4 of 89 Mt of industrial energy CO₂, or 8.6 % coverage.
   - The two models disagree: 3A is −18.2 Mt (rebuild) vs −11.8 Mt (prototype), and 3B is −12.7 vs −8.6 Mt.
   - Re-running EG3 with full industrial coverage would raise coverage, reductions, revenue and deaths avoided for 3A–3C. **Treat 3A–3C as lower bounds.**
2. **Block fuel CO₂ exceeds the sector energy totals.** For cement, non-ferrous metals and chemicals, the product-level fuel CO₂ is above CPAT's sector energy CO₂ in every year. For cement it is about 13.5 vs 9.5 Mt in 2022. The Egypt clinker fuel factor (0.314) widens the gap. This affects the prototype's fund (3C) and revenue, but not the rebuild's 1A–2B national totals.
3. **3C (abatement fund) revenue is negative in the prototype (−USD 0.47bn).** The fund is fixed at revenue before abatement and is spent in full on block abatement. Revenue after abatement is lower, and it is also inflated by caveat 2. The prototype's 3C reduction of −23.9 Mt depends on spending the whole fund. The rebuild's 3C uses a fixed USD 20/t shadow price (−22.6 Mt, net revenue 0).
4. **The prototype mixes two CPAT data vintages.** It uses older CPAT values stored in the workbook alongside the new Egypt CPAT runs: industrial energy CO₂ in 2030 is 75.4 vs 89.0 Mt. The prototype combines only changes within each source, but the mix still accounts for about 1.9 Mt of the gap in 1A–2B, and the coverage figure mixes levels from both.

## B. Provisional parameters

5. **The Egypt emission factors (EF v0.1) are Tier C/D estimates and still need verifying.**
   - Open items: ammonia energy per tonne, the nitric-acid N₂O abatement share, Egyptalum PFC rates, the kiln fuel mix, DRI gas use and the EISCO blast-furnace closure.
   - Egyptian data portals could not be reached.
   - The EU default values were copied, not re-verified.
6. **Process responses to the carbon price (IPCC AR6 based) involve judgement:**
   - **Price basis:** the response is anchored at USD 100 in 2019 dollars and not deflated. Deflating to the 2024 price basis (about USD 122) would reduce the process responses by roughly 15–20 %.
   - **Ammonium nitrate:** assumes 50 % existing N₂O abatement.
   - **Aluminium:** applies the combined response (0.2164) to both of its process categories.
   - **Ammonia and urea:** no process response, because the CCS/feedstock route is not implemented. This understates the fertiliser response.
   - **Basis:** global IPCC cost data, not Egyptian abatement cost curves.
7. **Several inputs are still placeholders:**
   - the output elasticity ε_Q (−0.5);
   - the EU allowance price P_EU (USD 100);
   - the rebuild's fund shadow price σ (USD 20/t).

## C. Structural limitations

8. **Missing response channels:**
   - The prototype holds the block's fuel intensity fixed, so its CBAM intensity change for 2A/2B is 0 (rebuild −2.2 %). Its obligation cuts are smaller for the same reason.
   - The output-based rebate (3B) is applied on two paths that are not reconciled.
9. **CBAM obligation convention.** The prototype defaults to FULL (phase-in factor 0.485 in 2030). The rebuild and Table 2 use NOPHASE. FULL roughly doubles the percentage reduction in obligations, so quote the convention with every obligation figure.
10. **General limitations:**
    - long-run elasticities are applied within one year;
    - industrial output is inferred rather than modelled, so read it as an upper bound;
    - there is no trade or leakage model;
    - emission factors are fleet averages;
    - revenue is simple revenue, excluding interactions with existing taxes and subsidies;
    - the CPAT runs have no recycling outputs.

## D. Relation to the initial results

11. **Initial results (Table 2) overstated reductions.** The rebuild gives 8–30 % smaller reductions for the economy-wide bundles and about USD 1bn more revenue. The main causes:
    - CPAT scaled all industrial process emissions with fuel CO₂;
    - coverage was typed in by hand;
    - 1A was built on the wrong run;
    - the 3B figures were stale.

    The initial document is also internally inconsistent: for 3B the table says −18.1 Mt and the text says 13.6 Mt, and the emission bases are mixed. See `ResultsComparison_Table2_v0.2`, section 4.
