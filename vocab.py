import sys

def alphas(w):
    return ''.join([c for c in w if c.lower() >= 'a' and c.lower() <= 'z'])

allwords = set()
for fname in sys.argv[1:]:
    with open(fname, "r") as f:
        text = f.read()
        words = text.split()
        justwords = {alphas(w) for w in words}
        allwords |= justwords

print(len(allwords))
print(list(allwords)[:10])
