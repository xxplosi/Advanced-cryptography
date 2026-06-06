import time

def lfsr(seed, taps, length):
    state = seed[:]
    sequence = []
    for _ in range(length):
        sequence.append(state[-1])
        new_bit = 0
        for tap in taps:
            new_bit ^= state[tap]
        state = [new_bit] + state[:-1]
    return sequence

def rc4(key, text):
    S = list(range(256))
    j = 0
    key_bytes = [ord(c) for c in key]
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = []
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ k))
    return ''.join(result)

print("=== Encryption Performance Results ===")

start = time.time()
lfsr([1,0,1,1], [0,3], 10000)
lfsr_time = time.time() - start
print("LFSR Time (10000 bits):", round(lfsr_time, 6), "seconds")

message = "Hello Cryptography" * 1000
start = time.time()
rc4("SECRET", message)
rc4_time = time.time() - start
print("RC4 Time (18000 chars):", round(rc4_time, 6), "seconds")

if rc4_time < lfsr_time:
    print("RC4 is faster than LFSR")
else:
    print("LFSR is faster than RC4")