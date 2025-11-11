from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generér en 128-bit (16 byte) nøgle
key = os.urandom(16)
print(f"Nøgle (hex): {key.hex()}")

# Generér en 128-bit (16 byte) nonce til CTR mode
nonce = os.urandom(16)
print(f"Nonce (hex): {nonce.hex()}")

# Plaintext - kan være vilkårlig længde (ingen padding nødvendig i CTR mode)
plaintext = b"Hello block world"
print(f"\nPlaintext: {plaintext.decode()}")
print(f"Plaintext (hex): {plaintext.hex()}")
print(f"Plaintext længde: {len(plaintext)} bytes")

# Opret cipher objekt med AES i CTR mode
cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())

# Kryptering
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
print(f"\nCiphertext (hex): {ciphertext.hex()}")
print(f"Ciphertext længde: {len(ciphertext)} bytes")

# Dekryptering
cipher_decrypt = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
decryptor = cipher_decrypt.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()
print(f"\nDekrypteret: {decrypted.decode()}")
print(f"Dekrypteret (hex): {decrypted.hex()}")

# Verificer at det matcher
print(f"\nMatcher original? {plaintext == decrypted}")
print(f"\nNote: CTR mode kræver INGEN padding - output er samme længde som input!")
