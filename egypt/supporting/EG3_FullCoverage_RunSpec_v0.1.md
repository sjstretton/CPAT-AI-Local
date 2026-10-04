# CPAT run EG3 with full industrial coverage: run specification and regeneration steps (v0.1)

## Why

The CPAT run behind scenarios 3A–3C (EG3) prices only 54% of industrial energy CO₂ (κ = 0.537; the effective carbon price in 2030 is USD 2.8/t against the headline USD 20/t). The methodology says aluminium and other manufacturing were not covered. The final Table 2 uses EG3 as run, so 3A–3C are lower bounds (coverage 14%). A run that prices all industry gives the intended scenario ("Energy CO₂ for all industry plus process emissions in CBAM sectors").

## Settings for the new run (CPAT `MTInputs` / Dashboard parameters)

Same as EG3 except the sector coverage. Parameter names are CPAT's `NameOfParameter`.

| Parameter | Value |
|---|---|
| Carbon pricing start year `CPIntro` | 2028 |
| Starting carbon price `CPLevelStart` | USD 5 |
| Target level `CPLevelTarget` | USD 50 |
| Year to reach target `CPOutro` | 2034 (USD 20 in 2030) |
| Fuel coverage `MCovCoa`, `MCovNga`, `MCovGso`, `MCovDie`, `MCovLpg`, `MCovKer`, `MCovOop` | all True |
| Sector coverage, industry: `MCovMch` (mining & chemicals), `MCovIrn` (iron and steel), `MCovNfm` (non-ferrous metals), `MCovMac` (machinery), `MCovCem` (cement), `MCovOmn` (other manufacturing), `MCovCst` (construction) | all True |
| Sector coverage, everything else: `MCovPow`, `MCovRod`, `MCovRal`, `MCovAvi`, `MCovNav`, `MCovRes`, `MCovFoo`, `MCovSrv`, `MCovFtr`, `MCovOen` | False |
| Revenue recycling | as EG3 (households) |

The existing EG3 sector switches are not recorded in this repository. Open the saved EG3 scenario and compare: the sectors that are False there (expected: `MCovNfm` and `MCovOmn`) are the gap.

## Acceptance check

After the run, in 2030: effective carbon tax trajectory `egy.mit.eff.cptraj.2` ≈ cptraj × (industry energy CO₂ ÷ total energy CO₂) = 20 × 88.97 ÷ 340.66 = **5.22** (it was 2.81). Equivalently κ = min(1, eff.cptraj ÷ cptraj × enr0 ÷ ind0) ≥ 0.99. `python cpat_run_constants.py <csv>` prints κ.

## Export

Export the same 32 CPAT output codes for run EG3 (years 2022–2041) and replace the EG3 rows in `egypt/supporting/AdHocRebuild/cpat_outputs_egypt_2022_2041.csv`. Do not change EG1, EG2 or EG4 (baselines must stay identical across runs). Keep the 128 keys and the column layout.

## Regeneration (after the csv is replaced)

1. `python cpat_run_constants.py` : κ ≈ 1; EG3 receipts, deaths, ΔGHG, ΔEnergy CO₂ listed.
2. `python make_carveout_v0_6.py` : preview of the new final Table 2 (Python mirror; writes `carveout_v1_7_results.json`).
3. Windows, `egypt/supporting/AdHocRebuild`: `python build_adhoc_rebuild_v0_5.py`, then `python recalc_and_check_adhoc_v0_5.py`. The builder reads the csv; with κ = 1 the 1/κ scaling switches itself off, so no setting change is needed.
4. Windows, `cpat_excel_new/standalone_working_version`: `python build_v1_7.py` (refreshes `CPAT_National`, the stored snapshots and `Table2_Final`; saves only if the regression is clean).
5. Regenerate the final documents from `carveout_v1_7_results_live.json`, then rewrite the statements that depend on the partial run (below). The generating scripts for v1.6 (`make_documents_v1_6.py`, `edit_methodology_v1_6.py`, `update_egypt_final_v1_6.py`) are the template for v1.7.

## Indicative effect (before the run)

If the full-coverage run behaves like the 1/κ scaling used in the rebuild and the prototype, the final Table 2 would move as follows (2030; mirror on a synthetic EG3; the real run will differ):

| | 3A | 3B | 3C |
|---|---|---|---|
| Emission cut, Mt: now (as run) | −20.0 | −12.0 | −30.8 |
| Emission cut, Mt: indicative full coverage | −29.3 | −15.1 | −40.1 |
| Revenue, USD bn: now / indicative | 1.6 / 2.4 | 0.3 / 0.6 | 0.4 / 1.3 |
| Deaths avoided: now / indicative | 509 / 716 | 330 / 399 | 607 / 814 |
| Coverage, % of GHG: now / indicative | 13.9 / 20.8 | 13.9 / 20.8 | 13.9 / 20.8 |

1A, 2A and 2B do not change (EG1 and EG2 already price all energy).

## Statements to rewrite after the run

- Final caveats F1 ("3A–3C use CPAT run EG3 as it was run… lower bounds… A true full-coverage EG3 CPAT run is still needed") and caveat A1.
- Methodology 4.7 ("EG3 prices 54% … no scaling to full coverage"; "κ × industry").
- Carve-out note: "Why 3A–3C are low", "Runs", "Coverage J", header sentence.
- Results text: "only about half of industrial energy-related CO₂ is priced, which is why coverage is 14% rather than about 21%"; 3A–3C figures and the ranking sentences.
- `egypt-final/` summary, results table and methodology (the "54%" limit and the footnotes).
- 3B rule: the +7.2 Mt and USD 0.33bn figures (they use κ).
