# Demoen viser ChaCha20s følsomhed overfor små ændringer:

# Ændrer du ét tegn i plaintext, ændres kun én byte i ciphertext (stream cipher egenskab).
# Ændrer du én bit i nonce, ændres hele ciphertexten (100% af bytes ændret).
# Dette demonstrerer:

# ChaCha20 er en stream cipher: Små ændringer i plaintext påvirker kun tilsvarende bytes i ciphertext.
# Nonce/key er kritisk: En lille ændring i nonce eller key giver helt forskellig output (god sikkerhed).
# Round-trip dekryptering virker, og demoen illustrerer tydeligt effekten af små ændringer!

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# ChaCha20 kræver 32-byte key og 16-byte nonce
key = os.urandom(32)
nonce = os.urandom(16)

plaintext = b"Hello stream world!"
print(f"Key (hex):   {key.hex()}")
print(f"Nonce (hex): {nonce.hex()}")
print(f"Plaintext:   {plaintext}")

# Krypter med ChaCha20
cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext)
print(f"\nCiphertext (hex): {ciphertext.hex()}")

# Dekrypter
cipher2 = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
decryptor = cipher2.decryptor()
decrypted = decryptor.update(ciphertext)
print(f"Dekrypteret: {decrypted}")
print(f"Matcher original? {decrypted == plaintext}")

# Ændring i plaintext
plaintext2 = b"Hello stream world?"  # ændrer sidste tegn ! -> ?
cipher3 = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
encryptor3 = cipher3.encryptor()
ciphertext2 = encryptor3.update(plaintext2)
print(f"\nÆndret plaintext:   {plaintext2}")
print(f"Ændret ciphertext (hex): {ciphertext2.hex()}")

# Sammenlign ciphertexts
changed_bytes = sum(a != b for a, b in zip(ciphertext, ciphertext2))
print(f"\nAntal ændrede bytes i ciphertext: {changed_bytes} af {len(ciphertext)}")
print(f"Procent ændret: {changed_bytes/len(ciphertext)*100:.1f}%")

# Ændring i nonce
nonce2 = bytearray(nonce)
nonce2[0] ^= 1  # flip første bit
nonce2 = bytes(nonce2)
cipher4 = Cipher(algorithms.ChaCha20(key, nonce2), mode=None)
encryptor4 = cipher4.encryptor()
ciphertext3 = encryptor4.update(plaintext)
print(f"\nÆndret nonce: {nonce2.hex()}")
print(f"Ciphertext med ændret nonce (hex): {ciphertext3.hex()}")
changed_bytes_nonce = sum(a != b for a, b in zip(ciphertext, ciphertext3))
print(f"Antal ændrede bytes (nonce): {changed_bytes_nonce} af {len(ciphertext)}")
print(f"Procent ændret (nonce): {changed_bytes_nonce/len(ciphertext)*100:.1f}%")
