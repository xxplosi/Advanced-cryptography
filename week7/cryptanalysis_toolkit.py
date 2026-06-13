S_BOX = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]
PERMUTATION = [2, 0, 3, 1, 6, 4, 7, 5, 10, 8, 11, 9, 14, 12, 15, 13]

def text_to_nibbles(text):
    nibbles = []
    for char in text:
        byte = ord(char)
        nibbles.append((byte >> 4) & 0xF)
        nibbles.append(byte & 0xF)
    return nibbles

def spn_encrypt(plaintext):
    nibbles = text_to_nibbles(plaintext)
    nibbles = [S_BOX[n] for n in nibbles]
    nibbles = [nibbles[PERMUTATION[i]] for i in range(len(nibbles))]
    return nibbles

def compute_difference(b1, b2):
    return [a ^ b for a, b in zip(b1, b2)]

def frequency_analysis(nibbles):
    freq = {}
    for n in nibbles:
        freq[n] = freq.get(n, 0) + 1
    return freq

def statistical_bias(freq, total):
    expected = total / 16
    bias = {}
    for val in range(16):
        actual = freq.get(val, 0)
        bias[val] = round(abs(actual - expected) / expected * 100, 2)
    return bias

p1 = input("Enter first plaintext (8 characters): ")
while len(p1) != 8:
    print("Error: Must be exactly 8 characters")
    p1 = input("Enter first plaintext (8 characters): ")

p2 = input("Enter second plaintext (8 characters): ")
while len(p2) != 8:
    print("Error: Must be exactly 8 characters")
    p2 = input("Enter second plaintext (8 characters): ")

n1 = text_to_nibbles(p1)
n2 = text_to_nibbles(p2)
c1 = spn_encrypt(p1)
c2 = spn_encrypt(p2)

input_diff = compute_difference(n1, n2)
output_diff = compute_difference(c1, c2)

print("\n=== Mini Cryptanalysis Toolkit ===")

print("\n--- Input Difference ---")
print("Plaintext 1:", p1)
print("Plaintext 2:", p2)
print("Difference: ", input_diff)
print("Non-zero positions:", [i for i, d in enumerate(input_diff) if d != 0])

print("\n--- Frequency Analysis (Ciphertext 1) ---")
freq = frequency_analysis(c1)
for val in sorted(freq.keys()):
    bar = "#" * freq[val]
    print(f"Value {val:2d}: {bar} ({freq[val]})")

print("\n--- Statistical Bias ---")
bias = statistical_bias(freq, len(c1))
for val in range(16):
    print(f"Value {val:2d}: {bias[val]}% bias")

avg_bias = round(sum(bias.values()) / len(bias), 2)
print(f"\nAverage bias: {avg_bias}%")
if avg_bias < 20:
    print("Result: LOW bias — good randomness in ciphertext")
elif avg_bias < 50:
    print("Result: MODERATE bias — some patterns detectable")
else:
    print("Result: HIGH bias — cipher is statistically weak")

print("\n--- Output Difference ---")
print("Ciphertext 1:", c1)
print("Ciphertext 2:", c2)
print("Difference:  ", output_diff)
bits_changed = sum(bin(d).count('1') for d in output_diff)
total_bits = len(output_diff) * 4
print(f"Bits changed: {bits_changed} out of {total_bits} ({round(bits_changed/total_bits*100,2)}%)")