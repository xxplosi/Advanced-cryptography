S_BOX = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]
PERMUTATION = [2, 0, 3, 1, 6, 4, 7, 5, 10, 8, 11, 9, 14, 12, 15, 13]

def text_to_nibbles(text):
    nibbles = []
    for char in text:
        byte = ord(char)
        nibbles.append((byte >> 4) & 0xF)
        nibbles.append(byte & 0xF)
    return nibbles

def substitution(nibbles):
    return [S_BOX[n] for n in nibbles]

def permutation(nibbles):
    return [nibbles[PERMUTATION[i]] for i in range(len(nibbles))]

def spn_encrypt(plaintext):
    nibbles = text_to_nibbles(plaintext)
    nibbles = substitution(nibbles)
    nibbles = permutation(nibbles)
    return nibbles

def compute_difference(block1, block2):
    return [a ^ b for a, b in zip(block1, block2)]

def count_different_bits(diff):
    total = 0
    for d in diff:
        total += bin(d).count('1')
    return total

print("=== Differential Cryptanalysis Simulation ===")
print()

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

input_diff = compute_difference(n1, n2)
input_bits_different = count_different_bits(input_diff)

c1 = spn_encrypt(p1)
c2 = spn_encrypt(p2)

output_diff = compute_difference(c1, c2)
output_bits_different = count_different_bits(output_diff)

print()
print("=== Input Analysis ===")
print("Plaintext 1:      ", p1)
print("Plaintext 2:      ", p2)
print("Input nibbles 1:  ", n1)
print("Input nibbles 2:  ", n2)
print("Input difference: ", input_diff)
print("Bits different:   ", input_bits_different)

print()
print("=== Output Analysis ===")
print("Ciphertext 1:      ", c1)
print("Ciphertext 2:      ", c2)
print("Output difference: ", output_diff)
print("Bits different:    ", output_bits_different)

print()
print("=== Observations ===")
print("Input bits changed: ", input_bits_different)
print("Output bits changed:", output_bits_different)
avalanche = round(output_bits_different / (len(c1) * 4) * 100, 2)
print("Avalanche effect:  ", avalanche, "%")

if avalanche >= 45:
    print("Result: STRONG avalanche effect — cipher behaves securely")
elif avalanche >= 25:
    print("Result: MODERATE avalanche effect — cipher has some weakness")
else:
    print("Result: WEAK avalanche effect — cipher is vulnerable to differential attack")