"""EGYPT_Methodology_v1.6.docx from v1.5: product-specific output elasticity (OutputElasticity_Note_v0.2). Current method only."""
import os

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.abspath(os.path.join(HERE, "..", "..", "final"))
d = docx.Document(os.path.join(F, "..", "archive", "EGYPT_Methodology_v1.5.docx"))


def replace_in(p, old, new):
    runs = p.runs
    full = "".join(r.text for r in runs)
    i = full.find(old)
    if i < 0:
        return False
    pos, first = 0, True
    for r in runs:
        t = r.text
        a, b = max(i, pos), min(i + len(old), pos + len(t))
        if a < b:
            r.text = (t[:a - pos] + new + t[b - pos:]) if first else (t[:a - pos] + t[b - pos:])
            first = False
        pos += len(t)
    return True


def set_cell(cell, text):
    p = cell.paragraphs[0]
    rs = p.runs
    rs[0].text = text
    for r in rs[1:]:
        r._element.getparent().remove(r._element)


for p in [Paragraph(x, d) for x in d.element.body.iter(qn("w:p"))]:
    if p.text.startswith("4.3 Output response") and "(placeholder)" in p.text:
        assert replace_in(p, "ε_Q = −0.5 (placeholder)",
                          "ε_Q by product: cement −0.10, steel and fertilisers −0.40, aluminium −0.50 (Section 5)")
        break
else:
    raise AssertionError("4.3 not found")
for old, new in (("This is the proportional IPPU row that this method removes.",
                  "For the CBAM block this proportional response is removed and replaced by the block calculation (Section 4); for non-block IPPU CPAT's response is kept."),
                 ("(the scenario's own scenario, 2030)", "(the scenario's own CPAT run, 2030)")):
    for p in [Paragraph(x, d) for x in d.element.body.iter(qn("w:p"))]:
        if old in p.text:
            assert replace_in(p, old, new)
            break
    else:
        raise AssertionError(old[:40])
for t in d.tables:
    for r in t.rows:
        if r.cells[0].text.strip() == "CPAT's IPPU row":
            set_cell(r.cells[2], "removed for the CBAM block; kept for non-block IPPU")
done = False
for t in d.tables:
    for r in t.rows:
        if r.cells[0].text.strip() == "ε_Q (output)":
            set_cell(r.cells[1], "Cement −0.10; steel, fertilisers −0.40; aluminium −0.50")
            set_cell(r.cells[2], "Product demand × pass-through × trade exposure. Cement demand −0.02 to −0.16 with pass-through 0.2–0.4 "
                                 "(EC / CE Delft–Oeko 2016); steel pass-through 0.55–0.85 (no steel demand study located); Armington elasticities about 3–4 "
                                 "(GTAP); EU ETS firm studies find no detectable fall in output (Colmer et al. 2025). Only cement matters at "
                                 "USD 20/t: its carbon cost is 15% of its price, against 1–3% for the other goods.")
            set_cell(r.cells[3], "Low–Medium")
            done = True
assert done, "parameter row not found"
d.save(os.path.join(F, "EGYPT_Methodology_v1.6.docx"))
print("saved EGYPT_Methodology_v1.6.docx")
