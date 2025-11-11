from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Demonstration: En ændring påvirker kun én blok (1/3 af ciphertexten)
print("\n" + "="*60)
print("DEMONSTRATION: ÆNDRING I ÉN BLOK")
print("="*60)

# Statisk 128-bit (16 byte) nøgle
key = b"0123456789abcdef"  # 16 bytes

# Original plaintext (3 blokke)
plaintext = b"Secret message: meet me here at the coffee shop!"
# Ændret plaintext - kun blok 3 ændres (coffee shop -> data center)
#plaintext = b"Secret message: meet me here at the data center!"
                                                   
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

print(f"\nPlaintext (hex): {plaintext.hex()}")
print(f"\nCiphertext (hex): {ciphertext.hex()}")

print(f"\nOriginal plaintext:")
print(f"Blok 1: {plaintext[0:16]}")
print(f"Blok 2: {plaintext[16:32]}")
print(f"Blok 3: {plaintext[32:48]}")

print(f"\nOriginal ciphertext (hex):")
print(f"Blok 1: {ciphertext[0:16].hex()}")
print(f"Blok 2: {ciphertext[16:32].hex()}")
print(f"Blok 3: {ciphertext[32:48].hex()}")

