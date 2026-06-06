def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def get_valid_shift():
    while True:
        try:
            shift = int(input("Enter shift value (1-25): "))
            if 1 <= shift <= 25:
                return shift
            else:
                print("Error: Shift must be between 1 and 25")
        except ValueError:
            print("Error: Please enter a valid number")

def get_valid_key():
    while True:
        key = input("Enter keyword (letters only): ")
        if key.isalpha():
            return key
        else:
            print("Error: Key must contain letters only")

message = input("Enter your message: ")

print("\n=== Caesar Cipher ===")
shift = get_valid_shift()
caesar_enc = caesar_encrypt(message, shift)
caesar_dec = caesar_decrypt(caesar_enc, shift)
print("Original: ", message)
print("Encrypted:", caesar_enc)
print("Decrypted:", caesar_dec)

print("\n=== Vigenere Cipher ===")
key = get_valid_key()
vig_enc = vigenere_encrypt(message, key)
vig_dec = vigenere_decrypt(vig_enc, key)
print("Original: ", message)
print("Encrypted:", vig_enc)
print("Decrypted:", vig_dec)