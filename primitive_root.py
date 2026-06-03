import math

# ---------- helpers ----------------------------------------------------------

def prime_factors(n):
    """Return the distinct prime factors of n (no multiplicities)."""
    factors = []
    if n % 2 == 0:
        factors.append(2)
        while n % 2 == 0:
            n //= 2
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


def euler_totient(n):
    """ϕ(n) – runs in O(√n) using trial division, math only."""
    if n <= 0:
        return 0
    result = n
    for p in prime_factors(n):
        result -= result // p
    return result


def has_primitive_root(n):
    if n in (2, 4):
        return True
    if n <= 1:
        return False
    while n % 2 == 0:
        n //= 2
    return len(prime_factors(n)) == 1


# ---------- main routines ----------------------------------------------------

def find_one_primitive_root(n):
    if not has_primitive_root(n):
        return None
    phi = euler_totient(n)
    pf = prime_factors(phi)
    for a in range(2, n):
        if math.gcd(a, n) != 1:
            continue
        if all(pow(a, phi // q, n) != 1 for q in pf):
            return a
    return None


def primitive_roots(n):
    """Return all primitive roots modulo n, sorted (canonical order)."""
    g = find_one_primitive_root(n)
    if g is None:
        return []
    if n == 2:
        return [1]
    phi = euler_totient(n)
    roots = []
    for k in range(1, phi):
        if math.gcd(k, phi) == 1:
            roots.append(pow(g, k, n))
    return sorted(roots)


# ---------- extra useful functions (still only math) -------------------------

def multiplicative_order(a, n):
    if n <= 1 or math.gcd(a, n) != 1:
        return None
    phi = euler_totient(n)
    order = phi
    for p in prime_factors(phi):
        while order % p == 0 and pow(a, order // p, n) == 1:
            order //= p
    return order


def is_primitive_root(a, n):
    return multiplicative_order(a, n) == euler_totient(n)


# ---------- interactive mode -------------------------------------------------

def process_n(n):
    print(f"\n{'='*60}")
    print(f"n = {n}")
    print(f"ϕ(n) = {euler_totient(n)}")
    print(f"Has primitive root: {'Yes' if has_primitive_root(n) else 'No'}")

    g = find_one_primitive_root(n)
    if g is not None:
        print(f"One primitive root: {g}")
        print(f"All primitive roots: {primitive_roots(n)}")
    else:
        print("No primitive roots exist.")
    print('='*60 + "\n")


def prompt():
    print("=== Primitive Roots (math only) ===")
    print("Enter n and press Enter (type q to quit)\n")
    while True:
        try:
            txt = input("n = ").strip().lower()
            if txt in ("q", "quit", "exit", ""):
                print("Goodbye!")
                break
            n = int(txt)
            if n < 1:
                print("n must be ≥ 1")
                continue
            process_n(n)
        except ValueError:
            print("Please enter a valid integer or q to quit.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    prompt()
