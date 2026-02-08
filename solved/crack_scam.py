import base64

def solve():
    # --- Configuration ---
    input_file = "encoded.js"
    output_file = "decoded_artifact.js"
    
    # 1. Setup the Alphabets
    # Standard Base64: A-Z, a-z, 0-9, +, /, =
    STANDARD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    # Custom is just the reverse of Standard
    CUSTOM = STANDARD[::-1]
    
    print(f"[*] Reading {input_file}...")
    try:
        with open(input_file, 'r') as f:
            # The file likely contains just the raw string, but we strip whitespace just in case
            encoded_data = f.read().strip()
    except FileNotFoundError:
        print(f"[!] Error: {input_file} not found. Did you download it?")
        return

    # 2. Reverse the Custom Alphabet (Substitution Cipher)
    print("[*] Reversing Custom Base64 map...")
    # Create a translation table: map CUSTOM chars -> STANDARD chars
    trans_table = str.maketrans(CUSTOM, STANDARD)
    # Translate the data
    standard_b64 = encoded_data.translate(trans_table)

    # 3. Base64 Decode
    print("[*] Decoding Base64...")
    try:
        decoded_bytes = base64.b64decode(standard_b64)
    except Exception as e:
        print(f"[!] Base64 Decode Failed: {e}")
        # Sometimes padding is off, but python usually handles it or we can pad manually
        return

    # 4. Rolling XOR Decryption
    print("[*] Decrypting XOR layer (Seed: 1377)...")
    # Logic from JS: const XOR_BASE = 1377 % 256; // equals 97
    XOR_BASE = 97
    
    final_bytes = bytearray()
    
    for i in range(len(decoded_bytes)):
        # JS: const roll = (XOR_BASE + (i % 255)) % 256;
        roll = (XOR_BASE + (i % 255)) % 256
        
        # JS: resultBytes[i] = xored[i] ^ roll;
        val = decoded_bytes[i] ^ roll
        final_bytes.append(val)

    # 5. Save the Result
    print(f"[*] Success! Writing output to {output_file}...")
    try:
        # Convert bytes to string (UTF-8)
        decrypted_text = final_bytes.decode('utf-8')
        
        with open(output_file, 'w') as f:
            f.write(decrypted_text)
            
        print("\n--- DECRYPTED CONTENT PREVIEW ---")
        print(decrypted_text[:500] + "...") # Print first 500 chars
        print("\n---------------------------------")
        print(f"[*] Full code saved to {output_file}")
        
    except UnicodeDecodeError:
        print("[!] Output is binary data, not text. Saving as binary...")
        with open("decoded_artifact.bin", "wb") as f:
            f.write(final_bytes)

if __name__ == "__main__":
    solve()
    