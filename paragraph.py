import os, re, sys
from collections import defaultdict
from os import path

# Regexes for processing.
name = re.compile("[a-z] +([A-Z][a-zA-Z]+)")
justname = re.compile("[A-Z][a-zA-Z]+")
punct = re.compile("[^-' a-zA-Z]+")
dash = re.compile("--")
possess = re.compile("'s")
endnote = re.compile("\[[ivxlcdm\d\s]+\]") # roman or arabic numeraled endnotes, as in Shelley's "Mathilda"
footnote = re.compile("^\[[ivxlcdm\d\s]+\]") # cooresponds to endnote

# novel should be an iterable text object.  Returns the
# processed text of novel as a string.
def process(novel):
    # List of paragraphs. Each paragraph is a list of string
    # lines, not newline-terminated.
    pars = list()

    # Accumulate paragraphs, filtering out extraneous lines.
    par = list()
    for line in novel:
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

    # Accumulate names by count of occurrences.
    pnames = defaultdict(int)
    for p in pars:
        text = ' '.join(p)
        for g in name.finditer(text):
            w = g.group(1)
            if len(w) > 2:
                pnames[w] += 1

    # Construct the set of names.
    propnames = {n for n in pnames if pnames[n] >= 2}
    propnames -= {
        "Lady",
        "Lord",
        "Madam",
        "Madame",
        "Miss",
        "Mr",
        "Mrs",
        "Sir",
        "The",
    }

    # Substitute names.
    def clean_names(line):
        matches = {str(m.group(0)) for m in justname.finditer(line)}
        for m in matches:
            if m in propnames:
                line = line.replace(m, "—")
        return line

    # Remove footnote links
    def remove_notes(line):
        matches = {str(m.group(0)) for m in footnote.finditer(line)}
        for m in matches:
            line = ""
        matches = {str(m.group(0)) for m in endnote.finditer(line)}
        for m in matches:
            line = line.replace(m, "")
        return line

    # Build up the paragraphs with the names cleaned.
    return "\n".join([
        ''.join([
            remove_notes(clean_names(l)) for l in p
        ])
        for p in pars
    ])

# Process all available novels.
prefix = "hacked"
for fn in os.listdir(prefix):
    with open(path.join(prefix, fn), "r", encoding="utf-8") as f_in:
        text = process(f_in)
        outname = fn if fn in ['austen-northanger-abbey.txt', 'austen-pride-and-prejudice.txt', 'shelley-frankenstein.txt', 'shelley-the-last-man.txt'] else ('addtl-'+fn)
        with open(outname, "w", encoding="utf-8") as f_out:
            f_out.write(text)
