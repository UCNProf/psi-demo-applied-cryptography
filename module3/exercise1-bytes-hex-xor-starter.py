def xor_bytes(b1, b2):
    return bytes([x ^ y for x, y in zip(b1, b2)])

text = "HELLO WORLD".encode()
key = b"\xAA" * len(text)

cipher = xor_bytes(text, key)
plain = xor_bytes(cipher, key)

print("Plaintext:", text)
print("Ciphertext (hex):", cipher.hex())
print("Decrypted:", plain)