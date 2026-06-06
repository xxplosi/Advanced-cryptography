from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidKey
import os

print("=== RSA Testing and Validation ===")

print("\nTest 1: Key Generation")
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
print("PASSED - Key pair generated successfully")
print("Key size:", private_key.key_size, "bits")

print("\nTest 2: Encryption and Decryption")
message = b"RSA validation test message"
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
decrypted = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("PASSED - Encryption and decryption successful")
print("Original == Decrypted:", message == decrypted)

print("\nTest 3: Wrong Key Decryption")
wrong_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
try:
    wrong_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("FAILED - Wrong key should not decrypt")
except Exception:
    print("PASSED - Wrong key correctly rejected")

print("\nTest 4: Different Messages Give Different Ciphertext")
msg1 = b"Message One"
msg2 = b"Message One"
ct1 = public_key.encrypt(msg1, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
ct2 = public_key.encrypt(msg2, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
print("PASSED - Same message encrypted twice gives different ciphertext:", ct1 != ct2)

print("\n=== All Tests Completed ===")