# Output elasticity of the CBAM goods: evidence and the values used (v0.2)

## What the parameter does

The kernel (`Manual inputs` rows 66–73) lowers output by Q = Q₀ × (1 + Δp)^ε, where Δp is the net carbon cost per tonne as a share of the product price. ε is therefore "how much less is made when the carbon cost is a given share of the price". It combines three things: how much buyers cut back when the price rises (demand elasticity), how much of the cost reaches the price (pass-through), and how easily buyers switch to imports or other exporters (trade exposure). The current −0.5 for every product is a placeholder.

## The first finding: only cement matters

At USD 20/t and the model's emission factors, the carbon cost is 15% of the price of cement clinker (USD 17 on USD 110) but 1–3% of the price of steel, fertiliser and aluminium. Of the 3.8 Mt output-channel cut in 1A, 3.6 Mt is cement. So the choice of ε for cement drives the result; the other seven products move the total by less than 0.3 Mt whatever ε is chosen. The output channel is about 10% of the 1A cut.

## Evidence (components, not a single published number)

Verification status: **checked** = the figure appeared in at least two independent search summaries of the source; **single** = one summary only; **not found** = no source located. The papers themselves could not be opened (the network policy blocks the publishers); the status refers to search summaries only.

| Component | Evidence | Status | Reading for the model |
|---|---|---|---|
| Cement, market demand | Aggregate elasticity −0.02 to −0.04 and a median industry-level elasticity of −0.10 (plant level −3.1) in the Miller et al. RAND cement papers; a further summary gave −0.16 for the median year; materials such as steel, asphalt and lumber are poor substitutes | checked (range); the −0.16 attribution not confirmed | Very inelastic at industry level |
| Cement, pass-through | EC / CE Delft–Oeko-Institut 2016 ex-post study: 20–40% in general | checked | Only part of the carbon cost reaches the price |
| Steel, pass-through | EC / CE Delft–Oeko 2016: 55–85% for iron and steel; wider ranges elsewhere (about 6% to above 100% by country and technology; NERA for Eurofer 46–200%) | checked | Central about 0.7 |
| Steel, market demand | −0.2 to −0.3 is quoted for derived demand in general; no specific study located | not found | Low confidence; immaterial (carbon cost 1–3% of price) |
| Manufacturing, general | US energy-cost pass-through 0.59 on average (elasticity 0.51), about 70% in the short to medium run (Ganapati, Shapiro, Walker 2020) | checked | Supports a central pass-through of 0.6–0.7 |
| Trade exposure | GTAP Armington elasticities (domestic against imports): chemicals 3.3, mineral products 2.9, ferrous metals 2.95, non-ferrous metals 4.2; import against import twice as large | single | Matters for goods that compete with imports |
| Fertiliser, market demand | Nitrogen demand and supply described as inelastic; no usable number | not found | Treat as inelastic; low weight |
| Observed output response | EU ETS firms cut CO₂ by 14–16% with no detectable fall in output or employment (Colmer, Martin, Muûls, Wagner 2025) | checked | Upper bound on real output responses at the observed prices |
| CPAT's own elasticities | Industry fuel elasticities (usage −0.3 to −0.7) are for fuel demand, not product demand | repository | Not transferable |

For a domestically sold, hard-to-substitute good such as cement: industry-level demand elasticity −0.02 to −0.16 × pass-through 0.2–0.4 gives about −0.005 to −0.06; allowing for some import and export competition lifts it to about −0.1, which is the value used.

## Recommendation

| Product | Current | Recommended central | Range | Basis |
|---|---|---|---|---|
| Grey clinker (cement) | −0.5 | **−0.10** | −0.03 to −0.30 | Industry demand −0.02 to −0.16, pass-through 0.2–0.4, small trade exposure (1.6% of output goes to the EU) |
| Steel (DRI-EAF, scrap-EAF, BF-BOF) | −0.5 | −0.40 | −0.2 to −1.0 | Pass-through 0.55–0.85, import competition (Armington about 3); no steel demand study located (Low) |
| Ammonia, urea, ammonium nitrate | −0.5 | −0.40 | −0.2 to −1.0 | Inelastic demand; large exports make producers price-takers |
| Primary aluminium | −0.5 | −0.50 (keep) | −0.3 to −1.5 | World-priced metal, 56% exported; no better evidence found |

Confidence: **Low–Medium** for every row. These are judgements built from sourced components, not published product-specific output elasticities. Only the cement row changes results noticeably.

## Effect on the final results (2030 emission cut, Mt; approximate)

Cement elasticity changed from −0.5, other products as recommended; the rest of the method unchanged (calculated outside the kernel from the stored product data; the kernel itself was not rerun).

| Cement ε | 1A | 2A | 2B | 3A | 3B | 3C |
|---|---|---|---|---|---|---|
| −0.5 (current) | −37.4 | −33.1 | −34.8 | −22.8 | −12.0 | −33.0 |
| −0.30 | −35.9 | −32.5 | −34.2 | −21.3 | −12.0 | −31.6 |
| **−0.10 (recommended)** | **−34.5** | **−31.9** | **−33.7** | **−19.9** | **−12.0** | **−30.1** |
| −0.03 | −34.0 | −31.7 | −33.5 | −19.4 | −12.0 | −29.6 |

A lower elasticity makes the cut smaller by about 3 Mt (8%) in 1A, 1A–2B ranking unchanged. 3B is unaffected because free allowances remove the output response. Revenue and deaths change very little; the CBAM intensity measures (N, O) do not use ε.

## Caveats on this note

- Verification was by search summaries only; the web egress blocked opening the papers (EC, RAND, AEA, OUP, GTAP and others). To close the check, allow these hosts in the environment's network settings or check the figures by hand. The GTAP values and the steel-demand range remain single-source / not found.
- No Egypt-specific output elasticity was found.
- Pass-through is not a separate input in the kernel; ε absorbs it. A cleaner design would split ε into demand elasticity × pass-through, with trade exposure by product.
- Applied in final set v1.6 (full recommended set). The kernel's `Manual inputs` F66:F68 text still says "pass-through about 0.5"; correct it at the next kernel rebuild.
