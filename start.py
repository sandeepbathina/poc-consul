#  Steps:

# 1. Grab Key from artifactory
# 2. store key in json file
# 3. start consul
# 4. encrypt key
# 5. store encrypted key in json file

import requests
import os
import subprocess
import json
from multiprocessing import Process
import time
# from binascii import hexlify,unhexlify
# from simplecrypt import encrypt, decrypt


# class obfuscation(object):
#     def __init__(self, ciphertext, duid):
#         self.ciphertext = ciphertext
#         self.duid = duid
#
#     def decrypt_token(self):
#         dehex = unhexlify(self.ciphertext)
#         plaintext = decrypt(self.duid, dehex)
#         return plaintext.rstrip()
#
#     def encrypt_token(self, text):
#         hex = encrypt(self.duid, text)
#         ciphertext = hexlify(self.ciphertext)
#         return ciphertext.rstrip()
def consul_start():
    # duid = requests.get('https://artifactory:443/artifactory/consul/pass.txt')
    encrypt_val = requests.get('https://artifactory:443/artifactory/consul/encrypt_key.txt')
    data = {}
    data['encrypt'] = encrypt_val.text
    with open('encrypt.json', 'w') as outfile:
        json.dump(data, outfile)
    f = open("/log/consul.log", "w")
    subprocess.call(["consul", "agent", "-config-dir", "/consul.d/", "-config-file", "encrypt.json"], stdout=f,stderr=f)

def encrypt_remove():
    time.sleep(3)
    if os.path.isfile('encrypt.json'):
        os.remove('encrypt.json')

def main():
    Process(target=consul_start).start()
    Process(target=encrypt_remove).start()
    # obf = obfuscation()
    # obf.encrypt_token()

if __name__ == '__main__':
    main()
