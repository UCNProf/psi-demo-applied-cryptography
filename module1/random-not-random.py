import random, time

current = time.time()
random.seed(current)

r1 = random.randrange(0, 65534)
random.seed(current)
r2 = random.randrange(0, 65534)

print(r1, r2)
