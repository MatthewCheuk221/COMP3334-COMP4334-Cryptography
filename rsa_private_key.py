import math

def prime_factors(n):
    """Return distinct prime factors of n."""
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


def extended_gcd(a, b):
    """Extended Euclidean Algorithm. Returns (gcd, x, y) where ax + by = gcd."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e, phi):
    """Return d such that (e * d) % phi == 1, or None if no inverse exists."""
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        return None
    return x % phi


def find_p_and_q(n):
    """Factor n = p * q (assumes n is product of two primes)."""
    factors = prime_factors(n)
    if len(factors) == 2:
        return factors[0], factors[1]
    if len(factors) == 1:
        p = factors[0]
        return p, n // p
    return None, None


def compute_private_key(n, e):
    """Given n and e, compute d (private exponent)."""
    p, q = find_p_and_q(n)
    if p is None or q is None:
        return None, "Could not factor n into two primes"

    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    if d is None:
        return None, "e has no modular inverse modulo phi(n)"

    return d, {"p": p, "q": q, "phi": phi}


# ---------- interactive mode -------------------------------------------------

def prompt():
    print("=== RSA Private Key Calculator (d from n and e) ===")
    try:
        n = int(input("n = "))
        e = int(input("e = "))

        d, info = compute_private_key(n, e)

        if d is not None:
            print(f"\np = {info['p']}, q = {info['q']}")
            print(f"phi(n) = {info['phi']}")
            print(f"\nTherefore, d = {d}")
        else:
            print(f"\nError: {info}")

    except ValueError:
        print("Please enter valid integers.")


if __name__ == "__main__":
    prompt()
