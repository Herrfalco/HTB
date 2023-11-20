#!/usr/bin/env python3

from pwn import *
from sympy.ntheory.modular import crt
from sympy.simplify.simplify import nthroot
from math import exp, log
from Crypto.Util.number import long_to_bytes
import sys, json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: writeup.py IP:PORT")
        exit(1)
    IP, PORT = sys.argv[1].split(':')
    data = []

    with remote(IP, PORT) as run:
        for _ in range(3):
            run.sendline(b'y')
            line = run.recvline()
            data.append(json.loads(line[line.find(b'{'):-1]))

    data = [{
        'm': x['time_capsule'],
        'n': x['pubkey'][0],
        'e': x['pubkey'][1]
        } for x in data]
    M = [int(x['n'], 16) for x in data]
    U = [int(x['m'], 16) for x in data]
    E = int(data[0]['e'], 10)
    print(long_to_bytes(nthroot(crt(M, U)[0], E)))
