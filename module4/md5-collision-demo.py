import hashlib

for f in ["shattered-1.pdf", "shattered-2.pdf"]:
    data = open(f, "rb").read()
    print(f, hashlib.sha1(data).hexdigest(), hashlib.sha256(data).hexdigest())
