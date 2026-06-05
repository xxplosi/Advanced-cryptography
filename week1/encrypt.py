from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

message = b"Hello Cryptography"
token = f.encrypt(message)
decrypted = f.decrypt(token)

print("Key:", key)
print("Encrypted:", token)
print("Decrypted:", decrypted)