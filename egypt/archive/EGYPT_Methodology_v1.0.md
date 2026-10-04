# Egypt carbon pricing and CBAM exposure: integrated methodology

**Final version 1.0 (2026-10-04).** Final Table 2 = the CBAM carve-out (§5.0). This is the main methodology document for the Egypt thread. It draws together the ad hoc results and their review, the rebuilt Table 2 (AdHoc rebuild v0.3), the CPAT industry kernel (v0.1–v0.17; final release v1.0), the emission factors and the process-emission semi-elasticities. Detailed derivations sit in the source documents listed in Appendix C. Where this document and a source disagree, this document governs.

| | |
|---|---|
| Question | What do six carbon-pricing bundles do for Egypt's revenue, emissions, health and **exposure to the EU CBAM**? |
| Reporting year and price | 2030; USD 20/tCO₂e in 2030 for every bundle (real 2026 USD in CPAT) |
| Core tools | CPAT (IMF–World Bank) for national energy, revenue and health; the **CPAT industry kernel** for the eight CBAM goods; an off-kernel **Table 2 rebuild** that combines the two |
| Appendices | **A**: emission factors split four ways (fc, fp, np, no). **B**: process-emission semi-elasticities. **C**: file map. **D**: glossary |
| Status | The method is complete. Some inputs are flagged *VERIFY*. The Task D semi-elasticities (T1), the EF v0.1 values (T5) and the national composition (Task M) are **loaded in kernel v0.16**, and the Table 2 rebuild v0.3 uses the same EFs and β. Both models now deflate P* to USD 122 (2024) and scale EG3 to full industrial coverage by 1/κ (approximation). The final Table 2 (§5.0) does not use the 1/κ scaling. Open: T3, a true full-coverage EG3 CPAT run, the VERIFY list. See §8 |
| Final v1.0 | Draft v1.3 proofread and released as v1.0, with kernel v1.0, carve-out v1.0 and results text v1.1 |
| Changes in draft v1.3 | New §5.0: final Table 2 is the CBAM carve-out (O = CBAM-product embedded-intensity change): original CPAT runs everywhere; only the CBAM block replaced, with CPAT's own fuel-intensity response |
| Changes in draft v1.2 | P* deflated to 122 (USD2024); EG3 scaled by 1/κ in both models; kernel: 3C fund capped at post-abatement revenue (fixed point) and block fuel CO₂ above the sector total reallocated from non-kernel industry; §5, §5.1, §6–8, B.5 and App. C updated to rebuild v0.3 / kernel v0.16 |
| Changes in draft v1.1 | §5 results = rebuild v0.2 (Egypt EF v0.1, AN blended β); new §5.1 final prototype results (kernel v0.15); §6 version table to v0.15; §7–8 status; A.3 kernel column = v0.15; B.5 routing as applied; App. C file map |

---

## 1. Purpose and scope

The work assesses six policy bundles for Egypt, with CBAM-sector industry treated in detail. Each bundle is a CPAT scenario plus adjustments made outside CPAT.

| Code | Bundle | CPAT run | What is priced | Use of revenue |
|---|---|---|---|---|
| 1A | Comprehensive levy | EG1 | Energy CO₂, all sectors + CBAM process emissions | Public investment |
| 2A | Upstream levy | EG1 | Energy CO₂, all sectors | Public investment |
| 2B | Upstream levy | EG2 | Energy CO₂, all sectors | Per-capita transfers |
| 3A | Downstream industry price | EG3 | Industrial energy CO₂ + CBAM process emissions | Households |
| 3B | as 3A + free allocation | EG3 + output-based rebate θ = 1 | as 3A | Returned to CBAM producers per unit of output |
| 3C | as 3A + abatement fund | EG3 + fund φ = 1 | as 3A | Fund for industrial abatement |

Price paths: **EG1/EG2** USD 20 flat from 2028; **EG3** USD 5 in 2028 rising to USD 50 in 2034 (USD 20 in 2030). EG4 (an industrial feebate) is excluded because the run is misconfigured (MajorIssues #8).

**Outputs reported (Table 2):**
- coverage (% of national GHG);
- total emission reduction (Mt, and % of GHG);
- coverage of CBAM-sector emissions;
- change in CBAM-sector emission intensity;
- change in CBAM obligations;
- carbon revenue;
- air-pollution deaths avoided;
- change in output of CBAM goods.

**CBAM goods covered** (eight products and routes, kernel `Manual inputs` rows 30–37):
- steel by three routes: DRI-EAF, scrap-EAF, and BF-BOF (BF-BOF is a reference only);
- grey clinker;
- ammonia;
- urea;
- ammonium nitrate (AN);
- primary aluminium.

---

## 2. How the method developed

1. **Initial results (2026-06).** Table 2 in `EgyptResultsInitial.docx` was built in an ad hoc workbook (`AdHocCalculations.xlsb` / `Model_Results_and_Matrix_V1_21_EGY.xlsb`) on top of three CPAT runs. A review (`TechnicalNoteonCPATResults_expanded_v2.docx`, `MajorIssues.docx`) found **19 issues**. The most consequential:
   - **Process emissions counted twice (#17).** CPAT already scales IPPU with industrial energy CO₂, so 31–38% of each "energy-only" reduction is process. 1A then added a semi-elasticity cut on top.
   - **Untraceable parameters.** The −0.549%/$ energy "half elasticity" (#14), the 53.6 Mt CBAM base (#16) and 3B's typed-in −13.59 × (2/3)/0.5 (#15) have no recorded source.
   - **Inconsistent bases.** Base years are mixed (2026/2030, #4). Three different denominators are used for "% of emissions" (#11), and coverage shares are typed in (#12).
   - **Wrong scenario base.** 1A was built on EG2 rather than EG1 (#3).
2. **Diagnosis (TASK-2a).** The ad hoc calculations were written out as pseudocode and each step was mapped to the issue list.
3. **Two-track repair.**
   - **Track 1, the Table 2 rebuild (TASK-2b).** A live workbook replaces the ad hoc layer. It has one base year (2030), one denominator, computed coverage, and a bottom-up CBAM block. CPAT's IPPU scaling is removed and replaced by the block's process response (§5).
   - **Track 2, the CPAT industry kernel (Tasks A–M).** The industry part of CPAT is re-implemented as a standalone, AI-coded Excel kernel. It keeps legacy CPAT column positions, and its CBAM block reproduces legacy `Mitigation` rows 12198–12353. The kernel is then extended task by task (§6). It is the intended long-term home of the method. The rebuild is the bridge until **Task M** ports the national composition into the kernel.
4. **Parameter evidence.** Two pieces of work fill the parameter gaps flagged in the review:
   - IPCC-based process semi-elasticities (Task D, Appendix B);
   - Egypt-specific emission factors split four ways (Task EF, Appendix A).

---

## 3. CPAT: what is used and how it is read

**Fuel demand.** Fuel use F in sector *j*, fuel *k* responds to GDP *Y* and to the retail price *P*. *P* includes the carbon charge τ × EF × coverage. The response has two margins: a usage elasticity ε_U and an efficiency elasticity ε_F, with rebound acting on the efficiency term. To a close approximation, policy fuel use relative to baseline is

  F₁/F₀ ≈ (P₁/P₀)^(ε_U + ε_F(1+ε_U)) × (Y₁/Y₀)^η

Energy CO₂ = F × EF, with the EF held fixed. Industrial IPPU is projected by CPAT at the growth rate of industrial energy CO₂ (CPAT Team 2024, §3.5.5.1). **This is the proportional IPPU row that this method removes.**

**Output inferred from the usage margin.** CPAT has no industrial output variable. The usage term is read as the output response, and the efficiency term as the response of energy intensity. The intensity share of the fuel response is

  s_int = ε_F(1+ε_U) / (ε_U + ε_F(1+ε_U))

With ε_U = ε_F = −0.5, s_int = **1/3** and the output share is 2/3. The implied fuel-intensity semi-elasticity on EG1 is b_f = s_int · ln(IndCO₂₁/IndCO₂₀)/τ = **−0.0025 per $/t**.

**Other CPAT quantities used** (the bundle's own scenario, 2030):
- ΔGHG;
- ΔIPPU;
- ΔEnergy CO₂ and ΔIndustry CO₂;
- carbon-tax receipts by fuel (after the demand response);
- deaths avoided;
- Δ net new revenue.

**Non-price policies.** These enter as a *shadow price* on the efficiency term only. The fund (3C) uses this mechanism, applied *after* the carbon price (CPAT Team 2024, §3.1.8.1).

**Known CPAT limits that matter here.** CPAT has:
- no explicit output model;
- long-run elasticities that take full effect within one year;
- no technology switches such as CCS or H₂-DRI;
- no trade model, so CBAM exposure is computed outside CPAT;
- fixed world fuel prices;
- default IIASA emission factors that include some process emissions, corrected only at the aggregate level (§3.1.8.6).

---

## 4. The CBAM product block

For each product *i* (one row per product; equations as in the kernel and the rebuild `CBAM_Products` sheet), with τ the carbon price on fuels and τ_p = τ × (process flag) the price on process emissions:

**4.1 Emission factors (Appendix A).** Direct emissions per tonne are split four ways:
- **fc**: fuel combustion;
- **fp**: fuel used as reductant or feedstock;
- **np**: non-fuel process CO₂ (carbonates, electrodes, anodes);
- **no**: non-CO₂ gases (N₂O, PFC).

Each category has its own coverage switch for each bundle (kernel `Scenarios` M:P). Upstream levies price the **fuel group F = fc + fp**. Downstream charges can also price the **process group G = max(np,0) + max(no,0)**.

**4.2 Costs and rebates.**
- Fuel cost: k_f = τF_i.
- Process cost: k_p = τ_p G_i.
- Output-based rebate: m_i = min(θτ, τ)F_i + min(θτ, τ_p)·flag·G_i.
- Net cost increase: Δp_i = (k_f + k_p − m_i)/P_i, where P_i is the product price.

**4.3 Output response (Task H).** Q_i = Q_i^b (1 + Δp_i)^ε_Q, with Q_i^b = Q₀(1+g)^(t−2024) and **ε_Q = −0.5** (placeholder). Only the *net* price reaches output. Free allocation therefore weakens the output response but not the intensity response.

**4.4 Intensity responses.** These are applied to the *full* price, plus the fund shadow price σ_eff = φσ with σ = 20 $/t:
- **Fuel group.** x_f = exp(b_f(τ + σ_eff)), so ER_f = E_f(x_f − 1). This is the CPAT efficiency margin.
- **Process group.** ER_p = −E_p(1 − exp(−β_i(τ_p + σ_eff))), where β_i is the **process semi-elasticity** (Appendix B). In kernel v0.9+ this is generalised to ER(P) = ER_max(1 − e^(−βP)), separately for np and no.

**4.5 Emissions, revenue and CBAM metrics.**
- **Emissions.** E_f = Q_i F_i/1000 and E_p = Q_i G_i/1000 (Mt). The post-policy total is E_i = E_f + ER_f + E_p + ER_p.
- **Revenue.** rev_i = (E_f + ER_f)τ + (E_p + ER_p)τ_p, measured after the response (fixes MajorIssues #4 and #10). Rebates are deducted.
- **Embedded intensity.** EI_i = 1000E_i/Q_i.
- **Coverage.** cbcov = Σcovered/Σ(E_f + E_p).
- **Intensity change.** cbintch = ΣE_i/Σ(E_f + E_p) − 1. An EU-export-weighted variant is also reported (cbintchx).
- **CBAM obligation (Task L).** The deductible domestic price is d_i = 1000rev_i/Q_i − m_i. The obligation per tonne is obl_i = max(0, CBF·P_EU·EI_i − S·max(0, d_i)). The total is Σ X_i(Q_i/Q₀)·obl_i, where X_i is EU exports. The change is cbobchu.
- **Conventions.** P_EU = USD 100 (placeholder). The CBAM phase-in factor CBF and the deduction scaling S are set by a selector:

  | Convention | CBF | S | Use |
  |---|---|---|---|
  | NOPHASE | 1 | 1 | default in the rebuild |
  | FULL | 0.485 in 2030 | 1 | kernel headline |
  | SCALED | 0.485 | 0.485 | alternative |

**4.6 Channels kept separate (no double counting).**

| Channel | Driver | Acts on |
|---|---|---|
| Output | net price (after rebate) | Q, hence all four categories |
| Fuel intensity | full price + fund shadow price | fc + fp, via b_f |
| Process intensity | process price + fund shadow price | np, no via β (Appendix B) |
| CPAT's IPPU row | — | **removed** (`IppuOther` = NONE) |

---

## 5. National composition (Table 2)

**The final results are in §5.0.** The rest of §5 and §5.1 document the superseded rebuild and prototype results; they are kept for reference.

This is implemented in the rebuild (TASK-2b). It is to be ported to the kernel as Task M. Every percentage uses one base: CPAT's 2030 baseline GHG (594.2 Mt).

- **Coverage** J = (E_f⁰ + flag·E_p^base)/GHG₀.
  - E_f⁰ is energy CO₂ for the economy-wide bundles.
  - E_f⁰ is κ·IndCO₂₀ for the industry bundles, where κ = the share of industrial energy CO₂ actually priced in the CPAT run. κ(EG3) = 0.537 because aluminium and other manufacturing are not covered in that run; κ = 1 for EG1 and EG2.
  - **Full-coverage scaling (rebuild v0.3 / kernel v0.16).** Bundles 3A–3C are meant to price all industry, so CPAT's EG3 industry energy CO₂ change, receipts and deaths are divided by κ (0.537 in 2030), and coverage uses κ = 1. This is a linear approximation pending a true full-coverage EG3 CPAT run.
- **Total reduction** K = ΔGHG − ΔIPPU + IPPU_other + ΣER_p + Σemrq_proc + D_obr + F_fund. The terms:
  - IPPU_other = 0: CPAT's proportional IPPU response is removed (#17).
  - ΣER_p: process-intensity response from the block.
  - Σemrq_proc: output-channel process reduction.
  - D_obr = −(1 − s_int)·w·ΔIndCO₂ when θ > 0. Free allocation neutralises the output share of CPAT's industrial fuel response. Here w = E_f^base/(κ·IndCO₂₀) = 0.57.
  - F_fund = κ·IndCO₂₁(exp(b_f σ_eff) − 1) when φ > 0. This is the fund's fuel-intensity abatement outside the block.
- **Revenue** P = (1 − φ)·(CPAT fuel carbon receipts after the response + Σ block process revenue − rebates).
- **Deaths.** CPAT deaths for the bundle's own scenario, rescaled by *energy* CO₂ only for the industry bundles. Process CO₂ carries no PM2.5 benefit (#19).
- **Decomposition check.** The decomposition columns AF–AM sum to K (check = 0).

**Rebuilt results, 2030** (AdHoc rebuild v0.3, REBUILD mode, NOPHASE, `EFSet` = EGY_EF_V01; original Table 2 in brackets). These use the Egypt CBAM EF v0.1 values (Appendix A; block baseline 62.42 Mt in 2030) and the Task D central β set, with the AN N₂O row blended at 50% abatement (ER at $100 = 0.6179), anchored at P* = USD 122 (USD 100 in 2019 dollars deflated to 2024), and EG3 scaled by 1/κ:

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Coverage, % GHG | 63 (72) | 57 (65) | 57 (65) | 21 (20) | 21 (20) | 21 (20) |
| Reduction, Mt | −31.4 (−41.6) | −27.8 (−38.9) | −29.3 (−41.0) | −25.1 (−21.5) | −19.6 (−18.1) | −30.6 (−24.5) |
| CBAM coverage, % | 100 | 44.2 (44.5) | 44.2 (44.5) | 100 | 100 | 100 |
| CBAM intensity, % | −5.8 (−7.6) | −2.2 (−5.5) | −2.2 (−5.5) | −5.8 (−7.6) | −5.8 (−7.6) | −11.2 (−13.1) |
| CBAM obligation per unit, % | −24.3 (−26.1) | −12.5 (−13.9) | −12.5 (−13.9) | −24.3 (−26.1) | −5.4 (−7.6) | −28.4 (−30.4) |
| Revenue, USD bn | 6.84 (5.8) | 6.23 (5.2) | 6.19 (5.2) | 2.34 (1.1) | 1.13 (0) | 0 (0) |
| Deaths avoided | 1,564 (1,656) | 1,564 (1,564) | 1,631 (1,631) | 850 (546) | 714 (345) | 997 (621) |

**Main differences from the original Table 2:**
- Economy-wide reductions are 8–29% smaller, because CPAT's IPPU scaling and the untraceable process term are removed.
- Economy-wide coverage is lower, because it is computed rather than typed in.
- Industry-only bundles (3A–3C) are larger than in Table 2 once EG3 is scaled to full industrial coverage (approximation).
- Revenue is higher, because it uses CPAT's own 2030 receipts.

Full comparison: `Old\MethodologyNote_v0.3.md` and `Old\ResultsComparison_Table2_v0.3.md`. The final results text is `EgyptResultsInitial_UpdatedResults_v1.2_tracked.docx` (top level of both Egypt folders).

### 5.0 Final Table 2: CBAM carve-out (adopted)

The final numbers (used in `EgyptResultsInitial_UpdatedResults_v1.2_tracked.docx`) keep the **original CPAT runs** for everything and change only the **CBAM block** (steel, cement, fertilisers, aluminium; 63.1 Mt in 2030). Full table and build: `EGYPT_CarveOut_Table2_v1.0.docx`, `Old\AdHocRebuild\make_carveout_v0_3.py`. Line by line in live formulas: kernel v1.0, sheet `CarveOut_Table2` (active bundle from Settings!B10, plus a stored 6-bundle snapshot and check).

- **K = ΔGHG_CPAT − r×B + ΔB.** r is CPAT's industry energy CO₂ change of the run (EG1 −13.9%, EG2 −14.6%, EG3 −9.6%). CPAT scales all IPPU by the same %, so r×B is CPAT's implied block change; it is removed in full. Non-CBAM IPPU keeps CPAT's response.
- **ΔB, counted once:** (i) **CPAT fuel-intensity response**: fuel per tonne × (1+r)^(1/3) (efficiency share s_int = 1/3, §3); −4.9% on EG1, −5.1% on EG2; 3A–3C use −4.9% (same USD 20/t, block fully priced; EG3's r is diluted by κ = 0.537); (ii) **output**: the kernel's CBAM output response; (iii) **process**: kernel process abatement where process emissions are charged (1A, 3A–3C). The kernel's own fuel-intensity response is not used.
- **Growth:** block output rescaled so 2024–2030 growth matches CPAT sector energy CO₂ (irn ×0.976, cem ×1.001); mch (mining & chemicals: ammonia, urea, AN) ×1.157 and nfm (aluminium) ×0.956 follow total CPAT industry, as CPAT has no energy in those sectors for Egypt.
- **N, O:** N = kernel values plus the fuel-intensity term. O = change in CBAM obligations per tonne exported = export-weighted change in the embedded (fuel + process) emission intensity of CBAM products only (2024 EU export weights). No deduction for the Egyptian carbon price is applied, so the EU price and phase-in cancel. Live calculation: `EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx`. The §4.5 conventions (FULL/NOPHASE/SCALED, with a domestic-price deduction) are no longer used for Table 2; the workbook shows them as memo rows only. **P:** CPAT receipts + block fuel adjustment + process fees − 3B rebate − 3C fund. **Q:** CPAT deaths × (ΔEnergyCO₂ + block fuel adjustment)/ΔEnergyCO₂. 3A–3C use EG3 as run (no 1/κ scaling).

| 2030 | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Coverage, % GHG | 63 | 57 | 57 | 14 | 14 | 14 |
| Revenue, USD bn | 6.9 | 6.3 | 6.2 | 1.5 | 0.6 | 0.4 |
| Reduction, Mt | −37.4 | −33.1 | −34.8 | −22.8 | −19.1 | −33.0 |
| CBAM coverage, % | 100 | 44 | 44 | 100 | 100 | 100 |
| CBAM intensity, % | −5.8 | −2.1 | −2.3 | −5.8 | −5.8 | −23.1 |
| CBAM obligations per tonne exported, % | −5.4 | −2.6 | −2.7 | −5.4 | −5.4 | −20.7 |
| Deaths avoided | 1,501 | 1,456 | 1,517 | 552 | 491 | 646 |

§5 (rebuild) and §5.1 (prototype) below are kept for reference; they are superseded by this section.

### 5.1 Final prototype results (kernel v0.16, Task M, 2030)

The kernel composes the same CPAT runs in deltas, replacing CPAT's industry and IPPU responses with its own (K = ΔGHG_CPAT + (ΔIPPU_kernel − ΔIPPU_CPAT) + (ΔInd_kernel − ΔInd_CPAT)). Same EFs and β as the rebuild; CBAM convention FULL by default (NOPHASE in brackets for O). Changes in v0.16: P* = 122; EG3 non-kernel industry responds at CPAT's full-coverage rate (ΔInd_CPAT/κ), coverage and receipts use κ = 1, deaths are divided by κ; block fuel CO₂ above a sector's CPAT energy CO₂ (cement 19.05 vs 10.91 Mt in 2030; chemicals; non-ferrous metals) is taken out of non-kernel industry (kernel sectors 26.5 Mt, non-kernel 48.9 Mt, total unchanged); the 3C fund is capped at the block's post-abatement payments (fixed point).

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Coverage, % GHG | 63.2 | 57.3 | 57.3 | 18.5 | 18.5 | 18.5 |
| Reduction, Mt | −29.0 | −25.5 | −26.7 | −21.1 | −17.4 | −32.9 |
| CBAM coverage, % | 100 | 44.2 | 44.2 | 100 | 100 | 100 |
| CBAM intensity, % | −3.6 | 0 | 0 | −3.6 | −3.6 | −21.1 |
| CBAM obligation per unit, % FULL (NOPHASE) | −42.9 (−22.3) | −21.6 (−10.5) | −21.6 (−10.5) | −42.9 (−22.3) | −2.9 (−2.9) | −51.9 (−34.6) |
| Revenue, USD bn | 6.89 | 6.28 | 6.24 | 1.88 | 0.98 | 0.73 |
| Deaths avoided | 1,421 | 1,421 | 1,473 | 816 | 746 | 985 |

**Prototype vs rebuild.** Within about 2.4 Mt for 1A–2B and 4 Mt for 3A/3B. The process response is common; the remaining gap is the data-vintage mix in the composition (≈ 1.9 Mt at κ = 1, ≈ 3.5 Mt for EG3 after 1/κ) plus the fixed block fuel intensity, which also makes intensity N smaller. 3C is larger (−32.9 vs −30.6 Mt) because the fund buys block process abatement at the solved shadow price; its net revenue (0.73) is the non-block industry revenue, which the rebuild sends to the fund instead (convention difference).

---

## 6. Implementation: the CPAT industry kernel

`cpat_excel_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v1.0.xlsx` (final release; `build_v1_0.py` relabels v0.17, which is v0.16 + sheet `CarveOut_Table2`; earlier versions and builders in `Old\`). Each increment adds one task, has its own builder, and must pass a zero-difference regression against the previous version and against legacy CPAT (`Check` sheet).

| Version | Task | Content |
|---|---|---|
| v0.1–v0.2 | — | Industry kernel; conformed to NORMS (MTInputs layout, colours) |
| v0.3 | TASK-1 | CBAM block (legacy rows 12198–12353) after each scenario; `Manual inputs` rows 18–47 |
| v0.4 | E | `Scenarios` sheet: price paths (FLAT20_2028, RAMP_EG3, …) and bundles LEGACY, 1A–3C |
| v0.5 | A | Unique output codes for fuel and process rows; revenue rows corrected (post-policy emissions, correct flags, fuel revenue included) |
| v0.6 | B | Four-way EF split with a coverage switch per bundle and category |
| v0.7 | C | Process emissions priced at the process path `pptraj` |
| v0.8 | K | CBAM coverage and intensity metrics (cbcov, cbint, cbintch, cbintchx, cbcovx) |
| v0.9 | D (scaffold) | Process semi-elasticities by product and category (np, no) with ER_max; selector `E50`. Values were placeholders; IPCC values loaded in v0.15 |
| v0.10 | H | Output responds to the net cost increase (ε_Q placeholder −0.5) |
| v0.11 | L | CBAM obligations (EU price, phase-in, deduction convention) |
| v0.12 | F, I, J (merged) | `Data_EF`, `Emissions_Industry` (energy CO₂), `Rebate_Industry` (output-based rebate), `Fund_Industry` (fund to shadow price) |
| v0.13 | G | `IPPU_Industry`: CPAT IPPU row replaced by block np + no (+ fp flagged as IPPU, e.g. ammonia); switch `IppuOther`; sector fuel-CO₂ reconciliation. Report only |
| v0.14 | M | `CPAT_National`, `Table2_Industry`: links to main CPAT and Table 2 assembly (composition in deltas; stored 2030 snapshot) |
| v0.15 | T1 + T5 | Egypt CBAM EF v0.1 in `Manual inputs` H30:K37; Task D IPCC β in rows 53–60 (`E50` = IPCC); fix of the non-CO₂ process rows (o15/o16) |
| v0.16 | Run 2 fixes | P* = 122 (USD2024); `Table2_Industry` κ row 54, EG3 1/κ scaling (rows 64, 84, 91, 94, 96), block fuel CO₂ reallocation (rows 59–60); `Fund_Industry` stored fixed-point fund (rows 425–433) capped at post-abatement revenue; new Check section |
| v0.17 | Final Table 2 | Sheet `CarveOut_Table2`: CBAM carve-out in live formulas (active bundle) plus stored 6-bundle snapshot and check; no other formulas changed |
| v1.0 | Release | v0.17 relabelled as the final release; no formula or value changes |

**Audit-trail rules** (`NORMS.md`):
- legacy column positions;
- inputs are green and calculation cells hold no typed numbers;
- every new input has a code, a source and a confidence rating;
- every saved change gets a new version number and a version-log row;
- an append-only `CAVEATS.md` entry for every finished task.

The EF and semi-elasticity workbooks follow the same rules. Every number is a cited constant, a flagged input or a formula. Inputs carry defined names, and a recalculation script checks for errors.

---

## 7. Parameters and their basis

| Parameter | Value | Basis | Confidence |
|---|---|---|---|
| Emission factors fc / fp / np / no | Appendix A | Egypt fleet + IPCC 2006 / CBAM Annex VIII | Tier C/D; VERIFY list |
| Process semi-elasticities β_i | Appendix B; loaded in kernel v0.16 and rebuild v0.3 (AN 0.6179 blend; Al 0.2164 on np and no; NH₃/urea 0); P* = USD 122 (USD2024) | IPCC AR6 WGIII Tables 11.3, 12.3; AR4 for N₂O and PFC | Medium–low; range = 2030 vs long run |
| Usage / efficiency elasticities | CPAT `Data_Elast` | Labandeira et al. (2017) | CPAT default |
| s_int | 1/3 | ε_U = ε_F = −0.5 | Judgement |
| b_f | −0.0025 per $/t | s_int × CPAT EG1 industry CO₂ response | Derived |
| ε_Q (output) | −0.5 | Placeholder | Low |
| P_EU; CBF | USD 100; 0.485 (2030) | Placeholder; EU CBAM phase-in | Medium |
| σ (fund shadow price) | USD 20/t in the rebuild; solved in the kernel from a fund equal to post-abatement block payments | Judgement (rebuild fund outlay well below the budget of USD 1.48bn) | Low |
| Production, exports, prices | Kernel `Manual inputs` | worldsteel, IFA, trade data (2024) | Medium (T3 to formalise) |

---

## 8. Status, open issues and next steps

| # | Item | Status / action |
|---|---|---|
| 1 | **Task D values in the kernel** (T1): rows 53–60 = IPCC central. Routing β to fp (ammonia CCS, DRI; Appendix B.5) not implemented | Done v0.15 (P* deflated to 122 in v0.16); fp routing open (caveat) |
| 2 | **EF v0.1 in the kernel** (T5): H30:K37; urea np = 0 (CBAM rule), AN no = 0.9944 (HNO₃ N₂O folded in, 50% abatement for β) | Done v0.15 (provisional conventions) |
| 3 | **Task M**: §5 composition in the kernel (`Table2_Industry`) | Done v0.14, refreshed v0.15 and v0.16 |
| 4 | **Re-run EG3 with full industrial coverage** so that κ = 1 | Approximated by 1/κ scaling in rebuild v0.3 and kernel v0.16; a true CPAT re-run is still open |
| 5 | **Fuel-CO₂ reconciliation** (v0.13): block fuel CO₂ exceeds CPAT sector energy CO₂ for cement, non-ferrous metals and chemicals (cement ≈ 13.5 vs 9.5 Mt in 2022). EF v0.1 raises clinker fc to 0.314 (now in v0.15), which widens the gap; CPAT energy balances need review | Kernel v0.16 reallocates the excess out of non-kernel industry (industry total unchanged); CPAT energy balances still need review |
| 6 | **T3**: move market data (exports, prices, EU defaults) into `Manual inputs` with sources | Queued |
| 7 | **VERIFY list** for EFs (Appendix A.6) and for the AN abatement baseline (B.4) | Data requests |
| 8 | **Placeholders**: ε_Q, P_EU, σ | Calibrate or document |

**Overall limitations:**
- Long-run elasticities are applied within a single year.
- Industrial output is inferred, not modelled; read it as an upper bound.
- There is no trade or leakage model.
- Process responses come from global IPCC cost data rather than Egyptian MACCs.
- National EFs are fleet averages, not plant distributions.
- Revenue is "simple revenue", excluding effects on existing taxes and subsidies.

---

# Appendix A. Emission factors for Egypt's CBAM goods, split four ways

**Source:** `EmissionFactors\EGY_CBAM_EF_Methodology_v0.1.md` and workbook `EGY_CBAM_EF_v0.1.xlsx`. The workbook is built by `build_ef_v0_1.py` and checked by `recalc_and_check.py`: 0 errors, 14 checks OK.

### A.1 Method in brief
1. **Boundary.** Direct (Scope 1) emissions of the installation making the good, per tonne, using CBAM boundaries:
   - crude steel at the melt shop;
   - clinker at the kiln;
   - the ammonia complex;
   - the urea plant;
   - the AN plant;
   - primary aluminium.

   Electricity (Scope 2) is excluded. A **chain EF** adds precursor emissions category by category (urea 0.570 t NH₃/t; AN 0.79 t HNO₃ + 0.215 t NH₃/t; HNO₃ 0.27 t NH₃/t).
2. **Attribution.** The four categories are additive: EF = fc + fp + np + no. The split attributes the same carbon to different categories and never changes the total.
   - **fc vs fp, the "purpose of the carbon" rule.** Fuel carbon charged into the process as reductant or feedstock is **fp**. This covers ammonia reformer feed gas, DRI reducing gas, and BF coke and PCI. Fuel burned for heat is **fc**. Carbon retained in DRI is carried into the EAF and counted as fp there.
   - **np** is computed stoichiometrically: CaO × 0.785 and MgO × 1.092 tCO₂/t, with a kiln-dust correction. Electrode, charge-carbon and anode carbon use CBAM carbon contents.
   - **no** = kg gas/t × GWP. The CBAM/EU MRR set (AR5) is used: N₂O 265, CF₄ 6630, C₂F₆ 11100.
3. **Conventions.**
   - Urea: under the CBAM rule, CO₂ bound in urea is counted at the ammonia plant, so urea np = 0. The switch `urea_conv` = IPCC reproduces the inventory netting of −0.733.
   - AN: HNO₃ is treated as a precursor, and its N₂O is shown in the chain EF.
4. **Data hierarchy.** Inputs are graded in tiers:
   - **A**: plant data (none yet);
   - **B**: Egyptian statistics;
   - **C**: technology default calibrated to Egypt's plant fleet;
   - **D**: IPCC or international default.

   Every input row records its value, a low–high range, its tier, the source ID and a VERIFY flag.

### A.2 Key equations (tCO₂e/t; EF_NG = 0.0561 tCO₂/GJ; C→CO₂ = 3.664)
- **DRI** (Midrex/HYL, Ezz Steel):
  - fp = NG 10.5 GJ × feed share 0.75 × EF_NG − C_DRI × 3.664 = 0.372;
  - fc = 10.5 × 0.25 × EF_NG = 0.147;
  - the carbon balance closes (check 1).
- **DRI-EAF steel** = 0.98 × DRI + EAF:
  - EAF fc = 0.6 GJ × EF_NG;
  - EAF fp = DRI carbon − steel carbon;
  - EAF np = electrodes + charge carbon + limestone.
- **Clinker:**
  - fc = 3.5 GJ/t × fuel-mix EF 0.0896 (coal 45 / petcoke 40 / NG 5 / HFO 2 / alternative fuels 8%) = 0.314;
  - np = (0.65 × 0.785 + 0.015 × 1.092) × 1.02 = 0.537;
  - cement memo at clinker ratio 0.85: 0.723.
- **Ammonia:**
  - fp = feed 22.5 GJ × EF_NG = 1.262;
  - fc = (35.2 − 22.5) GJ × EF_NG = 0.712.
- **Nitric acid:** no = [0.5 × 2.5 + 0.5 × 7.0] kg N₂O × 265/1000 = 1.259 per t HNO₃.
- **Aluminium:**
  - np = anode 0.44 × (1 − 0.024) × 3.664 + baking 0.05 = 1.623;
  - no = (CF₄ 0.10 × 6630 + C₂F₆ 0.01 × 11100)/1000 = 0.774;
  - fc = 2.2 GJ × EF_NG = 0.123.

### A.3 Results (own process, CBAM conventions, tCO₂e/t)

| Good (kernel row) | fc | fp | np | no | **Own** | Chain | Kernel v0.13 (before T5) |
|---|---|---|---|---|---|---|---|
| DRI-EAF steel (30) | 0.178 | 0.393 | 0.038 | 0 | **0.609** | 0.609 | 0.730 |
| Scrap-EAF steel (31) | 0.045 | 0 | 0.044 | 0 | **0.089** | 0.089 | 0.155 |
| BF-BOF steel, reference (32) | 0.168 | 1.257 | 0.053 | 0 | **1.478** | 1.478 | 2.172 |
| Grey clinker (33) | 0.314 | 0 | 0.537 | 0 | **0.851** | 0.851 | 0.814 |
| Ammonia (34) | 0.712 | 1.262 | 0 | 0 | **1.975** | 1.975 | 1.851 |
| Urea (35) | 0.112 | 0 | 0 | 0 | **0.112** | 1.238 | −0.621 |
| Ammonium nitrate (36) | 0.112 | 0 | 0 | 0 | **0.112** | 1.953 | 1.082 |
| Primary aluminium (37) | 0.123 | 0 | 1.623 | 0.774 | **2.521** | 2.521 | 2.506 |

**Kernel v0.15 uses these fc / fp / np / no values** (`Manual inputs` H30:K37), with two conventions: urea np = 0 (as here) and AN no = 0.9944 (HNO₃ N₂O 0.79 × 1.2588 folded into own emissions, so AN own = 1.107). The last column shows the pre-T5 kernel values.

**Why the results differ from the pre-T5 kernel (v0.13):**
- **Urea:** CBAM rule here, inventory netting in the kernel.
- **AN:** the kernel folds 0.97 of HNO₃ N₂O into own emissions.
- **DRI-EAF:** rebuilt from a carbon balance, because the kernel's EF-input columns S:V are inconsistent with its own H:I values.
- **Ammonia:** 35.2 GJ/t here versus about 33 in the kernel.
- **Clinker and aluminium:** within 5% of the kernel.

### A.4 Checks
The workbook runs 14 checks:
- **Structural:** carbon balance, fuel shares, bounds.
- **Integrity:** totals equal the sum of components; no negative components.
- **Plausibility against IPCC Tier 1:**
  - ammonia 1.694–2.104;
  - clinker np 0.50–0.55;
  - aluminium np 1.45–1.75;
  - DRI.
- **Information:** reconciliation of about 50.7 MtCO₂e at kernel production volumes, of which clinker is about 42.6, to be compared with the BTR inventory.

### A.5 How the split is used
fc and fp form the **fuel group**, which is priced by upstream and downstream levies. np and no form the **process group**, which is priced only by downstream or process charges. Each category is the base for one response channel (§4.6 and Appendix B.5).

### A.6 VERIFY list (in order of impact)

| # | Input | Current value | Sensitivity of the EF |
|---|---|---|---|
| 1 | Ammonia gas use | 35.2 GJ/t | ±0.056 per GJ |
| 2 | HNO₃ N₂O abatement share (Abu Qir CDM) | 50% | ±0.6 per t HNO₃ |
| 3 | Egyptalum PFC rates | — | up to +2.0 |
| 4 | Kiln fuel mix | — | coal↔NG swap ≈ 0.13 |
| 5 | DRI gas use and feed/fuel split | — | — |
| 6 | Closure of EISCO's blast furnace (unconfirmed) | — | — |
| 7 | EU default values | — | — |

---

# Appendix B. Process-emission semi-elasticities (Task D)

**Sources:**
- `ProcessEmissions_CarbonPrice_Response\ProcessEmissions_CarbonPriceResponse_Report.md` and its workbook, which contain the derivation;
- `TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`, which gives the kernel-ready values.

The earlier near-term MACC draft (`InitialResultsAndIssues\CBAM_Process_MACC_Audit_Trail.docx`) is superseded. It assumed undeployed CCS on ammonia (85% at USD 100) and no deployment constraint.

### B.1 What is being estimated
The **semi-elasticity** β is the proportional change in process-emission *intensity* (tCO₂e per tonne of product) per USD 1/t of carbon price. Output effects are excluded; they are handled by ε_Q. "Half elasticity" in earlier documents means this semi-elasticity.

Scope is IPCC category 2 (IPPU) emissions:
- calcination CO₂;
- reductant and feedstock CO₂ (BF, DRI, SMR shift);
- electrode, anode and flux CO₂;
- N₂O from nitric acid;
- aluminium PFCs.

Combustion is excluded.

### B.2 Method in brief
1. **Evidence.** IPCC AR6 WGIII publishes costs and potentials, not elasticities. Two tables are used:
   - Table 11.3: technology GHG reductions and cost ranges, USD2019;
   - Table 12.3: 2030 economic potentials by cost bin.

   For N₂O and PFCs, IPCC AR4 WGIII Ch. 7 is used, cross-checked against NACAG.
2. **Cost-bucket MACC by product.** Each abatement option *i* has:
   - a technical reduction r_i;
   - a share s_i of the process pool it addresses;
   - a cost range [c_low, c_high];
   - a deployment factor d_i,h for horizon h.

   Plants' costs are assumed uniform over the range, so the share of plants in the money at price τ is f_i(τ) = clip((τ − c_low)/(c_high − c_low), 0, 1). Options combine multiplicatively, which avoids double counting:

   a_h(τ) = 1 − Π_i (1 − r_i s_i d_i,h f_i(τ))
3. **Two horizons.**
   - **2030**: d calibrated to the IPCC Table 12.3 potentials (constrained by deployment).
   - **Long run**: full turnover of the capital stock at Table 11.3 costs.
   - **Central** = the mean of the two. It is the recommended value for 2030–2045 policy runs. The 2030 value is the low case and the long-run value the high case.
4. **Semi-elasticity form.** Iso-semi-elastic: E(τ) = E₀ e^(−βτ), with β = −ln(1 − a(100))/100. This is the kernel convention: E stored positive, per $. It keeps emissions positive and is defined at τ = 0. A constant elasticity form is not.
   - Kernel v0.9+ uses ER(P) = ER_max(1 − e^(−βP)). With ER_max = 1 (**Option A**) this is identical to the iso-semi-elastic form.
   - **Option B** fits a saturating form (ER_max = A) to a(100) and a(200).
5. **Prices** are in USD2019; USD 100 (2019) ≈ USD 122 (2024). The kernel price paths must be deflated, or ER rescaled, before use.

### B.3 Results (central; ER = reduction in process intensity at USD 100)

| Product | ER at $100: 2030 / long run / **central** | β central (per $; kernel convention) | Option B: A / β |
|---|---|---|---|
| DRI-EAF steel | 0.113 / 0.573 / **0.343** | 0.00420 | 0.408 / 0.0184 |
| Scrap-EAF steel | 0.095 / 0.267 / **0.181** | 0.00200 | 0.399 / 0.0060 |
| BF-BOF steel (reference) | 0.102 / 0.459 / **0.280** | 0.00329 | 0.387 / 0.0129 |
| Grey clinker | 0.193 / 0.478 / **0.335** | 0.00408 | 0.433 / 0.0149 |
| Ammonia | 0.150 / 0.445 / **0.297** | 0.00353 | 0.443 / 0.0111 |
| Urea | 0.048 / 0.184 / **0.116** | 0.00123 | fit degenerate; use Option A |
| AN, unabated N₂O | 0.676 / 0.766 / **0.721** | 0.01277 | 0.739 / 0.0371 |
| AN, N₂O ≈ 90% abated | — / — / **0.329** | 0.00399 | 0.414 / 0.0158 |
| Primary aluminium | 0.069 / 0.364 / **0.216** | 0.00244 | 0.372 / 0.0087 |

For aluminium, the central value splits into np 0.128 (inert anodes) and no 0.108 (PFC / anode-effect control).

At USD 20, the central values imply intensity cuts of about 2–8% for most goods and about 23% for unabated AN.

**Cross-checks:**
- The IPCC Table 12.3 aggregate of process options at or below USD 100 is 15–17% of 2030 process emissions (β ≈ 0.0017).
- EU ETS ex-post studies find −7 to −16% at ≤ USD 50. These are total emissions dominated by combustion, so they are not transferable.
- The earlier Egypt value, β = 0.00104 (a(100) ≈ 10%), is a conservative lower bound.

### B.4 Egypt-specific points (qualitative; the same values are used for all countries)
- **DRI.** Concentrated DRI top-gas CO₂ is cheap to capture, but Egypt has no CO₂ transport or storage. This argues for the 2030 column in the near term.
- **Cement.** Cement dominates process emissions. Clinker substitution (LC3; limited slag and fly ash) is the main lever.
- **Nitric acid.** The status of N₂O abatement at the nitric acid plants (CDM-era projects at Abu Qir) decides between the unabated and abated AN rows. This item is shared with VERIFY item #2 in A.6.
- **Urea.** Under the CBAM rule, bound CO₂ is counted at the ammonia stage. Urea's response is therefore inherited from ammonia and should not be applied twice.

### B.5 Link between Appendices A and B (routing; recommendation for T1)
β applies to the categories that carry process carbon:

| Category | Response |
|---|---|
| **np** | product β (np column); aluminium uses the inert-anode part |
| **no** | product β (no column): AN N₂O and aluminium PFC |
| **fp** (DRI, BF-BOF, ammonia) | product β. Task D's scope includes reductant and feedstock CO₂, and for these goods it is the main process stream |
| **fc** | **not** β. The response is CPAT's efficiency margin (b_f) |

The kernel v0.9 scaffold applies β to np and no only. Without the fp routing, the process-type response of DRI and ammonia is lost.

**As applied in kernel v0.16 and rebuild v0.3:** np rows use the product central ER at $100 (DRI 0.3433, scrap 0.1810, BF-BOF 0.2803, clinker 0.3352); AN no uses the N₂O-weighted blend (3.5 × 0.7210 + 1.25 × 0.3292)/4.75 = 0.6179 at the EF workbook's 50% abatement share; aluminium uses the combined 0.2164 on both np and no (the 0.128/0.108 split is not additive); ammonia and urea get 0 (fp routing not implemented). ER_max = 1 (Option A), P* = 100 USD2019 = 122 USD2024 (deflated in kernel v0.16 and rebuild v0.3; v0.15/v0.2 used 100). Mapping: `TASK-D_ProcessHalfElasticities_DropIn_v0.2.md`.

### B.6 Caveats
1. The β values are calibration devices built from engineering costs, not estimated behavioural responses. The deployment factors d are analyst assumptions, and IPCC potentials carry ±25% uncertainty.
2. The constant-β form is only an approximation:
   - **Convex MACCs** (cement, steel, aluminium) are over-predicted below about USD 50 and under-predicted above USD 100.
   - **Concave MACCs** (N₂O) are under-predicted at low prices.

   Calibrating at USD 100 suits USD 50–150 scenarios. Below USD 30, use the 2030 column.
3. In v0.8 the kernel shared one ER table between fuel and process. The values here are for process emissions only.
4. The same values are used for Egypt and non-Egypt.

---

# Appendix C. File map

| Topic | File (relative to `egypt+mitigation\` unless stated) |
|---|---|
| Original results and review (read-only) | `Old\InitialResultsAndIssues\EgyptResultsInitial.docx`, `TechnicalNoteonCPATResults_expanded_v2.docx`, `MajorIssues.docx`, `CBAM_Process_MACC_Audit_Trail.docx`, `Methodological Note.txt` |
| Pseudocode of ad hoc calculations | `Old\TASK-2a_AdHocCalculations_Pseudocode_v0.1.md` |
| Table 2 rebuild (superseded by §5.0) | `Old\AdHocRebuild\AdHocCalculations_Rebuild_v0.3.xlsx`, `MethodologyNote_v0.3.md`, `build_adhoc_rebuild_v0_3.py`, `recalc_and_check_adhoc_v0_3.py`; comparison `Old\ResultsComparison_Table2_v0.3.md`; earlier results texts in `Old\Superseded\` |
| Final deliverables (v1.0) | Top level of `Egypt Final results\` and `egypt+mitigation\` (identical): kernel, `EGYPT_CarveOut_Table2_v1.0.docx`, `EgyptResultsInitial_UpdatedResults_v1.2_tracked.docx`, this document, `EGYPT_FinalCaveats_v1.0.docx`, `EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx` (Table 2 with live O). Markdown sources in `Old\`; earlier drafts in `Old\Superseded\` |
| Final Table 2 builders | `Old\AdHocRebuild\make_carveout_v0_3.py` (numbers); `Old\AdHocRebuild\make_results_page_v1_2.py` (tracked text) |
| Kernel (final) | `cpat_excel_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v1.0.xlsx`, `build_v1_0.py`; sheet `CarveOut_Table2` = final Table 2 (repo root path; copies in `Egypt Final results\` and `egypt+mitigation\`) |
| Task list and gaps | `EgyptTaskReference.md`; `instructions\instructions-egypt.yaml`; root `TODO.md` |
| Emission factors (App. A) | `Old\EmissionFactors\EGY_CBAM_EF_Methodology_v0.1.md`, `EGY_CBAM_EF_v0.1.xlsx`, `build_ef_v0_1.py`, `recalc_and_check.py` |
| Semi-elasticities (App. B) | `Old\ProcessEmissions_CarbonPrice_Response\ProcessEmissions_CarbonPriceResponse_Report.md` + `.xlsx`; `Old\TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`, `_v0.2.md` (mapping as applied) |
| Norms and log | root `NORMS.md`, `CAVEATS.md`, `README.md` |

# Appendix D. Glossary

| Term | Meaning |
|---|---|
| **fc / fp / np / no** | fuel combustion / fuel-based process (reductant, feedstock) / non-fuel process CO₂ / non-CO₂ process gases |
| **β** | process semi-elasticity, fraction of intensity per USD/t |
| **ER(P)** | emission-intensity reduction at price P |
| **s_int** | intensity share of the fuel response |
| **b_f** | fuel-intensity semi-elasticity |
| **κ** | priced share of industrial energy CO₂ in the CPAT run |
| **θ** | output-based rebate share |
| **φ** | fund share |
| **σ** | fund shadow price |
| **ε_Q** | output elasticity |
| **CBF** | CBAM phase-in factor |
| **P_EU** | EU allowance price |
| **NOPHASE / FULL / SCALED** | CBAM obligation conventions (§4.5) |
| **EG1–EG4** | CPAT Egypt runs |
| **1A–3C** | policy bundles |

*Version log:* **Final v1.0 (2026-10-04):** release of draft v1.3, proofread; kernel v1.0, carve-out v1.0, results text v1.1; 2026-10-06: O restated as CBAM-product embedded-intensity change (results text v1.2). Drafts: v1.0 (2026-10). First integrated methodology covering TASK-2a/2b, kernel v0.1–v0.13 and Tasks A–L, Task D, and Task EF. v1.1 (2026-10-02): final results: rebuild v0.2 and kernel v0.15 (Task D β and Egypt EF v0.1 loaded; Task M); §5.1 prototype results; §6–8, A.3, B.5 and App. C updated. v1.2 (2026-10-03): rebuild v0.3 and kernel v0.16 (P* deflated to 122; EG3 1/κ full-coverage approximation; 3C fund fixed point; block fuel CO₂ reallocation); §1, §5–8, B.5 and App. C updated. v1.3 (2026-10-03): §5.0 final Table 2 = CBAM carve-out v0.3 (O on FULL), implemented in kernel v0.17 sheet `CarveOut_Table2`.
