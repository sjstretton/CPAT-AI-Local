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

- Kernel increments v0.3-v0.11 (Tasks E, A, B, C, K, D-scaffold, H, L): `notes` under `TASK-1` in [`egypt/instructions/instructions-egypt.yaml`](egypt/instructions/instructions-egypt.yaml) and each workbook's `Settings` version log.
- Process semi-elasticities (Task D): [`egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`](egypt/supporting/TASK-D_ProcessHalfElasticities_DropIn_v0.1.md) section 4.
- Gap list for the Egypt kernel: [`egypt/instructions/EgyptTaskReference.md`](egypt/instructions/EgyptTaskReference.md).
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

## 2026-10-02 - Repo tidy: final deliverables vs Old/ (no model changes)
- **Task:** Tidy the Egypt output and working folders so only the final deliverables sit at top level; everything else moved to `Old/`. The prototype kernel v0.16 (not the ad hoc rebuild) is treated as the final model.
- **Inputs:** `Egypt Final results\`, `egypt+mitigation\`, `cpat_excel_new\standalone_working_version\`.
- **Outputs:** `Egypt Final results\` and `egypt+mitigation\` now both hold the identical final set at top level (hash-checked): `CPAT_Industry_Kernel_Egypt_v0.16.xlsx`, `EGYPT_Methodology_v1.2`, `EGYPT_FinalCaveats_v1.1`, `ResultsComparison_Table2_v0.3`, `EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx` (+ `EgyptTaskReference.md` in the working folder). Moved to `Egypt Final results\Old\`: rebuild v0.3, MethodologyNote_v0.3, `CAVEATS.md` snapshot; exact duplicates of files already in `Old\` removed. Moved to `egypt+mitigation\Old\`: `AdHocRebuild\`, `EmissionFactors\`, `InitialResultsAndIssues\`, `ProcessEmissions_CarbonPrice_Response\`, TASK-2a/TASK-D specs, Methodology v1.0/v1.1, ResultsSummary v1.0, kernel v0.1. `standalone_working_version\`: builders other than `build_v0_16.py` moved to `Old\`, `__pycache__` deleted; `build_v0_16.py` paths updated (adds `Old\` to `sys.path`, reads v0.15 and `rebuild_v0_3_K2030.json` from their `Old\` locations; imports verified). Removed an empty stray root folder named `EGYPT_FinalCaveats_v1.1.md\`. Paths updated in `README.md`, `NORMS.md`, `TODO.md`, `instructions\context-egypt.md`.
- **Caveats:**
  1. `EGYPT_Methodology_v1.2` Appendix C (file map) and earlier entries in this log / `instructions-egypt.yaml` still cite pre-tidy paths; prefix `Old\` for anything not in the final set.
  2. `egypt+mitigation\EGYPT_ResultsSummary_v1.0.docx` was locked (open in Word); a copy is in `Old\`, delete the top-level one once closed.

## 2026-10-02 - Repo tidy follow-up
- **Task:** Resolve both caveats of the previous entry.
- **Inputs:** EGYPT_Methodology_v1.2.md/.docx.
- **Outputs:** Appendix C paths now point to Old\ in the .md and .docx (table text only, formatting kept), copied to both Egypt folders; locked egypt+mitigation\EGYPT_ResultsSummary_v1.0.docx removed (copy in Old\).
- **Caveats:** Earlier log entries and instructions-egypt.yaml still cite pre-tidy paths (historical record).

## 2026-10-02 - Updated results text v0.4 (final prototype values)
- **Task:** Put the final prototype (kernel v0.16) numbers into the tracked-changes results text; v0.3 carried the ad hoc rebuild values.
- **Inputs:** Egypt Final results\Old\EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx; kernel v0.16 2030 values from ResultsComparison_Table2_v0.3.md.
- **Outputs:** EgyptResultsInitial_UpdatedResults_v0.4_tracked.docx in both Egypt folders (builder egypt+mitigation\Old\AdHocRebuild\make_results_page_v0_4.py); tracked changes still relative to the original text; Table 2 checked against v0.16 (P, K, J, N, O, Q). References updated in README, FinalCaveats v1.1, Methodology v1.2, ResultsComparison v0.3. v0.3 moved to Old\.
- **Caveats:** O uses NOPHASE (as Table 2); the prototype's default FULL roughly doubles it. 2A/2B intensity shows 0% because the prototype holds block fuel intensity fixed (stated in the text). Narrative re-ranked: 3C now has the largest cut (32.9 Mt), 2B the largest health gain (1,473). Methodology v1.2 section text still describes the rebuild-based results page.

## 2026-10-02 - CBAM carve-out of Table 2 (v0.1)
- **Task:** Original CPAT run results everywhere except the CBAM block; block from kernel v0.16 with growth matched to CPAT sectors. 3A-3C use EG3 as run (no 1/kappa).
- **Outputs:** EGYPT_CarveOut_Table2_v0.1.md/.docx in both Egypt folders; builder egypt+mitigation\Old\AdHocRebuild\make_carveout_v0_1.py with kernel extracts carveout_kernel_*_2030.json (Excel COM, Settings!B10 per bundle).
- **Result (2030 K, Mt):** 1A -36.1, 2A -31.7, 2B -33.4, 3A -21.5, 3B -17.8, 3C -31.9.
- **Caveats:** K = CPAT dGHG - r x block + kernel block change, with r = CPAT industry energy CO2 % change (also CPAT's IPPU %). Non-CBAM IPPU (about 50 Mt) keeps CPAT's response; prototype v0.16 held it fixed (main cause of its low 1A). Growth rescaled 2024-2030: irn x0.976, cem x1.001; mch (mining & chemicals = fertilisers) x1.157 and nfm x0.956 follow total CPAT industry because CPAT sector energy is 0 for Egypt. M/N/O kept from v0.16 (O NOPHASE). Deaths scaled by block fuel adjustment. 1A remains 5.5 Mt below the original: about 2.7 Mt was the original's process double count, the rest is the block responding less than CPAT's industry average (fuel intensity fixed). Tracked doc v0.4 not updated to the carve-out.

## CBAM carve-out v0.2 (CPAT fuel-intensity response), updated text v0.5, Methodology v1.3 (2026-10-03)

- **Task:** Final Table 2 = original CPAT runs everywhere; only the CBAM block replaced, using CPAT's own emissions-intensity reduction plus the CBAM output/process adjustment, with no double counting.
- **Method:** K = dGHG_CPAT - r*B + dB. CPAT's implied block change (r*B) removed in full; dB = kernel output response + kernel process abatement (where charged) + CPAT fuel-intensity response (1+r)^(1/3)-1 (s_int = 1/3, Methodology section 3): EG1 -4.9%, EG2 -5.1%, 3A-3C use -4.9%. N/O = kernel v0.16 plus the fuel-intensity term (O x0.8 NOPHASE; 3B x1.0). Check: the N formula reproduces kernel N to within 0.2 pt with i_f = 0.
- **Results 2030 (1A/2A/2B/3A/3B/3C):** K -37.4/-33.1/-34.8/-22.8/-19.1/-33.0; P 6.9/6.3/6.2/1.5/0.6/0.4; N -5.8/-2.1/-2.3/-5.8/-5.8/-23.1; O -24.0/-12.2/-12.3/-24.0/-5.1/-36.2; Q 1,501/1,456/1,517/552/491/646; J 63/57/57/14/14/14.
- **Outputs:** EGYPT_CarveOut_Table2_v0.2.md/.docx (builder Old\AdHocRebuild\make_carveout_v0_2.py); EgyptResultsInitial_UpdatedResults_v0.5_tracked.docx (make_results_page_v0_5.py, tracked relative to the original; rankings rechecked); EGYPT_Methodology_v1.3 (new section 5.0). Both Egypt folders identical. v0.4 text, carve-out v0.1 and Methodology v1.2 moved to Old\. References updated in README, NORMS, TODO, context-egypt.md, FinalCaveats v1.1, ResultsComparison v0.3.
- **Caveats:**
  1. The 3B rebate and the 3C fund are not re-solved for the lower block fuel payments (under 0.05 $bn).
  2. O on NOPHASE, not yet confirmed by the user.
  3. 3A-3C use EG3 as run (54% industry coverage), so their non-block industry cut is diluted.
  4. The CPAT intensity share (1/3) is the CPAT efficiency/fuel-switch split; it is not product-specific.

## CBAM obligations on FULL convention: carve-out v0.3, updated text v0.6 (2026-10-03)

- **Task:** Report CBAM obligations (O) on the FULL convention (EU CBAM factor 0.485 in 2030, full credit for the domestic price; kernel headline) instead of NOPHASE.
- **Method:** O = kernel v0.16 FULL value + 0.59 x the fuel-intensity change in N ((48.5 - 20)/48.5); 3B x1.0. NOPHASE kept as a memo row. All other values as in carve-out v0.2.
- **Results 2030 O FULL (1A/2A/2B/3A/3B/3C):** -44.2/-22.9/-23.0/-44.2/-5.0/-53.1 (NOPHASE -24.0/-12.2/-12.3/-24.0/-5.1/-36.2).
- **Outputs:** EGYPT_CarveOut_Table2_v0.3.md/.docx (make_carveout_v0_3.py); EgyptResultsInitial_UpdatedResults_v0.6_tracked.docx (make_results_page_v0_6.py; O cells and O narrative only); Methodology v1.3 section 5.0 edited in place. v0.5 text and carve-out v0.2 moved to Old\. Both Egypt folders identical; references updated.
- **Caveats:**
  1. The FULL percentages are not like-for-like with the original Table 2, which used NOPHASE; the comparison table shows both.
  2. The results text does not state the convention explicitly; add a footnote to Table 2 if needed.

## Egypt finalisation: final set docx-only, FinalCaveats v1.2, convention note (2026-10-03)

- **Task:** Finalise the Egypt deliverables, archive the old versions and the .md files, and tie off loose ends.
- **Final set (top level of both `Egypt Final results\` and `egypt+mitigation\`, hash-identical):** EGYPT_CarveOut_Table2_v0.3.docx (final Table 2), EgyptResultsInitial_UpdatedResults_v0.6_tracked.docx, EGYPT_Methodology_v1.3.docx, EGYPT_FinalCaveats_v1.2.docx, CPAT_Industry_Kernel_Egypt_v0.16.xlsx. The working folder also keeps EgyptTaskReference.md (workflow tracker, per NORMS).
- **Changes:**
  - FinalCaveats v1.2 adds section F (carve-out caveats F1-F7) and updates items 8-9.
  - The results text v0.6 now says obligations are "under the 2030 CBAM phase-in" (tracked).
  - The .md sources and ResultsComparison_Table2_v0.3 moved to Old\. make_carveout_v0_3.py now writes its md to Old\.
  - References updated in README, NORMS, TODO, context-egypt.md and instructions-egypt.yaml (FINAL note under TASK-1).
- **Caveats:**
  1. The egypt+mitigation\Old copy of FinalCaveats v1.1 was restored from the Egypt Final results\Old copy, which has the older file references (superseded anyway).
  2. The kernel xlsx could not be hash-checked because it is open in Excel.

## Kernel v0.17: CBAM carve-out in the kernel (2026-10-03)

- **Task:** Put the final Table 2 (CBAM carve-out v0.3, O on FULL) into the kernel with live formulas.
- **Outputs:** `CPAT_Industry_Kernel_Egypt_v0.17.xlsx` + `build_v0_17.py` (Excel COM, from v0.16). New sheet `CarveOut_Table2`:
  - A: inputs (live links to Table2_Industry, Manual inputs, CPAT_National, Emissions/IPPU_Industry);
  - B: rates r and i_f;
  - C: block by sector (mch, irn, nfm, cem; growth factors);
  - D: carve-out;
  - E: Table 2 columns for the active bundle (Settings!B10);
  - F: stored 6-bundle snapshot and a live-vs-stored check.
  - Also: a Check sheet section, a pointer in Table2_Industry B112, and a Settings version row. No other formulas changed.
- **Copies:** in both `Egypt Final results\` and `egypt+mitigation\` (hash-identical). v0.16 and `build_v0_16.py` moved to `Old\`.
- **Verification:** each bundle set active in turn, CalculateFull. Live = stored within 0.006 (largest in 3A-3C J: kappa 0.537 is rounded in the script). Kernel N rebuilt from the block table is within 0.19 pt.
- **Fix:** Methodology v1.3 section 5.0 and FinalCaveats v1.2 section F had symbols (minus, delta, times, section sign, kappa, CO2 subscript) saved as "?" (encoding slip in the earlier edit). Repaired, and both docx regenerated.
- **References updated:** README, TODO, context-egypt.md, instructions-egypt.yaml, Methodology (5.0, 6, App. C, version log), FinalCaveats header.
- **Caveats:**
  1. The NOPHASE memo uses the stored v0.16 NOPHASE O per bundle (hard input, rounded to 0.1), not a live convention switch.
  2. With Settings!B10 = LEGACY the carve-out sheet shows n/a; pick a bundle from 1A to 3C.

## 2026-10-04 - Tracked results text v0.7 (terminology; author Stephen Stretton)
- `EgyptResultsInitial_UpdatedResults_v0.7_tracked.docx` (both Egypt folders) built from v0.6 by `egypt+mitigation/Old/AdHocRebuild/make_results_page_v0_7.py`; v0.6 moved to `Old/`.
- Fixes: 3C CBAM obligation cut 30% -> 53% (summary paragraph, missed in v0.6); 3B "undermines both revenue and CBAM relief" -> "raises less revenue and delivers the smallest CBAM relief"; 3C "forgoes revenue and health benefits" -> "raises less revenue and yields smaller health benefits than broad-based pricing"; added note that EG3 prices only about half of industrial energy CO2 (14% coverage, not about 21%).
- Terminology standardised: "industrial abatement rebate", "CBAM-sector emission intensity", "CBAM-sector emissions", "national GHG emissions"; en-dashes in numeric ranges.
- All tracked changes and docProps (creator/lastModifiedBy) of the final .docx files now attributed to Stephen Stretton; Lelia Croitoru's comments kept. References v0.6 -> v0.7 updated (README, instructions, Methodology/FinalCaveats md; docx regenerated).
- Consistency check: final numbers identical across tracked text, CarveOut v0.3, Methodology v1.3 §5.0 and kernel v0.17 snapshot; both folders hash-identical. Not verified by opening in Word (automation hung); XML validated.


## 2026-10-04 - Egypt final v1.0 release (Stephen Stretton)

- All final deliverables relabelled v1.0 and placed identically (hash-checked) at the top of `Egypt Final results\` and `egypt+mitigation\`: CPAT_Industry_Kernel_Egypt_v1.0.xlsx (= v0.17 relabelled, no formula changes), EGYPT_CarveOut_Table2_v1.0, EgyptResultsInitial_UpdatedResults_v1.0_tracked, EGYPT_Methodology_v1.0, EGYPT_FinalCaveats_v1.0. Numbers unchanged (2030 K: -37.4/-33.1/-34.8/-22.8/-19.1/-33.0 Mt).
- Proofread: tracked text fixes (double spaces, punctuation, "CBAM obligations", "trade-offs", 3C label, table-header units), all revisions and docProps by Stephen Stretton. Methodology: final-status header, §5 pointer to §5.0, coverage row in §5.0, kernel v0.17/v1.0 rows, file map updated.
- Md sources in `Old\` (both folders); earlier drafts and md (Methodology v1.3, FinalCaveats v1.2, CarveOut v0.3, text v0.7, kernel v0.17) archived in `Old\Superseded\` and `standalone_working_version\Old\`.
- Not validated by opening in Word (Word COM hangs in this environment); XML checked. Open items unchanged: full-coverage EG3 CPAT run; 3B published deaths (345) untraced; 3B rebate and 3C fund not re-solved.


## 2026-10-05 - Egypt results text v1.1: single scenario term (Stephen Stretton)

- Reviewer comment: the chapter mixed "policy options", "families", "bundles", "choices" and "designs" for the scenarios. `EgyptResultsInitial_UpdatedResults_v1.1_tracked.docx` (builder `egypt+mitigation\Old\AdHocRebuild\make_results_page_v1_1.py`) makes 22 minimal tracked replacements, all by Stephen Stretton, so that every reference to 1A-3C uses "scenario(s)" (for example "Policy bundle" -> "Policy scenario", "The second family" -> "The second set of scenarios", "The six bundles" -> "The six scenarios"). Uses that do not refer to scenarios are kept: "Revenue Recycling Option", "recycling options/choice(s)", "policy design". No numbers changed.
- v1.0 text archived in `Old\Superseded\` (both folders); v1.1 copied to both folders (hash-identical). Methodology and FinalCaveats v1.0 updated only to point to the v1.1 text file. Not opened in Word (COM hangs); XML checked.


## 2026-10-05 - Table 2 workbook with live CBAM obligations (Stephen Stretton)

- New `EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx` (both Egypt folders; builder `egypt+mitigation\Old\AdHocRebuild\make_table2_cbam_xlsx.py`, data `kernel_products_2030.json` from `extract_kernel_products_2030.py`). Rows J, P, K, M, N, Q are hard-coded from the CBAM carve-out v1.0. Row O is computed live by product: obl = max(0, CBF x P_EU x EI - S x d), weighted by 2024 EU exports.
- Inputs are on the Assumptions sheet: EU price in 2030 (USD 100, placeholder kept from the initial analysis); convention (default **Full implementation, CBF = 1**, as in the initial table; alternative 2030 phase-in, CBF = 0.485); deduction scaled by CBF (No); net the 3C fund (No).
- Product-level O reproduces the kernel's O exactly (all six scenarios). It differs from the carve-out v1.0 linear shortcut by <= 0.4 pt. Default O: 1A -24.3, 2A -12.5, 2B -12.6, 3A -24.3, 3B -5.4, 3C -36.6 (2030 phase-in: -44.4/-23.1/-23.2/-44.4/-5.4/-53.4). Sensitivities: net the 3C fund -> 3C -20.7; P_EU 120 -> 1A -21.2; P_EU 80 -> 1A -29.1.
- **Pending:** the v1.0/v1.1 docx (CarveOut, tracked text, Methodology, Caveats) still quote O on the 2030 phase-in convention. Update them once the convention is agreed.


## 2026-10-06 - CBAM obligations restated as CBAM-product intensity change (Stephen Stretton)

- Table 2 row O is now the change in CBAM obligations per tonne exported = export-weighted change in embedded (fuel + process) emission intensity of CBAM products only (2024 EU export weights). The Egyptian carbon-price deduction is not applied, so the EU price and phase-in cancel. Final O: 1A -5.4, 2A -2.6, 2B -2.7, 3A -5.4, 3B -5.4, 3C -20.7% (was FULL -44.2/-22.9/-23.0/-44.2/-5.0/-53.1).
- Updated: `EGYPT_Table2_Final_CBAMcalc_v1.0.xlsx` (O live, deduction variants as memo rows only); results text **v1.2** tracked (`make_results_page_v1_2.py`; O cells, range "3 to 21%", 1A/3A 5%, 2A/2B 3%, 3C 21%, 3B sentence); CarveOut, Methodology §5.0, FinalCaveats F5/item 9; README and instructions references. v1.1 text and `EGYPT_CBAM_ObligationNote_v0.1` (deduction-based) moved to `Old\Superseded\`.
- Not changed: kernel v1.0 sheet `CarveOut_Table2` still reports O on FULL (the workbook governs). The user's `Egypt Final results\EGYPT_Methodology_v1.1 - Edited.docx` and the renamed note in `CBAM Guess - Needs Carolyn Input\` were left untouched and still quote the old O.

## 2026-10-07 - All Egypt deliverables aligned at v1.3

- Methodology v1.3 is built from the author's edited master (`EGYPT_Methodology_v1.1 - Edited.docx`, archived in `Egypt Final results/Old/`). Edits: §2 output and §4.5 now define Table 2 O as intensity-only (export-weighted, no deduction); the kernel's deduction-based Task L obligation and the NOPHASE/FULL/SCALED conventions are kept only as a memo; the P_EU/CBF parameter row and the glossary entry are marked memo-only; "bundle" changed to "scenario" (as in the tracked text). The edited master has no Markdown source, so it was edited directly in Word XML.
- CBAM obligation note rewritten to v1.3 (intensity-only; source `egypt+mitigation/Old/EGYPT_CBAM_ObligationNote_v1.3.md`, via pypandoc).
- CBAM workbook, CarveOut, FinalCaveats, tracked text and kernel are all at v1.3; content is unchanged apart from version references and "scenario" terminology. Kernel v1.3 `CarveOut_Table2`: column M80:M85 stores the intensity-only O; row 71 is relabelled as the FULL deduction memo (live O is still FULL there; the workbook governs).
- v1.0/v1.2 copies archived (FIN `Old/`, WRK `Old/Superseded/`). FIN and WRK copies are byte-identical. README, instructions and EgyptTaskReference now point to v1.3.

## 2026-10-08 - Egypt folder reorganisation and doc consistency fixes
- **Task:** merged `Egypt Final results/`, `egypt+mitigation/` and `instructions/` into a single root folder `egypt/` (`final/`, `supporting/`, `archive/`, `instructions/`); fixed documentation inconsistencies (latest kernel is v1.3 everywhere; legacy folder is `cpat_excel_original/`; methodology master is the edited `.docx`).
- **Inputs:** the three old folders (byte-identical duplicates found by hash; the two folders held the same v1.3 deliverables and mirrored archives).
- **Outputs:** `egypt/` (new `README.md`); duplicates removed, one copy of each file kept; tracked `__pycache__` files removed; path references updated in README, NORMS, TODO, AGENTS, the instructions yaml/context, the TASK-D/TASK-2a specs and the Python builders (`egypt/supporting/AdHocRebuild/*`, `cpat_excel_new/standalone_working_version/Old/build_v0_14-17.py`). Entries above this one still quote the old paths: map `Egypt Final results\`/`egypt+mitigation\` to `egypt\final\`, `Old\` and `Old\Superseded\` to `egypt\archive\` or `egypt\supporting\`.
- **Caveats:** builders were not re-run (they need Excel COM on Windows); path edits are untested. Final CBAM workbook/note renamed to `..._v1.3_NeedsCarolynConfirmation` (from the `CBAM Guess - Needs Carolyn Input/` folder name). Two variants that differed were kept with `_alt1` (FinalCaveats v1.0, Methodology v1.0 md) and the pre-edit Methodology v1.3 renamed `_preedit`, all in `egypt/archive/`; the two `CAVEATS.md` copies from the old `Old/` folders are `egypt/archive/CAVEATS_snapshot_*.md`. `extract_kernel_products_2030.py` still points at the (now archived) v1.0 kernel and old Windows root. Historical versions in `egypt/archive/` were left with their original path text.

## 2026-10-04 - Decisions: 3B rebate scope and O convention (no model change)
- **Task:** resolved the two open TODO T4 decisions on the user's instruction (Stephen Stretton): the 3B rebate goes to all covered industry (`Inputs!ThetaOther` = 1, P approx. 0); the CBAM obligation O is on the FULL convention (CBAM factor phase-in, domestic carbon price deducted in full). NOPHASE (CBF = 1) is kept as a memo only.
- **Inputs:** `TODO.md` T4; `build_v0_11.py` / `build_v0_17.py` convention definitions; CAVEATS 2026-10-03 kernel v0.17 entry (kernel already reports O on FULL).
- **Outputs:** `TODO.md` T4 item updated; this entry. No workbook, builder or yaml changes.
- **Caveats:** decisions only, not yet applied. The AdHoc rebuild defaults (`ThetaOther`, convention) must be set to these values in a new builder version and re-verified with `recalc_and_check_adhoc.py` (Windows/Excel COM). Any Table 2 numbers built under `ThetaOther` = 0 or NOPHASE are superseded once that is done.

## 2026-10-04 - AdHoc rebuild v0.4 builder and verifier drafted (not built, not run)
- **Task:** applied the 2026-10-04 decisions to the AdHoc rebuild defaults: `Conv` = FULL (NOPHASE kept as a memo) and `ThetaOther` = 1. `ThetaOther` is forced to 0 in PROTOTYPE mode so the v0.11 reproduction is unchanged. No formula changes.
- **Inputs:** `build_adhoc_rebuild_v0_3.py`, `recalc_and_check_adhoc_v0_3.py`; CAVEATS 2026-10-04 decisions entry.
- **Outputs:** `egypt/supporting/AdHocRebuild/build_adhoc_rebuild_v0_4.py` and `recalc_and_check_adhoc_v0_4.py` (docstrings, defaults, ReadMe version log; the verifier now saves with Conv = FULL). v0.3 files untouched. Both compile (`py_compile`).
- **Caveats:** drafted on Linux. `AdHocCalculations_Rebuild_v0.4.xlsx` has NOT been built, and the verifier (Excel COM, Windows) has NOT been run. Run `python build_adhoc_rebuild_v0_4.py` then `python recalc_and_check_adhoc_v0_4.py` and check the report. Still to do after a clean run: MethodologyNote v0.4 and ResultsComparison_Table2 v0.4 (results change with ThetaOther = 1 and FULL), the yaml / `EgyptTaskReference.md` / `context-egypt.md` bookkeeping, and whether the final Table 2 deliverables need regenerating.

## 2026-10-04 - T3 builder drafted (kernel v1.4, not built, not run)
- **Task:** drafted `build_v1_4.py` for T3: move 2024 production, growth, EU exports and pre-policy prices out of `Mitigation_Industry` (both blocks) into a new `Manual inputs` section and link them. Values are read from the workbook, so no number should change.
- **Inputs:** `CPAT_Industry_Kernel_Egypt_v1.3.xlsx` (layout and values inspected read-only with openpyxl: both blocks identical, rows 97-108 of `Manual inputs` empty); TODO T3 spec (corrected: the spec's row 62 and v0.9 references are stale).
- **Outputs:** `cpat_excel_new/standalone_working_version/build_v1_4.py`; TODO T3 note. No workbook produced.
- **Caveats:** drafted on Linux, never run; Excel COM needed. New section at `Manual inputs` rows 98-108 (title 98, header 100, products 101-108); links F/G/I rows 276-283 and 675-682, G rows 288-295 and 687-694; total exports (column H, blank placeholder) deliberately not linked. The builder aborts without saving unless the max abs difference over pre-existing cells is 0 and the new Check literal count is 0, then writes the version-log row and moves v1.3 to `Old/`. Check sheet rows 595-1020 hold CPAT values that equal the literals (e.g. 5100); they are comparison data, left as is. Pending after a clean run: yaml (TASK-T3 + TASK-1 notes), `EgyptTaskReference.md`, `context-egypt.md`, the kernel path references in other documents (still say v1.3), tick T3.

## 2026-10-04 - AdHoc rebuild v0.4 built and verified; housekeeping and reconciliation (no model change)
- **Task:** (1) resolves the entry "AdHoc rebuild v0.4 builder and verifier drafted (not built, not run)": v0.4 was built and verified on Windows (`recalc_and_check_adhoc_v0_4_report.txt`: ALL PASSED; PROTOTYPE 132/132 for FULL and NOPHASE, REBUILD 588/588 against the Python mirror). (2) Wrote `MethodologyNote_v0.4` (current method only), `ResultsComparison_Table2_v0.4` and `VersionNotes_AdHocRebuild.md` (change history, kept out of the methodology). (3) Added NORMS section 7 and an AGENTS.md rule: methodology and version notes are always separate documents. (4) Reconciled stale pointers in README, `instructions-egypt.yaml` (TASK-2a, 2b, D, EF, QUEUE statuses), `context-egypt.md`, `EgyptTaskReference.md` (current-status table at the top) and `TODO.md` (header, T4, Final steps plan). (5) Archived superseded AdHoc files to `egypt/archive/AdHocRebuild/` (workbooks, builders and verifiers v0.1-v0.2; methodology notes and comparisons v0.1-v0.3; make_carveout v0.1-v0.2; make_results_page v0.3-v0.6 and v1.0). Files still needed by live scripts stay in `supporting/AdHocRebuild/` (rebuild v0.3 workbook/builder for the example-results builder; make_results_page v0.7, v1.1, v1.2; make_carveout_v0_3).
- **Inputs:** CAVEATS 2026-10-04 decisions; v0.4 workbook and report; v1.3 kernel and final documents (read-only checks).
- **Reconciliation findings:** (a) The final numbers agree across `EGYPT_CarveOut_Table2_v1.3.md`, the Table 2 CBAM-calc workbook and the kernel `CarveOut_Table2` stored snapshot (K, P, Q, J, N, T checked). (b) The two 2026-10-04 decisions are in the rebuild only, not the final Table 2: final 3B still has the block-only rebate (P 0.64, K -19.1), and final row O is the intensity-only measure, so the FULL decision affects the kernel/rebuild memo only. (c) The CBAM-calc workbook's "Full implementation" (CBF = 1) is what the kernel calls NOPHASE. (d) The v1.3 kernel's Settings title and last log row say v1.0 (no v1.1-v1.3 rows). (e) `EGYPT_FinalCaveats_v1.3` still names rebuild v0.3; the Methodology docx carries before/after material. (f) The CBAM-calc workbook's Table 2 rows are hard-coded.
- **Caveats:** no model or deliverable changed. `.docx` versions of the new notes were produced with `md_to_docx.py` and not opened in Word. The final-steps plan in `TODO.md` lists the decisions needed (D1-D4) before the single confirmation workbook is built.

## 2026-10-04 - Decisions applied everywhere: 3B rebate to all covered industry, one CBAM convention, single confirmation workbook (final set v1.5; builders drafted, not run)
- **Task:** (D1) apply the 3B rebate decision to the final Table 2 and every document; (D2) apply one CBAM convention consistently; (D3) put the single confirmation workbook inside the kernel; (D4) keep EG3 as run for 3A-3C.
- **Method for 3B (new; review it):** `make_carveout_v0_4.py`. In non-block covered industry the output share (1 - s_int = 2/3) of CPAT's response (fuel + proportional IPPU, NB = dInd + dIPPU - r x block) is removed from K (+7.2 Mt); its fuel part enters the deaths adjustment; the rebate tau x (kappa x IND1 - block post-policy fuel) = USD 0.33bn is deducted from revenue, with no feedback onto CPAT receipts. Result, 3B: K -19.1 to -12.0 Mt, P 0.6 to 0.3 $bn, Q 491 to 330; all other scenarios and columns unchanged. 3B net revenue is 0.3, not 0, because EG3 prices only 54% of industry.
- **CBAM convention (D2, interpretation):** Table 2 row O stays the CBAM-product intensity change (EU price and phase-in cancel). The deduction-based memo obligation is on FULL (2030 phase-in, CBAM factor 0.485) with NOPHASE (no phase-in, factor 1) as the other memo, under those names in the kernel, rebuild and documents. The old workbook label "Full implementation" (CBF = 1) was NOPHASE.
- **Outputs:** `egypt/final/` v1.5 documents: `EGYPT_Methodology_v1.5.docx` (3B scope, new section 4.7, history removed), `EGYPT_CarveOut_Table2_v1.5`, `EGYPT_FinalCaveats_v1.5`, `EGYPT_CBAM_ObligationNote_v1.5_NeedsCarolynConfirmation`, `EgyptResultsInitial_UpdatedResults_v1.5_tracked.docx`, `EGYPT_VersionNotes_v1.5` (new, change history), md sources in `md_sources/`. Builders/scripts in `egypt/supporting/AdHocRebuild/`: `make_carveout_v0_4.py` (+ `carveout_v1_5_results.json`), `make_results_page_v1_5.py`, `edit_methodology_v1_5.py`, `check_final_documents.py`. Kernel builders (`cpat_excel_new/standalone_working_version/`): `build_v1_4.py` (T3) then `build_v1_5.py` (3B rule, `Manual inputs` E112, `CarveOut_Table2` section G, new sheet `Table2_Final`). The v1.3 document set and the CBAM-calc workbook (with its script and data) are in `egypt/archive/`.
- **Verification:** `check_final_documents.py`: every Table 2 figure printed in the carve-out note and the results text equals the independent Python mirror (15 rows, 0 failures). The kernel builders have NOT been run (Excel COM, Windows). `build_v1_5.py` refuses to save unless the live kernel equals the mirror, the stored snapshot, the live row O and the printed figures, and the regression over all other cells is 0.
- **Caveats:** (1) `egypt/final/` documents say kernel v1.5, which exists only after `build_v1_5.py` has run (until then `final/` holds kernel v1.3). (2) The new `.docx` files were generated with pandoc / python-docx and not opened in Word. (3) The kernel's prototype composition (`Table2_Industry`, `Rebate_Industry`) still rebates the CBAM block only (reference). (4) The row O definition is still pending Carolyn's confirmation. (5) The 3B non-block rule is an application of CPAT's usage/efficiency split, not a CPAT re-run. (6) Open as before: true full-coverage EG3 run, EF VERIFY list, fp routing.

## 2026-10-04 - `egypt-final/` simplified hand-over folder
- **Task:** new top-level folder `egypt-final/` with a plain, version-free set of the final Egypt deliverables: `1_Summary.docx` (2 pages, plain language), `2_Results_Table.docx`, `3_Methodology.docx` (simplified rewrite), `Egypt_Model.xlsx`, `Egypt_CBAM_Obligations.xlsx`.
- **Inputs:** `egypt/final/` (kernel v1.3, Table 2 carve-out, CBAM calc workbook, methodology v1.3, caveats).
- **Outputs:** the five files above. Nothing in `egypt/` was changed or moved.
- **Caveats:** the two workbooks are byte copies renamed; internal sheet text (ReadMe/Settings version log, builder names) still carries version labels, because Linux cannot recalculate or rebuild them. The three Word files are new text; numbers were copied from `EGYPT_CarveOut_Table2_v1.3.md` and the methodology v1.3 and not independently recomputed. The CBAM-bill workbook is still pending Carolyn's confirmation (stated in the summary). Page counts checked via LibreOffice (summary 2 pages).

## 2026-10-04 - Kernel v1.4 (T3) and v1.5 (3B decision, Table2_Final) built and verified on Windows
- **Task:** resolves the entries "T3 builder drafted" and the v1.5 caveat that the builders had not been run. `build_v1_4.py` and `build_v1_5.py` were run by the user (commits "Minor changes", "Rebuilt to v1.5").
- **Checked after the pull (read-only, openpyxl on the saved v1.5):** sheets include `Table2_Final`; Settings log has rows v1.4 and v1.5; `Manual inputs` E112 = 1 and rows 101-108 hold the T3 values; Check section v1.4 literal count = 0 and v1.5 printed-vs-workbook mismatches = 0 (`Table2_Final` D42 = 0). Final Table 2 stored values: 3B K -11.976, P 0.315, Q 329.8, J 13.921 (others unchanged from v1.3: 1A K -37.39, 2A -33.08, 2B -34.83, 3A -22.77, 3C -33.04). Section D memo: FULL -44.2/-22.9/-23.0/-44.2/-5.0/-53.1, NOPHASE -24.0/-12.2/-12.3/-24.0/-5.1/-36.2.
- **Outputs:** `egypt/final/CPAT_Industry_Kernel_Egypt_v1.5.xlsx` (= `cpat_excel_new/standalone_working_version/` copy); v1.4 in `Old/`; v1.3 in `Old/` and `egypt/archive/`.
- **Caveats:** the builders' own printed regression output was not available to me, so the "regression 0" gate is inferred from the fact that they saved (they abort otherwise). 3B coverage J is 13.921 in the kernel (live kappa) against 13.916 in the documents (rounded to 14); no printed figure changes. Still open: the `egypt-final/` hand-over folder (built from v1.3, shows the old 3B numbers), Word check of the new .docx files, Carolyn's confirmation of row O, EG3 full-coverage run, EF VERIFY list.

## 2026-10-04 - `egypt-final/` updated to v1.5 (3B rebate to all covered industry)
- **Task:** brought the hand-over folder in line with the final set v1.5. `update_egypt_final_v1_5.py` (in `egypt/supporting/AdHocRebuild/`) edited the three Word files in place and replaced the model workbook.
- **Changes:** 3B figures in all three documents (K -19.1 to -12.0 Mt, -3.2 to -2.0% of GHG, revenue 0.6 to 0.3 USD bn, deaths 491 to 330); 3B described as free allowances for all covered industry; new row in the "how the cut is built" table (+7.2 Mt) and a note; a 3B paragraph in the methodology; pointers to the CBAM calculation now say `Egypt_Model.xlsx`, sheet `Table2_Final`. `Egypt_Model.xlsx` = kernel v1.5 (byte copy of `egypt/final/`). `Egypt_CBAM_Obligations.xlsx` removed (retired; its content is in `Table2_Final`).
- **Caveats:** the Word files were edited with python-docx and not opened in Word; the summary was 2 pages before and gained one sentence (page count not re-checked, LibreOffice does not open files in this environment). The 3B column of "how the cut is built" shows rounding (-21.5 + 6.1 - 3.7 + 7.2 = -11.9 against -12.0). The workbook still carries version labels internally (Settings log).

## 2026-10-04 - `egypt-final/simple/Egypt_Simple.xlsx` (plain-words workbook)
- **Task:** a very small workbook for a non-specialist reader: sheet "How it works" (five plain steps), "Results" (six scenarios; final cut built live from four visible lines; CBAM bill as before/after index), "Try it" (one example product, yellow cells = the seven material parameters, green = worked out), and a hidden sheet "Other parameters" holding everything else. Builder: `egypt/supporting/AdHocRebuild/build_simple_workbook.py` (openpyxl, formulas).
- **Inputs:** `carveout_v1_5_results.json` (same source as the v1.5 documents).
- **Caveats:** simplified picture only; the Results numbers are typed from the full model (kernel v1.5), only the sums and the "Try it" example are live. The "Try it" example (cement clinker, USD 20) uses rounded inputs (process saving 6.5%, fuel saving 4.9%) and is illustrative, not a reproduction of the kernel. Not recalculated in Excel here (checked the formulas in Python: final cut equals K for all six scenarios; example gives -5.9% emissions per tonne, -12.4% total).

## 2026-10-04 - Output elasticity: evidence note and recommendation (no model change)
- **Task:** looked for a better basis for the uniform output elasticity -0.5 (`Manual inputs` rows 66-73). Wrote `egypt/supporting/OutputElasticity_Note_v0.1.md/.docx`.
- **Findings:** only cement matters (3.6 of the 3.8 Mt output-channel cut in 1A, because the carbon cost is 15% of the clinker price). Evidence for cement: demand elasticity about -0.02 to -0.16, pass-through 20-40%; steel demand -0.2 to -0.3, pass-through very wide (about 0.5 central); EU ETS firm studies find no detectable output fall. Recommended: cement -0.10 (range -0.03 to -0.30), steel and fertilisers -0.40, aluminium -0.50 (unchanged). Effect (approximate, outside the kernel): 1A cut -37.4 to -34.5 Mt, 3A -22.8 to -19.9, 3C -33.0 to -30.1; 3B unchanged.
- **Caveats:** values are judgements from sourced components (Low-Medium confidence), from web search summaries; the papers could not be opened (egress blocked). Nothing in the kernel or deliverables changed. Decision pending: apply cement -0.10 (kernel rebuild, new carve-out numbers, document updates) or keep -0.5 as a documented placeholder.

## 2026-10-08 - Final set v1.6: product-specific output elasticities (documents on mirror numbers; kernel builder and rebuild v0.5 drafted, not run)
- **Task:** apply cement -0.10 and the full recommended set (steel and fertilisers -0.40, aluminium -0.50; was -0.5 for all) per `OutputElasticity_Note_v0.1`, everywhere. Decisions: full set; one pass with approximate numbers; rebuild v0.5 included; set labelled v1.6.
- **New numbers (mirror, `make_carveout_v0_5.py`), 2030 K Mt old to new:** 1A -37.4 to -34.7; 2A -33.1 to -31.9; 2B -34.8 to -33.7; 3A -22.8 to -20.0; 3B -12.0 unchanged; 3C -33.0 to -30.8. Deaths: 1A 1,501 to 1,440; 2A 1,456 to 1,431; 2B 1,517 to 1,492; 3A 552 to 509; 3C 646 to 607. Revenue 3A 1.5 to 1.6; others within rounding. N 1A/3A -5.8 to -5.7, 2B -2.3 to -2.2, 3C -23.1 to -23.0; T (block emissions) 1A/3A -11.6 to -7.2, 2A -4.7 to -2.9, 2B -4.8 to -3.0, 3C -27.8 to -24.3. O (row O), J, M unchanged.
- **Mirror method:** emissions scale linearly with output, so the stored kernel block rows (policy rows 773-788, product outputs 675-682) and the block process revenue / 3C fund items are rescaled per product by (1 + dp)^eps_new / (1 + dp)^-0.5 and the carve-out arithmetic is rerun. Approximations: the 3C fund shadow price is not re-solved; kernel N is shifted by the change in the output weights; O is unchanged.
- **Outputs:** documents v1.6 in `egypt/final/` (methodology, carve-out note, final caveats, CBAM obligation note, tracked results text, version notes; v1.5 set in `egypt/archive/`), `egypt-final/` (three Word files; `simple/Egypt_Simple.xlsx` with cement default -0.1), scripts `make_carveout_v0_5.py`, `make_documents_v1_6.py`, `edit_methodology_v1_6.py`, `update_egypt_final_v1_6.py`, `build_v1_6.py` (kernel), `build_adhoc_rebuild_v0_5.py` and `recalc_and_check_adhoc_v0_5.py` (rebuild).
- **Verification:** `check_final_documents.py` (printed figures = mirror: 15 rows, 0 failures). Kernel v1.6 and rebuild v0.5 have NOT been built or run (Excel COM). `egypt/final/` still holds kernel v1.5 and `egypt-final/Egypt_Model.xlsx` is still v1.5 until `build_v1_6.py` runs; the documents state v1.6 numbers that come from the mirror.
- **Caveats:** the exact kernel numbers can differ from the mirror (largest expected for 3C, whose fund is re-solved in the kernel); the builder saves anyway, prints "DOCUMENTS MUST BE REGENERATED" if the printed figures differ, and the documents are rebuilt from `carveout_v1_6_results_live.json` (TODO, Final steps). Rebuild v0.5 notes and results are not written yet. Elasticity values are judgements (Low-Medium confidence); citations unverified against the papers.

## 2026-10-08 - Final set v1.6 finalised on the live kernel results
- **Task:** after `build_v1_6.py` and the rebuild v0.5 run (both on Windows, user), regenerated every document from `carveout_v1_6_results_live.json`, finalised the supporting notes and tidied the final folder.
- **Live kernel against mirror:** K, P, Q, T and O agree to rounding; the printed figures that changed are N for 1A/3A (-5.74 mirror to -5.79 live, still printed -5.8), 2B (-2.26, printed -2.3) and 3C (-23.10, printed -23.1), 3C deaths 606 (mirror 607), 3C K -30.82. Kernel `Table2_Final` mismatch count 0; `check_final_documents.py` 15 rows, 0 failures; kernel coverage J is 13.921 (live kappa) against 14 printed.
- **Outputs:** `egypt/final/` (v1.6): kernel, methodology, carve-out note, final caveats, CBAM obligation note, tracked results text, version notes (md sources in `md_sources/`); `egypt-final/` three Word files, `Egypt_Model.xlsx` (= kernel v1.6) and `simple/Egypt_Simple.xlsx` from the live numbers. Final caveats sections A-D now use the rebuild v0.5 and prototype v1.6 figures and no history wording (NORMS section 7). Rebuild notes: `MethodologyNote_v0.5`, `ResultsComparison_Table2_v0.5` (shortened: tables plus qualitative reasons; the old numeric decomposition of the prototype gap was dropped because it could not be recomputed outside Excel); v0.4 notes archived.
- **Caveats:** the new .docx files were generated with pandoc / python-docx and not opened in Word; row O still needs Carolyn's confirmation; evidence-note citations unchecked against the papers; the rebuild/prototype figures in the final caveats are as of the v0.5 / v1.6 runs.

## 2026-10-08 - TODO.md simplified
- **Task:** rewrote `TODO.md` to open work only: three checks for the user (Word check, Carolyn's confirmation of row O, citation check), seven modelling items (full-coverage EG3 run, EF VERIFY list, fp routing, block fuel-intensity channel, fuel-CO2 reconciliation, aligning the kernel's own composition with the 3B decision, items under review) and a short conventions list. Completed T1-T5, D1-D4 and the v1.4-v1.6 steps were removed (history is in this log). README and yaml pointers to TODO updated.
- **Caveats:** none.

## 2026-10-08 - Evidence check, EG3 full-coverage preparation, kernel-increment specs (no model change)
- **Task:** worked through the open modelling list as far as possible without Excel or CPAT.
- **Citations (`OutputElasticity_Note_v0.2`, replaces v0.1 in the archive):** checked by search summaries: EC / CE Delft-Oeko 2016 pass-through (cement 20-40%, steel 55-85%, correcting the earlier "about 0.5"), Ganapati-Shapiro-Walker 2020 (about 0.59 average), Colmer et al. 2025 (14-16% emission cut, no detectable output fall), cement demand (aggregate -0.02 to -0.04, median industry-level -0.10; the -0.16 attribution unconfirmed). Single-source: GTAP Armington values. Not found: a steel demand study and a numeric fertiliser demand elasticity. All fetches of the papers were blocked by the network policy. Methodology (parameter table) and `egypt-final` methodology text corrected for steel pass-through; recommended values unchanged.
- **Methodology wording:** Section 3 and the channel table said the proportional IPPU row "is removed"; now: removed for the CBAM block, kept for non-block IPPU. Typo fixed.
- **EG3 full coverage:** `EG3_FullCoverage_RunSpec_v0.1` (CPAT settings, acceptance check kappa about 1, export, regeneration, statements to rewrite); `cpat_run_constants.py` (reproduces every constant behind the final Table 2 from the csv); `make_carveout_v0_6.py` (mirror on a new csv; reproduces v1.6 on the current csv to 0.006); `build_v1_7.py` (kernel refresh of `CPAT_National`, stored snapshots and `Table2_Final`; drafted, not run). Indicative effect on the final Table 2 (1/kappa proxy): 3A -20.0 to about -29 Mt, 3B -12.0 to -15, 3C -30.8 to -40.
- **Kernel increments:** `KernelIncrements_Spec_v0.1`: fp routing about -0.3 Mt (optional), block fuel-intensity channel (none; double-counting risk with the carve-out; not recommended), 3B alignment of the kernel's own composition (reference sheet; label instead). No builders written for these three.
- **Caveats:** the indicative EG3 numbers are a proxy, not a CPAT result; `build_v1_7.py` has not been run and needs the new csv; the text of `Manual inputs` F66:F68 in the kernel still carries the old steel pass-through wording.

## 2026-10-05 - Kernel v1.7: CPAT_National linked to the new CPAT_Results sheet
- **Task:** in the user's `egypt/final/CPAT_Industry_Kernel_Egypt_v1.7.xlsx` (v1.6 plus a new raw CPAT export sheet `CPAT_Results`, runs EG1-EG5, 6,420 rows), replaced the stored values of `CPAT_National!L6:AE133` (2022-2041) with `=INDEX(CPAT_Results!$A:$AD,MATCH($H6&"_"&$C6,CPAT_Results!$F:$F,0),MATCH(L$5,CPAT_Results!$1:$1,0))` (key = CPAT code & "_" & run in `CPAT_Results` column F; year from row 5). Source column F and the section A band text updated. Done by Excel COM; `build_v1_7.py` was not used.
- **Verification:** all 128 keys found; 2,560 linked cells equal `CPAT_Results` exactly, no errors. 16 keys occur twice in `CPAT_Results` (co2.tot, rev.new.usd); the duplicates are identical, the first is used.
- **Caveats:** the new export changes the baselines as well as EG3 (about 2,060 of 2,560 cells differ from v1.6 in EG1, EG2, EG3 and EG4; e.g. `egy.air.mort` by about 31,000), so the new run is not an EG3-only replacement. EG5 is in `CPAT_Results` but not used. `CarveOut_Table2` (42 cells, from D22/D23: `Table2_Industry!G31/G32 & "|" & run` not found in `CPAT_National`) and `Table2_Final` (16 cells) show #N/A / #DIV/0!; these errors were already present in the v1.7 file before the links and are unchanged. Stored snapshots, documents and `egypt-final/` not refreshed.
