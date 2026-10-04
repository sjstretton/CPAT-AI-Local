---
title: "Note: How the change in CBAM obligations is calculated (v1.6)"
author: "Stephen Stretton"
---

The CBAM obligation is what Egyptian exporters of steel, cement, fertilisers and aluminium would pay at the EU border for the emissions embedded in their exports. Table 2 reports the change in this obligation per tonne exported in 2030, relative to a baseline without an Egyptian carbon price. The EU export mix, export volumes and the EU carbon price are held fixed, so the figure reflects only the change in the emissions embedded in each tonne exported.

**Obligation per tonne.** For each CBAM product $i$:

$$
\text{obl}_i = \text{CBF}\cdot P_{EU}\cdot EI_i
$$

where:

- $P_{EU}$ is the EU allowance price;
- $\text{CBF}$ is the share of embedded emissions charged by the EU CBAM in the reporting year (48.5% in 2030);
- $EI_i$ is embedded emissions per tonne of product (fuel plus process).

**Reported change.** The change is weighted by base-year (2024) EU exports $X_i$:

$$
O \;=\; \frac{\sum_i X_i\,\text{obl}_i^{\,policy}}{\sum_i X_i\,\text{obl}_i^{\,base}} - 1
\;=\; \frac{\sum_i X_i\,EI_i^{\,policy}}{\sum_i X_i\,EI_i^{\,base}} - 1
$$

$P_{EU}$ and $\text{CBF}$ cancel, so the result does not depend on the EU price or the phase-in schedule.

**Policy intensity.** For each product:

$$
EI_i^{\,policy} = F_i^{\,0}\,(1+i_f) + \frac{1000\,\Delta F_i^{\,abate}}{Q_i} + \frac{1000\,(P_i + \Delta P_i)}{Q_i}
$$

where $F_i^{\,0}$ is baseline fuel emissions per tonne, $i_f$ is CPAT's fuel-intensity response, $\Delta F_i^{\,abate}$ is the additional fuel abatement funded in 3C, $P_i$ and $\Delta P_i$ are process emissions and their change (Mt), and $Q_i$ is output (kt).

**Treatment of the domestic carbon price.** No deduction for the carbon price paid in Egypt is applied. The headline therefore measures the change in exposure driven by lower emissions intensity, consistent across all scenarios and independent of the assumed EU price and phase-in path. Deduction-based variants are kept in the kernel workbook as memo items only, under one naming: FULL (2030 phase-in, CBAM factor 0.485) and NOPHASE (no phase-in, CBAM factor 1).

**Why the scenarios differ:**

- **1A, 3A, 3B:** fuel and process emissions are both priced, so intensity falls by about 5%.
- **2A, 2B:** the upstream price covers fuel only, so intensity falls by about 3%.
- **3C:** the abatement rebate funds extra fuel abatement, so intensity falls by about 21%.

**Results, 2030 (% change in CBAM obligation per tonne exported):**

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Initial table | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| Updated (Table 2) | −5.4 | −2.6 | −2.7 | −5.4 | −5.4 | −20.7 |

The calculation is live in the kernel workbook `CPAT_Industry_Kernel_Egypt_v1.6.xlsx`, sheet `Table2_Final`, section E (the deduction-based memo is section D).
