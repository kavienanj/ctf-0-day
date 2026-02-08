import re

# Focus only on the 'run_some_where' crate and crypto data
INCLUDE_PATTERNS = [
    r"run_some_where",
    r"aes",
    r"cbc",
    r"flag",
    r"\{.*\}", # Potential flag format
]

# Specifically exclude the "drop_in_place" garbage (it's just memory management)
EXCLUDE_PATTERNS = [
    r"drop_in_place",
    r"GCC_except_table",
    r"anon\.",
    r"llvm\.",
]

def analyze_strings(input_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    results = []
    for line in lines:
        line = line.strip()
        # Keep if it matches an include pattern AND doesn't match an exclude pattern
        if any(re.search(p, line, re.I) for p in INCLUDE_PATTERNS):
            if not any(re.search(e, line) for e in EXCLUDE_PATTERNS):
                results.append(line)
        
        # Also keep high-entropy strings that aren't symbols (potential keys/flags)
        elif len(line) > 10 and not line.startswith("_ZN"):
            if re.match(r"^[a-zA-Z0-9_\-]+$", line):
                results.append(f"[!] POTENTIAL KEY/FLAG: {line}")

    return sorted(list(set(results)))

if __name__ == "__main__":
    analyze_strings("output.txt")