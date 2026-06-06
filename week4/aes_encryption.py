from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(32)
iv = os.urandom(16)

print("=== AES Key Generation ===")
print("Key (hex):", key.hex())
print("IV  (hex):", iv.hex())
print("Key size:", len(key) * 8, "bits")

message = b"Hello AES Encryption"
padded = message + b" " * (16 - len(message) % 16)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded) + encryptor.finalize()

decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("\n=== AES Encryption ===")
print("Original: ", message)
print("Encrypted:", ciphertext.hex())
print("Decrypted:", decrypted.strip())