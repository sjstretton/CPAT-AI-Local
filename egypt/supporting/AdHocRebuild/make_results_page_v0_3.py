"""Build EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx from v0.2 (rebuild v0.3 values, 2030)."""
import re
import shutil
import zipfile

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\egypt\final"
SRC = F + r"\EgyptResultsInitial_UpdatedResults_v0.2_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx"
DATE = "2026-10-03T12:00:00Z"

# index of existing w:ins -> new text (None = unchanged)
INS = {
    2: "-31.4", 3: "-5.8%", 4: "-24.3%",
    15: "21%", 16: "2.3", 17: "-25.1", 18: "-5.8%", 19: "-24.3%",
    20: "1.1", 21: "-19.6", 22: "-5.8%", 23: "-5.4%", 24: "714",
    25: "-30.6", 26: "-11.2%", 27: "-28.4%", 28: "997",
    31: "21%", 34: "USD2.3", 35: "less", 36: "raises USD1.1 billion and",
    38: "19.6 to 31.4", 39: "8-13%", 40: "31.4 MtCO\u2082 (about 13%",
    44: "30.6 MtCO\u2082 (about 12%", 45: "25.1 MtCO\u2082 (about 10%", 46: "19.6",
    47: "5", 48: "6%", 49: "24%", 50: "5%", 53: "714 to 1,631", 57: "997", 58: "714",
    59: "31.4", 62: "24%",
}

nid = [30000]


def ins_run(rpr, text):
    nid[0] += 1
    return ('<w:ins w:id="%d" w:author="Copilot" w:date="%s"><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:ins>'
            % (nid[0], DATE, rpr, text))


def del_run(rpr, text):
    nid[0] += 1
    return ('<w:del w:id="%d" w:author="Copilot" w:date="%s"><w:r>%s<w:delText xml:space="preserve">%s</w:delText></w:r></w:del>'
            % (nid[0], DATE, rpr, text))


def plain_run(rpr, text):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, text) if text else ""


def tracked(x, wt_text, old, new, after=0):
    """Tracked replace of `old` inside the first top-level run whose w:t equals wt_text, searching from `after`."""
    m = re.compile(r'<w:t(?: [^>]*)?>%s</w:t>' % re.escape(wt_text)).search(x, after)
    assert m, wt_text
    rs = x.rfind("<w:r>", 0, m.start())
    rs2 = x.rfind("<w:r ", 0, m.start())
    rs = max(rs, rs2)
    re_ = x.find("</w:r>", m.end()) + len("</w:r>")
    run = x[rs:re_]
    assert run.count("<w:t") == 1, run
    assert "<w:ins " not in x[x.rfind("<w:", 0, rs - 1):rs] or True
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', run, re.S)
    rpr = rpr.group(0) if rpr else ""
    i = wt_text.index(old)
    pre, post = wt_text[:i], wt_text[i + len(old):]
    out = plain_run(rpr, pre)
    if old:
        out += del_run(rpr, old)
    out += ins_run(rpr, new) + plain_run(rpr, post)
    return x[:rs] + out + x[re_:], rs + len(out)


def main():
    z = zipfile.ZipFile(SRC)
    x = z.read("word/document.xml").decode("utf8")
    spans = [m.span(1) for m in re.finditer(r'<w:ins [^>]*>(.*?)</w:ins>', x, re.S)]
    for k in sorted(INS, reverse=True):
        a, b = spans[k]
        seg = x[a:b]
        ts = list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', seg))
        new = seg[:ts[0].start()] + '<w:t xml:space="preserve">' + INS[k] + "</w:t>"
        last = ts[0].end()
        for t in ts[1:]:
            new += seg[last:t.start()] + t.group(1) + t.group(3)
            last = t.end()
        new += seg[last:]
        x = x[:a] + new + x[b:]

    x, _ = tracked(x, "546", "546", "850")
    x, _ = tracked(x, "546, and the free-allocation design (3B) ", "546", "850")
    x, _ = tracked(x, " MtCO\u2082 (about 5", "5", "8")
    x, _ = tracked(x, " reduce emissions less because they cover", " reduce", " generally reduce")
    x, _ = tracked(x, " a narrower industrial base", " a narrower industrial base",
                   " a narrower industrial base; the exception is the abatement rebate (3C), whose rebate-funded "
                   "process abatement brings it close to the economy-wide levies")
    p = x.find("performs best")
    x, p = tracked(x, " 13", " 13", " 11", p)
    x, p = tracked(x, " 30", " 30", " 28", p)
    p = x.find("eductions in CBAM obligations rang")
    x, p = tracked(x, " to 30", "30", "28", p)
    x, p = tracked(x, "nearly ", "nearly ", "about ", p)

    shutil.copy2(SRC, DST)
    zin = zipfile.ZipFile(SRC)
    tmp = DST + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "word/document.xml":
                data = x.encode("utf8")
            zo.writestr(it, data)
    zin.close()
    shutil.move(tmp, DST)
    print("saved", DST)


if __name__ == "__main__":
    main()
