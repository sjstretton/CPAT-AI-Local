# Egypt Table 2 (2030): CPAT results with a CBAM carve-out (final v1.5)

**What this is.** The original CPAT runs give every result, except the CBAM block (steel, cement, fertilisers, aluminium). For the block, CPAT's implied change is taken out and replaced by: CPAT's own fuel-intensity response (fuel per tonne), the kernel's CBAM output response and, where process emissions are charged, the kernel's process abatement. Each effect is counted once. 3A–3C use CPAT run EG3 exactly as run (no scaling to full industry coverage). Carbon price USD 20/t in 2030 in every scenario. Line by line in live formulas: kernel `CPAT_Industry_Kernel_Egypt_v1.3.xlsx`, sheet `CarveOut_Table2`.

## Table 2 columns

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Coverage, % of GHG (J) | 63 | 57 | 57 | 14 | 14 | 14 |
| Revenue, $bn (P) | 6.9 | 6.3 | 6.2 | 1.5 | 0.3 | 0.4 |
| Emission cut, MtCO₂e (K) | −37.4 | −33.1 | −34.8 | −22.8 | −12.0 | −33.0 |
| Cut, % of GHG | −6.3 | −5.6 | −5.9 | −3.8 | −2.0 | −5.6 |
| CBAM coverage, % (M) | 100 | 44 | 44 | 100 | 100 | 100 |
| CBAM intensity, % (N) | −5.8 | −2.1 | −2.3 | −5.8 | −5.8 | −23.1 |
| CBAM obligations per tonne exported, % (O) | −5.4 | −2.6 | −2.7 | −5.4 | −5.4 | −20.7 |
| CBAM block emissions, % (T) | −11.6 | −4.7 | −4.8 | −11.6 | −5.8 | −27.8 |
| Deaths avoided (Q) | 1,501 | 1,456 | 1,517 | 552 | 330 | 646 |

## Comparison

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Emission cut, Mt: original Table 2 | −41.6 | −38.9 | −41.0 | −21.5 | −18.1 | −24.5 |
| Emission cut, Mt: **new** | −37.4 | −33.1 | −34.8 | −22.8 | −12.0 | −33.0 |
| Revenue, $bn: original Table 2 | 5.8 | 5.2 | 5.2 | 1.1 | 0.0 | 0.0 |
| Revenue, $bn: **new** | 6.9 | 6.3 | 6.2 | 1.5 | 0.3 | 0.4 |
| Deaths avoided: original Table 2 | 1,656 | 1,564 | 1,631 | 546 | 345 | 621 |
| Deaths avoided: **new** | 1,501 | 1,456 | 1,517 | 552 | 330 | 646 |
| Coverage, %: original Table 2 | 72 | 65 | 65 | 20 | 20 | 20 |
| Coverage, %: **new** | 63 | 57 | 57 | 14 | 14 | 14 |
| CBAM intensity, %: original Table 2 | −7.6 | −5.5 | −5.5 | −7.6 | −7.6 | −13.1 |
| CBAM intensity, %: **new** | −5.8 | −2.1 | −2.3 | −5.8 | −5.8 | −23.1 |
| CBAM obligations, %: original Table 2 | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| CBAM obligations, %: **new** | −5.4 | −2.6 | −2.7 | −5.4 | −5.4 | −20.7 |

## How K is built, MtCO₂e

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| CPAT ΔGHG of the run | −38.9 | −38.9 | −41.0 | −21.5 | −21.5 | −21.5 |
| CPAT industry change, % (applied to block) | −13.9 | −13.9 | −14.6 | −9.6 | −9.6 | −9.6 |
| Block emissions, baseline (fuel + process) | 63.1 | 63.1 | 63.1 | 63.1 | 63.1 | 63.1 |
| less: CPAT's implied block change | 8.8 | 8.8 | 9.2 | 6.1 | 6.1 | 6.1 |
| memo: CPAT fuel-intensity response, % | −4.9 | −4.9 | −5.1 | −4.9 | −4.9 | −4.9 |
| plus: new block change | −7.3 | −3.0 | −3.0 | −7.3 | −3.7 | −17.6 |
| plus: 3B rebate, non-block covered industry | 0.0 | 0.0 | 0.0 | 0.0 | 7.2 | 0.0 |
| **K** | −37.4 | −33.1 | −34.8 | −22.8 | −12.0 | −33.0 |

## Method notes

- **Runs.** 1A and 2A = EG1, 2B = EG2, 3A–3C = EG3 (CPAT csv, 2030).
- **IPPU.** CPAT scales all IPPU with industrial energy CO₂. The carve-out keeps that for non-CBAM IPPU (about 50 Mt, mainly F-gases and other process emissions) and replaces it only for the block. The earlier prototype (kernel v0.16) held non-CBAM IPPU fixed, which is most of why its 1A cut was lower.
- **Growth.** Block output is rescaled so 2024–2030 growth matches CPAT sector energy CO₂: steel (irn) ×0.976, cement (cem) ×1.001. CPAT has no energy in mining & chemicals (mch) or non-ferrous metals (nfm) for Egypt, so fertilisers (mch) ×1.157 and aluminium (nfm) ×0.956 follow total CPAT industry growth.
- **Sectors.** irn = iron and steel; cem = cement (non-metallic minerals); mch = mining and chemicals (ammonia, urea, ammonium nitrate); nfm = non-ferrous metals (aluminium).
- **Revenue P.** CPAT carbon-tax receipts of the run, plus the block fuel-revenue adjustment, plus block process fees; less the 3B output-based rebate (block rebate from the kernel plus the rebate to non-block covered industry, see below) and the 3C abatement fund (kernel value).
- **Deaths Q.** CPAT deaths of the run, scaled by (CPAT Δenergy CO₂ + block fuel adjustment) / CPAT Δenergy CO₂.
- **Coverage J.** 1A: all energy CO₂ plus block process; 2A/2B: energy CO₂; 3A–3C: EG3's priced industry energy (κ = 0.537 of 89.0 Mt) plus block process.
- **CBAM-sector intensity.** Fuel per tonne falls by CPAT's efficiency response: one third of CPAT's industry fuel response (s_int = 1/3, Methodology v1.5, section 5), i.e. (1 + r)^(1/3) − 1. EG3 prices only 54% of industry, so 3A–3C use the EG1 value (same USD 20/t; the block is fully priced). Process emissions per tonne change only where they are charged (1A, 3A–3C), from the kernel.
- **No double counting.** CPAT's block change (energy and its proportional IPPU) is removed in full; the block then gets CPAT's intensity response once and the kernel's output and process response once. The kernel's own fuel response is not used.
- **N, O.** N: kernel values plus the fuel-intensity term (output-weighted). O = change in CBAM obligations per tonne exported = export-weighted change in the embedded (fuel + process) emission intensity of CBAM products only (2024 EU export weights). No deduction for the Egyptian carbon price is applied, so the EU price and phase-in cancel. Live calculation: kernel sheet `Table2_Final`, section E (`CPAT_Industry_Kernel_Egypt_v1.5.xlsx`). O therefore differs from N only by weighting; it refers to CBAM products alone. M is unchanged.
- **3B rebate (decision 2026-10-04).** The output-based rebate covers all covered industry, not only CBAM producers. It removes the output channel of CPAT's response in the non-block industry: NB = CPAT industry fuel change + CPAT IPPU change − r × block (−10.7 Mt for EG3), and the output share (1 − s_int = 2/3) of it is taken out of K (+7.2 Mt). The fuel part of that term (+3.9 Mt) enters the deaths adjustment. Revenue is reduced by the rebate to non-block covered industry, USD 20/t × (κ × IND1 − block post-policy fuel CO₂) = USD 0.33bn. Switch: kernel `Manual inputs` E112 (1 = all covered industry, 0 = CBAM block only). The other scenarios and N, M, O, T, J do not change.
- **3C fund** is a kernel value; the small change in block fuel payments is not fed back into it or into the 3B rebate (under 0.05 $bn).
- **Why 3A–3C are low.** EG3 prices only about 54% of industrial energy CO₂, as CPAT ran it.
