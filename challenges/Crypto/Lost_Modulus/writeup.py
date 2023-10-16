#!/usr/bin/env python3

from Crypto.Util.number import getPrime, long_to_bytes, inverse

if __name__ == '__main__':
    with open('output.txt', 'r') as file:
        key = file.read().split(' ')[1]
    key = int(key, 16)

    while True:
        p = getPrime(512)
        q = getPrime(512)
        n = p * q
        try:
            d = inverse(3, (p - 1) * (q - 1))
            break
        except:
            continue
    pt = pow(key, d, n)
    print(long_to_bytes(pt).decode())
