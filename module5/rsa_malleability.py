n = 2537
e = 13
d = 937

m1 = 5
m2 = 7

# Encrypt the messages
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)

# Multiply the two ciphertexts
c_prod = (c1 * c2) % n

# Decrypt the product ciphertext
m_prod = pow(c_prod, d, n)

print("Decrypted product:", m_prod) # How does this relate to m1 and m2?