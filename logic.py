#!/usr/bin/env python3
import base64
import zlib
import hashlib
import codecs
import string

# -----------------------------
# Part 1: Hex -> ASCII -> ROT13 -> Base64 decode
# -----------------------------
part1_hex = "5a52454f4a4b663d"
p1_ascii = bytes.fromhex(part1_hex).decode("ascii")          # "ZREOJKf="
p1_rot13 = codecs.decode(p1_ascii, "rot_13")                 # "MERBWXs="
part1 = base64.b64decode(p1_rot13).decode("ascii")           # "0DAY{"

# -----------------------------
# Part 2: Reverse -> Base64 -> XOR("MATRIX")
# -----------------------------
part2_encoded = "=YBPmE3D"
p2_rev = part2_encoded[::-1]                                 # "D3EmPBY="
p2_bytes = base64.b64decode(p2_rev)                          # b'\x0fq&<\x16'

key = b"MATRIX"
part2 = bytes(b ^ key[i % len(key)] for i, b in enumerate(p2_bytes)).decode("ascii")  # "B0rn_"

# -----------------------------
# Part 3: Caesar(-7) -> Base64 -> Zlib decompress
# (Caesar shift only letters; keep other chars unchanged)
# -----------------------------
part3_encoded = "lQdyTFoWTAFyaFdOHH6CHa4="

def caesar_letters_only(s: str, shift: int) -> str:
    out = []
    for ch in s:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)

p3_shifted = caesar_letters_only(part3_encoded, -7)           # "eJwrMYhPMTYrtYwHAA6VAt4="
p3_b64 = base64.b64decode(p3_shifted)
part3 = zlib.decompress(p3_b64).decode("ascii")               # "t0_d36u9_"

# -----------------------------
# Part 4: brute-force MD5 for pattern R3[a-z0-9]1ty}
# -----------------------------
target_md5 = "a09135e6941fad5972f992337064bb32"
alphabet = string.ascii_lowercase + string.digits

part4 = None
for ch in alphabet:
    candidate = f"R3{ch}1ty}}"
    if hashlib.md5(candidate.encode()).hexdigest() == target_md5:
        part4 = candidate
        break

if part4 is None:
    raise RuntimeError("Part 4 not found")

# -----------------------------
# Combine
# -----------------------------
flag = part1 + part2 + part3 + part4
print("Part1:", part1)
print("Part2:", part2)
print("Part3:", part3)
print("Part4:", part4)
print("FLAG:", flag)
