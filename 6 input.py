import sys
from functools import lru_cache

calls = 0

def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)

def ways_loop(n):
    prev, cur = 1, 1                        # ways(0), ways(1)
    for _ in range(2, n + 1):
        prev, cur = cur, prev + cur
    return cur

calls = 0; print("naive:", ways_naive(25), "calls =", calls)
ways_memo.cache_clear()
calls = 0; print("memo :", ways_memo(25), "calls =", calls)

print("\n--- Correctness check, n = 1..6 (hand: 1, 2, 3, 5, 8, 13) ---")
print([ways_naive(n) for n in range(1, 7)], [ways_loop(n) for n in range(1, 7)])

print("\n--- Call tree for n = 5 (indentation = depth) ---")
def tree(n, depth=0):
    print("  " * depth + f"ways({n})")
    if n > 1:
        tree(n - 1, depth + 1)
        tree(n - 2, depth + 1)
tree(5)

print("\n--- Growth investigation: number of function calls ---")
print(f"{'n':>3} | {'naive calls':>12} | {'memo calls':>10} | {'loop iterations':>15}")
for n in (10, 20, 25, 30):
    calls = 0; ways_naive(n); c_naive = calls
    ways_memo.cache_clear(); calls = 0; ways_memo(n); c_memo = calls
    print(f"{n:>3} | {c_naive:>12} | {c_memo:>10} | {max(n - 1, 0):>15}")

print("\n--- Deployment decision: n = 1000 ---")
print("sys.getrecursionlimit() =", sys.getrecursionlimit())
ways_memo.cache_clear()
try:
    ways_memo(1000)
except RecursionError as err:
    print("ways_memo(1000) ->", type(err).__name__, ":", err)

old = sys.getrecursionlimit()
sys.setrecursionlimit(3000)
ways_memo.cache_clear()
r_memo = ways_memo(1000)
sys.setrecursionlimit(old)
r_loop = ways_loop(1000)
print("after setrecursionlimit(3000), memo works; memo == loop:", r_memo == r_loop)
print("ways(1000) has", len(str(r_loop)), "digits; first 20 digits:", str(r_loop)[:20])
