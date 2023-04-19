import binascii

def isuint32(i):
    return isinstance(i, int) and abs(i) == i and i < 0xFFFFFFFF

def asint32(i):
    return i & 0xFFFFFFFF

def fromstring(bytestring, byte_length):
    assert len(bytestring) % (byte_length) == 0
    for i in range(0, len(bytestring), byte_length):
        c = bytestring[i: i+byte_length]
        yield int.from_bytes(c, 'little')

def chacha20_wordtobyte(inp):
    x = inp.copy()
    def quarter_round(a, b, c, d):
        rotate = lambda v, c: asint32((asint32(v << c)) | (asint32(v >> (32 - c))))
        x[a] = asint32(x[a] + x[b])
        x[d] = asint32(rotate(x[d] ^ x[a], 16))
        x[c] = asint32(x[c] + x[d])
        x[b] = asint32(rotate(x[b] ^ x[c], 12))
        x[a] = asint32(x[a] + x[b])
        x[d] = asint32(rotate(x[d] ^ x[a], 8))
        x[c] = asint32(x[c] + x[d])
        x[b] = asint32(rotate(x[b] ^ x[c], 7))
    for i in range(10):
        quarter_round(0, 4,  8, 12)
        quarter_round(1, 5,  9, 13)
        quarter_round(2, 6, 10, 14)
        quarter_round(3, 7, 11, 15)
        quarter_round(0, 5, 10, 15)
        quarter_round(1, 6, 11, 12)
        quarter_round(2, 7,  8, 13)
        quarter_round(3, 4,  9, 14)
    for i in range(16):
        x[i] = asint32(x[i] + inp[i])
    x = [i for n in x for i in n.to_bytes(4, 'little')]
    return x

sigma = b"expand 32-byte k"

def keysetup(iv, key, counter = 0):
    assert isuint32(counter)
    key_arr =   list(fromstring(key,   4))
    nonce =    list(fromstring(iv,    4))
    const_arr = list(fromstring(sigma, 4))

    ctx = [0] * 16

    ctx[4] = key_arr[0]
    ctx[5] = key_arr[1]
    ctx[6] = key_arr[2]
    ctx[7] = key_arr[3]
    ctx[8] = key_arr[4]
    ctx[9] = key_arr[5]
    ctx[10] = key_arr[6]
    ctx[11] = key_arr[7]

    ctx[0] = const_arr[0]
    ctx[1] = const_arr[1]
    ctx[2] = const_arr[2]
    ctx[3] = const_arr[3]

    ctx[12] = counter
    ctx[13] = counter

    ctx[14] = nonce[0]
    ctx[15] = nonce[1]

    return ctx

def encrypt_bytes(ctx, m, byts):
    c = [0] * len(m)

    if byts == 0:
        return

    c_pos = 0
    m_pos = 0

    while True:
        output = chacha20_wordtobyte(ctx)
        ctx[12] = asint32(ctx[12] + 1)

        if ctx[12] == 0:
            ctx[13] = asint32(ctx[13] + 1)

        if byts <= 64:
            for i in range(byts):
                c[i + c_pos] = asint32(m[i + m_pos] ^ output[i])
            return c

        for i in range(64):
            c[i + c_pos] = asint32(m[i + m_pos] ^ output[i])

        byts  = asint32(byts  - 64)
        c_pos = asint32(c_pos + 64)
        m_pos = asint32(m_pos + 64)

def decrypt_bytes(ctx, c, byts):
    return encrypt_bytes(ctx, c, byts)

def to_string(c):
    c_str = ""
    for i in c:
        c_str += chr(i)
    return c_str

e_key = [
    b"00000000000000000000000000000000000000000000000000000000"
    b"00000000",
    b"00000000000000000000000000000000000000000000000000000000"
    b"00000000",
    b"00000000000000000000000000000000000000000000000000000000"
    b"00000000",
    b"00000000000000000000000000000000000000000000000000000000"
    b"00000000",
    b"00000000000000000000000000000000000000000000000000000000"
    b"00000000"
]

value = [
    b"0000000000000000",
    b"0000000000000001",
    b"0000000000000010",
    b"0000000000000011",
    b"0000000000000100"
]
def test_passes(i):
    key = binascii.unhexlify(e_key[i])
    iv = binascii.unhexlify(value[i])

    m = [0] * (100 // 2)
    ctx = keysetup(iv, key)
    c = encrypt_bytes(ctx, m, len(m))
    encrypted_str = binascii.hexlify(b''.join([int(x).to_bytes(1,'little') for x in c]))
    print("Output: "+str(encrypted_str))

def run_tests():
    amount_tests = len(value)

    for i in range(amount_tests):
        print("Input: "+str(value[i]))
        test_passes(i)

if __name__ == "__main__":
    run_tests()

