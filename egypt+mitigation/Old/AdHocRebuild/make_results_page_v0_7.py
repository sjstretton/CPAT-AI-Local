"""Tracked results page v0.7 (from v0.6): fixes ¶98 (3C 53%), standardises terminology,
and attributes every tracked change to Stephen Stretton."""
import re
import shutil
import zipfile

F = r"C:\Users\wb547395\Repos\CPAT-ai-local\Egypt Final results"
SRC = F + r"\Old\EgyptResultsInitial_UpdatedResults_v0.6_tracked.docx"
DST = F + r"\EgyptResultsInitial_UpdatedResults_v0.7_tracked.docx"
AUTHOR = "Stephen Stretton"
DATE = "2026-10-04T09:00:00Z"
nid = [50000]

RUN = re.compile(r'<w:r(?: [^>]*)?>(?:(?!</w:r>).)*?</w:r>', re.S)


def ins_run(rpr, text):
    nid[0] += 1
    return ('<w:ins w:id="%d" w:author="%s" w:date="%s"><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:ins>'
            % (nid[0], AUTHOR, DATE, rpr, text))


def del_run(rpr, text):
    nid[0] += 1
    return ('<w:del w:id="%d" w:author="%s" w:date="%s"><w:r>%s<w:delText xml:space="preserve">%s</w:delText></w:r></w:del>'
            % (nid[0], AUTHOR, DATE, rpr, text))


def plain_run(rpr, text):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, text) if text else ""


def state(x, pos):
    for tag in ("w:ins", "w:del"):
        o, c = x.rfind("<%s " % tag, 0, pos), x.rfind("</%s>" % tag, 0, pos)
        if o > c:
            return tag
    return None


def runs_from(x, start, span=400000):
    out = []
    for m in RUN.finditer(x, start, min(len(x), start + span)):
        r = m.group(0)
        if "<w:delText" in r:
            continue
        t = re.search(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', r)
        if not t:
            continue
        rpr = re.search(r'<w:rPr>.*?</w:rPr>', r, re.S)
        out.append(dict(s=m.start(), e=m.end(), text=t.group(1), rpr=rpr.group(0) if rpr else "",
                        st=state(x, m.start()), raw=r))
    return out


def tr(x, anchor, old, new, nth_anchor=0):
    """Tracked replace of `old` (may span several plain runs) in visible text after `anchor`."""
    rs = runs_from(x, 0, len(x))
    full = "".join(r["text"] for r in rs)
    a = full.find(anchor)
    assert a >= 0, anchor
    i = full.find(old, a)
    assert i >= 0, (anchor, old)
    j = i + len(old)
    pos, parts = 0, []
    for r in rs:
        rs_, re_ = pos, pos + len(r["text"])
        pos = re_
        if re_ <= i or rs_ >= j:
            continue
        parts.append((r, max(i, rs_) - rs_, min(j, re_) - rs_))
    for r, _, _ in parts:
        assert r["st"] is None, ("tracked run in span", old, r["text"])
    out_x = x
    for k, (r, lo, hi) in reversed(list(enumerate(parts))):
        t = r["text"]
        rep = plain_run(r["rpr"], t[:lo]) + del_run(r["rpr"], t[lo:hi])
        if k == len(parts) - 1 and new:
            rep += ins_run(parts[0][0]["rpr"], new)
        rep += plain_run(r["rpr"], t[hi:])
        out_x = out_x[:r["s"]] + rep + out_x[r["e"]:]
    return out_x


def tins(x, anchor, after_text, new):
    """Tracked insertion of `new` immediately after visible `after_text` (inside one plain run)."""
    rs = runs_from(x, 0, len(x))
    full = "".join(r["text"] for r in rs)
    a = full.find(anchor)
    assert a >= 0, anchor
    pos = 0
    for r in rs:
        pos += len(r["text"])
        if pos < a:
            continue
        if after_text in r["text"] and r["st"] is None:
            k = r["text"].index(after_text) + len(after_text)
            rep = plain_run(r["rpr"], r["text"][:k]) + ins_run(r["rpr"], new) + plain_run(r["rpr"], r["text"][k:])
            return x[:r["s"]] + rep + x[r["e"]:]
    raise AssertionError(after_text)


def edit_ins(x, old, new):
    """Edit text that is already inside one of our tracked insertions."""
    n = 0
    for m in list(re.finditer(r'(<w:t(?: [^>]*)?>)([^<]*)(</w:t>)', x))[::-1]:
        if old in m.group(2) and state(x, m.start()) == "w:ins":
            x = x[:m.start(2)] + m.group(2).replace(old, new) + x[m.end(2):]
            n += 1
    assert n, old
    return x


def main():
    z = zipfile.ZipFile(SRC)
    x = z.read("word/document.xml").decode("utf8")

    # Numbers / substance
    x = tr(x, "Third, ", "by 30%", "by 53%")
    x = tr(x, "Third, ", "undermines both revenue and CBAM relief",
           "raises less revenue and delivers the smallest CBAM relief")
    x = tr(x, "though", "forgoes revenue and health benefits",
           "raises less revenue and yields smaller health benefits than broad-based pricing")
    x = tins(x, "narrowest option at", "50 by 2034.",
             " As modeled, only about half of industrial energy-related CO\u2082 is priced, which is why coverage is 14% rather than about 21%.")

    # Terminology: "industrial abatement rebate"
    x = tr(x, "Table 2. Simulated outcomes", "rebate for industrial abatement", "industrial abatement rebate")
    x = tr(x, "Value returned to firms", "the rebate for industrial abatement (3C)", "the industrial abatement rebate (3C)")
    x = tr(x, "each cover", "a rebate for industrial abatement", "an industrial abatement rebate")
    x = tr(x, "Estimated emission reductions", "with abatement rebate (3C)", "with an industrial abatement rebate (3C)")
    x = edit_ins(x, "the abatement rebate (3C)", "the industrial abatement rebate (3C)")

    # Terminology: "CBAM-sector emission intensity"
    x = tr(x, "produce ", "industrial carbon intensity reductions", "CBAM-sector emission intensity reductions")
    x = tr(x, "Table 2. Simulated outcomes", "Emission intensity reduction, CBAM sectors",
           "CBAM-sector emission intensity reduction")
    x = tr(x, "Table 2. Simulated outcomes", "% of CBAM sector emissions", "% of CBAM-sector emissions")
    x = tr(x, "each cover", "of CBAM sector emissions", "of CBAM-sector emissions")

    # Terminology: "national GHG emissions"
    for n in range(3):
        x = tr(x, "national GHGs covered", "national GHGs covered", "national GHG emissions covered")
    x = tr(x, "matrix at", "of national GHG.", "of national GHG emissions.")
    x = tr(x, "narrowest option at", "of national GHG.", "of national GHG emissions.")
    x = tr(x, "The second family", "of national GHG.", "of national GHG emissions.")

    # En-dashes in numeric ranges (our own insertions)
    for a, b in (("USD6.2-6.3", "USD6.2\u20136.3"), ("8-15%", "8\u201315%"), ("13-14%", "13\u201314%")):
        x = edit_ins(x, a, b)

    # Attribute all tracked changes to Stephen Stretton
    x = x.replace('w:author="Copilot"', 'w:author="%s"' % AUTHOR)
    assert 'w:author="Copilot"' not in x

    tmp = DST + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for it in z.infolist():
            data = z.read(it.filename)
            if it.filename == "word/document.xml":
                data = x.encode("utf8")
            elif it.filename == "word/people.xml":
                p = data.decode("utf8")
                if AUTHOR not in p:
                    p = p.replace("</w15:people>", '<w15:person w15:author="%s"><w15:presenceInfo w15:providerId="None" w15:userId="%s"/></w15:person></w15:people>' % (AUTHOR, AUTHOR))
                data = p.encode("utf8")
            elif it.filename.endswith(".xml"):
                data = data.decode("utf8").replace('w:author="Copilot"', 'w:author="%s"' % AUTHOR).encode("utf8")
            zo.writestr(it, data)
    z.close()
    shutil.move(tmp, DST)
    print("saved", DST)


if __name__ == "__main__":
    main()
