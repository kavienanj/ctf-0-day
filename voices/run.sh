python3 - <<'PY'
import glob, re

tokens = {}
for f in sorted(glob.glob("Voices_in_my_Head/*.wav")):
    b = open(f, "rb").read()
    # printable runs length >= 7 (filters out most junk)
    runs = [r.decode("ascii", "ignore") for r in re.findall(rb"[ -~]{7,}", b)]
    # keep ones that look "token-like" (letters/digits, maybe mixed case)
    good = []
    for s in runs:
        if re.fullmatch(r"[A-Za-z0-9]{7,}", s):
            good.append(s)
    if good:
        tokens[f] = sorted(set(good))

for f, toks in tokens.items():
    print(f, "->", toks[:20])
PY
