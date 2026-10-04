# Egypt policy-options matrix (Table 2) – rebuilt ad hoc calculations: methodology note v0.4

Workbook: `AdHocCalculations_Rebuild_v0.4.xlsx` (builder `build_adhoc_rebuild_v0_4.py`, verification `recalc_and_check_adhoc_v0_4.py`). Change history is in `VersionNotes_AdHocRebuild.md`, not here.

Defaults: emission factors = Egypt CBAM EF v0.1 (`EFSet` = EGY_EF_V01; `EmissionFactors/EGY_CBAM_EF_v0.1.xlsx`, Products D:G; urea np = 0; AN keeps the integrated HNO3 N2O in its own `no`; AN process ER100 = N2O-weighted blend of the TASK-D unabated and abated rows at 50 % abatement, central 0.6179); IPCC beta anchor `PStar` = 122 USD2024; `KappaMode` = SCALE; `Conv` = FULL; `ThetaOther` = 1; fund shadow price sigma = 20 $/t.

All assumptions sit on **Inputs**; **PolicyMatrix** keeps the original layout and is fully live. One switch (`Mode`) selects **REBUILD** (coherent method, default) or **PROTOTYPE** (reproduces `CPAT_Industry_Kernel_Egypt_v0.11` exactly). Reporting year `Yr` = 2030, carbon price τ = CPAT `cptraj.2` of the bundle's scenario ($20 in 2030 for all six bundles).

## 1. Inputs (Inputs tab)

| Block | Content | Source |
|---|---|---|
| A Switches | `Mode`, `Conv` (CBAM convention: FULL / NOPHASE / SCALED), `Yr`, `SigmaEff` (fund shadow price sigma = 20 $/t), `BetaSet`, `BfScen`, `ThetaOther`, `IppuOther`, `KappaMode` | this note |
| B Parameters | eps_U = eps_F = -0.5 -> s_int = eps_F(1+eps_U)/(eps_U+eps_F(1+eps_U)) = 1/3; eps_Q = -0.5; P_EU = 100 $/t; `PStar` = 122 $/t; b_f (derived); CBAM phase-in factor | TechNote App. A; prototype v0.11; PStar from USD2019 100 deflated to USD2024 |
| C CPAT values | 22 CPAT `Outputs` codes × EG1–EG4, looked up live for `Yr` (GHG, IPPU, energy CO2, industry CO2, price, effective price, revenues, deaths) + 8 derived rows | `CPAT_Outputs` sheet (trimmed CPAT Outputs 2022–2041) |
| D Bundles | code → CPAT scenario, scope (ALL/IND), process flag, θ (OBR share), φ (fund share), τ | TechNote §Bundles |
| E Products | 8 CBAM products: Q0 (2024), g, EU exports X, price P, fuel factor F = fc+fp, process factor G = max(np,0)+max(no,0), ER100 -> beta = -ln(1-ER100)/PStar for IPCC sets; PROTOTYPE beta keeps /100 | activity / prices: prototype v0.11 Manual inputs; EFs: Egypt CBAM EF v0.1 (`EFSet`); IPCC beta set (TASK-D) |
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
  Conventions: FULL (default) CBF=0.485 (2030), S=1; NOPHASE (memo) CBF=1, S=1; SCALED CBF=S=0.485. This obligation is the kernel's deduction-based Task L measure. Row O of the final Table 2 is a different, intensity-only measure (EGYPT_Methodology section 4.5) and is not taken from this workbook.
- Block metrics: E_base = ΣQ_i^b(F_i+G_i)/1000 (= 62.42 Mt in 2030; 61.16 Mt with prototype EFs); cbcov = Σcovered/Σ(E_f+E_p); cbintch = ΣE_i/Σ(E_f+E_p) − 1; cbqch = Σemrq/E_base; emrt = Σemrq + ΣER_f + ΣER_p; cbobchu = ΣX_i·obl_i / ΣX_i·CBF·P_EU(F_i+G_i) − 1.

**National quantities (CPAT, scenario s of the bundle, year Yr)**: DeltaGHG, DeltaIPPU, DeltaEnergyCO2, DeltaIndCO2 = policy - baseline; kappa = min(1, (eff.cptraj/cptraj)*EnergyCO2_0/IndCO2_0) = share of industrial energy CO2 actually priced in the CPAT run (kappa(EG3) = 0.54; kappa = 1 for EG1/EG2). Under `KappaMode=SCALE`, EG3 bundles use scale factor s_k = 1/kappa to approximate a full-coverage industry run: DeltaIndCO2_adj = s_k*DeltaIndCO2; DeltaIPPU_adj = s_k*DeltaIPPU; DeltaGHG_adj = DeltaGHG + (s_k-1)(DeltaIndCO2 + DeltaIPPU); DeltaEnergyCO2_adj = DeltaEnergyCO2 + (s_k-1)DeltaIndCO2; IndCO2_1_adj = IndCO2_0 + DeltaIndCO2_adj. Coverage J uses kappa=1; D_obr uses w = E_f^base/IndCO2_0 and DeltaIndCO2_adj; F_fund uses IndCO2_1_adj. CPAT fuel-tax receipts are scaled by s_k. Deaths use CPAT deaths x (DeltaEnergyCO2_adj + D_obr + F_fund)/DeltaEnergyCO2. This is an approximation of a full-coverage EG3 run, pending a CPAT re-run. `AUTO` keeps the original partial-coverage (kappa) treatment; `ONE` assumes kappa=1 without scaling. b_f = s_int*ln(IndCO2_1/IndCO2_0)/tau on EG1 = -0.0025 per $/t.

**Table-2 metrics (sheet Results; PolicyMatrix column in brackets)**

- Coverage [J] = (E_f0 + flag*E_p^base)/GHG0, with E_f0 = EnergyCO2_0 (ALL), kappa*IndCO2_0 (IND/AUTO), or IndCO2_0 (IND/SCALE).
- Total reduction [K] = DeltaGHG_adj - DeltaIPPU_adj + IPPU_other + sum(ER_p) + sum(emrq_proc) + D_obr + F_fund, where adjusted deltas equal CPAT deltas except under `KappaMode=SCALE`, and
  IPPU_other = 0 (switch `IppuOther`; CPAT's IPPU scaling with industrial fuel use is removed, MajorIssues #17),
  D_obr = -(1-s_int)*w*DeltaIndCO2_adj if theta>0 (OBR neutralises the output share of CPAT's industrial fuel response; w = E_f^base/(kappa*IndCO2_0) in AUTO and E_f^base/IndCO2_0 under SCALE, unless `ThetaOther` = 1; with `ThetaOther` = 1 (default) w = 1, the rebate covers all covered industry and the output channel is removed everywhere),
  F_fund = [kappa*IndCO2_1 in AUTO, or IndCO2_1_adj in SCALE]*(exp(b_f*sigma_eff)-1) if phi>0 (fund buys fuel-intensity abatement outside the block).
- [L] = K/GHG₀. [M] = cbcov. [N] = cbintch. [O] = cbobchu (selected convention, FULL by default; AQ always shows FULL).
- Revenue [P] = (1-phi)*(P_gross - rebates), P_gross = CPAT carbon-tax receipts on fuels (six fuels, post-response; scaled by 1/kappa under SCALE) + sum(rev_p)/1000; rebates = sum(rebate_i)/1000 (+ tau*(covered IndCO2_1 - sum(E_f,post))/1000 if `ThetaOther` = 1). Fund budget = phi*(P_gross - rebates); outlay upper bound = sigma*abs(sum(ER_f)+sum(ER_p)+F_fund)/1000.
- Deaths [Q] = CPAT deaths avoided(s) x (DeltaEnergyCO2_adj + D_obr + F_fund)/DeltaEnergyCO2 for IND bundles (energy CO2 only; SCALE first scales deaths by DeltaEnergyCO2_adj/DeltaEnergyCO2); [R] = Q/baseline deaths.
- [T] = emrt/E_base; [U] = cbqch; [AR] = CPAT Delta net new revenue(s) - (P_gross - P), using the scaled P_gross/P approximation under SCALE.
- Decomposition columns AF-AM on PolicyMatrix: DeltaGHG_adj, -DeltaIPPU_adj, IPPU_other, sum(ER_p), sum(emrq_proc), D_obr, F_fund, check (= 0).

## 3. Results, 2030 (Mode = REBUILD, Conv = FULL, EFSet = EGY_EF_V01, KappaMode = SCALE, ThetaOther = 1)

The EG3 industry scenarios (3A/3B/3C) approximate a full-coverage EG3 run with `KappaMode` = SCALE (1/kappa scaling; a linear approximation, not a CPAT re-run). O is shown for the default FULL convention and, in parentheses, NOPHASE.

| Metric | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---:|---:|---:|---:|---:|---:|
| J coverage, % GHG | 63.2 | 57.3 | 57.3 | 20.8 | 20.8 | 20.8 |
| K reduction, Mt | -31.35 | -27.82 | -29.34 | -25.07 | -12.31 | -30.60 |
| L, % of GHG | -5.28 | -4.68 | -4.94 | -4.22 | -2.07 | -5.15 |
| M CBAM coverage, % | 100.0 | 44.2 | 44.2 | 100.0 | 100.0 | 100.0 |
| N intensity, % | -5.79 | -2.15 | -2.15 | -5.79 | -5.80 | -11.24 |
| O obligation per unit, % FULL (NOPHASE) | -44.42 (-24.34) | -23.12 (-12.53) | -23.12 (-12.53) | -44.42 (-24.34) | -5.42 (-5.42) | -47.41 (-28.41) |
| P net revenue, $bn | 6.84 | 6.23 | 6.19 | 2.34 | 0.20 | 0.00 |
| P gross revenue, $bn | 6.84 | 6.23 | 6.19 | 2.34 | 2.38 | 2.30 |
| Rebates, $bn | 0.00 | 0.00 | 0.00 | 0.00 | 2.18 | 0.00 |
| Q deaths avoided | 1564 | 1564 | 1631 | 850 | 412 | 997 |
| T block emissions, % | -11.6 | -4.7 | -4.7 | -11.6 | -5.8 | -16.7 |
| U block output, % | -6.1 | -2.6 | -2.6 | -6.1 | 0.0 | -6.1 |
| AR Dnet revenue, $bn | 10.43 | 10.43 | 10.62 | 2.69 | 0.51 | 0.39 |

K decomposition (PolicyMatrix AF-AM, Mt):

| Bundle | AF DeltaGHG_adj | AG -DeltaIPPU_adj | AH IPPU_other | AI ER_p | AJ emrq_proc | AK D_obr | AL F_fund | AM check |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1A | -38.88 | 11.96 | 0.00 | -2.13 | -2.30 | 0.00 | 0.00 | 0.00 |
| 2A | -38.88 | 11.96 | 0.00 | 0.00 | -0.90 | 0.00 | 0.00 | 0.00 |
| 2B | -41.00 | 12.56 | 0.00 | 0.00 | -0.90 | 0.00 | 0.00 | 0.00 |
| 3A | -36.02 | 15.37 | 0.00 | -2.13 | -2.30 | 0.00 | 0.00 | 0.00 |
| 3B | -36.02 | 15.37 | 0.00 | -2.28 | 0.00 | 10.61 | 0.00 | 0.00 |
| 3C | -36.02 | 15.37 | 0.00 | -4.11 | -2.30 | 0.00 | -3.56 | 0.00 |

3B: with `ThetaOther` = 1 the rebate (2.18 $bn: 1.25 to CBAM producers, 0.94 to the rest of covered industry) offsets almost all of the gross revenue, so net P is about 0, and D_obr removes the output channel for all covered industry.

Verification: `Mode = PROTOTYPE` reproduces all 22 block metrics x 6 bundles of kernel v0.11 to < 1e-7 for FULL and NOPHASE (132/132 values for each convention; `ThetaOther` is forced to 0 in PROTOTYPE mode). REBUILD matches an independent Python re-implementation (588/588 values), the Checks sheet passes, and the workbook has no Excel error cells (report `recalc_and_check_adhoc_v0_4_report.txt`).

## 4. Differences

**(a) vs the original AdHocCalculations.xlsb**

1. One base: every % uses CPAT 2030 baseline total GHG (594.2 Mt); the original mixed 2026/2030 and three denominators (#4, #11).
2. Coverage computed, not typed; κ makes the partial industry coverage of the EG3 run explicit (J_int memo = 20.7% at κ = 1) (#12, #13).
3. CBAM base bottom-up (61.2 Mt from eight products) instead of 53.6 Mt (#16); process response via β and the output channel, CPAT's proportional IPPU scaling removed (#14, #17).
4. 1A on EG1 (was EG2-based) (#3); 3B from EG3 with an explicit OBR correction instead of −13.592·(2/3)/0.5 (#9, #15); output change per bundle, not 3B's −8.3% for all (#18).
5. Revenue = CPAT fuel receipts (post-response) + block process revenue, net of rebates/fund; 3B rebates all covered industry (`ThetaOther` = 1), so its net revenue is about 0 (#10).
6. Deaths from the bundle's own scenario, rescaled by energy CO2 only (#2, #19); AR from the bundle's own scenario (#6); price start 2028 (#5); nothing hard-typed (#7); EG4 excluded (#8).
   Net effect: K is 15–30% smaller than the original for the economy-wide bundles (the original's K included CPAT's IPPU scaling and an untraceable process term) and 10–30% smaller for the industry bundles.

**(b) vs the prototype kernel v0.11**

1. Fuel-intensity channel x_f = exp(b_f(τ+σ)) (prototype: fuel intensity fixed) → N, T, O larger in magnitude.
2. IPCC-based β set (prototype set available via `BetaSet`) → ER_p 4× larger.
3. Fund (3C) modelled as shadow price σ = 20 $/t on both intensity channels (prototype: fund inactive) → 3C ≠ 3A.
4. National totals, coverage, revenue, deaths and AR from CPAT (outside the prototype's scope); OBR rebates deducted from revenue.
5. FULL as the default convention for O, the same as the prototype headline; NOPHASE is shown as a memo.
6. Kernel rebate and fund: the kernel caps the 3B rebate by sector shares and activates the 3C fund (shadow price about 150 $/t), whereas this rebuild rebates all covered industry in 3B and uses sigma = 20 $/t in 3C. The kernel's own Table 2 is the sheet `Table2_Industry`; the comparison with the rebuild is in `ResultsComparison_Table2_v0.4.md`.

## 5. Format changes vs the original PolicyMatrix

- Assumptions moved to **Inputs**; new sheets CPAT_Outputs, CBAM_Products, Results, Comparison, Issues resolved, Checks; GHG tab not rebuilt.
- Columns **AF–AQ redefined** (yellow headers): legacy half-elasticity block replaced by the K decomposition (AF–AM), export-weighted intensity change (AN), gross revenue (AO), rebates (AP), O under FULL (AQ).
- Row 4 mode indicator; C3 is a formula; G7 label corrected ("$20 flat from 2028").
- Rows 14–22 (non-modelled bundles) copied verbatim and greyed, not recomputed.
- Trajectory rows 26–29 rebuilt as contiguous years 2027–2034 in F–M, live, plus a CBAM phase-in row.
- Columns B, D, E hidden as in the original; widths and header styling preserved.

## 6. Open flags for review

1. kappa(EG3) = 0.54: `KappaMode` = SCALE approximates full coverage; a CPAT EG3 re-run with all industrial energy CO2 priced is still pending. After a true full-coverage run, set `KappaMode` = ONE or retire SCALE.
2. Non-CBAM IPPU (43 % of IPPU) is assumed unresponsive to a fuel-only price (`IppuOther`).
3. Deaths rescaling for 3B/3C is proportional to energy CO2 (approximation).
4. The beta set (IPCC central), `PStar` = 122 and sigma = 20 $/t are judgements; the fund outlay bound stays below the 3C budget.
5. 3B rebates all covered industry (`ThetaOther` = 1); `ThetaOther` = 0 (CBAM producers only) remains available as a switch.
6. O here is the deduction-based obligation (FULL default). The final Table 2 row O is the intensity-only measure and is calculated elsewhere.
