import re, sys
from collections import defaultdict

name = re.compile("[a-z] +([A-Z][a-zA-Z]+)")
punct = re.compile("[^-' a-zA-Z]+")
dash = re.compile("--")
possess = re.compile("'s\>")

pars = list()
par = list()
for line in sys.stdin:
    words = line.split()
    if not words or words[0] in {
            "CHAPTER",
            "VOL.",
            "VOLUME",
            "Letter",
            "Chapter",
    }:
        if par and len(par) > 1:
            pars.append(par)
        par = list()
        continue
    par.append(line)
if par and len(par) > 1:
    pars.append(par)

pnames = defaultdict(int)

for p in pars:
    text = ' '.join(p)
    for g in name.finditer(text):
        pnames[g.group(1)] += 1

propnames = {n for n in pnames if pnames[n] >= 2}

propnames -= {
    "Sir",
    "Miss",
    "Mr",
    "Mrs",
    "Madam",
    "Madame",
    "Lord",
    "Lady",
}

def clean_words(line):
    global sentenced, mistered, propnames
    # print(line, end="")
    line = dash.sub(" ", line)
    line = punct.sub(" ", line)
    # line = possess.sub("", line)
    # print(line)
    # print()
    cleaned = line.split()
    for i in range(len(cleaned)):
        w = cleaned[i]
        if w in propnames:
            cleaned[i] = "—"
    return " ".join(cleaned) + "\n"

print("\n\n".join([
    ''.join([
        clean_words(l) for l in p
    ])
    for p in pars
]))
