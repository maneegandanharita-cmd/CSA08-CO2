import timeit


# ---------- Version 1: separate if statements (BUGGY - no lower bound) ----------
def subsidy_separate_buggy(units, ration_card, senior):
    result = []
    if units <= 100:
        result.append("FULL")
    if units <= 200 and ration_card:        # BUG: lower bound 101 is missing
        result.append("PARTIAL")
    if units > 200 and senior:
        result.append("SENIOR")
    if not result:
        result.append("NONE")
    return result


# ---------- Version 2: separate if statements with chained comparison (FIXED) ----------
def subsidy_separate_fixed(units, ration_card, senior):
    result = []
    if units <= 100:
        result.append("FULL")
    if 101 <= units <= 200 and ration_card:
        result.append("PARTIAL")
    if units > 200 and senior:
        result.append("SENIOR")
    if not result:
        result.append("NONE")
    return result


# ---------- Version 3: if - elif - else (exactly one result) ----------
def subsidy_elif(units, ration_card, senior):
    if units <= 100:
        return "FULL"
    elif 101 <= units <= 200 and ration_card:
        return "PARTIAL"
    elif units > 200 and senior:
        return "SENIOR"
    else:
        return "NONE"


# ---------- Alternative 1: match-case (Python 3.10+) ----------
def subsidy_match(units, ration_card, senior):
    match (units <= 100, 101 <= units <= 200, ration_card, senior):
        case (True, _, _, _):
            return "FULL"
        case (False, True, True, _):
            return "PARTIAL"
        case (False, False, _, True):
            return "SENIOR"
        case _:
            return "NONE"


# ---------- Alternative 2: table-driven (slabs) ----------
SLABS = [
    (100, lambda ration, senior: "FULL"),
    (200, lambda ration, senior: "PARTIAL" if ration else "NONE"),
    (float("inf"), lambda ration, senior: "SENIOR" if senior else "NONE"),
]


def subsidy_table(units, ration_card, senior):
    for limit, rule in SLABS:
        if units <= limit:
            return rule(ration_card, senior)


# ---------- Test: eight households including every boundary ----------
households = [  # (units, ration card, member above 80)
    (50, True, False), (100, False, False), (100, True, False), (101, True, False),
    (101, False, False), (200, True, False), (201, False, False), (201, False, True),
]
predicted = ["FULL", "FULL", "FULL", "PARTIAL", "NONE", "PARTIAL", "NONE", "SENIOR"]

print(f"{'units':>5} {'ration':>6} {'age>80':>6} | {'predicted':9} | {'buggy separate-if':22} | "
      f"{'fixed separate-if':18} | {'elif':7} | {'match':7} | {'table':7}")
for h, p in zip(households, predicted):
    print(f"{h[0]:>5} {str(h[1]):>6} {str(h[2]):>6} | {p:9} | {str(subsidy_separate_buggy(*h)):22} | "
          f"{str(subsidy_separate_fixed(*h)):18} | {subsidy_elif(*h):7} | {subsidy_match(*h):7} | {subsidy_table(*h):7}")

all_ok = all(subsidy_elif(*h) == p == subsidy_match(*h) == subsidy_table(*h)
             for h, p in zip(households, predicted))
print("elif / match / table agree with prediction:", all_ok)

# ---------- Time per decision ----------
print("\nTime for 200,000 decisions (units=250, last slab, worst case):")
for f in (subsidy_elif, subsidy_match, subsidy_table):
    t = timeit.timeit(lambda: f(250, False, True), number=200_000)
    print(f"{f.__name__:<15} {t:.4f} s")
