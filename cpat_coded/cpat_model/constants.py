ID_COL_NAMES = ['CountryCode', 'SectorCode', 'FuelCode']

# dims columns
COUNTRY_CODE = 'CountryCode'
SECTOR_CODE = 'SectorCode'
FUEL_CODE = 'FuelCode'

ID_COL_NAMES = [COUNTRY_CODE, SECTOR_CODE, FUEL_CODE]

# sectors
POW = 'pow' # Power
ROD = 'rod' # Road
RAL = 'ral' # Rail
AVI = 'avi' # Domestic aviation
NAV = 'nav' # Domestic shipping
RES = 'res' # Residential
OEN = 'oen' # Other energy use
FOO = 'foo' # Food & forestry
SRV = 'srv' # Services (private & public)
MCH = 'mch' # Mining & chemicals
IRN = 'irn' # Iron & steel
NFM = 'nfm' # Other metals
MAC = 'mac' # Machinery
CEM = 'cem' # Cement
OMN = 'omn' # Other manufacturing
CST = 'cst' # Construction
FTR = 'ftr' # Fuel transformation & transportation
# Sectors not included in the policies:
ELEC = 'elec'
WAV = 'wav'
NEU = 'neu'

# 'sector groups'
TRA = 'tra'
BLD = 'bld'
IND = 'ind'


# fuels
COA = 'coa' # Coal
NGA = 'nga' # Natural Gas
GSO = 'gso' # Gasoline
DIE = 'die' # Diesel
LPG = 'lpg' # LPG
KER = 'ker' # Kerosene
OOP = 'oop' # Other oil products
# Fuels not included in the policies:
BIO = 'bio' # Biomass
JFU = 'jfu' # Jetfuel
ORE = 'ore' # Other Renewables
HYD = 'hyd' # Hydro
NUC = 'nuc' # Nuclear
SOL = 'sol' # Solar
WND = 'wnd' # Wind
ELE = 'ele' # Electricity
# Biomass composites
BGS = 'bgs' # - in which: biogasoline
BDI = 'bdi' # - in which: biodiesel
OBF = 'obf' # - in which: other liquid biofuels
BIO_COMPONENTS = [BGS, BDI, OBF]

# heat
HEA = 'hea'

# additional fuel aggregations
LPK = 'lpk'
OIL = 'oil'
REN = 'ren'

# all (for all sectors)
ALL = 'all'


ALL_FUELS = {
    COA: 'Coal',
    NGA: 'Natural Gas',
    GSO: 'Gasoline',
    DIE: 'Diesel',
    LPG: 'LPG',
    KER: 'Kerosene',
    OOP: 'Other oil products'
    # Fuels not included in the policies:
    # 'bio': Biomass, 'jfu': Jetfuel, 'ore': Other Renewables, 'hyd': Hydro,
    # 'nuc': Nuclear, 'sol': Solar, 'wnd': Wind, 'ele': Electricity
}

ALL_SECTORS = {
    POW: 'Power',
    ROD: 'Road',
    RAL: 'Rail',
    AVI: 'Domestic aviation',
    NAV: 'Domestic shipping',
    RES: 'Residential',
    OEN: 'Other energy use',
    FOO: 'Food & forestry',
    SRV: 'Services (private & public)',
    MCH: 'Mining & chemicals',
    IRN: 'Iron & steel',
    NFM: 'Other metals',
    MAC: 'Machinery',
    CEM: 'Cement',
    OMN: 'Other manufacturing',
    CST: 'Construction',
    FTR: 'Fuel transformation & transportation'
    # Sectors not included in the policies:
    # ['elec' 'wav' 'neu']
}

FUELS_UNIQUE = list(ALL_FUELS.keys()) + [BIO, JFU, ORE, HYD, NUC, SOL, WND, ELE]
SECTORS_UNIQUE = list(ALL_SECTORS.keys()) + [ELEC, WAV, NEU]

# fuel groups
FOSSIL_FUELS = ['coa', 'nga', 'gso', 'die', 'lpg', 'ker', 'oop']
FOSSIL_FUELS_SORTED = sorted(FOSSIL_FUELS)
FOSSIL_FUELS_AND_BIO = FOSSIL_FUELS +  ['bio']

# sectors aggregations
SECTORS_AGG = {
    'tra': ['rod', 'ral', 'avi', 'nav'],
    'res': ['res', 'foo', 'srv'],
    'ind': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr'],
    'oen': ['oen'],
    'pow': ['pow']
}
SECTORS_AGG_TMP = { # TODO: name differently
    'tra': ['rod', 'ral', 'avi', 'nav'],
    'bld': ['res', 'foo', 'srv'],
    'ind': ['mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr'],
    'oen': ['oen'],
    'pow': ['pow']
}
SECTOR_GROUPS = list(SECTORS_AGG_TMP.keys())

### Elasticities
# 'Income elasticities - energy use':
EL_INC = 'el_inc'
# 'Own-price elasticities of demand - intensive margin (usage of energy-using capital)':
EL_DEM = 'el_dem'
# 'Own-price elasticities of demand - efficiency and extenstive margin
# (fuel economy of energy-using capital and ownership):
EL_EFF = 'el_eff'
# 'Autonomous efficiency improvements':
EFF_IMP = 'eff_imp'

# GHGs and Methane fee
AGR = 'agr'
WST = 'wst'
LIV = 'liv'
RIC = 'ric'

GAS = 'Gas'
AGG_GHGS = 'Aggregate GHGs'
CH4 = 'CH4'
CO2 = 'CO2'
F_GAS = 'F-gas'
N2O = 'N2O'

# revenues
REVENUES_CODE = 'RevenuesCode'
EXC = 'EXC' # Excise taxes (EXC)
PIT = 'PIT' # Personal income tax (PIT)
CIT = 'CIT' # Corporate income tax (CIT)
VAT = 'VAT' # Sales tax (VAT)
CAPT = 'CAPT' # Capital expenditures (CAPT)
GNFS = 'GNFS' # Expenditures on goods and services (GNFS)
TRNS = 'TRNS' # Transfers (TRNS)
WAGE = 'WAGE' # Wage expenditures (WAGE)
REVENUES_ORDER = [EXC, PIT, CIT, VAT, CAPT, GNFS, TRNS, WAGE]

# Transport
ACC = 'acc' # Accident
CON = 'con' # Congestion
RDM = 'rdm' # Road damage

# scenarios
BASELINE_SCENARIO = "BaselineScenario"

# scenario types:
BASELINE = 'Baseline'
CARBON_TAX = 'Carbon tax'
ETS = 'ETS'
FEEBATES = 'Feebates'
ENERGY_EFFICIENCY_REGULATIONS = 'Energy efficiency regulations'
TCP = 'TCP'
COAL_EXCISE = 'Coal excise'
ROAD_FUEL_TAX = 'Road fuel tax'
ELECTRICITY_EMISSION_TAX = 'Electricity emissions tax'
POWER_FEEBATE = 'Power feebate'
ELECTRICITY_EXCISE = 'Electricity excise'
VEHICLE_FUEL_ECONOMY = 'Vehicle fuel economy'
RESIDENTIAL_EFFICIENCY_REGULATIONS = 'Residential efficiency regulations'
INDUSTRIAL_EFFICIENCY_REGULATIONS = 'Industrial efficiency regulations'

ALL_SCENARIOS = (
    BASELINE, CARBON_TAX, ETS, FEEBATES, ENERGY_EFFICIENCY_REGULATIONS, TCP,
    COAL_EXCISE, ROAD_FUEL_TAX, ELECTRICITY_EMISSION_TAX, POWER_FEEBATE, ELECTRICITY_EXCISE,
    VEHICLE_FUEL_ECONOMY, RESIDENTIAL_EFFICIENCY_REGULATIONS, INDUSTRIAL_EFFICIENCY_REGULATIONS
)

EXISTING_ETS_CT_F_FUELS = sorted([COA, NGA, OOP, GSO, DIE, KER, LPG, JFU, BIO])
MT_OUTPUTS_COLUMNS = [
    'Include?', 'Country', 'Scenario', 'CPATIndicator', 'CPATCode',
    'MTCode', 'Tab', 'Variable', 'Unit', 'SubScenario'
]

### Conversion factors
KTOE_TO_GWH = 11.63 # ktoe to GWh
GWH_TO_MWY = 1000 / (365 * 24) # GWh to MWy
KTOE_TO_MWY = KTOE_TO_GWH * GWH_TO_MWY
KWH_TO_GJ = 3.6 / 1e3 # same as 3600 / 1000000
BARREL_TO_GJ = 6.12
KTOE_TO_GJ = 41868
