# Egypt policy-options matrix (Table 2) – rebuilt ad hoc calculations: methodology note v0.1

Workbook: `AdHocCalculations_Rebuild_v0.1.xlsx` (builder `build_adhoc_rebuild_v0_1.py`, verification `recalc_and_check_adhoc.py`).
All assumptions sit on **Inputs**; **PolicyMatrix** keeps the original layout and is fully live. One switch (`Mode`) selects **REBUILD** (coherent method, default) or **PROTOTYPE** (reproduces `CPAT_Industry_Kernel_Egypt_v0.11` exactly). Reporting year `Yr` = 2030, carbon price τ = CPAT `cptraj.2` of the bundle's scenario ($20 in 2030 for all six bundles).

## 1. Inputs (Inputs tab)

| Block | Content | Source |
|---|---|---|
| A Switches | `Mode`, `Conv` (CBAM convention: NOPHASE / FULL / SCALED), `Yr`, `SigmaEff` (fund shadow price σ = 20 $/t), `BetaSet`, `BfScen`, `ThetaOther`, `IppuOther`, `KappaMode` | this note |
| B Parameters | ε_U = ε_F = −0.5 → s_int = ε_F(1+ε_U)/(ε_U+ε_F(1+ε_U)) = 1/3; ε_Q = −0.5; P_EU = 100 $/t; b_f (derived); CBAM phase-in factor | TechNote App. A; prototype v0.11 |
| C CPAT values | 22 CPAT `Outputs` codes × EG1–EG4, looked up live for `Yr` (GHG, IPPU, energy CO2, industry CO2, price, effective price, revenues, deaths) + 8 derived rows | `CPAT_Outputs` sheet (trimmed CPAT Outputs 2022–2041) |
| D Bundles | code → CPAT scenario, scope (ALL/IND), process flag, θ (OBR share), φ (fund share), τ | TechNote §Bundles |
| E Products | 8 CBAM products: Q₀ (2024), g, EU exports X, price P, fuel factor F = fc+fp, process factor G = max(np,0)+max(no,0), ER100 → β = −ln(1−ER100)/100 | prototype v0.11 Manual inputs; IPCC β set (TASK‑D) |
| F Year vectors | CBAM phase-in, flat $20 path, CPAT EG3 ramp (live) | EU CBAM; CPAT |

Bundle mapping: 1A→EG1 (ALL, process priced), 2A→EG1 (ALL, fuels only), 2B→EG2 (ALL, fuels only, household recycling), 3A→EG3 (IND, process priced), 3B→EG3 + θ=1 (output-based rebate), 3C→EG3 + φ=1 (abatement fund).

## 2. Core equations

**CBAM block (per product i, sheet CBAM_Products; prototype v0.11 equations)**

- Prices: τ_p = τ·flag; OBR rate = θτ; fund price σ_eff = φσ (0 in PROTOTYPE).
- Cost per tonne: k_f = τF_i; k_p = τ_p G_i; rebate m_i = min(θτ,τ)F_i + min(θτ,τ_p)·flag·G_i; Δp_i = (k_f+k_p−m_i)/P_i.
- Output: Q_i^b = Q₀(1+g)^(Yr−2024); Q_i = Q_i^b(1+Δp_i)^ε_Q.
- Emissions at baseline intensity: E_f = Q_iF_i/1000, E_p = Q_iG_i/1000 (Mt).
- Intensity responses: ER_f = E_f(x_f−1) with x_f = exp(b_f(τ+σ_eff)) [REBUILD; x_f = 1 in PROTOTYPE]; ER_p = −E_p(1−exp(−β_i(τ_p+σ_eff))).
- Post-response emissions: E_i = E_f+ER_f+E_p+ER_p; output-channel reduction emrq_i = (E_f+E_p)(1−(1+Δp_i)^(−ε_Q)) (process part uses E_p only).
- Revenue: rev_i = (E_f+ER_f)τ + (E_p·1[G_i>0]+ER_p)τ_p ($m); rebate_i = m_iQ_i/1000.
- CBAM: intensity EI_i = 1000E_i/Q_i; deductible carbon price d_i = 1000rev_i/Q_i − m_i; obligation per tonne obl_i = max(0, CBF·P_EU·EI_i − S·max(0,d_i)); cbobl = ΣX_i(Q_i/Q₀)obl_i/1000; cbobl₀ = ΣX_i(1+g)^t·CBF·P_EU(F_i+G_i)/1000.
  Conventions: NOPHASE (default) CBF=1, S=1; FULL CBF=0.485 (2030), S=1; SCALED CBF=S=0.485.
- Block metrics: E_base = ΣQ_i^b(F_i+G_i)/1000 (= 61.16 Mt in 2030); cbcov = Σcovered/Σ(E_f+E_p); cbintch = ΣE_i/Σ(E_f+E_p) − 1; cbqch = Σemrq/E_base; emrt = Σemrq + ΣER_f + ΣER_p; cbobchu = ΣX_i·obl_i / ΣX_i·CBF·P_EU(F_i+G_i) − 1.

**National quantities (CPAT, scenario s of the bundle, year Yr)**: ΔGHG, ΔIPPU, ΔEnergyCO2, ΔIndCO2 = policy − baseline; κ = min(1, (eff.cptraj/cptraj)·EnergyCO2₀/IndCO2₀) = share of industrial energy CO2 actually priced in the CPAT run (κ(EG3) = 0.54; κ = 1 for EG1/EG2); b_f = s_int·ln(IndCO2₁/IndCO2₀)/τ on EG1 = −0.0025 per $/t.

**Table-2 metrics (sheet Results; PolicyMatrix column in brackets)**

- Coverage [J] = (E_f⁰ + flag·E_p^base)/GHG₀, with E_f⁰ = EnergyCO2₀ (ALL) or κ·IndCO2₀ (IND).
- Total reduction [K] = ΔGHG − ΔIPPU + IPPU_other + ΣER_p + Σemrq_proc + D_obr + F_fund, where
  IPPU_other = 0 (switch `IppuOther`; CPAT's IPPU scaling with industrial fuel use is removed, MajorIssues #17),
  D_obr = −(1−s_int)·w·ΔIndCO2 if θ>0 (OBR neutralises the output share of CPAT's industrial fuel response; w = E_f^base/(κ·IndCO2₀) = 0.57 for EG3 unless `ThetaOther` = 1),
  F_fund = κ·IndCO2₁(exp(b_fσ_eff)−1) if φ>0 (fund buys fuel-intensity abatement outside the block).
- [L] = K/GHG₀. [M] = cbcov. [N] = cbintch. [O] = cbobchu (selected convention; FULL shown in AQ).
- Revenue [P] = (1−φ)·(P_gross − rebates), P_gross = CPAT carbon-tax receipts on fuels (six fuels, post-response) + Σrev_p/1000; rebates = Σrebate_i/1000 (+ τ(κ·IndCO2₁ − ΣE_f,post)/1000 if `ThetaOther` = 1). Fund budget = φ·(P_gross − rebates); outlay upper bound = σ|ΣER_f+ΣER_p+F_fund|/1000 (3C: 0.19 vs budget 1.47 $bn).
- Deaths [Q] = CPAT deaths avoided(s) × (ΔEnergyCO2 + D_obr + F_fund)/ΔEnergyCO2 for IND bundles (energy CO2 only); [R] = Q/baseline deaths.
- [T] = emrt/E_base; [U] = cbqch; [AR] = CPAT Δnet new revenue(s) − (P_gross − P).
- Decomposition columns AF–AM on PolicyMatrix: ΔGHG, −ΔIPPU, IPPU_other, ΣER_p, Σemrq_proc, D_obr, F_fund, check (= 0).

## 3. Results, 2030 (Mode = REBUILD, Conv = NOPHASE)

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| J coverage, % GHG — rebuilt / original / Table 2 | 63 / 72 / 72 | 57 / 65 / 65 | 57 / 65 / 65 | 14 / 24 / 20 | 14 / 24 / 20 | 14 / 24 / 20 |
| K reduction, Mt — rebuilt / original | −31.6 / −41.6 | −27.7 / −38.9 | −29.3 / −41.0 | −18.0 / −21.5 | −12.8 / −18.1 | −22.4 / −24.5 |
| L, % of GHG — rebuilt / original | −5.3 / −8.5 | −4.7 / −8.0 | −4.9 / −8.4 | −3.0 / −4.4 | −2.1 / −3.7 | −3.8 / −5.0 |
| M CBAM coverage — rebuilt / original / proto | 100 / 100 / 100 | 44.5 / 44.5 / 44.5 | 44.5 / 44.5 / 44.5 | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 100 / 100 |
| N intensity, % — rebuilt / original / proto | −6.6 / −7.6 / −1.1 | −2.2 / −5.5 / 0 | −2.2 / −5.5 / 0 | −6.6 / −7.6 / −1.1 | −6.6 / −7.6 / −1.1 | −12.7 / −13.1 / −1.1 |
| O obligation per unit, % — rebuilt / original / proto NOPHASE (FULL) | −24.9 / −26.1 / −21.1 (−42.1) | −13.1 / −13.9 / −10.9 (−22.6) | −13.1 / −13.9 / −10.9 (−22.6) | −24.9 / −26.1 / −21.1 (−42.1) | −6.2 / −7.6 / −1.4 (−1.4) | −29.5 / −30.4 / −21.1 (−42.1) |
| P revenue, $bn — rebuilt / original / Table 2 | 6.81 / 5.77 / 5.8 | 6.23 / 5.18 / 5.2 | 6.19 / 5.18 / 5.2 | 1.51 / 2.38 / 1.1 | 0.33 / 0 / 0 | 0 / 0 / 0 |
| Q deaths avoided — rebuilt / original | 1564 / 1656 | 1564 / 1564 | 1631 / 1631 | 546 / 546 | 412 / 345 | 633 / 621 |
| T block emissions, % — rebuilt / original / proto | −12.0 / −15.3 / −6.8 | −4.5 / −13.4 / −2.4 | −4.5 / −13.4 / −2.4 | −12.0 / −18.1 / −6.8 | −6.6 / −15.3 / −1.1 | −17.8 / −20.6 / −6.8 |
| U block output, % — rebuilt / original / proto | −5.8 / −8.3 / −5.8 | −2.4 / −8.3 / −2.4 | −2.4 / −8.3 / −2.4 | −5.8 / −11.4 / −5.8 | 0 / −8.3 / 0 | −5.8 / −8.7 / −5.8 |
| AR Δnet revenue, $bn — rebuilt / original | 10.43 / 10.62 | 10.43 / 10.62 | 10.62 / 10.62 | 2.69 / 2.69 | 1.47 / 0 | 1.22 / – |

Verification: `Mode = PROTOTYPE` reproduces all 21 block metrics × 6 bundles of v0.11 to < 1e‑7 for FULL and NOPHASE (Comparison §2, Checks); REBUILD matches an independent Python re-implementation (534/534 values).

## 4. Differences

**(a) vs the original AdHocCalculations.xlsb**

1. One base: every % uses CPAT 2030 baseline total GHG (594.2 Mt); the original mixed 2026/2030 and three denominators (#4, #11).
2. Coverage computed, not typed; κ makes the partial industry coverage of the EG3 run explicit (J_int memo = 20.7% at κ = 1) (#12, #13).
3. CBAM base bottom-up (61.2 Mt from eight products) instead of 53.6 Mt (#16); process response via β and the output channel, CPAT's proportional IPPU scaling removed (#14, #17).
4. 1A on EG1 (was EG2-based) (#3); 3B from EG3 with an explicit OBR correction instead of −13.592·(2/3)/0.5 (#9, #15); output change per bundle, not 3B's −8.3% for all (#18).
5. Revenue = CPAT fuel receipts (post-response) + block process revenue, net of rebates/fund; 3B now raises 0.33 $bn because only CBAM producers are rebated (`ThetaOther` = 0) (#10).
6. Deaths from the bundle's own scenario, rescaled by energy CO2 only (#2, #19); AR from the bundle's own scenario (#6); price start 2028 (#5); nothing hard-typed (#7); EG4 excluded (#8).
   Net effect: K is 15–30% smaller than the original for the economy-wide bundles (the original's K included CPAT's IPPU scaling and an untraceable process term) and 10–30% smaller for the industry bundles.

**(b) vs the prototype kernel v0.11**

1. Fuel-intensity channel x_f = exp(b_f(τ+σ)) (prototype: fuel intensity fixed) → N, T, O larger in magnitude.
2. IPCC-based β set (prototype set available via `BetaSet`) → ER_p 4× larger.
3. Fund (3C) modelled as shadow price σ = 20 $/t on both intensity channels (prototype: fund inactive) → 3C ≠ 3A.
4. National totals, coverage, revenue, deaths and AR from CPAT (outside the prototype's scope); OBR rebates deducted from revenue.
5. NOPHASE as default convention for O (prototype headline uses FULL; both shown).
6. Kernel v0.13/v0.14 (after this note's PROTOTYPE calibration on v0.11): 3B rebate capped by sector shares (0.97 vs 1.22 $bn), 3C fund active (shadow price 150 $/t), and Task M adds the prototype's own Table 2 (`Table2_Industry`). Full comparison of Table 2 vs this rebuild vs v0.14: `ResultsComparison_Table2_v0.1.md`.

## 5. Format changes vs the original PolicyMatrix

- Assumptions moved to **Inputs**; new sheets CPAT_Outputs, CBAM_Products, Results, Comparison, Issues resolved, Checks; GHG tab not rebuilt.
- Columns **AF–AQ redefined** (yellow headers): legacy half-elasticity block replaced by the K decomposition (AF–AM), export-weighted intensity change (AN), gross revenue (AO), rebates (AP), O under FULL (AQ).
- Row 4 mode indicator; C3 is a formula; G7 label corrected ("$20 flat from 2028").
- Rows 14–22 (non-modelled bundles) copied verbatim and greyed, not recomputed.
- Trajectory rows 26–29 rebuilt as contiguous years 2027–2034 in F–M, live, plus a CBAM phase-in row.
- Columns B, D, E hidden as in the original; widths and header styling preserved.

## 6. Open flags for review

1. κ(EG3) = 0.54: the industry CPAT run prices only part of industrial energy CO2 (aluminium, other manufacturing excluded) — re-run EG3 with full coverage, then set `KappaMode` = ONE.
2. 3B revenue depends on `ThetaOther` (0: CBAM producers rebated only, P = 0.33 $bn; 1: all covered industry rebated, P ≈ 0).
3. Non-CBAM IPPU (43% of IPPU) assumed unresponsive to a fuel-only price (`IppuOther`).
4. Deaths rescaling for 3B/3C is proportional to energy CO2 (approximation).
5. β set (IPCC central) and σ = 20 $/t are judgements; fund outlay bound (0.19 $bn) is far below the 3C budget (1.47 $bn).
6. O convention: NOPHASE default vs FULL; both reported.
