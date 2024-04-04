from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime

p = getPrime(512)
q = getPrime(512)
e = 3
n = p*q
m = bytes_to_long(b"short message")
c = pow(m, e, n)

print(f"{n = }")
print(f"{c = }")
# notice from the prints above that c is considerably smaller than n, this, combined with the fact that e = 3(which is very small) means we can usually take the 3rd root to find m

m, check = iroot(c, e)
assert check
print("Recovered message:", long_to_bytes(m))

print()

# Second example where m^e is sliiiiightly larger than n, bruteforce k(read the slides for more details)
m = bytes_to_long(b"This message is exactly 43 characters long!") # on purpose because 43 characters -> 43*8 = 344 bits, when raised to e = 3, it will be roughly 1032 bits which is larger than the 1024 bits of the public modulus n
c = pow(m, e, n)
assert m**e > n
print(f"{c = }")
# this time c isn't smaller than n BUT c = m^3 - k*n   =>  m^3 = c + k*n, we'll try many values of k until we find the correct message
for k in range(10**7):
    m3 = c + k*n
    m, check = iroot(m3, e)
    if check: # when it's a perfect cube it's probably the correct message, that's why we break, we could also check that the length of the message is 43 characters after doing long_to_bytes() or that all characters are printable, in CTFs we usually just check that the message starts with the correct flag format (e.g. break when b"NH4CK{" in long_to_bytes(m))
        break
print("Recovered message:", long_to_bytes(m))
print(f"Correct {k = }")
