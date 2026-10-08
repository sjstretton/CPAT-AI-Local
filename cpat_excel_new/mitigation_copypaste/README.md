# Mitigation module - copy-pasteable prototype

Replacement for the CPAT mitigation module whose formulas are **fully copy-pasteable**: one formula per block, valid across (years) and down (subsectors x fuels), and a whole scenario group can be copied to a new scenario. Goal: auditable equations that a model builder can extend by dragging.

Current version: `CPAT_Mitigation_CopyPaste_v0.8.xlsx` (policies and price -> fuel use). Earlier versions in `Old/`.

## Design (agreed)

Layout follows the legacy CPAT Mitigation sheet: numbered sections **1. Policies**, **3. Power sector** (placeholder), **5. Transport**, **6. Buildings**, **7. Industrial**, **8. Other energy use**, **11. Results - energy consumption**.

| Dimension | Axis | Nest |
|---|---|---|
| Scenario | columns | outer: one group per scenario (output-code column, base year 2022 - column L for scenario 1 as in legacy - and 2023-2035) |
| Year | columns | inner |
| Sector section | rows | outer (sections 5-8), each with a total fuel-use line |
| Subsector | rows | heading line (its total fuel use), the 16 CPAT energy-use subsectors |
| Variable | rows | `sp` pre-tax price, `ctxnew` new carbon tax, `ntx` new excise (fuel price reform), `nce` total new policy, `tax`, `atp` after-tax price, `shp` shadow price on the efficiency margin, `ener` fuel use |
| Fuel | rows | inner: coa nga gso die lpg ker oop bio |

- **Section 1 (policies)** reads the scenario inputs from `MTInputs` (one *Used for calculation* column per scenario from column J; rows A:H = legacy template) by MTInputs row (hidden column D) and scenario number (row 5): carbon tax (`CPIntro`..`CPOutro`, `ExtendCarbonPriceBeyondOutro`), carbon-tax coverage by fuel and sector (`MCov*`), fuel price reform (rows 140-169), feebates (rows 53-64, coverage 66-82). It computes the carbon price (legacy rule), the fuel price reform paths (14 price fuels) and the feebate rate paths (power, transport, residential, industry). One default for all paths: 0 before the start year, linear to the target, continuing linearly afterwards (the carbon price keeps its MTInputs switch). Shadow prices: by sector ($/tCO2, legacy rows 2345-2349) = feebate path (later + non-auctioned ETS, regulations); share impacting efficiency by subsector (`ssc`, legacy rows 2403-2419) = feebate coverage x adjustment (1.0 for feebates).
- **Wedges:** `ctxnew` = carbon price x EF x fuel coverage x sector coverage; `ntx` = fuel price reform path / GJ per price unit; `nce` = `ctxnew` + `ntx`; `tax` = base tax + `nce`; `shp` = sector shadow price x EF x `ssc`. Fuel use: the usage term uses `atp`, the efficiency term `(atp + shp)` (legacy / `cpat_coded` `ec.py`). No ETS yet.
- **Data step separate from formulas.** Sheet `Inputs` (one row per fuel|subsector) holds every lookup; `Mitigation` reads it in the hidden parameter columns D:G (labels in `Variables` G:J) and the base-year column. Calculation cells hold no searching lookups; `ctxnew`, `ntx` and `shp` pick a Section-1 row by position with `INDEX(range, position)`.
- **Copy-pasteable:** every variable has one formula (relative R1C1) across all subsectors, fuels, years and scenarios; 2035 calls named LAMBDAs (`PRETAX`, `TAX`, `POSTTAX`, `FUELUSE`) for `sp`, `tax`, `atp`, `ener`.
- **Codes and labels.** Column A holds the variable code; description, unit and source come from `Variables`; each scenario group starts with a code column building `country.mit.<variable>.<subsector>.<fuel>.<suffix>.<scenario>` (e.g. `egy.mit.ener.rod.gso.e.1`).
- **Roll-up.** Sector sections show their total and the subsector heading lines; + on a heading opens its variables. Section 1 shows the carbon price, its inputs and paths are rolled up. Green section bands have white text.
- **Parameters are global**; scenarios differ only in their MTInputs columns. Country lookups via `Settings!C4` (elasticities and prices for all CPAT countries; energy use, GDP and EFs Egypt only).

## Files

| File | Role |
|---|---|
| `CPAT_Mitigation_CopyPaste_v0.8.xlsx` | Workbook (formulas only; recalculates on open) |
| `build_v0_8.py` | Builder (reads `templates/MTInputs_template.xlsx`) (openpyxl; no Excel COM needed) |
| `extract_data_v0_1.py` | Writes `data/*.csv` from the legacy workbook, the price-module data and kernel v1.6 (needs `pyxlsb`) |
| `check_v0_8.py` | LibreOffice checks: errors only in the LAMBDA column, one R1C1 formula per block and per label/code column, LAMBDA encoding, LAMBDA expansion and drag-forward vs an independent Python recomputation, scenario-copy test with auto-numbering, expected CPAT codes, row outline, band format and summary lines, MTInputs = template, carbon price vs legacy trajectory, fuel price reform and feebate test scenarios (feebates lower fuel use only where covered), regression vs v0.7 on shared output codes |
| `check_report_v0.8.md` | Output of the last check run |
| `data/` | Extracted source data (non-proprietary) |
| `Old/` | v0.1-v0.7 workbooks, builders, check scripts and reports |

Rebuild: `python extract_data_v0_1.py` (only if sources change), `python build_v0_8.py`, `python check_v0_8.py`.

## Add a scenario

Copy the last scenario column on `MTInputs` one column to the right and edit its inputs (name in row 6). Then copy a whole group on `Mitigation` (scenario 2 = `Z:AM`, code column first) and paste at `AN`. Scenario numbers, names, codes and the carbon price update by themselves.

## Roadmap (buckets)

1. Goal and spec (done, 2026-10-08).
2. Skeleton with working equations, Egypt data: v0.1, revised to v0.2-v0.5 after review - **awaiting review in Excel**.
3. Copy-paste stress test: add a fuel, a subsector and a scenario by dragging; fix what breaks.
4. Policies (bucket 6): 6a MTInputs and the carbon price (v0.6, done); 6b policy wedges and legacy section layout (v0.7, done); shadow price on the efficiency margin (v0.8, done). Next: ETS, regulations as shadow prices, subsidy phase-out.
5. Numerical check against legacy CPAT for Egypt.
6. Later: emissions, power, revenue/macro links, Python port.
