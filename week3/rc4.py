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

key = "SECRET"
message = "Hello Cryptography"

encrypted = rc4(key, message)
decrypted = rc4(key, encrypted)

print("=== RC4 Stream Cipher ===")
print("Key:      ", key)
print("Original: ", message)
print("Encrypted:", encrypted.encode())
print("Decrypted:", decrypted)