from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time

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

def aes_encrypt(message):
    key = os.urandom(32)
    iv = os.urandom(16)
    data = message.encode()
    padding_length = 16 - len(data) % 16
    padded = data + bytes([padding_length] * padding_length)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return key, iv, ciphertext

def aes_decrypt(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    padding_length = decrypted_padded[-1]
    return decrypted_padded[:-padding_length].decode()

def rsa_encrypt(message):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return private_key, ciphertext

def rsa_decrypt(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()

while True:
    print("\n=== Secure Chat Simulator ===")
    print("Sender: Coco  |  Receiver: Mike")
    print("1. Caesar Cipher")
    print("2. Vigenere Cipher")
    print("3. RC4 Stream Cipher")
    print("4. AES Encryption")
    print("5. RSA Encryption")
    print("6. Exit")

    choice = input("\nSelect encryption method: ")

    if choice == "6":
        print("Exiting Secure Chat Simulator.")
        break

    message = input("Coco's message to Mike: ")

    if choice == "1":
        shift = int(input("Enter shift value (1-25): "))
        start = time.time()
        encrypted = caesar_encrypt(message, shift)
        decrypted = caesar_decrypt(encrypted, shift)
        duration = time.time() - start
        print("\n--- Caesar Cipher Results ---")
        print("Original: ", message)
        print("Encrypted:", encrypted)
        print("Decrypted:", decrypted)
        print("Time taken:", round(duration, 6), "seconds")

    elif choice == "2":
        key = input("Enter keyword: ")
        start = time.time()
        encrypted = vigenere_encrypt(message, key)
        decrypted = vigenere_decrypt(encrypted, key)
        duration = time.time() - start
        print("\n--- Vigenere Cipher Results ---")
        print("Original: ", message)
        print("Encrypted:", encrypted)
        print("Decrypted:", decrypted)
        print("Time taken:", round(duration, 6), "seconds")

    elif choice == "3":
        key = input("Enter RC4 key: ")
        start = time.time()
        encrypted = rc4(key, message)
        decrypted = rc4(key, encrypted)
        duration = time.time() - start
        print("\n--- RC4 Stream Cipher Results ---")
        print("Original: ", message)
        print("Encrypted:", encrypted.encode())
        print("Decrypted:", decrypted)
        print("Time taken:", round(duration, 6), "seconds")

    elif choice == "4":
        start = time.time()
        key, iv, encrypted = aes_encrypt(message)
        decrypted = aes_decrypt(key, iv, encrypted)
        duration = time.time() - start
        print("\n--- AES Encryption Results ---")
        print("Original: ", message)
        print("Encrypted:", encrypted.hex())
        print("Decrypted:", decrypted)
        print("Time taken:", round(duration, 6), "seconds")

    elif choice == "5":
        print("Generating RSA keys for Mike...")
        start = time.time()
        private_key, encrypted = rsa_encrypt(message)
        decrypted = rsa_decrypt(private_key, encrypted)
        duration = time.time() - start
        print("\n--- RSA Encryption Results ---")
        print("Original: ", message)
        print("Encrypted:", encrypted.hex()[:50], "...")
        print("Decrypted:", decrypted)
        print("Time taken:", round(duration, 6), "seconds")

    else:
        print("Invalid choice. Please select 1-6.")