from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time

def aes_encrypt(data, key, iv):
    padding_length = 16 - len(data) % 16
    padded = data + bytes([padding_length] * padding_length)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()

key = os.urandom(32)
iv = os.urandom(16)

small = os.urandom(1024)
medium = os.urandom(1024 * 100)
large = os.urandom(1024 * 1000)

print("=== AES Performance Testing ===")

start = time.time()
aes_encrypt(small, key, iv)
print("Small  (1KB)  :", round(time.time() - start, 6), "seconds")

start = time.time()
aes_encrypt(medium, key, iv)
print("Medium (100KB):", round(time.time() - start, 6), "seconds")

start = time.time()
aes_encrypt(large, key, iv)
print("Large  (1MB)  :", round(time.time() - start, 6), "seconds")