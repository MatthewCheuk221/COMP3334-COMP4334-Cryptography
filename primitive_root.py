"""
primitive_roots.py
A pure math number theory utility (math module only).

Focused on primitive roots, multiplicative orders, and Euler's totient.
No argparse, sys, or other modules — just math + built-in input().

Canonical output: primitive roots lists are always returned sorted.
"""

import math
from typing import List, Optional


# =============================================================================
#                              HELPER FUNCTIONS
# =============================================================================

def prime_factors(n: int) -> List[int]:
    """
    Return the distinct prime factors of n (no multiplicities).
    Runs in O(√n) time.
    """
    if n <= 1:
        return []
    factors: List[int] = []
    # factor 2
    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2
    # odd factors
    p = 3
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 2
    if n > 1:
        factors.append(n)
    return factors


def euler_totient(n: int) -> int:
    """
    Euler's totient function ϕ(n).
    Runs in O(√n) using trial division.
    """
    if n <= 0:
        return 0
    result = n
    for p in prime_factors(n):
        result -= result // p
    return result


def has_primitive_root(n: int) -> bool:
    """
    Return True iff primitive roots exist modulo n.

    Primitive roots exist precisely when n is one of:
        2, 4, p^k, or 2·p^k   (p odd prime, k ≥ 1)
    """
    if n in (2, 4):
        return True
    if n <= 1:
        return False
    # remove all factors of 2
    while n % 2 == 0:
        n //= 2
    # remaining part must be a power of exactly one odd prime
    return len(prime_factors(n)) == 1


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


# =============================================================================
#                        MULTIPLICATIVE ORDER & PRIMITIVE ROOTS
# =============================================================================

def multiplicative_order(a: int, n: int) -> Optional[int]:
    """
    Return the multiplicative order of a modulo n,
    i.e. the smallest positive integer k such that a^k ≡ 1 (mod n).

    Returns None if gcd(a, n) != 1 (i.e. a is not invertible mod n).
    """
    if n <= 1:
        return None
    if math.gcd(a, n) != 1:
        return None

    phi = euler_totient(n)
    order = phi
    for p in prime_factors(phi):
        while order % p == 0 and pow(a, order // p, n) == 1:
            order //= p
    return order


def is_primitive_root(a: int, n: int) -> bool:
    """
    Return True if a is a primitive root modulo n
    (i.e. the order of a modulo n equals ϕ(n)).
    """
    if n <= 1 or math.gcd(a, n) != 1:
        return False
    phi = euler_totient(n)
    return multiplicative_order(a, n) == phi


def find_one_primitive_root(n: int) -> Optional[int]:
    """
    Return a single primitive root modulo n (the smallest one found),
    or None if no primitive root exists.
    """
    if not has_primitive_root(n):
        return None
    if n == 2:
        return 1          # 1 is a primitive root mod 2 (order 1 == ϕ(2))
    phi = euler_totient(n)
    pf = prime_factors(phi)
    for a in range(2, n):
        if math.gcd(a, n) != 1:
            continue
        if all(pow(a, phi // q, n) != 1 for q in pf):
            return a
    return None


def primitive_roots(n: int) -> List[int]:
    """
    Return *all* primitive roots modulo n as a sorted list
    (canonical / ascending order). Returns [] if none exist.
    """
    g = find_one_primitive_root(n)
    if g is None:
        return []
    if n == 2:
        return [1]
    phi = euler_totient(n)
    roots: List[int] = []
    for k in range(1, phi):
        if math.gcd(k, phi) == 1:
            roots.append(pow(g, k, n))
    return sorted(roots)


# =============================================================================
#                               CLI / MAIN
# =============================================================================

def process_n(n: int) -> None:
    """Pretty-print information about primitive roots and order for a given n."""
    print(f"\n{'='*60}")
    print(f"n = {n}")
    print(f"ϕ(n) = {euler_totient(n)}")
    print(f"Has primitive root: {'Yes' if has_primitive_root(n) else 'No'}")

    g = find_one_primitive_root(n)
    if g is not None:
        print(f"One primitive root (smallest found): {g}")
        roots = primitive_roots(n)
        print(f"All primitive roots (canonical): {roots}")
        print(f"Number of primitive roots: {len(roots)}  (= ϕ(ϕ(n)) = {euler_totient(euler_totient(n))})")
    else:
        print("No primitive roots exist for this modulus.")

    # Bonus: show a couple of orders if n is small
    if 2 <= n <= 100:
        print("\nSample multiplicative orders (a coprime to n):")
        shown = 0
        for a in range(1, n):
            if math.gcd(a, n) == 1:
                ord_a = multiplicative_order(a, n)
                print(f"  order({a:>3} mod {n}) = {ord_a}")
                shown += 1
                if shown >= 6:
                    break
    print('='*60 + "\n")


def prompt() -> None:
    """Simple interactive prompt — input the number after running the script."""
    print("=== Primitive Roots Utility ===")
    print("Enter a positive integer n (type q to quit)\n")
    while True:
        try:
            user_input = input("n = ").strip().lower()
            if user_input in ("q", "quit", "exit", ""):
                print("Goodbye!")
                break
            n = int(user_input)
            if n < 1:
                print("Please enter n ≥ 1")
                continue
            process_n(n)
        except ValueError:
            print("Please enter a valid integer (or q to quit)")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    prompt()
