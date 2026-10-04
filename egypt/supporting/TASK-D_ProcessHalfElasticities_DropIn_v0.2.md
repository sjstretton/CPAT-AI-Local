# TASK-D — IPCC-based process half-elasticities: drop-in table for the CPAT Industry Kernel

| | |
|---|---|
| Task | Task D (`egypt/instructions/instructions-egypt.yaml`; referenced from TASK-1 v0.8 notes as "IPCC semi-elasticities are pending") |
| Version | v0.1, 2026-10-02 (values final; not yet applied to a kernel version) |
| Status | **Ready to drop in.** No kernel file has been modified. |
| Target | `cpat_excel_new/standalone_working_version/CPAT_Industry_Kernel_Egypt_v0.8.xlsx` (or the latest increment), sheet `Manual inputs`, block `D38:F47` "Process Emissions Half Elasticities" |
| Derivation | `egypt/supporting/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse_Report.md` (+ `.docx`) — Appendix D is this table; workbook `ProcessEmissions_CarbonPriceResponse.xlsx`, sheet `CPAT_v0.8_Table` |
| Closes | `EgyptTaskReference.md` item 1b ("values … have no IPCC derivation") |

---

## 1. Kernel convention (verified from v0.8)

`'Manual inputs'!D39:F47` has columns **Process | Half Elasticity | ER at $100 (%)**.
The v0.8 numbers satisfy exactly

```
Half Elasticity  =  -LN(1 - ER_at_100) / 100        (positive, fraction per USD/tCO2e)
e.g. ER = 0.10  ->  0.0010536 ;  ER = 0.65  ->  0.0104982
```

The kernel then applies `exp(-HalfElasticity x price)` (process price `pptraj`) to the covered emission factor. This is the same iso-semi-elastic model as the report, β_iso = ln(1−a(100))/100, with the sign reversed (report: β in %/$; kernel: −β/100 per $). ER is stored as a **fraction** (0.10), displayed as %.

`Mitigation_Industry` reads the table twice: row 352–359 (`'Manual inputs'!E$40:F$47`, **fuel** ER, output `emrf`) and rows 363–370 (same cells, **process** ER, output `emrp`). See caveat 4.1.

## 2. Drop-in values (recommended = central estimate)

Paste into `'Manual inputs'!E40:F47`. Row labels are the existing `D40:D47` — do not change them.

| Row | D: Process | E: Half Elasticity | F: ER at $100 (%) | v0.8 E (now) | v0.8 F (now) |
|---|---|---|---|---|---|
| 40 | DRI-EAF steel | 0.004205 | 0.3433 | 0.001054 | 0.10 |
| 41 | Scrap-EAF steel | 0.001997 | 0.1810 | 0.000202 | 0.02 |
| 42 | BF-BOF steel reference | 0.003289 | 0.2803 | 0.000513 | 0.05 |
| 43 | Grey clinker dry-process | 0.004083 | 0.3352 | 0.000834 | 0.08 |
| 44 | Ammonia net | 0.003530 | 0.2974 | 0.001985 | 0.18 |
| 45 | Urea | 0.001231 | 0.1158 | 0 | 0 |
| 46 | AN | 0.012765 | 0.7210 | 0.010498 | 0.65 |
| 47 | Primary aluminium | 0.002439 | 0.2164 | 0.000834 | 0.08 |

Preferred implementation: make **F the only input** and set `E40 = -LN(1-F40)/100` (fill down to E47). This keeps the kernel's existing convention and lets a later task switch horizon by editing F alone.

### 2.1 Alternative horizons (same format)

| D: Process | 2030-horizon E | 2030 F | Long-run E | Long-run F |
|---|---|---|---|---|
| DRI-EAF steel | 0.001203 | 0.1133 | 0.008519 | 0.5734 |
| Scrap-EAF steel | 0.000999 | 0.0951 | 0.003105 | 0.2669 |
| BF-BOF steel reference | 0.001072 | 0.1016 | 0.006143 | 0.4589 |
| Grey clinker dry-process | 0.002138 | 0.1925 | 0.006499 | 0.4779 |
| Ammonia net | 0.001624 | 0.1499 | 0.005887 | 0.4449 |
| Urea | 0.000491 | 0.0479 | 0.002030 | 0.1838 |
| AN | 0.011283 | 0.6764 | 0.014509 | 0.7656 |
| Primary aluminium | 0.000716 | 0.0691 | 0.004522 | 0.3638 |

*2030-horizon* = deployment-constrained, calibrated to IPCC AR6 Table 12.3 2030 economic potentials; *long-run* = full capital-stock turnover at IPCC AR6 Table 11.3 technology costs; *central* = arithmetic mean (report §4–5, §11). Use 2030-horizon for results reported for ≤2030; central for a 2030–2045 policy horizon.

### 2.2 Conditional substitutions

| Case | Row | E | F |
|---|---|---|---|
| Egyptian nitric-acid plants already catalytically abated (~90 % N2O) | AN (46) | 0.003993 | 0.3292 |
| Embedded-NH3 CO2 of urea (`M35`) **not** priced (v0.8 default: own `np` floored at 0) | Urea (45) | 0 | 0 |

### 2.3 Mapping onto the v0.9 layout (added 2026-10-02 — supersedes §3 step 2 when the target is v0.9 or later)

v0.9 (`build_v0_9.py`) replaced the single table with a two-category scaffold in `Manual inputs` rows 53–60 (products in the same order as above), selector `E50` (`"IPCC"` → rows 53–60; `"ADHOC"` → rows 40–47, reproduces v0.8), and the form `ER(P) = ERmax·(1 − exp(−β·P))`. Columns: **np** (process CO2) `E` ERmax, `F` anchor P\*, `G` ER at P\*, `H` β (formula); **no** (N2O/PFC) `I` ERmax, `J` P\*, `K` ER at P\*, `L` β (formula); `Q`/`R` lever + source text; `S` confidence. Only `E:G`, `I:K`, `Q:S` and `E50` are written.

Option A (exact v0.8 convention, ERmax = 1, P\* = 100, ER\* = central ER at $100; unused category ERmax = 0):

| Row | Product | np E / F / G | no I / J / K | Note |
|---|---|---|---|---|
| 53 | DRI-EAF steel | 1 / 100 / 0.3433 | 0 / 100 / 0 | |
| 54 | Scrap-EAF steel | 1 / 100 / 0.1810 | 0 / 100 / 0 | |
| 55 | BF-BOF steel (reference) | 1 / 100 / 0.2803 | 0 / 100 / 0 | |
| 56 | Grey clinker | 1 / 100 / 0.3352 | 0 / 100 / 0 | |
| 57 | Ammonia (net) | 0 / 100 / 0 **or** 1 / 100 / 0.2974 | 0 / 100 / 0 | v0.9 puts SMR CO2 in `fp` (np = 0); decide whether the np β is routed to the feedstock line (see TODO.md T1) |
| 58 | Urea | 0 / 100 / 0 | 0 / 100 / 0 | np negative in v0.9; response inherits from ammonia (0.1158 chain value) — do not apply separately |
| 59 | Ammonium nitrate | 0 / 100 / 0 | 1 / 100 / 0.7210 (abated baseline: 0.3292) | |
| 60 | Primary aluminium | 1 / 100 / 0.1282 | 1 / 100 / 0.1078 | split of 0.2164: inert anodes (anode CO2) vs anode-effect/PFC control; option-level ER at $100, mean of 2030 & LR |

Option B (saturating form using ERmax properly; fitted to a(100) and a(200) on the `Results` sheet): ERmax = A, ER\* = a(100), P\* = 100 — DRI-EAF A 0.4079 β 0.01843; Scrap-EAF 0.3994 / 0.00604; BF-BOF 0.3874 / 0.01285; clinker 0.4325 / 0.01492; ammonia 0.4433 / 0.01112; AN unabated 0.7391 / 0.03712, abated 0.4142 / 0.01584; aluminium (combined) 0.3720 / 0.00872; urea fit degenerate (A > 1) → use Option A.

Full procedure, acceptance checks and bookkeeping: root `TODO.md`, task **T1**.

## 3. Step-by-step for the applying task (written for v0.8; for v0.9+ use §2.3 for step 2)

1. Copy the latest kernel to a new increment (`..._v0.9.xlsx` or next) and its builder (`build_v0_9.py` from `build_v0_8.py`); keep the version history in `standalone_working_version/Old/` per existing practice.
2. In `Manual inputs`: write F40:F47 from §2 (or §2.1), set `E40:E47 = -LN(1-F)/100`. Add a source note in the row-38 title or an adjacent comment cell: *"IPCC AR6 WGIII (Table 11.3, Table 12.3) via egypt/supporting/ProcessEmissions_CarbonPrice_Response, TASK-D v0.1, central estimate, USD2019"*.
3. Check the AN baseline: if `K36` (S1.no for AN) is changed from 0.97 to an abated value, apply the §2.2 AN row at the same time.
4. Decide the urea rule (§2.2): keep 0 unless `M35` (embedded NH3 CO2) enters the priced EF.
5. Price basis: the derivation is in **USD2019/tCO2e**; USD 100 (2019) ≈ USD 122 (2024). If the kernel's `pptraj` is in nominal or 2024 dollars, either deflate the path or rescale ER using `Results` sheet a(τ) values (τ = 20/50/100/150/200) in the derivation workbook.
6. Regression: re-run `Check`; expected effect is only on `emrp`/`emrf`, `cbint`, `cbintch`, `cbintchx`, revenue rows (`revp`, `revf`) and post-policy emissions (`emisnp`, `emisno`, …). Pre-policy rows and coverage (`cbcov`, `cbcovx`) must be unchanged.
7. Record the increment in `egypt/instructions/instructions-egypt.yaml` (TASK-1 notes, "Task D") and tick item 1b in `EgyptTaskReference.md`.

## 4. Caveats (must be read before applying)

1. **Shared fuel/process table.** v0.8 applies the same half elasticity to fuel-combustion ER (row 351) and process ER (row 362). The values above are derived for **process emissions only** (CBAM-scope non-combustion CO2 and N2O/PFC, plus reductant/feedstock CO2). Fuel-combustion responsiveness is governed elsewhere by the master elasticity table (`Data_Elast`); the applying task should either (a) add a separate fuel row set in `Manual inputs` (e.g. rows 49–57) and repoint row 352–359, or (b) consciously accept the process values as a proxy for fuel ER and say so.
2. **Scope vs EF split.** The kernel puts NG-reductant CO2 (DRI) and SMR feedstock CO2 (ammonia) in `fp`, so its `np` for these rows is ≈ 0. The report's "process" scope includes those streams. Because the half elasticity is applied to all four categories, the result is unaffected — but the response acts mainly through the `fp` column for these two products.
3. **AN baseline.** The AN row assumes an **unabated** N2O baseline (0.97 tCO2e/t, `K36`). Response is dominated by cheap secondary/tertiary catalysts (NACAG; IPCC AR4 §7.4.3.4). Verify Egyptian plant status (CDM-era projects) before finalising.
4. **Urea under CBAM.** CO2 bound into urea is counted, not deducted (Implementing Regulation (EU) 2023/1773 Annex III; Guidance 5c). Urea's own `np` is negative in the kernel and floored at 0; the 11.6 % applies to the embedded NH3-stage CO2.
5. **Same values for Egypt and non-Egypt** by instruction; Egypt-specific points are qualitative (report §9).
6. **Not elasticities from IPCC.** IPCC gives costs and potentials, not price elasticities; the 2030 vs long-run split rests on labelled deployment assumptions (`Parameters` sheet, yellow cells). Cross-checks: IPCC Table 12.3 aggregate process options ≤ USD 100 ≈ 15–17 % of 2030 process emissions (β ≈ −0.17 %/$); econometric EU ETS studies −7 to −16 % at ≤ USD 50.

## 5. Where everything lives

| Item | Path |
|---|---|
| This drop-in spec | `egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` |
| Report (md / docx), Appendix D = this table | `egypt/supporting/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse_Report.{md,docx}` |
| Derivation workbook (live formulas; sheet `CPAT_v0.8_Table` = paste-ready block B5:C12) | `egypt/supporting/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse.xlsx` |
| Target kernel (unchanged) | `cpat_excel_new/standalone_working_version/CPAT_Industry_Kernel_Egypt_v0.8.xlsx` (now in `Old/`) → `'Manual inputs'!D39:F47`; readers `Mitigation_Industry` rows 352–359, 363–370. **Latest:** `..._v0.9.xlsx` → `'Manual inputs'` rows 53–60 + `E50` (§2.3) |
| Queued application task (T1), merge (T2), inputs clean-up (T3) | root `TODO.md` |
| Earlier method note (β = −0.104 %/$ precedent) | `egypt/supporting/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md`; `InitialResultsAndIssues/Methodological Note.txt` |

---

## Addendum v0.2 (2026-10-02): mapping as applied in kernel v0.15 and AdHoc rebuild v0.2

Kernel `Manual inputs` (v0.9+ layout): selector E50 = IPCC; rows 53-60 per product, columns E/F/G = np ERmax / P* / ER*, I/J/K = no ERmax / P* / ER*; beta = -ln(1 - ER*/ERmax)/P*. P* = 100 (USD2019, not deflated). Fuel ER rows 40-47 unchanged.

| Row | Product | np ERmax | np ER* | no ERmax | no ER* | Note |
|---|---|---|---|---|---|---|
| 53 | DRI | 1 | 0.3433 | 0 | 0 | IPCC central |
| 54 | Scrap EAF | 1 | 0.1810 | 0 | 0 | |
| 55 | BF-BOF | 1 | 0.2803 | 0 | 0 | |
| 56 | Clinker | 1 | 0.3352 | 0 | 0 | |
| 57 | Ammonia | 0 | 0 | 0 | 0 | CCS lever acts on fp; routing not implemented |
| 58 | Urea | 0 | 0 | 0 | 0 | np = 0 under the CBAM rule |
| 59 | AN | 0 | 0 | 1 | 0.6179 | (3.5 x 0.7210 + 1.25 x 0.3292)/4.75, 50 % HNO3 abatement share (EF v0.1) |
| 60 | Aluminium | 1 | 0.2164 | 1 | 0.2164 | combined value on both; split 0.1282/0.1078 is not additive |

AdHoc rebuild v0.2 uses the same ER100 (AN 0.6179; 2030 0.5539, long-run 0.6818). See CAVEATS.md 2026-10-02 T1 + T5.
