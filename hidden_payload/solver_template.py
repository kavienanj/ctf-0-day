#!/usr/bin/env python3
import base64
import zlib
import hashlib
import string

# Part 1: Hex -> ROT13(reverse) -> Base64(decode)
part1_hex = "5a52454f4a4b663d"
# TODO: Decode to get: 0DAY{

# Part 2: Reverse -> Base64 -> XOR("MATRIX")  
part2_encoded = "=YBPmE3D"
# TODO: Decode to get: B0rn_

# Part 3: Caesar(-7) -> Base64 -> Zlib
part3_encoded = "lQdyTFoWTAFyaFdOHH6CHa4="
# TODO: Decode to get: t0_d36u9_

# Part 4: MD5 crack
target_md5 = "a09135e6941fad5972f992337064bb32"
# TODO: Brute force or lookup to get: R3a1ty}

# Combine all parts
flag = part1 + part2 + part3 + part4
print(f"FLAG: {flag}")
