"""
Demo: Length-extension attack på MD5

Idé:
- Serveren laver et token = MD5(secret || message)
- Angriberen kender *kun* message og token (ikke secret)
- Ved at udnytte MD5's Merkle–Damgård konstruktion kan angriberen
  beregne MD5(secret || message || padding || ekstraData)
  UDEN at kende secret.

Denne demo viser:
- Originalt request (som serveren ser det)
- Angribers forfalskede request med ekstra kommando
- At serverens check accepterer det forfalskede request
"""

from pymd5 import md5, padding  # sørg for at pymd5.py er tilgængelig
import binascii

# "Serverens" hemmelige nøgle – ukendt for angriberen
SECRET = b"super_secret_key"

# Den oprindelige besked, som både klient og angriber kender
ORIGINAL_MSG = b"user=lars&command=balance"

# Det angriberen vil tilføje
SUFFIX = b"&command=transferAll"


def server_token(message: bytes) -> str:
    """
    Simulerer serverens måde at lave token på:
    token = MD5(secret || message)
    """
    h = md5()
    h.update(SECRET + message)
    return h.hexdigest()


def server_accepts(message: bytes, token_hex: str) -> bool:
    """
    Serveren verificerer et request ved at genskabe token:
    check = MD5(secret || message)
    """
    h = md5()
    h.update(SECRET + message)
    return h.hexdigest() == token_hex


def demo_length_extension(secret_len_guess: int):
    print("=== LENGTH-EXTENSION DEMO (MD5) ===\n")

    # 1. Serveren laver oprindeligt token
    original_token = server_token(ORIGINAL_MSG)

    print("Original message (kendt af angriber):")
    print(ORIGINAL_MSG)
    print("\nOriginal token (kendt af angriber):")
    print(original_token)
    print()

    # Angriberen kender IKKE SECRET, men gætter dens længde
    # (her gætter vi korrekt for demoens skyld)
    print(f"Angriberens gæt på længden af secret: {secret_len_guess} bytes\n")

    # 2. Angriberen konstruerer padding for (secret || ORIGINAL_MSG)
    # MD5 bruger bit-længde i padding, derfor *8
    original_len_bits = (secret_len_guess + len(ORIGINAL_MSG)) * 8

    # padding() forventer længden i bits af det, der allerede er hashed
    pad = padding(original_len_bits)

    print("Padding (hex) for (secret || original_msg):")
    print(binascii.hexlify(pad))
    print()

    # 3. Angriberen starter MD5 i samme interne state som original_token
    #    og fortsætter med SUFFIX
    forged_md5 = md5(state=bytes.fromhex(original_token), count=original_len_bits + len(pad) * 8)
    forged_md5.update(SUFFIX)
    forged_token = forged_md5.hexdigest()

    # 4. Den forfalskede besked, som serveren ser
    forged_message = ORIGINAL_MSG + pad + SUFFIX

    print("Forfalsket (angribers) message som serveren vil se:")
    print(forged_message)
    print("\nForfalsket token (beregnet uden at kende SECRET):")
    print(forged_token)
    print()

    # 5. Tjek om serveren accepterer den forfalskede besked
    accepts = server_accepts(forged_message, forged_token)
    print("Accepterer serveren det forfalskede request?")
    print("==>", "JA ✅" if accepts else "NEJ ❌")


if __name__ == "__main__":
    # Til demo: vi ved at SECRET er 20 bytes lang (len(b"super_hemmelig_nøgle"))
    demo_length_extension(secret_len_guess=len(SECRET))
