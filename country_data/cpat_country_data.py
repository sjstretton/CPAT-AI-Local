"""Read CPAT country data from the shared file on the CPAT SharePoint drive.

The file (cpat_country_data.xlsx, table CountryData: iso3, year, variable,
value, unit, source, vintage) lives in the SharePoint folder CountryData and
is synced to each laptop by OneDrive. The local path differs per user, so it
is found, in this order:

  1. the CPAT_DATA environment variable (the file, or the folder holding it);
  2. the synced SharePoint library:  C:/Users/<you>/WBG/<site - library>/.../CountryData/
  3. a "Add shortcut to My files" link: %OneDriveCommercial%/.../CountryData/

Usage:
    from cpat_country_data import get_value, load_country_data, to_wide
    get_value('EGY', 'mit.sp.nga.ind', 2022)          # one number
    df = load_country_data(countries=['EGY'], prefix='bal.')
    to_wide(df)                                        # rows iso3, year; columns = variables

The xlsx is read once per version: cached in memory and as a pickle in
%LOCALAPPDATA%/cpat_country_data (~/.cache elsewhere); a changed file is re-read.
This module needs only pandas and openpyxl; copy it anywhere.
"""
import hashlib
import os
from pathlib import Path

import pandas as pd

FILE_NAME = 'cpat_country_data.xlsx'
FOLDER_NAME = 'CountryData'
ORG_FOLDER = 'WBG'  # synced SharePoint libraries land in C:/Users/<you>/WBG/
COLUMNS = ['iso3', 'year', 'variable', 'value', 'unit', 'source', 'vintage']

_cache: dict = {}


def find_data_file() -> Path:
    """Return the path of cpat_country_data.xlsx on this machine."""
    env = os.environ.get('CPAT_DATA')
    if env:
        p = Path(env).expanduser()
        p = p / FILE_NAME if p.is_dir() else p
        if not p.is_file():
            raise FileNotFoundError(f'CPAT_DATA is set to {env}, but {p} does not exist.')
        return p

    roots = [Path.home() / ORG_FOLDER]
    if os.environ.get('OneDriveCommercial'):
        roots.append(Path(os.environ['OneDriveCommercial']))
    found = []
    for root in roots:
        # library/CountryData, library/<channel>/CountryData, library/<channel>/<folder>/CountryData
        for depth in ('*', '*/*', '*/*/*'):
            found += root.glob(f'{depth}/{FOLDER_NAME}/{FILE_NAME}')
    found = sorted(set(found))
    if len(found) == 1:
        return found[0]
    if not found:
        raise FileNotFoundError(
            f'{FILE_NAME} not found under {" or ".join(str(r) for r in roots)}. '
            f'Sync the SharePoint folder {FOLDER_NAME} (or add a shortcut to My files), '
            f'or set the CPAT_DATA environment variable to the file path.')
    raise FileNotFoundError(
        f'Several copies of {FILE_NAME} found: {", ".join(map(str, found))}. '
        f'Set the CPAT_DATA environment variable to the one to use.')


def _cache_file(path: Path, mtime: float) -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home() / '.cache') / 'cpat_country_data'
    return base / f'{hashlib.md5(str(path.resolve()).encode()).hexdigest()[:12]}_{int(mtime)}.pkl'


def _read(path: Path) -> pd.DataFrame:
    mtime = path.stat().st_mtime
    key = str(path)
    if key in _cache and _cache[key][0] == mtime:
        return _cache[key][1]

    # Reading the xlsx takes ~15 s; a pickle per file version on the local disk makes later sessions instant.
    disk = _cache_file(path, mtime)
    if disk.is_file():
        df = pd.read_pickle(disk)
        _cache[key] = (mtime, df)
        return df

    df = pd.read_excel(path, sheet_name='Data', engine='openpyxl')
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f'{path}: sheet Data is missing columns {missing}.')
    df = df[COLUMNS].dropna(how='all')
    df['iso3'] = df['iso3'].astype(str).str.strip().str.upper()
    df['variable'] = df['variable'].astype(str).str.strip()
    df['year'] = pd.to_numeric(df['year'], errors='raise').astype(int)
    df['value'] = pd.to_numeric(df['value'], errors='raise')

    dup = df.duplicated(['iso3', 'year', 'variable'], keep=False)
    if dup.any():
        sample = df.loc[dup, ['iso3', 'year', 'variable']].drop_duplicates().head(10)
        raise ValueError(f'{path}: {int(dup.sum())} rows share an iso3|year|variable key, e.g.\n{sample.to_string(index=False)}')

    try:
        disk.parent.mkdir(parents=True, exist_ok=True)
        for stale in disk.parent.glob(f'{disk.name.split("_")[0]}_*.pkl'):
            stale.unlink()
        df.to_pickle(disk)
    except OSError:
        pass  # cache is optional
    _cache[key] = (mtime, df)
    return df


def load_country_data(countries=None, variables=None, prefix=None, years=None, path=None) -> pd.DataFrame:
    """Long table (iso3, year, variable, value, unit, source, vintage), optionally filtered.

    countries: ISO3 codes; variables: exact codes; prefix: start of the code,
    e.g. 'mit.sp.' (supply costs), 'bal.' (energy balances), 'mit.ener.'
    (base-year energy use); years: list of years.
    """
    df = _read(Path(path) if path else find_data_file())
    if countries is not None:
        df = df[df['iso3'].isin([c.upper() for c in _as_list(countries)])]
    if variables is not None:
        df = df[df['variable'].isin(_as_list(variables))]
    if prefix is not None:
        df = df[df['variable'].str.startswith(prefix)]
    if years is not None:
        df = df[df['year'].isin(_as_list(years))]
    return df.reset_index(drop=True)


def get_value(iso3: str, variable: str, year: int, path=None) -> float:
    """One value; KeyError if the iso3|year|variable row does not exist."""
    df = load_country_data(countries=[iso3], variables=[variable], years=[year], path=path)
    if df.empty:
        raise KeyError(f'No country data for {iso3.upper()}|{year}|{variable}.')
    return float(df['value'].iloc[0])


def to_wide(df: pd.DataFrame) -> pd.DataFrame:
    """Rows (iso3, year), one column per variable, like the legacy country-year data sheets."""
    return df.pivot(index=['iso3', 'year'], columns='variable', values='value')


def _as_list(x):
    return [x] if isinstance(x, (str, int)) else list(x)


if __name__ == '__main__':
    p = find_data_file()
    df = load_country_data(path=p)
    print(f'{p}\n{len(df):,} rows, {df["iso3"].nunique()} countries, {df["variable"].nunique()} variables, '
          f'years {df["year"].min()}-{df["year"].max()}')
