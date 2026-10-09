# Mitigation module - copy-pasteable prototype

Replacement for the CPAT mitigation module whose formulas are **fully copy-pasteable**: one formula per block, valid across (years) and down (subsectors x fuels), and a whole scenario group can be copied to a new scenario. Goal: auditable equations that a model builder can extend by dragging.

Current version: `CPAT_Mitigation_CopyPaste_v0.12.xlsx` (policies incl. new ETS and feebates with sectoral shadow prices, domestic prices with existing taxes and subsidies, price -> fuel use, revenues, 2022-2040). Earlier versions in `Old/`. Price method and the explicit real/nominal assumptions: `PriceProjection_Method_v0.4.md`. Differences with legacy CPAT: workbook sheet `LegacyDiff`. Data changed by assumption (other oil products, VAT rate) is bright yellow with red text in `Inputs_prices`.

## Design (agreed)

Layout follows the legacy CPAT Mitigation sheet: numbered sections **1. Policies**, **2. Retail energy prices**, **3. Power sector** (placeholder), **5. Transport**, **6. Buildings**, **7. Industrial**, **8. Other energy use**, **11. Results - energy consumption**.

| Dimension | Axis | Nest |
|---|---|---|
| Scenario | columns | outer: one group per scenario (output-code column, base year 2022 - column L for scenario 1 as in legacy - and 2023-2035) |
| Year | columns | inner |
| Sector section | rows | outer (sections 5-8), each with a total fuel-use line |
| Subsector | rows | heading line (its total fuel use), the 16 CPAT energy-use subsectors |
| Variable | rows | `ctxnew` new carbon tax, `ets` new ETS permit cost, `ntx` new excise (fuel price reform), `nce` total new policy, `atp` after-tax price, `shp` shadow price on the efficiency margin, `ener` fuel use |
| Fuel | rows | inner: coa nga gso die lpg ker oop bio |

- **Section 1 (policies)** reads the scenario inputs from `MTInputs` (one *Used for calculation* column per scenario from column J; rows A:H = legacy template) by MTInputs row (hidden column D) and scenario number (row 5): carbon tax (`CPIntro`..`CPOutro`, `ExtendCarbonPriceBeyondOutro`), carbon-tax coverage by fuel and sector (`MCov*`), fuel price reform (rows 140-169), feebates (rows 53-64, coverage 66-82). It computes the carbon price (legacy rule), the fuel price reform paths (14 price fuels) and the feebate rate paths (power, transport, residential, industry). One default for all paths: 0 before the start year, linear to the target, continuing linearly afterwards (the carbon price keeps its MTInputs switch). Shadow prices: by sector ($/tCO2, legacy rows 2345-2349) = feebate path (later + non-auctioned ETS, regulations); share impacting efficiency by subsector (`ssc`, legacy rows 2403-2419) = feebate coverage x adjustment (1.0 for feebates).
- **Real terms (v0.9):** everything is in real USD of `ResultsYear` (2026) per GJ. Row `infl` (US CPI index) converts nominal domestic data and nominal policy inputs; row `defl` (US GDP deflator index) converts international prices. The two differ by up to 1.2% before 2030, so both are kept. MTInputs policy values are real, except a carbon price marked `NomorReal` = Nominal. Values after 2030 are not a legacy target.
- **Section 2 (prices, by 12 price fuels):** `gp` international prices (MTInputs source and High/Low adjustment; country gas market); `sp` = data up to 2024, then fixsp + floating part x gp(t)/gp(t-1); `txo` = data, then the legacy pass-through rule; `rpb` = (sp + txo) x (1 + VAT rate). VAT rate: dataset where filled, else VAT_WEO (Egypt 14%) for residential coal/gas and oil products, 0 for power, industry, biomass (v0.10 assumption). Data step: sheet `Inputs_prices`.
- **Wedges:** `ctxnew` = carbon price x EF x fuel coverage x sector coverage x (1 - ETS coverage); `ets` = ETS permit price x EF x effective ETS coverage; `ntx` = fuel price reform path / GJ per price unit; `nce` = `ctxnew` + `ets` + `ntx`; `atp` = max(`rpb` of the price fuel + `nce` x (1 + VAT rate), 0.01); `shp` = sector shadow price x EF x `ssc`.
- **ETS (v0.11):** MTInputs rows 84-115 per scenario. Permit price = carbon price path once the new ETS applies (as effective as a carbon tax; the cap needs emissions, not yet modelled); it replaces the carbon tax in ETS-covered sectors; the full price enters `atp`, the auctioned share only revenue. Sectoral shadow prices = feebates + regulations (placeholder 0).
- **Existing taxes and subsidies (v0.11, section 2):** `vat`, `etx` = max(txo, 0), `esub` = max(-txo, 0), `esubpu` = subsidy per MTInputs price unit (input for a later per-fuel policy). 
- **Revenues (v0.12):** three separate calculations per subsector and fuel (USD million real): `rtx` existing tax revenue = fuel use x PJ/ktoe x (`etx` + `vat`); `rsub` existing subsidy cost = fuel use x PJ/ktoe x `esub`; `rnew` new-policy revenue = fuel use x PJ/ktoe x (`ctxnew` + `ntx` + `ets` x auctioned share + `nce` x VAT rate). Section 12: totals by sector, net existing (`rnet`), total (`rtot`), change vs scenario 1 (`rtot.chg`). Feebates revenue-neutral; no power or electricity yet.
- **Data step separate from formulas.** Sheet `Inputs` (one row per fuel|subsector) holds every lookup; `Mitigation` reads it in the hidden parameter columns D:G (labels in `Variables` G:J) and the base-year column. Calculation cells hold no searching lookups; `ctxnew`, `ntx` and `shp` pick a Section-1 row by position with `INDEX(range, position)`.
- **Copy-pasteable:** every variable has one formula (relative R1C1) per column block across all subsectors, fuels and scenarios. Supply cost and taxes have separate history (2022-2024, data) and projection blocks without IF. The right column (2040) of every calculated row calls a named LAMBDA (19 in all, Name Manager), which holds the IF between history and projection where needed, so it can be copied back over a whole row.
- **Codes and labels.** Column A holds the variable code; description, unit and source come from `Variables`; each scenario group starts with a code column building `country.mit.<variable>.<subsector>.<fuel>.<suffix>.<scenario>` (e.g. `egy.mit.ener.rod.gso.e.1`).
- **Roll-up.** Sector sections show their total and the subsector heading lines; + on a heading opens its variables. Section 1 shows the carbon price, its inputs and paths are rolled up. Green section bands have white text.
- **Parameters are global**; scenarios differ only in their MTInputs columns. Country lookups via `Settings!C4` (elasticities and prices for all CPAT countries; energy use, GDP and EFs Egypt only).

## Files

| File | Role |
|---|---|
| `CPAT_Mitigation_CopyPaste_v0.12.xlsx` | Workbook (formulas only; recalculates on open) |
| `build_v0_12.py` | Builder (reads `templates/MTInputs_template.xlsx`) (openpyxl; no Excel COM needed) |
| `extract_data_v0_2.py` | Writes `data/*.csv` from the legacy workbook, the price-module data and kernel v1.6 (needs `pyxlsb`); v0.2 adds international prices by source, US CPI and GDP deflator, regional price assumptions |
| `PriceProjection_Method_v0.4.md` | Price projection method as implemented, with the holistic real/nominal assumptions (A1-A11) and existing taxes and subsidies |
| `check_v0_12.py` | LibreOffice checks: errors only in the LAMBDA column, one R1C1 formula per block and per label/code column, LAMBDA encoding, LAMBDA expansion and drag-forward vs an independent Python recomputation, scenario-copy test with auto-numbering, expected CPAT codes, row outline, band format and summary lines, MTInputs = template, carbon price vs legacy trajectory, fuel price reform and feebate test scenarios (feebates lower fuel use only where covered), price chain (gp, sp, txo, rpb) vs an independent Python recomputation from the CSVs incl. price source IMF-WB*/High, nominal carbon price and price controls None/Manual, revenues (per subsector and fuel and section-12 totals) vs Python, regression vs v0.11 on all shared output codes, bright marking of changed data, column blocks (history / projection / LAMBDA), LAMBDA in the right column of every calculated row, LAMBDA copied back over whole rows, ETS = carbon tax test, LegacyDiff sheet |
| `check_report_v0.12.md` | Output of the last check run |
| `data/` | Extracted source data (non-proprietary) |
| `Old/` | v0.1-v0.11 workbooks, builders, check scripts and reports; method notes v0.1-v0.3; extract_data_v0_1 |

Rebuild: `python extract_data_v0_2.py` (only if sources change), `python build_v0_12.py`, `python check_v0_12.py`.

## Add a scenario

Copy the last scenario column on `MTInputs` one column to the right and edit its inputs (name in row 6). Then copy a whole group on `Mitigation` (scenario 2 = `Z:AM`, code column first) and paste at `AN`. Scenario numbers, names, codes and the carbon price update by themselves.

## Roadmap (buckets)

1. Goal and spec (done, 2026-10-08).
2. Skeleton with working equations, Egypt data: v0.1, revised to v0.2-v0.5 after review - **awaiting review in Excel**.
3. Copy-paste stress test: add a fuel, a subsector and a scenario by dragging; fix what breaks.
4. Policies (bucket 6): 6a MTInputs and the carbon price (v0.6, done); 6b policy wedges and legacy section layout (v0.7, done); shadow price on the efficiency margin (v0.8, done); domestic price projection in real terms (v0.9, done); other oil products and VAT assumption (v0.10, done); ETS, sectoral shadow prices, existing taxes and subsidies, 2040 horizon (v0.11, done). Revenues (v0.12, done). Next: emissions (also needed for a cap-based ETS price), power sector. Next: ETS, regulations as shadow prices, subsidy phase-out.
5. Numerical check against legacy CPAT for Egypt.
6. Later: emissions, power, revenue/macro links, Python port.
