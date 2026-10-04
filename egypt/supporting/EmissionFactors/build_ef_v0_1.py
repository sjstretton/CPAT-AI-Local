"""Build EGY_CBAM_EF_v0.1.xlsx: auditable derivation of direct (Scope 1) emission factors for Egypt's CBAM goods,
split four ways:
  fc = fuel combustion CO2          (fuel burned for heat: kilns, reformer burners, EAF burners, boilers)
  fp = fuel-based process CO2       (fuel carbon entering the process as reductant / feedstock: NG reformer feed in
                                     DRI and ammonia, coke + PCI in a blast furnace; incl. carbon carried in DRI)
  np = non-fuel process CO2         (carbonate decomposition, carbon anodes, EAF electrodes / charge carbon,
                                     CO2 chemically bound in urea under the IPCC netting convention)
  no = non-CO2 process gases        (N2O from nitric acid, PFCs from aluminium electrolysis), CO2e

Every number in the workbook is either (a) a standard factor or Egypt input with a SourceID in `Sources`, or (b) a
formula. Inputs are exposed as workbook-level defined names (= their Code) so every derivation step reads
`=dri_ng_total*dri_feed_share*ef_ng` rather than cell addresses; `Derivation` column G shows the live formula text.

Companion document: EGY_CBAM_EF_Methodology_v0.1.md (same folder). Run: python build_ef_v0_1.py (openpyxl); then
recalc_and_check.py (Excel COM) recalculates, verifies the Checks sheet and prints the Summary.
"""
import datetime
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "v0.1"
DST = os.path.join(HERE, "EGY_CBAM_EF_%s.xlsx" % VERSION)
TODAY = datetime.date(2026, 10, 2).isoformat()

# NORMS.md colours
TITLE = PatternFill("solid", fgColor="00B050")
SECTION = PatternFill("solid", fgColor="92D050")
GREEN = PatternFill("solid", fgColor="EBF1DE")     # inputs
BLUE = PatternFill("solid", fgColor="DCE6F1")      # codes
TAN = PatternFill("solid", fgColor="DDD9C4")       # switches
GREY = PatternFill("solid", fgColor="F2F2F2")      # inactive / reference only
REVIEW = PatternFill("solid", fgColor="FFF2CC")    # results / to review
ARIAL = Font(name="Arial", size=10)
BOLD = Font(name="Arial", size=10, bold=True)
WHITE_BOLD = Font(name="Arial", size=14, bold=True, color="FFFFFF")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

# ----------------------------------------------------------------------------------------------------------------
# 1. SOURCES  (id, short, full reference, url, type)   type: Authoritative / Estimate / Proxy / Internal
# ----------------------------------------------------------------------------------------------------------------
SOURCES = [
    ("S01", "IPCC 2006 Vol.2 Ch.1-2", "IPCC (2006) Guidelines for National GHG Inventories, Vol. 2 Energy, Ch. 1-2 "
     "(Table 1.2 NCV, Table 2.2 p. 2.16 default CO2 emission factors for stationary combustion; verified from PDF: "
     "NG 56.1, other bituminous coal 94.6, residual fuel oil 77.4, petroleum coke 97.5, coke oven coke 107 tCO2/TJ)",
     "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf",
     "Authoritative"),
    ("S02", "CBAM IR 2023/1773 Annex VIII / Guidance Doc 3 Tables 4-7..4-12", "Commission Implementing Regulation "
     "(EU) 2023/1773, Annex VIII standard factors; EC CBAM Guidance Document 3 (Methodology), Tables 4-7 to 4-12 "
     "(fuel EFs, carbonate stoichiometric factors, carbon contents of process materials, GWPs)",
     "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en", "Authoritative"),
    ("S03", "IPCC 2006 Vol.3 Ch.2 (2A1 cement)", "IPCC (2006) Vol. 3 IPPU, Ch. 2 Mineral industry: Eq. 2.4 (p. 2.12) "
     "Tier 1 clinker EF 0.52 tCO2/t (0.51 at 65% CaO x CKD correction 1.02); Table 2.4 (p. 2.22) stoichiometric "
     "0.785 tCO2/t CaO. NOTE: the MgO factor 1.092 is NOT printed in IPCC; it is the derived molar ratio "
     "44.01/40.30 used by GCCA/CSI and EU ETS (computed here from molar masses).",
     "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_2_Ch2_Mineral_Industry.pdf",
     "Authoritative"),
    ("S04", "IPCC 2006 Vol.3 Ch.3 (2B1 ammonia, 2B2 nitric acid)", "IPCC (2006) Vol. 3 Ch. 3 Chemical industry: "
     "Table 3.1 (p. 3.15) ammonia total fuel requirement and EF (modern conventional/autothermal reforming NG "
     "30.2 GJ/t, 1.694 tCO2/t; European average, mix of modern and older NG plants 37.5 GJ/t, 2.104 tCO2/t; "
     "CCF 15.3 kgC/GJ); Table 3.3 (p. 3.23) nitric acid N2O defaults (kg N2O/t HNO3). Verified from PDF.",
     "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_3_Ch3_Chemical_Industry.pdf",
     "Authoritative"),
    ("S05", "IPCC 2006 Vol.3 Ch.4 (2C1 iron & steel, 2C3 aluminium)", "IPCC (2006) Vol. 3 Ch. 4 Metal industry: "
     "Table 4.1 iron & steel Tier 1 EFs; Table 4.10 anode CO2 (prebake 1.6, Soderberg 1.7 tCO2/t Al); "
     "Table 4.15 Tier 1 PFC EFs by cell technology (CWPB 0.4 kg CF4/t, 0.04 kg C2F6/t)",
     "https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_4_Ch4_Metal_Industry.pdf", "Authoritative"),
    ("S06", "IPCC AR6 WGI Ch.7 Table 7.SM.7", "IPCC (2021) AR6 WGI, GWP100: N2O 273, CF4 7380, C2F6 12400",
     "https://www.ipcc.ch/report/ar6/wg1/", "Authoritative"),
    ("S07", "Midrex process energy", "Midrex Technologies, process descriptions / World DRI Statistics: natural-gas "
     "Midrex plants consume about 10-11 GJ NG per t DRI (approx. 2.5 Gcal/t), of which the larger part is reformed "
     "to reducing gas and the remainder fired in the reformer burners together with recycled top gas",
     "https://www.midrex.com/", "Estimate"),
    ("S08", "World Steel Association", "worldsteel annual crude steel production (Egypt: 2020 8.2, 2021 10.3, "
     "2022 9.8, 2023 10.4, 2024 10.7 Mt; read via secondary aggregation, verify against World Steel in Figures). "
     "Route: 100% EAF assumed; EISCO Helwan BF closure (2021) is widely reported but NOT yet confirmed from a "
     "citable primary source - VERIFY", "https://worldsteel.org/data/annual-production-steel-data/", "Estimate"),
    ("S08b", "Ezz Steel (EZDK) corporate", "Ezz Steel plant pages: integrated route = direct reduction plants "
     "(three Midrex, one HYL/Energiron at Suez) feeding EAFs; charge ~80% DRI + scrap; ~5 Mt DRI/yr (2017 figure)",
     "https://www.ezzsteel.com/ezz-steel-plants", "Authoritative"),
    ("S09", "GCCA GNR / IEA cement", "GCCA Getting the Numbers Right (GNR) database and IEA cement tracking: thermal "
     "energy intensity 3.3-3.7 GJ/t clinker for dry preheater/precalciner kilns; Egypt fuel switch to coal/petcoke "
     "after the 2014 authorisation", "https://gccassociation.org/sustainability-innovation/gnr-gcca-in-numbers/",
     "Estimate"),
    ("S10", "IFA / EFMA BAT ammonia", "Fertilizers Europe (EFMA) BAT booklet No. 1 (ammonia) and IFA energy "
     "benchmarking: NG feedstock about 22-24 GJ/t NH3, fuel 7-14 GJ/t NH3 depending on plant vintage; "
     "stoichiometric minimum about 20.9 GJ/t",
     "https://www.fertilizerseurope.com/", "Estimate"),
    ("S11", "EFMA BAT nitric acid / AN", "Fertilizers Europe BAT booklets No. 2 (nitric acid) and No. 6 (AN/CAN): "
     "nitric acid is a net steam exporter (negligible fuel); AN evaporation/prilling 1.5-2.5 GJ/t; N2O abatement "
     "catalysts destroy 80-99% of N2O", "https://www.fertilizerseurope.com/", "Estimate"),
    ("S12", "IAI aluminium", "International Aluminium Institute: anode consumption 0.40-0.45 t/t Al (prebake); PFC "
     "statistics page confirms GWP vintages (AR5 CF4 6630 / C2F6 11100 used 2021-23; AR6 7380 / 12400 from 2024). "
     "Egyptalum cell technology and PFC performance NOT confirmed in this version - VERIFY",
     "https://international-aluminium.org/statistics/perfluorocarbon-pfc-emissions/", "Estimate"),
    ("S13", "Kernel v0.12 Manual inputs", "CPAT_Industry_Kernel_Egypt_v0.12.xlsx, sheet 'Manual inputs' rows 30-37 (EF block unchanged since v0.6) "
     "(current EF values, EU default values and benchmarks as recorded there; EU values to be re-verified against "
     "the Official Journal)", "cpat_excel_new/standalone_working_version/", "Internal"),
    ("S14", "Egypt plant structure (analyst)", "Analyst assessment of Egypt's plant fleet: steel = NG-based Midrex "
     "DRI + EAF (Ezz, Suez Steel, Beshay) and scrap-EAF mills; cement = dry kilns, coal/petcoke-fired since 2014-16; "
     "ammonia = NG SMR (Abu Qir, MOPCO, EFC, Helwan, KIMA, El Nasr, Alexfert); aluminium = Egyptalum Nag Hammadi "
     "prebake. To be replaced by cited plant data as collected.", "", "Estimate"),
    ("S15", "Stoichiometry", "Molar masses (IUPAC) and reaction stoichiometry: CO2/C = 44.009/12.011; CaO, MgO "
     "carbonate factors; urea CO(NH2)2 = 60.056; NH3 = 17.031; HNO3 = 63.012; NH4NO3 = 80.043",
     "", "Authoritative"),
]

# ----------------------------------------------------------------------------------------------------------------
# 2. STANDARD FACTORS (code, description, value-or-formula, unit, source, note)
# ----------------------------------------------------------------------------------------------------------------
FACTORS = [
    ("Fuel CO2 emission factors (net calorific value basis), oxidation factor 1", None, None, None, None, None),
    ("ef_ng", "Natural gas", 0.0561, "tCO2/GJ", "S01;S02", "56.1 tCO2/TJ"),
    ("ef_coal", "Other bituminous coal (steam coal)", 0.0946, "tCO2/GJ", "S01;S02", "94.6 tCO2/TJ"),
    ("ef_petcoke", "Petroleum coke", 0.0975, "tCO2/GJ", "S01;S02", "97.5 tCO2/TJ"),
    ("ef_hfo", "Residual fuel oil (mazut)", 0.0774, "tCO2/GJ", "S01;S02", "77.4 tCO2/TJ"),
    ("ef_diesel", "Gas/diesel oil", 0.0741, "tCO2/GJ", "S01;S02", "74.1 tCO2/TJ"),
    ("ef_coke", "Coke oven coke", 0.1070, "tCO2/GJ", "S01;S02", "107 tCO2/TJ"),
    ("ef_cog", "Coke oven gas", 0.0444, "tCO2/GJ", "S01;S02", "44.4 tCO2/TJ"),
    ("ef_af_fossil", "Fossil fraction of waste-derived fuels (RDF, tyres)", 0.0917, "tCO2/GJ", "S01;S02",
     "IPCC MSW fossil fraction 91.7 tCO2/TJ; biogenic fraction counted as zero"),
    ("oxf", "Oxidation factor", 1.0, "-", "S01;S02", "IPCC / CBAM default"),
    ("Global warming potentials (GWP100), tCO2e per t gas", None, None, None, None, None),
    ("gwp_n2o_cbam", "N2O - CBAM / EU MRR (AR5)", 265, "tCO2e/t", "S02", ""),
    ("gwp_cf4_cbam", "CF4 - CBAM / EU MRR (AR5)", 6630, "tCO2e/t", "S02", ""),
    ("gwp_c2f6_cbam", "C2F6 - CBAM / EU MRR (AR5)", 11100, "tCO2e/t", "S02", ""),
    ("gwp_n2o_ar6", "N2O - IPCC AR6", 273, "tCO2e/t", "S06", ""),
    ("gwp_cf4_ar6", "CF4 - IPCC AR6", 7380, "tCO2e/t", "S06", ""),
    ("gwp_c2f6_ar6", "C2F6 - IPCC AR6", 12400, "tCO2e/t", "S06", ""),
    ("gwp_n2o", "N2O - selected set (Settings!gwp_set)", '=IF(gwp_set="AR6",gwp_n2o_ar6,gwp_n2o_cbam)', "tCO2e/t",
     "calc", ""),
    ("gwp_cf4", "CF4 - selected set", '=IF(gwp_set="AR6",gwp_cf4_ar6,gwp_cf4_cbam)', "tCO2e/t", "calc", ""),
    ("gwp_c2f6", "C2F6 - selected set", '=IF(gwp_set="AR6",gwp_c2f6_ar6,gwp_c2f6_cbam)', "tCO2e/t", "calc", ""),
    ("Molar masses and stoichiometric factors", None, None, None, None, None),
    ("m_c", "Carbon", 12.011, "g/mol", "S15", ""),
    ("m_co2", "CO2", 44.009, "g/mol", "S15", ""),
    ("m_cao", "CaO", 56.077, "g/mol", "S15", ""),
    ("m_mgo", "MgO", 40.304, "g/mol", "S15", ""),
    ("m_nh3", "NH3", 17.031, "g/mol", "S15", ""),
    ("m_urea", "Urea CO(NH2)2", 60.056, "g/mol", "S15", ""),
    ("m_hno3", "HNO3", 63.012, "g/mol", "S15", ""),
    ("m_an", "NH4NO3", 80.043, "g/mol", "S15", ""),
    ("m_caco3", "CaCO3", 100.086, "g/mol", "S15", ""),
    ("c_to_co2", "tCO2 per t carbon", "=m_co2/m_c", "t/t", "calc", "3.664"),
    ("ef_caco3", "tCO2 per t CaCO3 (limestone) calcined (CBAM Method A)", "=m_co2/m_caco3", "t/t", "calc;S02",
     "0.440"),
    ("ef_cao", "tCO2 per t CaO from CaCO3 (CBAM Method B)", "=m_co2/m_cao", "t/t", "calc;S02", "0.785"),
    ("ef_mgo", "tCO2 per t MgO from MgCO3 (CBAM Method B)", "=m_co2/m_mgo", "t/t", "calc;S02", "1.092"),
    ("co2_per_urea", "CO2 chemically bound per t urea", "=m_co2/m_urea", "t/t", "calc", "0.733"),
    ("nh3_per_urea_st", "NH3 per t urea (stoichiometric)", "=2*m_nh3/m_urea", "t/t", "calc", "0.567"),
    ("hno3_per_an_st", "HNO3 (100%) per t AN (stoichiometric)", "=m_hno3/m_an", "t/t", "calc", "0.787"),
    ("nh3_per_an_st", "NH3 per t AN for neutralisation (stoichiometric)", "=m_nh3/m_an", "t/t", "calc", "0.213"),
    ("nh3_per_hno3_st", "NH3 per t HNO3 (100%) (stoichiometric)", "=m_nh3/m_hno3", "t/t", "calc", "0.270"),
    ("Carbon content of process materials (CBAM Guidance 3, Table 4-11)", None, None, None, None, None),
    ("cc_electrode", "EAF carbon electrodes", 0.8188, "tC/t", "S02", "3.00 tCO2/t"),
    ("cc_charge_carbon", "EAF charge carbon (coal / petcoke injected)", 0.8297, "tC/t", "S02", "3.04 tCO2/t"),
    ("cc_dri", "Direct reduced iron (DRI/HBI)", 0.0191, "tC/t", "S02", "0.07 tCO2/t"),
    ("cc_steel", "Crude steel", 0.0109, "tC/t", "S02", "0.04 tCO2/t"),
    ("cc_pig_iron", "Pig iron / hot metal", 0.0409, "tC/t", "S02", "0.15 tCO2/t"),
    ("cc_coke", "Metallurgical coke (carbon content)", 0.85, "tC/t", "S05", "IPCC 2006 Table 4.3 default 0.83"),
    ("cc_pci_coal", "PCI coal (carbon content)", 0.80, "tC/t", "S05", "IPCC 2006 Table 4.3 coal 0.67-0.80"),
    ("ncv_ng", "Natural gas NCV", 48.0, "GJ/t", "S01", "Table 4-7: 48.0 TJ/Gg"),
    ("IPCC Tier 1 reference values (comparison only, not used in the derivation)", None, None, None, None, None),
    ("ipcc_clinker_t1", "Clinker CO2, Tier 1 incl. CKD correction", 0.52, "tCO2/t clinker", "S03", "0.51 x 1.02"),
    ("ipcc_nh3_conv", "Ammonia, modern conventional / autothermal reforming NG", 1.694, "tCO2/t NH3", "S04",
     "Table 3.1: 30.2 GJ/t x 15.3 kgC/GJ x 44/12"),
    ("ipcc_nh3_euavg", "Ammonia, European average (mix of modern and older NG plants)", 2.104, "tCO2/t NH3", "S04",
     "Table 3.1: 37.5 GJ/t x 15.3 kgC/GJ x 44/12"),
    ("ipcc_n2o_mp", "Nitric acid N2O, medium-pressure plant, unabated", 7.0, "kg N2O/t HNO3", "S04",
     "Table 3.3; range 4-10; high-pressure 9, atmospheric 5"),
    ("ipcc_n2o_destr", "Nitric acid N2O, with process-integrated or tail-gas destruction", 2.5, "kg N2O/t HNO3",
     "S04", "Table 3.3; NSCR 2"),
    ("ipcc_anode_prebake", "Aluminium anode CO2, prebake Tier 1", 1.6, "tCO2/t Al", "S05", "Table 4.10"),
    ("ipcc_cf4_cwpb", "CF4 Tier 1, centre-worked prebake", 0.4, "kg/t Al", "S05", "Table 4.15"),
    ("ipcc_c2f6_cwpb", "C2F6 Tier 1, centre-worked prebake", 0.04, "kg/t Al", "S05", "Table 4.15"),
    ("ipcc_dri_t1", "DRI Tier 1 (all NG carbon)", 0.70, "tCO2/t DRI", "S05", "Table 4.1"),
    ("ipcc_eaf_t1", "EAF Tier 1", 0.08, "tCO2/t steel", "S05", "Table 4.1"),
]

# ----------------------------------------------------------------------------------------------------------------
# 3. SETTINGS (code, description, value, allowed, note)
# ----------------------------------------------------------------------------------------------------------------
SETTINGS = [
    ("gwp_set", "GWP set for N2O and PFCs", "CBAM", "CBAM | AR6",
     "CBAM = Implementing Regulation 2023/1773 Annex VIII (AR5 values, used by EU ETS/CBAM). AR6 for inventory-style "
     "reporting."),
    ("urea_conv", "Treatment of CO2 chemically bound in urea", "CBAM", "CBAM | IPCC",
     "CBAM: CO2 consumed in urea is counted as emitted at the ammonia plant and NOT deducted (Guidance 5c s.3.1.1); "
     "urea np = 0. IPCC: inventory netting - bound CO2 deducted at the urea plant (np = -0.733) and released on soil "
     "application (AFOLU 3C3). Kernel v0.12 uses IPCC."),
    ("ref_year", "Reference year of the Egypt inputs", 2022, "year", "Base year of the kernel (Settings!B6)."),
]

# ----------------------------------------------------------------------------------------------------------------
# 4. EGYPT INPUTS  (code, description, value, unit, low, high, tier, source, note)
#    Tier: A = Egypt plant data; B = Egypt sector statistic; C = technology default calibrated to Egypt's plant fleet;
#          D = international / IPCC default.  Low/High = plausible range used in Checks (sensitivity).
# ----------------------------------------------------------------------------------------------------------------
INPUTS = [
    ("STEEL - DRI (Midrex, natural gas) and EAF", None, None, None, None, None, None, None, None),
    ("dri_ng_total", "Natural gas use of the DRI plant, total (reformer feed + burner fuel)", 10.5, "GJ/t DRI",
     9.6, 11.5, "C", "S07;S14", "Midrex NG plants ~2.5 Gcal/t DRI; Egypt plants are Midrex (Ezz, Suez, Beshay)."),
    ("dri_feed_share", "Share of DRI natural gas that is reformed to reducing gas (reductant / feedstock)", 0.75,
     "share", 0.70, 0.80, "C", "S07", "Remainder is fired in the reformer burners (with recycled top gas) = fc."),
    ("dri_per_steel", "DRI charged per t crude steel on the DRI-EAF route", 0.98, "t DRI/t steel", 0.90, 1.10, "C",
     "S14", "~85% DRI / 15% scrap charge, ~1.15 t metallics per t liquid steel."),
    ("eaf_ng_dri", "EAF meltshop natural gas (burners, ladle furnace, preheating), DRI-EAF route", 0.6,
     "GJ/t steel", 0.3, 1.2, "C", "S14", "Crude-steel boundary: reheating furnaces for rolling excluded."),
    ("eaf_ng_scrap", "EAF meltshop natural gas, scrap-EAF route", 0.8, "GJ/t steel", 0.4, 1.5, "C", "S14",
     "Scrap melting uses more oxy-fuel burner energy than hot/warm DRI charging."),
    ("eaf_electrode", "Graphite electrode consumption", 2.5, "kg/t steel", 1.5, 3.5, "C", "S14", ""),
    ("eaf_charge_c_dri", "Charge / injection carbon, DRI-EAF route", 10, "kg/t steel", 5, 20, "C", "S14",
     "Slag foaming carbon; DRI carbon (cc_dri) supplies part of the carbon need."),
    ("eaf_charge_c_scrap", "Charge / injection carbon, scrap-EAF route", 12, "kg/t steel", 5, 20, "C", "S14", ""),
    ("eaf_limestone", "Limestone / dolomite charged directly (not pre-burnt lime)", 0, "kg/t steel", 0, 30, "C",
     "S14", "Egypt EAFs charge purchased lime; its CO2 is emitted at the lime kiln (outside the steel boundary)."),
    ("STEEL - BF-BOF (reference route only; no Egyptian production since 2021)", None, None, None, None, None, None,
     None, None),
    ("bf_coke", "Coke rate", 0.35, "t/t hot metal", 0.30, 0.45, "D", "S05;S08", "Global average ~ 350 kg/t HM"),
    ("bf_pci", "Pulverised coal injection", 0.15, "t/t hot metal", 0.10, 0.20, "D", "S05;S08", ""),
    ("hm_c", "Carbon content of hot metal", 0.045, "tC/t HM", 0.040, 0.048, "D", "S02", ""),
    ("hm_per_steel", "Hot metal per t crude steel (BOF)", 0.95, "t HM/t steel", 0.85, 1.0, "D", "S08", ""),
    ("bof_other_fuel", "Other fuels burned per t steel (coke ovens, sinter, stoves net of BF gas, BOF)", 3.0,
     "GJ/t steel", 2.0, 5.0, "D", "S08", "Works gases are derived from the coke/coal carbon counted in fp; this "
     "row is for purchased NG/oil only."),
    ("bf_flux", "Limestone + dolomite flux (sinter plant, BF, BOF)", 0.12, "t/t steel", 0.08, 0.20, "D", "S05", ""),
    ("CEMENT - grey clinker, dry process", None, None, None, None, None, None, None, None),
    ("clk_thermal", "Kiln thermal energy", 3.5, "GJ/t clinker", 3.2, 3.9, "C", "S09;S14",
     "Dry 4-5 stage preheater kilns; Egyptian kilns burning coal/petcoke tend to the upper half of the range."),
    ("clk_sh_coal", "Fuel share - coal", 0.45, "share of GJ", 0.30, 0.60, "C", "S09;S14", "Post-2014 fuel switch."),
    ("clk_sh_petcoke", "Fuel share - petroleum coke", 0.40, "share of GJ", 0.25, 0.55, "C", "S09;S14", ""),
    ("clk_sh_ng", "Fuel share - natural gas", 0.05, "share of GJ", 0.0, 0.20, "C", "S09;S14", ""),
    ("clk_sh_hfo", "Fuel share - heavy fuel oil", 0.02, "share of GJ", 0.0, 0.10, "C", "S09;S14", ""),
    ("clk_sh_af", "Fuel share - alternative fuels (RDF, tyres, biomass)", 0.08, "share of GJ", 0.03, 0.15, "C",
     "S09;S14", "Shares must sum to 1 (Checks)."),
    ("clk_af_fossil", "Fossil fraction of alternative fuels (energy basis)", 0.5, "share", 0.3, 0.7, "D", "S01", ""),
    ("clk_cao", "CaO content of clinker", 0.65, "t/t clinker", 0.63, 0.67, "C", "S03;S14", "Typical Portland clinker."),
    ("clk_mgo", "MgO content of clinker (from carbonate)", 0.015, "t/t clinker", 0.01, 0.03, "C", "S03;S14", ""),
    ("clk_ckd", "Cement kiln dust / bypass dust correction factor", 1.02, "-", 1.00, 1.05, "D", "S03",
     "IPCC Tier 1 default; Egyptian kilns with chlorine bypass may be higher."),
    ("clk_ratio", "Clinker-to-cement ratio (memo, for cement EF)", 0.85, "t clinker/t cement", 0.75, 0.92, "C",
     "S09;S14", "Egypt produces mostly CEM I / CEM II with high clinker factor."),
    ("AMMONIA - steam methane reforming + Haber-Bosch", None, None, None, None, None, None, None, None),
    ("nh3_ng_total", "Natural gas use of the ammonia plant, total (feedstock + fuel)", 35.2, "GJ/t NH3", 30.2, 37.5,
     "D", "S04;S10;S14", "VERIFY. Egypt fleet of Uhde/KBR plants (1979-2019 vintage): analyst mid-point between "
     "IPCC Table 3.1 modern plants (30.2 GJ/t) and European average of mixed vintage (37.5 GJ/t), used until "
     "plant data are collected. The kernel's EU Egypt default 2.05 tCO2/t implies ~36.5 GJ/t."),
    ("nh3_ng_feed", "Natural gas used as feedstock (reformer feed -> H2 + process CO2)", 22.5, "GJ/t NH3", 21.0,
     24.0, "C", "S10", "Yields the concentrated process-CO2 stream (~1.2-1.3 tCO2/t NH3)."),
    ("UREA - synthesis from NH3 and process CO2", None, None, None, None, None, None, None, None),
    ("urea_fuel", "Natural gas for steam attributable to the urea plant", 2.0, "GJ/t urea", 1.5, 3.0, "C", "S10;S14",
     "Steam usually from the ammonia complex; attributed to urea per CBAM measurable-heat rules."),
    ("urea_nh3_in", "Ammonia input per t urea", 0.570, "t NH3/t urea", 0.567, 0.580, "C", "S15", "Stoich. 0.567 + losses"),
    ("NITRIC ACID (precursor of AN) - Ostwald process", None, None, None, None, None, None, None, None),
    ("hno3_n2o_unab", "N2O generation, unabated medium-pressure plant", 7.0, "kg N2O/t HNO3", 4.0, 10.0, "D", "S04",
     "IPCC Table 3.3"),
    ("hno3_n2o_abat", "N2O emission with secondary / tertiary abatement", 2.5, "kg N2O/t HNO3", 0.5, 2.5, "D",
     "S04;S11", "IPCC default for process-integrated / tail-gas destruction; modern catalysts reach 0.5-1."),
    ("hno3_abat_share", "Share of Egyptian nitric acid output with N2O abatement", 0.5, "share", 0.0, 0.8, "C",
     "S14", "Abu Qir Fertilizers ran CDM N2O abatement on its nitric acid lines; other plants assumed unabated. "
     "VERIFY against UNFCCC CDM registry and current operation."),
    ("hno3_fuel", "Fuel burned in nitric acid production", 0.0, "GJ/t HNO3", 0.0, 0.5, "D", "S11",
     "Exothermic process, net steam exporter."),
    ("AMMONIUM NITRATE - neutralisation, evaporation, prilling/granulation", None, None, None, None, None, None, None,
     None),
    ("an_fuel", "Natural gas for evaporation, drying, prilling", 2.0, "GJ/t AN", 1.5, 2.5, "C", "S11;S14", ""),
    ("an_hno3_in", "Nitric acid (100%) input per t AN", 0.79, "t HNO3/t AN", 0.787, 0.80, "C", "S15", "Stoich. 0.787"),
    ("an_nh3_in", "Ammonia input to neutralisation per t AN", 0.215, "t NH3/t AN", 0.213, 0.22, "C", "S15",
     "Stoich. 0.213; the NH3 consumed to make the HNO3 is counted via the HNO3 precursor."),
    ("ALUMINIUM - Hall-Heroult, prebaked anodes (Egyptalum, Nag Hammadi)", None, None, None, None, None, None, None,
     None),
    ("al_anode_net", "Net anode consumption", 0.44, "t anode/t Al", 0.40, 0.48, "C", "S12;S14",
     "Older prebake potlines consume more anode than modern (0.40-0.42)."),
    ("al_anode_s", "Sulphur content of anode", 0.02, "share", 0.01, 0.03, "D", "S05", "IPCC Tier 2 default"),
    ("al_anode_ash", "Ash content of anode", 0.004, "share", 0.002, 0.01, "D", "S05", "IPCC Tier 2 default"),
    ("al_bake_np", "Process CO2 from anode baking (pitch volatiles, packing coke)", 0.05, "tCO2/t Al", 0.03, 0.08,
     "D", "S05", "IPCC Tier 2 baking-furnace terms, typical value."),
    ("al_ng_total", "Natural gas: anode baking furnaces + casthouse + auxiliaries", 2.2, "GJ/t Al", 1.5, 3.0, "C",
     "S12;S14", "Electricity for electrolysis is Scope 2 (excluded here)."),
    ("al_cf4", "CF4 emission rate", 0.10, "kg CF4/t Al", 0.05, 0.40, "D", "S12;S14",
     "VERIFY. Assumes point-fed prebake with medium anode-effect performance (Egyptalum cell technology not "
     "confirmed); IPCC Tier 1 CWPB default 0.4 kg/t (1990 data) is the upper bound = +2.0 tCO2e/t."),
    ("al_c2f6", "C2F6 emission rate", 0.01, "kg C2F6/t Al", 0.005, 0.04, "D", "S12;S14", "C2F6/CF4 mass ratio ~0.1"),
    ("EGYPT PRODUCTION (reference year; for reconciliation checks only)", None, None, None, None, None, None, None,
     None),
    ("prod_steel_dri", "Crude steel, DRI-EAF route", 5100, "kt", None, None, "B", "S08;S13", "Kernel v0.12 block input"),
    ("prod_steel_scrap", "Crude steel, scrap-EAF route", 4800, "kt", None, None, "B", "S08;S13", "Kernel v0.12 block input"),
    ("prod_clinker", "Clinker", 50000, "kt", None, None, "B", "S13", "Kernel v0.12 block input (cement ~ clinker/ratio)"),
    ("prod_nh3", "Ammonia (net merchant, excl. captive use)", 1785, "kt", None, None, "B", "S13", "Kernel v0.12"),
    ("prod_urea", "Urea", 2800, "kt", None, None, "B", "S13", "Kernel v0.12 (national output is higher; verify)"),
    ("prod_an", "Ammonium nitrate", 600, "kt", None, None, "B", "S13", "Kernel v0.12"),
    ("prod_al", "Primary aluminium", 300, "kt", None, None, "B", "S13", "Kernel v0.12"),
]

# ----------------------------------------------------------------------------------------------------------------
# 5. DERIVATION STEPS   (step id, description, formula, unit, component, note)   -- id None => section header
#    Outputs (component != None and id startswith 'ef_') become defined names.
# ----------------------------------------------------------------------------------------------------------------
DERIV = [
    ("P1 DRI - direct reduced iron (per t DRI)", None, None, None, None, None),
    ("dri_co2_total", "Total CO2 from natural gas carbon entering the DRI plant", "=dri_ng_total*ef_ng*oxf",
     "tCO2/t DRI", "", "All NG carbon ends as CO2 except the carbon retained in the DRI."),
    ("dri_c_retained", "CO2-equivalent of carbon retained in the DRI (released later in the EAF)", "=cc_dri*c_to_co2",
     "tCO2/t DRI", "", "CBAM Table 4-11 carbon content 1.91%"),
    ("ef_dri_fp", "fp: reformer feed gas carbon (reductant), net of carbon retained in DRI",
     "=dri_ng_total*dri_feed_share*ef_ng*oxf-dri_c_retained", "tCO2/t DRI", "fp",
     "Reductant carbon: CO in the reducing gas oxidised to CO2 in the shaft; top gas then burned."),
    ("ef_dri_fc", "fc: reformer burner fuel gas", "=dri_ng_total*(1-dri_feed_share)*ef_ng*oxf", "tCO2/t DRI", "fc",
     "Natural gas fired directly in the reformer burners (recycled top gas is already counted in fp)."),
    ("ef_dri_np", "np: none", "=0", "tCO2/t DRI", "np", "No carbonate flux in the shaft furnace."),
    ("ef_dri_no", "no: none", "=0", "tCO2e/t DRI", "no", ""),
    ("dri_check", "Check: fc + fp + retained = total", "=ef_dri_fc+ef_dri_fp+dri_c_retained-dri_co2_total",
     "tCO2/t DRI", "", "Must be 0"),
    ("P2 EAF on the DRI route (per t crude steel, meltshop only)", None, None, None, None, None),
    ("ef_eafd_fc", "fc: natural gas burners / ladle furnace", "=eaf_ng_dri*ef_ng*oxf", "tCO2/t steel", "fc", ""),
    ("ef_eafd_fp", "fp: carbon carried in the DRI, oxidised in the EAF, net of carbon in steel",
     "=dri_per_steel*dri_c_retained-cc_steel*c_to_co2", "tCO2/t steel", "fp",
     "Reductant-derived carbon; completes the DRI carbon balance."),
    ("ef_eafd_np", "np: electrodes + charge carbon + direct limestone",
     "=(eaf_electrode*cc_electrode+eaf_charge_c_dri*cc_charge_carbon)/1000*c_to_co2+eaf_limestone/1000*ef_caco3",
     "tCO2/t steel", "np", "0.44 tCO2/t CaCO3 (CBAM Table 4-9). Non-fuel process materials."),
    ("ef_eafd_no", "no: none", "=0", "tCO2e/t steel", "no", ""),
    ("P3 EAF on the scrap route (per t crude steel)", None, None, None, None, None),
    ("ef_eafs_fc", "fc: natural gas burners / ladle furnace", "=eaf_ng_scrap*ef_ng*oxf", "tCO2/t steel", "fc", ""),
    ("ef_eafs_fp", "fp: none (no reductant)", "=0", "tCO2/t steel", "fp", "Scrap carbon (1.1%) ~ carbon in product."),
    ("ef_eafs_np", "np: electrodes + charge carbon + direct limestone",
     "=(eaf_electrode*cc_electrode+eaf_charge_c_scrap*cc_charge_carbon)/1000*c_to_co2+eaf_limestone/1000*ef_caco3",
     "tCO2/t steel", "np", ""),
    ("ef_eafs_no", "no: none", "=0", "tCO2e/t steel", "no", ""),
    ("P4 BF-BOF reference route (per t crude steel) - no Egyptian production", None, None, None, None, None),
    ("ef_bof_fp", "fp: coke + PCI carbon into the blast furnace, net of carbon in hot metal and steel",
     "=((bf_coke*cc_coke+bf_pci*cc_pci_coal-hm_c)*hm_per_steel-cc_steel)*c_to_co2", "tCO2/t steel", "fp",
     "Includes CO2 from BF gas burned in stoves / power plant (carbon entered as reductant)."),
    ("ef_bof_fc", "fc: other purchased fuels", "=bof_other_fuel*ef_ng*oxf", "tCO2/t steel", "fc",
     "Assumed natural gas; coal for coke ovens is in cc_coke via coke rate (simplification)."),
    ("ef_bof_np", "np: limestone / dolomite flux", "=bf_flux*ef_caco3", "tCO2/t steel", "np", "limestone basis"),
    ("ef_bof_no", "no: none", "=0", "tCO2e/t steel", "no", ""),
    ("P5 Clinker (per t clinker)", None, None, None, None, None),
    ("clk_ef_mix", "Weighted fuel EF of the kiln fuel mix",
     "=clk_sh_coal*ef_coal+clk_sh_petcoke*ef_petcoke+clk_sh_ng*ef_ng+clk_sh_hfo*ef_hfo+clk_sh_af*clk_af_fossil*ef_af_fossil",
     "tCO2/GJ", "", "Biogenic share of alternative fuels counted as zero."),
    ("ef_clk_fc", "fc: kiln fuel combustion", "=clk_thermal*clk_ef_mix*oxf", "tCO2/t clinker", "fc", ""),
    ("ef_clk_fp", "fp: none", "=0", "tCO2/t clinker", "fp", ""),
    ("ef_clk_np", "np: calcination of CaCO3 and MgCO3, corrected for kiln dust",
     "=(clk_cao*ef_cao+clk_mgo*ef_mgo)*clk_ckd", "tCO2/t clinker", "np", "CBAM Method B / IPCC Tier 2"),
    ("ef_clk_no", "no: none", "=0", "tCO2e/t clinker", "no", ""),
    ("clk_cement_memo", "Memo: direct EF per t cement (clinker share only; grinding is electricity)",
     "=(ef_clk_fc+ef_clk_np)*clk_ratio", "tCO2/t cement", "", "Not a CBAM EF row; shown for reference."),
    ("P6 Ammonia (per t NH3)", None, None, None, None, None),
    ("nh3_ng_fuel", "Natural gas burned as fuel (total - feedstock)", "=nh3_ng_total-nh3_ng_feed", "GJ/t NH3", "", ""),
    ("ef_nh3_fp", "fp: feedstock carbon -> process CO2 stream (all counted as emitted; see urea_conv)",
     "=nh3_ng_feed*ef_ng*oxf", "tCO2/t NH3", "fp",
     "Under the CBAM convention CO2 transferred to urea remains an emission of the ammonia plant."),
    ("ef_nh3_fc", "fc: reformer and auxiliary boiler fuel", "=nh3_ng_fuel*ef_ng*oxf", "tCO2/t NH3", "fc", ""),
    ("ef_nh3_np", "np: none", "=0", "tCO2/t NH3", "np", ""),
    ("ef_nh3_no", "no: none", "=0", "tCO2e/t NH3", "no", ""),
    ("P7 Urea synthesis (per t urea, own process)", None, None, None, None, None),
    ("ef_urea_fc", "fc: steam / utilities fuel attributed to urea", "=urea_fuel*ef_ng*oxf", "tCO2/t urea", "fc", ""),
    ("ef_urea_fp", "fp: none", "=0", "tCO2/t urea", "fp", ""),
    ("ef_urea_np", "np: CO2 chemically bound in urea (0 under CBAM; -0.733 under IPCC netting)",
     '=IF(urea_conv="IPCC",-co2_per_urea,0)', "tCO2/t urea", "np", "Settings!urea_conv"),
    ("ef_urea_no", "no: none", "=0", "tCO2e/t urea", "no", ""),
    ("P8 Nitric acid (per t HNO3 100%, precursor of AN)", None, None, None, None, None),
    ("hno3_n2o_rate", "Weighted N2O emission rate",
     "=hno3_abat_share*hno3_n2o_abat+(1-hno3_abat_share)*hno3_n2o_unab", "kg N2O/t HNO3", "", ""),
    ("ef_hno3_no", "no: N2O x GWP", "=hno3_n2o_rate/1000*gwp_n2o", "tCO2e/t HNO3", "no", ""),
    ("ef_hno3_fc", "fc: fuel", "=hno3_fuel*ef_ng*oxf", "tCO2/t HNO3", "fc", ""),
    ("ef_hno3_fp", "fp: none", "=0", "tCO2/t HNO3", "fp", ""),
    ("ef_hno3_np", "np: none", "=0", "tCO2/t HNO3", "np", ""),
    ("P9 Ammonium nitrate (per t AN, own process = neutralisation + finishing)", None, None, None, None, None),
    ("ef_an_fc", "fc: evaporation / prilling fuel", "=an_fuel*ef_ng*oxf", "tCO2/t AN", "fc", ""),
    ("ef_an_fp", "fp: none", "=0", "tCO2/t AN", "fp", ""),
    ("ef_an_np", "np: none", "=0", "tCO2/t AN", "np", ""),
    ("ef_an_no", "no: none in neutralisation (N2O arises in the nitric acid precursor)", "=0", "tCO2e/t AN", "no", ""),
    ("P10 Primary aluminium (per t Al)", None, None, None, None, None),
    ("al_anode_co2", "CO2 from net anode consumption (IPCC Tier 2)",
     "=al_anode_net*(1-al_anode_s-al_anode_ash)*c_to_co2", "tCO2/t Al", "", ""),
    ("ef_al_np", "np: anode consumption + anode baking", "=al_anode_co2+al_bake_np", "tCO2/t Al", "np", ""),
    ("ef_al_fc", "fc: baking furnace, casthouse and auxiliary fuel", "=al_ng_total*ef_ng*oxf", "tCO2/t Al", "fc", ""),
    ("ef_al_fp", "fp: none (reduction is electrolytic)", "=0", "tCO2/t Al", "fp", ""),
    ("ef_al_no", "no: PFCs (CF4 + C2F6) x GWP", "=(al_cf4*gwp_cf4+al_c2f6*gwp_c2f6)/1000", "tCO2e/t Al", "no", ""),
]

# ----------------------------------------------------------------------------------------------------------------
# 6. PRODUCTS: kernel goods = own-process EF (sum of process steps) + precursor EFs (chain).  Formulas per component.
#    (name, unit, kernel row, own{comp: formula}, precursors [(label, qty-name, process prefix)], kernel values,
#     EU default base 2026, EU benchmark, kernel embed NH3)
# ----------------------------------------------------------------------------------------------------------------
def own(prefixes, weights=None):
    weights = weights or ["1"] * len(prefixes)
    return {c: "=" + "+".join("%s*ef_%s_%s" % (w, p, c) for p, w in zip(prefixes, weights)) for c in
            ("fc", "fp", "np", "no")}


PRODUCTS = [
    ("DRI-EAF steel", "t crude steel", 30, own(["dri", "eafd"], ["dri_per_steel", "1"]), [],
     (0.12903, 0.561, 0.04, 0, 0), 1.82, 0.481),
    ("Scrap-EAF steel", "t crude steel", 31, own(["eafs"]), [], (0.14025, 0, 0.015, 0, 0), 0.72, 0.072),
    ("BF-BOF steel (reference)", "t crude steel", 32, own(["bof"]), [], (0.3844, 1.5376, 0.25, 0, 0), 2.8, 1.37),
    ("Grey clinker (dry-process)", "t clinker", 33, own(["clk"]), [], (0.2883, 0, 0.526, 0, 0), 1.58, 0.666),
    ("Ammonia (net merchant)", "t NH3", 34, own(["nh3"]), [], (0.3927, 1.4586, 0, 0, 0), 2.05, 1.484),
    ("Urea", "t urea", 35, own(["urea"]), [("Ammonia", "urea_nh3_in", "nh3")],
     (0.1122, 0, -0.733, 0, 1.0709496), 1.39, 0.902),
    ("Ammonium nitrate", "t AN", 36, own(["an"]),
     [("Nitric acid", "an_hno3_in", "hno3"), ("Ammonia (neutralisation)", "an_nh3_in", "nh3"),
      ("Ammonia (via nitric acid)", "an_hno3_in*nh3_per_hno3_st", "nh3")],
     (0.1122, 0, 0, 0.97, 0.40137), 2.64, 0.302),
    ("Primary aluminium", "t Al", 37, own(["al"]), [], (0.156, 0, 1.5, 0.85, 0), 2.06, 1.423),
]
COMPS = ("fc", "fp", "np", "no")
COMP_LABEL = {"fc": "fc fuel combustion CO2", "fp": "fp fuel-based process CO2", "np": "np non-fuel process CO2",
              "no": "no non-CO2 process (CO2e)"}


# ----------------------------------------------------------------------------------------------------------------
def style_range(ws, rng, fill=None, font=None, border=True, align=None):
    for row in ws[rng]:
        for c in row:
            if fill is not None:
                c.fill = fill
            c.font = font or ARIAL
            if border:
                c.border = BOX
            if align is not None:
                c.alignment = align


def title(ws, text, subtitle, ncols):
    ws["A1"] = text
    ws["A1"].font = WHITE_BOLD
    for c in range(1, ncols + 1):
        ws.cell(1, c).fill = TITLE
    ws["A2"] = subtitle
    ws["A2"].font = ARIAL
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    ws.row_dimensions[2].height = 45


def section(ws, r, text, ncols):
    ws.cell(r, 1, text).font = BOLD
    for c in range(1, ncols + 1):
        ws.cell(r, c).fill = SECTION


def header(ws, r, labels, start_col=1):
    for i, lab in enumerate(labels):
        c = ws.cell(r, start_col + i, lab)
        c.font = BOLD
        c.fill = GREEN
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical="top")


def add_name(wb, name, sheet, cell):
    ref = "'%s'!$%s$%d" % (sheet, get_column_letter(cell.column), cell.row)
    wb.defined_names[name] = DefinedName(name, attr_text=ref)


def widths(ws, w):
    for i, x in enumerate(w, start=1):
        ws.column_dimensions[get_column_letter(i)].width = x


def build():
    wb = Workbook()
    # ------------------------------------------------------------------ ReadMe
    ws = wb.active
    ws.title = "ReadMe"
    title(ws, "Egypt CBAM goods - direct emission factors, four-way split (%s)" % VERSION,
          "Auditable derivation of Scope 1 emission factors (tCO2e per t product) for the eight CBAM goods carried in "
          "CPAT_Industry_Kernel_Egypt ('Manual inputs' H30:K37). Methodology: EGY_CBAM_EF_Methodology_%s.md."
          % VERSION, 4)
    rows = [
        ("Component", "Definition", "IPCC 2006 category", "CBAM IR 2023/1773 source stream"),
        ("fc", "Fuel combustion CO2: fuel burned for heat (kilns, reformer burners, EAF burners, boilers, baking "
         "furnaces).", "1A2 Energy - manufacturing", "Combustion emissions (Annex III B.3)"),
        ("fp", "Fuel-based process CO2: fuel carbon entering the process as reductant or feedstock (NG reformer feed "
         "in DRI and ammonia, coke/PCI in a blast furnace), incl. carbon carried in DRI to the EAF.",
         "2C1 (iron & steel), 2B1 (ammonia)", "Process emissions - mass balance (Annex III B.3.2 / B.4)"),
        ("np", "Non-fuel process CO2: carbonate decomposition (clinker, flux), carbon anodes, EAF electrodes and "
         "charge carbon; CO2 bound in urea under the IPCC netting convention (negative).",
         "2A1 (cement), 2C3 (aluminium), 2C1 (electrodes/flux)", "Process emissions (Annex III B.3.2)"),
        ("no", "Non-CO2 process gases in CO2e: N2O from nitric acid (precursor of AN), CF4 and C2F6 from aluminium "
         "electrolysis.", "2B2 (nitric acid), 2C3 (PFC)", "N2O (Annex III B.9.3), PFC (Annex III B.7)"),
        ("", "", "", ""),
        ("Sheet", "Content", "", ""),
        ("Sources", "Register of every source used (SourceID S01..). Every input row cites one or more SourceIDs.",
         "", ""),
        ("Settings", "Conventions: GWP set (CBAM/AR5 vs AR6); treatment of CO2 bound in urea (CBAM vs IPCC netting).",
         "", ""),
        ("Factors", "Standard factors: fuel EFs, GWPs, molar masses, stoichiometric factors, carbon contents, IPCC "
         "Tier 1 reference values. Each row = a defined name (column B).", "", ""),
        ("Egypt_Inputs", "Egypt-specific technology / activity parameters per process with value, range, tier "
         "(A plant data .. D international default), SourceID and note. Green cells are the only inputs.", "", ""),
        ("Derivation", "Step-by-step formulas per process (P1 DRI .. P10 aluminium). Column G shows the live formula "
         "text; outputs ef_<process>_<component> are defined names.", "", ""),
        ("Products", "Roll-up to the eight kernel goods: own-process EF by component, precursor (chain) EF by "
         "component, totals, comparison with kernel v0.12 and EU default / benchmark.", "", ""),
        ("Summary", "The deliverable table: four EFs per good (own process, as used by the kernel) plus chain totals, "
         "confidence grade and one-line derivation.", "", ""),
        ("Checks", "Balance, range and reconciliation checks; all must show OK.", "", ""),
        ("", "", "", ""),
        ("Colour", "Meaning", "", ""),
        ("green EBF1DE", "input (change only here)", "", ""),
        ("blue DCE6F1", "code / defined name", "", ""),
        ("tan DDD9C4", "convention switch", "", ""),
        ("yellow FFF2CC", "result / to review", "", ""),
        ("grey F2F2F2", "reference only (not Egyptian production)", "", ""),
        ("no fill", "calculation", "", ""),
        ("", "", "", ""),
        ("Version log", "", "", ""),
        (VERSION, TODAY, "Initial derivation; inputs are tier C/D estimates pending collection of Egyptian plant data "
         "(see Egypt_Inputs notes marked VERIFY).", ""),
    ]
    for i, row in enumerate(rows, start=4):
        for j, v in enumerate(row, start=1):
            c = ws.cell(i, j, v)
            c.font = BOLD if (i == 4 or row[0] in ("Sheet", "Colour", "Version log")) else ARIAL
            c.alignment = WRAP
    for i, fill in ((21, GREEN), (22, BLUE), (23, TAN), (24, REVIEW), (25, GREY)):
        ws.cell(i, 1).fill = fill
    widths(ws, [16, 90, 34, 40])

    # ------------------------------------------------------------------ Sources
    ws = wb.create_sheet("Sources")
    title(ws, "Sources register", "Every input in Factors and Egypt_Inputs cites a SourceID from this list. Type: "
          "Authoritative (official statistic / regulation / IPCC), Estimate (technology literature, to be replaced by "
          "Egyptian plant data), Proxy (non-Egypt data standing in), Internal (repo file).", 5)
    header(ws, 4, ["SourceID", "Short reference", "Full reference", "URL", "Type"])
    for i, s in enumerate(SOURCES, start=5):
        for j, v in enumerate(s, start=1):
            c = ws.cell(i, j, v)
            c.font = ARIAL
            c.border = BOX
            c.alignment = WRAP
        ws.cell(i, 1).fill = BLUE
    widths(ws, [10, 34, 90, 50, 14])

    # ------------------------------------------------------------------ Settings
    ws = wb.create_sheet("Settings")
    title(ws, "Settings - conventions", "Switches read by the derivation (tan cells). Change here only.", 5)
    header(ws, 4, ["Code", "Setting", "Value", "Allowed", "Note"])
    for i, (code, desc, val, allowed, note) in enumerate(SETTINGS, start=5):
        ws.cell(i, 1, code).fill = BLUE
        ws.cell(i, 2, desc)
        ws.cell(i, 3, val).fill = TAN
        ws.cell(i, 4, allowed)
        ws.cell(i, 5, note)
        for j in range(1, 6):
            ws.cell(i, j).font = ARIAL
            ws.cell(i, j).border = BOX
            ws.cell(i, j).alignment = WRAP
        add_name(wb, code, "Settings", ws.cell(i, 3))
    widths(ws, [14, 44, 10, 16, 110])

    # ------------------------------------------------------------------ Factors
    ws = wb.create_sheet("Factors")
    title(ws, "Standard factors", "Fuel emission factors, GWPs, stoichiometry and carbon contents. Column B is the "
          "defined name used in Derivation. Formulas (no fill) derive stoichiometric factors from molar masses.", 6)
    header(ws, 4, ["", "Code", "Description", "Value", "Unit", "Source", "Note"])
    r = 5
    for code, desc, val, unit, src, note in FACTORS:
        if desc is None:
            section(ws, r, code, 7)
            r += 1
            continue
        ws.cell(r, 2, code).fill = BLUE
        ws.cell(r, 3, desc)
        v = ws.cell(r, 4, val)
        if not (isinstance(val, str) and val.startswith("=")):
            v.fill = GREEN
        v.number_format = "0.0000"
        ws.cell(r, 5, unit)
        ws.cell(r, 6, src)
        ws.cell(r, 7, note)
        for j in range(2, 8):
            ws.cell(r, j).font = ARIAL
            ws.cell(r, j).border = BOX
        add_name(wb, code, "Factors", v)
        r += 1
    widths(ws, [3, 20, 62, 12, 16, 12, 60])

    # ------------------------------------------------------------------ Egypt_Inputs
    ws = wb.create_sheet("Egypt_Inputs")
    title(ws, "Egypt-specific inputs", "One row per technology / activity parameter. Tier: A = Egyptian plant data, "
          "B = Egyptian sector statistic, C = technology default calibrated to Egypt's plant fleet, D = international "
          "/ IPCC default. Low/High give the plausible range (used for sensitivity in Checks). Rows marked VERIFY "
          "are the priority for data collection.", 10)
    header(ws, 4, ["", "Code", "Description", "Value", "Unit", "Low", "High", "Tier", "Source", "Note"])
    r = 5
    for code, desc, val, unit, lo, hi, tier, src, note in INPUTS:
        if desc is None:
            section(ws, r, code, 10)
            r += 1
            continue
        ws.cell(r, 2, code).fill = BLUE
        ws.cell(r, 3, desc)
        v = ws.cell(r, 4, val)
        v.fill = GREEN
        v.number_format = "0.000" if isinstance(val, float) else "0"
        ws.cell(r, 5, unit)
        ws.cell(r, 6, lo)
        ws.cell(r, 7, hi)
        ws.cell(r, 8, tier)
        ws.cell(r, 9, src)
        ws.cell(r, 10, note)
        for j in range(2, 11):
            ws.cell(r, j).font = ARIAL
            ws.cell(r, j).border = BOX
            ws.cell(r, j).alignment = WRAP
        if "VERIFY" in (note or ""):
            ws.cell(r, 10).fill = REVIEW
        add_name(wb, code, "Egypt_Inputs", v)
        r += 1
    widths(ws, [3, 20, 60, 10, 14, 8, 8, 6, 12, 80])

    # ------------------------------------------------------------------ Derivation
    ws = wb.create_sheet("Derivation")
    title(ws, "Derivation - step by step", "Each process block computes the four components from named inputs. "
          "Column D holds the formula, column G its live text (FORMULATEXT). Rows with an ef_ code are the outputs "
          "(yellow) and become defined names used in Products.", 8)
    header(ws, 4, ["", "Step / output code", "Description", "Value", "Unit", "Component", "Formula", "Note"])
    r = 5
    for sid, desc, formula, unit, comp, note in DERIV:
        if desc is None:
            section(ws, r, sid, 8)
            r += 1
            continue
        ws.cell(r, 2, sid).fill = BLUE
        ws.cell(r, 3, desc)
        v = ws.cell(r, 4, formula)
        v.number_format = "0.0000"
        ws.cell(r, 5, unit)
        ws.cell(r, 6, comp)
        ws.cell(r, 7, "=_xlfn.FORMULATEXT(D%d)" % r)
        ws.cell(r, 8, note)
        for j in range(2, 9):
            ws.cell(r, j).font = ARIAL
            ws.cell(r, j).border = BOX
            ws.cell(r, j).alignment = WRAP
        if sid.startswith("ef_"):
            v.fill = REVIEW
        add_name(wb, sid, "Derivation", v)
        r += 1
    widths(ws, [3, 18, 70, 11, 14, 10, 70, 60])

    # ------------------------------------------------------------------ Products
    ws = wb.create_sheet("Products")
    title(ws, "Products - roll-up to the kernel goods", "Own-process EF = sum of the process steps of the route. "
          "Precursor (chain) EF = precursor quantity x precursor EF, component by component (so fuel carbon in "
          "ammonia stays fp when embedded in urea). Kernel v0.12 and EU values are hard-coded references (S13).", 24)
    cols = ["Product", "Unit", "Kernel row", "Own fc", "Own fp", "Own np", "Own no", "Own total",
            "Precursors", "Chain fc", "Chain fp", "Chain np", "Chain no", "Chain total",
            "Kernel fc", "Kernel fp", "Kernel np", "Kernel no", "Kernel embed NH3", "Kernel total",
            "Own - kernel own", "EU default base", "Own total / EU default", "EU benchmark"]
    header(ws, 4, cols)
    r = 5
    prod_rows = {}
    for name, unit, krow, ownf, precs, kern, eu_def, eu_bench in PRODUCTS:
        prod_rows[name] = r
        ws.cell(r, 1, name)
        ws.cell(r, 2, unit)
        ws.cell(r, 3, "'Manual inputs'!%d" % krow)
        for j, comp in enumerate(COMPS, start=4):
            ws.cell(r, j, ownf[comp]).number_format = "0.0000"
        ws.cell(r, 8, "=SUM(D%d:G%d)" % (r, r)).number_format = "0.0000"
        ws.cell(r, 9, "; ".join("%s x %s" % (lab, q) for lab, q, _ in precs) or "-")
        for j, comp in enumerate(COMPS, start=10):
            f = "=" + ("+".join("%s*ef_%s_%s" % (q, p, comp) for _, q, p in precs) or "0")
            ws.cell(r, j, f).number_format = "0.0000"
        ws.cell(r, 14, "=H%d+SUM(J%d:M%d)" % (r, r, r)).number_format = "0.0000"
        for j, kv in enumerate(kern, start=15):
            ws.cell(r, j, kv).number_format = "0.0000"
            ws.cell(r, j).fill = GREY
        ws.cell(r, 20, "=SUM(O%d:S%d)" % (r, r)).number_format = "0.0000"
        ws.cell(r, 21, "=H%d-SUM(O%d:R%d)" % (r, r, r)).number_format = "0.0000"
        ws.cell(r, 22, eu_def).fill = GREY
        ws.cell(r, 23, "=IF(V%d>0,N%d/V%d,\"\")" % (r, r, r)).number_format = "0.00"
        ws.cell(r, 24, eu_bench).fill = GREY
        for j in range(1, 25):
            ws.cell(r, j).font = ARIAL
            ws.cell(r, j).border = BOX
        for j in range(4, 9):
            ws.cell(r, j).fill = REVIEW
        if "reference" in name:
            for j in range(1, 4):
                ws.cell(r, j).fill = GREY
        r += 1
    ws.cell(r + 1, 1, "Chain total for urea / AN embeds the ammonia (and nitric acid) direct emissions, i.e. the "
            "CBAM 'embedded emissions incl. precursors' view. Own total is the plant-level view used by the kernel's "
            "H:K columns; the kernel carries the ammonia precursor separately in column M.").font = ARIAL
    widths(ws, [26, 13, 16] + [10] * 5 + [34] + [10] * 14)

    # ------------------------------------------------------------------ Summary
    ws = wb.create_sheet("Summary")
    title(ws, "Summary - Egypt direct emission factors for CBAM goods (tCO2e per t product)",
          "Own-process values (columns D:G) are the four kernel inputs ('Manual inputs' H:K). Chain total adds "
          "precursor emissions for urea and AN. Confidence: A plant data, B sector statistic, C calibrated "
          "technology default, D international default (lowest tier among the inputs that drive the value).", 11)
    header(ws, 4, ["Product", "Unit", "Route", "fc", "fp", "np", "no", "Total own", "Total chain", "Confidence",
                   "Derivation in one line"])
    routes = {
        "DRI-EAF steel": ("Midrex NG DRI + EAF", "C",
                          "fp = 75% of DRI gas (reformer feed, 10.5 GJ/t DRI) x 56.1 kg/GJ incl. DRI carbon; fc = "
                          "reformer burner gas + EAF gas; np = electrodes + charge carbon."),
        "Scrap-EAF steel": ("Scrap EAF", "C", "fc = EAF natural gas; np = electrodes + charge carbon; no reductant."),
        "BF-BOF steel (reference)": ("BF-BOF, reference only", "D",
                                     "fp = coke + PCI carbon net of hot-metal carbon; fc = purchased fuels; np = flux."),
        "Grey clinker (dry-process)": ("Dry kiln, coal/petcoke", "C",
                                       "fc = 3.5 GJ/t x fuel-mix EF (coal 45%, petcoke 40%); np = CaO 65% x 0.785 + "
                                       "MgO x 1.092, x1.02 CKD."),
        "Ammonia (net merchant)": ("NG SMR + Haber-Bosch", "C",
                                   "fp = feedstock 22.5 GJ/t x 56.1; fc = fuel (35.2 - 22.5) GJ/t x 56.1."),
        "Urea": ("NH3 + CO2 synthesis", "C",
                 "fc = steam fuel 2 GJ/t; np = 0 (CBAM) or -0.733 (IPCC netting); chain adds 0.57 t NH3."),
        "Ammonium nitrate": ("HNO3 + NH3 neutralisation", "C",
                             "fc = 2 GJ/t finishing fuel; chain adds 0.79 t HNO3 (N2O: weighted 4.75 kg/t x GWP) and "
                             "0.43 t NH3."),
        "Primary aluminium": ("Prebake Hall-Heroult", "C",
                              "np = 0.44 t anode x 97.6% C x 3.664 + baking; fc = 2.2 GJ/t gas; no = CF4 0.10 + C2F6 "
                              "0.01 kg/t x GWP."),
    }
    r = 5
    for name, unit, krow, _, _, _, _, _ in PRODUCTS:
        pr = prod_rows[name]
        route, conf, line = routes[name]
        ws.cell(r, 1, name)
        ws.cell(r, 2, unit)
        ws.cell(r, 3, route)
        for j, col in enumerate("DEFG", start=4):
            ws.cell(r, j, "=Products!%s%d" % (col, pr)).number_format = "0.000"
            ws.cell(r, j).fill = REVIEW
        ws.cell(r, 8, "=Products!H%d" % pr).number_format = "0.000"
        ws.cell(r, 9, "=Products!N%d" % pr).number_format = "0.000"
        ws.cell(r, 10, conf)
        ws.cell(r, 11, line)
        for j in range(1, 12):
            ws.cell(r, j).font = ARIAL
            ws.cell(r, j).border = BOX
            ws.cell(r, j).alignment = WRAP
        if "reference" in name:
            ws.cell(r, 1).fill = GREY
        r += 1
    r += 1
    ws.cell(r, 1, "Conventions in force:").font = BOLD
    ws.cell(r, 3, '="GWP set: "&gwp_set&"; urea bound CO2: "&urea_conv&"; reference year: "&ref_year').font = ARIAL
    ws.cell(r + 1, 1, "Memo: cement").font = BOLD
    ws.cell(r + 1, 3, "=clk_cement_memo").number_format = "0.000"
    ws.cell(r + 1, 4, '="tCO2/t cement at clinker ratio "&TEXT(clk_ratio,"0.00")&" (fc + np of clinker only)"').font = ARIAL
    widths(ws, [26, 13, 24, 9, 9, 9, 9, 10, 10, 11, 100])

    # ------------------------------------------------------------------ Checks
    ws = wb.create_sheet("Checks")
    title(ws, "Checks", "All rows must read OK. Tolerance 1e-9 for balances.", 5)
    header(ws, 4, ["#", "Check", "Value", "Result", "Note"])
    checks = [
        ("DRI carbon balance: fc + fp + retained - total = 0", "=dri_check", '=IF(ABS(C{r})<1E-9,"OK","FAIL")', ""),
        ("Clinker fuel shares sum to 1", "=clk_sh_coal+clk_sh_petcoke+clk_sh_ng+clk_sh_hfo+clk_sh_af",
         '=IF(ABS(C{r}-1)<1E-9,"OK","FAIL")', ""),
        ("Ammonia feedstock <= total gas", "=nh3_ng_total-nh3_ng_feed", '=IF(C{r}>=0,"OK","FAIL")', "fuel GJ/t"),
        ("DRI feed share within [0,1]", "=dri_feed_share", '=IF(AND(C{r}>=0,C{r}<=1),"OK","FAIL")', ""),
        ("Settings: GWP set valid", "=gwp_set", '=IF(OR(C{r}="CBAM",C{r}="AR6"),"OK","FAIL")', ""),
        ("Settings: urea convention valid", "=urea_conv", '=IF(OR(C{r}="CBAM",C{r}="IPCC"),"OK","FAIL")', ""),
        ("Products: own total = sum of components (all rows)",
         "=SUMPRODUCT(ABS(Products!H5:H12-Products!D5:D12-Products!E5:E12-Products!F5:F12-Products!G5:G12))",
         '=IF(C{r}<1E-9,"OK","FAIL")', ""),
        ("No negative component except urea np under IPCC netting",
         '=MIN(Products!D5:G12)+IF(urea_conv="IPCC",co2_per_urea,0)', '=IF(C{r}>=-1E-9,"OK","FAIL")', ""),
        ("Ammonia own total within IPCC Table 3.1 band (modern 1.694 .. European average 2.104)", "=Products!H9",
         '=IF(AND(C{r}>=ipcc_nh3_conv*0.95,C{r}<=ipcc_nh3_euavg*1.05),"OK","REVIEW")', "Range check, not a failure"),
        ("Clinker np within 0.50-0.55 (IPCC Tier 1 0.52)", "=ef_clk_np", '=IF(AND(C{r}>=0.50,C{r}<=0.55),"OK","REVIEW")',
         ""),
        ("Aluminium np within 1.45-1.75 (IPCC Tier 1 1.6 + baking)", "=ef_al_np",
         '=IF(AND(C{r}>=1.45,C{r}<=1.75),"OK","REVIEW")', ""),
        ("DRI total (fc+fp per t DRI, incl. retained C) vs IPCC Tier 1 0.70: ratio", "=dri_co2_total/ipcc_dri_t1",
         '=IF(AND(C{r}>=0.7,C{r}<=1.1),"OK","REVIEW")', "IPCC Tier 1 is a global default"),
        ("Own totals vs EU default base: ratio range (excl. BF-BOF reference)",
         "=MAX(Products!W5:W6,Products!W8:W12)&\" max; \"&MIN(Products!W5:W6,Products!W8:W12)&\" min\"",
         '="INFO"', "Egypt own totals are expected below EU third-country defaults (which carry mark-ups)."),
        ("Reconciliation memo: implied national direct emissions of the eight goods (MtCO2e, own process)",
         "=(prod_steel_dri*Products!H5+prod_steel_scrap*Products!H6+prod_clinker*Products!H8+prod_nh3*Products!H9"
         "+prod_urea*Products!H10+prod_an*Products!H11+prod_al*Products!H12)/1000", '="INFO"',
         "Compare with Egypt's inventory (1A2 + 2A1 + 2B1 + 2B2 + 2C1 + 2C3) once BTR1 figures are entered."),
    ]
    r = 5
    for i, (desc, val, res, note) in enumerate(checks, start=1):
        ws.cell(r, 1, i)
        ws.cell(r, 2, desc)
        ws.cell(r, 3, val).number_format = "0.0000"
        ws.cell(r, 4, res.format(r=r)).fill = REVIEW
        ws.cell(r, 5, note)
        for j in range(1, 6):
            ws.cell(r, j).font = ARIAL
            ws.cell(r, j).border = BOX
            ws.cell(r, j).alignment = WRAP
        r += 1
    ws.cell(r + 1, 2, "Overall").font = BOLD
    ws.cell(r + 1, 4, '=IF(COUNTIF(D5:D%d,"FAIL")=0,"OK","FAIL")' % (r - 1)).fill = REVIEW
    ws.cell(r + 1, 4).font = BOLD
    widths(ws, [4, 70, 16, 10, 80])

    wb.save(DST)
    print("saved", DST)


if __name__ == "__main__":
    build()
