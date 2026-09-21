from types import SimpleNamespace

import pytest
import pandas as pd

from cpat_model.components.distribution.distribution import Distribution
import cpat_model.constants as c


YEAR = 2030
Y = str(YEAR)
COUNTRIES = ['EGY']


def _rp_df(values: dict) -> pd.DataFrame:
    """
    Builds a (CountryCode, SectorCode, FuelCode)-indexed, single-year-column
    DataFrame like EnergyPrices.rp / ele_prices['rp'], from
    {(country, sector, fuel): price}.
    """
    rows = [(country, sector, fuel, price) for (country, sector, fuel), price in values.items()]
    df = pd.DataFrame(rows, columns=[c.COUNTRY_CODE, c.SECTOR_CODE, c.FUEL_CODE, Y])
    return df.set_index(c.ID_COL_NAMES)


def _scenario_results(rp: pd.DataFrame, ele_rp: pd.DataFrame, cp: float | None = None, em: float | None = None):
    """
    Minimal stand-in for ScenarioResults carrying just what
    Distribution.__init_price_change_direct/__init_cp_revenue read:
    energy_prices.rp, energy_prices.ele_prices['rp'], policies.cp_trajectory,
    em.total_em. Avoids constructing real EnergyPrices/Policies/CO2Emissions
    objects, which need full InputData.
    """
    energy_prices = SimpleNamespace(rp=rp, ele_prices={'rp': ele_rp})
    policies = SimpleNamespace(
        cp_trajectory=pd.DataFrame({Y: [cp]}, index=pd.Index(COUNTRIES, name=c.COUNTRY_CODE))
        if cp is not None else None
    )
    em_obj = SimpleNamespace(
        total_em=pd.DataFrame({Y: [em]}, index=pd.Index(COUNTRIES, name=c.COUNTRY_CODE))
        if em is not None else None
    )
    return SimpleNamespace(energy_prices=energy_prices, policies=policies, em=em_obj)


def test_init_price_change_direct():
    fossil_fuels = [f for f in c.DISTN_DIRECT_FUELS if f not in [c.ELE] + c.COOKING_BIOMASS_FUELS]

    baseline_rp = _rp_df({('EGY', c.RES, f): 10.0 for f in fossil_fuels})
    policy_rp = _rp_df({('EGY', c.RES, f): 11.0 for f in fossil_fuels}) # +10% for every fossil fuel

    baseline_ele = _rp_df({('EGY', c.RES, c.ELE): 5.0})
    policy_ele = _rp_df({('EGY', c.RES, c.ELE): 6.0}) # +20%

    baseline = _scenario_results(baseline_rp, baseline_ele)
    policy = _scenario_results(policy_rp, policy_ele)

    distribution = Distribution.__new__(Distribution)
    distribution.analysis_year = YEAR
    init_price_change_direct = distribution._Distribution__init_price_change_direct # pylint: disable=protected-access
    init_price_change_direct(COUNTRIES, baseline, policy)

    for f in fossil_fuels:
        assert distribution.price_change_direct[('EGY', f)] == pytest.approx(0.1)
    assert distribution.price_change_direct[('EGY', c.ELE)] == pytest.approx(0.2)
    for f in c.COOKING_BIOMASS_FUELS:
        assert distribution.price_change_direct[('EGY', f)] == 0.0

    # every direct fuel is present, nothing extra
    assert sorted(distribution.price_change_direct.index.get_level_values(c.FUEL_CODE)) == sorted(
        c.DISTN_DIRECT_FUELS
    )


def test_init_cp_revenue():
    baseline = _scenario_results(_rp_df({}), _rp_df({}))
    policy = _scenario_results(_rp_df({}), _rp_df({}), cp=50.0, em=1_000.0)

    distribution = Distribution.__new__(Distribution)
    distribution.analysis_year = YEAR
    init_cp_revenue = distribution._Distribution__init_cp_revenue # pylint: disable=protected-access
    init_cp_revenue(COUNTRIES, policy)

    assert distribution.cp_revenue['EGY'] == pytest.approx(50_000.0)
