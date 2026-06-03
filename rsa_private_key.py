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


def extended_gcd_steps(e, phi):
    """
    Extended Euclidean Algorithm that prints steps.
    Returns d such that (e * d) % phi == 1.
    """
    print("\n=== Extended Euclidean Algorithm Steps ===")
    print(f"{'t':>6} {'d':>6} {'e':>6} {'q':>6} {'c':>6} {'x':>6}")
    print("-" * 45)

    x = phi
    c = 0
    d = 1

    if x == 1:
        d = 0

    while e > 1:
        q = e // x
        t = x

        # Euclid step
        x = e % x
        e = t
        t = c

        # Update coefficients
        c = d - q * c
        d = t

        print(f"{t:6d} {d:6d} {e:6d} {q:6d} {c:6d} {x:6d}")

    # Make d positive
    if d < 0:
        d += phi

    print("-" * 45)
    return d


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
    d = extended_gcd_steps(e, phi)
    if (e * d) % phi != 1:
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
