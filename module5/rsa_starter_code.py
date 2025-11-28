"""
RSA starter code

Uses the Cryptography module in Python to encrypt and decrypt data using RSA

Generates private and public keys and saves them in separate PEM files
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Generate private RSA key
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Generate public RSA key
public_key = private_key.public_key()

# Save private RSA key in file
with open("rsa_private_key.pem", "wb") as rsa_file:
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    rsa_file.write(pem)

# Save public RSA key in file
with open("rsa_public_key.pem", "wb") as rsa_file:
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    rsa_file.write(pem)

# Reset keys
public_key = None
private_key = None

# Load public RSA key from file
with open("rsa_public_key.pem", "rb") as rsa_file:
    pem = rsa_file.read()
    public_key = serialization.load_pem_public_key(pem)

# Load private RSA key from file
with open("rsa_private_key.pem", "rb") as rsa_file:
    pem = rsa_file.read()
    private_key = serialization.load_pem_private_key(pem, password=None)

# Encryption
plaintext = b'Hello world' * 15 

ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Ciphertext:", ciphertext.hex())

# Decryption
decrypted_plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Decrypted plaintext:", decrypted_plaintext.decode())