from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom

key = urandom(16)    # 128-bit key
nonce = urandom(16)  # CTR nonces er ofte 16 bytes i denne implementation

plaintext = b"HELLO WORLD"

cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Decrypt
cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
decryptor = cipher.decryptor()
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("Ciphertext:", ciphertext.hex())
print("Decrypted:", decrypted)