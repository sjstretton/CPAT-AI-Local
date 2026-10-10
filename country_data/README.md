# CPAT country data on SharePoint

One shared file holds CPAT's country data, so Python code and Excel workbooks look values up instead of each carrying their own copy. It is a stopgap until the World Bank provides a proper data platform. When that arrives, only the loader and the Power Query source change, not the models.

| What | Where |
|---|---|
| The data file | CPAT SharePoint drive, folder `CountryData`, file `cpat_country_data.xlsx` |
| Python loader | `country_data/cpat_country_data.py` (this folder) |
| Seed builder | `country_data/build_country_data.py` (used once to create the file) |
| Tests | `country_data/test_cpat_country_data.py` (`pytest country_data`) |

## The file

Sheet `Data` holds one Excel table, `CountryData`, with one row per country, year and variable:

| iso3 | year | variable | value | unit | source | vintage |
|---|---|---|---|---|---|---|
| EGY | 2022 | mit.sp.nga.ind | 10.785 | current USD/GJ | Corrected Egypt price block ... | 2026-10-10 |

- The lookup key is `iso3|year|variable`, and each key occurs once. The Python loader refuses a file with duplicate keys.
- Sheet `Variables` lists every variable code with its group, description and unit. Sheet `ReadMe` has the rules and a change log.
- The seed covers the mitigation module (83,813 rows):

| Group | Codes | Coverage | Source |
|---|---|---|---|
| Domestic prices | `mit.sp.*`, `mit.txo.*`, `mit.rp.*`, `mit.vatrate.*`, `mit.ps.*`, `mit.mar.*`, `VAT_WEO`, production costs etc. (the legacy `Prices_dom` codes) | 220 countries, 2019-2024 | MVP v1.00 `Prices_dom`, including the corrected Egypt block (291 cells, marked in `source`) |
| Energy balances | `bal.<flow>.<fuel>`, e.g. `bal.cement.nga`, `bal.tfc.total` (ktoe; `bal.eloutput.*` in GWh) | Egypt 2022 | Legacy `Balances` sheet |
| Base-year energy use | `mit.ener.<subsector>.<fuel>`, e.g. `mit.ener.rod.gso` (ktoe) | Egypt 2022 | MVP v1.00 `EnergyCons` (derived from the balances) |

The other countries' energy balances are licensed IEA data. They are not in this repo, so add them on SharePoint (see "Adding data").

## One-time setup on SharePoint (data owner)

1. In the CPAT SharePoint drive, create a folder named `CountryData` and upload `cpat_country_data.xlsx` to it.
2. Permissions: the CPAT team gets **read** access, and the data owners get **edit** access. To set them, go to folder `CountryData` → ... → Manage access. Licensed IEA data makes this restriction necessary.
3. Never rename or move the file or folder: every user's path and every workbook's link points at them. Use SharePoint version history instead of making `_v2` copies. (This file is the exception to the NORMS section 5 versioning rule, because its path must stay fixed.)

## Python

**One-time setup per laptop:** open the CPAT SharePoint folder in the browser, select `CountryData`, and click **Sync**. Alternatively, use **Add shortcut to My files**. The file then appears at a path like
`C:\Users\<you>\WBG\CPAT - Documents\CountryData\cpat_country_data.xlsx`.

The loader finds the file without anyone typing a path. It tries, in order:
1. the environment variable `CPAT_DATA`, which can be the file or its folder. Use this if a laptop's setup is unusual;
2. `C:\Users\<you>\WBG\<library>\...\CountryData\` (synced library, up to three folders deep);
3. `%OneDriveCommercial%\...\CountryData\` (the "My files" shortcut).

If no copy is found, or more than one, the loader raises an error explaining what to do.

```python
import sys; sys.path.insert(0, r'<path to CPAT-AI-Local>\country_data')   # or copy cpat_country_data.py next to your script
from cpat_country_data import get_value, load_country_data, to_wide

get_value('EGY', 'mit.sp.nga.ind', 2022)                    # 10.785
prices = load_country_data(countries=['EGY'], prefix='mit.')  # long table, filtered
to_wide(load_country_data(countries='EGY', prefix='bal.'))   # rows (iso3, year), one column per variable
```

- The first read of a new file version takes about 15 seconds. After that, reads take milliseconds: the result is cached in `%LOCALAPPDATA%\cpat_country_data` and re-read only when the file changes.
- Python reads the **synced copy**. If OneDrive sync is paused on a laptop, that copy can be out of date. Check the OneDrive icon in the taskbar.

## Excel (Power Query)

Excel reads the file over the web from SharePoint. Everyone uses the same address, so different user folders don't matter, and the WB login handles access.

**Get the address once:** open `cpat_country_data.xlsx` from SharePoint in Excel desktop, choose File → Info → **Copy path**, and delete the trailing `?web=1`. It looks like
`https://worldbankgroup.sharepoint.com/sites/<CPAT site>/Shared Documents/CountryData/cpat_country_data.xlsx`.

**In the workbook that needs the data:**
1. Data → Get Data → From Other Sources → **Blank Query**, then Home → **Advanced Editor**. Paste the query below and put your address in `Url`:
   ```
   let
       Url    = "https://worldbankgroup.sharepoint.com/sites/<CPAT site>/Shared Documents/CountryData/cpat_country_data.xlsx",
       Source = Excel.Workbook(Web.Contents(Url), null, true),
       Data   = Source{[Item = "CountryData", Kind = "Table"]}[Data],
       Typed  = Table.TransformColumnTypes(Data, {{"iso3", type text}, {"year", Int64.Type}, {"variable", type text},
                    {"value", type number}, {"unit", type text}, {"source", type text}, {"vintage", type text}}),
       Keyed  = Table.AddColumn(Typed, "key", each [iso3] & "|" & Text.From([year]) & "|" & [variable], type text)
   in
       Table.ReorderColumns(Keyed, {"key", "iso3", "year", "variable", "value", "unit", "source", "vintage"})
   ```
2. Name the query `CountryData`, then choose **Close & Load** onto a data sheet, e.g. `DATA_Country`.
3. When Excel asks for credentials, choose **Organizational account**, then **Sign in** with your WB login. Apply the credentials at the site level. You only do this once per laptop.
4. Look values up with the key, for example in a country-year row with the year in row 5 and the code in column G:
   ```
   =XLOOKUP(Settings!$C$4 & "|" & L$5 & "|" & $G10, CountryData[key], CountryData[value], NA())
   ```
   A missing value shows `#N/A` rather than a silent 0.
5. To pick up changes, use Data → **Refresh All**. Without network access, the workbook keeps the last loaded values.

Optional: to load one country only, add a step `Table.SelectRows(Typed, each [iso3] = "EGY")`. If the country instead comes from a cell in the workbook, Excel raises a "Formula.Firewall" error unless File → Options → Query Options → Current Workbook → Privacy is set to *Ignore privacy levels*. Loading all countries (about 84,000 rows) is fine and avoids that error.

## Adding or changing data (data owners)

- **Add:** add rows at the bottom of the `CountryData` table; it grows automatically. Fill all seven columns, use existing codes where they exist, and add new codes to `Variables` first.
- **Change:** to correct a value, overwrite `value` and update `source` and `vintage`. SharePoint version history keeps the old file.
- **Many rows**, e.g. all-country energy balances: arrange them in the same seven columns in another sheet, check for duplicate keys, then paste them under the table.
- **Never** insert columns, rename the table or sheets, merge cells, or type formulas in `Data`: keep it a plain table of values.
- Add a line to the change log in `ReadMe`.
