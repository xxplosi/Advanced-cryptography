S_BOX = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]
INV_S_BOX = [10, 5, 9, 11, 1, 7, 8, 15, 6, 0, 2, 3, 12, 4, 13, 14]
PERMUTATION = [2, 0, 3, 1, 6, 4, 7, 5, 10, 8, 11, 9, 14, 12, 15, 13]
INV_PERMUTATION = [1, 3, 0, 2, 5, 7, 4, 6, 9, 11, 8, 10, 13, 15, 12, 14]

def text_to_nibbles(text):
    nibbles = []
    for char in text:
        byte = ord(char)
        nibbles.append((byte >> 4) & 0xF)
        nibbles.append(byte & 0xF)
    return nibbles

def nibbles_to_text(nibbles):
    result = ""
    for i in range(0, len(nibbles), 2):
        byte = (nibbles[i] << 4) | nibbles[i+1]
        result += chr(byte)
    return result

def key_mixing(nibbles, key_nibbles):
    extended_key = (key_nibbles * (len(nibbles) // len(key_nibbles) + 1))[:len(nibbles)]
    return [n ^ k for n, k in zip(nibbles, extended_key)]

def substitution(nibbles):
    return [S_BOX[n] for n in nibbles]

def inv_substitution(nibbles):
    return [INV_S_BOX[n] for n in nibbles]

def permutation(nibbles):
    return [nibbles[PERMUTATION[i]] for i in range(len(nibbles))]

def inv_permutation(nibbles):
    return [nibbles[INV_PERMUTATION[i]] for i in range(len(nibbles))]

def mini_aes_encrypt(plaintext, key, rounds):
    print("\n=== Mini AES Encryption ===")
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
        if r < rounds - 1:
            nibbles = permutation(nibbles)
            print("After permutation:", nibbles)

    nibbles = key_mixing(nibbles, key_nibbles)
    ciphertext = ''.join([hex(n)[2:] for n in nibbles])
    print("\nCiphertext (hex):", ciphertext)
    return nibbles

def mini_aes_decrypt(ciphertext_nibbles, key, rounds):
    print("\n=== Mini AES Decryption ===")

    nibbles = ciphertext_nibbles
    key_nibbles = text_to_nibbles(key)

    nibbles = key_mixing(nibbles, key_nibbles)

    for r in range(rounds - 1, -1, -1):
        print(f"\n--- Round {r+1} ---")
        if r < rounds - 1:
            nibbles = inv_permutation(nibbles)
            print("After inverse permutation:", nibbles)
        nibbles = inv_substitution(nibbles)
        print("After inverse substitution:", nibbles)
        nibbles = key_mixing(nibbles, key_nibbles)
        print("After key mixing:", nibbles)

    decrypted = nibbles_to_text(nibbles)
    print("\nDecrypted text:", decrypted)
    return decrypted

while True:
    print("\n=== Mini AES Simulator ===")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Exit")

    choice = input("\nSelect option: ")

    if choice == "3":
        print("Exiting Mini AES Simulator.")
        break

    elif choice == "1":
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
        ciphertext_nibbles = mini_aes_encrypt(plaintext, key, rounds)

    elif choice == "2":
        if 'ciphertext_nibbles' not in dir():
            print("Please encrypt a message first.")
        else:
            key = input("Enter key (4 characters): ")
            while len(key) != 4:
                print("Error: Key must be exactly 4 characters")
                key = input("Enter key (4 characters): ")
            rounds = int(input("Enter number of rounds (1-5): "))
            mini_aes_decrypt(ciphertext_nibbles, key, rounds)

    else:
        print("Invalid choice. Please select 1-3.")