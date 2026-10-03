"""md_to_docx.py - render a Markdown note of this folder to .docx (python-docx).

Minimal Markdown subset: #/##/### headings, paragraphs, '-' / 'n.' list items (with continuation lines),
pipe tables (header + separator + rows) and `code` spans. Arial 10 throughout, tables 'Table Grid'.
Usage:  python md_to_docx.py [note.md]   (run from egypt+mitigation/AdHocRebuild; default MethodologyNote_v0.1.md;
        output = same stem .docx)
"""
import re
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "MethodologyNote_v0.1.md"
DST = SRC.with_suffix(".docx")

doc = Document()
for s in doc.sections:
    s.left_margin = s.right_margin = Pt(54)
    s.top_margin = s.bottom_margin = Pt(54)
st = doc.styles["Normal"]
st.font.name = "Arial"
st.font.size = Pt(10)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
st.paragraph_format.space_after = Pt(4)
for name, size in (("Heading 1", 14), ("Heading 2", 12), ("Heading 3", 10.5)):
    h = doc.styles[name]
    h.font.name = "Arial"
    h.font.size = Pt(size)
    h.font.bold = True
    h.font.color.rgb = RGBColor(0, 0x60, 0x30)
    h.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def add_runs(par, text, size=None):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**"):
            r = par.add_run(part[2:-2])
            r.bold = True
        elif part.startswith("`"):
            r = par.add_run(part[1:-1])
            r.font.name = "Consolas"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
        else:
            r = par.add_run(part)
        if size:
            r.font.size = Pt(size)


def flush_table(rows):
    if not rows:
        return
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [c for c in cells if not all(re.fullmatch(r":?-{2,}:?", x or "---") for x in c)]
    ncol = max(len(c) for c in cells)
    t = doc.add_table(rows=len(cells), cols=ncol)
    t.style = "Table Grid"
    for i, row in enumerate(cells):
        for j in range(ncol):
            cell = t.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            add_runs(p, row[j] if j < len(row) else "", size=8)
            if i == 0:
                for r in p.runs:
                    r.bold = True
    doc.add_paragraph()


lines = SRC.read_text(encoding="utf-8").splitlines()
table, i = [], 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("|"):
        table.append(ln)
        i += 1
        continue
    flush_table(table)
    table = []
    if not ln.strip():
        i += 1
        continue
    m = re.match(r"^(#{1,3})\s+(.*)", ln)
    if m:
        doc.add_heading(m.group(2), level=len(m.group(1)))
        i += 1
        continue
    m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", ln)
    if m:
        indent, marker, text = m.groups()
        style = "List Number" if marker[0].isdigit() else "List Bullet"
        # continuation lines (indented, non-list, non-blank)
        j = i + 1
        while j < len(lines) and lines[j].strip() and lines[j].startswith("  ") and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[j]):
            text += " " + lines[j].strip()
            j += 1
        p = doc.add_paragraph(style=style)
        add_runs(p, text)
        i = j
        continue
    # plain paragraph: join following non-blank, non-special lines
    j = i + 1
    text = ln.strip()
    while j < len(lines) and lines[j].strip() and not lines[j].startswith(("|", "#")) and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[j]):
        text += " " + lines[j].strip()
        j += 1
    p = doc.add_paragraph()
    add_runs(p, text)
    i = j
flush_table(table)
doc.save(DST)
print("saved", DST)
