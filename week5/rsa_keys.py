from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("Week5/private_key.pem", "wb") as f:
    f.write(private_pem)

with open("Week5/public_key.pem", "wb") as f:
    f.write(public_pem)

print("=== RSA Key Pair Generation ===")
print("Key size: 2048 bits")
print("Public exponent: 65537")
print("\nPublic Key:")
print(public_pem.decode())
print("Private Key:")
print(private_pem.decode())
print("Keys saved to public_key.pem and private_key.pem")