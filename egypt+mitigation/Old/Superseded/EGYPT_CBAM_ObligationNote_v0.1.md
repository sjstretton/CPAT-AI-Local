---
title: "Note: How the change in CBAM obligations is calculated"
author: "Stephen Stretton"
---

The CBAM obligation is what Egyptian exporters of steel, cement, fertilisers and aluminium would pay at the EU border for the emissions embedded in their exports. Table 2 reports the change in this obligation per tonne exported in 2030, compared with a baseline without an Egyptian carbon price. The EU export mix and export volumes are held at base-year levels. The figure therefore captures only two things: the policy's effect on emission intensity, and the carbon price actually paid in Egypt.

**Obligation per tonne.** For each CBAM product $i$:

$$
\text{obl}_i = \max\!\Big(0,\; \text{CBF}\cdot P_{EU}\cdot EI_i \;-\; d_i\Big),
\qquad
d_i = \tau\cdot EI_i^{\,cov} - m_i
$$

where:

- $P_{EU}$ is the EU allowance price (USD 100/tCO$_2$);
- $\text{CBF}$ is the share of embedded emissions charged by the EU CBAM in the reporting year. It rises from 2.5% in 2026 to 48.5% in 2030 and 100% from 2034, as free allocation under the EU ETS is withdrawn;
- $EI_i$ is embedded emissions per tonne of product (fuel and process), after the policy;
- $d_i$ is the carbon price effectively paid in Egypt per tonne of product. It equals the domestic price $\tau$ (USD 20/tCO$_2$) times the priced emissions per tonne $EI_i^{\,cov}$, less any rebate $m_i$ returned to the producer per tonne of output. The EU CBAM allows this amount to be deducted.

**Reported change.** The change is weighted by base-year EU exports $X_i$:

$$
O \;=\; \frac{\sum_i X_i\,\text{obl}_i^{\,policy}}{\sum_i X_i\,\text{obl}_i^{\,base}} \;-\; 1
$$

**What drives the result.** For a product priced in full, with no rebate, the formula reduces to:

$$
1 + O \;\approx\; \frac{\text{CBF}\cdot P_{EU} - \tau}{\text{CBF}\cdot P_{EU}}\,\big(1 + N\big)
$$

where $N$ is the change in CBAM-sector emission intensity. Two effects lower the obligation:

- **Deduction effect:** the domestic price offsets a share $\tau/(\text{CBF}\cdot P_{EU})$ of the obligation;
- **Intensity effect:** lower emissions per tonne reduce the remaining obligation in proportion.

The size of the deduction effect depends on the convention for CBF:

| Convention | CBF | Share offset by USD 20 | 1A example ($N=-5.8\%$) |
|---|---|---|---|
| Full implementation (initial table) | 1 | 20/100 = 20% | $0.80 \times 0.942 - 1 \approx -25\%$ |
| 2030 phase-in (current final table) | 0.485 | 20/48.5 = 41% | $0.59 \times 0.942 - 1 \approx -44\%$ |

**Why the scenarios differ:**

- **2A and 2B:** the upstream price covers fuel emissions only (44% of embedded emissions), so the deduction is smaller.
- **3B:** the output-based rebate returns the carbon payment to producers ($m_i \approx \tau\cdot EI_i^{\,cov}$), so almost nothing can be deducted. The obligation falls only with intensity.
- **3C:** the abatement rebate cuts intensity most ($N = -23\%$). As in the initial table, the abatement fund is not netted off the deductible price.

**Results, 2030 (% change in CBAM obligation per tonne exported):**

| | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| Initial table (full implementation) | −26.1 | −13.9 | −13.9 | −26.1 | −7.6 | −30.4 |
| Updated, full implementation | −24.0 | −12.2 | −12.3 | −24.0 | −5.1 | −36.2 |
| Updated, 2030 phase-in (current Table 2) | −44.2 | −22.9 | −23.0 | −44.2 | −5.0 | −53.1 |
