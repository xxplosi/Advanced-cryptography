from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

with open("Week5/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

message = b"Secure message using RSA encryption"

ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("=== RSA Public Key Encryption ===")
print("Original message:", message)
print("Encrypted (hex):", ciphertext.hex())
print("Encrypted size:", len(ciphertext), "bytes")

with open("Week5/encrypted_message.bin", "wb") as f:
    f.write(ciphertext)

print("Encrypted message saved to encrypted_message.bin")