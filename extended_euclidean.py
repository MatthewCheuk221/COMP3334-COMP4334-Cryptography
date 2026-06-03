import math

def extended_gcd_steps(a, b):
    """
    Extended Euclidean Algorithm with step-by-step table output.
    Same format as rsa_private_key.py (12 character columns).
    Returns d such that (a * d) % b == 1 (if it exists).
    """
    if b == 0:
        return None

    print(f"{'t':>12} {'d':>12} {'e':>12} {'q':>12} {'c':>12} {'x':>12}")
    print("-" * 77)

    # Initialize variables
    x = b          # modulus
    e = a          # we want inverse of a mod b
    c = 0
    d = 1

    if x == 1:
        d = 0

    while e > 1:
        q = e // x
        t = x

        # Euclid's algorithm step
        x = e % x
        e = t
        t = c

        # Update coefficients
        c = d - q * c
        d = t

        print(f"{t:12d} {d:12d} {e:12d} {q:12d} {c:12d} {x:12d}")

    # Make d positive
    if d < 0:
        d += b

    print("-" * 77)
    return d


# ---------- interactive mode -------------------------------------------------

def prompt():
    print("=== Extended Euclidean Algorithm (d from a and b) ===\n")
    try:
        a = int(input("a = "))
        b = int(input("b = "))

        print()

        d = extended_gcd_steps(a, b)

        if d is not None:
            if (a * d) % b == 1:
                print(f"\nd = a^(-1) mod b\n  = {a}^(-1) mod {b}\n  = {d}")
                print(f"\nVerification:\n({a} * {d}) mod {b} = {(a * d) % b}\n")
            else:
                print("\nNo modular inverse exists (gcd(a, b) != 1).")
        else:
            print("\nInvalid input (b cannot be 0).")

    except ValueError:
        print("Please enter valid integers.")


if __name__ == "__main__":
    prompt()
