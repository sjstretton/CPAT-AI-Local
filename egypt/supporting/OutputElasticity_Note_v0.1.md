# Output elasticity of the CBAM goods: evidence and a recommended replacement for the uniform −0.5

## What the parameter does

The kernel (`Manual inputs` rows 66–73) lowers output by Q = Q₀ × (1 + Δp)^ε, where Δp is the net carbon cost per tonne as a share of the product price. ε is therefore "how much less is made when the carbon cost is a given share of the price". It combines three things: how much buyers cut back when the price rises (demand elasticity), how much of the cost reaches the price (pass-through), and how easily buyers switch to imports or other exporters (trade exposure). The current −0.5 for every product is a placeholder.

## The first finding: only cement matters

At USD 20/t and the model's emission factors, the carbon cost is 15% of the price of cement clinker (USD 17 on USD 110) but 1–3% of the price of steel, fertiliser and aluminium. Of the 3.8 Mt output-channel cut in 1A, 3.6 Mt is cement. So the choice of ε for cement drives the result; the other seven products move the total by less than 0.3 Mt whatever ε is chosen. The output channel is about 10% of the 1A cut.

## Evidence (components, not a single published number)

| Component | Evidence found | Reading for the model |
|---|---|---|
| Cement, market demand | Aggregate demand elasticity about −0.02 to −0.16 (cement studies of the Miller–Osborne type): materials such as steel, asphalt and lumber are poor substitutes for cement | Very inelastic |
| Cement, pass-through | EC / CE Delft–Oeko-Institut review: 20–40% typical, with a range of 0–100% by country | Only part of the carbon cost reaches the price |
| Steel, market demand | −0.2 to −0.3 (derived demand, inelastic) | Inelastic |
| Steel, pass-through | Very wide: from about 6% to above 100% by country and technology (NERA for Eurofer: 46–200% depending on emission factor) | Central about 50–60% |
| Manufacturing, general | US energy-cost pass-through 0.59 on average, 70% in the short to medium run (Ganapati, Shapiro, Walker 2020) | Supports a central pass-through near 0.6 |
| Trade exposure | GTAP Armington elasticities (domestic against imports): chemicals 3.3, mineral products 2.9, ferrous metals 2.95, non-ferrous metals 4.2; import against import twice as large | Traded goods respond strongly when the cost is passed on, so the answer depends on the traded share |
| Fertiliser, market demand | Nitrogen demand and supply described as inelastic; no usable number retrieved | Treat as inelastic; low weight |
| Observed output response to carbon prices | EU ETS firms cut CO₂ by 14–16% with no detectable fall in output or employment (Colmer, Martin, Muûls, Wagner 2025) | Upper bound: real output responses to a USD 20 price are small |
| CPAT's own elasticities | CPAT's industry fuel elasticities (usage −0.3 to −0.7) are for fuel demand, not product demand | Not transferable |

For a domestically sold, hard-to-substitute good such as cement: demand elasticity −0.16 × pass-through 0.2–0.4 gives about −0.03 to −0.06; allowing for some import and export competition lifts it to about −0.1.

## Recommendation

| Product | Current | Recommended central | Range | Basis |
|---|---|---|---|---|
| Grey clinker (cement) | −0.5 | **−0.10** | −0.03 to −0.30 | Demand −0.02 to −0.16, pass-through 0.2–0.4, small trade exposure (1.6% of output goes to the EU) |
| Steel (DRI-EAF, scrap-EAF, BF-BOF) | −0.5 | −0.40 | −0.2 to −1.0 | Demand −0.2 to −0.3, pass-through about 0.5, import competition (Armington about 3) |
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

- The numbers above come from web search summaries; the web egress here blocked opening the papers, so I could not confirm which study gives each cement and steel figure, nor read the GTAP and Ganapati tables directly. Check the citations before using them in a publication.
- No Egypt-specific output elasticity was found.
- Pass-through is not a separate input in the kernel; ε absorbs it. A cleaner design would split ε into demand elasticity × pass-through, with trade exposure by product.
- Nothing in the kernel or the final documents has been changed. Applying −0.10 for cement would need a kernel rebuild (`Manual inputs` rows 66–73), new carve-out numbers and updates to all documents.
