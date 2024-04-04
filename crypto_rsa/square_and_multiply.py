import time

def efficient_exp(base, exp, modulus= 0):
    q = base
    r = 1
    
    while exp > 0:
        begintime = time.time()
        if exp % 2 == 1:
            r *= q
            if modulus: r %= modulus
            time.sleep(0.00001)
        q *= q
        if modulus: q %= modulus
        time.sleep(0.00001)
        print(time.time() - begintime, exp % 2)
        exp >>= 1
    return r


base = 1337
exp = 31337
mod = 65537
print(efficient_exp(base, exp, mod))



