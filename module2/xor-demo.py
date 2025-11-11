m = 0b0110; 
k = 0b1101; 

c = m ^ k; 

print(f'Ciphertext: {c:04b}') # outputs: 0b1011

p = c ^ k;

print(f'Plaintext: {p:04b}') # outputs: 0b0110