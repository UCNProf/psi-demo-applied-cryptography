"""
Simpel demo af anonym Diffie-Hellman key exchange.

Formål:
- Vise at Alice og Bob ender med den samme shared secret
- Illustrere at de aldrig sender deres hemmelige værdier over nettet
"""

import secrets

# Offentlige parametre (kendt af alle)
p = 23  # et lille primtal (i praksis meget større)
g = 5   # en generator i gruppen modulo p

print(f"Offentlige parametre: p = {p}, g = {g}")
print("-" * 50)

# Alice vælger en hemmelig værdi a
a = secrets.randbelow(p - 2) + 2  # vælg i [2, p-1]
A = pow(g, a, p)                  # A = g^a mod p

print("[Alice]")
print(f"  Hemmelig værdi a: {a}")
print(f"  Sender public value A = g^a mod p = {A} til Bob\n")

# Bob vælger en hemmelig værdi b
b = secrets.randbelow(p - 2) + 2  # vælg i [2, p-1]
B = pow(g, b, p)                  # B = g^b mod p

print("[Bob]")
print(f"  Hemmelig værdi b: {b}")
print(f"  Sender public value B = g^b mod p = {B} til Alice\n")

# Alice modtager B og beregner shared secret
shared_secret_alice = pow(B, a, p)  # s_A = B^a mod p

# Bob modtager A og beregner shared secret
shared_secret_bob = pow(A, b, p)    # s_B = A^b mod p

print("[Efter udveksling]")
print(f"  Alice' shared secret: {shared_secret_alice}")
print(f"  Bobs shared secret:   {shared_secret_bob}")
print()

if shared_secret_alice == shared_secret_bob:
    print("✅ Alice og Bob har den samme shared secret!")
else:
    print("❌ Noget gik galt – shared secrets matcher ikke.")
