import re, sys
from collections import defaultdict

lead_punct = re.compile("^[^a-zA-Z]+")
trail_punct = re.compile("[^a-zA-Z]+$")
body = re.compile("^[a-z][a-zA-Z]*[-']?[a-zA-Z]+$")
name = re.compile("[A-Z][a-zA-Z]+")

sentenced = True
mistered = False
propnames = defaultdict(int)

def clean_words(line):
    global sentenced, mistered, propnames
    cleaned = list()
    for w in line.split():
        w0 = lead_punct.sub("", w)
        w0 = trail_punct.sub("", w0)
        m = w0 in ("Mr", "Mrs", "Dr", "Prof")
        if body.match(w0) or m:
            cleaned.append(w)
            sentenced = w[-1] in '.!?"'
            mistered = m
            continue
        m = name.match(w0)
        if m:
            if sentenced and not mistered:
                w0 = w
            else:
                w0 = name.sub("—", w)
                # print(w, m.group())
                propnames[m.group()] += 1
            cleaned.append(w0)
            sentenced = w[-1] in '.!?"'
            mistered = False
            continue
    return " ".join(cleaned)

for pname in ["Sir", "Miss", "Madam", "Madame", "Lady"]:
    if pname in propnames:
        del propnames[pname]

pars = list()
par = list()
for line in sys.stdin:
    words = line.split()
    if not words or words[0] in {"CHAPTER", "VOL.", "VOLUME", "Letter", "Chapter"}:
        if par and len(par) > 1:
            pars.append(par)
        par = list()
        continue
    if not par and not sentenced:
        sentenced = True
    par.append(clean_words(line))

if par and len(par) > 1:
    pars.append(par)

for n in propnames:
    if propnames[n] > 3:
        pars = [[l.replace(n, "—") for l in p] for p in pars]

print("\n\n".join(["\n".join(p) for p in pars]))
