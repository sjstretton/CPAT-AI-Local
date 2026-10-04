# Three optional kernel increments: what they would change and whether to build them (v0.1)

All three are modelling clean-ups, not errors in the final Table 2. Effects were estimated outside the kernel from the stored product data (2030).

## 1. Route the ammonia (and DRI) CCS response to the fuel/feedstock emissions (fp)

**Today.** The process response (`Manual inputs` rows 53–60, applied in `Mitigation_Industry` rows 762–769) acts on the non-fuel process emissions np and no only. Ammonia's process CO₂ comes from natural gas used as feedstock (fp = 1.26 t/t), so ammonia's np = 0 and it has no response; DRI's reductant gas (fp = 0.39 t/t) has none either, although the IPCC response (DRI 0.34, ammonia 0.30 at USD 100, 2019) is a CCS response on that CO₂.

**Design.** Add fp response columns beside the np/no ones (ERmax, P\*, ER\*, β) on `Manual inputs` rows 53–60 (ammonia 0.2974, DRI 0.3433, BF-BOF 0.2803 as in the TASK-D table), a switch (default OFF), and an fp term in `Mitigation_Industry` rows 762–769: `fp EF × ER_fp × (1 − exp(−β_fp × price))` priced at the process price where the process group is charged.

**Effect** (USD 20/t, scenarios that charge process emissions: 1A, 3A, 3B, 3C): emissions −0.31 Mt (DRI −0.17, ammonia −0.14), about 0.9% of the 1A cut; 2A and 2B unchanged.

**Recommendation.** Small. Build only if the fertiliser response is a topic for the readers; otherwise keep it as a documented limitation (final caveats B6). If built: switch default OFF with regression 0, then decide the default.

## 2. Block fuel-intensity channel in the kernel

**Today.** The kernel's block fuel emissions respond to the fund shadow price only (`Mitigation_Industry` rows 751–758: `fuel × (EXP(−β × shadow price) − 1)`, β from `Manual inputs` E40:E47), not to the carbon price. The final Table 2 does not use a kernel fuel response at all: it applies CPAT's own efficiency response i_f = (1 + r)^(1/3) − 1 (about −4.9%) to the block's baseline-intensity fuel (`CarveOut_Table2` rows 31 and 46).

**Why it is not needed.** Adding a carbon-price term to rows 751–758 would put a second fuel response into the block. The carve-out reads those rows and then applies i_f, so the response would be counted twice; avoiding that needs a change to the carve-out arithmetic as well. The final results would not change (they already carry the response), only the prototype composition in `Table2_Industry`, which is reference material.

**Recommendation.** Do not build. Keep as a documented limitation of the prototype composition: "block fuel intensity is fixed in the kernel; the final Table 2 uses CPAT's response". If a kernel-only prototype is ever wanted, add a switch (OFF in the carve-out) and a uniform b_f from CPAT run EG1 (b_f = s_int × ln(IND1/IND0)/τ = −0.0025 per USD/t) as in the rebuild.

## 3. Align the kernel's own composition (`Table2_Industry`, `Rebate_Industry`) with the 3B decision

**Today.** `Table2_Industry` (prototype composition) rebates the CBAM block only in 3B (K −17.4 Mt, P 1.0 USD bn, deaths 746). The final Table 2 and the rebuild rebate all covered industry (K −12.0 / −12.3 Mt). The sheet is labelled reference.

**Design.** In `Table2_Industry`, multiply the non-kernel industry response (row 64) by s_int when the bundle has θ > 0 and `Manual inputs` E112 = 1, and deduct the rebate on non-kernel covered fuel from revenue (rows 91–92); `Rebate_Industry` needs no change (it prices the block only).

**Effect.** 3B composition K about −17.4 → −12 Mt, bringing it level with the final Table 2 and the rebuild; other bundles unchanged.

**Recommendation.** Low value: the composition is not a deliverable. Cheaper alternative: label `Table2_Industry` section E "block-only 3B rebate; reference" in the next kernel rebuild (text only). Build only if the prototype composition is to be quoted.

## Summary

| Increment | Effect on final Table 2 | Build? |
|---|---|---|
| fp routing | about −0.3 Mt (1A, 3A–3C) | Optional; low priority |
| Block fuel-intensity channel | none (risk of double counting) | No; document |
| 3B alignment of the composition | none (reference sheet) | No; label the sheet |

None of the three has a builder: they change formulas inside the calculation block and could not be verified without Excel, and the effects do not justify unverified code. Say if you want the fp routing built (a switch, default OFF, regression 0) and I will draft it.
