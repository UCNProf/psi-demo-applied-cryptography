from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

key = urandom(32)    # 256-bit key
nonce = urandom(16)  # ChaCha20 nonce er 16 bytes i dette API

plaintext = b"HELLO WORLD"

cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext)

# Decrypt original ciphertext
cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext)

print("Ciphertext:", ciphertext.hex())
print("Decrypted (original):", decrypted)
