from binascii import hexlify
import random

# ----------  low-level helpers ----------

def rotl32(x: int, n: int) -> int:
    """Rotate a 32-bit integer x left by n bits."""
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

def quarter_round(a: int, b: int, c: int, d: int):
    """ChaCha20 quarter-round (ARX) – spec §2.1."""
    a = (a + b) & 0xffffffff;  d ^= a;  d = rotl32(d, 16)
    c = (c + d) & 0xffffffff;  b ^= c;  b = rotl32(b, 12)
    a = (a + b) & 0xffffffff;  d ^= a;  d = rotl32(d,  8)
    c = (c + d) & 0xffffffff;  b ^= c;  b = rotl32(b,  7)
    return a, b, c, d

# ----------  part (a): 5 test cases ----------

TEST_VECTORS = [
    # 1) RFC 8439 round-test vector
    (0x11111111, 0x01020304, 0x9B8D6F43, 0x01234567),
    # 2) all-zero input (should stay zero)
    (0x00000000, 0x00000000, 0x00000000, 0x00000000),
    # 3) small ascending integers
    (0x00000001, 0x00000002, 0x00000003, 0x00000004),
    # 4) quirky “dead-beef” values
    (0xDEADBEEF, 0xCAFEBABE, 0x8BADF00D, 0xFEEDFACE),
    # 5) all ones (0xFFFFFFFF)
    (0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF),
]

print("Quarter-round test-vectors:")
for idx, (a, b, c, d) in enumerate(TEST_VECTORS, 1):
    out = quarter_round(a, b, c, d)
    pretty_in  = ", ".join(f"0x{x:08x}" for x in (a, b, c, d))
    pretty_out = ", ".join(f"0x{x:08x}" for x in out)
    print(f"{idx}. in: [{pretty_in}]  →  out: [{pretty_out}]")
print()

# ----------  part (b): diffusion measurement ----------

def popcount(x: int) -> int:
    """Count 1-bits (works on any Python version)."""
    return bin(x & 0xffffffff).count("1")        # mask to 32 bits, count '1's

def hamming_distance128(q1, q2) -> int:
    """Hamming distance between two 4-word (128-bit) tuples."""
    diff_bits = 0
    for w1, w2 in zip(q1, q2):
        diff_bits += popcount(w1 ^ w2)
    return diff_bits

def diffusion_for_input(words):
    """Flip each of the 128 input bits once, average #changed output bits."""
    base_out = quarter_round(*words)
    total_diff = 0
    for bit in range(128):
        w = bit // 32;  pos = bit % 32
        flipped = list(words);  flipped[w] ^= (1 << pos)
        diff = hamming_distance128(base_out, quarter_round(*flipped))
        total_diff += diff
    return total_diff / 128

random.seed(0)
sample = tuple(random.getrandbits(32) for _ in range(4))
avg_diff = diffusion_for_input(sample)
print(f"Diffusion experiment on random sample {sample}:")
print(f"  average changed output-bits per 1-bit input flip ≈ {avg_diff:.2f} / 128\n")

# ----------  complete ChaCha20 encrypt / decrypt ----------

CONST = (0x61707865, 0x3320646e, 0x79622d32, 0x6b206574)  # "expand 32-byte k"

def chacha20_block(key: bytes, counter: int, nonce: bytes) -> bytes:
    assert len(key) == 32 and len(nonce) == 12
    state = list(CONST) \
          + [int.from_bytes(key[i:i+4], "little") for i in range(0, 32, 4)] \
          + [counter & 0xffffffff] \
          + [int.from_bytes(nonce[i:i+4], "little") for i in range(0, 12, 4)]

    working = state.copy()
    for _ in range(10):                         # 20 rounds = 10 double-rounds
        # odd round (column)
        working[0], working[4], working[ 8], working[12] = quarter_round(working[0], working[4], working[ 8], working[12])
        working[1], working[5], working[ 9], working[13] = quarter_round(working[1], working[5], working[ 9], working[13])
        working[2], working[6], working[10], working[14] = quarter_round(working[2], working[6], working[10], working[14])
        working[3], working[7], working[11], working[15] = quarter_round(working[3], working[7], working[11], working[15])
        # even round (diagonal)
        working[0], working[5], working[10], working[15] = quarter_round(working[0], working[5], working[10], working[15])
        working[1], working[6], working[11], working[12] = quarter_round(working[1], working[6], working[11], working[12])
        working[2], working[7], working[ 8], working[13] = quarter_round(working[2], working[7], working[ 8], working[13])
        working[3], working[4], working[ 9], working[14] = quarter_round(working[3], working[4], working[ 9], working[14])

    out_words = [(w + s) & 0xffffffff for w, s in zip(working, state)]
    return b"".join(w.to_bytes(4, "little") for w in out_words)

def chacha20_crypt(key: bytes, nonce: bytes, counter: int, data: bytes) -> bytes:
    """Encrypt *or* decrypt – XOR with keystream."""
    keystream_off = 0
    result = bytearray()
    while data:
        ks_block = chacha20_block(key, counter, nonce)
        block = data[:64]
        result += bytes(b ^ ks for b, ks in zip(block, ks_block))
        data = data[64:]
        counter += 1
    return bytes(result)

# Quick round-trip sanity check (RFC 8439 vector counter = 1)
key   = bytes.fromhex("000102030405060708090a0b0c0d0e0f"
                      "101112131415161718191a1b1c1d1e1f")
nonce = bytes.fromhex("000000090000004a00000000")
msg   = b"Hello ChaCha20!"
ct    = chacha20_crypt(key, nonce, 1, msg)
pt    = chacha20_crypt(key, nonce, 1, ct)
print("Stream-cipher demo:")
print("  ciphertext :", hexlify(ct).decode())
print("  decrypted  :", pt.decode())

ciphertext = chacha20_crypt(key, nonce, counter=0, data=b"plaintext")
plaintext_back = chacha20_crypt(key, nonce, counter=0, data=ciphertext)

print("  ciphertext :", hexlify(ciphertext).decode())
print("  decrypted  :", plaintext_back.decode())
