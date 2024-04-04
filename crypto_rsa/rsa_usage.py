from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime # pip install pycryptodome


def RSA_keygen(bitsize, e= 65537):
    '''Generates an RSA public-private keypair with public modulus being "bitsize" bits in size'''
    p = getPrime(bitsize//2) # random primes of half the desired bitsize
    q = getPrime(bitsize//2)

    n = p*q
    public_key = (n, e)
    
    phi = (p - 1)*(q - 1) # φ(n), Euler's totient function
    d = pow(e, -1, phi)
    private_key = (n, d)
    
    return public_key, private_key

def RSA_encrypt(message: bytes, pubkey: tuple):
    n, e = pubkey
    m = bytes_to_long(message) # convert the message to a number
    assert m < n, "Message m has to be smaller than n when encrypting with RSA"
    
    c = pow(m, e, n)
    return c

def RSA_decrypt(c: int, privkey: tuple):
    n, d = privkey
    m = pow(c, d, n)
    
    message = long_to_bytes(m) # convert number back to bytes
    return message

# Example
my_public_key, my_private_key = RSA_keygen(2048)
msg = b"This is a small example" # note the "b" in front to denote it's encoded as bytes in python
c = RSA_encrypt(msg, my_public_key)
print(f"Encrypted: {c = }")
m = RSA_decrypt(c, my_private_key)
print(f"Decrypted: {m = }")
