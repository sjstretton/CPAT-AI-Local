"""Tests for cpat_country_data.py.  Run: pytest country_data"""
from pathlib import Path

import pandas as pd
import pytest

import cpat_country_data as ccd

ROWS = [
    ['EGY', 2022, 'mit.sp.nga.ind', 10.785, 'current USD/GJ', 'test', '2026-10-10'],
    ['EGY', 2023, 'mit.sp.nga.ind', 9.5, 'current USD/GJ', 'test', '2026-10-10'],
    ['EGY', 2022, 'bal.cement.nga', 1747.39, 'ktoe', 'test', '2026-10-10'],
    ['ALB', 2022, 'mit.sp.nga.ind', 5.0, 'current USD/GJ', 'test', '2026-10-10'],
]


def write(path: Path, rows=ROWS):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=ccd.COLUMNS).to_excel(path, sheet_name='Data', index=False)
    return path


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    home = tmp_path / 'home'
    home.mkdir()
    monkeypatch.setattr(Path, 'home', lambda: home)
    monkeypatch.delenv('CPAT_DATA', raising=False)
    monkeypatch.delenv('OneDriveCommercial', raising=False)
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path / 'cache'))
    ccd._cache.clear()
    return home


def test_finds_synced_sharepoint_library(isolate):
    f = write(isolate / 'WBG' / 'CPAT - Documents' / 'General' / 'CountryData' / ccd.FILE_NAME)
    assert ccd.find_data_file() == f


def test_finds_onedrive_shortcut(isolate, tmp_path, monkeypatch):
    od = tmp_path / 'OneDrive - WBG'
    f = write(od / 'CPAT - Documents' / 'CountryData' / ccd.FILE_NAME)
    monkeypatch.setenv('OneDriveCommercial', str(od))
    assert ccd.find_data_file() == f


def test_env_var_wins_and_accepts_folder(isolate, tmp_path, monkeypatch):
    write(isolate / 'WBG' / 'CPAT - Documents' / 'CountryData' / ccd.FILE_NAME)
    f = write(tmp_path / 'elsewhere' / ccd.FILE_NAME)
    monkeypatch.setenv('CPAT_DATA', str(f.parent))
    assert ccd.find_data_file() == f
    monkeypatch.setenv('CPAT_DATA', str(tmp_path / 'missing.xlsx'))
    with pytest.raises(FileNotFoundError, match='CPAT_DATA'):
        ccd.find_data_file()


def test_not_found_and_ambiguous(isolate):
    with pytest.raises(FileNotFoundError, match='not found'):
        ccd.find_data_file()
    write(isolate / 'WBG' / 'A - Documents' / 'CountryData' / ccd.FILE_NAME)
    write(isolate / 'WBG' / 'B - Documents' / 'CountryData' / ccd.FILE_NAME)
    with pytest.raises(FileNotFoundError, match='Several copies'):
        ccd.find_data_file()


def test_lookups(tmp_path):
    f = write(tmp_path / ccd.FILE_NAME)
    assert ccd.get_value('egy', 'mit.sp.nga.ind', 2022, path=f) == 10.785
    with pytest.raises(KeyError):
        ccd.get_value('EGY', 'mit.sp.nga.ind', 2030, path=f)
    df = ccd.load_country_data(countries='EGY', prefix='mit.sp.', path=f)
    assert sorted(df['year']) == [2022, 2023]
    wide = ccd.to_wide(ccd.load_country_data(countries=['EGY'], path=f))
    assert wide.loc[('EGY', 2022), 'bal.cement.nga'] == 1747.39


def test_duplicate_keys_rejected(tmp_path):
    f = write(tmp_path / ccd.FILE_NAME, ROWS + [ROWS[0][:3] + [11.0] + ROWS[0][4:]])
    with pytest.raises(ValueError, match='share an iso3'):
        ccd.load_country_data(path=f)


def test_disk_cache_used_and_refreshed(tmp_path, monkeypatch):
    f = write(tmp_path / ccd.FILE_NAME)
    ccd.load_country_data(path=f)
    assert len(list((tmp_path / 'cache' / 'cpat_country_data').glob('*.pkl'))) == 1
    ccd._cache.clear()
    monkeypatch.setattr(pd, 'read_excel', lambda *a, **k: pytest.fail('should read the pickle'))
    assert ccd.get_value('ALB', 'mit.sp.nga.ind', 2022, path=f) == 5.0
