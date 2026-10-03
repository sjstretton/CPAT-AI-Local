"""Build EgyptResultsInitial_UpdatedResults_v0.4_tracked.docx from v0.3: final prototype (kernel v0.16) values, 2030.

Tracked changes stay relative to the original EgyptResultsInitial text. O uses the NOPHASE convention (as Table 2).
"""
import re
import shutil
import zipfile

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\Egypt Final results"
SRC = F + r"\Old\EgyptResultsInitial_UpdatedResults_v0.3_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v0.4_tracked.docx"
DATE = "2026-10-03T13:00:00Z"
CO2 = "MtCO\u2082"

# index of existing w:ins (in v0.3) -> new text
INS = {
    # Table 2: 1A, 2A, 2B, 3A, 3B, 3C
    0: "63%", 1: "6.9", 2: "-29.0", 3: "-3.6%", 4: "-22.3%", 5: "1,421",
    6: "57%", 7: "6.3", 8: "-25.5", 9: "0.0%", 10: "-10.5%",
    11: "6.2", 12: "-26.7", 13: "0.0%", 14: "-10.5%",
    15: "19%", 16: "1.9", 17: "-21.1", 18: "-3.6%", 19: "-22.3%", 20: "816",
    21: "1.0", 22: "-17.4", 23: "-3.6%", 24: "-2.9%", 25: "746",
    26: "-32.9", 27: "-21.1%", 28: "-34.6%", 29: "985",
    # narrative
    30: "63%", 31: "57%", 32: "19%",
    33: "USD6.9 billion\u2014roughly 12%", 34: "USD6.2-6.3", 35: "USD1.9", 36: "less",
    37: "raises USD1.0 billion and", 38: "USD0.7 billion, as both",
    39: "17.4 to 32.9", 40: "7-13%", 41: "29.0 " + CO2 + " (about 12%", 42: "10-11%",
    43: "26.7", 44: "25.5", 45: " generally reduce",
    46: " a narrower industrial base; the exception is the abatement rebate (3C), whose rebate-funded "
        "process abatement gives it the largest reduction of all bundles",
    47: "32.9 " + CO2 + " (about 13%", 48: "21.1 " + CO2 + " (about 8%", 49: "17.4", 50: "7",
    51: "3", 52: "35", 53: "about ", 54: "4%", 55: "22%", 56: "3%",
    57: "0% (the model holds their fuel intensity fixed)", 58: "11%", 59: " 21", 60: " 35",
    61: "746 to 1,473", 62: "a health gain of 1,421", 63: "yield similar gains:", 64: "deaths, the largest,",
    65: "985", 66: "816", 67: "746",
    68: "29.0", 69: "USD6.9", 70: "large air pollution co-benefits (1,421", 71: "22%",
}

nid = [40000]


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


def in_tracked(x, pos):
    for tag in ("w:ins", "w:del"):
        o, c = x.rfind("<%s " % tag, 0, pos), x.rfind("</%s>" % tag, 0, pos)
        if o > c:
            return True
    return False


def tracked(x, old, new, after=0, exact=False):
    """Tracked replace of `old` in the first plain (untracked) run containing it, searching from `after`."""
    pat = re.compile(r'<w:t(?: [^>]*)?>(%s)</w:t>' % (re.escape(old) if exact else r'[^<]*' + re.escape(old) + r'[^<]*'))
    for m in pat.finditer(x, after):
        if not in_tracked(x, m.start()):
            break
    else:
        raise AssertionError(old)
    wt = m.group(1)
    rs = max(x.rfind("<w:r>", 0, m.start()), x.rfind("<w:r ", 0, m.start()))
    re_ = x.find("</w:r>", m.end()) + len("</w:r>")
    run = x[rs:re_]
    assert run.count("<w:t") == 1, run
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', run, re.S)
    rpr = rpr.group(0) if rpr else ""
    i = wt.index(old)
    out = plain_run(rpr, wt[:i]) + del_run(rpr, old) + (ins_run(rpr, new) if new else "") + plain_run(rpr, wt[i + len(old):])
    return x[:rs] + out + x[re_:], rs + len(out)


def main():
    x = zipfile.ZipFile(SRC).read("word/document.xml").decode("utf8")
    spans = [m.span(1) for m in re.finditer(r'<w:ins [^>]*>(.*?)</w:ins>', x, re.S)]
    assert len(spans) == 72, len(spans)
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

    # Table 2 cells unchanged in v0.3 (2A/2B deaths, 3C revenue)
    p = x.find("Table 2. Simulated outcomes")
    x, _ = tracked(x, "1,564", "1,421", p, exact=True)
    x, _ = tracked(x, "1,631", "1,473", p, exact=True)
    x, _ = tracked(x, "0.0", "0.7", p, exact=True)
    # narrative: rankings that change with the prototype values
    x, _ = tracked(x, "largest reduction", "largest reduction among the economy-wide levies", exact=True)
    x, _ = tracked(x, "nearly ", "", x.find("household-recycling variant (2B) and"), exact=True)
    p = x.find("yield similar gains:")
    x, p = tracked(x, "1,631", "1,473", p)
    x, p = tracked(x, "1,564", "1,421", p, exact=True)
    x, _ = tracked(x, "the largest emissions reductions", "large emissions reductions")

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
