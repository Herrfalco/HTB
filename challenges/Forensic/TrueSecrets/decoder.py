#!/usr/bin/env python3

from Crypto.Cipher import DES
from base64 import b64decode
import os, re

KEY = b'AKaPdSgV'
IV = b'QeThWmYq'

def get_enc_files(path):
    paths = []
    for path, _, files in os.walk(path):
        for file in {file for file in files if file[-4:] == '.enc'}:
            paths.append(path + '/' + file)
    return paths

if __name__ == '__main__':
    cypher = DES.new(KEY, DES.MODE_CBC)
    files = get_enc_files('.')
    for f in files:
        with open(f, 'r') as file:
            for line in file:
                match = re.search(b'HTB{.+}', \
                        cypher.decrypt(b64decode(bytes(line[:-1], 'utf-8'))))
                if match:
                    print(match[0].decode('utf-8'))
