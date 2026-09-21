from typing import TypedDict, Literal

import cpat_model.constants as c


LaborTaxReductionMethodType = Literal[
    'Proportional Compensation', 'Personal Allowance', 'Targeted Exemption'
]
StatisticType = Literal['mean', 'median', 'p25', 'p75']


class DistributionInputsDict(TypedDict):
    """
    Distribution module inputs.

    Based on the CPAT Excel 'Distribution' sheet, section B (Key assumptions and
    inputs). Kept as its own TypedDict, separate from DashboardInputsDict
    (Mitigation module inputs), because the Distribution sheet has its own
    independent input block in the Excel model -- it *consumes* the Mitigation
    module's results (prices, carbon-price revenue; see
    cpat_model.components.distribution.distribution.Distribution) rather than
    sharing Dashboard-level scenario config.

    See distribution/docs/CPAT_Distribution_Module_Pseudocode.docx (§4 Inputs)
    for the full input inventory this is progressively implementing.
    """
    # B.I Basic inputs
    analysis_year: int # Distribution!'Analysis Year'
    statistic_output: StatisticType # Distribution!'Statistic - Outputs', default 'mean'

    # B.I Incidence adjustments (§4.2)
    adjust_for_behavioral_change: bool
    behavioral_response_adj_factor: float
    adjust_for_deadweight_losses: bool
    use_decile_specific_elasticities: bool
    assume_imperfect_passthrough: bool

    # B.I Exemptions (§4.5)
    exempt_cooking_fuel: bool
    exempt_cooking_fuel_code: str # one of c.DISTN_DIRECT_FUELS, used when exempt_cooking_fuel=True
    exempt_cooking_fuel_share: float
    exempt_cooking_fuel_bottom_deciles: int # exempt the bottom N deciles

    # B.I Revenue recycling (§4.4): shares of CP revenue, should sum to <= 1.0
    share_labor_tax_reduction: float
    share_targeted_transfer: float
    share_public_investment: float
    share_current_spending: float

    labor_tax_reduction_method: LaborTaxReductionMethodType
    labor_tax_exempt_bottom_deciles: int # 'Targeted Exemption' method
    labor_tax_cut_coefficient: float # 'Proportional Compensation' method


class DistributionInputs:
    """
    Contains all Distribution module inputs in d: DistributionInputsDict.
    Mirrors cpat_model.inputs.dashboard_inputs.DashboardInputs (default dict + overrides).
    Hardcoded defaults for now -> TODO: UI, same as DashboardInputs.
    """
    d: DistributionInputsDict

    def __init__(self, config_input: dict | None = None) -> None:
        # default
        self.d = {
            'analysis_year': 2030,
            'statistic_output': 'mean',

            'adjust_for_behavioral_change': False,
            'behavioral_response_adj_factor': 1.0,
            'adjust_for_deadweight_losses': False,
            'use_decile_specific_elasticities': False,
            'assume_imperfect_passthrough': False,

            'exempt_cooking_fuel': False,
            'exempt_cooking_fuel_code': c.KER,
            'exempt_cooking_fuel_share': 0.0,
            'exempt_cooking_fuel_bottom_deciles': 0,

            'share_labor_tax_reduction': 0.0,
            'share_targeted_transfer': 0.0,
            'share_public_investment': 0.0,
            'share_current_spending': 0.0,

            'labor_tax_reduction_method': 'Proportional Compensation',
            'labor_tax_exempt_bottom_deciles': 0,
            'labor_tax_cut_coefficient': 0.0,
        }

        if config_input:
            self.d.update(config_input)
