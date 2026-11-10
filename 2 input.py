OTP = "4821"


# ---------- Design 1: while loop ----------
def verify_while(entries, otp=OTP, security_ok=False):
    attempts, pos, limit = 0, 0, 3
    while attempts < limit:
        if pos == len(entries):
            return ("Session ended - account not locked", attempts)
        entry = entries[pos].strip()
        pos += 1
        if entry == "":
            continue                        # blank entry: NOT counted as an attempt
        attempts += 1                       # counted only after the blank check
        if entry == otp:
            break                           # correct OTP: leave the loop
        elif not entry.isdigit():
            pass                            # placeholder: a 'digits only' warning can be added here later
        if attempts == limit and security_ok and limit == 3:
            limit = 5                       # changed condition: 2 extra attempts (given once)
    else:
        return ("LOCKED for 30 minutes", attempts)   # loop-else: runs only if no break
    return ("Verified", attempts)


# ---------- Design 1 with the counter in the WRONG place (bug) ----------
def verify_while_buggy(entries, otp=OTP):
    attempts, pos = 0, 0
    while attempts < 3 and pos < len(entries):
        entry = entries[pos].strip()
        pos += 1
        attempts += 1                       # BUG: counted before the blank check
        if entry == "":
            continue
        if entry == otp:
            return ("Verified", attempts)
    return ("LOCKED for 30 minutes", attempts)


# ---------- Design 2: for loop with range(3) ----------
def verify_for(entries, otp=OTP):
    pos = 0
    for attempt in range(1, 4):
        entry = ""
        while entry == "" and pos < len(entries):   # skip blanks without using an attempt
            entry = entries[pos].strip()
            pos += 1
        if entry == "":
            return ("Session ended - account not locked", attempt - 1)
        if entry == otp:
            break
    else:
        return ("LOCKED for 30 minutes", 3)
    return ("Verified", attempt)


# ---------- Alternative: recursion ----------
def verify_rec(entries, otp=OTP, pos=0, attempts=0, limit=3):
    if attempts == limit:
        return ("LOCKED for 30 minutes", attempts)
    if pos == len(entries):
        return ("Session ended - account not locked", attempts)
    entry = entries[pos].strip()
    if entry == "":
        return verify_rec(entries, otp, pos + 1, attempts, limit)
    if entry == otp:
        return ("Verified", attempts + 1)
    return verify_rec(entries, otp, pos + 1, attempts + 1, limit)


tests = {
    "correct on 3rd attempt":          ["1111", "", "2222", "4821"],
    "three wrong -> lock":             ["1", "2", "3"],
    "blanks first, correct 3rd":       ["", "", "1", "2", "4821"],
    "blank then 2 wrong (bug demo)":   ["", "1111", "2222", "4821"],
}

for name, e in tests.items():
    print(f"{name:32} while: {verify_while(e)}  | for: {verify_for(e)} | recursion: {verify_rec(e)}")

print("\nBuggy counter on 'blank then 2 wrong':", verify_while_buggy(tests["blank then 2 wrong (bug demo)"]))

print("\nChanged condition (security question answered correctly -> 2 extra attempts):")
e = ["1", "2", "3", "9", "4821"]
print("  4th wrong, 5th correct, security_ok=True :", verify_while(e, security_ok=True))
print("  same entries, security_ok=False          :", verify_while(e, security_ok=False))
print("  for-range(3) design cannot do this without changing range(3) itself")
