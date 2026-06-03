import math

# ---------- helpers ----------------------------------------------------------

def prime_factors(n: int) -> list[int]:
    """Return the distinct prime factors of n (no multiplicities)."""
    factors = []
    # handle factor 2
    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2
    # handle odd factors
    p = 3
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 2
    if n > 1:                       # n itself is prime
        factors.append(n)
    return factors


def euler_totient(n: int) -> int:
    """ϕ(n) – runs in O(√n) using trial division, math only."""
    result = n
    for p in prime_factors(n):
        result -= result // p
    return result


def has_primitive_root(n: int) -> bool:
    """
    Primitive roots exist ⇔
        n is 2, 4, p^k or 2·p^k   for an odd prime p.
    """
    if n in (2, 4):
        return True
    # strip powers of two
    while n % 2 == 0:
        n //= 2
    # now n must be a power of one odd prime
    return len(prime_factors(n)) == 1


# ---------- main routines ----------------------------------------------------

def find_one_primitive_root(n: int) -> int | None:
    """
    Return a single primitive root modulo n,
    or None if no primitive root exists.
    """
    if not has_primitive_root(n):
        return None

    phi = euler_totient(n)
    pf = prime_factors(phi)           # prime divisors of ϕ(n)

    for a in range(2, n):
        if math.gcd(a, n) != 1:
            continue
        # a is a primitive root iff a^(phi/q) != 1 (mod n) for every q | phi
        if all(pow(a, phi // q, n) != 1 for q in pf):
            return a
    return None                       # should never happen when a root exists


def primitive_roots(n: int) -> list[int]:
    """
    Return *all* primitive roots modulo n (possibly empty list).
    """
    g = find_one_primitive_root(n)
    if g is None:
        return []

    phi = euler_totient(n)
    roots = []
    for k in range(1, phi):
        if math.gcd(k, phi) == 1:     # k must be coprime to ϕ(n)
            roots.append(pow(g, k, n))
    return roots
