from Crypto.Cipher import AES # pycryptodome
from Crypto.Util.Padding import pad, unpad
import json
import os
from base64 import b64encode, b64decode

server_key = os.urandom(16) # 16 bytes = 128 bits -> 128-AES

def register(username, key):
    user_json = json.dumps({"admin": False, "username": f"{username}"}).encode()
    print(user_json, f"<- unpadded, unencrypted cookie, {len(user_json) = }")
    user_json = pad(user_json, 16) # 16 is the block size of AES
    print(user_json, f"<- padded, unencrypted cookie, {len(user_json) = }")
    
    # encrypt cookie and store client-side
    IV = os.urandom(16)
    aes = AES.new(key, AES.MODE_CBC, iv= IV)
    ciphertext = aes.encrypt(user_json)
    
    # return base64 encoded IV and ciphertext
    return b64encode(IV).decode() + "." + b64encode(ciphertext).decode() 
    
    
def login(cookie, key):
    # decode the base64 encoded IV, ciphertext
    IV, ciphertext = cookie.split('.')
    IV = b64decode(IV)
    ciphertext = b64decode(ciphertext)
    
    # decrypt cookie
    aes = AES.new(key, AES.MODE_CBC, iv= IV)
    user_json = aes.decrypt(ciphertext)
    
    # unpad
    user_json = unpad(user_json, 16)
    
    user_json = json.loads(user_json)
    if user_json["admin"]:
        print(f'Congrats you are admin, {user_json["username"]}!')
    else:
        print(f'Welcome {user_json["username"]}! You are just another normal user.')
    

def attack(cookie):
    # decode the base64 encoded IV, ciphertext
    IV, ciphertext = cookie.split('.')
    IV = b64decode(IV)
    ciphertext = b64decode(ciphertext)
    
    # the first 16 bytes of the plaintext:
    pt16      = b'{"admin": false,'
    desired16 = b'{"admin":  true,' # extra space between ":" and "true," so it's 16 bytes because "false" has 5 letter and "true" has 4
    
    # xor IV to change(predictably) the plaintext
    from pwn import xor # pwntools
    new_IV = xor(IV, xor(pt16, desired16))
    
    # encode again
    malicious_cookie = b64encode(new_IV).decode() + "." + b64encode(ciphertext).decode() 
    return malicious_cookie

    
user_cookie = register("Bobos", server_key)
print(user_cookie) # normal cookie


# login with normal cookie
print('\n[+] Logging in with "normal" cookie')
login(user_cookie, server_key)

# do bit flipping on cookie   
malicious_user_cookie = attack(user_cookie)
# login with malicious cookie
print('\n[+] Logging in with "tweaked" cookie')
login(malicious_user_cookie, server_key) 


