from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

with open("Week5/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("Week5/encrypted_message.bin", "rb") as f:
    ciphertext = f.read()

decrypted = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("=== RSA Private Key Decryption ===")
print("Encrypted (hex):", ciphertext.hex())
print("Decrypted message:", decrypted)
print("Decryption successful:", decrypted == b"Secure message using RSA encryption")