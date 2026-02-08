import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def test_most_likely_scenario():
    """
    Based on analysis, the most likely scenario:
    - Uses ChaCha20 (32-byte key from 'expand 32-byte k' string)
    - Key is derived from '0123456789ABCDEFmodnarodsetybdet' (32 chars = 32 bytes as ASCII)
    - Or '4lpb1svfrzy98dcic58gw2zaw' might be an encoded version
    """
    
    print("=== Most Likely Decryption Scenario ===")
    
    # Candidate 1: The 32-char string as direct key
    key_candidate1 = "0123456789ABCDEFmodnarodsetybdet"
    print(f"\nCandidate 1 (direct 32-byte key):")
    print(f"  String: {key_candidate1}")
    print(f"  Length: {len(key_candidate1)} chars")
    print(f"  As bytes: {key_candidate1.encode()}")
    print(f"  Hex: {key_candidate1.encode().hex()}")
    
    # Candidate 2: The mysterious 26-char string
    key_candidate2 = "4lpb1svfrzy98dcic58gw2zaw"
    print(f"\nCandidate 2 (mystery string):")
    print(f"  String: {key_candidate2}")
    print(f"  Length: {len(key_candidate2)} chars")
    
    # Try to decode candidate2 as base32
    try:
        # Add padding for base32
        padded = key_candidate2.upper() + '=' * ((8 - len(key_candidate2) % 8) % 8)
        decoded_b32 = base64.b32decode(padded)
        print(f"  Base32 decode: {decoded_b32}")
        print(f"  Base32 hex: {decoded_b32.hex()}")
    except:
        print("  Not valid base32")
    
    # Try as base64
    try:
        decoded_b64 = base64.b64decode(key_candidate2 + '=' * ((4 - len(key_candidate2) % 4) % 4))
        print(f"  Base64 decode: {decoded_b64}")
        print(f"  Base64 hex: {decoded_b64.hex()}")
    except:
        print("  Not valid base64")
    
    # Candidate 3: Simple hex key
    key_candidate3 = "0123456789ABCDEF"
    print(f"\nCandidate 3 (simple hex, AES-128):")
    print(f"  String: {key_candidate3}")
    print(f"  As bytes: {bytes.fromhex(key_candidate3)}")
    
    # If we had a ciphertext, we would try:
    # 1. ChaCha20 with candidate1 as key (32 bytes)
    # 2. AES-128 with candidate3 as key (16 bytes)
    # 3. AES-256 with SHA256(candidate1) as key
    
    print("\n=== Decryption Approach ===")
    print("If you have an encrypted file:")
    print("1. Try ChaCha20 with key: '0123456789ABCDEFmodnarodsetybdet'")
    print("2. Try AES-128 with key: '0123456789ABCDEF'")
    print("3. The flag might be revealed after decryption")

def derive_key_from_system_info():
    """
    Ransomware often derives keys from system info.
    The strings 'GenuineII1', 'AuthentiL1', 'HygonGenL1' suggest
    checking CPU authenticity.
    """
    print("\n=== System-Based Key Derivation ===")
    
    # Common system info that might be used
    system_strings = [
        "GenuineIntel",
        "AuthenticAMD", 
        "HygonGenuine",
        "CPUInfo",
        "Hostname",
        "MachineID"
    ]
    
    for sys_str in system_strings:
        # Simple hash derivation
        key_sha256 = hashlib.sha256(sys_str.encode()).digest()
        print(f"\nSystem: {sys_str}")
        print(f"  SHA256 key (first 32): {key_sha256.hex()[:64]}")
        
        # For AES-128, take first 16 bytes
        aes128_key = key_sha256[:16]
        print(f"  AES-128 key: {aes128_key.hex()}")

if __name__ == "__main__":
    test_most_likely_scenario()
    derive_key_from_system_info()
    
    print("\n" + "="*60)
    print("SUMMARY: Without the actual encrypted files or binary,")
    print("we can only hypothesize. The most promising key is:")
    print("'0123456789ABCDEFmodnarodsetybdet' (32 bytes for ChaCha20)")
    print("or '0123456789ABCDEF' (16 bytes for AES-128)")
    print("\nThe flag format is likely 0DAY{...} based on the challenge.")
