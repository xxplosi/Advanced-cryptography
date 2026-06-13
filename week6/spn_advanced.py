S_BOX = [
    9, 4, 10, 11, 13, 1, 8, 5,
    6, 2, 0, 3, 12, 14, 15, 7,
    3, 7, 15, 14, 12, 6, 11, 5,
    9, 0, 10, 4, 1, 13, 8, 2
]

PERMUTATION = [2, 0, 3, 1, 6, 4, 7, 5, 10, 8, 11, 9, 14, 12, 15, 13]

def text_to_nibbles(text):
    nibbles = []
    for char in text:
        byte = ord(char)
        nibbles.append((byte >> 4) & 0xF)
        nibbles.append(byte & 0xF)
    return nibbles

def substitution(nibbles):
    return [S_BOX[n % len(S_BOX)] for n in nibbles]

def permutation(nibbles):
    return [nibbles[PERMUTATION[i]] for i in range(len(nibbles))]

def key_mixing(nibbles, key_nibbles):
    return [n ^ k for n, k in zip(nibbles, key_nibbles * (len(nibbles) // len(key_nibbles) + 1))]

def spn_encrypt_rounds(plaintext, key, rounds):
    print("\n=== Advanced SPN Encryption ===")
    print("Plaintext:", plaintext)
    print("Key:", key)
    print("Rounds:", rounds)
    
    nibbles = text_to_nibbles(plaintext)
    key_nibbles = text_to_nibbles(key)
    
    for r in range(rounds):
        print(f"\n--- Round {r+1} ---")
        nibbles = key_mixing(nibbles, key_nibbles)
        print("After key mixing:", nibbles)
        nibbles = substitution(nibbles)
        print("After substitution:", nibbles)
        nibbles = permutation(nibbles)
        print("After permutation:", nibbles)
    
    ciphertext = ''.join([hex(n)[2:] for n in nibbles])
    print("\nFinal Ciphertext (hex):", ciphertext)
    return nibbles

def avalanche_effect(plaintext, key, rounds):
    print("\n=== Avalanche Effect Demonstration ===")
    
    plaintext2 = plaintext[:-1] + chr(ord(plaintext[-1]) + 1)
    print("Original plaintext:", plaintext)
    print("Modified plaintext:", plaintext2)
    
    ct1 = spn_encrypt_rounds(plaintext, key, rounds)
    ct2 = spn_encrypt_rounds(plaintext2, key, rounds)
    
    differences = sum(1 for a, b in zip(ct1, ct2) if a != b)
    print(f"\nDifferences in output: {differences} out of {len(ct1)} nibbles changed")
    print("Avalanche effect:", round(differences/len(ct1)*100, 2), "%")

plaintext = input("Enter plaintext (8 characters): ")
while len(plaintext) != 8:
    print("Error: Must be exactly 8 characters")
    plaintext = input("Enter plaintext (8 characters): ")

key = input("Enter key (4 characters): ")
while len(key) != 4:
    print("Error: Key must be exactly 4 characters")
    key = input("Enter key (4 characters): ")

rounds = int(input("Enter number of rounds (1-5): "))
while rounds < 1 or rounds > 5:
    print("Error: Rounds must be between 1 and 5")
    rounds = int(input("Enter number of rounds (1-5): "))

spn_encrypt_rounds(plaintext, key, rounds)
avalanche_effect(plaintext, key, rounds)