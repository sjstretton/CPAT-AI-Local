"""EGYPT_Methodology_v1.5.docx from the author's v1.3 master (python-docx, untracked edits):
  * 3B rebate decision: scenario table wording, new section 4.7 (composition of the final Table 2, carve-out);
  * CBAM obligation naming (FULL = 2030 phase-in, NOPHASE = no phase-in) and the live-calculation pointer;
  * version/history clutter removed (NORMS section 7): the pre-T5 comparison column and bullets, kernel/rebuild version
    mentions, the "earlier Egypt value" remark. That history is in EGYPT_VersionNotes.
"""
import copy
import os

import docx
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.abspath(os.path.join(HERE, "..", "..", "final"))
SRC = os.path.join(F, "..", "archive", "EGYPT_Methodology_v1.3.docx")
DST = os.path.join(F, "EGYPT_Methodology_v1.5.docx")
d = docx.Document(SRC)


def paras():
    return [Paragraph(p, d) for p in d.element.body.iter(qn("w:p"))]


def replace_in(p, old, new):
    runs = p.runs
    full = "".join(r.text for r in runs)
    i = full.find(old)
    if i < 0:
        return False
    pos = 0
    first = True
    for r in runs:
        t = r.text
        a, b = max(i, pos), min(i + len(old), pos + len(t))
        if a < b:
            if first:
                r.text = t[:a - pos] + new + t[b - pos:]
                first = False
            else:
                r.text = t[:a - pos] + t[b - pos:]
        pos += len(t)
    return True


def sub(old, new, startswith=None, count=1):
    n = 0
    for p in paras():
        if startswith and not p.text.startswith(startswith):
            continue
        if old in p.text and replace_in(p, old, new):
            n += 1
            if n == count:
                break
    assert n >= 1, ("not found", old[:60])


def delete(startswith):
    for p in paras():
        if p.text.startswith(startswith):
            p._element.getparent().remove(p._element)
            return
    raise AssertionError(("not found", startswith))


def new_para_after(anchor, template, lead, text):
    el = copy.deepcopy(template._element)
    anchor._element.addnext(el)
    p = Paragraph(el, anchor._parent)
    rs = p.runs
    rs[0].text = lead
    if len(rs) > 1:
        rs[1].text = text
        for r in rs[2:]:
            r._element.getparent().remove(r._element)
    else:
        rs[0].text = lead + text
    return p


# --- 3B rebate decision: scenario table
sub("as 3A + free allocation", "as 3A + free allocation for all covered industry", startswith="as 3A + free allocation")
sub("Returned to CBAM producers per unit of output", "Returned to all covered industry per unit of output",
    startswith="Returned to CBAM producers")

# --- obligation naming and pointers
sub("The calculation is live in EGYPT_Table2_Final_CBAMcalc_v1.3.xlsx.",
    "The calculation is live in the kernel workbook, sheet Table2_Final, section E.", startswith="CBAM obligation (Table 2")
sub("are set by the NOPHASE / FULL / SCALED selector.",
    "are set by the selector FULL (2030 phase-in, CBAM factor 0.485; the default), NOPHASE (no phase-in, factor 1) or SCALED "
    "(phase-in applied to the obligation and to the deduction).", startswith="Kernel memo (Task L)")

# --- 4.7: composition of the final Table 2
ps = paras()
head = next(p for p in ps if p.text.startswith("4.6 Channels kept separate"))
tpl_head = next(p for p in ps if p.text.startswith("4.5 Emissions, revenue"))
tpl_bul = next(p for p in ps if p.text.startswith("Revenue. rev_i"))
# the 4.6 section ends with a table; the new section goes after that table, before "5. Parameters"
h5 = next(p for p in ps if p.text.startswith("5. Parameters and their basis"))
items = [
    ("4.7 Table 2: composition of the final results (CBAM carve-out).", None, None),
    (None, "Principle. ", "Every Table 2 result is the original CPAT run except the CBAM block. CPAT's implied change in the block, "
     "r × B, is removed and replaced by the block calculation of 4.1–4.5. Runs: 1A and 2A = EG1, 2B = EG2, 3A–3C = EG3, as run "
     "(EG3 prices 54% of industrial energy CO₂, κ = 0.537; no scaling to full coverage)."),
    (None, "Emission cut. ", "K = ΔGHG(run) − r × B + dB. r is the CPAT industry energy CO₂ change of the run; B is the block's "
     "baseline fuel plus process emissions, growth-matched to CPAT sector energy CO₂; dB is the block output response, the process "
     "abatement (where charged) and CPAT's fuel-intensity response i_f = (1 + r)^(s_int) − 1 applied to block fuel (3A–3C use the EG1 "
     "value: same USD 20/t, block fully priced). CPAT's proportional IPPU row is kept for non-block IPPU."),
    (None, "3B rebate scope. ", "The output-based rebate covers all covered industry. In non-block industry the output share of "
     "CPAT's response, NB = ΔInd + ΔIPPU − r × B, is removed: K changes by −(1 − s_int) × NB (+7.2 Mt for EG3), the fuel part "
     "of that term enters the deaths adjustment, and the rebate τ × (κ × IND1 − block post-policy fuel CO₂) (USD 0.33bn) is "
     "deducted from revenue. There is no feedback onto CPAT receipts. Switch: kernel Manual inputs E112 (1 = all covered industry, "
     "0 = CBAM block only)."),
    (None, "Other columns. ", "Revenue P = CPAT receipts of the run + τ × block fuel adjustment + block process fees − rebates − "
     "fund. Deaths Q = CPAT deaths × (ΔEnergy CO₂ + block fuel adjustment (+ 3B term)) / ΔEnergy CO₂. Coverage J = energy CO₂ in "
     "scope (EG3: κ × industry) + block process emissions where charged. N, M and T are block metrics; O is as in 4.5."),
    (None, "Confirmation. ", "Kernel sheet CarveOut_Table2 computes the above for the active scenario; sheet Table2_Final holds the "
     "six scenarios, the figures printed in the final documents and their differences (all zero), and recomputes row O live."),
]
# insert before the heading of section 5: add after the element preceding h5
prev = h5._element.getprevious()
anchor = Paragraph(prev, h5._parent) if prev.tag == qn("w:p") else None
if anchor is None:                      # preceded by a table: use a temporary paragraph after it
    tmp = copy.deepcopy(tpl_head._element)
    prev.addnext(tmp)
    anchor = Paragraph(tmp, h5._parent)
    anchor.runs[0].text = "4.7 Table 2: composition of the final results (CBAM carve-out)."
    items = items[1:]
for lead, a, b in items:
    if lead:
        anchor = new_para_after(anchor, tpl_head, lead, "")
    else:
        anchor = new_para_after(anchor, tpl_bul, a, b)

# --- history clutter out
sub("Appendix B; loaded in kernel v0.16 and rebuild v0.3 (", "Appendix B; loaded in the kernel and the rebuild (")
sub("In kernel v0.9+ this is generalised", "In the kernel this is generalised")
sub("Kernel v0.9+ uses ER(P)", "The kernel uses ER(P)")
sub("Kernel v0.15 uses these", "The kernel uses these", startswith="Kernel v0.15 uses")
sub(" The last column shows the pre-T5 kernel values.", "", startswith="The kernel uses these")
for s in ("Why the results differ from the pre-T5 kernel", "Urea: CBAM rule here, inventory netting", "AN: the kernel folds 0.97",
          "DRI-EAF: rebuilt from a carbon balance", "Ammonia: 35.2 GJ/t here versus about 33", "Clinker and aluminium: within 5%",
          "The earlier Egypt value, β = 0.00104"):
    delete(s)
# last column of the EF table ("Kernel v0.13 (before T5)")
for t in d.tables:
    if t.rows[0].cells[-1].text.startswith("Kernel v0.13"):
        n = len(t.columns)
        grid = t._tbl.tblGrid
        grid.remove(grid.findall(qn("w:gridCol"))[-1])
        for row in t.rows:
            tc = row._tr.findall(qn("w:tc"))[-1]
            row._tr.remove(tc)
        break
else:
    raise AssertionError("EF table not found")
d.save(DST)
print("saved", DST)
