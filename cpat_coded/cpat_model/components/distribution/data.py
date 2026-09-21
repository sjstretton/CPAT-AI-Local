"""
[Data Loading] for the Distribution module.

Mirrors the load_*/get_* functions in the other components (e.g.
energy_consumption/energy_data.py, power/data.py): each function reads one
CSV from DATA_PATH and returns it filtered/indexed for the selected
countries. InputData.__init__ wires these in the same way it wires every
other component's loaders.

Source (pre-extraction, currently in this repo): the six DATA_DISTN sheets of
cpat_excel/original/CPAT 1.0pre_456_NoPropData.xlsb, already extracted to
cpat_excel/Distribution/data_standardized/CPAT_DistributionalData.xlsx by the
cpat_excel/scripts pipeline. TODO: this xlsx -> cpat_data/new_data/*.csv
export does not exist yet -- these loaders establish the shape/contract the
export needs to produce, they do not (yet) generate the CSVs themselves.
See distribution/docs/CPAT_Distribution_Module_Pseudocode.docx §4.7-§4.9, §8.
"""
import pandas as pd

import cpat_model.constants as c
from config import DATA_PATH


IO_GTAP_FILE_NAME = 'distn_io_gtap'
HH_SURVEY_FILE_NAME = 'distn_hh_survey'
HH_ELAST_FILE_NAME = 'distn_hh_elast'
ASPIRE_FILE_NAME = 'distn_aspire'
WHO_COOKING_FILE_NAME = 'distn_who_cooking'
GDP_RATIOS_FILE_NAME = 'distn_gdp_ratios'
SECTOR_CROSSWALK_FILE_NAME = 'distn_mapping_sector_crosswalk'

# Household-survey-shaped tables (HHSurvey, HH_Elast) all carry this dimension
# set, per the pseudocode spec §3.1: one row per
# (country, fuel-or-category, decile, sample, statistic).
HH_SHAPED_ID_COLS = [
    c.COUNTRY_CODE, c.DECILE_CODE, c.SAMPLE_CODE, c.STATISTIC_CODE
]


def load_io_gtap(selected_countries: list[str]) -> pd.DataFrame:
    """
    GTAP10 input-output table: sectoral energy intensities (Leontief
    coefficients), the Leontief inverse, and household-demand/export/output
    aggregates by GTAP sector. Feeds Step 1 (price-change derivation).

    CPAT Excel: 'Distribution' sheet §C.I (rows 489-736); source sheet 'IO_GTAP'.

    return dims (CountryCode, GtapSectorCode)
    """
    df = pd.read_csv(f'{DATA_PATH}/{IO_GTAP_FILE_NAME}.csv')
    df = df[df[c.COUNTRY_CODE].isin(selected_countries)]
    return df.set_index([c.COUNTRY_CODE, c.GTAP_SECTOR_CODE])


def load_hh_survey(selected_countries: list[str]) -> pd.DataFrame:
    """
    Household budget survey extract: per (fuel-or-category, decile, sample,
    statistic) budget shares, population and per-capita/total consumption.
    Feeds Step 3 (budget shares) and Step 7 (survey-to-NA rebasing).

    CPAT Excel: 'Distribution' sheet §C.III, §C.IV, §C.VIII; source sheet 'HHSurvey'.

    return dims (CountryCode, Decile, Sample, Statistic)
    """
    df = pd.read_csv(f'{DATA_PATH}/{HH_SURVEY_FILE_NAME}.csv')
    df = df[df[c.COUNTRY_CODE].isin(selected_countries)]
    return df.set_index(HH_SHAPED_ID_COLS)


def load_hh_elast(selected_countries: list[str]) -> pd.DataFrame:
    """
    Own-price elasticities of demand by fuel/category (national, and
    decile-specific where available). Feeds Step 2 (behavioural/DWL
    adjustments).

    CPAT Excel: 'Distribution' sheet §C.II; source sheet 'HH_Elast'.

    return dims (CountryCode, Decile, Sample, Statistic)
    """
    df = pd.read_csv(f'{DATA_PATH}/{HH_ELAST_FILE_NAME}.csv')
    df = df[df[c.COUNTRY_CODE].isin(selected_countries)]
    return df.set_index(HH_SHAPED_ID_COLS)


def load_aspire(selected_countries: list[str]) -> pd.DataFrame:
    """
    World Bank ASPIRE database: per-decile incidence (coverage/benefit
    shares) of social-protection and infrastructure-access programs, by
    program code. Feeds Step 8 (targeted transfers / public investment /
    current spending recycling).

    CPAT Excel: 'Distribution' sheet §C.X; source sheet 'ASPIRE'.

    return dims (CountryCode, Decile)
    """
    df = pd.read_csv(f'{DATA_PATH}/{ASPIRE_FILE_NAME}.csv')
    df = df[df[c.COUNTRY_CODE].isin(selected_countries)]
    return df.set_index([c.COUNTRY_CODE, c.DECILE_CODE])


def load_who_cooking(selected_countries: list[str]) -> pd.DataFrame:
    """
    WHO household energy database: informs which fossil fuel is the
    country's "most-used cooking fuel" for the exemption logic, and cooking
    fuel (charcoal/ethanol/firewood) budget shares.

    CPAT Excel: 'Distribution' sheet §C.III (cooking fuel rows); source
    sheet 'WHOCooking'.

    return dims (CountryCode)
    """
    df = pd.read_csv(f'{DATA_PATH}/{WHO_COOKING_FILE_NAME}.csv')
    return df[df[c.COUNTRY_CODE].isin(selected_countries)].set_index(c.COUNTRY_CODE)


def load_gdp_ratios(selected_countries: list[str]) -> pd.DataFrame:
    """
    GDP deflators and household-consumption-to-GDP ratios by country/year.
    Feeds Step 7 (survey-to-national-accounts rebasing).

    CPAT Excel: 'Distribution' sheet §B.I ('Household Consumption'),
    §C.VIII; source sheet 'GDPRatios'.

    return dims (CountryCode)
    """
    df = pd.read_csv(f'{DATA_PATH}/{GDP_RATIOS_FILE_NAME}.csv')
    return df[df[c.COUNTRY_CODE].isin(selected_countries)].set_index(c.COUNTRY_CODE)


def load_gtap_cpat_sector_crosswalk() -> pd.DataFrame:
    """
    GTAP10 <-> CPAT <-> ISIC sector crosswalk. Not country-specific. Feeds
    Step 1.6 (aggregating ~59 GTAP sectors up to the ~14 CPAT indirect
    consumption categories).

    CPAT Excel: source sheets Mapping_SectorCrosswalk,
    Mapping_CPATSectorsToISIC, Mapping_IEAFlowsToISIC, Mapping_ISICToCPAT
    (see cpat_excel/Distribution/data_standardized).

    return dims (GtapSectorCode)
    """
    df = pd.read_csv(f'{DATA_PATH}/{SECTOR_CROSSWALK_FILE_NAME}.csv')
    return df.set_index(c.GTAP_SECTOR_CODE)
