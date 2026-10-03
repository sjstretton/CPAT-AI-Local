# Responsiveness of Industrial Process Emissions to Carbon Prices in CBAM Sectors

**Evidence from IPCC AR6 WGIII (2022), percentage reductions at USD 100/tCO2e and implied semi-elasticities**

*Prepared 2026-10-02. Companion workbook: `ProcessEmissions_CarbonPriceResponse.xlsx` (all calculations are live formulas; yellow cells are inputs).*

## 0. Headline answer


| Sector (process emissions only) | %ER @ $100, 2030 horizon | %ER @ $100, long run | %ER @ $100, central | Î² iso 2030 (%/$) | Î² iso LR (%/$) | Î² iso central (%/$) | Î² linear central (%/$) |
|---|---|---|---|---|---|---|---|
| Cement clinker / cement / concrete | 19.3% | 47.8% | 33.5% | -0.214 | -0.650 | -0.408 | -0.335 |
| Primary steel: BF-BOF route | 10.2% | 45.9% | 28.0% | -0.107 | -0.614 | -0.329 | -0.280 |
| Primary steel: natural-gas DRI-EAF route (Egypt-type) | 11.3% | 57.3% | 34.3% | -0.120 | -0.852 | -0.421 | -0.343 |
| Secondary steel: scrap-EAF | 9.5% | 26.7% | 18.1% | -0.100 | -0.310 | -0.200 | -0.181 |
| Primary aluminium (Hall-Heroult) | 6.9% | 36.4% | 21.6% | -0.072 | -0.452 | -0.244 | -0.216 |
| Ammonia (natural-gas SMR; merchant and non-urea uses) | 15.0% | 44.5% | 29.7% | -0.162 | -0.589 | -0.353 | -0.297 |
| Urea (ammonia precursor + urea plant) | 4.8% | 18.4% | 11.6% | -0.049 | -0.203 | -0.123 | -0.116 |
| Nitric acid (N2O) - component of ammonium nitrate and other N fertilisers | 79.2% | 83.6% | 81.4% | -1.570 | -1.808 | -1.682 | -0.814 |
| Ammonium nitrate - unabated N2O baseline | 67.6% | 76.6% | 72.1% | -1.128 | -1.451 | -1.277 | -0.721 |
| Ammonium nitrate - N2O already ~90% abated (EU / CDM-legacy plants) | 21.2% | 44.6% | 32.9% | -0.238 | -0.591 | -0.399 | -0.329 |
| Hydrogen (merchant, SMR) | 15.7% | 70.4% | 43.0% | -0.171 | -1.218 | -0.563 | -0.430 |

*%ER = percentage reduction of baseline process-emission intensity (tCO2e per tonne of product) at a carbon price of USD 100 (2019 dollars) per tCO2e. Î² iso = iso-semi-elastic parameter, Î² = ln(1 âˆ’ a(100))/100, expressed in % change in emissions per USD 1 of carbon price (negative = reduction). "2030 horizon" is a deployment-constrained estimate calibrated to IPCC AR6 2030 economic potentials; "long run" assumes full capital-stock turnover with the same price; "central" is the arithmetic mean of the two and is the recommended parameter for a medium-run policy model (see Â§5).*

**Cross-checks.** (i) The IPCC AR6 Table 12.3 aggregate for industry *process-related* options costing â‰¤ USD 100 in 2030 (feedstock decarbonisation/process change 0.38 Gt + cementitious substitution 0.28 Gt + non-CO2 reductions 0.20 Gt = 0.86 GtCO2e) equals **14.9%â€“16.6%** of 2030 reference industrial process emissions (central 15.7%; 23.3%â€“25.9% if enhanced recycling is included), i.e. Î² â‰ˆ -0.171 %/$. (ii) The semi-elasticity currently in the CPAT Egypt workbook, Î² = -0.1040 %/$, corresponds to a(100) = 9.9% â€” close to the IPCC 2030 aggregate for cement-dominated process emissions, but below the sector-specific 2030 estimates for nitric acid, ammonia and hydrogen, and well below long-run technology-cost potentials.

## 1. Purpose and scope

The task is to trace, as rigorously as the public evidence allows, how **process emissions** (non-combustion emissions from chemical or physical transformation of feedstocks) in the main EU CBAM sectors respond to a carbon price, using the latest IPCC assessment (AR6 WGIII, 2022) as the primary source, to report the percentage reduction at USD 100/tCO2e, and to derive the implied semi-elasticities under an iso-(semi-)elastic model. Sectors covered: cement/clinker/concrete; primary steel by BF-BOF and by natural-gas DRI-EAF (the Egyptian route); scrap-EAF steel; primary aluminium; ammonia; urea; nitric acid and ammonium nitrate; hydrogen. Electricity (a CBAM good) has no process emissions and is out of scope; iron-ore pellets/sinter, ferro-alloys and downstream iron/steel/aluminium articles are discussed briefly in Â§7.10. Fuel-combustion emissions and indirect (electricity) emissions are excluded throughout; demand-side measures (material efficiency, product substitution) are excluded because they change output, not emission intensity, and are handled elsewhere in CPAT through demand elasticities.

The same parameter set is applied to Egypt and non-Egypt (per instruction); Egypt-specific considerations are discussed qualitatively in Â§9.

## 2. What the IPCC actually provides (and does not)

IPCC AR6 WGIII does **not** publish price elasticities of process emissions. It provides two things from which a price response can be constructed:

1. **Chapter 12, Table 12.3** â€” global 2030 *economic mitigation potentials* for industry by option and cost bin (<0, 0â€“20, 20â€“50, 50â€“100, 100â€“200 USD2019/tCO2e), overlap-corrected within industry (Â±25 %), against a current-policies reference (SSP2/WEO-2019-CPS-like). Industry rows: energy efficiency 1.14 Gt (0â€“20); material efficiency 0.93 (20â€“50); circularity/enhanced recycling 0.48 (20â€“50); fuel switching 1.28/0.67/0.15 (20â€“50/50â€“100/100â€“200); feedstock decarbonisation & process change 0.38 (50â€“100); CCU/CCS 0.15 (100â€“200, range 0.08â€“0.36, not overlap-corrected); cementitious material substitution 0.28 (20â€“50); reduction of non-CO2 emissions 0.20 (0â€“20). Table 12.4: industry direct potential < USD 100 = 5.4 Gt (4.0â€“6.7). SPM C.12.1: options â‰¤ USD 100 could halve 2019 GHG by 2030, but Chapter 12 notes that industry is the one sector in which only energy efficiency is available below USD 20.
2. **Chapter 11, Table 11.3 and Â§11.4** â€” per-technology GHG-reduction percentages and cost ranges (USD2019/tCO2e) for steel, cement, aluminium, ammonia/hydrogen and cross-cutting CCS, with TRL and earliest availability. These are *technology costs*, not deployment-constrained potentials, and therefore describe the long-run response once capital stock turns over (Chapter 11 ES: "mitigation costs are high in the rough range of USD 50â€“150 tCO2-eq", "5 to 15 years of intensive innovation, commercialisation and policy").

For the two non-CO2 process gases relevant to CBAM goods (N2O from nitric acid; PFCs from aluminium) AR6 gives only qualitative statements (Ch.11 footnote 24; Â§11.4.1.4), so the quantitative cost-bin data are taken from **IPCC AR4 WGIII Chapter 7 (Table 7.9, Â§7.4.3.4, Â§7.4.2.1)**, cross-checked against NACAG (2024).

Consequently two horizons are reported: a **2030 / deployment-constrained** estimate (calibrated to Table 12.3 where the mapping is unambiguous) and a **long-run / technology-cost** estimate (Table 11.3). The central value is the mean.

## 3. Definitions and accounting conventions

- **Process emissions** follow IPCC inventory category 2 (IPPU): calcination CO2 in clinker and lime; reductant CO2 in iron-making (coke, coal, natural gas) and ferro-alloys; anode CO2 and PFCs in aluminium smelting; feedstock-derived CO2 in ammonia/hydrogen (shift reaction); N2O in nitric acid. Carbon inputs to EAFs (electrodes, charge carbon) and flux calcination are included.
- **CBAM accounting (Implementing Regulation (EU) 2023/1773; Commission Guidance 5c)** counts all direct emissions of the installation, with precursors' embedded emissions added. Two CBAM-specific points matter here: (a) CO2 chemically bound into **urea** is *not* deducted â€” "CO2 received from another installation as process input shall be considered an emission, if not already counted as emission of the installation where the CO2 was produced" â€” so the ammonia-stage process CO2 is embedded in urea and cannot be abated by CCS (it is the urea feedstock); (b) nitric-acid N2O must be reported "including unabated and abated emissions", so the CBAM charge creates a direct incentive to install de-N2O catalysts.
- **Carbon price Ï„** is in USD2019 per tCO2e, matching IPCC AR6 cost bins (no inflation correction is applied in AR6; USD 100 of 2019 â‰ˆ USD 122 of 2024 at US CPI, so a nominal 2024 price of USD 100 corresponds to â‰ˆ USD 82 on the IPCC scale â€” the workbook lets the user evaluate any Ï„).

## 4. Method: from MACC steps to a price response

For each sector, the process-emission MACC is represented by a small number of options *i*, each described by a cost range [c_low, c_high], a technical reduction *r_i* of the pool it addresses, the share *s_i* of the sector's process emissions in that pool, and a horizon-specific deployment (penetration) factor *d_i,h* for h âˆˆ {2030, LR}.

- Cost heterogeneity across plants is assumed uniform over [c_low, c_high], so the share of plants for which option *i* is in the money at price Ï„ is f_i(Ï„) = min(1, max(0, (Ï„ âˆ’ c_low)/(c_high âˆ’ c_low))). This smooths the step function implicit in a single-cost MACC and is the reason some options contribute fractionally at Ï„ = 100.
- Options are combined multiplicatively: a_h(Ï„) = 1 âˆ’ Î _i (1 âˆ’ r_iÂ·s_iÂ·d_i,hÂ·f_i(Ï„)). This is exact for sequential options on the same pool (e.g. CCS applied to the clinker remaining after substitution) and slightly conservative for disjoint pools (e.g. PFCs vs anode CO2).
- Costs and *r* come from the IPCC tables cited in each row; *s* from stoichiometry or published emission splits; **d_2030 and d_LR are analyst assumptions**, chosen so that the 2030 figures reproduce the relevant IPCC Table 12.3 potentials where a one-to-one mapping exists (cementitious substitution; CCUS absent below USD 100 in 2030; non-CO2 potential) and otherwise reflect capital-stock turnover (BF relining 15â€“25 yr; aluminium pot relining 5â€“7 yr; cement kiln life 30â€“50 yr; catalysts retrofittable within a year). All are visible and editable in the workbook.

## 5. Derivation of the iso-semi-elastic model and the implied semi-elasticities

Let E(Ï„) be process-emission intensity at carbon price Ï„, E0 = E(0), and a(Ï„) = 1 âˆ’ E(Ï„)/E0 the abatement fraction. Define the **semi-elasticity** Î²(Ï„) â‰¡ (dE/dÏ„)/E = d ln E/dÏ„: the proportional change in emissions per unit increase in the price.

**Iso-semi-elastic assumption.** Suppose Î² is constant in Ï„ (the log-linear analogue of a constant-elasticity model). Integrating d ln E = Î² dÏ„ from 0 to Ï„:

  ln E(Ï„) âˆ’ ln E0 = Î² Ï„  â‡’  **E(Ï„) = E0 Â· e^(Î²Ï„)**,  **a(Ï„) = 1 âˆ’ e^(Î²Ï„)**.

Calibrating on a single observed point (a* at Ï„* = 100):

  **Î² = ln(1 âˆ’ a*) / Ï„***  (per USD),  or **100Â·Î² % per USD**.

This is exactly the form used in the CPAT Egypt workbook, Î”I/I = exp(Î²Â·Ï„) âˆ’ 1 = âˆ’a(Ï„). Properties: (i) a(Ï„) â†’ 1 as Ï„ â†’ âˆž, so emissions never go negative; (ii) the *marginal* response at any price is Î²Â·E(Ï„), i.e. a constant percentage of *current* emissions; (iii) the linear approximation a(Ï„) â‰ˆ âˆ’Î²Ï„ gives Î²_lin = âˆ’a*/Ï„*, and |Î²_iso| â‰¥ |Î²_lin| always because âˆ’ln(1 âˆ’ a) â‰¥ a (e.g. a* = 0.50 â‡’ Î²_iso = âˆ’0.693 %/$ vs Î²_lin = âˆ’0.500 %/$). (iv) The *price elasticity* implied is Îµ(Ï„) = Î²Â·Ï„, which rises with the price; Îµ(100) = 100Î². A true isoelastic (constant-elasticity) form E = E0(Ï„/Ï„_ref)^(âˆ’Îµ) is undefined at Ï„ = 0 and cannot be anchored to a zero-price baseline, which is why the semi-elastic form is the appropriate "iso" model for carbon-price scenarios starting from zero.

**Consistency test across cost bins.** If the constant-Î² assumption were exact, Î²_k = ln(1 âˆ’ a(Ï„_k))/Ï„_k would be the same for every Ï„_k. Computing it at Ï„ = 20, 50, 100, 150, 200 (central horizon) gives:


| Sector | Î²(20) | Î²(50) | Î²(100) | Î²(150) | Î²(200) |
|---|---|---|---|---|---|
| Cement clinker / cement / concrete | -0.439 | -0.471 | -0.408 | -0.352 | -0.264 |
| Primary steel: BF-BOF route | 0 | -0.156 | -0.329 | -0.295 | -0.221 |
| Primary steel: natural-gas DRI-EAF route (Egypt-type) | 0 | -0.143 | -0.421 | -0.326 | -0.253 |
| Secondary steel: scrap-EAF | -0.353 | -0.141 | -0.200 | -0.219 | -0.164 |
| Primary aluminium (Hall-Heroult) | -0.570 | -0.269 | -0.244 | -0.244 | -0.183 |
| Ammonia (natural-gas SMR; merchant and non-urea uses) | -0.171 | -0.536 | -0.353 | -0.294 | -0.251 |
| Urea (ammonia precursor + urea plant) | -0.037 | -0.107 | -0.123 | -0.136 | -0.129 |
| Nitric acid (N2O) - component of ammonium nitrate and other N fertilisers | -8.410 | -3.364 | -1.682 | -1.121 | -0.841 |
| Ammonium nitrate - unabated N2O baseline | -5.597 | -2.474 | -1.277 | -0.877 | -0.671 |
| Ammonium nitrate - N2O already ~90% abated (EU / CDM-legacy plants) | -0.796 | -0.674 | -0.399 | -0.308 | -0.253 |
| Hydrogen (merchant, SMR) | -0.297 | -1.034 | -0.563 | -0.407 | -0.331 |

Reading: for nitric acid (very cheap catalysts) |Î²| is largest at low prices and falls â€” the MACC is concave and the exponential over-predicts additional abatement above USD 20; for cement, steel and aluminium |Î²| rises with the price because the decisive options (CCS, H2-DRI, inert anodes) only enter above USD 40â€“70 â€” the MACC is convex and a constant Î² calibrated at USD 100 *over*-predicts the response below â‰ˆ USD 50 (where little is actually in the money) and *under*-predicts it above USD 100. Calibrating at USD 100 is therefore the right anchor for policy scenarios in the USD 50â€“150 range; for scenarios below USD 30 the 2030 column is a safer guide. The workbook also offers a saturating alternative a(Ï„) = A(1 âˆ’ e^(âˆ’Ï„/Ï„_s)) with closed-form two-point calibration Ï„_s = âˆ’100/ln(a(200)/a(100) âˆ’ 1).

## 6. Aggregate IPCC benchmark

Process-related industry options in Table 12.3 costing â‰¤ USD 100 in 2030 sum to 0.86 GtCO2e (0.38 + 0.28 + 0.20); CCU/CCS (0.15 Gt) sits entirely in the 100â€“200 bin. Industrial process GHG were 4.5 Gt in 2019 (Ch.11 Â§11.2); the AR6 reference grows industry CO2 by â‰ˆ 28 % over 2017â€“2030 (Ch.12 SM), while IEA projections for cement and steel output are flatter, so a 2030 reference of 5.2â€“5.8 Gt is used. Result: a(100) = 14.9%â€“16.6% (central 15.7%, Î² â‰ˆ -0.171 %/$); adding enhanced recycling (0.48 Gt, a route-shift option that lowers sector-average intensity) gives 23.3%â€“25.9%. Caveats: "feedstock decarbonisation" includes chemical feedstocks beyond CBAM goods; the Â±25 % uncertainty applies; potentials are deployment-constrained 2030 values. The sector-specific 2030 estimates below (cement 19 %, steel 10â€“11 %, aluminium 7 %, ammonia 15 %, nitric acid 79 %) are consistent with this aggregate once weighted by emissions (cement â‰ˆ 1.5 Gt and steel â‰ˆ 2 Gt dominate; nitric-acid N2O is â‰ˆ 0.1â€“0.2 Gt).

## 7. Sector-by-sector evidence and results

Each table lists the options, the IPCC-sourced cost range and technical reduction, the applicable share, the two deployment factors, the in-the-money fraction at USD 100 and the resulting contribution x = rÂ·sÂ·dÂ·f(100). Sources are listed under each table.


### 7.1 Cement clinker / cement / concrete

*CBAM goods:* Cement, clinker, concrete products (CN 2523, 6810 etc.)  
*Process emissions:* Calcination CO2 from limestone (CaCO3 -> CaO + CO2): ~0.52 tCO2/t clinker; ~60% of a BAT plant's direct GHG (IPCC AR6 Ch.11 ES & Table 11.3). Fuel CO2 excluded.

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| Clinker substitution (SCMs: slag, fly ash, calcined clay/LC3, limestone filler) and blended cements | 0-50 | 0.30 | 1.00 | 0.55 | 0.85 | 1.00 | 16.5% | 25.5% |
| Novel binders / alternative chemistries (CSA, belite, alkali-activated) in niche applications | 50-150 | 0.50 | 0.20 | 0.10 | 0.50 | 0.50 | 0.5% | 2.5% |
| CO2 capture on calcination stream (indirect calcination/LEILAC, oxyfuel, post-combustion) + transport & storage | 50-130 | 0.90 | 1.00 | 0.05 | 0.50 | 0.62 | 2.8% | 28.1% |
| **Combined a(100)** |  |  |  |  |  |  | **19.3%** | **47.8%** |

Sources and parameter notes:
- *Clinker substitution (SCMs: slag, fly ash, calcined clay/LC3, limestone filler) and blended cements*: IPCC AR6 Table 11.3: clinker substitution 40-50% reduction of plant GHG at 'near-zero' cost; Table 12.3: cementitious substitution 0.28 Gt in USD20-50 bin (2030); Fig 11.13 FeedCI 20-50. r=0.30 from clinker ratio 0.71 (2019, Ch.11) -> technical floor ~0.50 (IEA G7 2022): 1-0.50/0.71. d2030=0.55 reproduces 0.28 Gt / ~1.65 Gt 2030 reference calcination CO2 (~17%).
- *Novel binders / alternative chemistries (CSA, belite, alkali-activated) in niche applications*: IPCC AR6 SPM C.5.2: 'until new chemistries are mastered'; Ch.11 11.4.1.2. Cost range analyst judgement; niche share s=0.2.
- *CO2 capture on calcination stream (indirect calcination/LEILAC, oxyfuel, post-combustion) + transport & storage*: IPCC AR6 Table 11.3: CCUS 99% of calcination CO2 at <=USD40 capture (TRL 5-7, 2025) + storage of concentrated CO2 USD10-40 (fn f) -> ~50-80 USD; diluted post-combustion 60-170 (Leeson 2017), most <120; Fig 11.13 cement CCUS 60-130; Rootzen & Johnsson 25-110 EUR; ETC 110-130. Table 12.3 puts 2030 industrial CCUS wholly in USD100-200 bin -> d2030 ~0. dLR=0.5 (storage access; Material Economics CCS share 29-79%, Table 11.5).

**Result:** a(100) = 19.3% (2030), 47.8% (long run), 33.5% (central); Î²_iso = -0.214 / -0.650 / -0.408 %/$; Î²_lin (central) = -0.335 %/$.

### 7.2 Primary steel: BF-BOF route

*CBAM goods:* Pig iron, crude steel, iron & steel products (Ch.72/73)  
*Process emissions:* CO2 from carbon reductant (coke/coal) and carbonate fluxes: ~1.8-2.0 of 2.3 tCO2/t crude steel (IPCC AR6 Ch.11 11.4.1.1). Under IPCC inventory rules reductant CO2 is IPPU 2C1 (process); under CBAM all direct emissions are counted.

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| Incremental: higher scrap charge in BOF, H2/biomass/plastics injection in BF, top-gas efficiency | 20-80 | 0.20 | 1.00 | 0.30 | 0.70 | 1.00 | 6.0% | 14.0% |
| BF-BOF with top-gas recycling + CCUS (retrofit, <=50-60% capture) | 70-130 | 0.60 | 1.00 | 0.03 | 0.40 | 0.50 | 0.9% | 12.0% |
| Route switch at relining: H2-DRI-EAF (or HIsarna+CCS, syngas DRI+CCS) | 40-120 | 0.95 | 1.00 | 0.05 | 0.40 | 0.75 | 3.6% | 28.5% |
| **Combined a(100)** |  |  |  |  |  |  | **10.2%** | **45.9%** |

Sources and parameter notes:
- *Incremental: higher scrap charge in BOF, H2/biomass/plastics injection in BF, top-gas efficiency*: IPCC AR6 Ch.11: H2 co-firing 30-40% max (coke needed for stack integrity); 15% energy-efficiency potential (Fig 11.8); bio-coal limited by biomass demand. Costs: Fig 11.13 steel EE <20, ME/circ 20-50, FeedCI 20-80.
- *BF-BOF with top-gas recycling + CCUS (retrofit, <=50-60% capture)*: IPCC AR6 Table 11.3: BF-BOF + TGR + CCUS 60% at USD70-130 (2025-30); Ch.11: hard to retrofit beyond 50% capture; Fig 11.13 steel CCUS 60-100. Table 12.3 2030 CCUS in 100-200 bin -> d2030 ~0.
- *Route switch at relining: H2-DRI-EAF (or HIsarna+CCS, syngas DRI+CCS)*: IPCC AR6 Table 11.3: H2-DRI-EAF up to 99% at USD39-79 (EUR40/MWh electricity); HIsarna+CCS 80-90% at USD40-70; syngas DRI-EAF+CCUS >=90% at >=USD40; ETC steel avg USD60; Material Economics new-process pathway EUR91. Upper bound 120 reflects higher electricity prices. SPM C.5.2: H2-DRI 'near-commercial'. Relining cycle 15-25 yrs -> dLR=0.4 at USD100.

**Result:** a(100) = 10.2% (2030), 45.9% (long run), 28.0% (central); Î²_iso = -0.107 / -0.614 / -0.329 %/$; Î²_lin (central) = -0.280 %/$.

### 7.3 Primary steel: natural-gas DRI-EAF route (Egypt-type)

*CBAM goods:* DRI (CN 7203), crude steel and products  
*Process emissions:* CO2 from natural-gas reductant in the shaft furnace (~0.5-0.7 tCO2/t DRI, partly separated in the top-gas CO2-removal unit) plus EAF carbon inputs and fluxes (~0.05-0.1 tCO2/t).

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| CO2 capture on DRI process gas (concentrated top-gas stream) + T&S (Al Reyadah/Emirates Steel type) | 40-90 | 0.85 | 0.85 | 0.10 | 0.60 | 1.00 | 7.2% | 43.3% |
| Hydrogen blending <=30% in existing DRI shaft (no process change) | 70-400 | 0.30 | 0.85 | 0.30 | 0.80 | 0.09 | 0.7% | 1.9% |
| Full conversion to H2-DRI (electrolytic hydrogen) | 40-120 | 0.95 | 0.85 | 0.05 | 0.35 | 0.75 | 3.0% | 21.2% |
| EAF: bio-based charge carbon/electrodes, lime from decarbonised kilns | 50-150 | 0.50 | 0.15 | 0.20 | 0.70 | 0.50 | 0.8% | 2.6% |
| **Combined a(100)** |  |  |  |  |  |  | **11.3%** | **57.3%** |

Sources and parameter notes:
- *CO2 capture on DRI process gas (concentrated top-gas stream) + T&S (Al Reyadah/Emirates Steel type)*: IPCC AR6 Table 11.3: syngas DRI-EAF + CCUS >=90% at >=USD40; Ch.11 11.4.1.1 Abu Dhabi DRI capture operating since 2016; concentrated-CO2 storage USD10-40 (fn f). s=0.85 = DRI share of route process emissions.
- *Hydrogen blending <=30% in existing DRI shaft (no process change)*: IPCC AR6 Ch.11: <=30% H2 substitutable without process change. Cost = H2 premium: at H2 USD1.0-3.0/kg vs gas USD5/MMBtu, abatement cost ~70-400 USD/tCO2 (own calc.: 1 kg H2 displaces 0.114 MMBtu gas = 6 kgCO2).
- *Full conversion to H2-DRI (electrolytic hydrogen)*: IPCC AR6 Table 11.3: H2-DRI-EAF up to 99% at USD39-79 (converted from EUR2018 34-68; EUR40/MWh). Brownfield DRI plants are the easiest conversion candidates.
- *EAF: bio-based charge carbon/electrodes, lime from decarbonised kilns*: Analyst judgement; see scrap-EAF row for sources.

**Result:** a(100) = 11.3% (2030), 57.3% (long run), 34.3% (central); Î²_iso = -0.120 / -0.852 / -0.421 %/$; Î²_lin (central) = -0.343 %/$.

### 7.4 Secondary steel: scrap-EAF

*CBAM goods:* Crude steel and products  
*Process emissions:* CO2 from graphite electrodes, charge/injection carbon and lime/dolomite fluxes: ~0.05-0.10 tCO2/t steel (IPCC AR6 Ch.11: EAF route 0.3 tCO2/t or less incl. gas burners; electricity excluded).

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| Operational optimisation (electrode consumption, carbon injection control, foamy-slag practice) | 0-20 | 0.15 | 0.70 | 0.50 | 0.80 | 1.00 | 5.2% | 8.4% |
| Bio-based charge carbon / biochar, bio-derived electrodes | 50-150 | 0.60 | 0.70 | 0.20 | 0.70 | 0.50 | 4.2% | 14.7% |
| Lime/dolime from kilns with CO2 capture (supply-chain measure) | 60-130 | 0.90 | 0.30 | 0.02 | 0.40 | 0.57 | 0.3% | 6.2% |
| **Combined a(100)** |  |  |  |  |  |  | **9.5%** | **26.7%** |

Sources and parameter notes:
- *Operational optimisation (electrode consumption, carbon injection control, foamy-slag practice)*: Low/no-cost measures; s=0.7 = share of EAF process CO2 from carbon inputs (remainder = flux calcination). Analyst judgement, consistent with IPCC Fig 11.13 steel EE <USD20.
- *Bio-based charge carbon / biochar, bio-derived electrodes*: IPCC AR6 Ch.11: bio-based fuels can substitute part of coal input but limited by biomass demand; cost range from biochar price premium (analyst calc.).
- *Lime/dolime from kilns with CO2 capture (supply-chain measure)*: Same cost basis as cement calcination capture (IPCC Table 11.3 / Fig 11.13).

**Result:** a(100) = 9.5% (2030), 26.7% (long run), 18.1% (central); Î²_iso = -0.100 / -0.310 / -0.200 %/$; Î²_lin (central) = -0.181 %/$.

### 7.5 Primary aluminium (Hall-Heroult)

*CBAM goods:* Unwrought aluminium and products (Ch.76)  
*Process emissions:* CO2 from consumption of carbon (prebaked) anodes ~1.5-1.6 tCO2/t Al (IPCC AR6 Table 11.3; AR4 Table 7.6: 1.55) plus PFCs (CF4, C2F6) from anode effects ~0.3-1.2 tCO2e/t (IPCC AR6: 'up to 2', 'almost eliminated in well-run facilities'; IAI: process emissions ~15% of sector total). Central split: anode CO2 72% / PFC 28%.

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| PFC control: anode-effect reduction (point feeders, process control, LV-PFC management) | 0-20 | 0.70 | 0.28 | 0.30 | 0.80 | 1.00 | 5.9% | 15.7% |
| Inert (non-carbon) anodes - eliminates anode CO2 and PFCs | 40-150 | 1.00 | 1.00 | 0.02 | 0.45 | 0.55 | 1.1% | 24.5% |
| **Combined a(100)** |  |  |  |  |  |  | **6.9%** | **36.4%** |

Sources and parameter notes:
- *PFC control: anode-effect reduction (point feeders, process control, LV-PFC management)*: IPCC AR4 Ch.7: PFC steps 'mainly low or no-cost'; intensity fell 4.4 -> 1.2 tCO2e/t 1990-2004; AR4 Table 7.9: 7.6 of 51 Mt (15%) of 2030 PFC baseline <USD20 (remaining potential concentrated in non-BAT smelters). r=0.7 for non-BAT smelters.
- *Inert (non-carbon) anodes - eliminates anode CO2 and PFCs*: IPCC AR6 Table 11.3 & fn h: inert electrodes 100% of process emissions at 'relatively low' cost, TRL 6-7, commercialisation target 2024 (ELYSIS); no USD/tCO2 figure given -> wide analyst range 40-150. Pot relining cycle ~5-7 yrs allows retrofit; dLR=0.45.

**Result:** a(100) = 6.9% (2030), 36.4% (long run), 21.6% (central); Î²_iso = -0.072 / -0.452 / -0.244 %/$; Î²_lin (central) = -0.216 %/$.

### 7.6 Ammonia (natural-gas SMR; merchant and non-urea uses)

*CBAM goods:* Ammonia (CN 2814)  
*Process emissions:* CO2 from the feedstock (shift) reaction, removed as a concentrated stream in the CO2-removal unit: ~1.2 of 1.6-1.8 tCO2/t NH3 for gas-based plants (IPCC AR6 Table 11.3: 1.6 t gas / 3.8 t coal). Fuel CO2 excluded.

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| CCS of already-separated process CO2 (compression + T&S) - plants not integrated with urea | 15-50 | 0.95 | 0.45 | 0.30 | 0.80 | 1.00 | 12.8% | 34.2% |
| Electrolytic (renewable) hydrogen feed - full replacement | 50-200 | 1.00 | 1.00 | 0.03 | 0.35 | 0.33 | 1.0% | 11.7% |
| Partial electrolysis (hybrid 10-20% H2) and feedstock-efficiency improvements | 50-150 | 0.15 | 1.00 | 0.20 | 0.60 | 0.50 | 1.5% | 4.5% |
| **Combined a(100)** |  |  |  |  |  |  | **15.0%** | **44.5%** |

Sources and parameter notes:
- *CCS of already-separated process CO2 (compression + T&S) - plants not integrated with urea*: IPCC AR6 Table 11.3 fn f: CCS of concentrated CO2 USD15-40 commercial; SMR+CCS 56% (process stream) at <=USD40. s=0.45: ~55% of global NH3 goes to urea (IEA Ammonia Roadmap 2021: 177 Mt urea x 0.57 t NH3/t = ~100 Mt of ~183 Mt NH3) and that CO2 is consumed, not storable.
- *Electrolytic (renewable) hydrogen feed - full replacement*: IPCC AR6 Table 11.3: low-GHG H2 <=99% 'at cost of H2'; electrolysis H2 ~USD50/t at low-cost renewables; IEA Ammonia Roadmap 2021: electrolysis competitive with CCS only at very low electricity prices -> upper bound 200.
- *Partial electrolysis (hybrid 10-20% H2) and feedstock-efficiency improvements*: Analyst judgement; same H2 cost basis.

**Result:** a(100) = 15.0% (2030), 44.5% (long run), 29.7% (central); Î²_iso = -0.162 / -0.589 / -0.353 %/$; Î²_lin (central) = -0.297 %/$.

### 7.7 Urea (ammonia precursor + urea plant)

*CBAM goods:* Urea (CN 3102 10)  
*Process emissions:* Embedded process CO2 = ammonia-stage process CO2 (0.57 t NH3/t urea x ~1.2 = ~0.7 tCO2/t). Under CBAM the CO2 bound into urea is NOT deducted: Implementing Regulation (EU) 2023/1773 Annex III / Commission Guidance 5c - CO2 received as process input is counted as an emission if not already counted upstream. Hence the process CO2 cannot be abated by CCS (it is the feedstock).

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| CCS of surplus process CO2 (plants with CO2 in excess of urea stoichiometry, ~10%) | 15-50 | 0.95 | 0.10 | 0.30 | 0.80 | 1.00 | 2.8% | 7.6% |
| Electrolytic H2 + alternative CO2 source (bio-CO2, captured fuel CO2, DAC) | 60-220 | 1.00 | 1.00 | 0.02 | 0.30 | 0.25 | 0.5% | 7.5% |
| Hybrid partial electrolysis / efficiency | 50-150 | 0.15 | 1.00 | 0.20 | 0.60 | 0.50 | 1.5% | 4.5% |
| **Combined a(100)** |  |  |  |  |  |  | **4.8%** | **18.4%** |

Sources and parameter notes:
- *CCS of surplus process CO2 (plants with CO2 in excess of urea stoichiometry, ~10%)*: Same cost basis as ammonia CCS; s=0.10 analyst estimate of surplus CO2.
- *Electrolytic H2 + alternative CO2 source (bio-CO2, captured fuel CO2, DAC)*: IPCC AR6 Table 11.3 (cost of H2) + Ch.11 p.1185: DAC-sourced CO2 feedstock very high cost today; bio-CO2 cheaper. Upper bound raised vs ammonia for CO2 sourcing.
- *Hybrid partial electrolysis / efficiency*: Analyst judgement.

**Result:** a(100) = 4.8% (2030), 18.4% (long run), 11.6% (central); Î²_iso = -0.049 / -0.203 / -0.123 %/$; Î²_lin (central) = -0.116 %/$.

### 7.8 Nitric acid (N2O) - component of ammonium nitrate and other N fertilisers

*CBAM goods:* Nitric acid (CN 2808), ammonium nitrate (CN 3102 30/40), mixed fertilisers  
*Process emissions:* N2O by-product of ammonia oxidation: unabated 5-9 kg N2O/t HNO3 (= 1.4-2.5 tCO2e/t HNO3 at GWP100=273, AR6). CBAM requires reporting of N2O 'including unabated and abated emissions' (Guidance 5c).

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| Secondary / tertiary N2O decomposition catalysts (de-N2O) | 2-10 | 0.88 | 1.00 | 0.90 | 0.95 | 1.00 | 79.2% | 83.6% |
| **Combined a(100)** |  |  |  |  |  |  | **79.2%** | **83.6%** |

Sources and parameter notes:
- *Secondary / tertiary N2O decomposition catalysts (de-N2O)*: IPCC AR4 WGIII Ch.7 7.4.3.4: costs USD2000 2.0-5.8/tCO2e (= ~USD2019 3-9), potential 70% to 'almost 100%', 89% typical; AR4 Table 7.9: 158 of 190 Mt (83%) of 2030 baseline <USD0 and 174 (92%) <USD100. NACAG FAQ 2024: secondary 70-90%, tertiary up to 99%; 'low-cost'. Quick retrofit -> d2030=0.9.

**Result:** a(100) = 79.2% (2030), 83.6% (long run), 81.4% (central); Î²_iso = -1.570 / -1.808 / -1.682 %/$; Î²_lin (central) = -0.814 %/$.

### 7.9 Hydrogen (merchant, SMR)

*CBAM goods:* Hydrogen (CN 2804 10)  
*Process emissions:* CO2 from feedstock (shift) reaction, concentrated stream ~55-60% of total SMR CO2 (~9-10 tCO2/t H2). Fuel CO2 excluded.

| Option | Cost USD2019/t | r | s | d2030 | dLR | f(100) | x2030(100) | xLR(100) |
|---|---|---|---|---|---|---|---|---|
| CCS of concentrated process CO2 stream (+ T&S) | 15-50 | 0.95 | 1.00 | 0.15 | 0.70 | 1.00 | 14.2% | 66.5% |
| Electrolysis (renewable) replacing SMR | 50-200 | 1.00 | 1.00 | 0.05 | 0.35 | 0.33 | 1.7% | 11.7% |
| **Combined a(100)** |  |  |  |  |  |  | **15.7%** | **70.4%** |

Sources and parameter notes:
- *CCS of concentrated process CO2 stream (+ T&S)*: IPCC AR6 Table 11.3: SMR + CCS 56% at <=USD40 (chem. stream), <=90% at <=USD120 incl. heat; fn f concentrated CO2 USD15-40. d2030=0.15 reflects IEA project pipeline.
- *Electrolysis (renewable) replacing SMR*: IPCC AR6 Table 11.3: electrolysis H2 ~USD50/t with low-cost renewables; wide range for electricity price.

**Result:** a(100) = 15.7% (2030), 70.4% (long run), 43.0% (central); Î²_iso = -0.171 / -1.218 / -0.563 %/$; Î²_lin (central) = -0.430 %/$.

### 7.9 Ammonium nitrate (composite of nitric acid and ammonia)

Per tonne of AN: â‰ˆ 0.60 t HNO3 and â‰ˆ 0.21 t NH3. With unabated nitric acid (7 kg N2O/t HNO3 Ã— 273) the N2O pool is â‰ˆ 1.15 tCO2e/t AN against â‰ˆ 0.25 tCO2 of ammonia-stage process CO2 â€” shares 82 %/18 %. Where N2O is already â‰ˆ 90 % abated (EU plants since 2013; CDM-legacy plants elsewhere) the residual N2O pool is â‰ˆ 0.115 tCO2e and the shares become 31 %/69 %, with only a secondary-to-tertiary upgrade (assumed r = 0.5 of the residual) left on the N2O side. Pools are disjoint, so abatement is additive.


| Case | a(100) 2030 | a(100) LR | a(100) central | Î² iso central (%/$) |
|---|---|---|---|---|
| Ammonium nitrate - unabated N2O baseline | 67.6% | 76.6% | 72.1% | -1.277 |
| Ammonium nitrate - N2O already ~90% abated (EU / CDM-legacy plants) | 21.2% | 44.6% | 32.9% | -0.399 |

The choice between the two AN rows is an **empirical question about the baseline plant**: a CBAM-exposed producer whose nitric-acid lines are unabated has by far the most price-responsive process emissions of any CBAM good (and the cheapest: USD 3â€“9/tCO2e), whereas an already-abated producer behaves essentially like an ammonia producer.

### 7.10 Other CBAM goods

- **Iron-ore pellets and sinter**: process CO2 only from carbonate fluxes/binders (small); treat with the scrap-EAF flux parameters. **Ferro-alloys**: reductant CO2 as in BF iron-making (AR4 Table 7.6: 1.6â€“4.9 tCO2/t); use BF-BOF parameters (bio-reductants are a somewhat cheaper option, which would raise the 2030 figure). **Downstream iron/steel and aluminium articles, mixed fertilisers**: embedded emissions are inherited from precursors; apply the precursor's Î² weighted by the precursor's share of embedded process emissions. **Electricity**: no process emissions.

## 8. Comparison with empirical (econometric) evidence and with the existing CPAT parameter

Ex-post studies of the EU ETS find total installation emissions 7â€“16 % below counterfactual at average allowance prices of roughly EUR 10â€“25 (Bayer & Aklin 2020: âˆ’8 to âˆ’12 % for covered sectors; DechezleprÃªtre et al. 2023: â‰ˆ âˆ’10 % 2005â€“12; Colmer et al. 2024: âˆ’14 %/âˆ’16 % in Phases I/II with marginal abatement cost "not exceeding USD 53/t"; DÃ¶bbeling-Hildebrandt et al. 2024 meta-analysis: âˆ’7.3 % for the EU ETS at a mean USD 20/t, âˆ’10.4 % across 21 schemes, bias-corrected âˆ’6.8 %). Mechanically these imply semi-elasticities of 0.3â€“1.0 % per EUR â€” several times the MACC-based values above. They are **not transferable to process emissions**: the estimates are for total emissions, dominated by combustion and fuel switching in power and heat, over a period when process-emission technologies (CCS, H2-DRI, inert anodes) were unavailable; the meta-analysis authors explicitly judge the price-elasticity evidence insufficient for a pooled estimate. The one process gas with observed ETS evidence is nitric-acid N2O, whose EU emissions fell by roughly an order of magnitude after inclusion in 2013 â€” consistent with the â‰ˆ 80â€“90 % figures derived here from AR4/NACAG.

The existing CPAT Egypt process semi-elasticity (Î² = âˆ’0.104 %/$, a(100) â‰ˆ 9.9%) is consistent with a 2030, cement-dominated reading of IPCC AR6 (aggregate 15â€“17 %; cement 19 %) and is conservative relative to the long-run technology-cost potentials. It materially understates the response of nitric-acid N2O (where a Î² of about âˆ’1.5 %/$ at prices up to USD 20 â€” effectively full abatement â€” is appropriate) and of ammonia/hydrogen process CO2 where CO2 storage is accessible.

## 9. Egypt versus non-Egypt

Per instruction the same parameters are used. Points that would differentiate Egypt if a country-specific calibration were attempted: (i) Egyptian primary steel is natural-gas DRI-EAF, for which the relevant row is 7.3 â€” the concentrated DRI top-gas CO2 is one of the cheapest industrial CCS opportunities and Egypt has depleted hydrocarbon reservoirs, but no CO2 transport/storage infrastructure exists today, which argues for the 2030 column in the near term; (ii) cement is the dominant process-emission source (â‰ˆ 28 of â‰ˆ 30 Mt in the CPAT CBAM base) and clinker substitution is the operative lever â€” Egypt's clinker ratio and SCM availability (limited slag/fly ash; abundant limestone and clay for LC3) determine whether the 30 % technical ceiling is reachable; (iii) nitric-acid N2O status at Egyptian AN plants should be verified (CDM-era de-N2O projects were registered in Egypt; if catalysts are in place and operating, use the "already abated" AN row); (iv) low-cost gas and the absence of a domestic carbon price mean that the price-induced response starts from a less abated baseline than in the EU, which raises the 2030 percentages for N2O and PFCs and leaves cement/steel/ammonia essentially unchanged.

## 10. Limitations

1. The IPCC provides engineering potentials and technology costs, not behavioural price responses; converting them to a price response requires the deployment assumptions in Â§4, which are the main source of uncertainty (Â±25 % on IPCC potentials; larger on d_LR).
2. Costs are USD2019 and partly pre-2020 study vintages; capture and electrolyser costs have moved in both directions since.
3. Potentials across sectors are "not necessarily additive" (SPM Fig. SPM.7 caption); the multiplicative combination is an approximation.
4. The constant-Î² form is a calibration device, not a structural result; its bin-consistency is shown in Â§5.
5. CBAM-specific rules (urea CO2, N2O reporting) are taken from the Commission's guidance because the EUR-Lex text was not machine-accessible during this exercise; the substantive provisions quoted are those of Annex III of Regulation (EU) 2023/1773.
6. No sector-specific econometric estimate of process-emission price elasticity exists in the literature reviewed.

## 11. Recommendation

For a medium-run CPAT-type simulation at carbon prices of USD 50â€“150: use the **central** Î² values in Â§0 by sector (cement -0.41, BF-BOF -0.33, NG-DRI-EAF -0.42, scrap-EAF -0.20, aluminium -0.24, ammonia -0.35, urea -0.12, nitric acid -1.68, ammonium nitrate -1.28 (unabated) / -0.40 (abated), hydrogen -0.56 %/$), with the 2030 column as the low case and the long-run column as the high case. If a single economy-wide process parameter is required, the emissions-weighted 2030 IPCC aggregate (Î² â‰ˆ -0.17 %/$, a(100) â‰ˆ 16%) is the defensible IPCC-anchored figure; the existing âˆ’0.104 %/$ is a conservative lower bound.

## References


- IPCC (2022) AR6 WGIII, Summary for Policymakers: C.5, C.5.2, C.12, C.12.1, Figure SPM.7.
- IPCC (2022) AR6 WGIII, Chapter 11 'Industry' (Bashmakov et al.): Executive Summary (p.1163), 11.2 (p.1170 emissions), 11.3.6 (CCS p.1185), 11.4.1.1-11.4.1.5, Table 11.3 (p.1197-1198), Table 11.5, Figure 11.13.
- IPCC (2022) AR6 WGIII, Chapter 12 'Cross-sectoral perspectives' (Babiker et al.): 12.2, Table 12.2 (p.1254), Table 12.3 (p.1255-1256), Table 12.4 (p.1257); Chapter 12 Supplementary Material (industry reference scenario note).
- IPCC (2007) AR4 WGIII, Chapter 7 'Industry' (Bernstein et al.): 7.4.2.1 (aluminium PFC), 7.4.3.4 (N2O nitric/adipic acid), Table 7.6, Table 7.9.
- NACAG / GIZ (2024) Nitric Acid Climate Action Group - FAQ (EN) and Factsheet, nitricacidaction.org.
- IEA (2020) Iron and Steel Technology Roadmap; IEA (2021) Ammonia Technology Roadmap (production volumes: urea 177 Mt, AN 49 Mt, 2019); IEA (2022) Achieving Net Zero Heavy Industry Sectors in G7 Members (clinker ratio floor ~0.5).
- International Aluminium Institute (2021) Aluminium Sector Greenhouse Gas Pathways to 2050 (process emissions ~15% of sector total); IAI PFC statistics (GWP basis).
- European Commission (2023) Implementing Regulation (EU) 2023/1773 (CBAM transitional period) and Guidance No. 5c - Sector-specific guidance document on fertilisers (urea CO2 and nitric-acid N2O provisions).
- Material Economics (2019) Industrial Transformation 2050 - as cited in IPCC AR6 Ch.11 (pathway costs EUR 12-91/t; CCS shares).
- Energy Transitions Commission (2018) Mission Possible - as cited in IPCC AR6 Ch.11 (steel USD60/t, cement USD110-130/t).
- Rootzen & Johnsson (2016); Leeson et al. (2017) - as cited in IPCC AR6 Ch.11.
- Bayer & Aklin (2020) PNAS 117(16): 8804-8812. doi:10.1073/pnas.1918128117.
- Dechezlepretre, Nachtigall & Venmans (2023) JEEM 118: 102758. doi:10.1016/j.jeem.2022.102758.
- Colmer, Martin, Muuls & Wagner (2024) Review of Economic Studies (forthcoming) 'Does pricing carbon mitigate climate change? Firm-level evidence from the EU ETS'.
- Dobbeling-Hildebrandt et al. (2024) Nature Communications 15: 4147. doi:10.1038/s41467-024-48512-w.
- CPAT Egypt workbook method note (this repository): TASK-2a_AdHocCalculations_Pseudocode_v0.1.md; InitialResultsAndIssues/Methodological Note.txt (existing process semi-elasticity -0.104 %/USD).

## Appendix A â€” IPCC AR6 WGIII Table 12.3, industry rows (GtCO2-eq, 2030)


| Option | <0 | 0â€“20 | 20â€“50 | 50â€“100 | 100â€“200 | Classification here |
|---|---|---|---|---|---|---|
| Energy efficiency (fuels only) |  | 1.14 |  |  |  | not process |
| Material efficiency |  |  | 0.93 |  |  | demand-side (not intensity) |
| Circularity (enhanced recycling) |  |  | 0.48 |  |  | route shift (partly process) |
| Fuel switching |  |  | 1.28 | 0.67 | 0.15 | not process |
| Feedstock decarbonisation, process change |  |  |  | 0.38 |  | process |
| CCU and CCS |  |  |  |  | 0.15 | process (and fuel) - 0.08-0.36 range; not overlap-corrected |
| Cementitious material substitution |  |  | 0.28 |  |  | process |
| Reduction of non-CO2 emissions |  | 0.2 |  |  |  | process (N2O, PFC, CH4) |

Notes (verbatim): "The numbers for the industry sector typically have an uncertainty of Â±25%, unless indicated differently. The numbers are corrected for overlap between the options, except for the 0.15 GtCO2 potential in the highest cost bin." "Energy efficiency â€” This only applies to more efficient use of fuels."

## Appendix B â€” IPCC AR4 WGIII Table 7.9 extract (MtCO2-eq, 2030)


| Source | 2030 baseline | <0 | <20 | <50 | <100 | share <0 | share <100 |
|---|---|---|---|---|---|---|---|
| N2O from adipic and nitric acid production | 190 | 158 | 158 | 158 | 174 | 83% | 92% |
| PFC from aluminium production | 51 | 1.6 | 7.6 | 8.2 | 8.2 | 3% | 16% |

## Appendix C â€” Workbook map

`Parameters` (inputs; f(Ï„), x_h(Ï„) per option) â†’ `Results` (a_h(Ï„), central, Î²_iso, Î²_lin, elasticity, bin-consistency) â†’ `SemiElasticity` (derivation and worked example) â†’ `IPCC_Aggregate` (benchmark) â†’ `IPCC_T12_3`, `IPCC_T11_3`, `AR4_T7_9`, `Econometric`, `Sources`. `CPAT_v0.8_Table` holds the drop-in parameter table of Appendix D.

## Appendix D â€” Drop-in parameter table for CPAT_Industry_Kernel_Egypt_v0.8.xlsx

The kernel's table `'Manual inputs'!D39:F47` ("Process Emissions Half Elasticities") has columns *Process | Half Elasticity | ER at $100 (%)*. Reverse-engineering the v0.8 values shows the convention **Half Elasticity = âˆ’ln(1 âˆ’ ER)/100** (positive, fraction per USD/tCO2e; e.g. ER = 0.10 â†’ 0.0010536). This is exactly this report's Î²_iso with the sign reversed and divided by 100. The recommended values are the *central* estimates (A5, A11); 2030 and long-run alternatives follow. Row labels match v0.8 `D40:D47`.

| Process | Half Elasticity | ER at $100 (%) | v0.8 Half Elasticity | v0.8 ER at $100 |
|---|---|---|---|---|
| DRI-EAF steel | 0.004206 | 34.3% | 0.001054 | 10.0% |
| Scrap-EAF steel | 0.001997 | 18.1% | 0.000202 | 2.0% |
| BF-BOF steel reference | 0.003289 | 28.0% | 0.000513 | 5.0% |
| Grey clinker dry-process | 0.004083 | 33.5% | 0.000834 | 8.0% |
| Ammonia net | 0.003530 | 29.7% | 0.001985 | 18.0% |
| Urea | 0.001231 | 11.6% | 0.000000 | 0.0% |
| AN | 0.012766 | 72.1% | 0.010498 | 65.0% |
| Primary aluminium | 0.002439 | 21.6% | 0.000834 | 8.0% |

*Alternatives (same format):*

| Process | Half Elast. 2030 | ER $100 2030 | Half Elast. LR | ER $100 LR |
|---|---|---|---|---|
| DRI-EAF steel | 0.001202 | 11.3% | 0.008518 | 57.3% |
| Scrap-EAF steel | 0.000999 | 9.5% | 0.003104 | 26.7% |
| BF-BOF steel reference | 0.001072 | 10.2% | 0.006141 | 45.9% |
| Grey clinker dry-process | 0.002139 | 19.3% | 0.006499 | 47.8% |
| Ammonia net | 0.001624 | 15.0% | 0.005886 | 44.5% |
| Urea | 0.000490 | 4.8% | 0.002030 | 18.4% |
| AN | 0.011283 | 67.6% | 0.014508 | 76.6% |
| Primary aluminium | 0.000716 | 6.9% | 0.004522 | 36.4% |

*Mapping notes:*

- **DRI-EAF steel** â€” Report 7.3. Scope includes NG-reductant CO2, which the kernel classifies as fp (priced with fuel flags); the kernel applies the same half elasticity to fuel and process ER (Mitigation_Industry rows 351 and 362), so the mismatch is immaterial.
- **Scrap-EAF steel** â€” Report 7.4 (electrode/charge carbon and flux CO2).
- **BF-BOF steel reference** â€” Report 7.2 (coke/limestone CO2; TGR+CCUS, H2-DRI switch, scrap share).
- **Grey clinker dry-process** â€” Report 7.1 (calcination CO2; clinker substitution, CCUS, alternative binders).
- **Ammonia net** â€” Report 7.6 (SMR feedstock CO2 = kernel fp; CCS of separated stream, electrolytic H2). Applies to merchant/non-urea NH3.
- **Urea** â€” Report 7.7 (embedded NH3-stage CO2 counted under CBAM; abatement only via surplus-CO2 CCS or electrolytic H2 + alternative CO2). Kernel v0.8 has 0 because own np is floored at 0; use this value only if the embedded-NH3 column (M35) is priced.
- **AN** â€” Report 7.9 composite, UNABATED nitric-acid N2O baseline - consistent with kernel S1.no = 0.97 tCO2e/t AN (K36). If Egyptian plants are already catalytically abated, use the 'AN abated' row instead: ER(100) = 32.9%.
- **Primary aluminium** â€” Report 7.5 (anode CO2 + PFC; PFC control, inert anodes).

Caveats specific to the kernel: (i) v0.8 applies the same half elasticity to fuel-combustion ER (`Mitigation_Industry` row 351) and to process ER (row 362); the values here are derived for process emissions only. (ii) The kernel's DRI-EAF and ammonia "process" rows carry near-zero `np` because reductant/feedstock CO2 is classified as `fp`; since the half elasticity is applied to both categories this does not change the result, but it does mean the ER acts on the fp column. (iii) Urea's own `np` is negative (CO2 credit) and floored at zero, so the urea row only matters if the embedded-NH3 CO2 (`M35`) is priced; otherwise retain 0. (iv) The AN row assumes an unabated N2O baseline, consistent with `K36` = 0.97 tCO2e/t; if Egyptian nitric-acid plants are already catalytically abated, both `K36` and the AN response should be revised together. (v) Costs are USD2019; USD100 (2019) â‰ˆ USD122 (2024).
