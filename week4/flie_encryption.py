from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(32)
iv = os.urandom(16)

with open("Week4/secret.txt", "rb") as f:
    plaintext = f.read()

padding_length = 16 - len(plaintext) % 16
padded = plaintext + bytes([padding_length] * padding_length)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded) + encryptor.finalize()

with open("Week4/secret_encrypted.txt", "wb") as f:
    f.write(ciphertext)

print("=== File Encryption ===")
print("Original file contents:", plaintext)
print("File encrypted successfully")
print("Encrypted file size:", len(ciphertext), "bytes")
print("Key (hex):", key.hex())
print("IV  (hex):", iv.hex())

decryptor = cipher.decryptor()
decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
padding_length = decrypted_padded[-1]
decrypted = decrypted_padded[:-padding_length]

with open("Week4/secret_decrypted.txt", "wb") as f:
    f.write(decrypted)

print("\n=== File Decryption ===")
print("Decrypted file contents:", decrypted)
print("File decrypted successfully")