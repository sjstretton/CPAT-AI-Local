Key: ✅ done in v0.3, ◐ partly done, ✗ not started.

> The integrated methodology for the whole Egypt thread is **[`EGYPT_Methodology_v1.3.docx`](EGYPT_Methodology_v1.3.docx)** (also `.docx`). Its appendices cover the EF derivation (A) and the process semi-elasticities (B). This file stays the gap list.

## 1. Carbon pricing on non-fuel process emissions


**a) Four-way emission factor split: ◐**



- ✅ `Manual inputs` H:K already holds all four factors for 8 products:

- combustion

- reduction fuel (fuel used in the process)

- non-fuel process CO₂

- non-CO₂ process

- ◐ The calculation block merges them back into two (combustion + reduction; process + non-CO₂). They need to be kept as four separate rows, each with its own coverage switch. An upstream levy covers the first two; a downstream charge can cover all four.

- ◐ **EF derivation (2026): methodology and audit-trail workbook done, not yet applied to the kernel.** `EmissionFactors/EGY_CBAM_EF_Methodology_v0.1.md` + `EGY_CBAM_EF_v0.1.xlsx` (built by `build_ef_v0_1.py`, verified by `recalc_and_check.py`; 14 checks OK). Own-process EFs (fc / fp / np / no, CBAM conventions): DRI-EAF 0.178 / 0.393 / 0.038 / 0 = 0.609; scrap-EAF 0.045 / 0 / 0.044 / 0 = 0.089; clinker 0.314 / 0 / 0.537 / 0 = 0.851; ammonia 0.712 / 1.262 / 0 / 0 = 1.975; urea 0.112 / 0 / 0 / 0 (chain 1.238); AN 0.112 / 0 / 0 / 0 (chain incl. HNO₃ N₂O 1.953); aluminium 0.123 / 0 / 1.623 / 0.774 = 2.521. Differences from `Manual inputs` H30:K37: urea np uses the CBAM rule (bound CO₂ counted at the ammonia plant; switch `urea_conv` reproduces the −0.733 netting), AN keeps HNO₃ as a precursor (kernel folds N₂O into own), DRI-EAF rebuilt from a Midrex carbon balance (kernel EF-input columns S:V inconsistent with H:I). Egypt-specific inputs are Tier C/D with VERIFY flags (ammonia GJ/t, N₂O abatement share, Egyptalum PFC rates, kiln fuel mix). Adoption in the kernel is queued as `TODO.md` **T5**.



**b) Half-elasticities for process emissions: ◐**



- ✅ Inputs and the exponential formula exist (`Manual inputs` E40:E47).

- ✗ The values are just −ln(1 − reduction at $100)/100. That is a full elasticity, not a half, and it has no IPCC derivation. It needs an IPCC-based derivation, documented by product.

- ◐ **Task D (2026-10-02): IPCC-based derivation done, drop-in table ready, not yet applied to a kernel increment.** Spec and paste-ready values: `TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` (§2.3 maps onto the v0.9 rows 53–60 / `E50` layout); derivation report and live workbook in `ProcessEmissions_CarbonPrice_Response/`. Central ER at $100: DRI-EAF 34 %, scrap-EAF 18 %, BF-BOF 28 %, clinker 34 %, ammonia 30 %, urea 12 %, AN (unabated N₂O) 72 %, aluminium 22 %; convention kept as E = −ln(1 − F)/100. **Application queued as root `TODO.md` T1** (T2 = merge Stream 2, T3 = CBAM market data into Manual inputs).



**Process pricing: ◐**



- ◐ The formulas exist but are switched off: `Manual inputs` E21 = FALSE, so the process price is 0.

- ✗ The revenue rows have bugs:

- they use the fuel coverage flags instead of the process ones;

- they use pre-policy emissions instead of post-policy;

- they leave out revenue from fuel emissions.

- ✗ Fuel and process rows share the same output codes (`cpe.ind.*`).



## 2. Use-of-funds model: ✗


Only placeholder rows exist ("Total Shadow Price" and "Revenues Fund", both hard-coded 0). Still needed:



- fund size (a share of revenue);

- the fund turned into a shadow price acting on the efficiency term, with process emissions handled through the process semi-elasticity;

- the fund applied after the carbon price, not added to it.



## 3. Output-based rebating: ◐



- ✅ The kernel already has the mechanism: a shadow price with a share acting on efficiency (`shp`, `ssc`).

- ✗ There is no rebate scenario yet. It needs:

- a rebate per unit of output, equal to price × benchmark;

- only the net price reaching the usage/output term;

- the full price reaching efficiency and process intensity.



## 4. CBAM metrics: ✗


The inputs are there: EU default values, benchmarks, 2024 exports and the product price increase.


Still needed:



- embedded intensity per product (pre and post policy) and its % change, weighted by exports;

- coverage of CBAM-sector emissions;

- CBAM obligation = EU exports × (intensity − benchmark × CBAM phase-in factor) × (EU price − deductible domestic price, net of any rebate) and its change against baseline;

- new inputs for the EU ETS price path and the CBAM phase-in schedule.



## 5. Other gaps



1. ◐ **Emissions in the kernel** (energy CO₂ = Task F, v0.12; IPPU replacement = Task G, v0.13, report-only)**:** the kernel computes energy only, with no CO₂ or IPPU rows. It needs energy CO₂ by sector, and the block's process emissions must replace CPAT's proportional IPPU row so they aren't counted twice.

2. ◐ **Two measures of fuel emissions** (reconciled in v0.13 `IPPU_Industry` sections C1/C2, report-only; gap open)**:** product-level fuel emissions (production × emission factor) aren't linked to sector-level energy CO₂. They need reconciling or calibrating against each other.

3. ✗ **No output response:** production follows a fixed growth rate. The product price increase (rows 719–726) is calculated but never used. Output should respond to the net price.

4. ✗ **Egypt price paths:** the current path is the legacy one ($50 in 2030). It needs the Egypt paths: $20 flat from 2028, and $5 rising to $50 by 2034.

5. ✗ **More scenarios:** only baseline + one carbon tax scenario exist. The Egypt bundles each need their own coverage switches:

- upstream all fuels;

- downstream industry;

- process-only fee;

- free allocation / output-based rebate;

- fund.

6. ◐ **Links to main CPAT (outside the kernel; in-kernel Table 2 = Task M, v0.14 `Table2_Industry`, before T1/T3):** national GHG for the coverage %, total revenue, deaths avoided, recycling effects.
   - ◐ **TASK-2b rebuild (2026-10-02)** does this off-kernel for Table 2: `AdHocRebuild/AdHocCalculations_Rebuild_v0.1.xlsx` + `MethodologyNote_v0.1.md/.docx`. Composition K = ΔGHG − ΔIPPU + ΣER_p + Σemrq_proc + D_obr + F_fund on CPAT 2030 national totals; coverage with κ; revenue net of rebates/fund; deaths rescaled by energy CO₂. `Mode = PROTOTYPE` reproduces the v0.11 block exactly. 2030 K (Mt) 1A/2A/2B/3A/3B/3C = −31.6/−27.7/−29.3/−18.0/−12.8/−22.4 (original −41.6/−38.9/−41.0/−21.5/−18.1/−24.5). Open: κ(EG3) = 0.54 → re-run EG3 with full industry coverage; port the composition into the kernel as Task M.
   - ◐ **Results comparison (2026-10-02)** `AdHocRebuild/ResultsComparison_Table2_v0.1.md/.docx`: Table 2 of `EgyptResultsInitial.docx` vs rebuild vs v0.14 Task M, 2030, every Table 2 column + K decomposition. Task M K = −27.7/−25.7/−27.0/−9.7/−6.6/−17.3. Gaps to the rebuild: smaller kernel process response (placeholder β), industry-only scope = 4 kernel sectors (CPAT EG3 −8.55 Mt industrial fuel → kernel −2.06), +1.9 Mt data-vintage mix for All-sector bundles (`nk1 = indx − ek1` mixes kernel 75.4 with csv 89.0 Mt), 3C fund fixed at pre-abatement revenue → P = −0.37 $bn, J(3A–3C) 8.5% vs 13.8% (κ) vs 20% (Table 2). Candidate Task M fixes: scale the kernel-sector response to the run's full industry scope; use one vintage for `indx`; cap fund at post-abatement revenue.






24m ago











## You said: By half elasticity I mean semi-elasticity, ie the % change in emissions for a $1 change in carbon price. Could…

By half elasticity I mean semi-elasticity, ie the % change in emissions for a $1 change in carbon price. Could you split the above into a number of smaller tasks. so we can increment quickly. Just concisely describe them: Task A, Task B etc. No need to replicate the detailed instructions but can refer to them (e.g. do 2a and 2b)







21m ago







## Copilot said: Understood: "half-elasticity" means semi-elasticity. That corrects 1b. The E40:E47 values are valid semi-elasticities in the exponential form. They are only…

Thought for 11s



Understood: "half-elasticity" means semi-elasticity. That corrects 1b. The E40:E47 values are valid semi-elasticities in the exponential form. They are only missing a documented IPCC derivation.


The list below splits the work into small tasks. Each one should end with a new kernel version and a check row.



- **Task A – Separate output codes, fix revenue rows** (1, process pricing)

- Give fuel and process rows separate output codes.

- Fix the process revenue rows: use the process coverage flags and post-policy emissions, and add fuel revenue.

- **Task B – Four-way emission factor split** (1a). Carry the four emission factors as separate rows, each with its own coverage switch. Depends on A.

- **Task C – Turn on process carbon pricing** (1). Enable the switch per scenario and check that process emissions fall as expected. Depends on B.

- **Task D – Document process semi-elasticities** (1b). Derive the E40:E47 values from IPCC by product, and record sources and confidence. Independent.

- **Task E – Egypt price paths and scenario set** (5.4, 5.5). Add the $20 flat path from 2028 and the $5→$50 by 2034 path, plus scenario slots for each bundle with coverage switches. Independent.

- **Task F – Energy CO₂ in the kernel** (5.1). Calculate energy CO₂ by sector and fuel (emission factor × energy). Independent.

- **Task G – Replace the IPPU row and reconcile** (5.1, 5.2) — ☑ **done in v0.13** (`build_v0_13.py`; sheet `IPPU_Industry`, switch `Manual inputs` E85, fp-as-IPPU flags E88:E95). Report-only: kernel IPPU = block + non-block, not yet fed into the national GHG total (Task M). The reconciliation shows that block fuel CO₂ is above sector energy CO₂ (cem, nfm, mch in every year); this is open. See `CAVEATS.md`.

- Replace CPAT's proportional IPPU row with the block's process emissions.

- Reconcile product-level fuel emissions with sector energy CO₂.

- Depends on B and F.

- **Task H – Output response** (5.3). Production responds to the net product price increase. Depends on C.

- **Task I – Output-based rebating** (3). Net price goes to usage/output, and the full price goes to efficiency and process intensity, using the existing shadow-price mechanism. Depends on E and H.

- **Task J – Use-of-funds model** (2). Fund size, then conversion to a shadow price, then applied after the carbon price. Depends on C and E.

- **Task K – CBAM intensity and coverage metrics** (4, first part). Embedded intensity before and after policy, % change weighted by exports, and coverage. Depends on B and C.

- **Task L – CBAM obligations** (4, second part). Add the EU ETS price and CBAM phase-in inputs, and calculate obligations and their change, net of any rebate. Depends on K, and on I for the rebate scenarios.

- **Task M – Links to main CPAT** (5.6). National GHG, total revenue, deaths avoided and recycling effects, then assemble Table 2. Depends on G, K and L. - ◐ **built in v0.14** (`build_v0_14.py`; sheets `CPAT_National`, `Table2_Industry`; Check Task M D1861) before T1/T3: deltas composition with the kernel's own industry/IPPU response; 2030 K (Mt) 1A/2A/2B/3A/3B/3C = −27.7/−25.7/−27.1/−9.7/−6.6/−17.3. Re-run after T1/T3 and the EG3 full-coverage re-run. See `CAVEATS.md`.


•	Suggested order: E → A → B → C → K (first CBAM metrics) → D, H, L. 
•	Stream 2: F → I → J. 
•	Then the merge, then G and M.
•	Status (2026-10-02): mainline E, A, B, C, K, D-scaffold, H, L = v0.3-v0.11; Stream 2 F, I, J built on the v0.7 branch and **merged into v0.12** (TODO.md T2; caveats in `CAVEATS.md`); Task G = v0.13; Task M = v0.14; Task D values (T1) + Egypt EF v0.1 (T5) = v0.15 (2030 K −29.8/−25.8/−27.1/−11.8/−8.6/−23.9; AdHoc rebuild v0.2 on the same EFs/β). Next: T3, EG3 full-coverage re-run, then re-run M.
