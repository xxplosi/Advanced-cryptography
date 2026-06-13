S_BOX = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]

PERMUTATION = [2, 0, 3, 1, 6, 4, 7, 5, 10, 8, 11, 9, 14, 12, 15, 13]

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

def substitution(nibbles):
    return [S_BOX[n] for n in nibbles]

def permutation(nibbles):
    return [nibbles[PERMUTATION[i]] for i in range(len(nibbles))]

def spn_encrypt(plaintext):
    print("\n=== SPN Encryption Process ===")
    print("Plaintext:", plaintext)
    
    nibbles = text_to_nibbles(plaintext)
    print("As nibbles:", nibbles)
    
    after_sub = substitution(nibbles)
    print("After substitution:", after_sub)
    
    after_perm = permutation(after_sub)
    print("After permutation:", after_perm)
    
    ciphertext = ''.join([hex(n)[2:] for n in after_perm])
    print("Ciphertext (hex):", ciphertext)
    
    return after_perm

plaintext = input("Enter plaintext (must be 8 characters): ")
while len(plaintext) != 8:
    print("Error: Must be exactly 8 characters")
    plaintext = input("Enter plaintext (must be 8 characters): ")

spn_encrypt(plaintext)