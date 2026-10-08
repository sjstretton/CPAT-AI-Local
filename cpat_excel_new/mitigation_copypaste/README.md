# Mitigation module - copy-pasteable prototype

Replacement for the CPAT mitigation module whose formulas are **fully copy-pasteable**: one formula per block, valid across (years) and down (subsectors x fuels), and a whole scenario group can be copied to a new scenario. Goal: auditable equations that a model builder can extend by dragging.

Current version: `CPAT_Mitigation_CopyPaste_v0.6.xlsx` (price -> fuel use only). Earlier versions in `Old/`.

## Design (agreed)

| Dimension | Axis | Nest |
|---|---|---|
| Scenario | columns | outer: one group per scenario (output-code column, base year 2022 - column L for scenario 1 as in legacy - and 2023-2035) |
| Year | columns | inner |
| Variable block | rows | outer: Pre-tax price (sp), Tax, After-tax price (atp), Fuel use (ener), Totals |
| Subsector | rows | middle: the 16 CPAT energy-use subsectors |
| Fuel | rows | inner: coa nga gso die lpg ker oop bio (same set for every subsector) |

- **Data step separate from formulas.** Sheet `Inputs` has one row per fuel|subsector (the taxonomy of `Mitigation` columns B:C) with every lookup: mappings, elasticities expanded to fuel|subsector for the selected income group, base prices, base tax, EF, base-year fuel use. `Mitigation` reads it with one short INDEX/MATCH in the four parameter columns D:G (hidden by default) and in the base-year column. Calculation cells hold no lookups.
- **Codes and labels.** Column A holds the variable code (`sp`, `tax`, `atp`, `ener`, ...). Description, unit and source are looked up from sheet `Variables`. Each scenario group starts with a code column that builds the full CPAT code `country.mit.<variable>.<subsector>.<fuel>.<suffix>.<scenario>` (e.g. `egy.mit.ener.rod.gso.e.1`, as in legacy) from the scenario number at its top; later groups number themselves (previous + 1).
- **Roll-up and summary lines.** Green bands have white text. Under each band a white summary line stays visible when the block is rolled up (+/- at the left of that line, or the 1/2 outline buttons): total fuel use (`egy.mit.ener.all.all.e.N`), the policy carbon price in the tax block (`cptraj.ref`), no total for prices (not additive). Blocks open collapsed, totals open.
- **Policy inputs (MTInputs).** Sheet `MTInputs` keeps the legacy row structure, names, units and `NameOfParameter` (columns A:H = template). From column J there is one *Used for calculation* column per scenario (number in row 5, auto-numbered; name in row 6). `Mitigation` rows 9-13 look up the carbon-tax parameters (`CPIntro`, `CPLevelStart`, `CPLevelTarget`, `CPOutro`, `ExtendCarbonPriceBeyondOutro`) by name and scenario number; row 14 computes the carbon price trajectory as legacy CPAT.
- **Parameters are global.** Scenarios differ only in their assumption rows (carbon price); parameters and the carbon price are not changed together.
- **Formulas:** 2023-2034 plain formulas; 2035 calls named LAMBDAs (`PRETAX`, `TAX`, `POSTTAX`, `FUELUSE`; orange) so they can be dragged back over the row.
- Fuel use follows CPAT documentation 3.3.3 (GDP, usage and efficiency price effects, autonomous efficiency with rebound), without the Covid factor and shadow prices. Prices: base pre-tax price plus growth (0 %), tax = base tax + carbon price x EF x coverage.
- Country lookups (`Settings!C4`): elasticities by income group and domestic prices cover all CPAT countries; base-year energy use, GDP growth and EFs are Egypt only so far.

## Files

| File | Role |
|---|---|
| `CPAT_Mitigation_CopyPaste_v0.6.xlsx` | Workbook (formulas only; recalculates on open) |
| `build_v0_6.py` | Builder (reads `templates/MTInputs_template.xlsx`) (openpyxl; no Excel COM needed) |
| `extract_data_v0_1.py` | Writes `data/*.csv` from the legacy workbook, the price-module data and kernel v1.6 (needs `pyxlsb`) |
| `check_v0_6.py` | LibreOffice checks: errors only in the LAMBDA column, one R1C1 formula per block and per label/code column, LAMBDA encoding, LAMBDA expansion and drag-forward vs an independent Python recomputation, scenario-copy test with auto-numbering, expected CPAT codes, row outline, band format and summary lines, MTInputs = template, carbon price vs legacy trajectory, regression vs v0.5 |
| `check_report_v0.6.md` | Output of the last check run |
| `data/` | Extracted source data (non-proprietary) |
| `Old/` | v0.1-v0.5 workbooks, builders, check scripts and reports |

Rebuild: `python extract_data_v0_1.py` (only if sources change), `python build_v0_6.py`, `python check_v0_6.py`.

## Add a scenario

Copy the last scenario column on `MTInputs` one column to the right and edit its inputs (name in row 6). Then copy a whole group on `Mitigation` (scenario 2 = `Z:AM`, code column first) and paste at `AN`. Scenario numbers, names, codes and the carbon price update by themselves.

## Roadmap (buckets)

1. Goal and spec (done, 2026-10-08).
2. Skeleton with working equations, Egypt data: v0.1, revised to v0.2-v0.5 after review - **awaiting review in Excel**.
3. Copy-paste stress test: add a fuel, a subsector and a scenario by dragging; fix what breaks.
4. Policies (bucket 6): 6a MTInputs and the carbon price (v0.6, done); 6b policy wedges by fuel x subsector (carbon tax with MTInputs coverage, excise / fuel price reform, net new policy tax) and a feebate shadow-price block (calculated, not yet used). No ETS yet.
5. Numerical check against legacy CPAT for Egypt.
6. Later: emissions, power, revenue/macro links, Python port.
