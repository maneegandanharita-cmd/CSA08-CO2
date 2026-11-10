def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    return text.strip().replace(" ", "").replace("-", "").upper()


def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    if len(reg) not in (9, 10):
        return False
    state, district = reg[:2], reg[2:4]
    series, number = reg[4:-4], reg[-4:]
    return (state.isalpha() and district.isdigit()
            and series.isalpha() and 1 <= len(series) <= 2
            and number.isdigit())


def format_plate(reg):
    """'TN09AB1234' -> 'TN 09 AB 1234' (only for a valid number)."""
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])


for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

print("\n--- Six designed inputs (predicted vs observed) ---")
cases = [("tn 09 ab 1234", True), ("TN-09-AB-1234", True), ("Tn09Ab1234", True),
         ("KA-01-M-0007", True), ("TN9AB1234", False), ("TN 09 ABC 1234", False)]
for raw, expected in cases:
    reg = normalise(raw)
    ok = is_valid(reg)
    receipt = format_plate(reg) if ok else "-"
    print(f"{raw:16} -> {reg:12} predicted={'valid' if expected else 'INVALID':7} observed={'valid' if ok else 'INVALID':7} receipt: {receipt}")

print("\n--- Immutability and slicing ---")
text = "tn09ab1234"
print("text.upper() ->", text.upper(), "| text is still ->", text)
try:
    text[0] = "T"
except TypeError as err:
    print("text[0] = 'T' ->", err)
for s in ("KA01M0007", "TN09AB1234"):
    print(f"{s} (len {len(s)}): s[-4:] = {s[-4:]!r}  s[4:-4] = {s[4:-4]!r}")


# ---------- Alternative: regular expression ----------
import re


def is_valid_regex(reg):
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg) is not None


same = all(is_valid(normalise(r)) == is_valid_regex(normalise(r)) for r, _ in cases)
print("\nRegex version gives the same answers on all six inputs:", same)
