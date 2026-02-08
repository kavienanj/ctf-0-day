import re

# We target the common prefixes for mangled Rust symbols and system noise
NOISE_PATTERNS = [
    r"^_ZN3std",    # Standard library symbols
    r"^_ZN4core",   # Core library symbols
    r"^_ZN5alloc",  # Allocator symbols
    r"^_ZN.*h[0-9a-f]{16}E", # Generic Rust mangled symbols with hashes
    r"^type..",      # Rust type metadata
    r"^vtable..",    # Dynamic dispatch tables
    r"^GCC_",        # Compiler noise
    r"^GLIBC_",      # System C library noise
]

def is_interesting(s):
    s = s.strip()
    
    # 1. Length check: Too short or absurdly long (usually junk)
    if len(s) < 5 or len(s) > 300:
        return False

    # 2. Filter out the mangled noise patterns
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, s):
            return False

    # 3. Explicitly keep potential flags (adjust prefix as needed)
    # Common CTF flag formats or suspicious patterns
    if re.search(r'[a-zA-Z0-9]{3,}\{.*\}', s):
        return True

    # 4. Keep things that look like human-written code paths
    if ".rs" in s or "src/" in s:
        return True

    # 5. Filter out low-entropy "garbage"
    # If a string has no vowels or is 80% digits/symbols, it's likely memory junk
    vowels = set("aeiouAEIOU")
    if not any(char in vowels for char in s):
        # Flags sometimes don't have vowels, so don't discard if it looks like a flag
        if "{" not in s: 
            return False

    return True

def clean_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
            lines = infile.readlines()
        
        # Deduplicate using a set
        unique_lines = set(l.strip() for l in lines)
        
        # Apply filter
        cleaned_lines = [l for l in unique_lines if is_interesting(l)]
        
        # Sort for easier reading (usually puts paths and flags in groups)
        cleaned_lines.sort()

        with open(output_path, 'w') as outfile:
            outfile.write("\n".join(cleaned_lines))

        print(f"Original lines: {len(lines)}")
        print(f"Cleaned lines:  {len(cleaned_lines)}")
        print(f"Check '{output_path}' for the results.")

    except FileNotFoundError:
        print(f"Error: {input_path} not found.")

if __name__ == "__main__":
    clean_file("output.txt", "cleaned_output.txt")
