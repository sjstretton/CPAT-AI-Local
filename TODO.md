# TODO — CPAT Industry Kernel (Egypt) — queued tasks

Status key: ☐ not started · ◐ in progress · ☑ done.
Latest mainline workbook: `cpat_excel_new\standalone_working_version\CPAT_Industry_Kernel_Egypt_v1.3.xlsx` (identical copy in `egypt\final\`); the final Table 2 is its sheet `CarveOut_Table2`. Done: T1, T2, T5 adoption (kernel v0.15-v0.16). Open: T3 (v1.4) and the 3B decision with `Table2_Final` (v1.5) are done; open: true full-coverage EG3 CPAT run, fp routing, block fuel-intensity channel, EF VERIFY list; see Final steps at the end of this file. `Manual inputs` uses rows up to 95 and `Check` rows up to ~1920, so T3 rows start at 98.
Stream‑2 branch: merged into v0.12 (T2) and closed; branch workbooks `…v0.7branch_Stream2_v1/v2/v3.xlsx` are in `Old\`, builders `build_stream2_v1/v2/v3.py` stay in place (imported by `build_v0_12.py`).

Conventions that apply to **every** task below (see `NORMS.md`, `egypt\instructions\instructions-egypt.yaml`):

- Never edit a shipped version in place. Copy the previous workbook to `Old\`, create `CPAT_Industry_Kernel_Egypt_v0.<n+1>.xlsx` with a matching `build_v0_<n+1>.py` that opens the prior file, applies changes via Excel COM (`win32com`, as the existing builders do — `from build_v0_4 import BLOCKS, DATA_COLS, REVIEW, TAN, col, copy_formats`) and saves the new file. Run builders from the `standalone_working_version` folder in a normal (non‑sandboxed) shell; Excel COM `Workbooks.Open` fails from the Copilot sandbox.
- Every new input gets: a code (`<cty>.<module>.<var>.<sector>…` pattern already used in column C/D), a source string and a confidence rating (High/Medium/Low), coloured per the sheet legend (TAN = assumption, REVIEW = needs review).
- Append a row to the version log in `Settings` (rows 28–36 in v0.9; v0.9 is row 36 → next is row 37). Do **not** extend the `Settings` sheet list (rows 17–25) — Stream‑1 builders assert on those row positions; add new sheets to the note text instead.
- Regression: run every item in the `Check` sheet before/after; pre‑policy (baseline) rows must be numerically identical unless the task says otherwise; record max abs diff in the version‑log row.
- Update `egypt\instructions\instructions-egypt.yaml` (TASK‑1 `notes` version list + the task entry), `egypt\instructions\EgyptTaskReference.md` and `egypt\instructions\context-egypt.md` key‑files table. Tick the box here.
- Do not commit unless explicitly asked.

---

## ☑ T1 — Apply Task D (IPCC process‑emission half‑elasticities) to the latest kernel

**Done in v0.15** (`build_v0_15.py`, together with T5): E50 = IPCC; rows 53–60 ERmax / P* = 100 / ER* = IPCC central (DRI 0.3433, scrap 0.1810, BF 0.2803, clinker 0.3352, AN no 0.6179 blend, Al 0.2164 np+no, NH₃/urea 0); o15/o16 formula bug fixed. Spec mapping recorded in `TASK-D_ProcessHalfElasticities_DropIn_v0.2.md`. See CAVEATS 2026-10-02 T1 + T5.

**Goal.** Replace the placeholder process‑emission response parameters in `Manual inputs` rows 53–60 with the IPCC‑AR6‑derived values, and switch the model to use them.

**Inputs.**
- Central spec: `egypt\supporting\TASK-D_ProcessHalfElasticities_DropIn_v0.1.md` (convention, table, alternatives, caveats). Note the spec was written against the v0.8 layout (`E40:F47`); the v0.9 mapping is given below and should be copied into the spec as §2.3 / v0.2.
- Derivation: `egypt\supporting\ProcessEmissions_CarbonPrice_Response\ProcessEmissions_CarbonPriceResponse.xlsx` (sheets `Results`, `SemiElasticity`, `CPAT_v0.8_Table`) and `…_Report.md|.docx` (§7 options, Appendix D). Generator: session artifact `build_process_report.py`.
- Target: `Manual inputs` sheet of v0.9 (or later).

**v0.9 layout (what you are filling).**

| Cell / range | Content |
|---|---|
| `E50` | Selector: `"IPCC"` uses rows 53–60; `"ADHOC"` uses the v0.8 table in rows 40–47 with ERmax = 1 (reproduces v0.8). Set to `"IPCC"`. |
| Rows 53–60 | Products in order: DRI‑EAF steel, Scrap‑EAF steel, BF‑BOF steel (reference), Grey clinker (dry‑process), Ammonia (net merchant), Urea, Ammonium nitrate, Primary aluminium. |
| `E` `F` `G` `H` | **np** (non‑process‑gas = process CO₂): ERmax, anchor price P\* (USD/t), ER at P\*, β = `IF(OR(E=0,G=0),0,-LN(1-G/E)/F)` (formula — leave). |
| `I` `J` `K` `L` | **no** (non‑CO₂ process gas: N₂O, PFC): same four columns. |
| `M:P` | Derived (semi‑el at P=0 = ERmax·β; ER at $20) — formulas, leave. |
| `Q`, `R` | Lever / source text for np and no. |
| `S` | Confidence. |
| `T:W` | Effective β.np, ERmax.np, β.no, ERmax.no via `=IF($E$50="ADHOC",…,H53)` — formulas, leave. |

Model: `ER(P) = ERmax · (1 − exp(−β·P))`, P = process‑emission carbon price (`Mitigation_Industry` row o65 flags × o63 price trajectory + ETS), applied in the CBAM block rows o118–o125 of both scenario blocks.

**Values to enter (Option A — "isoelastic/exponential, ERmax = 1").** Keeps the v0.8 convention exactly (β = −LN(1−ER)/100): set ERmax = 1, P\* = 100, ER\* = central ER at $100 from the TASK‑D table. Assign each product's response to **one** category; set the other category's ERmax = 0 (β then evaluates to 0).

| Row | Product | np: ERmax / P\* / ER\* | no: ERmax / P\* / ER\* | Notes |
|---|---|---|---|---|
| 53 | DRI‑EAF steel | 1 / 100 / **0.3433** | 0 / 100 / 0 | process CO₂ (DRI reductant + EAF carbon); β = 0.004205 |
| 54 | Scrap‑EAF steel | 1 / 100 / **0.1810** | 0 / 100 / 0 | electrode/charge carbon, lime; β = 0.001997 |
| 55 | BF‑BOF steel (reference) | 1 / 100 / **0.2803** | 0 / 100 / 0 | reference only (Egypt volume 0); β = 0.003289 |
| 56 | Grey clinker | 1 / 100 / **0.3352** | 0 / 100 / 0 | calcination CO₂ (clinker substitution, CCS); β = 0.004083 |
| 57 | Ammonia (net) | see note | 0 / 100 / 0 | v0.9 treats SMR CO₂ as **fp** (fuel/feedstock), np = 0. Decision required: either (i) leave np ERmax = 0 (no process response; fuel response handled by fuel half‑elasticity rows 40–47), or (ii) enter 1 / 100 / **0.2974** and have the builder route the np β to the feedstock‑CO₂ line. Record the choice in `Q57`. |
| 58 | Urea | see note | 0 / 100 / 0 | np is negative in v0.9 (CO₂ uptake credit); abatement of ammonia feedstock CO₂ reduces the credit's base. Default: ERmax = 0 and note "response inherits from ammonia (0.1158 central at $100 for net‑urea chain) — not applied separately to avoid double counting". |
| 59 | Ammonium nitrate | 0 / 100 / 0 | 1 / 100 / **0.7210** | HNO₃ N₂O (unabated plant baseline). If `Manual inputs!K36` (existing N₂O abatement share) > 0, use the abated‑baseline value **0.3292** instead (TASK‑D §2.2). β = 0.012765 / 0.003993 |
| 60 | Primary aluminium | 1 / 100 / **0.1282** | 1 / 100 / **0.1078** | Split of the combined 0.2164: anode CO₂ via inert anodes (np) and PFC via anode‑effect control (no). Derivation: option‑level ER at $100, mean of 2030 & LR: inert anodes 0.0109/0.2455 → 0.1282; PFC control 0.0588/0.1568 → 0.1078. Check the kernel's aluminium `no` EF covers PFCs only. |

Text for `Q`/`R`: `"IPCC AR6 WGIII Table 11.3/12.3 cost‑bucket MACC, central (mean 2030 & LR), USD2019. Derivation: egypt/supporting/ProcessEmissions_CarbonPrice_Response; drop‑in spec TASK‑D v0.1. Lever: <lever>."` `S`: `Medium` (steel, clinker, AN‑unabated), `Low` (aluminium split, ammonia/urea, Scrap‑EAF).

**Option B — saturating form (recommended as a sensitivity, optionally default).** Uses the model's ERmax properly: ERmax = A, β = 1/τs fitted to a($100) and a($200) (report §Results, saturating block). P\* and ER\* then are P\* = 100, ER\* = central a(100), ERmax = A:

| Product | ERmax (A) | β (per $) | ER\* at $100 |
|---|---|---|---|
| DRI‑EAF | 0.4079 | 0.01843 | 0.3433 |
| Scrap‑EAF | 0.3994 | 0.00604 | 0.1810 |
| BF‑BOF | 0.3874 | 0.01285 | 0.2803 |
| Clinker | 0.4325 | 0.01492 | 0.3352 |
| Ammonia | 0.4433 | 0.01112 | 0.2974 |
| Urea | n/a (fit degenerate, A>1) — use Option A or inherit from ammonia | — | 0.1158 |
| AN unabated / abated | 0.7391 / 0.4142 | 0.03712 / 0.01584 | 0.7210 / 0.3292 |
| Aluminium (combined) | 0.3720 | 0.00872 | 0.2164 |

Enter ERmax in `E`/`I`, P\* = 100 in `F`/`J`, ER\* in `G`/`K`; column `H`/`L` recomputes β (should match the table to 3 s.f. — verify). If both options are wanted, add a second selector value (e.g. `"IPCC_SAT"`) and a second block of rows (≥ 62) rather than overwriting.

**Procedure.**
1. Copy v0.9 → `Old\`, create `build_v0_10.py` (from `build_v0_9.py` skeleton), SRC = v0.9, DST = v0.10.
2. Write `E50 = "IPCC"`; write E/F/G and I/J/K rows 53–60 per Option A (or B); write Q/R/S text; recolour to the "input, sourced" colour (not TAN/REVIEW).
3. Resolve the AN baseline: read `K36`; choose 0.7210 vs 0.3292; document in `R59`.
4. Price basis: IPCC costs are USD2019; the kernel price trajectory is nominal/2024 USD. Either deflate P\* to 122 (USD2024 equivalent of $100 USD2019) in `F`/`J`, or add a note. Decide once, apply to all rows, document in `Settings` version log.
5. Caveat from v0.8: the same table (rows 40–47) drove **both** fuel ER (Mitigation_Industry 352–359) and process ER (363–370). In v0.9 the fund placeholder rows o107–o114 still read rows 40–47. Confirm T1 leaves fuel/fund paths untouched (they are Task G/J) and note this in the version log.
6. Regression: with `E50="ADHOC"` results must equal v0.9 exactly (max diff 0). With `"IPCC"`, only the CBAM process rows o118–o125 (both blocks) and downstream aggregates change; baseline (pre‑policy, P = 0) rows unchanged. Add a `Check` line "Task D applied: E50=IPCC, ER(100) row 53 = 0.3433 ± 1e‑6".
7. Bookkeeping: `Settings` version log row 37; yaml TASK‑D `status: applied_v0.10`, `target: Manual inputs rows 53–60`; `EgyptTaskReference.md` item 1b ☑; retarget `TASK-D_…_v0.1.md` → v0.2 with this mapping; tick here.

---

## ☑ T2 — Merge Stream 1 (mainline) and Stream 2 (Task F energy‑CO₂ branch)

**Done 2026‑10‑02 → v0.12** (`build_v0_12.py`, from v0.11 + Stream2 v1/v2/v3 = Tasks F, I, J). See the `CAVEATS.md` entry for the merge notes and differences from the procedure below.

**Goal.** Bring the Stream‑2 additions (fuel emission factors and sector energy‑CO₂ accounting) onto the latest mainline so there is a single workbook lineage again.

**Inputs.**
- Mainline: v0.9 (or v0.10 if T1 lands first — preferred order is T1 → T2 → T3, but T2 and T3 are independent of T1).
- Branch: `CPAT_Industry_Kernel_Egypt_v0.7branch_Stream2_v1.xlsx`, builder `build_stream2_v1.py` (built from `Old\…v0.7`).

**What Stream 2 adds (all additive — new sheets or appended rows only).**
- Sheet `Data_EF` (inserted after `Data_Elast`): fuel CO₂ EFs in tCO₂/ktoe = IIASA tCO₂/GJ × 41 868 × 0.9296150140376861 (oxidation/unit factor); codes `egy.mit.efc.<fuel>`.
- Sheet `Emissions_Industry` (after `Mitigation_Industry`): per scenario (1 = baseline, 2 = policy) and sector (irn, cem, nfm, mch): 9 fuel rows `eco2 = ener × EF / 1e6` (MtCO₂), codes `egy.mit.eco2.<sector>.<fuel>.e.<s>`, plus a total row.
- `Check` section "Task F (Stream2 v1)" items (a)–(d).
- `Settings`: title text, `C25` note, version‑log row. `Scenarios`: one note line. `MTInputs`: cell colouring.
- Layout assumptions baked into the branch builder: energy rows = sector header row + 49..+57; sector header rows `{1: (5, 65, 125, 185), 2: (404, 464, 524, 584)}`; `PRICE_ROW = 645`.

**Procedure.**
1. Verify layout assumptions against the mainline target: open v0.9/v0.10 and assert the sector header rows and `ener` row offsets above still hold (v0.8→v0.9 inserted rows in `Manual inputs`, not in `Mitigation_Industry`; confirm). If they moved, parametrise `build_stream2_v1.py` (HEADERS, PRICE_ROW) rather than hard‑coding.
2. Refactor `build_stream2_v1.py` so its steps are importable functions taking `(wb)`; create `build_v0_11.py` (or v0.10 if T1 has not run) that opens the mainline file, calls those functions, and saves. Do **not** build from the branch file — the branch is v0.7‑based and lacks Task D rows.
3. Sheet order: `Data_EF` after `Data_Elast`; `Emissions_Industry` after `Mitigation_Industry`. Do not add to the `Settings` sheet list rows 17–25; mention the two sheets in the `C25` note / version‑log text.
4. Merge the `Settings` version log: keep all Stream‑1 rows; append one row "v0.1x — merged Stream 2 v1 (Task F: Data_EF, Emissions_Industry)". Append the Stream‑2 `Check` section after the existing Stream‑1 sections.
5. Regression: (i) all Stream‑1 `Check` items unchanged; (ii) Stream‑2 items (a)–(d) pass; (iii) `Emissions_Industry` totals for scenario 1 equal those in the branch file where inputs are identical (energy inputs unchanged between v0.7 and v0.9 — confirm; if not, explain the diff); (iv) no `#REF!`/`#NAME?` anywhere (scan all sheets).
6. Retire the branch: move `…v0.7branch_Stream2_v1.xlsx` and `build_stream2_v1.py` to `Old\` (keep; do not delete). Note in the mainline `Settings` that Stream 2 is merged and the branch is closed.
7. Bookkeeping: add a `TASK-F` entry to `instructions-egypt.yaml` (status merged, version), update TASK‑1 `notes`; `EgyptTaskReference.md`; `context-egypt.md` (prototype path still says v0.3 — update to latest); tick here.

---

## ☑ T3 — Move hard‑coded CBAM market data from `Mitigation_Industry` into `Manual inputs`

**Done 2026-10-04 in kernel v1.4 (`build_v1_4.py`, run on Windows; regression 0, Check literal count 0, Settings row v1.4).** Corrections to the plan below: `Manual inputs` is no longer 60 rows long (rows 62-95 are used by the output-response, CBAM-obligation and IPPU sections), so the new section is at rows 98-108 (title 98, note 99, header 100, products 101-108); the latest workbook is v1.3, not v0.9; Settings log last row is 45. Run on Windows; it aborts without saving unless the regression diff and the literal-count Check are both 0. Then do the bookkeeping in step 7 and tick this item.

**Goal.** No market/production constants in the calc sheet. All CBAM product data entered once in `Manual inputs` with code/source/confidence, and linked from both scenario blocks.

**What is hard‑coded today (v0.9), duplicated verbatim in both scenario blocks.**

| Item | Baseline block | Policy block | Values (rows in product order DRI‑EAF, Scrap‑EAF, BF‑BOF, Clinker, Ammonia, Urea, AN, Aluminium) |
|---|---|---|---|
| 2024 production, kt | `F276:F283` | `F675:F682` | 5100, 4800, 0, 50000, 1785, 2800, 600, 300 |
| Production growth, %/yr | `G276:G283` | `G675:G682` | 0.044, 0.044, 0, 0.033, 0.022, 0.022, 0.022, 0.055 |
| 2024 total exports, kt | `H276:H283` | `H675:H682` | blank (placeholder column) |
| 2024 EU exports, kt | `I276:I283` | `I675:I682` | 580, 300, 0, 800, 120, 1600, 80, 167 |
| Pre‑policy product price, USD/t | `G288:G295` | `G687:G694` | 750, 680, 620, 110, 450, 380, 320, 2400 (codes `all.in.ppx.<prod>.---`) |

Surrounding formulas to preserve: `N276 = IF(UPPER(Settings!$B$3)="EGY",F276,0)` (country switch), `L:M` back‑cast from 2024 by growth, `L288:AI295 = $G288` (flat price path). Other CBAM inputs (EU default EFs `W:Z`, pass‑through, export shares) are already in `Manual inputs` — confirm with a scan for numeric literals in columns F:AI of rows 245–400 and 644–799 (the scan used to write this list found only the cells above plus zero‑filled `machinery` rows 377/388/776/787, which are fine).

**Procedure.**
1. New builder `build_v0_1x.py` from the latest mainline.
2. Add a `Manual inputs` section starting at row 62 (sheet currently ends at row 60; leave row 61 blank): title "CBAM product market data (Task T3)", header row, then 8 product rows in the same product order as rows 53–60. Columns: `D` product, `E` 2024 production kt, `F` growth %/yr, `G` 2024 total exports kt, `H` 2024 EU exports kt, `I` pre‑policy price USD/t, `J` code (`egy.in.prod.<prod>`, `egy.in.prodg.<prod>`, `egy.in.expt.<prod>`, `egy.in.expeu.<prod>`, `all.in.ppx.<prod>.---` — reuse the existing price codes), `K` source, `L` confidence. Colour TAN (assumption) until sources are attached; current sources are the v0.7 ad hoc assumptions — say so.
3. In `Mitigation_Industry`, replace each literal with a direct link (`='Manual inputs'!E64` etc.) in **both** blocks. Prefer direct cell links over INDEX/MATCH (consistent with the rest of the sheet); keep the `N` country switch and the `L:AI` path formulas untouched.
4. Recolour the replaced calc‑sheet cells from input colour to formula/link colour per the legend.
5. Regression: full workbook values identical before/after (max abs diff = 0 across `Mitigation_Industry`, `Check`, outputs). Add a `Check` line: "T3: no numeric literals in Mitigation_Industry F:I rows 276–283/675–682 and G288:G295/G687:G694" (can be implemented as `=ISFORMULA()` AND over those ranges).
6. Optional follow‑up (separate task): source real 2024 Egypt production/export data (CAPMAS, UN Comtrade CN codes already listed in rows 288–295 labels) to replace the ad hoc values; raise confidence from Low.
7. Bookkeeping: `Settings` version‑log row; yaml (new `TASK-T3` entry + TASK‑1 notes); `EgyptTaskReference.md`; tick here.

---

## ☐ T4 — Follow-ups from the TASK-2b ad hoc rebuild (`egypt\supporting\AdHocRebuild\`)

Source: `AdHocCalculations_Rebuild_v0.1.xlsx` (ReadMe / Issues resolved / Checks) and `MethodologyNote_v0.1.md` §6. Not kernel work by themselves; listed so they are not lost.

- ☐ **Re-run CPAT EG3 with full industry coverage.** The industry run prices only κ = 0.54 of industrial energy CO₂ (aluminium, other manufacturing excluded), which drives J = 14 % and the 3A/3B/3C fuel-side results. After the re-run: replace `CPAT_Outputs` (via `cpat_outputs_egypt_2022_2041.csv`), set `Inputs!KappaMode = ONE`, rebuild with `build_adhoc_rebuild_v0_1.py` → v0.2, re-verify with `recalc_and_check_adhoc.py`.
- ☑ **3B rebate scope and O convention: decided 2026-10-04** (see CAVEATS): `Inputs!ThetaOther` = 1 (rebate to all covered industry, P ≈ 0) and O on FULL (NOPHASE kept as memo only). ☑ Applied to the AdHoc rebuild v0.4 (built and verified on Windows, ALL PASSED; `MethodologyNote_v0.4`, `ResultsComparison_Table2_v0.4`, `VersionNotes_AdHocRebuild.md`). ☐ Not yet applied to the final Table 2 or the kernel: see Final steps, decision D1 (3B) and D2 (O).
- ☑ **AdHoc rebuild v0.2** on Egypt EF v0.1 + AN blended β (`build_adhoc_rebuild_v0_2.py`, `MethodologyNote_v0.2`); EG3 full-coverage re-run still pending (would be v0.3).
- ☑ **Kernel Task M** — Table 2 snapshot refilled in v0.15 after T1 (T3 still pending); done in v0.14 (`build_v0_14.py`, sheets `CPAT_National`, `Table2_Industry`) before T1/T3, composed in deltas with the kernel's own responses (see CAVEATS 2026-10-02 Task M); re-run once T1/T3 land. Original item: port the national composition (K = ΔGHG − ΔIPPU + ΣER_p + Σemrq_proc + D_obr + F_fund, κ coverage, revenue net of rebates/fund, deaths rescaling) from `Results` into the kernel once T1/T3 are done, so Table 2 comes from one workbook.
- ☐ Keep β set (`BetaSet` = IPCC, Task D) and σ = 20 $/t under review; fund outlay bound (0.19 $bn) ≪ 3C budget (1.47 $bn).

---

## ◐ T5 — Adopt the Egypt emission factors (Task EF v0.1) in the kernel

Source: `egypt\supporting\EmissionFactors\EGY_CBAM_EF_Methodology_v0.1.md` §5/§10 (`Products!D:G` → `'Manual inputs'!H30:K37`); integrated method `egypt\archive\EGYPT_Methodology_v1.0.md` App. A, App. B.5.

- ☑ Conventions decided (v0.15, provisional): urea np = 0 (CBAM rule); AN N₂O folded into own no = 0.9944.
- ☑ New kernel increment v0.15 (`build_v0_15.py`): H30:K37 from the EF workbook with sources/tiers in AD/AE; S:V memo restated. Regression explained in the Settings log row 42 and CAVEATS.
- ◐ Fuel-CO₂ reconciliation: clinker fc now 0.3136; the cement gap widens (Task G info rows) — not yet resolved.
- ☑ AdHoc rebuild v0.2 on the new EFs. ☐ Routing the NH₃ CCS β to fp (App. B.5) not implemented (NH₃/urea β = 0).
- ☐ Work through the VERIFY list (App. A.6) before treating the values as final.

---

## Order and dependencies

```
T1 (Task D values)  ──►  T2 (merge Stream 2)  ──►  T3 (inputs to Manual inputs)  ──►  T4 (rebuild follow-ups / Task M)
T5 (EF v0.1 adoption) ── alongside T1 (β routed to fp) ──►  T4 (rebuild v0.2 on new EFs)
```
T1→T2→T3 was the recommended order; T2 ran first (v0.12), so T1 and T3 now build on v0.12. T3's `Manual inputs` additions do not touch the Stream‑2 row assumptions.

## Cross‑references
- Task D spec: `egypt\supporting\TASK-D_ProcessHalfElasticities_DropIn_v0.1.md`
- TASK-2b rebuild: `egypt\supporting\AdHocRebuild\` (workbook, builder, verifier, methodology note)
- Task inventory: `egypt\instructions\instructions-egypt.yaml`, `egypt\instructions\EgyptTaskReference.md`
- Norms: `NORMS.md`


---

## Final steps (decisions taken 2026-10-04; one workbook that confirms the final numbers)

Decisions: **D1** the 3B rebate to all covered industry applies everywhere (final Table 2, documents, rebuild, kernel). **D2** one CBAM convention everywhere: Table 2 row O is the CBAM-product intensity change (no deduction); the deduction-based memo obligation is reported on FULL (2030 phase-in, factor 0.485) with NOPHASE (no phase-in, factor 1) as the other memo, under those names only. **D3** the single workbook is the kernel (v1.5, sheet `Table2_Final`). **D4** 3A-3C use EG3 as run (J = 14 %) until a true full-coverage EG3 run exists.

Result of applying D1: final 3B = revenue 0.3 $bn (was 0.6), K -12.0 Mt (was -19.1), deaths 330 (was 491); nothing else changes. Method: `make_carveout_v0_4.py` (3B rule), documented in Methodology section 4.7 and carve-out note.

1. ☑ **`build_v1_4.py` (T3) run on Windows.** Gate: regression diff 0 and literal-count Check 0. Then bookkeeping (tick T3).
2. ☑ **`build_v1_5.py` run on Windows** (kernel v1.5 in `egypt/final/`; `Table2_Final` mismatch count 0) (needs kernel v1.4 in `standalone_working_version`). It applies the 3B rule in `CarveOut_Table2` (section G, `Manual inputs` E112), adds `Table2_Final`, loops the six scenarios, and saves only if: live 3B = Python mirror (`carveout_v1_5_results.json`), live = stored for the other five, live row O = stored, regression over all other cells = 0, printed-vs-workbook mismatches = 0. It then copies the kernel to `egypt/final/` and moves kernel v1.3 to `egypt/archive/`. Then CAVEATS entry (result), yaml (builders run), commit.
3. ☑ **Documents v1.5** generated from the same mirror: carve-out note, final caveats, CBAM obligation note, tracked results text (`make_results_page_v1_5.py`), methodology (`edit_methodology_v1_5.py`: 3B scope, section 4.7, history removed), `EGYPT_VersionNotes_v1.5`. `check_final_documents.py` confirms the printed Table 2 figures equal the mirror (15 rows, 0 failures). The v1.3 set and the retired CBAM-calc workbook are in `egypt/archive/`.
4. ☐ **Open after the run:** open the new .docx files in Word (not done here); Carolyn's confirmation of the row O definition; the kernel's own prototype composition (`Table2_Industry`, `Rebate_Industry`) still rebates the CBAM block only and is reference material, not the final Table 2; EG3 full-coverage CPAT run; EF VERIFY list.
