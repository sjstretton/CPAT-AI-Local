# CAVEATS - log of completed tasks

Append-only log of every completed task in this repo: what was asked, what went in, what came out, and what the next person must know before building on it. One entry per completed task (or per workbook version increment). **Newest entry at the bottom.** Never edit or delete an earlier entry; if a caveat is later resolved, add a new entry that says so and names the entry it resolves.

The rule that every finished task gets an entry here, and the other bookkeeping that goes with it (workbook version log, task inventory, `TODO.md`), is in [`NORMS.md` section 6](NORMS.md#6-task-completion-caveats-log-and-bookkeeping). Repo map and key documents: [`README.md`](README.md).

## Entry template

Copy the block below to the end of the file and fill it in. Keep it short; point to the task spec, report or yaml notes for detail rather than repeating them.

```markdown
## YYYY-MM-DD - <task id / short name> (<version or increment, if any>)
- **Task:** what was asked and what was done (one or two sentences).
- **Inputs:** files, sheets/ranges, data sources, specs and prior versions used.
- **Outputs:** files created or changed (paths), version numbers, documents updated.
- **Caveats:** placeholders, assumptions, known gaps, deferred items, regression differences that were explained rather than zero, decisions still open. Write "None" only if there genuinely are none.
```

## Caveats recorded before this log existed

Earlier work was logged in the task documents themselves; they remain the detailed record:

- Kernel increments v0.3-v0.11 (Tasks E, A, B, C, K, D-scaffold, H, L): `notes` under `TASK-1` in [`instructions/instructions-egypt.yaml`](instructions/instructions-egypt.yaml) and each workbook's `Settings` version log.
- Process semi-elasticities (Task D): [`egypt+mitigation/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`](egypt+mitigation/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md) section 4.
- Gap list for the Egypt kernel: [`egypt+mitigation/EgyptTaskReference.md`](egypt+mitigation/EgyptTaskReference.md).
- LAMBDA/VBA distribution workbook: [`cpat_excel_new/distribution/LESSONS_LEARNED.md`](cpat_excel_new/distribution/LESSONS_LEARNED.md); Python Distribution module gaps vs Excel: [`cpat_excel_new/distribution/README.md`](cpat_excel_new/distribution/README.md).

---

## Entries

## 2026-10-02 - TASK-D: IPCC-based process semi-elasticities (values ready, not applied)
- **Task:** Derive documented, IPCC-based process-emission semi-elasticities ("half-elasticities") for the eight CBAM products of the industry kernel, to replace the undocumented v0.8 `Manual inputs` E40:F47 values. Values are final; applying them to a kernel increment is queued as `TODO.md` T1.
- **Inputs:** IPCC AR6 WGIII Ch. 11 (Table 11.3 technology costs) and Ch. 12 (Table 12.3 2030 potentials) in `_research/`; CBAM Implementing Regulation (EU) 2023/1773 and guidance documents in `_research/`; kernel convention from `CPAT_Industry_Kernel_Egypt_v0.8.xlsx` (`Manual inputs` D38:F47) and the v0.9 layout (`Manual inputs` rows 53-60, selector `E50`); earlier method note in `egypt+mitigation/TASK-2a_AdHocCalculations_Pseudocode_v0.1.md` and `egypt+mitigation/InitialResultsAndIssues/Methodological Note.txt`.
- **Outputs:** `egypt+mitigation/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` (drop-in spec, sections 2.3 maps onto v0.9+); `egypt+mitigation/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse_Report.md` and `.docx` (derivation report, Appendix D = drop-in table); `egypt+mitigation/ProcessEmissions_CarbonPrice_Response/ProcessEmissions_CarbonPriceResponse.xlsx` (live derivation, sheet `CPAT_v0.8_Table`); `TASK-D` entry in `instructions/instructions-egypt.yaml`; `EgyptTaskReference.md` item 1b marked partly done; `TODO.md` T1.
- **Caveats:** (1) Not applied: v0.9-v0.11 rows 53-60 hold placeholder anchors, so process response in those versions still equals v0.8. (2) Values are for process emissions only; v0.8 used one table for both fuel ER (rows 352-359) and process ER (363-370) - the applying task must separate them or accept the proxy explicitly. (3) The kernel books DRI reductant and SMR feedstock CO2 as `fp`, so `np` is ~0 for DRI-EAF and ammonia; the response then acts through `fp`. (4) AN assumes an unabated N2O baseline (`K36` = 0.97); use 0.3292 instead of 0.7210 if Egyptian nitric-acid plants are already abated. (5) Urea's own `np` is negative and floored at 0; the 11.6 % applies to embedded NH3 CO2 and is not applied separately. (6) Same values used for Egypt and non-Egypt. (7) IPCC supplies costs and potentials, not elasticities; the 2030 vs long-run split rests on labelled deployment assumptions. (8) USD2019 basis (100 USD2019 ~ 122 USD2024) versus the kernel's nominal/2024 price path - deflate or note when applying.

## 2026-10-02 - Docs: task-completion norm, caveats log and cross-references
- **Task:** Make the task-completion process explicit: every finished task is appended to this file (task, inputs, outputs, caveats), and `README.md`/`NORMS.md` reference the norms, processes and key documents.
- **Inputs:** `README.md`, `NORMS.md`, `TODO.md` (per-task conventions), `instructions/instructions-egypt.yaml`, `instructions/context-egypt.md`, `egypt+mitigation/EgyptTaskReference.md`, `egypt+mitigation/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`, `cpat_excel_new/distribution/*.md`, current folder listing.
- **Outputs:** `CAVEATS.md` (new, this file); `NORMS.md` (new "Key documents" table and section 6 "Task completion: caveats log and bookkeeping"; legacy workbook path corrected to `cpat_excel_original\`); `README.md` (layout block, "When a task is done", "Key documents", folder sections brought up to date with the current tree).
- **Caveats:** (1) Only Task D is back-filled above; caveats for kernel increments v0.3-v0.11 stay in the yaml `TASK-1` notes and the workbook `Settings` logs. (2) Not changed here and still stale: `TODO.md` header says the latest mainline is v0.9 (disk and yaml say v0.11, with `build_stream2_v2.py`/`..._Stream2_v2.xlsx` also present); `instructions/context-egypt.md` key-files table points at the v0.3 prototype and at `egypt+mitigation/Methodology/` (the methodology note now sits in `egypt+mitigation/InitialResultsAndIssues/`); the yaml, context file and TASK-D spec still write the legacy folder as `original_cpat_excel/` although the folder on disk is `cpat_excel_original/`. (3) Working-tree reorganisation (`cpat_excel_new/standalone-final/` -> `standalone_initial_prototypes/`, legacy folder rename, `NORMS.md`/`TODO.md`/`_research/` untracked) is uncommitted; nothing was committed in this task.

## 2026-10-02 - T2: merge Stream 2 (Tasks F, I, J) into the mainline (v0.12)
- **Task:** Integrate the Stream-2 branch (v0.7 -> `Stream2_v1/v2/v3` = Task F energy CO2, Task I output-based rebate, Task J revenue fund) with the mainline v0.11 (Tasks A-E, H, K, L, D-scaffold) into one workbook, v0.12.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.11.xlsx`; branch `Old\CPAT_Industry_Kernel_Egypt_v0.7branch_Stream2_v3.xlsx` (reference); builders `build_stream2_v1.py`, `build_stream2_v2.py`, `build_stream2_v3.py` (imported, not modified).
- **Outputs:** `cpat_excel_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v0.12.xlsx` and `build_v0_12.py`. New sheets Data_EF, Emissions_Industry, Rebate_Industry, Fund_Industry; Check sections F, I, J appended after row 1516; Settings version-log row v0.12. v0.11 and the three branch workbooks moved to `Old\`. Updated `TODO.md` (T2 ticked, header), `NORMS.md`, yaml, `context-egypt.md`, `EgyptTaskReference.md`.
- **Regression:** for every bundle (LEGACY, 1A, 2A, 2B, 3A, 3B, 3C) all Check "Max |" summaries are 0, except the comparison rows 2-4, 584/585 and 1381, which are compared with v0.11 instead. LEGACY, 1A, 2A, 2B and 3A are identical to v0.11 (Mitigation_Industry and Check rows 1-1516, max abs diff 0). Only 3B (theta = 1, rebate) and 3C (phi = 1, fund) change, by design. No error values on any sheet.
- **Caveats:**
  1. **Fund_Industry process abatement adapted.** It now uses the v0.9 per-category ERmax form: wm = Q x cov x max(EF, 0) x ERmax / 1000, wp = wm x e^(-beta P), with 16 rows (np/no). The branch used the v0.7 single-beta form. The fund is still calibrated on the block curves, and the fuel side is unchanged. Fund 3C results therefore differ from the branch file.
  2. **`+o4` added to the process price term.** It is in o118-o125 (np and no) and in o15/o16. In v0.11, o15/o16 are still in the v0.7 form (beta.np from E363:E370 for both np and no, no ERmax), which is inconsistent with o118 (v0.9). This is pre-existing and was not changed here.
  3. **Task F check (d) re-pointed.** It used block o1 (row 645), which cascades to the year row (o29), not to a price. In the branch the check never bound because output was exogenous. Under Task H (v0.10), 2027 scenario-2 coal/gas CO2 is about 3e-6 Mt above scenario 1 at a zero explicit price. The check now conditions on o2 + o3 (rows 646/647). Block o1 itself is unchanged and stays a label cascade.
  4. **Rebate is counted on two paths.** Task I's rebate uses EU benchmark x obrrb, while Task H's output response (v0.10) deducts min(obrrb, price) x covered EF. Task I's ppin is kept as a memo so the rebate does not enter output twice; the two bases are not reconciled.
  5. **ssc rows now hold 1 in every bundle.** Data_Prices `egy.mit.ssc.<sector>.2` is 1 for all bundles (ssc_fund default); it has no effect while shp.<fuel>.ind.2 = 0 (phi = 0).
  6. **Ex-post shortfall in 3C.** In 3C the ex-post shortfall is negative (e.g. -152 USD mn in 2030): actual o155 revenue is below F, because F is phi x pre-fund revenue rev0. This is the Stream-2 design that avoids circularity.
  7. **T1 still not applied.** Rows 53-60 remain placeholders.

## 2026-10-02 - Task G: IPPU replacement and fuel-CO2 reconciliation (v0.13)
- **Task:** Task G (EgyptTaskReference 5.1/5.2). Replace CPAT's proportional IPPU row with the block's process emissions to remove the double count, and reconcile block product fuel CO2 with sector energy CO2. Produces v0.13.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.12.xlsx`. Legacy `cpat_excel_original\CPAT 1.0pre_456_NoPropData.xlsb`, Mitigation rows 7566-7570 / 13883-13887 (IPPU co2/ch4/n2o/fga/tot) and 6590 (ind CO2), values stored. CPAT method: IPPU(t) = IPPU(t-1) x ind CO2(t)/ind CO2(t-1) from 2024.
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.13.xlsx` and `build_v0_13.py`. Manual inputs rows 84-95: switch E85 `IppuOther` NONE (default) / CPAT, plus a per-product "fp counted as IPPU" flag (E88:E95; ammonia = 1). New sheet `IPPU_Industry`: CPAT IPPU; CPAT-method IPPU; block np/no/proc; fp as IPPU; non-block remainder; kernel IPPU = block + non-block; double-count correction; sector fuel-CO2 reconciliation. Check section Task G after row 1827 (summary D1831). v0.12 moved to `Old\`.
- **Regression:** for all bundles, every Check "Max |" row is 0 (Task G identities included), and all prior sheets are identical to v0.12 (max diff 0). There are no error values. The IppuOther = CPAT switch test passes. 2030 s2, kernel vs CPAT-method IPPU (Mt): LEGACY 87.67 vs 82.79; 1A/3A 84.75 vs 85.27; 2A/2B 86.74 vs 85.27; 3B 86.99 vs 86.29; 3C 80.01 vs 81.91. Non-block 50.75 in all.
- **Caveats:**
  1. **Report-only.** Kernel IPPU is not yet fed into a national GHG total; this needs the CPAT links (Task M). There is no calibration to CPAT.
  2. **Non-block baseline.** Non-block IPPU in s1 = CPAT IPPU - block. Under NONE it is held at s1 in s2; under CPAT it follows CPAT's s2/s1 ratio.
  3. **CPAT-method s2 is an approximation.** It reproduces CPAT exactly only in s1. In s2 it applies CPAT's rule to the kernel's own industrial energy CO2 change, with the non-kernel sectors (omn, ftr) held at baseline.
  4. **fp flag judgement.** Only ammonia SMR feedstock fp is booked as IPPU (IPCC 2B1; CPAT mch energy CO2 = 0). DRI reductant fp stays in energy.
  5. **Reconciliation gap (Info rows).** Block fuel CO2 net of fp-as-IPPU exceeds kernel sector energy CO2 in every year for cem, nfm and mch, and in 11 (s1) / 16 (s2) years for irn. Cement is about 13.5 Mt (50 Mt clinker x 0.2883) against 9.5 Mt in 2022. Block fuel EFs or CPAT sector energy balances need review; not resolved here.
  6. **Data source.** CPAT values come from the legacy xlsb (as in Task F), not from the Egypt csv run.
  7. **T1 still not applied** (rows 53-60 are placeholders).

## 2026-10-02 - Task M: links to main CPAT and Table 2 assembly (v0.14)
- **Task:** Task M (EgyptTaskReference 5.6). Link the kernel to CPAT national outputs (GHG for coverage %, revenue, deaths avoided, recycling) and assemble Table 2 in the kernel, porting the TASK-2b rebuild composition. Produces v0.14.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.13.xlsx`; `egypt+mitigation\AdHocRebuild\cpat_outputs_egypt_2022_2041.csv` (CPAT runs EG1-EG4, 32 codes); rebuild method `MethodologyNote_v0.1.md`, `build_adhoc_rebuild_v0_1.py` (Results).
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.14.xlsx` and `build_v0_14.py`. New sheets `CPAT_National` (csv stored) and `Table2_Industry`: A bundle -> run mapping (D6:D12; 1A/2A EG1, 2B EG2, 3A-3C EG3, LEGACY '-') + active bundle, scope (Scenarios L), summary year; B CPAT series of the mapped run + deltas; C kernel series; D Table 2 columns J K L M N O P Q R T U AR per year; E live summary row + stored 2030 snapshot of all bundles with rebuild v0.1 K. Check section Task M after row 1857. v0.13 moved to `Old\`.
- **Method (deltas only):** K = dGHG_CPAT + (dIPPU_kernel - dIPPU_CPAT) + (dInd_kernel - dInd_CPAT); dInd_kernel = d energy CO2 of the kernel sectors + non-kernel industry change (All sectors: non-kernel baseline x CPAT run's ind2/ind1 - 1; Industry only: 0). J = (All sectors: CPAT energy CO2; Industry only: encov x kernel-sector energy CO2 + flag x block process baseline) / CPAT GHG baseline. P = gross - rebates (Rebate_Industry) - fund F (Fund_Industry); gross = All: CPAT six-fuel carbon-tax receipts + cptraj x encov x (dInd_kernel - dInd_CPAT) + block process revenue; Industry only: cptraj x encov x kernel-sector energy CO2 (policy) + process revenue. Q = CPAT deaths avoided x dEnergy CO2 (kernel composition) / dEnergy CO2 (CPAT). AR = CPAT dNet new revenue - CPAT carbon-tax receipts + P. M/N/O/T/U = block cbcov/cbintch/cbobchu/emrt over baseline emis/cbqch.
- **Regression:** every Check "Max |" row is 0 for all bundles (Task M included), all prior sheets identical to v0.13 (max diff 0), no error values; live row = stored snapshot.
- **2030 results (kernel / rebuild v0.1):** K Mt 1A -27.7/-31.6, 2A -25.7/-27.7, 2B -27.1/-29.3, 3A -9.7/-18.0, 3B -6.6/-12.8, 3C -17.3/-22.4. J % 63.0, 57.3, 57.3, 8.5, 8.5, 8.5. P $bn 6.90, 6.27, 6.24, 0.91, 0.00, -0.37. Q 1441, 1441, 1497, 278, 241, 397. AR $bn 11.10, 10.47, 10.67, 2.67, 1.76, 1.39.
- **Caveats:**
  1. **T1/T3 not done.** TODO T4 asked for Task M after T1/T3; built now on request. Process semi-elasticities are still placeholders, so K, N, T change once T1 is applied.
  2. **Data vintage.** The csv runs differ from the CPAT values stored in the kernel (xlsb; 2030 baseline IPPU 85.97 vs 87.67, industrial energy CO2 88.97 vs 75.38). Only deltas within one source are composed; J mixes csv GHG with kernel-sector levels.
  3. **Smaller K than the rebuild,** mainly for 3x: the kernel's own industry response replaces CPAT's (no kappa, D_obr, F_fund add-ons); kernel-sector energy CO2 is smaller than kappa x CPAT industry CO2 (J 8.5 % vs 14 %).
  4. **Negative P in 3C (-0.37).** Fund F = phi x block revenue (CBAM products), which exceeds kernel-sector carbon revenue because block fuel CO2 > sector energy CO2 (Task G reconciliation gap). Left unclamped.
  5. **LEGACY** is not a Table 2 bundle: national-linked columns are 0; block metrics shown as is.
  6. **Recycling effects:** the csv has no recycling outputs; reported as revenue use (Scenarios K) + AR only.
  7. **Run mapping** is a stored input (Table2_Industry D6:D12); EG3 prices kappa = 0.54 of industry, so its dGHG residual (non-industry) is that run's.
  8. **Snapshot** rows are stored at default Manual inputs; Check compares live = snapshot only in 2030.

## 2026-10-02 - TASK-EF: Egypt CBAM emission factors split four ways (v0.1, values ready, not applied)
- **Task:** A transparent, auditable derivation of Scope 1 emission factors for the eight kernel CBAM goods, split into fuel combustion (fc), fuel-based process/reductant (fp), non-fuel process CO2 (np) and non-CO2 (no).
- **Inputs:** IPCC 2006 Vol.2 Table 2.2 and Vol.3 Tables 2.4, 3.1, 3.3, 4.1, 4.10 and 4.15; CBAM Implementing Regulation (EU) 2023/1773 and its default-value conventions; `Manual inputs` H30:K37 and S:V of kernel v0.12/v0.13; Egypt plant information (Tier C/D).
- **Outputs:** `egypt+mitigation/EmissionFactors/EGY_CBAM_EF_v0.1.xlsx`, `build_ef_v0_1.py`, `recalc_and_check.py` (0 errors, 14 checks OK) and `EGY_CBAM_EF_Methodology_v0.1.md`; `TASK-EF` in `instructions/instructions-egypt.yaml`; `EgyptTaskReference.md` section 1; `TODO.md` T5.
- **Caveats:**
  1. Not applied to the kernel. Adoption is queued as T5.
  2. Conventions differ from the kernel:
     - urea np = 0 under the CBAM rule, against the kernel's -0.733 (the `urea_conv` switch reproduces the kernel);
     - AN keeps HNO3 as a precursor (own 0.112, against the kernel's folded-in 0.97);
     - DRI-EAF is rebuilt from a carbon balance (0.609, against 0.730).
  3. Egypt-specific inputs are Tier C/D and carry VERIFY flags: ammonia GJ/t, the nitric-acid N2O abatement share, Egyptalum PFC rates, the kiln fuel mix, DRI gas use and the EISCO BF closure. Egypt portals (UNFCCC, CDM, GNR, IEA) were not reachable.
  4. Clinker fc 0.314 (> 0.2883) widens the v0.13 cement fuel-CO2 reconciliation gap.
  5. EU default values are copied from the kernel, not re-verified.

## 2026-10-02 - Integrated Egypt methodology document (v1.0)
- **Task:** Bring the whole Egypt thread into one main methodology document. The EF derivation is Appendix A and the process semi-elasticity work (Task D) is Appendix B.
- **Inputs:**
  - `README.md`, `instructions/context-egypt.md`, `CAVEATS.md`, `TODO.md`, `NORMS.md`, `EgyptTaskReference.md`, `instructions/instructions-egypt.yaml`;
  - `TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` and the `ProcessEmissions_CarbonPriceResponse_Report.md` report;
  - `AdHocRebuild/MethodologyNote_v0.1.md`;
  - `EmissionFactors/EGY_CBAM_EF_Methodology_v0.1.md`;
  - the `InitialResultsAndIssues/` docx files (Technical note, MajorIssues, EgyptResultsInitial, MACC audit trail);
  - kernel v0.13 (`Manual inputs` H30:K37 and rows 53-60).
- **Outputs:** `egypt+mitigation/EGYPT_Methodology_v1.0.md` and `.docx`. The docx is generated from the md by a python-docx script, which is not in the repo. Pointers added in `README.md` (Key documents, egypt folder), the `NORMS.md` Key documents table, the `instructions/context-egypt.md` key files, `EgyptTaskReference.md`, and `TASK-METHOD` in `instructions/instructions-egypt.yaml`.
- **Caveats:**
  1. The document describes the current state. The Table 2 results come from the TASK-2b rebuild, which uses kernel EFs, not EF v0.1, and has open flags: kappa(EG3) = 0.54, and eps_Q, P_EU and sigma are placeholders.
  2. Kernel v0.13 still holds the Task D placeholders (T1 not applied), so the App. B values are not yet live.
  3. App. B.5 recommends routing beta to fp for DRI, BF and ammonia, together with np/no. This is a recommendation, not implemented.
  4. The earlier MACC audit-trail docx (ammonia 85 %, AN 89 % at $100) is treated as superseded by Task D.
  5. If the md is edited, regenerate the docx or the two will drift.

## 2026-10-02 - T1 + T5: Task D semi-elasticities and Egypt CBAM EF v0.1 applied (kernel v0.15, AdHoc rebuild v0.2)
- **Task:** Apply the updated emission factors (TASK-EF v0.1) and the IPCC process-emission semi-elasticities (Task D, TODO T1) to both the kernel prototype and the TASK-2b ad hoc rebuild.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.14.xlsx`; `egypt+mitigation\EmissionFactors\EGY_CBAM_EF_v0.1.xlsx` (Products D:G); `TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` and `ProcessEmissions_CarbonPriceResponse.xlsx` (IPCC central ER at $100); `AdHocRebuild\AdHocCalculations_Rebuild_v0.1.xlsx` builder.
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.15.xlsx` + `build_v0_15.py` (Manual inputs H30:K37 EFs, M35/M36 embedded NH3, S:V memo, AD/AE sources; E50 = IPCC; rows 53-60 ERmax / P* = 100 / ER*; Check section T1/T5 at row 1881; Settings log row 42). `AdHocRebuild\AdHocCalculations_Rebuild_v0.2.xlsx` + `build_adhoc_rebuild_v0_2.py`, `recalc_and_check_adhoc_v0_2.py` (report `_v0_2_report.txt`), `MethodologyNote_v0.2.md/.docx`, new switch `Inputs!EFSet` (EGY_EF_V01 default / PROTOTYPE). v0.14 moved to `Old\`.
- **Regression:** kernel: every Check "Max |" row 0 for all 7 bundles, no error values (stored Task J v2 table and Task M Table 2 snapshot refilled; baseline-independent rows unchanged except via EFs). AdHoc: ALL PASSED; PROTOTYPE FULL/NOPHASE = v0.11 132/132 (EFSet forced PROTOTYPE); REBUILD = Python mirror 534/534; check 8 (E_base 61.16) is n/a unless EFSet = PROTOTYPE (E_base 2030 now 62.42 Mt).
- **2030 K (Mt):** kernel v0.15 1A -29.8, 2A -25.8, 2B -27.1, 3A -11.8, 3B -8.6, 3C -23.9 (v0.14 -27.7/-25.7/-27.0/-9.7/-6.6/-17.3); rebuild v0.2 -31.8/-27.8/-29.3/-18.2/-12.7/-22.6 (v0.1 -31.6/-27.7/-29.3/-18.0/-12.8/-22.4).
- **Caveats:**
  1. **Bug fixed (kernel):** EF-category rows o15/o16 (Mitigation_Industry 260/261, 659/660) applied the np beta to no and ignored ERmax; now np = F x (1 - exp(-E x P)), no = H x (1 - exp(-G x P)), as in o118-o125. Latent while the placeholders were equal.
  2. **AN:** HNO3 N2O folded into AN own no (0.79 x 1.2588 = 0.9944); ER at $100 = N2O-weighted blend of unabated 0.7210 and abated 0.3292 at the EF workbook's 50 % abatement share: (3.5 x 0.7210 + 1.25 x 0.3292) / 4.75 = 0.6179.
  3. **Urea np = 0** (CBAM rule; was -0.733, floored to 0 in the process factor anyway). Ammonia/urea beta = 0: routing the CCS lever to fp (EF App. B.5) is not implemented.
  4. **Aluminium:** combined ER 0.2164 applied to both np (anode CO2) and no (PFC) instead of the non-additive split 0.1282 / 0.1078.
  5. **P* = 100 in USD2019,** no deflation to the kernel price unit. Fuel ER (rows 40-47) and the fund path unchanged; 3C fund shadow price 2028 falls 72.4 -> 44.5 $/t because the higher beta buys more abatement per dollar.
  6. **Cement fc 0.2883 -> 0.3136** widens the Task G block-vs-sector fuel CO2 gap (info rows in Check still non-zero counts).
  7. **EF VERIFY list** (EF App. A.6) still open; values not final.
  8. Table 2 snapshot rebuild column now "Rebuild v0.2 K"; Task M not otherwise redesigned (T3 and the EG3 full-coverage re-run still pending).

## 2026-10-02 - AdHoc rebuild v0.3: P* deflation and EG3 full-coverage approximation
- **Task:** Build `AdHocCalculations_Rebuild_v0.3.xlsx` without modifying v0.2. Added `PStar=122` for IPCC beta sets and made `KappaMode=SCALE` the default to approximate full industrial coverage for EG3 bundles 3A/3B/3C.
- **Inputs:** `AdHocCalculations_Rebuild_v0.2.xlsx`, `build_adhoc_rebuild_v0_2.py`, `recalc_and_check_adhoc_v0_2.py`, `MethodologyNote_v0.2.md`, `cpat_outputs_egypt_2022_2041.csv`, `prototype_v0_11_results.json`, Egypt EF v0.1 and Task-D IPCC ER100 values.
- **Outputs:** `egypt+mitigation\AdHocRebuild\AdHocCalculations_Rebuild_v0.3.xlsx`, `build_adhoc_rebuild_v0_3.py`, `recalc_and_check_adhoc_v0_3.py`, `recalc_and_check_adhoc_v0_3_report.txt`, `MethodologyNote_v0.3.md` and `.docx`. Verification passed: PROTOTYPE FULL/NOPHASE 132/132 each; REBUILD Python mirror 588/588; no Excel errors.
- **Caveats:** `KappaMode=SCALE` is an approximation of a full-coverage EG3 run pending a CPAT re-run. CPAT fuel receipts are scaled by 1/kappa; CPAT delta net new revenue itself is not independently re-run. `PStar=122` has Medium confidence and applies only to IPCC beta sets; PROTOTYPE keeps /100.

## 2026-10-02 - Worked example results workbook (v0.1, quick draft)
- **Task:** One-example-per-level walkthrough of the ad hoc Table 2 rebuild v0.3 (parameters -> CPAT inputs -> clinker in 1A -> 8-product block -> national 1A metrics -> 3A/3B/3C variants), with a column noting where the main version (kernel v0.15) differs.
- **Inputs:** `AdHocCalculations_Rebuild_v0.3.xlsx` (Inputs, Results), `cpat_outputs_egypt_2022_2041.csv` (2030), `MethodologyNote_v0.3.md`, `EGYPT_Methodology_v1.1.md` section 5.1.
- **Outputs:** `egypt+mitigation\AdHocRebuild\ExampleResults_v0.1.xlsx` (sheets Example, Inputs, Block), builder `build_example_results_v0_1.py`. All 30 check values match v0.3 to 4 dp (max diff 5e-5); no Excel errors.
- **Caveats:** Quick draft for iteration. Inputs copied as values (not linked to v0.3). Only REBUILD / NOPHASE / SCALE / EGY_EF_V01 shown. Kernel column quotes v0.15 headline values and method differences only; kernel steps are not recomputed.

## 2026-10-03 - Kernel v0.16: run-2 fixes (P* deflation, EG3 1/kappa scaling, block fuel CO2 reallocation, 3C fund fixed point)
- **Task:** Apply the four user-agreed fixes to the final prototype (decisions recorded in the session; mirrors AdHoc rebuild v0.3 for items 1-2) and refresh the `Egypt Final results` deliverables.
- **Inputs:** `Old\CPAT_Industry_Kernel_Egypt_v0.15.xlsx`; `egypt+mitigation\AdHocRebuild\rebuild_v0_3_K2030.json` (rebuild v0.3 K for the Table 2 comparison column).
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.16.xlsx` + `build_v0_16.py`: Manual inputs F/J 53-60 P* = 122 (Check T1/T5 ER rows use 122); `Table2_Industry` row 54 kappa, rows 59-60 block fuel CO2 reallocation (ek1' = sum max(block, sector)), row 64 non-kernel response /kappa, rows 84/91 coverage and gross revenue at kappa = 1 for Industry only, row 94 deaths /kappa, row 96 AR; `Fund_Industry` rows 425-433 stored fund R* per bundle (fixed point R = post-abatement block payments o155, secant per year, tol 1e-9), row 329 reads it; new Check section; Table 2 rebuild column "Rebuild v0.3 K". `Egypt Final results\`: kernel v0.16, rebuild v0.3, MethodologyNote_v0.3, ResultsComparison_Table2_v0.3, EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx (built by `AdHocRebuild\make_results_page_v0_3.py`), EGYPT_Methodology_v1.2, EGYPT_FinalCaveats_v1.1; superseded files in `Egypt Final results\Old\`.
- **Regression:** every Check "Max |" row 0 for all 7 bundles, no error values; 3C fund fixed point residual 5e-12 (5 iterations); other bundles have no fund.
- **2030 (kernel v0.16 / v0.15):** K 1A -29.0/-29.8, 2A -25.5/-25.8, 2B -26.7/-27.1, 3A -21.1/-11.8, 3B -17.4/-8.6, 3C -32.9/-23.9 Mt; J 3A-3C 18.5/8.6 %; P 1A 6.89, 3A 1.88/0.89, 3B 0.98/-0.02, 3C 0.73/-0.47 $bn; Q 3A 816/278, 3B 746/239, 3C 985/366. Rebuild v0.3 K -31.4/-27.8/-29.3/-25.1/-19.6/-30.6.
- **Caveats:**
  1. 1/kappa scaling is a linear approximation of a full-coverage EG3 CPAT run (non-kernel industry responds at CPAT's average priced-industry rate).
  2. 3C fund = block's own post-abatement payments; non-block industry revenue (0.73 $bn) stays in P. The rebuild sends all industrial revenue to the fund (P = 0): convention difference.
  3. Reallocation removes the block-above-sector excess (cement 19.05 vs 10.91 Mt in 2030) from non-kernel industry; the underlying CPAT energy-balance mismatch is not resolved.
  4. Data-vintage mix remains (stored industry CO2 75.4 vs csv 89.0 Mt): about 1.9 Mt of the prototype-rebuild K gap at kappa = 1, about 3.5 Mt for EG3.
  5. fp routing (ammonia/urea beta = 0) and the block fuel-intensity channel remain unimplemented (kept as caveats).
  6. The stale `EgyptResultsInitial_UpdatedResults_tracked.docx` (v0.1) may still be open in Word; move it to `Egypt Final results\Old\` if it remains in place.
