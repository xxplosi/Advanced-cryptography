from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

print("=== Secure Message Transmission ===")
print("Generating Mike's key pair...")

mike_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
mike_public_key = mike_private_key.public_key()
print("Mike's key pair generated successfully")

message = b"Hello Mike, this is Coco. This message is encrypted with your public key."

print("\nCoco is encrypting message with Mike's public key...")
ciphertext = mike_public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Message encrypted successfully")
print("Encrypted (hex):", ciphertext.hex()[:50], "...")

print("\nMike is decrypting message with his private key...")
decrypted = mike_private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("=== Transmission Results ===")
print("Original message :", message)
print("Decrypted message:", decrypted)
print("Transmission successful:", message == decrypted)