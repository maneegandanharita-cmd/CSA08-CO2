import time

calls = 0

def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

def ways_redesigned(n):
    """Returns (answer, number_of_additions)."""
    prev, cur, additions = 1, 1, 0
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
        additions += 1
    return cur, additions

print("--- A. Diagnosis: how the work grows with n (original) ---")
prev_calls = None
for n in (10, 15, 20, 25, 30):
    calls = 0; t = time.perf_counter(); ways_naive(n); t = time.perf_counter() - t
    ratio = f"{calls / prev_calls:.2f}x" if prev_calls else "-"
    print(f"n={n:>2}  calls={calls:>8}  time={t:.4f} s   growth over previous row (5 steps more): {ratio}")
    prev_calls = calls

print("\n--- Repeated work inside ways_naive(30): how often is each sub-problem computed? ---")
from collections import Counter
seen = Counter()

def count_subproblems(n):
    seen[n] += 1
    if n > 1:
        count_subproblems(n - 1); count_subproblems(n - 2)

count_subproblems(20)
print("n=20 -> ways(1) computed", seen[1], "times, ways(2):", seen[2], ", ways(5):", seen[5], ", ways(10):", seen[10])
print("distinct sub-problems:", len(seen), "but total calls:", sum(seen.values()))

print("\n--- E. Original vs Redesigned (same inputs) ---")
print(f"{'n':>4} | {'orig calls':>10} | {'new additions':>13} | {'orig time (s)':>13} | {'new time (s)':>12} | same answer")
for n in (10, 20, 25, 30):
    calls = 0; t0 = time.perf_counter(); a = ways_naive(n); t_orig = time.perf_counter() - t0
    t1 = time.perf_counter(); b, adds = ways_redesigned(n); t_new = time.perf_counter() - t1
    print(f"{n:>4} | {calls:>10} | {adds:>13} | {t_orig:>13.6f} | {t_new:>12.8f} | {a == b}")

print("\nRedesign on larger inputs (original cannot finish / crashes):")
for n in (1000, 10000):
    t = time.perf_counter(); r, adds = ways_redesigned(n); t = time.perf_counter() - t
    print(f"n={n:>5}  additions={adds:>5}  time={t:.6f} s  digits in answer={len(str(r))}")

try:
    ways_naive(1000)
except RecursionError as err:
    print("original ways_naive(1000) ->", type(err).__name__)
