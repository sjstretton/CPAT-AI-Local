# Egypt carbon pricing and CBAM: version notes (final v1.6)

Change history for the final Egypt deliverables and the kernel. The methodology (`EGYPT_Methodology_v1.6`) describes the current method only and carries no history (repository rule, `NORMS.md` section 7). Task-level detail and caveats are in `CAVEATS.md`; the kernel's own log is on its `Settings` sheet.

## Final set v1.6 (2026-10-08)

- **Product-specific output elasticities.** `Manual inputs` E66:E73 change from the uniform −0.5 placeholder to cement −0.10, steel −0.40, ammonia / urea / ammonium nitrate −0.40, aluminium −0.50 (`OutputElasticity_Note_v0.1`). Only cement matters (carbon cost 15% of its price). 2030 emission cut (Mt), old to new: 1A −37.4 to −34.7; 2A −33.1 to −31.9; 2B −34.8 to −33.7; 3A −22.8 to −20.0; 3B unchanged −12.0; 3C −33.0 to −30.8. Deaths avoided, old to new: 1A 1,501 to 1,440; 2A 1,456 to 1,431; 2B 1,517 to 1,492; 3A 552 to 509; 3C 646 to 606. Revenue changes by less than USD 0.1bn. Obligations (row O) are unchanged.
- Rebuild v0.5 (per-product elasticities) and kernel v1.6 are the supporting models.

## Final set v1.5 (2026-10-08)

- **3B rebate decision applied everywhere.** The output-based rebate in 3B covers all covered industry (rebuild switch `ThetaOther` = 1; kernel `Manual inputs` E112 = 1), not only CBAM producers. Final Table 2, 3B: revenue 0.6 to 0.3 USD bn; emission cut −19.1 to −12.0 Mt (−3.2% to −2.0% of GHG); deaths avoided 491 to 330. No other scenario and no other column changes.
- **CBAM obligation naming made consistent.** Table 2 row O is the CBAM-product intensity change and does not depend on the EU price or the phase-in. The deduction-based memo obligation is reported on FULL (2030 phase-in, CBAM factor 0.485) with NOPHASE (no phase-in, factor 1) as the other memo, in the kernel, the rebuild and the documents. The former "Full implementation" label in the CBAM-calculation workbook meant CBF = 1, i.e. NOPHASE.
- **One workbook.** Kernel v1.5 sheet `Table2_Final` holds the final Table 2, the figures as printed in the documents, their differences (zero) and a live recomputation of row O. The separate `EGYPT_Table2_Final_CBAMcalc` workbook (hard-coded rows) is retired to the archive.
- **Methodology.** New section 4.7 (composition of the final results); the 3B rebate scope in the scenario table; the pre-T5 comparison column and bullets, the "earlier Egypt value" remark and kernel/rebuild version mentions removed from the methodology (moved here, below).
- **Rebuild v0.4 and kernel v1.5** are the supporting models; see `VersionNotes_AdHocRebuild.md` and the kernel `Settings` log.

## Earlier final sets

| Set | Date | Change |
|---|---|---|
| v1.5 | 2026-10-08 | 3B rebate to all covered industry; one CBAM convention; single confirmation workbook |
| v1.3 | 2026-10-07 | All documents aligned; methodology rebuilt from the author's edited version; obligations on intensity only |
| v1.2 | 2026-10-06 | Row O restated as CBAM-product intensity change (no domestic-price deduction) |
| v1.1 | 2026-10-05 | One scenario term throughout the results text; Table 2 workbook with live obligations |
| v1.0 | 2026-10-04 | First final release (carve-out Table 2; proofread) |

## Kernel

| Version | Content |
|---|---|
| v0.3 | CBAM block added (legacy rows 12198–12353 layout) |
| v0.4–v0.7 | Scenarios sheet and bundles (E); revenue rows fixed (A); four-way EF split (B); process emissions priced (C) |
| v0.8 | CBAM metrics (K) |
| v0.9 | Process semi-elasticity layout (D) |
| v0.10 | Output response (H) |
| v0.11 | CBAM obligations, deduction-based memo (L) |
| v0.12 | Stream 2 merged: energy CO₂ (F), output-based rebate (I), revenue fund (J) |
| v0.13 | IPPU replacement and fuel-CO₂ reconciliation (G) |
| v0.14 | Links to main CPAT and Table 2 composition (M) |
| v0.15 | Egypt EF v0.1 and IPCC process semi-elasticities adopted (T1, T5) |
| v0.16 | P* = 122 (USD 2024); EG3 1/κ approximation in the kernel composition; fuel-CO₂ reallocation; 3C fund fixed point |
| v0.17 | Sheet `CarveOut_Table2` (final Table 2, carve-out) |
| v1.0 | Final release (v0.17 relabelled); v1.1–v1.3 relabelled with the deliverable set |
| v1.4 | CBAM market data moved to `Manual inputs` (T3), no value changes |
| v1.5 | 3B rebate decision; sheet `Table2_Final` |
| v1.6 | Product-specific output elasticities (cement −0.10); fund fixed point and stored snapshots re-solved |

## Material moved out of the methodology

**Emission factors: pre-T5 kernel values (tCO₂e/t, own process emissions), kernel v0.13 against the Egypt EF v0.1 values now in the kernel.**

| Good | EF v0.1 (own) | Kernel v0.13 |
|---|---|---|
| DRI-EAF steel | 0.609 | 0.730 |
| Scrap-EAF steel | 0.089 | 0.155 |
| BF-BOF steel (reference) | 1.478 | 2.172 |
| Grey clinker | 0.851 | 0.814 |
| Ammonia | 1.975 | 1.851 |
| Urea | 0.112 | −0.621 |
| Ammonium nitrate | 0.112 | 1.082 |
| Primary aluminium | 2.521 | 2.506 |

Why they differ: urea follows the CBAM rule here, inventory netting in the kernel; the kernel folded 0.97 of HNO₃ N₂O into the own emissions of AN; DRI-EAF is rebuilt from a carbon balance because the kernel's EF-input columns S:V were inconsistent with its own H:I values; ammonia 35.2 GJ/t here against about 33 in the kernel; clinker and aluminium within 5% of the kernel.

**Output elasticity.** Before v1.6 the kernel used a uniform −0.5 placeholder for every product.

**Process semi-elasticities.** The earlier Egypt value, β = 0.00104 (a(100) ≈ 10%), is a conservative lower bound compared with the IPCC-based values now used (Appendix B).
