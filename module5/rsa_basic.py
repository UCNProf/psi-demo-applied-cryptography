n = 2537
e = 13
d = 937

c = 988

# Decrypt the ciphertext
m = pow(c, d, n)
print("Decrypted message:", m)

# Encrypt the message again to verify
c_verify = pow(m, e, n)
print("Re-encrypted message:", c_verify) # It should equal m1 * m2 mod n